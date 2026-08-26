#!/usr/bin/env python3
"""Validate reusable Folloze webinar portal manifests with staged gates."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import urlparse
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


PORTAL_MODES = {
    "single_event_lifecycle": 1,
    "series_hub": 2,
    "webinar_platform": 3,
}
OPERATIONS = {"audit_only", "new_board", "existing_board"}
AUDIENCE_MOTIONS = {"one-to-one", "one-to-few", "one-to-many"}
SOURCE_MODES = {"verified_real", "illustrative_demo"}
SOURCE_STATES = {"verified", "illustrative"}
LIFECYCLES = {
    "upcoming_registration",
    "live_companion",
    "on_demand_replay",
    "post_event_follow_up",
}
PROVIDERS = {
    "zoom_meeting",
    "zoom_webinar",
    "on24",
    "vimeo_live",
    "youtube_live",
    "external_live",
}
EMBED_MODES = {"native_widget", "external_link", "companion_only"}
CAPABILITY_STATES = {"unresolved", "supported", "unsupported"}
REGISTRATION_MODES = {
    "provider_registration",
    "folloze_then_provider",
    "direct_join_after_registration",
    "none",
}
REPLAY_STATES = {"not_available", "planned", "available"}
THEME_MODES = {"source_brand", "reuse_existing"}
ACCESS_MODELS = {"open", "registration_page", "email_authorization"}
ITEM_TYPES = {"link", "pdf", "youtube", "video", "vimeo", "brightcove", "on24"}
PLACEHOLDER_RE = re.compile(r"\$\{[^}]+\}|\b(?:TBD|TODO|PLACEHOLDER)\b|example\.com", re.I)
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--build-ready", action="store_true")
    parser.add_argument("--release-ready", action="store_true")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable output")
    return parser.parse_args()


def is_positive_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def require_mapping(data: dict[str, Any], key: str, errors: list[str]) -> dict[str, Any]:
    value = data.get(key)
    if not isinstance(value, dict):
        errors.append(f"{key} must be an object")
        return {}
    return value


def require_text(value: Any, path: str, errors: list[str], *, optional: bool = False) -> str | None:
    if optional and (value is None or value == ""):
        return None
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{path} must be a non-empty string")
        return None
    return value.strip()


def require_https(value: Any, path: str, errors: list[str], *, optional: bool = False) -> str | None:
    if optional and (value is None or value == ""):
        return None
    text = require_text(value, path, errors)
    if not text:
        return None
    parsed = urlparse(text)
    if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password:
        errors.append(f"{path} must be a credential-free HTTPS URL")
        return None
    return text


def require_destination(value: Any, path: str, errors: list[str], *, optional: bool = False) -> str | None:
    if optional and (value is None or value == ""):
        return None
    text = require_text(value, path, errors)
    if not text:
        return None
    if text.startswith("#") and len(text) > 1:
        return text
    return require_https(text, path, errors)


def parse_timestamp(value: Any, path: str, errors: list[str], *, optional: bool = False) -> datetime | None:
    if optional and (value is None or value == ""):
        return None
    text = require_text(value, path, errors)
    if not text:
        return None
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        errors.append(f"{path} must be an ISO 8601 timestamp")
        return None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        errors.append(f"{path} must include a UTC offset")
        return None
    return parsed


def validate_timezone(value: Any, path: str, errors: list[str], *, optional: bool = False) -> ZoneInfo | None:
    if optional and (value is None or value == ""):
        return None
    text = require_text(value, path, errors)
    if not text:
        return None
    try:
        return ZoneInfo(text)
    except ZoneInfoNotFoundError:
        errors.append(f"{path} must be a valid IANA time zone")
        return None


def validate_repo_path(value: Any, path: str, errors: list[str]) -> None:
    text = require_text(value, path, errors)
    if not text:
        return
    pure = PurePosixPath(text)
    if pure.is_absolute() or text.startswith("~") or ".." in pure.parts:
        errors.append(f"{path} must be a safe repo-relative path")


def scan_placeholders(value: Any, path: str, errors: list[str]) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            scan_placeholders(child, f"{path}.{key}" if path else key, errors)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            scan_placeholders(child, f"{path}[{index}]", errors)
    elif isinstance(value, str) and PLACEHOLDER_RE.search(value):
        errors.append(f"Unresolved placeholder in {path}: {value}")


def validate_event(
    event: Any,
    index: int,
    *,
    source_mode: str | None,
    build_ready: bool,
    errors: list[str],
) -> tuple[str | None, bool]:
    path = f"events[{index}]"
    if not isinstance(event, dict):
        errors.append(f"{path} must be an object")
        return None, False

    key = require_text(event.get("event_key"), f"{path}.event_key", errors)
    require_text(event.get("title"), f"{path}.title", errors)
    require_text(event.get("description"), f"{path}.description", errors)

    source_status = event.get("source_status")
    if source_status not in SOURCE_STATES:
        errors.append(f"{path}.source_status must be one of: {', '.join(sorted(SOURCE_STATES))}")
    expected_source = "verified" if source_mode == "verified_real" else "illustrative"
    if source_mode in SOURCE_MODES and source_status != expected_source:
        errors.append(f"{path}.source_status must be {expected_source} for portal.source_mode={source_mode}")
    if source_status == "verified":
        require_https(event.get("source_url"), f"{path}.source_url", errors)
        parse_timestamp(event.get("source_checked_at"), f"{path}.source_checked_at", errors)
    else:
        require_https(event.get("source_url"), f"{path}.source_url", errors, optional=True)
        parse_timestamp(event.get("source_checked_at"), f"{path}.source_checked_at", errors, optional=True)

    lifecycle = event.get("lifecycle")
    if lifecycle not in LIFECYCLES:
        errors.append(f"{path}.lifecycle must be one of: {', '.join(sorted(LIFECYCLES))}")

    start = parse_timestamp(event.get("start_at"), f"{path}.start_at", errors, optional=not build_ready)
    end = parse_timestamp(event.get("end_at"), f"{path}.end_at", errors, optional=True)
    zone = validate_timezone(event.get("timezone"), f"{path}.timezone", errors, optional=not build_ready)
    if start and zone and start.astimezone(zone).utcoffset() != start.utcoffset():
        errors.append(f"{path}.start_at offset does not match {path}.timezone")
    if start and end and end <= start:
        errors.append(f"{path}.end_at must be later than start_at")
    duration = event.get("duration_minutes")
    if duration is not None and not is_positive_int(duration):
        errors.append(f"{path}.duration_minutes must be a positive integer or null")
    if build_ready and not is_positive_int(duration) and end is None:
        errors.append(f"{path} requires duration_minutes or end_at for build readiness")
    if start and end and is_positive_int(duration):
        actual_minutes = int((end - start).total_seconds() / 60)
        if actual_minutes != duration:
            errors.append(f"{path}.end_at must equal start_at plus duration_minutes")

    outcomes = event.get("learning_outcomes")
    if not isinstance(outcomes, list) or not 3 <= len(outcomes) <= 5:
        errors.append(f"{path}.learning_outcomes must contain three to five items")
    else:
        for outcome_index, outcome in enumerate(outcomes):
            require_text(outcome, f"{path}.learning_outcomes[{outcome_index}]", errors)

    speakers = event.get("speakers")
    if not isinstance(speakers, list):
        errors.append(f"{path}.speakers must be a list")
    else:
        for speaker_index, speaker in enumerate(speakers):
            speaker_path = f"{path}.speakers[{speaker_index}]"
            if not isinstance(speaker, dict):
                errors.append(f"{speaker_path} must be an object")
                continue
            require_text(speaker.get("name"), f"{speaker_path}.name", errors)
            require_text(speaker.get("title"), f"{speaker_path}.title", errors)
            require_https(
                speaker.get("source_url"),
                f"{speaker_path}.source_url",
                errors,
                optional=source_status == "illustrative",
            )
            require_https(speaker.get("headshot_url"), f"{speaker_path}.headshot_url", errors, optional=True)

    registration = event.get("registration")
    if not isinstance(registration, dict):
        errors.append(f"{path}.registration must be an object")
        registration = {}
    registration_mode = registration.get("mode")
    if registration_mode not in REGISTRATION_MODES:
        errors.append(
            f"{path}.registration.mode must be one of: {', '.join(sorted(REGISTRATION_MODES))}"
        )
    registration_url = require_https(
        registration.get("url"),
        f"{path}.registration.url",
        errors,
        optional=not build_ready or registration_mode == "none",
    )
    redirect_url = require_https(
        registration.get("submit_redirect_url"),
        f"{path}.registration.submit_redirect_url",
        errors,
        optional=registration_mode != "folloze_then_provider" or not build_ready,
    )
    if registration_mode == "folloze_then_provider" and build_ready:
        if not is_positive_int(registration.get("form_id")):
            errors.append(f"{path}.registration.form_id must be positive for folloze_then_provider")
        if registration_url and redirect_url and registration_url != redirect_url:
            errors.append(f"{path}.registration.submit_redirect_url must equal registration.url")
    notifications = registration.get("email_notifications_enabled")
    if not isinstance(notifications, bool):
        errors.append(f"{path}.registration.email_notifications_enabled must be boolean")
    if notifications:
        require_text(
            registration.get("email_notification_authorization_note"),
            f"{path}.registration.email_notification_authorization_note",
            errors,
        )
    if lifecycle == "upcoming_registration" and build_ready and registration_mode == "none":
        errors.append(f"{path} cannot use registration.mode=none while upcoming")

    live = event.get("live")
    if not isinstance(live, dict):
        errors.append(f"{path}.live must be an object")
        live = {}
    if live.get("provider") not in PROVIDERS:
        errors.append(f"{path}.live.provider must be one of: {', '.join(sorted(PROVIDERS))}")
    embed_mode = live.get("embed_mode")
    if embed_mode not in EMBED_MODES:
        errors.append(f"{path}.live.embed_mode must be one of: {', '.join(sorted(EMBED_MODES))}")
    capability = live.get("capability_status")
    if capability not in CAPABILITY_STATES:
        errors.append(
            f"{path}.live.capability_status must be one of: {', '.join(sorted(CAPABILITY_STATES))}"
        )
    destination_url = require_https(
        live.get("destination_url"), f"{path}.live.destination_url", errors, optional=True
    )
    fallback_url = require_https(live.get("fallback_url"), f"{path}.live.fallback_url", errors, optional=True)
    native_widget = embed_mode == "native_widget"
    if native_widget and build_ready:
        if capability != "supported":
            errors.append(f"{path}.live.capability_status must be supported for native_widget")
        for field in ("schema_source", "widget_id", "widget_tag"):
            require_text(live.get(field), f"{path}.live.{field}", errors)
        if not fallback_url:
            errors.append(f"{path}.live.fallback_url is required for native_widget")
    if lifecycle == "live_companion" and build_ready:
        if embed_mode in {"native_widget", "external_link"} and not destination_url:
            errors.append(f"{path}.live.destination_url is required for the live lifecycle")
        if not fallback_url:
            errors.append(f"{path}.live.fallback_url is required for the live lifecycle")

    replay = event.get("replay")
    if not isinstance(replay, dict):
        errors.append(f"{path}.replay must be an object")
        replay = {}
    replay_status = replay.get("status")
    if replay_status not in REPLAY_STATES:
        errors.append(f"{path}.replay.status must be one of: {', '.join(sorted(REPLAY_STATES))}")
    replay_url = require_https(replay.get("url"), f"{path}.replay.url", errors, optional=True)
    if lifecycle in {"on_demand_replay", "post_event_follow_up"} and build_ready:
        if replay_status != "available" or not replay_url:
            errors.append(f"{path}.replay must be available with a verified URL for this lifecycle")

    action = event.get("primary_action")
    if not isinstance(action, dict):
        errors.append(f"{path}.primary_action must be an object")
        action = {}
    require_text(action.get("label"), f"{path}.primary_action.label", errors)
    action_url = require_destination(
        action.get("url"), f"{path}.primary_action.url", errors, optional=not build_ready
    )
    if build_ready and lifecycle == "upcoming_registration" and registration_mode == "provider_registration":
        if registration_url and action_url != registration_url:
            errors.append(f"{path}.primary_action.url must equal registration.url for provider registration")
    if build_ready and lifecycle == "live_companion" and embed_mode == "external_link":
        if destination_url and action_url != destination_url:
            errors.append(f"{path}.primary_action.url must equal live.destination_url for external live access")
    if build_ready and lifecycle == "on_demand_replay" and replay_url and action_url != replay_url:
        errors.append(f"{path}.primary_action.url must equal replay.url for on-demand replay")

    return key, native_widget


def validate_manifest(
    data: Any,
    *,
    build_ready: bool = False,
    release_ready: bool = False,
) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["Manifest root must be an object"]
    if release_ready:
        build_ready = True

    scan_placeholders(data, "", errors)
    if data.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    require_text(data.get("profile_name"), "profile_name", errors)

    portal = require_mapping(data, "portal", errors)
    portal_mode = portal.get("mode")
    if portal_mode not in PORTAL_MODES:
        errors.append(f"portal.mode must be one of: {', '.join(sorted(PORTAL_MODES))}")
    operation = portal.get("operation")
    if operation not in OPERATIONS:
        errors.append(f"portal.operation must be one of: {', '.join(sorted(OPERATIONS))}")
    for field in ("title", "audience", "primary_conversion_job"):
        require_text(portal.get(field), f"portal.{field}", errors)
    if portal.get("audience_motion") not in AUDIENCE_MOTIONS:
        errors.append(
            f"portal.audience_motion must be one of: {', '.join(sorted(AUDIENCE_MOTIONS))}"
        )
    source_mode = portal.get("source_mode")
    if source_mode not in SOURCE_MODES:
        errors.append(f"portal.source_mode must be one of: {', '.join(sorted(SOURCE_MODES))}")
    if source_mode == "illustrative_demo":
        require_text(portal.get("demo_disclosure"), "portal.demo_disclosure", errors)
    slug = require_text(portal.get("vanity_slug"), "portal.vanity_slug", errors)
    if slug and not SLUG_RE.fullmatch(slug):
        errors.append("portal.vanity_slug must use lowercase letters, numbers, and hyphens")
    if build_ready and operation == "audit_only":
        errors.append("build-ready validation requires portal.operation=new_board or existing_board")

    brand = require_mapping(data, "brand", errors)
    brand_owner = brand.get("owner")
    if brand_owner not in {"external", "folloze"}:
        errors.append("brand.owner must be external or folloze")
    require_https(brand.get("source_url"), "brand.source_url", errors, optional=not build_ready)
    if brand.get("evidence_status") not in {"unresolved", "ok", "failed"}:
        errors.append("brand.evidence_status must be unresolved, ok, or failed")
    if build_ready:
        if brand.get("evidence_status") != "ok":
            errors.append("build-ready validation requires brand.evidence_status=ok")
        if brand_owner == "external":
            validate_repo_path(brand.get("brand_json_path"), "brand.brand_json_path", errors)
            if brand.get("brand_json_validation_status") != "ok":
                errors.append("external brands require brand.brand_json_validation_status=ok")
        if brand_owner == "folloze" and brand.get("folloze_brand_kit_status") != "ok":
            errors.append("Folloze-owned portals require brand.folloze_brand_kit_status=ok")

    events = data.get("events")
    if not isinstance(events, list) or not events:
        errors.append("events must contain at least one event")
        events = []
    minimum = PORTAL_MODES.get(portal_mode)
    if minimum and len(events) < minimum:
        errors.append(f"portal.mode={portal_mode} requires at least {minimum} event(s)")
    if portal_mode == "single_event_lifecycle" and len(events) != 1:
        errors.append("single_event_lifecycle requires exactly one event")

    keys: set[str] = set()
    native_widget_requested = False
    for index, event in enumerate(events):
        key, uses_native_widget = validate_event(
            event,
            index,
            source_mode=source_mode if isinstance(source_mode, str) else None,
            build_ready=build_ready,
            errors=errors,
        )
        native_widget_requested = native_widget_requested or uses_native_widget
        if key:
            if key in keys:
                errors.append(f"Duplicate event_key: {key}")
            keys.add(key)

    resources = require_mapping(data, "resources", errors)
    if resources.get("status") not in {"unresolved", "ok", "failed"}:
        errors.append("resources.status must be unresolved, ok, or failed")
    expected_count = resources.get("expected_count")
    if expected_count not in {5, 6}:
        errors.append("resources.expected_count must be 5 or 6")
    items = resources.get("items")
    if not isinstance(items, list):
        errors.append("resources.items must be a list")
        items = []
    if build_ready:
        if resources.get("status") != "ok":
            errors.append("build-ready validation requires resources.status=ok")
        if len(items) != expected_count:
            errors.append("resources.items count must equal resources.expected_count")
    resource_keys: set[str] = set()
    resource_urls: set[str] = set()
    for index, item in enumerate(items):
        path = f"resources.items[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{path} must be an object")
            continue
        key = require_text(item.get("key"), f"{path}.key", errors)
        require_text(item.get("title"), f"{path}.title", errors)
        require_text(item.get("description"), f"{path}.description", errors)
        canonical = require_https(item.get("canonical_url"), f"{path}.canonical_url", errors)
        require_https(item.get("thumbnail_url"), f"{path}.thumbnail_url", errors, optional=True)
        require_https(item.get("source_url"), f"{path}.source_url", errors)
        require_https(item.get("fallback_url"), f"{path}.fallback_url", errors)
        if item.get("native_item_type") not in ITEM_TYPES:
            errors.append(f"{path}.native_item_type must be one of: {', '.join(sorted(ITEM_TYPES))}")
        if key:
            if key in resource_keys:
                errors.append(f"Duplicate resource key: {key}")
            resource_keys.add(key)
        if canonical:
            if canonical in resource_urls:
                errors.append(f"Duplicate resource canonical_url: {canonical}")
            resource_urls.add(canonical)

    folloze = require_mapping(data, "folloze", errors)
    connection = require_text(
        folloze.get("connection_label"), "folloze.connection_label", errors, optional=not build_ready
    )
    template_id = folloze.get("template_board_id")
    target_id = folloze.get("target_board_id")
    if template_id is not None and not is_positive_int(template_id):
        errors.append("folloze.template_board_id must be a positive integer or null")
    if target_id is not None and not is_positive_int(target_id):
        errors.append("folloze.target_board_id must be a positive integer or null")
    if is_positive_int(template_id) and is_positive_int(target_id) and template_id == target_id:
        errors.append("folloze.template_board_id and target_board_id must differ")
    target_name = require_text(folloze.get("target_board_name"), "folloze.target_board_name", errors)
    allowed_names = folloze.get("allowed_target_names")
    if not isinstance(allowed_names, list) or not allowed_names:
        errors.append("folloze.allowed_target_names must contain at least one name")
    elif target_name and target_name not in allowed_names:
        errors.append("folloze.target_board_name must be in allowed_target_names")
    if folloze.get("theme_mode") not in THEME_MODES:
        errors.append(f"folloze.theme_mode must be one of: {', '.join(sorted(THEME_MODES))}")
    if folloze.get("native_editability_required") is not True:
        errors.append("folloze.native_editability_required must be true")
    if folloze.get("expected_access") not in ACCESS_MODELS:
        errors.append(f"folloze.expected_access must be one of: {', '.join(sorted(ACCESS_MODELS))}")
    require_https(
        folloze.get("expected_public_url"),
        "folloze.expected_public_url",
        errors,
        optional=not release_ready,
    )
    if build_ready and not connection:
        errors.append("build-ready validation requires folloze.connection_label")
    if build_ready and operation == "existing_board" and not is_positive_int(target_id):
        errors.append("existing_board requires a positive folloze.target_board_id")
    if build_ready and operation == "new_board" and native_widget_requested and not is_positive_int(template_id):
        errors.append("new_board with a native widget requires a positive folloze.template_board_id")

    release = require_mapping(data, "release", errors)
    for field in ("apply", "publish"):
        if not isinstance(release.get(field), bool):
            errors.append(f"release.{field} must be boolean")
    if release.get("publish") and not release.get("apply"):
        errors.append("release.publish=true requires release.apply=true")
    if build_ready and release.get("apply") is not True:
        errors.append("build-ready validation requires release.apply=true")
    if release_ready:
        if release.get("publish") is not True:
            errors.append("release-ready validation requires release.publish=true")
        require_text(
            release.get("publication_authorization_note"),
            "release.publication_authorization_note",
            errors,
        )

    evidence = require_mapping(data, "evidence", errors)
    for field in (
        "source_ledger_path",
        "brand_evidence_path",
        "manifest_path",
        "readback_path",
        "qa_dir",
        "release_receipt_path",
    ):
        validate_repo_path(evidence.get(field), f"evidence.{field}", errors)
    for field in (
        "structured_readback_passed",
        "desktop_qa_passed",
        "mobile_qa_passed",
        "functional_qa_passed",
        "anonymous_qa_passed",
        "analytics_observed",
    ):
        if not isinstance(evidence.get(field), bool):
            errors.append(f"evidence.{field} must be boolean")
    if release_ready:
        for field in (
            "structured_readback_passed",
            "desktop_qa_passed",
            "mobile_qa_passed",
            "functional_qa_passed",
        ):
            if evidence.get(field) is not True:
                errors.append(f"release-ready validation requires evidence.{field}=true")

    return errors


def main() -> int:
    args = parse_args()
    try:
        data = json.loads(args.manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors = [f"Unable to read manifest: {exc}"]
    else:
        errors = validate_manifest(
            data,
            build_ready=args.build_ready,
            release_ready=args.release_ready,
        )

    stage = "release" if args.release_ready else "build" if args.build_ready else "planning"
    payload = {"valid": not errors, "stage": stage, "errors": errors}
    if args.json:
        print(json.dumps(payload, indent=2))
    elif errors:
        print(f"Webinar portal manifest validation failed ({stage}):")
        for error in errors:
            print(f"- {error}")
    else:
        print(f"Webinar portal manifest validation passed ({stage}).")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
