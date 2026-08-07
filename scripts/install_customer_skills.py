#!/usr/bin/env python3
"""Install or update the public Folloze skill bundle for Claude and Codex."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import shutil
import sys
import uuid
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
OWNERSHIP_MARKER = ".folloze-skill-install.json"


class InstallSafetyError(RuntimeError):
    pass


def timestamp() -> str:
    return dt.datetime.now().strftime("%Y%m%d-%H%M%S")


def manifest_skill_dirs(repo_root: Path) -> list[tuple[str, Path]]:
    repo_root = repo_root.resolve()
    manifest = json.loads((repo_root / "skills-manifest.json").read_text(encoding="utf-8"))
    skills: list[tuple[str, Path]] = []
    for entry in manifest.get("skills", []):
        name = entry["name"]
        if not isinstance(name, str) or not name or Path(name).name != name or name in {".", ".."}:
            raise InstallSafetyError(f"unsafe skill name in manifest: {name!r}")
        relative_source = Path(entry["path"])
        if relative_source.is_absolute():
            raise InstallSafetyError(f"absolute skill path is not allowed: {relative_source}")
        source = repo_root / relative_source
        if source.is_symlink():
            raise InstallSafetyError(f"skill source is a symlink: {source}")
        resolved_source = source.resolve()
        try:
            resolved_source.relative_to(repo_root / "Skills")
        except ValueError as exc:
            raise InstallSafetyError(f"skill source escapes the repository Skills directory: {source}") from exc
        if not source.is_dir():
            raise InstallSafetyError(f"missing skill source: {source}")
        if any(path.is_symlink() for path in source.rglob("*")):
            raise InstallSafetyError(f"skill source contains a symlink: {source}")
        skills.append((name, resolved_source))
    return skills


def prepare_root(root: Path) -> Path:
    root = root.expanduser()
    if root.is_symlink():
        raise InstallSafetyError(f"skill root is a symlink; refusing to write through it: {root}")
    root.mkdir(parents=True, exist_ok=True)
    if not root.is_dir():
        raise InstallSafetyError(f"skill root is not a directory: {root}")
    return root


def unique_backup(root: Path, name: str, kind: str) -> Path:
    base = root / f".{name}.{kind}-backup-{timestamp()}"
    candidate = base
    counter = 1
    while candidate.exists() or candidate.is_symlink():
        candidate = root / f"{base.name}-{counter}"
        counter += 1
    return candidate


def install_skill(
    name: str,
    source: Path,
    root: Path,
    *,
    replace_symlinks: bool = False,
    dry_run: bool = False,
) -> dict[str, str]:
    root = prepare_root(root)
    destination = root / name
    destination_is_symlink = destination.is_symlink()
    if destination_is_symlink and not replace_symlinks:
        raise InstallSafetyError(
            "destination is a symlink; refusing to follow or replace it without "
            f"--replace-symlinks: {destination}"
        )

    existing = destination.exists() or destination_is_symlink
    kind = "symlink" if destination_is_symlink else "directory"
    backup = unique_backup(root, name, kind) if existing else None
    if dry_run:
        return {
            "skill": name,
            "destination": str(destination),
            "action": "replace" if existing else "install",
            "backup": str(backup) if backup else "",
        }

    staging = root / f".{name}.staging-{uuid.uuid4().hex}"
    try:
        shutil.copytree(source, staging, symlinks=False)
        (staging / OWNERSHIP_MARKER).write_text(
            json.dumps(
                {
                    "managed_by": "folloze-mcp-customer-skills",
                    "skill": name,
                    "installed_at": dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat(),
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        if existing and backup:
            # os.replace renames the directory entry itself. For a symlink this moves
            # only the link and never traverses into the linked checkout.
            os.replace(destination, backup)
        os.replace(staging, destination)
    except Exception:
        if staging.exists():
            shutil.rmtree(staging)
        if backup and (backup.exists() or backup.is_symlink()) and not (destination.exists() or destination.is_symlink()):
            os.replace(backup, destination)
        raise

    return {
        "skill": name,
        "destination": str(destination),
        "action": "replaced" if existing else "installed",
        "backup": str(backup) if backup else "",
    }


def default_codex_root() -> Path:
    codex_home = os.environ.get("CODEX_HOME")
    return (Path(codex_home).expanduser() if codex_home else Path.home() / ".codex") / "skills"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", choices=("claude", "codex", "both"), default="both")
    parser.add_argument("--claude-root", type=Path, default=Path.home() / ".claude" / "skills")
    parser.add_argument("--codex-root", type=Path, default=default_codex_root())
    parser.add_argument(
        "--replace-symlinks",
        action="store_true",
        help="Move each existing skill symlink itself to a timestamped backup, then install a real directory.",
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT, help=argparse.SUPPRESS)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    roots: list[tuple[str, Path]] = []
    if args.target in {"claude", "both"}:
        roots.append(("claude", args.claude_root))
    if args.target in {"codex", "both"}:
        roots.append(("codex", args.codex_root))

    try:
        sources = manifest_skill_dirs(args.repo_root.resolve())
        results: list[dict[str, str]] = []
        for client, root in roots:
            for name, source in sources:
                result = install_skill(
                    name,
                    source,
                    root,
                    replace_symlinks=args.replace_symlinks,
                    dry_run=args.dry_run,
                )
                result["client"] = client
                results.append(result)
    except (InstallSafetyError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    print(json.dumps({"status": "ok", "dry_run": args.dry_run, "results": results}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
