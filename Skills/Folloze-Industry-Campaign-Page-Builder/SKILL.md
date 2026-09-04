---
name: Folloze-Industry-Campaign-Page-Builder
description: Build Folloze industry-level, segment-level, cohort-level, and campaign-level pages that speak to a group of similar accounts rather than one named account. Use for vertical ABM, one-to-few campaigns, event cohorts, account clusters, regional plays, persona pages, and reusable campaign experiences.
---

# Folloze Industry Campaign Page Builder

Use this skill when the page should serve a vertical, segment, persona, cohort, event audience, or campaign group. The output should be reusable across multiple accounts while still feeling specific enough to support ABM.

## Fit

Use this for industry pages, one-to-few account clusters, vertical plays, persona paths, event follow-up cohorts, regional campaigns, and campaign-level pages. Use `Folloze-One-To-One-Microsite-Builder` when one named account owns the story.

## Required Foundations

- `$abm-strategist` is bundled with this skill. Run it before design for one-to-few and named account-cluster work and consume its completed `../abm-strategist/references/builder-handoff-contract.md`. For a broad vertical, persona, event, or regional motion, keep the campaign brief audience-level and do not invent a target account.
- Run `$brand-harvester` for every build before choosing visual treatments or writing CSS/HTML.
- Store the harvest in the active project repo and review its screenshots, `source-dna.md`, `folloze-board-brief.md`, `brand-tokens.css`, `asset-manifest.json`, and `brand.json`. Require a zero CLI exit and `brand.json.validation.status: ok`; inspect the resolved source, requirement-specific asset acceptance, extraction statuses, and desktop/mobile screenshot pair or approved manual evidence.
- If the source is blocked or unreadable, stop visual design until the user supplies a screenshot, brand guide, or equivalent approved evidence.

## Build Mode Gate

Set the construction mode before design:

- `native_traditional`: a classic or U3-style Folloze board with native sections, native content, a board-scoped
  Custom Theme, and Designer personalization rules. Build the native board with the available API or CLI. Use
  authenticated browser control for rule creation or verification when the API does not expose those actions.
  HTML may be a wireframe only when the user explicitly requests one. It is never the final substitute.
- `mcp_html`: a custom HTML campaign page. Use this only when the user explicitly requests HTML.
- `mcp_template`: a template-based Board MCP experience. Return to the strategist's template workflow.

Variants are views of one board. Do not create a new board for each domain or count personalized variants as
extra deliverables.

## Minimum Inputs

Gather only what is missing:

- Industry, segment, cohort, persona, or campaign group.
- Campaign goal and CTA.
- Source brand or design input.
- Public or approved content sources.
- Whether named account examples are allowed.
- Required resource, event, product, or offer modules.
- Build mode and whether personalization must be native.
- Generic fallback plus each approved exact domain, variant key, account logo, copy difference, content set,
  and CTA difference when domain personalization is required.

## Workflow

1. Define the audience boundary: who is included, who is not, and what shared pressure connects them.
2. For one-to-few or named account-cluster work, run `$abm-strategist` and inherit its approved handoff. For broader motions, build an audience-level campaign brief: audience insight, why now, offer, proof, CTA, source constraints, and build mode.
3. Run `$brand-harvester`, save the durable evidence bundle, and review the required outputs before visual design.
4. Choose a reusable structure: vertical narrative, cohort workflow, persona path, account-selection hub, lifecycle/event page, or competitive-replacement path.
5. Choose one signature interaction that advances the campaign decision. For competitive displacement, prefer
   a readiness diagnostic, transition comparison, maturity score, or migration planner. Use
   `$Folloze-ROI-Calculator-Builder` only when sourced economic assumptions and a model owner exist.
6. For `native_traditional`, read `references/native-personalization-acceptance.md`. Build one native board,
   add native sections and content through the available API or CLI, apply the Custom Theme, and then create or
   verify personalization rules in the Designer. Do not stop at an HTML preview or configuration plan.
7. For `mcp_html`, build one self-contained local HTML source file in the active repo and keep it distinct from
   native-board completion.
