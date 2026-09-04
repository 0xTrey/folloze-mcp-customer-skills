---
name: Folloze-One-To-One-Microsite-Builder
description: Build named-account Folloze one-to-one microsites and follow-up pages for ABM, enterprise sales, post-event follow-up, renewal, expansion, and executive outreach. Use when the user wants a buyer-facing page tailored to one target account, one opportunity, or one named customer.
---

# Folloze One-To-One Microsite Builder

Use this skill to build a Folloze-ready page for one named account or customer. The page should feel like the seller or vendor understands the account's public business context, not like an internal account plan was pasted into a page.

## Fit

Use this skill for named-account pages, executive follow-up, post-event one-to-one pages, account-specific ABM, renewal/expansion stories, and deal-room-style microsites. If the user wants a broad campaign page, use `Folloze-Top-Of-Funnel-Campaign-Landing-Page`.

## Required Foundations

1. Run `$abm-strategist` first and consume its completed
   `../abm-strategist/references/builder-handoff-contract.md`. This skill owns the build when
   `build_mode: mcp_html`. When the handoff says `mcp_template`, return to the strategist's template workflow.
   When it says `native_traditional`, use the industry builder. Never collapse these modes.
2. Run `$brand-harvester` against the vendor's most specific approved source page before choosing visual treatments or writing CSS/HTML.
3. Store the harvest in the active project repo and review its screenshots, `source-dna.md`, `folloze-board-brief.md`, `brand-tokens.css`, `asset-manifest.json`, and `brand.json`. Require a zero CLI exit and `brand.json.validation.status: ok`; inspect the resolved source, requirement-specific asset acceptance, extraction statuses, and desktop/mobile screenshot pair or approved manual evidence.
4. If the source is blocked or unreadable, stop visual design until the user supplies a screenshot, brand guide, or equivalent approved evidence.

## Construction Contract

This skill produces a custom MCP/HTML one-to-one experience. Local HTML is source, not completion. Keep these
states separate: local source, rendered QA, Folloze save and readback, draft preview, publish, and anonymous
verification. Do not describe one state as another.

If the user asked for co-branding or the handoff requires both logos, the top header must show the vendor and
target-account marks together. An account logo that appears only in a hero card, proof block, or lower section
does not satisfy the requirement.

## Minimum Inputs

Gather only what is missing:

- Vendor or seller organization.
- Target account name and public website.
- The trigger: meeting, event, campaign, opportunity, renewal, expansion, or outreach.
- CTA: continue the conversation, book a workshop, review resources, register, evaluate a solution, or another clear next step.
- Approved sources: public account research, call notes, CRM, Drive assets, content links, screenshots, or pasted notes.

## Source Boundaries

- Private notes, CRM, email, Slack, and meeting summaries are strategy inputs only.
- Buyer-facing claims must come from public account evidence, approved content, or user-approved wording.
- Never expose contact-level intent data, private notes, known-contact counts, internal objections, budget comments, sales stage, pricing, or procurement details unless the user explicitly approves that visible copy.
- For any personalized detail, read `references/personalized-not-creepy.md` and classify it as Safe, Risky, or Prohibited before it appears on the page. Keep Safe, fix or cut Risky, and never include Prohibited.

## Workflow

1. Validate `build_mode: mcp_html` and carry forward the approved strategist handoff. If
   `approval_state: repair_mode`, do not reopen the brief unless its reset fields changed.
2. Run `$brand-harvester` with vendor-logo and target-logo requirements when co-branding is in scope. Save the
   durable evidence bundle and review every required output before visual design.
3. Use the vendor brand as the primary visual system. Use the target-account brand as a respectful recognition
   layer unless the user explicitly asks for deeper co-branding.
4. List the personalized elements, name each source in one sentence, and apply the
   `references/personalized-not-creepy.md` rubric before drafting buyer-facing copy.
5. Draft the first viewport from the handoff. It must make the target's pressure, the vendor's mechanism, the
   leadership outcome, and the next action clear without relying on the logo alone.
6. Choose one decision-advancing interaction based on the buying question. Use
   `$Folloze-ROI-Calculator-Builder` only when sourced assumptions and a model owner exist. Otherwise use a
   scenario model, diagnostic, readiness assessment, maturity score, comparison, or role path. Decorative
   widgets do not count.
