#!/usr/bin/env python3
"""Run deterministic pre-browser QA for a Content Magic HTML artifact."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlparse


IGNORED_TEXT_TAGS = {"script", "style", "template", "noscript"}
INTERACTIVE_TAGS = {"a", "button"}
ASSET_ATTRIBUTES = {
    "audio": ("src",),
    "embed": ("src",),
    "iframe": ("src",),
    "img": ("src", "srcset"),
    "object": ("data",),
    "source": ("src", "srcset"),
    "video": ("src", "poster"),
}
PROVENANCE_TOKENS = {
    "media-caption",
    "page-citation",
    "partner-note",
    "partnership-context",
    "proof-label",
    "source-label",
    "source-note",
    "source-proof",
}
PROHIBITED_COMPOSITION_TOKENS = {"dek", "eyebrow", "kicker"}
SOURCE_PROOF_PATTERNS = {
    "brief_narration": re.compile(r"\b(?:the|this)\s+(?:partnership\s+)?brief\s+(?:says|frames|states|shows|explains)\b", re.I),
    "source_narration": re.compile(r"\b(?:the|this)\s+source\s+(?:says|frames|states|shows|explains)\b", re.I),
    "brief_page_label": re.compile(r"\b(?:partnership\s+)?brief\s*,?\s*page(?:s)?\s+\d+\b", re.I),
    "supplied_brief": re.compile(r"\bfrom\s+the\s+(?:supplied|partnership)\s+brief\b", re.I),
    "source_proof": re.compile(r"\bsource[- ]proof\b", re.I),
    "source_label": re.compile(r"\bsource\s*:\s*", re.I),
}
PRIVATE_PATH_PATTERNS = (
    re.compile(r"^file:", re.I),
    re.compile(r"^blob:", re.I),
    re.compile(r"(?:^|/)Users/"),
    re.compile(r"(?:^|/)tmp/"),
    re.compile(r"/var/folders/"),
    re.compile(r"^[A-Za-z]:\\Users\\", re.I),
)
PRIVATE_HOSTS = {"0.0.0.0", "127.0.0.1", "::1", "localhost"}
SIGNED_QUERY_KEYS = {
    "expires",
    "policy",
    "signature",
    "token",
    "x-amz-credential",
    "x-amz-expires",
    "x-amz-signature",
    "x-goog-credential",
    "x-goog-expires",
    "x-goog-signature",
}
CONTENT_ITEM_EXTENSIONS = {
    ".doc",
    ".docx",
    ".epub",
    ".mov",
    ".mp3",
    ".mp4",
    ".pdf",
    ".ppt",
    ".pptx",
    ".wav",
    ".xls",
    ".xlsx",
}


class ContentMagicParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ignored_depth = 0
        self.visible_text: list[str] = []
        self.images: list[dict[str, str]] = []
        self.links: list[dict[str, str]] = []
        self.assets: list[dict[str, str]] = []
        self.tokens: list[tuple[str, str]] = []
        self.interactive_stack: list[dict[str, Any]] = []
        self.interactives: list[dict[str, Any]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        attr_map = {key.lower(): value or "" for key, value in attrs}
        if tag in IGNORED_TEXT_TAGS:
            self.ignored_depth += 1

        for attribute in ("class", "id"):
            for token in re.split(r"\s+", attr_map.get(attribute, "").strip()):
                if token:
                    self.tokens.append((attribute, token.lower()))

        if tag == "img":
            self.images.append(attr_map)
        if tag == "a":
            self.links.append(attr_map)
        for attribute in ASSET_ATTRIBUTES.get(tag, ()):
            value = attr_map.get(attribute, "").strip()
            if not value:
                continue
            values = [value]
            if attribute == "srcset":
                values = [part.strip().split()[0] for part in value.split(",") if part.strip()]
            for item in values:
                self.assets.append({"tag": tag, "attribute": attribute, "url": item})

        role = attr_map.get("role", "").lower()
        if tag in INTERACTIVE_TAGS or role in {"button", "tab"}:
            self.interactive_stack.append({"tag": tag, "attrs": attr_map, "text": []})

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if self.interactive_stack and self.interactive_stack[-1]["tag"] == tag:
            self.interactives.append(self.interactive_stack.pop())
        if tag in IGNORED_TEXT_TAGS and self.ignored_depth:
            self.ignored_depth -= 1

    def handle_data(self, data: str) -> None:
        if not self.ignored_depth and data.strip():
            self.visible_text.append(data)
        for interactive in self.interactive_stack:
            interactive["text"].append(data)


def finding(code: str, message: str, **evidence: Any) -> dict[str, Any]:
    item: dict[str, Any] = {"code": code, "message": message}
    if evidence:
        item["evidence"] = evidence
    return item


def portable_asset_error(url: str) -> str | None:
    value = url.strip()
    if not value:
        return "asset URL is empty"
    if value.lower().startswith("data:"):
        return None
    if any(pattern.search(value) for pattern in PRIVATE_PATH_PATTERNS):
        return "asset uses a local, temporary, private, or session-only path"

    parsed = urlparse(value)
    if parsed.scheme.lower() != "https":
        return "asset must use embedded data or stable HTTPS delivery"
    hostname = (parsed.hostname or "").lower()
    if hostname in PRIVATE_HOSTS or hostname.endswith(".local"):
        return "asset uses a local or loopback host"
    query_keys = {key.lower() for key, _ in parse_qsl(parsed.query, keep_blank_values=True)}
    if query_keys & SIGNED_QUERY_KEYS:
        return "asset URL appears signed, tokenized, or expiring"
    return None


def normalize_text(parts: list[str]) -> str:
    return re.sub(r"\s+", " ", " ".join(parts)).strip()


def control_label(interactive: dict[str, Any]) -> str:
    attrs = interactive["attrs"]
    return normalize_text(
        [attrs.get("aria-label", ""), attrs.get("title", ""), *interactive["text"]]
    )


def validate_document(
    html_text: str,
    *,
    chapter_path: bool = False,
    public_fallback: str | None = None,
) -> dict[str, Any]:
    parser = ContentMagicParser()
    parser.feed(html_text)
    parser.close()

    errors: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    visible_text = normalize_text(parser.visible_text)

    if "\u2014" in visible_text:
        errors.append(finding("copy.em_dash", "Buyer-facing copy contains an em dash character."))

    for code, pattern in SOURCE_PROOF_PATTERNS.items():
        match = pattern.search(visible_text)
        if match:
            errors.append(
                finding(
                    f"copy.{code}",
                    "Buyer-facing copy narrates source evidence or exposes provenance.",
                    match=match.group(0),
                )
            )

    token_values = {token.replace("_", "-") for _, token in parser.tokens}
    provenance_matches = {
        token
        for token in token_values
        if any(token == marker or token.startswith(marker + "-") for marker in PROVENANCE_TOKENS)
    }
    for token in sorted(provenance_matches):
        errors.append(
            finding(
                "copy.provenance_token",
                "Buyer-facing markup contains a provenance or source-proof token.",
                token=token,
            )
        )
    for token in sorted(token_values & PROHIBITED_COMPOSITION_TOKENS):
        errors.append(
            finding(
                "design.prohibited_composition_token",
                "Markup contains an eyebrow, kicker, or dek composition token.",
                token=token,
            )
        )

    for image_index, image in enumerate(parser.images, start=1):
        if not image.get("alt", "").strip():
            errors.append(
                finding(
                    "asset.image_alt",
                    "Image is missing useful alt text.",
                    image_index=image_index,
                    src=image.get("src", "")[:160],
                )
            )

    for asset in parser.assets:
        issue = portable_asset_error(asset["url"])
        if issue:
            errors.append(
                finding(
                    "asset.nonportable",
                    issue,
                    tag=asset["tag"],
                    attribute=asset["attribute"],
                    url=asset["url"][:240],
                )
            )

    asset_counts = Counter(asset["url"] for asset in parser.assets if asset["tag"] == "img")
    for url, count in asset_counts.items():
        if count > 1:
            warnings.append(
                finding(
                    "asset.repeated_image",
                    "The same image source appears more than once. Confirm that dominant visuals are not duplicated without a progression purpose.",
                    occurrences=count,
                    url=url[:240],
                )
            )

    hrefs: set[str] = set()
    for link_index, link in enumerate(parser.links, start=1):
        href = link.get("href", "").strip()
        hrefs.add(href)
        if not href or href == "#" or href.lower().startswith(("javascript:", "file:")):
            errors.append(
                finding(
                    "link.dead_or_unsafe",
                    "Link is empty, placeholder-only, or unsafe.",
                    link_index=link_index,
                    href=href,
                )
            )
        parsed_href = urlparse(href)
        if Path(parsed_href.path).suffix.lower() in CONTENT_ITEM_EXTENSIONS or any(
            pattern.search(href) for pattern in PRIVATE_PATH_PATTERNS
        ):
            issue = portable_asset_error(href)
            if issue:
                errors.append(
                    finding(
                        "link.nonportable_content_item",
                        issue,
                        link_index=link_index,
                        href=href[:240],
                    )
                )
        if link.get("target", "").lower() == "_blank":
            rel_tokens = {part.lower() for part in link.get("rel", "").split()}
            if "noopener" not in rel_tokens:
                errors.append(
                    finding(
                        "link.noopener",
                        "New-tab link is missing rel=noopener.",
                        link_index=link_index,
                        href=href,
                    )
                )

    navigation_terms = {"back", "chapter", "forward", "next", "previous", "scroll"}
    for control_index, interactive in enumerate(parser.interactives, start=1):
        label = control_label(interactive)
        attrs = interactive["attrs"]
        if not label:
            errors.append(
                finding(
                    "interaction.unlabeled",
                    "Interactive control has no accessible text label.",
                    control_index=control_index,
                    tag=interactive["tag"],
                )
            )
            continue
        has_arrow = any(character in label for character in ("←", "→", "↑", "↓", "<", ">"))
        lower_label = label.lower()
        is_navigation = any(term in lower_label for term in navigation_terms)
        target = attrs.get("aria-controls", "") or attrs.get("data-content-target", "")
        if has_arrow and not is_navigation and not target:
            errors.append(
                finding(
                    "interaction.arrow_target",
                    "Directional content control must declare its changing target with aria-controls or data-content-target.",
                    control_index=control_index,
                    label=label,
                )
            )

    if re.search(r"transition\s*:\s*all\b", html_text, re.I):
        errors.append(
            finding(
                "motion.transition_all",
                "CSS uses transition: all instead of naming the changed properties.",
            )
        )
    has_motion = bool(re.search(r"@keyframes|\banimation(?:-name)?\s*:", html_text, re.I))
    if has_motion and "prefers-reduced-motion" not in html_text:
        errors.append(
            finding(
                "motion.reduced_motion",
                "Animated content is missing a prefers-reduced-motion fallback.",
            )
        )

    if chapter_path:
        for marker, code, message in (
            ("100dvh", "chapter.dynamic_viewport", "Chapter path is missing a 100dvh desktop stage marker."),
            ("aria-hidden", "chapter.hidden_state", "Chapter path is missing an aria-hidden state contract."),
            ("inert", "chapter.inert_state", "Chapter path is missing an inert state contract."),
            ("900px", "chapter.mobile_breakpoint", "Chapter path is missing the required 900px mobile-flow breakpoint marker."),
        ):
            if marker not in html_text:
                errors.append(finding(code, message))

    if public_fallback:
        parsed = urlparse(public_fallback)
        if parsed.scheme.lower() != "https" or not parsed.netloc:
            errors.append(
                finding(
                    "fallback.invalid_url",
                    "Approved public fallback must be an absolute HTTPS URL.",
                    url=public_fallback,
                )
            )
        matching_links = [link for link in parser.links if link.get("href", "").strip() == public_fallback]
        if not matching_links:
            errors.append(
                finding(
                    "fallback.missing",
                    "Approved public fallback URL is not present in the artifact.",
                    url=public_fallback,
                )
            )
        for link in matching_links:
            rel_tokens = {part.lower() for part in link.get("rel", "").split()}
            if link.get("target", "").lower() != "_blank" or "noopener" not in rel_tokens:
                errors.append(
                    finding(
                        "fallback.safe_new_tab",
                        "Public fallback must open in a safe new tab.",
                        url=public_fallback,
                    )
                )
        if matching_links and "flzAnalytic" not in html_text:
            errors.append(
                finding(
                    "fallback.analytics",
                    "Public fallback is present but no Folloze analytics marker was found.",
                    url=public_fallback,
                )
            )

    external_links = [href for href in hrefs if urlparse(href).scheme.lower() in {"http", "https"}]
    if external_links and "flzAnalytic" not in html_text:
        warnings.append(
            finding(
                "analytics.marker_missing",
                "External actions exist but no flzAnalytic marker was found. Confirm the current publishing analytics contract.",
                external_link_count=len(external_links),
            )
        )

    return {
        "pass": not errors,
        "errors": errors,
        "warnings": warnings,
        "counts": {
            "assets": len(parser.assets),
            "images": len(parser.images),
            "links": len(parser.links),
            "interactives": len(parser.interactives),
        },
        "runtime_checks_required": [
            "brand comparison at 1440x900 and 390x844",
            "compact-height fit at 1366x768",
            "interaction target fingerprint changes",
            "arrow direction matches target geometry",
            "image complete and natural dimensions in every state",
            "zero horizontal overflow",
            "zero page-authored console errors",
            "saved readback",
            "anonymous hosted verification after publish",
        ],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html", type=Path, help="Content Magic HTML artifact to validate")
    parser.add_argument("--chapter-path", action="store_true", help="Apply guided pinned-chapter static markers")
    parser.add_argument("--public-fallback", help="Approved authoritative public URL replacing an unavailable original file")
    parser.add_argument("--json-output", type=Path, help="Optional path for the JSON report")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        html_bytes = args.html.read_bytes()
    except OSError as exc:
        print(f"ERROR: cannot read {args.html}: {exc}", file=sys.stderr)
        return 2

    try:
        html_text = html_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        print(f"ERROR: {args.html} is not UTF-8: {exc}", file=sys.stderr)
        return 2

    report = validate_document(
        html_text,
        chapter_path=args.chapter_path,
        public_fallback=args.public_fallback,
    )
    report["artifact"] = str(args.html.resolve())
    report["artifact_sha256"] = hashlib.sha256(html_bytes).hexdigest()

    serialized = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(serialized, encoding="utf-8")
    print(serialized, end="")
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
