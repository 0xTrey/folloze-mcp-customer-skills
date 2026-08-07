---
name: Folloze-Webinar-Promotion-Page-Builder
description: Build a source-branded Folloze webinar promotion, live-event companion, replay, or follow-up page with a clear event promise, speaker and proof discipline, lifecycle-aware CTAs, and responsive buyer-facing QA. Use when a webinar or virtual event is the page's primary conversion job.
---

# Folloze Webinar Promotion Page Builder

Build a complete webinar experience, not a generic campaign page with a video tile. The event promise, timing state, speakers, agenda, registration or replay path, and supporting resources must work together.

## Required Composition

1. Confirm the webinar lifecycle state and primary conversion job. If an upstream route handoff is supplied, inherit it without rerunning routing.
2. Run `$abm-strategist` only when the webinar targets named accounts or a one-to-few cluster. Otherwise use an audience-level webinar brief.
3. For a Folloze-owned event, use `$folloze-brand-kit`. For an external-brand event, run `$brand-harvester` and require `brand.json.validation.status: ok` before visual design.
4. Use `$folloze-board-quality-core` for shape selection, design and proof discipline, responsive/functional QA, analytics, and MCP preflight.

## Minimum Inputs

Gather only what is missing:

- event title and approved description
- audience and buyer stage
- lifecycle state: upcoming, live companion, on-demand replay, or post-event follow-up
- date, time, time zone, duration, and registration/replay destination
- approved speakers, titles, headshots, and biographies
- agenda or learning outcomes
- brand owner and source evidence
- supporting resources and primary CTA

Do not invent dates, speakers, customer participation, attendance, outcomes, or registration URLs. Use clear review placeholders only in local drafts, then remove or resolve them before save.

## Webinar Brief

Record:

- audience tension and why the topic matters now
- one event promise and three concrete learning outcomes
- proof or speaker authority supporting the promise
- lifecycle state and conversion path
- objections that the page must resolve
- supporting content and post-event next action

For named-account or one-to-few activation, inherit the approved `$abm-strategist` message spine and tailor the webinar relevance without exposing private account signals.

## Before / During / After Lifecycle Structure

Choose sections for the active state. Do not show contradictory CTAs.

### Before: Upcoming Promotion

- outcome-led hero with verified date/time and registration CTA
- useful learning outcomes or agenda
- verified speaker module
- who should attend and why now
- proof or supporting resources
- repeated registration CTA with time-zone clarity

### During: Live Companion

- join/watch action first
- concise session context and agenda
- speaker/reference material
- questions, resources, or follow-up path

### After: On-Demand Replay

- replay or watch CTA first
- chapter or takeaway path when the media supports it
- verified speakers and key ideas
- related resource path
- concrete next conversation CTA

### After: Post-Event Follow-Up

- concise recap and replay access
- takeaways translated into buyer implications
- supporting resources or role paths
- workshop, assessment, product tour, or meeting CTA

## Build Standards

- Keep the first viewport specific: topic, audience outcome, lifecycle state, and one action.
- Use the most useful event visual, speaker photography, product visual, or diagram. Avoid generic stock-stage imagery.
- Keep speaker content factual and proportionate. A logo wall is not event proof.
- Make time-zone language explicit. Do not rely on ambiguous locale abbreviations.
- Registration, calendar, join, recording/replay, resource, and contact controls must point to real approved destinations.
- If registration, live video, or recording is embedded, provide and test a direct fallback link.
- Track registration, calendar, join, recording/replay, chapter, resource, and follow-up actions with distinct analytics labels when supported.
- Every stateful interaction and primary/resource CTA should emit useful analytics when supported.
- Render and inspect desktop and mobile; verify long titles, speaker rows, agenda, embeds, and CTA labels do not clip or overflow.
- Do not describe fictional or illustrative events as real. Label examples clearly in working or seller-facing context without leaving internal staging language in the buyer page.

## Final Response

Return the local source path, route, strategy approval, brand evidence, lifecycle state, verified event facts, CTA destinations, desktop/mobile QA evidence, MCP preflight status, and save/publish states separately.