7. Translate the approved argument into a varied page composition. Do not default to hero, three cards,
   another row of cards, and a final CTA.
8. Build one self-contained local HTML source file in the active repo, then save or embed it through the
   authorized Folloze MCP path only when requested.
9. Include real resources, anchors, modals, videos, calculator actions, or CTA links. Do not include decorative
   dead controls.
10. QA desktop, 390px mobile, and 320px mobile. Check buyer-safe copy, personalization provenance, brand
    fidelity, header co-branding, interaction behavior, and CTA behavior.
11. Complete buyer-facing QA before save, publish, or delivery. Keep local source, readback, draft preview,
    publish, and anonymous verification separate.

## Page Standards

- First viewport must name the target account or make the account context obvious.
- The parent target account owns the headline, argument, leadership outcome, and primary CTA. A subsidiary,
  division, or product can support the case only when the user explicitly scoped the experience to it.
- Run the account-substitution test. If a peer account can be substituted without rewriting the hook,
  mechanism, leadership outcome, and CTA, the page is too generic.
- When co-branding is required, both vendor and target logos are visible in the top header at desktop, 390px,
  and 320px. They remain crisp, correctly proportioned, and readable on the actual header surface.
- Use the account's real operating context, public priorities, industry, event trigger, or known initiative to sharpen the story.
- The page should make the next seller action easier: a precise follow-up, a buyer-ready link, or a focused meeting ask.
- Do not over-personalize in a way that feels watched. Recognize the account; do not reveal surveillance.
- The page should feel prepared from professional homework, never like the account is being watched.
- Follow the harvested brand's headline capitalization and terminal-punctuation pattern. Do not add periods to
  display headlines when the source pattern omits them.
- Use full-width or full-bleed transition bands when the source evidence establishes that rhythm. Do not trap
  every section heading inside the same centered card container.
- Use at least three distinct composition types when the content supports them. Two adjacent equal-card grids
  fail the visual-variety gate unless the source design specifically depends on that repetition.
- The interaction must help the buyer evaluate value, readiness, fit, migration, or next steps. It must produce
  a useful state or result, not merely animate the page.

## QA Gates

Before final response or publish:

- Account identity is correct and not confused with a similarly named entity.
- `$abm-strategist` handoff is approved or explicitly in repair mode and declares `build_mode: mcp_html`.
- A durable `$brand-harvester` bundle exists in the active project repo, its validation status is `ok`, and all required outputs and evidence statuses were reviewed.
- Rendered desktop and mobile views were compared with the harvested source screenshots or approved equivalent brand evidence.
- Public-facing claims are sourced or user-approved.
- Private context has been translated into public-safe problem language.
- Every visible personalized element has a named source and has passed the Safe/Risky/Prohibited rubric.
- Any Risky personalized element has been generalized, explicitly confirmed by the user, or removed.
- CTA is specific and functional.
- Vendor and account logo treatment is verified. Required co-brand logos are in the top header, not only lower
  on the page.
- The parent target account remains the primary narrative subject across the hero, navigation, CTA, and page
  arc. Supporting business units have not displaced it.
- The account-substitution test fails as intended: another peer account would require material copy changes.
- The selected interaction advances a real buyer decision. Any calculator has sourced assumptions, disclosed
  formulas, and a named model owner.
- Headline punctuation and button styles match the harvested evidence, including the computed style of the
  rendered button label.
- Page composition includes meaningful variety and does not repeat equal-card rows across adjacent sections.
- Full-width transition treatment matches the harvested source pattern where applicable.
- Desktop, 390px, and 320px layouts are readable.
- Buyer-facing copy, links, interactions, desktop/mobile layout, placeholders, and dead controls have been checked and any blocking issues have been fixed or explicitly reported.
- The final response includes the list of personalized elements and sources for explicit confirmation before any live publish.
- If saved through Folloze, report local source path, board ID, returned designer URL, and public URL status separately.

## Final Response

Return the local file path, strategist handoff and repair-mode status, brand-harvest path and requirement
acceptance, account/page angle, signature interaction, CTA, source boundary caveats, desktop/390px/320px QA,
and separate Folloze save, readback, draft, publish, and anonymous-verification states.
