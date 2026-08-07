from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ManifestTopologyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        manifest = json.loads((ROOT / "skills-manifest.json").read_text(encoding="utf-8"))
        cls.entries = {entry["name"]: entry for entry in manifest["skills"]}

    def test_router_depends_on_all_builders_and_foundations(self) -> None:
        router_dependencies = set(self.entries["folloze-board-router"].get("requires", []))
        self.assertEqual(router_dependencies, set(self.entries) - {"folloze-board-router"})

    def test_builders_depend_on_quality_core_not_router(self) -> None:
        for name, entry in self.entries.items():
            if entry.get("role") != "builder":
                continue
            with self.subTest(builder=name):
                self.assertEqual(entry.get("requires"), ["folloze-board-quality-core"])
                self.assertNotIn("folloze-board-router", entry.get("requires", []))
                skill_text = (ROOT / entry["path"] / "SKILL.md").read_text(encoding="utf-8")
                agent_text = (ROOT / entry["path"] / "agents/openai.yaml").read_text(encoding="utf-8")
                self.assertNotIn("$folloze-board-router", skill_text)
                self.assertNotIn("$folloze-board-router", agent_text)

    def test_dependency_graph_has_no_cycle(self) -> None:
        graph = {
            name: set(entry.get("requires", []))
            | set(entry.get("conditional_requires", {}).values())
            for name, entry in self.entries.items()
        }
        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(name: str) -> None:
            if name in visiting:
                self.fail(f"dependency cycle includes {name}")
            if name in visited:
                return
            visiting.add(name)
            for dependency in graph[name]:
                visit(dependency)
            visiting.remove(name)
            visited.add(name)

        for name in graph:
            visit(name)


if __name__ == "__main__":
    unittest.main()
