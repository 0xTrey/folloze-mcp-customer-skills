---
name: folloze-board-router
description: Route a Folloze board request to the correct public builder, strategy gate, and brand source before copy or visual design begins. Use for any Folloze board, microsite, campaign landing page, webinar page or portal, industry page, or content-led buyer experience when the correct workflow is not already explicit.
---

# Folloze Board Router

Run this thin router before a customer builder. It chooses the motion, board type, strategy path, and one authoritative brand path. It does not write the final page.

## Routing Decisions

Record four decisions in the working brief:

1. **Audience motion**
   - `one-to-one`: one named account.
   - `one-to-few`: a small named cluster with shared evidence.
   - `one-to-many`: a broad campaign, segment, persona, or event audience without named-account posture.
2. **Brand owner**
   - `Folloze`: Folloze is the visible brand owner.
   - `external`: a customer, prospect, partner, or other vendor is the visible brand owner.
3. **Experience job**
   - named-account microsite
   - campaign landing page
   - webinar promotion or lifecycle page
   - hosted webinar portal, series hub, or replay platform
   - industry, segment, cohort, or persona page
   - content-led standalone experience
4. **Publishing state**
   - local source only
   - ready for MCP preflight
   - saved in Folloze
   - publicly deployed and independently verified

## Strategy Gate

- Run `$abm-strategist` for `one-to-one`, `one-to-few`, or any request naming target accounts. Get its brief and page structure approved before design.
- For `one-to-many` work, create a compact audience-level campaign brief. Do not invent a target account merely to run ABM strategy.
- If a broad request becomes account-specific, stop and route it through `$abm-strategist` before continuing.

## Brand Gate

Choose exactly one required brand source:

- For a **Folloze-owned** experience, use `$folloze-brand-kit`. Do not require `$brand-harvester` merely to rediscover the bundled Folloze system. A current public Folloze page may be harvested only when the request explicitly needs newer page-specific design evidence.
- For an **external-brand** experience, run `$brand-harvester`. Require a zero CLI exit and `brand.json.validation.status: ok` before visual design. If the source is blocked, wait for approved screenshots or brand material.
- For co-branded work, identify the primary visible brand owner. Use its required path, then treat the second brand as approved supporting evidence. Never blend two palettes or voices by guesswork.

## Builder Routing

- `one-to-one` named-account experience: `$Folloze-One-To-One-Microsite-Builder`
- broad offer, demand-generation, product-launch, partner, or general campaign page: `$Folloze-Top-Of-Funnel-Campaign-Landing-Page`
- webinar registration, promotion, live-event companion, or replay/follow-up page: `$Folloze-Webinar-Promotion-Page-Builder`
- hosted single-event destination, multi-session series hub, or reusable live and on-demand platform: `$folloze-webinar-portal-builder`
- industry, segment, cohort, persona, or one-to-few campaign: `$Folloze-Industry-Campaign-Page-Builder`
- one approved asset as the center of the experience: `$Folloze-Content-Magic-Builder`

When two routes seem plausible, choose the experience's primary job. A campaign page that promotes one webinar uses the promotion builder. A destination that hosts live access, multiple sessions, lifecycle transitions, or a reusable replay library uses the portal builder. A report featured inside a broader campaign remains a campaign page.

## Shared Production Contract

Every selected builder must use `$folloze-board-quality-core` for experience-shape selection, source/copy discipline, responsive and interaction QA, analytics checks, and MCP preflight. Keep local creation, Folloze save, returned edit URL, public deployment, and anonymous live verification as separate completion states.

## Router Output

Return a short working handoff:

```text
Board route:
- Motion:
- Brand owner:
- Strategy path and approval status:
- Brand path and evidence status:
- Selected builder:
- Primary conversion job:
- Publishing state requested:
```
