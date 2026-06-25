---
name: folloze-narration-sweep
description: Run the mandatory, AI-provider-neutral final buyer-facing production sweep on a Folloze board before approval, save, publish, or delivery. Invoke after every Folloze board-building workflow, especially demo boards that must also work with real buyers, to automatically remove fourth-wall narration, build-process commentary, visual demo artifacts, internal sales language, dead interactions, placeholders, and anything that prevents production use.
---

# Folloze Narration Sweep

Use this skill as the final enforcement pass after a Folloze board's content, design, and interactions have been built.

## Governing Principle

A board may demonstrate a skill, but it must never describe the demonstration.

The presenter may explain how the skill worked. The board must present only the finished buyer experience.

Treat every board as buyer-facing and production-usable unless the user explicitly identifies it as internal seller enablement. For mixed demo contexts, optimize the visible board for the external buyer and keep internal demo notes in the final response or a separate internal artifact.

## Runtime Independence

Apply this contract by outcomes, not by AI vendor, model, operating system, editor, browser, or publishing tool.

- Use the host environment's available file, page-source, browser, rendering, link-checking, and interaction-testing capabilities.
- Treat `agents/openai.yaml` only as optional OpenAI interface metadata. It is not part of the sweep logic.
- Prefer the bundled Python linter when Python 3 is available. It uses only the standard library.
- If Python is unavailable, perform the same phrase, placeholder, visible-copy, hidden-copy, attribute, comment, CSS-generated-content, and script-string review manually.
- If the board is not HTML, inspect the editable source or configuration plus the rendered buyer experience. Apply the same gate regardless of framework.
- If no browser or renderer is available, do not claim visual or interaction QA passed. Mark those checks `unverified` and block approval, save, publish, or delivery until a capable runtime completes them.
- If no editable source is available, report the exact visible issue and block automatic correction rather than inventing a fix.

Never convert a missing capability into a clean pass.

## Mandatory Builder Contract

Invoke this skill after every Folloze board-building workflow and before approval, save, publish, or delivery.

Every builder must:

1. Pass the completed local HTML and known audience, brand, CTA, source, and board details into this sweep.
2. Allow this skill to edit the HTML automatically.
3. Treat a failed production-usability gate as a save and publish blocker.
4. Resume save or publish only after this skill reports a clean pass.
5. Include the sweep result in its final QA summary.

Do not treat the builder's own copy review as a substitute for this independent pass.

## Required Inputs

Use the completed board artifact and, when available:

- Editable HTML, component source, page configuration, or equivalent.
- Local preview path, preview URL, or public URL.
- Intended audience.
- Vendor or publisher brand.
- Primary CTA.
- Approved source content.
- Folloze board ID or designer URL.

Infer missing context from the board and preceding builder workflow when safe. Do not delay the sweep for information that can be reliably inferred.

## Workflow

1. Confirm the editable source or board artifact exists and identify the renderable preview.
2. Record the current layout and interaction baseline.
3. When version history is available, inspect the current diff or preserve the last working version without overwriting unrelated user changes.
4. For HTML, resolve the skill directory and run `python3 <skill-directory>/scripts/narration_lint.py <path-to-html>` when Python is available. Otherwise perform the deterministic review manually.
5. Read the complete rendered experience and editable source or configuration.
6. Inventory all buyer-visible, accessibility-visible, hidden, and dynamically populated copy.
7. Identify textual and visual fourth-wall violations.
8. Automatically delete content that exists only to explain the build.
9. Automatically rewrite useful content from the buyer's perspective.
10. Preserve approved claims, quotations, legal language, source fidelity, and CTA intent.
11. Recheck the page from the first viewport through the final CTA.
12. Test all interactions, links, forms, conversion paths, desktop, and mobile.
13. When saved through Folloze, test visitor behavior in Folloze Preview mode.
14. Repeat the correction and QA loop until the production-usability gate passes.

Do not pause for approval on routine corrections. Ask only when the requested purpose conflicts with production usability or a safe correction requires new approved content.

## Minimum Evidence

A clean pass requires evidence from all applicable layers:

1. Source review: editable copy, metadata, hidden states, scripts, attributes, comments, and configuration.
2. Rendered review: first viewport through final CTA at required desktop and mobile sizes.
3. Interaction review: every visible control changes state, content, location, or next step as promised.
4. Destination review: anchors resolve and approved external links return the intended destination.
5. Claim review: approved claims, quotations, attribution, and legal copy remain accurate after corrections.
6. Platform review: Folloze Preview behavior is verified when a board has been saved.

Record unavailable layers as `unverified`; never omit them from the result.

## Inspect Every Surface

Inspect:

