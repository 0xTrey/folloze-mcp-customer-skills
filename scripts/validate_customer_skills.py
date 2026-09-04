#!/usr/bin/env python3
"""Validate the public Folloze customer-skill bundle."""

from __future__ import annotations

import ast
import hashlib
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "skills-manifest.json"
SOURCE_LOCK_PATH = ROOT / "skills-source-lock.json"
REQUIRED_FOUNDATIONS = {"abm-strategist", "brand-harvester"}
REQUIRED_BRAND_FILES = {
    "SKILL.md",
    "agents/openai.yaml",
    "references/brand-harvest-cli.md",
    "scripts/brand_harvest.py",
}
HUPO_FIXTURE_PATHS = {
    "one_to_one": ROOT / "tests/fixtures/hupo/bofa-one-to-one.json",
    "industry": ROOT / "tests/fixtures/hupo/finserv-highspot-native.json",
}
REQUIRED_HARDENING_MARKERS = {
    "Skills/abm-strategist/SKILL.md": {
        "mcp_html",
        "mcp_template",
        "native_traditional",
        "references/builder-handoff-contract.md",
        "Repair mode carries approval forward",
    },
    "Skills/Folloze-One-To-One-Microsite-Builder/SKILL.md": {
        "build_mode: mcp_html",
        "account-substitution test",
        "top header",
        "decision-advancing interaction",
        "320px",
    },
    "Skills/Folloze-Industry-Campaign-Page-Builder/SKILL.md": {
        "native_traditional",
        "Custom Theme",
        "generic fallback",
        "exact-domain",
        "different logos",
        "CTA context",
    },
    "Skills/brand-harvester/SKILL.md": {
        "--require-logo target",
        "--target-logo-source",
        "asset_requirements.status",
        "effective rendered button-label styles",
        "theme_handoff",
    },
}
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
OPTIONAL_BRAND = re.compile(
    r"(?:use|run)\s+[`$]*brand-harvester[`]*\s+when available",
    re.IGNORECASE,
)


def load_json(path: Path, errors: list[str]) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"cannot read {path.relative_to(ROOT)}: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{path.relative_to(ROOT)}: expected a JSON object")
        return {}
    return value


