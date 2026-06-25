---
name: Folloze-Content-Magic-Builder
description: Turn a customer-provided content item into a strategically framed, source-branded, interactive Folloze experience. Use when the user uploads or links a whitepaper, report, ebook, webinar, blog post, deck, video, checklist, guide, or similar asset and wants a standalone buyer experience rather than a static download or PDF wrapper.
---

# Folloze Content Magic Builder

Use this skill to transform one approved content item into a complete standalone Folloze-ready experience. The asset supplies the approved substance; the buyer context and source brand supply the strategy, visual system, and journey.

## Fit

Use this when the content item is the center of the page. This skill must stand on its own with the same strategic and visual discipline as the campaign and account builders.

If the asset is only one module inside a broader campaign, use the appropriate campaign builder instead. If the asset remains the primary experience, keep this skill in control and use the activation context to shape the page.

## Minimum Inputs

Gather only what is missing:

- The source content item: file, URL, pasted text, transcript, deck, video, or approved summary.
- Target audience.
- Activation context: standalone resource, demand-generation offer, event follow-up, sales follow-up, named-account experience, industry/persona experience, or another real use.
- Buyer stage: awareness, education, evaluation, validation, or decision support.
- Desired conversion action.
- Source brand website, specific source page, brand guide, screenshot, or approved design direction.
- Whether the full asset should stay gated, ungated, summarized, or used as supporting material.

If activation context or buyer stage is not clear from the request, ask one concise question before choosing the page structure. Do not ask the user to select an internal skill.

## Source And Rights Boundaries

- Use only user-provided, public, or approved content.
- Do not reproduce long third-party copyrighted text from an external source. Summarize, excerpt briefly, and link to the source when needed.
- Preserve compliance-sensitive claims exactly only when they are in the approved source. If a claim is unclear, label it for review.
- Keep internal content, notes, or unpublished materials out of buyer-facing copy unless explicitly approved.

## Workflow

1. Read the complete source asset before writing buyer-facing copy or HTML.
2. Extract the asset spine: core promise, audience pain, key ideas, proof points, recommended action, useful visuals, and source limitations.
3. Write an activation brief: use context, audience, buyer stage, why now, asset promise, proof hierarchy, gating model, CTA, and constraints.
4. Establish two sources of truth:
   - Use the asset for facts, claims, quotations, concepts, diagrams, and proof.
   - Use the vendor's public website or approved brand source for visual design, typography, imagery, layout rhythm, buttons, navigation, and footer treatment.
5. Capture the source design system before writing CSS. Inspect the specific source page first, then the vendor home page when useful. Use `brand-harvester` when available.
   - If the source site is blocked or unavailable, use an approved brand guide, screenshot, or source asset with sufficient design evidence.
   - If no reliable design source exists, ask for one concise brand input rather than inventing a generic visual system.
6. Build a message spine: buyer tension, useful promise, key ideas, proof, business implication, and natural next action. Do not mirror the asset page by page.
7. Choose the overall page shape before choosing interactions.
8. Plan the first viewport and section sequence. Give every section one primary job: orient, teach, prove, personalize, qualify, route, or convert.
9. Choose only the interactions that improve comprehension or progression: tabs, accordions, filters, progress path, quiz, assessment, checklist, calculator, modal, embedded media, or role selector.
10. Create one self-contained local HTML file in the active repo.
11. Link to or embed the original asset according to the approved gating/share model.
12. Render and QA the complete experience for design fidelity, desktop/mobile layout, interaction behavior, source fidelity, conversion path, and content-rights boundaries.
13. Invoke `codex-narration-sweep` on the completed HTML. Allow it to make automatic corrections and do not save, publish, or deliver the board until its production-usability gate passes.

## Recommended Page Shapes

Choose one primary composition based on the asset and activation brief:

- Narrative workflow: buyer problem, new approach, how it works, proof, next action.
- Proof-led story: strongest result or quotation first, followed by the evidence and method.
- Diagram-led experience: one central model or architecture with progressive explanation.
- Role-based explorer: one asset interpreted through distinct stakeholder priorities.
- Assessment or workbench: the buyer applies the asset's framework to their own environment.
- Chapter path: a guided sequence when the source has a strong natural progression.
- Resource companion: useful summary, media, tools, and access to the original asset.

Do not default to a chapter path merely because the source is a PDF or deck.

## Page Standards

- The page must feel like a complete vendor-owned digital experience, not an enhanced document viewer.
- Lead with the buyer problem and useful takeaway, not the asset title alone.
- Make the first viewport communicate the buyer problem or outcome in under 10 seconds.
- Include the vendor or subject identity, the strongest relevant visual or proof signal, one meaningful action, and a visible hint of what comes next.
- Break long content into scan-friendly modules and paths.
- Every interactive element should teach, qualify, route, or advance the buyer.
- Use the source asset's diagrams, concepts, or sections only when they are approved and render well.
- Use real vendor, product, customer, or source-asset visuals when available. Rebuild important diagrams as live HTML/SVG only when that improves comprehension.
- Match the source brand's logo treatment, typography scale, button styling, card treatment, imagery, spacing, section surfaces, and light/dark rhythm.
- Use the asset as content authority, not as the visual template. Do not reproduce PDF page proportions, document headers, or page-by-page composition.
- Avoid generic AI gradients, decorative blobs, repetitive card grids, oversized empty heroes, and interaction-heavy layouts with weak narrative hierarchy.
- Choose visual emphasis based on the asset's strongest material: proof statistics, model, architecture, process, quotation, checklist, or decision framework.
- Keep the original asset accessible without making it the primary visual experience.

## Design Review

Before building, confirm:

- The activation brief makes the real use case clear.
- The approved brand source has been inspected.
- The page shape fits the buyer stage and source material.
- The first viewport has a specific visual concept.
- Proof appears at the point where it strengthens the argument.
- Interactions support the page shape rather than becoming the page shape.

If these decisions are still generic, improve them before writing HTML.

## QA Gates

Before final response or publish:

- The source asset is identified and approved for the intended use.
- The activation brief identifies the use context, buyer stage, promise, proof hierarchy, gating model, and CTA.
- The vendor website or approved design source was inspected before CSS was written.
- The page shape was chosen before the interaction pattern.
- The first viewport looks source-branded and communicates a clear buyer outcome.
- Long text has been transformed into original summaries or short compliant excerpts.
- Interactions work and are not decorative.
- CTA and original asset access path are clear.
- The page does not follow the asset page by page or resemble a PDF wrapper.
- Desktop near `1440 x 900` and mobile near `390 x 844` have been rendered and visually inspected.
- Mobile reading and interaction states are clean, with no clipping, overlap, horizontal overflow, or layout shifts.
- Source-brand fidelity, visual hierarchy, imagery, section rhythm, and proof treatment meet the same quality bar as the campaign builders.
- `codex-narration-sweep` passes with no unresolved buyer-facing narration, internal demo language, visual production artifacts, placeholders, or dead controls.
- If saved through Folloze MCP, use the available Folloze MCP publishing tools and current Folloze guide. Report local source path, board ID, returned edit URL, and public URL status separately.

## Final Response

Return the local file path, source asset used, activation context, buyer stage, page shape, interaction pattern, CTA, content-rights caveats, design QA status, Codex Narration Sweep status, and Folloze save/publish status.