- Page title, metadata, SEO descriptions, social metadata, and JSON-LD.
- Header, navigation, hero, section labels, body copy, and footer.
- Buttons, links, tabs, accordions, filters, checklists, quizzes, and calculators.
- Modals, drawers, tooltips, hover text, captions, empty states, and confirmations.
- Hidden panels, inactive tabs, off-canvas content, and responsive variants.
- Image alt text, accessible labels, form labels, and validation messages.
- Embedded resource titles, downloads, and CTA destinations.
- HTML comments and commented-out buyer content.
- Inline scripts, JSON objects, configuration blocks, and template strings containing visible copy.
- `data-*` attributes used to populate interactions.
- Mobile-only and desktop-only content.

Do not exempt hidden or accessibility text from buyer-facing standards.

Remove internal source comments when they expose private context, build mechanics, credentials, unpublished claims, presenter instructions, or confidential information. Harmless developer comments may remain when they cannot affect buyer trust or expose sensitive context.

## Deterministic Phrase Lint

Treat lint findings as review candidates, not automatic proof that copy is invalid.

The linter is an accelerator, not the production-usability gate. A zero-finding result does not replace rendered, interaction, conversion, or claim QA.

Review phrases such as:

- `this board`
- `this page`
- `this experience`
- `this section`
- `demo board`
- `demo experience`
- `content magic`
- `built with`
- `created with`
- `generated by`
- `powered by AI`
- `prompt`
- `skill`
- `template`
- `prototype`
- `sample`
- `placeholder`
- `PDF wrapper`
- `static PDF`
- `interactive journey`
- `real interaction`
- `not decorative`
- `the panel changes`
- `what the rep should`
- `demo agenda`
- `sales motion`
- `before and after`
- Bracketed implementation markers such as `[URL]`, `[LOGO]`, `[CONFIRM]`, `[PLACEHOLDER]`, or `[TBD]`.

Judge purpose rather than isolated vocabulary.

Allow legitimate uses such as:

- A sourced customer `proof of concept`.
- A buyer CTA such as `Request a demo`.
- A real product demonstration requested by the buyer.
- Folloze capability language when Folloze is the approved buyer-facing subject.
- `Template` when it is the actual product or resource being offered.

## Textual Violations

### Construction Narration

Remove references to how the board was created, which skill or tool made it, how a source asset was transformed, why an interaction was added, or what the board proves internally.

Examples:

- "This board transforms the PDF into a buyer journey."
- "Built with the Content Magic skill."
- "We recreated the architecture as an interactive SVG."
- "This is not a PDF wrapper."

### Demonstration Narration

Remove copy that tells an internal audience what the demo proves.

Examples:

- "This is where the magic becomes visible."
- "The experience demonstrates how Folloze brings content to life."
- "This section proves that the buttons are functional."

### Interaction Narration

Keep concise buyer instructions:

- "Choose your role."
- "Select a result to explore the business impact."
- "Check what matches your environment."

Remove implementation explanations:

- "The panel changes, so this is a real routing interaction."
- "Every checked item visibly updates the recommendation."
- "This control is not decorative."

### Internal Sales And Production Language

Remove or translate presenter coaching, sales motion language, intent mechanics, sales stage, objections, known-contact activity, QA results, analytics details, publish status, approval instructions, source-rights explanations, missing-asset commentary, and bracketed implementation notes.

Keep these details in an internal artifact or final response, never in the buyer-facing page.

### Feature Self-Description

Remove static-PDF-to-board comparisons, lists of included interactions, "Content Magic proof" sections, "How this experience was made" sections, and claims that the board is interactive, personalized, dynamic, or production-ready.

## Visual Fourth-Wall Violations

Remove or redesign:

- Static-PDF-to-board before-and-after visuals.
- Prompt, skill, AI-tool, or board-generation workflow diagrams.
- Fake browser chrome, cursors, click indicators, or staged annotations.
- `Demo`, `prototype`, `sample`, `generated`, `preview`, or `Content Magic` ribbons.
- Callouts that highlight the existence of tabs, modals, personalization, or interaction mechanics.
- Decorative, disabled, or fake controls presented as functional.
- Mock dashboards, fabricated metrics, placeholder cards, or incomplete modules presented as real.
- Device frames or presentation shells whose only purpose is showing that a page was built.
- Production timelines, transformation arrows, or skill-output scorecards.

Keep diagrams, role selectors, assessments, progress indicators, and controls when they directly help the buyer understand the subject or take the next action.

Do not preserve a visual artifact merely because its wording has been cleaned up. Evaluate its purpose.

## Rewrite And Claim Safety

Apply this order:

1. Delete content that exists only to explain the build.
2. Rewrite it when genuine buyer value exists beneath the narration.
3. Move internal information to the final response when the team still needs it.
4. Preserve content only when necessary buyer guidance, legal language, or explicitly approved internal-enablement content requires it.

