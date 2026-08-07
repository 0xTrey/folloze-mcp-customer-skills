from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts/install_customer_skills.py"
SPEC = importlib.util.spec_from_file_location("install_customer_skills", MODULE_PATH)
assert SPEC and SPEC.loader
installer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(installer)


class InstallerSafetyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.source = self.base / "source" / "sample-skill"
        self.source.mkdir(parents=True)
        (self.source / "SKILL.md").write_text("---\nname: sample-skill\n---\n")
        self.root = self.base / "client" / "skills"
        self.root.mkdir(parents=True)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_symlink_destination_fails_closed_by_default(self) -> None:
        linked_checkout = self.base / "dirty-checkout" / "sample-skill"
        linked_checkout.mkdir(parents=True)
        sentinel = linked_checkout / "user-change.txt"
        sentinel.write_text("preserve me")
        destination = self.root / "sample-skill"
        destination.symlink_to(linked_checkout, target_is_directory=True)

        with self.assertRaises(installer.InstallSafetyError):
            installer.install_skill("sample-skill", self.source, self.root)

        self.assertTrue(destination.is_symlink())
        self.assertEqual(sentinel.read_text(), "preserve me")

    def test_explicit_symlink_replacement_moves_only_link(self) -> None:
        linked_checkout = self.base / "dirty-checkout" / "sample-skill"
        linked_checkout.mkdir(parents=True)
        sentinel = linked_checkout / "user-change.txt"
        sentinel.write_text("preserve me")
        destination = self.root / "sample-skill"
        destination.symlink_to(linked_checkout, target_is_directory=True)

        result = installer.install_skill(
            "sample-skill",
            self.source,
            self.root,
            replace_symlinks=True,
        )

        self.assertTrue(destination.is_dir())
        self.assertFalse(destination.is_symlink())
        self.assertTrue((destination / "SKILL.md").is_file())
        marker = json.loads((destination / installer.OWNERSHIP_MARKER).read_text())
        self.assertEqual(marker["managed_by"], "folloze-mcp-customer-skills")
        self.assertEqual(marker["skill"], "sample-skill")
        self.assertEqual(sentinel.read_text(), "preserve me")
        backup = Path(result["backup"])
        self.assertTrue(backup.is_symlink())
        self.assertEqual(backup.resolve(), linked_checkout.resolve())

    def test_regular_update_keeps_timestamped_backup(self) -> None:
        destination = self.root / "sample-skill"
        destination.mkdir()
        (destination / "old.txt").write_text("old")

        result = installer.install_skill("sample-skill", self.source, self.root)

        self.assertTrue((destination / "SKILL.md").is_file())
        self.assertEqual((Path(result["backup"]) / "old.txt").read_text(), "old")

    def test_skill_root_symlink_is_rejected(self) -> None:
        real_root = self.base / "real-skills"
        real_root.mkdir()
        linked_root = self.base / "linked-skills"
        linked_root.symlink_to(real_root, target_is_directory=True)
        with self.assertRaises(installer.InstallSafetyError):
            installer.install_skill("sample-skill", self.source, linked_root)

    def test_manifest_path_cannot_escape_skills_directory(self) -> None:
        repo = self.base / "repo"
        (repo / "Skills").mkdir(parents=True)
        outside = repo / "outside"
        outside.mkdir()
        (repo / "skills-manifest.json").write_text(
            json.dumps({"skills": [{"name": "escaped", "path": "outside"}]}),
            encoding="utf-8",
        )
        with self.assertRaises(installer.InstallSafetyError):
            installer.manifest_skill_dirs(repo)

    def test_manifest_skill_name_cannot_escape_destination(self) -> None:
        repo = self.base / "repo"
        source = repo / "Skills" / "sample"
        source.mkdir(parents=True)
        (repo / "skills-manifest.json").write_text(
            json.dumps({"skills": [{"name": "../escaped", "path": "Skills/sample"}]}),
            encoding="utf-8",
        )
        with self.assertRaises(installer.InstallSafetyError):
            installer.manifest_skill_dirs(repo)


if __name__ == "__main__":
    unittest.main()