def validate_hupo_fixtures(errors: list[str]) -> None:
    one_to_one = load_json(HUPO_FIXTURE_PATHS["one_to_one"], errors)
    industry = load_json(HUPO_FIXTURE_PATHS["industry"], errors)
    if not one_to_one or not industry:
        return

    total_boards = sum(
        int(item.get("board_count_contribution", 0))
        for item in (one_to_one, industry)
    )
    if total_boards != 2:
        errors.append(f"Hupo fixtures must describe exactly 2 boards, found {total_boards}")

    if one_to_one.get("build_mode") != "mcp_html":
        errors.append("Hupo Bank of America fixture must use build_mode mcp_html")
    if one_to_one.get("target_account") != "Bank of America":
        errors.append("Hupo one-to-one target must be Bank of America")
    account_scope = one_to_one.get("account_scope", {})
    if account_scope.get("parent_company") != "Bank of America":
        errors.append("Hupo one-to-one parent narrative must belong to Bank of America")
    if account_scope.get("supporting_business_units_may_own_primary_narrative") is not False:
        errors.append("Hupo supporting business units must not own the primary narrative")
    copy_contract = one_to_one.get("copy_contract", {})
    headline = str(copy_contract.get("headline") or "")
    primary_cta = str(copy_contract.get("primary_cta") or "")
    if "Bank of America" not in headline or "Bank of America" not in primary_cta:
        errors.append("Hupo one-to-one headline and primary CTA must name Bank of America")
    if re.search(r"[.!?:;]$", headline):
        errors.append("Hupo one-to-one headline must not use terminal punctuation")
    for field in (
        "parent_target_owns_headline",
        "parent_target_owns_primary_cta",
        "account_substitution_requires_rewrite",
        "leadership_audience",
    ):
        if copy_contract.get(field) is not True:
            errors.append(f"Hupo one-to-one copy contract requires {field}=true")
    header = one_to_one.get("header", {})
    if header.get("placement") != "top":
        errors.append("Hupo one-to-one co-branding must be in the top header")
    for role in ("vendor_logo", "target_logo"):
        logo = header.get(role, {})
        if logo.get("required") is not True or logo.get("official_asset_required") is not True:
            errors.append(f"Hupo one-to-one {role} must require an official asset")
    if set(header.get("required_viewports", [])) != {1440, 390, 320}:
        errors.append("Hupo one-to-one must verify 1440, 390, and 320 pixel viewports")
    interaction = one_to_one.get("signature_interaction", {})
    if interaction.get("type") not in {
        "calculator", "scenario_model", "diagnostic", "readiness_assessment",
        "maturity_score", "comparison", "role_path",
    }:
        errors.append("Hupo one-to-one requires a decision-advancing signature interaction")
    if interaction.get("unsupported_roi_claims_allowed") is not False:
        errors.append("Hupo one-to-one cannot allow unsupported ROI claims")
    composition = one_to_one.get("composition", {})
    if composition.get("minimum_distinct_composition_types", 0) < 3:
        errors.append("Hupo one-to-one requires at least 3 composition types")
    if composition.get("maximum_adjacent_equal_card_grids", 99) > 1:
        errors.append("Hupo one-to-one cannot allow consecutive equal-card grids")

    if industry.get("build_mode") != "native_traditional":
        errors.append("Hupo FinServ fixture must use build_mode native_traditional")
    if industry.get("incumbent") != "Highspot":
        errors.append("Hupo FinServ fixture must identify Highspot as the incumbent")
    industry_copy = industry.get("copy_contract", {})
    if "Highspot" not in str(industry_copy.get("headline") or ""):
        errors.append("Hupo FinServ first-viewport headline must name Highspot")
    if industry_copy.get("headline_terminal_punctuation") is not False:
        errors.append("Hupo FinServ headline must omit terminal punctuation")
    for field in (
        "incumbent_named_in_first_viewport",
        "different_mechanism_explained",
        "leadership_outcome_present",
    ):
        if industry_copy.get(field) is not True:
            errors.append(f"Hupo FinServ copy contract requires {field}=true")
    if industry_copy.get("unsupported_comparative_claims_allowed") is not False:
        errors.append("Hupo FinServ cannot allow unsupported comparative claims")
    if industry.get("native_content_required") is not True:
        errors.append("Hupo FinServ must require native content")
    if industry.get("html_final_substitute_allowed") is not False:
        errors.append("Hupo FinServ cannot allow HTML as the final substitute")
    theme = industry.get("theme", {})
    if theme.get("type") != "board_scoped_custom_theme" or theme.get("readback_required") is not True:
        errors.append("Hupo FinServ must require a board-scoped Custom Theme and readback")
    personalization = industry.get("personalization", {})
    if personalization.get("matching") != "exact_domain":
        errors.append("Hupo FinServ personalization must use exact-domain matching")
    if personalization.get("raw_domain_in_analytics") is not False:
        errors.append("Hupo FinServ analytics must not emit raw domains")
    variants = personalization.get("variants", [])
    expected_domains = {"fallback", "ubs.com", "allianz-trade.com"}
    actual_domains = {item.get("account_domain") for item in variants}
    if actual_domains != expected_domains:
        errors.append(
            f"Hupo FinServ variants must be {sorted(expected_domains)}, found {sorted(actual_domains)}"
        )
    content_sets: list[set[str]] = []
    for variant in variants:
        for field in (
            "recognition_logo", "hero_copy_key", "supporting_copy_key",
            "content_item_ids", "content_types", "cta_context",
        ):
            if not variant.get(field):
                errors.append(
                    f"Hupo FinServ variant {variant.get('variant_key')} is missing {field}"
                )
        if len(set(variant.get("content_types", []))) < 2:
            errors.append(
                f"Hupo FinServ variant {variant.get('variant_key')} needs at least 2 native content types"
            )
        content_sets.append(set(variant.get("content_item_ids", [])))
    for left_index, left in enumerate(content_sets):
        for right in content_sets[left_index + 1:]:
            if left & right:
                errors.append("Hupo FinServ personalized content sets must be disjoint")


def validate_hardening_markers(errors: list[str]) -> None:
    for relative_path, markers in REQUIRED_HARDENING_MARKERS.items():
        path = ROOT / relative_path
        if not path.is_file():
            errors.append(f"missing hardening target {relative_path}")
            continue
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                errors.append(f"{relative_path}: missing hardening marker {marker!r}")


def frontmatter_name(skill_file: Path) -> str | None:
    text = skill_file.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None
    _, frontmatter, _ = text.split("---", 2)
    match = re.search(r"^name:\s*(.+?)\s*$", frontmatter, re.MULTILINE)
    return match.group(1).strip("\"'") if match else None


def relative_link_errors(markdown_file: Path) -> list[str]:
    errors: list[str] = []
    text = markdown_file.read_text(encoding="utf-8")
    for target in MARKDOWN_LINK.findall(text):
        target = target.strip().split("#", 1)[0]
        if not target or re.match(r"^(?:https?://|mailto:)", target):
            continue
        resolved = (markdown_file.parent / target).resolve()
        if not resolved.exists():
            errors.append(
                f"{markdown_file.relative_to(ROOT)}: missing relative link target {target}"
            )
    return errors


