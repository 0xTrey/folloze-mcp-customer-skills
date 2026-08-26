---
name: folloze-webinar-portal-builder
description: Build a customer-branded Folloze portal that hosts one live webinar, a webinar series, or a replay library with source-safe event data, provider-aware registration and live access, native editability, lifecycle transitions, and staged release evidence. Use for customer demo experiences where Folloze should be the attendee destination. Do not use for a promotion-only page or when one content asset is the whole experience.
---

# Folloze Webinar Portal Builder

Build the webinar destination, not only the campaign page around it. The portal must give attendees a coherent route from discovery and registration through live access, supporting resources, replay, and the next useful action.

## Required Composition

1. Confirm the portal mode, audience motion, brand owner, source mode, lifecycle, and requested publishing state. Inherit an upstream route handoff when supplied.
2. Run `$abm-strategist` only for a named account or one-to-few cluster. Broad event audiences use an audience-level brief.
3. For a Folloze-owned portal, use `$folloze-brand-kit`. For an external brand, run `$brand-harvester` and require `brand.json.validation.status: ok` before visual design.
4. Use `$folloze-board-quality-core` for experience shape, copy and proof discipline, responsive and functional QA, analytics, and MCP preflight.

## Required Reading

Read each reference completely when its stage begins:

- [Source and demo truth contract](references/source-and-demo-truth-contract.md) before writing event facts.
- [Portal architecture](references/portal-architecture.md) before selecting pages, navigation, provider surfaces, or lifecycle behavior.
- [QA and release contract](references/qa-and-release-contract.md) before Folloze save, publish, or completion claims.

## Portal Modes

Choose exactly one mode and record it in the manifest:

- `single_event_lifecycle`: one event destination that moves from registration to live to replay or follow-up.
- `series_hub`: two or more related sessions with shared positioning, navigation, and resources.
- `webinar_platform`: three or more events organized as a reusable live and on-demand destination.

Use `$Folloze-Webinar-Promotion-Page-Builder` instead when the job is only a campaign page for one webinar. Use `$Folloze-Content-Magic-Builder` when one approved recording or asset is the whole experience.

## Minimum Inputs

Gather only what is missing:

- customer or Folloze brand owner and approved brand sources
- portal mode, audience, conversion job, and demo versus real-event status
- event title, description, date, time, IANA time zone, duration, lifecycle, and provider
- approved registration, live, fallback, and replay destinations
- verified speakers, outcomes, agenda, and event imagery
- supporting resources and next action
- intended Folloze connection, new versus existing target, theme mode, and access model

Never invent speakers, customer participation, event dates, attendance, recordings, provider compatibility, or URLs.

## Manifest Gates

Copy [the starter manifest](templates/webinar-portal.starter.json) into the active customer or demo repository. Keep credentials and personal join links out of it.

Planning validation allows explicitly unresolved build inputs:

```bash
python3 scripts/validate_webinar_portal_manifest.py path/to/webinar-portal.json
```

Before Folloze mutation, require:

```bash
python3 scripts/validate_webinar_portal_manifest.py \
  --build-ready path/to/webinar-portal.json
```

Before publication, require:

```bash
python3 scripts/validate_webinar_portal_manifest.py \
  --release-ready path/to/webinar-portal.json
```

A passing validator proves manifest readiness only. It does not authorize a save, publish, registration submission, notification, or provider change.

## Workflow

### 1. Lock source truth

Choose one source mode:

- `verified_real`: every event must have a current source URL, checked timestamp, and verified facts.
- `illustrative_demo`: every event must be visibly identified in the working handoff as illustrative. Use synthetic names and safe destinations until the user approves real event data.

Do not mix verified and illustrative facts in one portal. Keep unknown facts unresolved rather than making them plausible.

For Zoom registration pages, the optional helper can extract commonly exposed source facts:

```bash
python3 scripts/extract_zoom_registration.py \
  "https://tenant.zoom.us/meeting/register/registration-token" \
  --output event-source.json
```

Review its output. A Zoom registration URL proves registration access only. It does not prove an embeddable live player, a safe public join route, duration, speaker identity, or replay availability.

### 2. Establish brand and audience

Use the required brand path before visual design. For external brands, keep the validated Brand Harvester bundle repo-relative. For named-account or one-to-few portals, inherit the approved strategy brief without exposing private account signals.

### 3. Choose the portal architecture

Record the page map, navigation, active lifecycle, event ordering, provider route, registration route, resource library, and next action. A single event can use one page. A series or platform should support direct event access without forcing visitors through every prior session.

Start each major surface with one primary headline. Never use an eyebrow or kicker above a headline with an explanatory dek beneath it. Put supporting context in the body, a schedule block, metadata, or another content module.

### 4. Discover live capabilities

Read the current Folloze MCP guide or capability surface before choosing a live implementation.

For each event choose one:

- `native_widget`: use only after the current target or approved template proves the provider component, schema, scheduling shape, and safe destination fields.
- `external_link`: send the attendee to an approved provider registration or live destination.
- `companion_only`: keep Folloze as the branded agenda and resource destination while the live session runs elsewhere.

Never synthesize a component tag, reuse another customer's widget ID, expose a registrant-specific join URL, or paste arbitrary iframe code. A native widget always needs a tested direct fallback.

### 5. Build the attendee path

Use one active primary action per event lifecycle:

- `upcoming_registration`: register or reserve a seat
- `live_companion`: join or watch live
- `on_demand_replay`: watch the verified replay
- `post_event_follow_up`: review the recap, resources, and next action

If `folloze_then_provider` is selected, disclose that the attendee completes two steps. Keep form notifications off unless explicitly approved. Do not submit a test registration without authorization.

Curate five or six verified supporting resources. Use explicit item ordering so template content cannot leak into the portal.

### 6. Build safely in Folloze

Start with audit-only discovery. Preserve source templates and existing boards. Assert the exact connection, target identity, theme mode, access model, and allowed target names before mutation. Save through the narrowest current MCP or Designer operation. Keep the experience natively editable when that is part of the request.

### 7. Read back, QA, and release

After save, read back board identity, event navigation, provider configuration, registration route, resource ordering, access model, and saved state. Inspect desktop and mobile renders. Test every visible control without submitting data unless authorized.

Publish only with explicit authorization. Then verify draft and published state, open the public route anonymously, and report analytics configuration separately from observed analytics delivery.

## Completion Report

Return:

```text
Portal: <mode, source mode, audience, lifecycle summary>
Sources: <verified, illustrative, and unresolved facts>
Brand: <owner, required skill, evidence status>
Manifest: <path, planning, build-ready, release-ready>
Folloze: <connection, board ID, edit URL, access model>
Live providers: <event, route, capability evidence, fallback>
Registration: <mode, form status, submission status, notifications>
Resources: <verified count and item IDs>
QA: <desktop, mobile, interactions, structured readback>
Save: <status and evidence>
Publish: <status and authorization>
Public: <anonymous result>
Analytics: <configured versus observed>
Git: <commit and push state>
```

Never collapse local source, Folloze save, edit URL, publish, anonymous public access, successful registration, analytics observation, Git commit, and remote push into one completion claim.
