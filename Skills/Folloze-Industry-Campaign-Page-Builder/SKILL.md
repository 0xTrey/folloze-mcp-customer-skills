---
name: Folloze-Industry-Campaign-Page-Builder
description: Build Folloze industry-level, segment-level, cohort-level, and campaign-level pages that speak to a group of similar accounts rather than one named account. Use for vertical ABM, one-to-few campaigns, event cohorts, account clusters, regional plays, persona pages, and reusable campaign experiences.
---

# Folloze Industry Campaign Page Builder

Use this skill when the page should serve a vertical, segment, persona, cohort, event audience, or campaign group. The output should be reusable across multiple accounts while still feeling specific enough to support ABM.

## Fit

Use this for industry pages, one-to-few account clusters, vertical plays, persona paths, event follow-up cohorts, regional campaigns, and campaign-level pages. Use `Folloze-One-To-One-Microsite-Builder` when one named account owns the story.

## Minimum Inputs

Gather only what is missing:

- Industry, segment, cohort, persona, or campaign group.
- Campaign goal and CTA.
- Source brand or design input.
- Public or approved content sources.
- Whether named account examples are allowed.
- Required resource, event, product, or offer modules.

## Workflow

1. Define the audience boundary: who is included, who is not, and what shared pressure connects them.
2. Build a campaign brief: audience insight, why now, offer, proof, account examples if allowed, CTA, and source constraints.
3. Choose a reusable structure: vertical narrative, cohort workflow, persona path, account-selection hub, or lifecycle/event page.
4. Build one self-contained local HTML file in the active repo.
5. Use approved industry claims and public proof. Do not invent market stats or customer logos.
6. When named account examples, named customer examples, customer logos, quantified outcomes, benchmarks, approved stats, or other approved proof points are missing, unavailable, unapproved, weak, or disallowed, load `references/proof-without-logos.md` before writing proof sections, resource modules, or publishing.
7. If account examples are included, keep them illustrative and public-safe.
8. QA desktop/mobile, CTA behavior, source-brand fidelity, and whether the page stays reusable across the whole audience.

## Page Standards

- The hero should name the industry, segment, persona, or campaign group clearly.
- Copy should describe the shared business problem, not a generic product pitch.
- Use modules that help visitors self-identify: tabs, paths, filters, lifecycle states, account examples, or role-specific cards.
- If personalization is planned later, mark implementation hooks cleanly without exposing internal merge-tag mechanics to buyers.

## Recommended Page Shapes

- Industry narrative: market pressure, operational challenge, solution path, proof, CTA.
- Persona path: choose your role, role-specific challenge, resources, CTA.
- Event cohort: pre-event, during-event, post-event journey or follow-up paths.
- Account cluster: shared account pattern, examples, common triggers, next action.
- Campaign hub: overview, resource modules, proof, content tracks, CTA.

## QA Gates

Before final response or publish:

- The page is specific enough for the selected audience but not overfit to one account.
- Named examples are public-safe and approved.
- No unsupported market claims, fake logos, or invented stats.
- CTAs and path choices perform real actions.
- Mobile path selection is readable and tappable.
- If saved through Folloze MCP, use the available Folloze MCP publishing tools and current Folloze guide. Report local source path, board ID, returned edit URL, and public URL status separately.

## Final Response

Return the local file path, audience boundary, page shape, CTA, QA status, and Folloze save/publish status.