def main() -> int:
    errors: list[str] = []

    try:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read {MANIFEST_PATH}: {exc}", file=sys.stderr)
        return 1

    manifest_foundations = set(manifest.get("required_foundations", []))
    if manifest_foundations != REQUIRED_FOUNDATIONS:
        errors.append(
            "manifest required_foundations must be exactly "
            f"{sorted(REQUIRED_FOUNDATIONS)}"
        )

    try:
        source_lock = json.loads(SOURCE_LOCK_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"cannot read {SOURCE_LOCK_PATH.name}: {exc}")
        source_lock = {}

    for source_name, source in source_lock.get("sources", {}).items():
        for relative_path, expected_hash in source.get("vendored_files", {}).items():
            vendored_file = ROOT / relative_path
            if not vendored_file.is_file():
                errors.append(f"{source_name}: missing locked file {relative_path}")
                continue
            actual_hash = hashlib.sha256(vendored_file.read_bytes()).hexdigest()
            if actual_hash != expected_hash:
                errors.append(
                    f"{source_name}: checksum drift for {relative_path}; "
                    "update the source lock with the intentional change"
                )

    skills = manifest.get("skills", [])
    names = {entry.get("name") for entry in skills}
    if len(names) != len(skills):
        errors.append("manifest skill names must be unique and non-empty")

    for entry in skills:
        name = entry.get("name")
        path_value = entry.get("path")
        if not name or not path_value:
            errors.append(f"manifest entry is missing name/path: {entry!r}")
            continue

        skill_dir = ROOT / path_value
        skill_file = skill_dir / "SKILL.md"
        agent_file = skill_dir / "agents/openai.yaml"
        if not skill_file.is_file():
            errors.append(f"{path_value}: missing SKILL.md")
            continue
        if not agent_file.is_file():
            errors.append(f"{path_value}: missing agents/openai.yaml")

        actual_name = frontmatter_name(skill_file)
        if actual_name != name:
            errors.append(
                f"{path_value}: frontmatter name {actual_name!r} != manifest {name!r}"
            )

        if entry.get("role") == "builder":
            requires = set(entry.get("requires", []))
            missing = REQUIRED_FOUNDATIONS - requires
            if missing:
                errors.append(
                    f"{path_value}: missing required foundations {sorted(missing)}"
                )
            unknown = requires - names
            if unknown:
                errors.append(
                    f"{path_value}: unknown manifest dependencies {sorted(unknown)}"
                )

            skill_text = skill_file.read_text(encoding="utf-8")
            agent_text = (
                agent_file.read_text(encoding="utf-8")
                if agent_file.is_file()
                else ""
            )
            for foundation in REQUIRED_FOUNDATIONS:
                token = f"${foundation}"
                if token not in skill_text:
                    errors.append(f"{path_value}: SKILL.md does not reference {token}")
                if token not in agent_text:
                    errors.append(
                        f"{path_value}: agents/openai.yaml does not reference {token}"
                    )
            if "brand.json.validation.status" not in skill_text:
                errors.append(
                    f"{path_value}: SKILL.md does not enforce Brand Harvester validation"
                )
            if "brand.json.validation.status" not in agent_text:
                errors.append(
                    f"{path_value}: agents/openai.yaml does not enforce Brand Harvester validation"
                )
            if OPTIONAL_BRAND.search(skill_text):
                errors.append(
                    f"{path_value}: Brand Harvester is still described as optional"
                )

    brand_dir = ROOT / "Skills/brand-harvester"
    packaged_brand_files = {
        str(path.relative_to(brand_dir))
        for path in brand_dir.rglob("*")
        if path.is_file()
    }
    missing_brand_files = REQUIRED_BRAND_FILES - packaged_brand_files
    if missing_brand_files:
        errors.append(
            f"brand-harvester: missing packaged files {sorted(missing_brand_files)}"
        )

    brand_script = brand_dir / "scripts/brand_harvest.py"
    if brand_script.is_file():
        try:
            brand_script_text = brand_script.read_text(encoding="utf-8")
            ast.parse(brand_script_text)
        except (OSError, SyntaxError) as exc:
            errors.append(f"brand-harvester CLI does not parse: {exc}")
        else:
            fail_closed_markers = {
                '"validation": evidence_validation',
                '"status": evidence_status',
                'return 0 if evidence_status == "ok" else 2',
            }
            for marker in fail_closed_markers:
                if marker not in brand_script_text:
                    errors.append(
                        f"brand-harvester CLI is missing fail-closed marker {marker!r}"
                    )

    for path in ROOT.rglob("*"):
        if path.is_dir() and path.name == "__pycache__":
            errors.append(f"cache directory must not be packaged: {path.relative_to(ROOT)}")
        if path.is_file() and path.suffix == ".pyc":
            errors.append(f"cache file must not be packaged: {path.relative_to(ROOT)}")
        if path.is_symlink():
            errors.append(f"symlink must not be packaged: {path.relative_to(ROOT)}")

    markdown_files = [
        path
        for path in ROOT.rglob("*.md")
        if ".git" not in path.parts
    ]
    for markdown_file in markdown_files:
        errors.extend(relative_link_errors(markdown_file))
        text = markdown_file.read_text(encoding="utf-8")
        if "/Users/" in text:
            errors.append(
                f"{markdown_file.relative_to(ROOT)}: contains an absolute user path"
            )

    validate_hardening_markers(errors)
    validate_hupo_fixtures(errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"\nValidation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1

    builders = sum(1 for entry in skills if entry.get("role") == "builder")
    print(
        "Validation passed: "
        f"{len(skills)} skills, {builders} builders, "
        f"{len(REQUIRED_FOUNDATIONS)} required foundations, "
        "2 Hupo regression fixtures."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
