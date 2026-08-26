from __future__ import annotations

import copy
import json
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_DIR / "scripts"))

import extract_zoom_registration as extractor  # noqa: E402
import validate_webinar_portal_manifest as validator  # noqa: E402


STARTER_PATH = SKILL_DIR / "templates" / "webinar-portal.starter.json"

SYNTHETIC_ZOOM_PAGE = """
<html>
<head>
  <meta property="og:url" content="https://events.zoom.us/meeting/register/token" />
  <meta property="og:image" content="https://events.zoom.us/event-image.png" />
  <meta name="description" content="Fallback description" />
</head>
<body>
<script>
window.setData = {
  meetingTime: 'Sep 17, 2026 12:00 PM',
  timezoneId: "America/New_York",
  meeting: {"topic":"Illustrative AI Operations","duration":60,"agenda":"Build a practical operating model.\\n\\n→ Connect systems safely\\n→ Design reusable workflows\\n→ Measure the attendee path"},
  isCNCluster: false,
};
</script>
</body>
</html>
"""


def load_starter() -> dict:
    return json.loads(STARTER_PATH.read_text(encoding="utf-8"))


def resource(index: int) -> dict:
    base = f"https://resources.invalid/item-{index}"
    return {
        "key": f"resource-{index}",
        "title": f"Illustrative resource {index}",
        "description": f"Synthetic supporting resource {index} for workflow validation.",
        "canonical_url": base,
        "native_item_type": "link",
        "thumbnail_url": f"https://resources.invalid/item-{index}.png",
        "source_url": base,
        "fallback_url": base,
    }


def build_event(index: int, lifecycle: str = "upcoming_registration") -> dict:
    registration_url = f"https://events.invalid/session-{index}/register"
    event = {
        "event_key": f"session-{index}",
        "title": f"Illustrative session {index}",
        "description": "Synthetic event data for portal workflow validation.",
        "source_status": "illustrative",
        "source_url": None,
        "source_checked_at": None,
        "lifecycle": lifecycle,
        "start_at": f"2026-09-{16 + index:02d}T12:00:00-04:00",
        "end_at": f"2026-09-{16 + index:02d}T13:00:00-04:00",
        "timezone": "America/New_York",
        "duration_minutes": 60,
        "learning_outcomes": [
            "Understand the event topic",
            "Review a practical workflow",
            "Choose a useful next action",
        ],
        "speakers": [],
        "registration": {
            "mode": "provider_registration",
            "url": registration_url,
            "form_id": None,
            "submit_redirect_url": None,
            "email_notifications_enabled": False,
        },
        "live": {
            "provider": "zoom_webinar",
            "embed_mode": "external_link",
            "capability_status": "unsupported",
            "schema_source": None,
            "widget_id": None,
            "widget_tag": None,
            "destination_url": f"https://events.invalid/session-{index}/live",
            "fallback_url": f"https://events.invalid/session-{index}/live",
        },
        "replay": {"status": "not_available", "url": None},
        "primary_action": {"label": "Register", "url": registration_url},
    }
    if lifecycle == "live_companion":
        event["primary_action"] = {
            "label": "Join live",
            "url": event["live"]["destination_url"],
        }
    if lifecycle in {"on_demand_replay", "post_event_follow_up"}:
        replay_url = f"https://events.invalid/session-{index}/replay"
        event["registration"]["mode"] = "none"
        event["registration"]["url"] = None
        event["replay"] = {"status": "available", "url": replay_url}
        event["primary_action"] = {"label": "Watch replay", "url": replay_url}
    return event


def make_build_ready(mode: str = "single_event_lifecycle") -> dict:
    data = load_starter()
    data["portal"]["mode"] = mode
    data["portal"]["operation"] = "new_board"
    count = {"single_event_lifecycle": 1, "series_hub": 2, "webinar_platform": 3}[mode]
    data["events"] = [build_event(index) for index in range(1, count + 1)]
    data["brand"].update(
        {
            "source_url": "https://brand.invalid",
            "evidence_status": "ok",
            "brand_json_path": "webinar-portal/brand/brand.json",
            "brand_json_validation_status": "ok",
        }
    )
    data["resources"].update(
        {
            "status": "ok",
            "expected_count": 5,
            "items": [resource(index) for index in range(1, 6)],
        }
    )
    data["folloze"]["connection_label"] = "customer-demo"
    data["release"]["apply"] = True
    return data


