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
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
OPTIONAL_BRAND = re.compile(
    r"(?:use|run)\s+[`$]*brand-harvester[`]*\s+when available",
    re.IGNORECASE,
)


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

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"\nValidation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1

    builders = sum(1 for entry in skills if entry.get("role") == "builder")
    print(
        "Validation passed: "
        f"{len(skills)} skills, {builders} builders, "
        f"{len(REQUIRED_FOUNDATIONS)} required foundations."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
