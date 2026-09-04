from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "Skills/Folloze-Content-Magic-Builder/scripts/validate_content_magic.py"
SPEC = importlib.util.spec_from_file_location("validate_content_magic", MODULE_PATH)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


GOOD_HTML = """<!doctype html>
<html>
<head>
<style>
.stage { min-height: 100dvh; }
@keyframes orbit { to { transform: rotate(360deg); } }
.orbit { animation: orbit 20s linear infinite; }
@media (prefers-reduced-motion: reduce) { .orbit { animation: none; } }
@media (max-width: 900px) { .stage { min-height: auto; } }
</style>
</head>
<body>
<main aria-hidden="false">
  <img src="data:image/png;base64,AAAA" alt="People connected through one workflow">
  <button aria-controls="story-image" data-content-target="story-image">Show remote work ←</button>
  <div id="story-image"></div>
  <a href="https://example.com/resource" target="_blank" rel="noopener" onclick="flzAnalytic('cta_click')">Read the public resource</a>
</main>
<script>
document.querySelector('main').inert = false;
</script>
</body>
</html>
"""


class ContentMagicValidatorTests(unittest.TestCase):
    def codes(self, report: dict) -> set[str]:
        return {item["code"] for item in report["errors"]}

    def test_good_chapter_path_with_public_fallback_passes(self) -> None:
        report = validator.validate_document(
            GOOD_HTML,
            chapter_path=True,
            public_fallback="https://example.com/resource",
        )
        self.assertTrue(report["pass"], report["errors"])

    def test_source_proof_copy_and_provenance_class_fail(self) -> None:
        html = GOOD_HTML.replace(
            "<main aria-hidden=\"false\">",
            '<main aria-hidden="false"><p class="source-note">The brief says this came from the partnership brief, page 3.</p>',
        )
        report = validator.validate_document(html)
        codes = self.codes(report)
        self.assertIn("copy.brief_narration", codes)
        self.assertIn("copy.brief_page_label", codes)
        self.assertIn("copy.provenance_token", codes)

    def test_local_image_and_missing_alt_fail(self) -> None:
        html = GOOD_HTML.replace(
            '<img src="data:image/png;base64,AAAA" alt="People connected through one workflow">',
            '<img src="file:///tmp/private.png" alt="">',
        )
        report = validator.validate_document(html)
        codes = self.codes(report)
        self.assertIn("asset.nonportable", codes)
        self.assertIn("asset.image_alt", codes)

    def test_relative_pdf_link_fails_portability(self) -> None:
        html = GOOD_HTML.replace(
            "</main>",
            '<a href="downloads/brief.pdf">Read the brief</a></main>',
        )
        report = validator.validate_document(html)
        self.assertIn("link.nonportable_content_item", self.codes(report))

    def test_directional_control_requires_declared_target(self) -> None:
        html = GOOD_HTML.replace(
            ' aria-controls="story-image" data-content-target="story-image"',
            "",
        )
        report = validator.validate_document(html)
        self.assertIn("interaction.arrow_target", self.codes(report))

    def test_animation_requires_reduced_motion(self) -> None:
        html = GOOD_HTML.replace(
            "@media (prefers-reduced-motion: reduce) { .orbit { animation: none; } }",
            "",
        )
        report = validator.validate_document(html)
        self.assertIn("motion.reduced_motion", self.codes(report))

    def test_public_fallback_requires_safe_new_tab_and_analytics(self) -> None:
        html = GOOD_HTML.replace(' target="_blank" rel="noopener"', "").replace(
            ' onclick="flzAnalytic(\'cta_click\')"',
            "",
        )
        report = validator.validate_document(
            html,
            public_fallback="https://example.com/resource",
        )
        codes = self.codes(report)
        self.assertIn("fallback.safe_new_tab", codes)
        self.assertIn("fallback.analytics", codes)


if __name__ == "__main__":
    unittest.main()