class ManifestTests(unittest.TestCase):
    def test_starter_passes_planning_validation(self) -> None:
        self.assertEqual(validator.validate_manifest(load_starter()), [])

    def test_starter_fails_build_ready_with_actionable_gates(self) -> None:
        errors = validator.validate_manifest(load_starter(), build_ready=True)
        combined = "\n".join(errors)
        self.assertIn("portal.operation=new_board or existing_board", combined)
        self.assertIn("brand.evidence_status=ok", combined)
        self.assertIn("duration_minutes or end_at", combined)
        self.assertIn("resources.status=ok", combined)

    def test_single_event_build_and_release_gates(self) -> None:
        data = make_build_ready()
        self.assertEqual(validator.validate_manifest(data, build_ready=True), [])

        release_errors = validator.validate_manifest(data, release_ready=True)
        self.assertTrue(any("release.publish=true" in error for error in release_errors))

        released = copy.deepcopy(data)
        released["release"].update(
            {
                "publish": True,
                "publication_authorization_note": "Approved by the event owner after draft QA.",
            }
        )
        released["folloze"]["expected_public_url"] = "https://experience.invalid/webinar-portal"
        for field in (
            "structured_readback_passed",
            "desktop_qa_passed",
            "mobile_qa_passed",
            "functional_qa_passed",
        ):
            released["evidence"][field] = True
        self.assertEqual(validator.validate_manifest(released, release_ready=True), [])

    def test_multi_event_platform_requires_three_events(self) -> None:
        data = make_build_ready("webinar_platform")
        self.assertEqual(validator.validate_manifest(data, build_ready=True), [])
        data["events"] = data["events"][:2]
        errors = validator.validate_manifest(data, build_ready=True)
        self.assertTrue(any("requires at least 3" in error for error in errors))

    def test_native_widget_requires_capability_evidence_and_template(self) -> None:
        data = make_build_ready()
        live = data["events"][0]["live"]
        live.update(
            {
                "embed_mode": "native_widget",
                "capability_status": "supported",
                "schema_source": "approved-template-readback",
                "widget_id": "widget-1",
                "widget_tag": "verified-zoom-component",
            }
        )
        errors = validator.validate_manifest(data, build_ready=True)
        self.assertTrue(any("template_board_id" in error for error in errors))
        data["folloze"]["template_board_id"] = 101
        self.assertEqual(validator.validate_manifest(data, build_ready=True), [])

    def test_source_modes_cannot_mix(self) -> None:
        data = make_build_ready("series_hub")
        data["events"][1]["source_status"] = "verified"
        errors = validator.validate_manifest(data, build_ready=True)
        self.assertTrue(any("must be illustrative" in error for error in errors))


class ZoomSourceTests(unittest.TestCase):
    def test_extracts_zoom_source_facts(self) -> None:
        facts = extractor.extract_registration_page(
            SYNTHETIC_ZOOM_PAGE,
            "https://events.zoom.us/meeting/register/token#/registration",
            checked_at=datetime(2026, 8, 25, tzinfo=timezone.utc),
        )
        self.assertEqual(facts["title"], "Illustrative AI Operations")
        self.assertEqual(facts["provider"], "zoom_meeting")
        self.assertEqual(facts["start_at"], "2026-09-17T12:00:00-04:00")
        self.assertEqual(facts["duration_minutes"], 60)
        self.assertEqual(len(facts["learning_outcomes"]), 3)
        self.assertEqual(facts["registration_url"], "https://events.zoom.us/meeting/register/token")

    def test_merge_updates_selected_event(self) -> None:
        data = make_build_ready("series_hub")
        facts = extractor.extract_registration_page(
            SYNTHETIC_ZOOM_PAGE,
            "https://events.zoom.us/meeting/register/token",
            checked_at=datetime(2026, 8, 25, tzinfo=timezone.utc),
        )
        merged = extractor.merge_manifest(data, facts, event_key="session-2")
        event = merged["events"][1]
        self.assertEqual(event["title"], "Illustrative AI Operations")
        self.assertEqual(event["end_at"], "2026-09-17T13:00:00-04:00")
        self.assertEqual(event["registration"]["url"], "https://events.zoom.us/meeting/register/token")

    def test_rejects_non_zoom_and_credentialed_urls(self) -> None:
        for url in (
            "https://localhost/meeting/register/token",
            "https://attacker.invalid/meeting/register/token",
            "https://user:secret@zoom.us/meeting/register/token",
        ):
            with self.subTest(url=url), self.assertRaises(ValueError):
                extractor.normalize_url(url)


if __name__ == "__main__":
    unittest.main()
