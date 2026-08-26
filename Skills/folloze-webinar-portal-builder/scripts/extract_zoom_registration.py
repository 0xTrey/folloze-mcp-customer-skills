#!/usr/bin/env python3
"""Extract common source facts from a public Zoom registration page."""

from __future__ import annotations

import argparse
import ipaddress
import json
import re
import socket
import sys
from datetime import datetime, timedelta, timezone
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.error import HTTPError
from urllib.parse import urlsplit, urlunsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


ZOOM_HOST_SUFFIXES = ("zoom.us", "zoom.com", "zoomgov.com")


class MetaParser(HTMLParser):
    """Collect named and Open Graph metadata without third-party packages."""

    def __init__(self) -> None:
        super().__init__()
        self.values: dict[str, list[str]] = {}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "meta":
            return
        data = {key.lower(): value for key, value in attrs if value is not None}
        key = data.get("property") or data.get("name")
        content = data.get("content")
        if key and content:
            self.values.setdefault(key.lower(), []).append(unescape(content).strip())


def is_zoom_host(hostname: str) -> bool:
    host = hostname.lower().rstrip(".")
    return any(host == suffix or host.endswith(f".{suffix}") for suffix in ZOOM_HOST_SUFFIXES)


def normalize_url(value: str) -> str:
    parts = urlsplit(value.strip())
    hostname = parts.hostname or ""
    if parts.scheme.lower() != "https" or not hostname:
        raise ValueError("Zoom registration URL must be HTTPS")
    if parts.username or parts.password or parts.port not in {None, 443}:
        raise ValueError("Zoom registration URL must not include credentials or a custom port")
    if not is_zoom_host(hostname):
        raise ValueError("Registration URL must use an approved Zoom host")
    netloc = hostname.lower() if parts.port is None else f"{hostname.lower()}:{parts.port}"
    return urlunsplit(("https", netloc, parts.path.rstrip("/"), parts.query, ""))


def resolve_public_host(hostname: str) -> None:
    try:
        addresses = {
            ipaddress.ip_address(item[4][0])
            for item in socket.getaddrinfo(hostname, 443, type=socket.SOCK_STREAM)
        }
    except socket.gaierror as exc:
        raise ValueError(f"Unable to resolve Zoom host: {hostname}") from exc
    if not addresses or any(not address.is_global for address in addresses):
        raise ValueError("Zoom host must resolve only to public network addresses")


class SafeZoomRedirectHandler(HTTPRedirectHandler):
    """Permit redirects only between validated public Zoom hosts."""

    def redirect_request(
        self,
        req: Request,
        fp: Any,
        code: int,
        msg: str,
        headers: Any,
        newurl: str,
    ) -> Request:
        normalized = normalize_url(newurl)
        resolve_public_host(urlsplit(normalized).hostname or "")
        return super().redirect_request(req, fp, code, msg, headers, normalized)


def fetch_page(url: str, timeout: int = 30) -> str:
    normalized = normalize_url(url)
    resolve_public_host(urlsplit(normalized).hostname or "")
    request = Request(
        normalized,
        headers={"User-Agent": "Mozilla/5.0 (compatible; FollozeWebinarPortal/1.0)"},
    )
    opener = build_opener(SafeZoomRedirectHandler())
    with opener.open(request, timeout=timeout) as response:
        final_url = normalize_url(response.geturl())
        resolve_public_host(urlsplit(final_url).hostname or "")
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


def first_meta(parser: MetaParser, key: str) -> str | None:
    for value in parser.values.get(key.lower(), []):
        if value and not value.endswith("null"):
            return value
    return None


def js_scalar(page: str, key: str) -> str | None:
    pattern = rf"\b{re.escape(key)}\s*:\s*(['\"])(.*?)\1\s*,"
    match = re.search(pattern, page, flags=re.DOTALL)
    if not match:
        return None
    value = match.group(2)
    return (
        value.replace(r"\n", "\n")
        .replace(r"\r", "\r")
        .replace(r"\t", "\t")
        .replace(r"\'", "'")
        .replace(r'\"', '"')
        .replace(r"\/", "/")
    )


def meeting_object(page: str) -> dict[str, Any]:
    match = re.search(r"\bmeeting\s*:\s*(\{.*?\})\s*,\s*isCNCluster\s*:", page, re.DOTALL)
    if not match:
        return {}
    try:
        parsed = json.loads(unescape(match.group(1)))
    except json.JSONDecodeError:
        return {}
    return parsed if isinstance(parsed, dict) else {}


def parse_start(meeting_time: str | None, timezone_id: str | None) -> str | None:
    if not meeting_time or not timezone_id:
        return None
    try:
        zone = ZoneInfo(timezone_id)
    except ZoneInfoNotFoundError:
        return None
    for fmt in ("%b %d, %Y %I:%M %p", "%B %d, %Y %I:%M %p"):
        try:
            return datetime.strptime(meeting_time.strip(), fmt).replace(tzinfo=zone).isoformat()
        except ValueError:
            continue
    return None