Do not replace direct narration with softer narration. Rewritten copy must help the buyer understand the problem, solution, proof, fit, resource, or next action.

- Do not invent or strengthen claims, metrics, customer facts, quotations, capabilities, URLs, legal language, or outcomes.
- Preserve approved quotations, attribution, and compliance-sensitive wording.
- Do not turn an internal hypothesis into a public fact.
- Do not replace missing URLs or content with plausible-looking inventions.

When narration surrounds a valid claim, remove the narration and retain the claim.

When useful content cannot be rewritten safely:

1. Remove it if the page remains complete without it.
2. Use an approved neutral statement when one exists.
3. Otherwise block save or publish and report the exact unresolved item.

Ask whether the content would still belong if the vendor's own marketing team had created the page manually.

## Interaction And Conversion QA

- Click every tab, button, accordion, selector, checklist item, modal trigger, and close control.
- Confirm each control changes content, state, location, or next step as promised.
- Remove dead, decorative, disabled, staged, or presentation-only controls.
- Confirm every internal anchor resolves to an existing section.
- Confirm external CTAs, downloads, booking links, registration links, and demo-request links use real approved destinations.
- Confirm forms have labels, required states, validation, submit behavior, and a clear confirmation state.
- Confirm removed sections have not left orphaned navigation, buttons, or tracking handlers.
- Confirm required analytics hooks remain attached.

Do not submit a real lead form, booking, registration, purchase, or other consequential action during QA without explicit authorization. Validate safely up to the final submission boundary.

## Visual QA

Render and inspect:

- Desktop near `1440 x 900`.
- Mobile near `390 x 844`.
- Narrow mobile near `320px` when the layout contains dense navigation, diagrams, tables, or long words.

Check for horizontal overflow, clipping, overlaps, unfinished blank areas, loading remnants, fake controls, placeholder imagery, responsive-only narration, hidden content appearing at breakpoints, and layout shift caused by rewritten copy or interaction states.

Confirm brand identity, typography, logo treatment, and CTA hierarchy remain intact. Use screenshots and rendered states, not source inspection alone.

## Correction And Regression Loop

After every correction pass:

1. Rerun the lint.
2. Rescan rendered and dynamically populated copy.
3. Re-render desktop and mobile.
4. Re-click affected interactions.
5. Recheck links, anchors, forms, downloads, modals, and CTA destinations.
6. Confirm approved claims and quotations remain accurate.
7. Confirm analytics hooks remain present.
8. Repeat until no unresolved violation remains.

Do not approve based on a clean text scan alone.

## Production Usability Gate

The board passes only when every answer is yes:

1. Could the intended buyer receive the URL without a presenter explaining or apologizing for visible content?
2. Would the page make sense if the buyer did not know it was created for a demo?
3. Does every section help the buyer understand the problem, solution, proof, fit, resource, or next action?
4. Are references to skills, prompts, tools, templates, build choices, and transformation mechanics gone?
5. Are internal notes, QA language, placeholders, and presenter guidance absent?
6. Do all visible controls perform the action their labels imply?
7. Does the CTA feel earned by the preceding content?
8. Are all visuals serving the buyer rather than showcasing production?
9. Could the board be used immediately in a real campaign, sales conversation, follow-up, or evaluation?

Any `no` blocks save, publish, delivery, or final approval.

Any required answer that cannot be verified also blocks release.

## Failure And Rollback

If a violation cannot be corrected safely:

- Preserve the last working local version and unrelated user changes.
- Do not overwrite a known-good live board with a broken version.
- Block release when the issue affects buyer trust, factual accuracy, privacy, compliance, navigation, interaction, conversion, or layout.
- Report the exact file, section, element, issue, and reason automatic correction was unsafe.
- State the minimum decision or approved source needed to proceed.

Do not mark the sweep complete merely because a remaining issue appears small.

## Exceptions

Allow fourth-wall or internal language only when the user explicitly requests an internal seller-enablement board, Folloze is the approved buyer-facing subject, or legal, compliance, accessibility, or consent requirements demand the language.

Keep exceptions narrow and report them before publish.

## Final Response

Report:

- Skill name and version source used.
- Artifact or URL reviewed.
- Automated lint status: `passed`, `findings corrected`, `findings unresolved`, or `unavailable/manual fallback used`.
- Sections removed and copy rewritten.
- Intentional exceptions.
- Source, rendered, interaction, destination, claim, desktop/mobile, and Folloze Preview QA status.
- Any `unverified` or blocked items.
- Save and publish status.

Do not reproduce internal narration in the buyer-facing page while reporting that it was removed.