8. Use approved industry claims and public proof. Do not invent market stats or customer logos.
9. When named account examples, named customer examples, customer logos, quantified outcomes, benchmarks, approved stats, or other approved proof points are missing, unavailable, unapproved, weak, or disallowed, load `references/proof-without-logos.md` before writing proof sections, resource modules, or publishing.
10. If account examples are included, keep them illustrative and public-safe.
11. For domain personalization, define the generic fallback first, then each exact-domain variant. Each variant
    must change its recognition logo, copy, native content set, and CTA context. A logo-only or copy-only swap
    does not demonstrate complete personalization.
12. Read back the native board, theme, content items, and rule configuration. Preview the generic fallback and
    every domain variant in the Designer at desktop and mobile sizes.
13. Complete buyer-facing QA across copy, links, interactions, layout, placeholders, dead controls, fallback
    behavior, and variant differences before save, publish, or delivery.

## Page Standards

- The hero should name the industry, segment, persona, or campaign group clearly.
- Copy should describe the shared business problem, not a generic product pitch.
- Use modules that help visitors self-identify: tabs, paths, filters, lifecycle states, account examples, or role-specific cards.
- A competitive-displacement page must name the incumbent transition clearly, explain the limitation in the
  current operating model, show the seller's different mechanism, and connect that mechanism to a leadership
  outcome. Do not reduce the campaign to generic improvement language.
- Use varied compositions. Two adjacent equal-card grids fail unless the harvested source design clearly uses
  that repetition. The signature interaction should be the primary memorable moment.
- Follow the harvested headline capitalization, terminal punctuation, button families, full-width section
  rhythm, and background treatment.
- If personalization is planned later, mark implementation hooks cleanly without exposing internal merge-tag mechanics to buyers. A build cannot be called personalized until the rules and variant content are applied and read back.

## Recommended Page Shapes

- Industry narrative: market pressure, operational challenge, solution path, proof, CTA.
- Persona path: choose your role, role-specific challenge, resources, CTA.
- Event cohort: pre-event, during-event, post-event journey or follow-up paths.
- Account cluster: shared account pattern, examples, common triggers, next action.
- Campaign hub: overview, resource modules, proof, content tracks, CTA.

## QA Gates

Before final response or publish:

- The page is specific enough for the selected audience but not overfit to one account.
- Build mode is explicit. A `native_traditional` request produced a native board, not an HTML substitute.
- One-to-few/account-cluster work has an approved `$abm-strategist` handoff or is explicitly in repair mode.
  Template mapping is required only for `mcp_template`; the native workflow uses the native personalization
  contract instead.
- A durable `$brand-harvester` bundle exists in the active project repo, its validation status is `ok`, and all required outputs and evidence statuses were reviewed.
- Rendered desktop and mobile views were compared with the harvested source screenshots or approved equivalent brand evidence.
- Named examples are public-safe and approved.
- No unsupported market claims, fake logos, or invented stats.
- CTAs and path choices perform real actions.
- The signature interaction advances a buying decision and works on desktop and mobile. Any calculator has
  sourced assumptions, disclosed formulas, and a named model owner.
- Competitive-displacement copy makes the incumbent transition, different mechanism, and leadership outcome
  clear without unsupported comparative claims.
- No consecutive repetitive card grids remain unless the harvested source design requires them.
- For native personalization, the generic fallback and every approved domain variant have different logos,
  copy, content sets, and CTA context. Exact-domain matching and safe fallback behavior were verified.
- Native content uses multiple approved types. Configuration and content were read back after mutation.
- The board-scoped Custom Theme was applied and read back. Rendered buttons and labels match the harvested
  component evidence.
- Generic fallback and every personalized variant were previewed at desktop and mobile sizes.
- Mobile path selection is readable and tappable.
- Buyer-facing copy, links, interactions, desktop/mobile layout, placeholders, and dead controls have been checked and any blocking issues have been fixed or explicitly reported.
- If saved through Folloze MCP, use the available Folloze MCP publishing tools and current Folloze guide. Report local source path, board ID, returned edit URL, and public URL status separately.

## Final Response

Return the build mode, board count, brief and repair-mode status, brand-harvest requirement acceptance,
audience boundary, page shape, signature interaction, CTA, personalization matrix, native content types,
theme readback, variant preview status, and separate save, readback, publish, and anonymous-verification states.