def agenda_parts(agenda: str) -> tuple[str | None, list[str]]:
    paragraphs = [part.strip() for part in re.split(r"\n\s*\n", agenda) if part.strip()]
    summary = paragraphs[0] if paragraphs else None
    outcomes: list[str] = []
    for line in agenda.splitlines():
        item = line.strip()
        if item.startswith(("→", "•", "- ", "* ")):
            cleaned = item.lstrip("→•*- ").strip()
            if cleaned:
                outcomes.append(cleaned)
    return summary, outcomes


def extract_registration_page(
    page: str,
    source_url: str,
    *,
    checked_at: datetime | None = None,
) -> dict[str, Any]:
    parser = MetaParser()
    parser.feed(page)
    meeting = meeting_object(page)

    canonical = normalize_url(first_meta(parser, "og:url") or source_url)
    timezone_id = js_scalar(page, "timezoneId")
    start_at = parse_start(js_scalar(page, "meetingTime"), timezone_id)
    agenda = meeting.get("agenda") if isinstance(meeting.get("agenda"), str) else ""
    summary, outcomes = agenda_parts(agenda)
    duration_value = meeting.get("duration")
    duration = duration_value if isinstance(duration_value, int) and duration_value > 0 else None
    topic = meeting.get("topic") if isinstance(meeting.get("topic"), str) else None
    path = urlsplit(canonical).path.lower()
    provider = "zoom_webinar" if "/webinar/" in path else "zoom_meeting"
    checked = checked_at or datetime.now(timezone.utc)

    return {
        "source_url": canonical,
        "source_checked_at": checked.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
        "source_status": "verified",
        "provider": provider,
        "title": topic or first_meta(parser, "og:title"),
        "description": summary or first_meta(parser, "description"),
        "learning_outcomes": outcomes,
        "start_at": start_at,
        "timezone": timezone_id,
        "duration_minutes": duration,
        "registration_url": canonical,
        "event_image_url": first_meta(parser, "og:image"),
        "speakers": [],
    }


def select_event(manifest: dict[str, Any], event_key: str | None) -> dict[str, Any]:
    events = manifest.get("events")
    if not isinstance(events, list) or not events:
        raise ValueError("Manifest must contain an events list")
    if event_key:
        matches = [event for event in events if isinstance(event, dict) and event.get("event_key") == event_key]
        if len(matches) != 1:
            raise ValueError(f"Expected exactly one event with event_key={event_key!r}")
        return matches[0]
    if len(events) != 1 or not isinstance(events[0], dict):
        raise ValueError("Use --event-key when the manifest contains multiple events")
    return events[0]


def merge_manifest(
    manifest: dict[str, Any],
    facts: dict[str, Any],
    *,
    event_key: str | None = None,
) -> dict[str, Any]:
    event = select_event(manifest, event_key)
    for key in (
        "source_url",
        "source_checked_at",
        "source_status",
        "title",
        "description",
        "start_at",
        "timezone",
    ):
        value = facts.get(key)
        if value is not None:
            event[key] = value
    outcomes = facts.get("learning_outcomes")
    if isinstance(outcomes, list) and outcomes:
        event["learning_outcomes"] = outcomes
    duration = facts.get("duration_minutes")
    if isinstance(duration, int) and duration > 0:
        event["duration_minutes"] = duration

    registration_url = facts.get("registration_url")
    registration = event.setdefault("registration", {})
    if registration_url:
        registration["url"] = registration_url
        if registration.get("mode") == "folloze_then_provider":
            registration["submit_redirect_url"] = registration_url
        if event.get("lifecycle") == "upcoming_registration" and registration.get("mode") == "provider_registration":
            event.setdefault("primary_action", {})["url"] = registration_url

    live = event.setdefault("live", {})
    live["provider"] = facts.get("provider")
    if registration_url and not live.get("fallback_url"):
        live["fallback_url"] = registration_url

    start_text = event.get("start_at")
    duration_value = event.get("duration_minutes")
    if isinstance(start_text, str) and isinstance(duration_value, int) and duration_value > 0:
        start = datetime.fromisoformat(start_text.replace("Z", "+00:00"))
        event["end_at"] = (start + timedelta(minutes=duration_value)).isoformat()
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", help="Public Zoom meeting or webinar registration URL")
    parser.add_argument("--output", type=Path, help="Write extracted source facts as JSON")
    parser.add_argument("--manifest", type=Path, help="Refresh one event in an existing portal manifest")
    parser.add_argument("--event-key", help="Event key to update when the manifest has multiple events")
    parser.add_argument("--timeout", type=int, default=30, help="Network timeout in seconds")
    return parser.parse_args()


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    try:
        page = fetch_page(args.url, timeout=args.timeout)
        facts = extract_registration_page(page, args.url)
        if args.output:
            write_json(args.output, facts)
        if args.manifest:
            manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
            write_json(args.manifest, merge_manifest(manifest, facts, event_key=args.event_key))
        if not args.output and not args.manifest:
            print(json.dumps(facts, indent=2, ensure_ascii=False))
    except (OSError, ValueError, json.JSONDecodeError, HTTPError) as exc:
        print(f"Zoom source extraction failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
