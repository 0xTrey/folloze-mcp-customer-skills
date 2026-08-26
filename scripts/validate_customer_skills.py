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
REQUIRED_CORE = {"folloze-board-quality-core"}
BUILDER_TOKENS = {
    "$folloze-board-quality-core",
    "$abm-strategist",
    "$folloze-brand-kit",
    "$brand-harvester",
}
REQUIRED_BRAND_FILES = {
    "SKILL.md",
    "agents/openai.yaml",
    "references/brand-harvest-cli.md",
    "scripts/brand_harvest.py",
}
REQUIRED_QUALITY_FILES = {
    "SKILL.md",
    "agents/openai.yaml",
    "references/source-design-dna.md",
    "references/experience-shapes.md",
    "references/buyer-experience-quality-gates.md",
    "references/mcp-publishing-preflight.md",
}
LOCK_COMPLETE_SKILLS = {
    "folloze-board-router",
    "folloze-board-quality-core",
    "Folloze-Webinar-Promotion-Page-Builder",
    "folloze-webinar-portal-builder",
    "folloze-brand-kit",
}
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def load_json(path: Path, errors: list[str]) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"cannot read {path.name}: {exc}")
        return {}


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
            errors.append(f"{markdown_file.relative_to(ROOT)}: missing relative link target {target}")
    return errors


def dependency_cycle_errors(graph: dict[str, set[str]]) -> list[str]:
    errors: list[str] = []
    state: dict[str, int] = {name: 0 for name in graph}
    stack: list[str] = []

    def visit(name: str) -> None:
        state[name] = 1
        stack.append(name)
        for dependency in sorted(graph[name]):
            if dependency not in graph:
                continue
            if state[dependency] == 0:
                visit(dependency)
            elif state[dependency] == 1:
                start = stack.index(dependency)
                errors.append("dependency cycle: " + " -> ".join(stack[start:] + [dependency]))
        stack.pop()
        state[name] = 2

    for name in sorted(graph):
        if state[name] == 0:
            visit(name)
    return errors


def main() -> int:
    errors: list[str] = []
    manifest = load_json(MANIFEST_PATH, errors)
    source_lock = load_json(SOURCE_LOCK_PATH, errors)

    if set(manifest.get("required_foundations", [])) != REQUIRED_CORE:
        errors.append(f"manifest required_foundations must be exactly {sorted(REQUIRED_CORE)}")
    if manifest.get("bundle_version") != "3.1.0":
        errors.append("manifest bundle_version must be 3.1.0")

    locked_paths: set[str] = set()
    for source_name, source in source_lock.get("sources", {}).items():
        for relative_path, expected_hash in source.get("vendored_files", {}).items():
            locked_paths.add(relative_path)
            vendored_file = ROOT / relative_path
            if not vendored_file.is_file():
                errors.append(f"{source_name}: missing locked file {relative_path}")
                continue
            actual_hash = hashlib.sha256(vendored_file.read_bytes()).hexdigest()
            if actual_hash != expected_hash:
                errors.append(f"{source_name}: checksum drift for {relative_path}; refresh the intentional source lock")

    skills = manifest.get("skills", [])
    names = [entry.get("name") for entry in skills]
    name_set = set(names)
    if None in name_set or len(name_set) != len(names):
        errors.append("manifest skill names must be unique and non-empty")

    actual_skill_dirs = {path.name for path in (ROOT / "Skills").iterdir() if path.is_dir()}
    if actual_skill_dirs != name_set:
        errors.append(
            "manifest/filesystem skill mismatch: "
            f"manifest-only={sorted(name_set - actual_skill_dirs)}, "
            f"filesystem-only={sorted(actual_skill_dirs - name_set)}"
        )

    graph: dict[str, set[str]] = {}
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
        if frontmatter_name(skill_file) != name:
            errors.append(f"{path_value}: frontmatter name does not match manifest name {name!r}")

        requires = set(entry.get("requires", []))
        conditional = set(entry.get("conditional_requires", {}).values())
        unknown = (requires | conditional) - name_set
        if unknown:
            errors.append(f"{path_value}: unknown dependencies {sorted(unknown)}")
        graph[name] = requires | conditional

        for route in entry.get("routes_to", []):
            if route not in name_set:
                errors.append(f"{path_value}: unknown route target {route}")

        if entry.get("role") == "builder":
            if requires != REQUIRED_CORE:
                errors.append(f"{path_value}: builder requires must be exactly {sorted(REQUIRED_CORE)}")
            skill_text = skill_file.read_text(encoding="utf-8")
            agent_text = agent_file.read_text(encoding="utf-8") if agent_file.is_file() else ""
            for token in BUILDER_TOKENS:
                if token not in skill_text:
                    errors.append(f"{path_value}: SKILL.md does not reference {token}")
                if token not in agent_text:
                    errors.append(f"{path_value}: agents/openai.yaml does not reference {token}")
            if "brand.json.validation.status" not in skill_text or "brand.json.validation.status" not in agent_text:
                errors.append(f"{path_value}: external brand path does not enforce Brand Harvester validation")
            if "$folloze-board-router" in skill_text or "$folloze-board-router" in agent_text:
                errors.append(f"{path_value}: builder must not invoke or depend on the router")

        if entry.get("role") == "router":
            expected_router_dependencies = name_set - {name}
            if requires != expected_router_dependencies:
                errors.append(
                    f"{path_value}: router must depend on every routed builder and shared foundation; "
                    f"expected {sorted(expected_router_dependencies)}"
                )

        if name in LOCK_COMPLETE_SKILLS:
            packaged = {
                str(path.relative_to(ROOT))
                for path in skill_dir.rglob("*")
                if path.is_file()
            }
            missing_locks = packaged - locked_paths
            if missing_locks:
                errors.append(f"{path_value}: new public skill files missing source locks {sorted(missing_locks)}")

    errors.extend(dependency_cycle_errors(graph))

    for skill_name, required in (
        ("brand-harvester", REQUIRED_BRAND_FILES),
        ("folloze-board-quality-core", REQUIRED_QUALITY_FILES),
    ):
        skill_dir = ROOT / "Skills" / skill_name
        packaged = {str(path.relative_to(skill_dir)) for path in skill_dir.rglob("*") if path.is_file()}
        missing = required - packaged
        if missing:
            errors.append(f"{skill_name}: missing packaged files {sorted(missing)}")

    brand_script = ROOT / "Skills/brand-harvester/scripts/brand_harvest.py"
    if brand_script.is_file():
        script_text = brand_script.read_text(encoding="utf-8")
        try:
            ast.parse(script_text)
        except SyntaxError as exc:
            errors.append(f"brand-harvester CLI does not parse: {exc}")
        for marker in (
            'parsed.scheme.lower() not in {"http", "https"}',
            "address.is_private",
            "class SafeRedirectHandler",
            'allowed_redirect_hosts={"api.brandfetch.io"}',
            'message.get("method") == "Fetch.requestPaused"',
            'return 0 if evidence_status == "ok" else 2',
        ):
            if marker not in script_text:
                errors.append(f"brand-harvester CLI is missing security/fail-closed marker {marker!r}")

    brand_kit_dir = ROOT / "Skills/folloze-brand-kit"
    for path in brand_kit_dir.rglob("*"):
        if path.is_file() and path.suffix.lower() not in {".md", ".yaml"}:
            errors.append(f"folloze-brand-kit: unexpected redistributed binary or code asset {path.relative_to(ROOT)}")
        if path.is_file():
            text = path.read_text(encoding="utf-8", errors="replace")
            for forbidden in ("docs.google.com", "drive.google.com", "product-capabilities-internal.md"):
                if forbidden in text:
                    errors.append(f"{path.relative_to(ROOT)}: public brand kit contains forbidden private source marker {forbidden}")

    for path in ROOT.rglob("*"):
        if ".git" in path.parts:
            continue
        if path.is_dir() and path.name == "__pycache__":
            errors.append(f"cache directory must not be packaged: {path.relative_to(ROOT)}")
        if path.is_file() and path.suffix == ".pyc":
            errors.append(f"cache file must not be packaged: {path.relative_to(ROOT)}")
        if path.is_symlink():
            errors.append(f"symlink must not be packaged: {path.relative_to(ROOT)}")

    for markdown_file in (path for path in ROOT.rglob("*.md") if ".git" not in path.parts):
        errors.extend(relative_link_errors(markdown_file))
        text = markdown_file.read_text(encoding="utf-8")
        if "/Users/" in text:
            errors.append(f"{markdown_file.relative_to(ROOT)}: contains an absolute user path")
        if "CLAUDE_SKILLS_DIR" in text:
            errors.append(f"{markdown_file.relative_to(ROOT)}: contains a Claude-only skill path")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"\nValidation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1

    builders = sum(1 for entry in skills if entry.get("role") == "builder")
    print(f"Validation passed: {len(skills)} skills, {builders} builders, {len(REQUIRED_CORE)} shared foundations.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
