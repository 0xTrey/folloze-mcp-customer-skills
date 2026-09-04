---
name: Folloze-Content-Magic-Builder
description: Turn one approved report, PDF, webinar, video, deck, guide, or similar content item into a source-branded, editorially rewritten, interactive Folloze buyer experience with portable assets and verified public delivery. Use when the content item is the experience rather than one module in a broader campaign.
---

# Folloze Content Magic Builder

Transform one approved content item into a complete vendor-owned digital experience. The source supplies facts, claims, concepts, and proof. The activation context and declared visual owner supply the buyer strategy, editorial framing, design system, imagery, interactions, and conversion path.

## Fit

Use this skill when the content item is the center of the experience. If the item is only one module inside a broader campaign, use the appropriate campaign builder instead.

Do not treat a PDF or deck as a visual template. The output must stand alone as polished buyer-facing marketing, not as a document wrapper or evidence review.

## Required Foundations

- Confirm that the approved content item is the primary conversion job. Inherit an approved upstream route handoff without rerunning routing.
- Run `$abm-strategist` only for named-account or one-to-few activation. Do not invent a target account for broad or standalone content.
- Use `$folloze-brand-kit` for a Folloze-owned experience.
- For every external brand, run `$brand-harvester` and require a zero exit plus `brand.json.validation.status: ok` before choosing visual treatments or writing CSS or HTML.
- Use `$folloze-board-quality-core` for source discipline, shape selection, responsive and interaction QA, analytics, accessibility, and MCP preflight.
- Read [the Content Magic Production Contract](references/content-magic-production-contract.md) before concept selection, copywriting, interaction planning, or build work.

## Minimum Inputs

Gather only what is missing:

- Approved source content item or approved summary
- Audience and activation context
- Buyer stage and desired conversion action
- Primary visual owner and approved brand source
- Supporting partner or co-brand, when applicable
- Original asset access model: native, embedded, reader, gated, public source, or approved authoritative fallback

If activation context or buyer stage is genuinely unclear, ask one concise question before choosing the page shape. Do not ask the user to select an internal skill.

## Mandatory Production Packet

Before HTML, record these decisions in the active project repo:

1. Activation brief and claim matrix
2. Brand ownership declaration and surface map
3. Three materially distinct experience concepts when the user requests creative direction or the best shape is unclear
4. Selected page shape and reason
5. Message spine and per-scene copy plan
6. Visual allocation map with one distinct job per dominant visual
7. Interaction map naming the control, target region, material changes, direction, keyboard behavior, and analytics event
8. Asset manifest naming source, rights status, purpose, delivery method, expected dimensions, and fallback
9. Original asset access decision, including any approved unavailable-asset exception

Keep provenance, page citations, filenames, and evidence notes in this packet and QA receipts, never in ordinary buyer-facing sections.

## Production Workflow

1. Read the complete source before writing buyer-facing copy or HTML.
2. Extract its spine: buyer tension, useful promise, key ideas, proof, business implication, action, visual opportunities, and limitations.
3. Declare the primary visual owner, content authority, supporting partners, source evidence, and excluded brand signals. A partner mentioned in the source does not automatically own the visual system.
4. Complete the applicable brand gate. Stop visual design if Brand Harvester evidence is invalid, incomplete, or contradicted by the proposed composition.
5. Choose the experience shape before interactions. Do not default to chapters merely because the source is paginated.
6. Write customer-facing copy from the source facts. Never narrate the source document or expose the production process.
7. Allocate a distinct visual job to every scene. Do not repeat a dominant diagram, photograph, or composition unless the repetition communicates an intentional progression.
8. Specify every interaction before implementation. A control must materially change the region its affordance points toward or be removed.
9. Choose portable asset delivery before build. Embed approved assets or use stable public HTTPS locations. Do not depend on local, temporary, private, or expiring URLs.
10. Create one self-contained local HTML source in the active Git repo unless the approved Folloze method requires another portable source.
11. Resolve the validator relative to this `SKILL.md`, then run it against the exact artifact:

```bash
CONTENT_MAGIC_SKILL_DIR=/path/to/Folloze-Content-Magic-Builder
python3 "$CONTENT_MAGIC_SKILL_DIR/scripts/validate_content_magic.py" path/to/experience.html \
  --json-output path/to/qa/content-magic-static.json
```

Add `--chapter-path` for a guided pinned-scene experience. Add `--public-fallback URL` when an approved public resource replaces an unavailable original file.

12. Render and visually inspect desktop near `1440 x 900`, compact desktop near `1366 x 768`, and mobile near `390 x 844`. Exercise every interactive state and fix all blocking issues.
13. If the user requested Folloze save or publish, complete the current MCP preflight and analytics contract. Preserve the requested theme mode, board target, and vanity decision.
14. After save, verify the saved configuration independently. After publish, verify the anonymous public URL independently with fresh public loading.

## Copy Contract

- Write source-grounded, source-invisible marketing copy.
- Lead with the buyer problem, useful outcome, or strongest verified proof, not the asset title.
- Give each scene one primary editorial job: orient, teach, prove, personalize, qualify, route, or convert.
- Keep a major desktop headline near two or three lines when the source-faithful message permits it. Widen the composition or edit the copy before accepting a six-line stack.
- Remove source-proof labels, filenames, page citations, provenance microcopy, internal context notes, and phrases such as “the brief says” or “the source frames.”
- Do not use an eyebrow-headline-dek stack.
- Do not use em dash characters.
- Preserve verified claims and compliance-sensitive language. Do not invent results, customers, metrics, guarantees, timelines, quotations, or case-study outcomes.
- Read the complete experience once as a content marketer after scene-level edits. Repair ambiguity, repetition, abrupt transitions, and copy that describes the production process instead of buyer value.

## Design And Interaction Contract

- Match the declared visual owner's real logo treatment, typography, component families, imagery, spacing, surfaces, and light or dark rhythm.
- Keep supporting brands in their declared role. Do not average two brands into a generic co-branded theme.
- Every dominant visual must have a documented source, purpose, and distinct scene-level job.
- If a diagram represents orbit, flow, sequence, accumulation, or comparison, make the behavior communicate that meaning when motion improves comprehension. Provide a reduced-motion state.
- Directional controls must point toward the region that changes.
- A selector must update primary content such as image, headline, explanation, steps, diagram, or decision output. A change limited to small footer copy or incidental microcopy is not material.
- If no material state change is justified, remove the arrow and use static value propositions or another honest presentation.
- Every visible control must work with pointer and keyboard input, expose usable names and state, and emit descriptive analytics when the publishing path supports it.

## Asset Access And Portability

- Apply the shared Content Item Experience Contract when the original item can be safely kept on-board, embedded, or opened in an accessible reader.
- Never ship a reader, CTA, image, logo, video, or download that depends on `file:`, localhost, a user directory, a temporary directory, a private workspace, or an expiring signed URL.
- If the original file is unavailable and the user approves substitution, replace its access CTA with the closest authoritative public source. Record the exception internally. Do not expose a buyer-facing warning or evidence label.
- Public fallbacks open with `target="_blank" rel="noopener"` and retain analytics.
- Validate the effective source and natural dimensions of every hosted image after save and after publish, including images revealed by tabs or selectors.

## Guided Chapter Contract

Use this only when a chapter path is the selected shape:

- Desktop uses one stationary viewport, one active scene, one chapter per accepted navigation gesture, and inactive scenes that are hidden, inert, and noninteractive.
- At `900px` and below, switch to ordinary document flow and remove desktop-only inert and hidden state.
- Use `100dvh`, compact-height bands, measured active-scene overflow, and remeasurement after resize, font settlement, scene entry, and interaction changes.
- Provide visible progress, previous and next controls, keyboard navigation, reduced motion, and an honest hint of what comes next.
- Never solve height pressure with a single hard cutoff that clips content.

## QA And Release Gates

Before delivery, save, or publish, require all applicable gates in the production contract. In particular:

- Static validation passes against the exact artifact hash.
- Brand fidelity is compared with approved desktop and mobile evidence.
- Desktop, compact-height desktop, and mobile renders have no clipping, overlap, horizontal overflow, or unreadable content.
- Every control is exercised and every declared target changes materially.
- Every image state loads with nonzero natural dimensions.
- No page-authored console errors remain.
- The original asset or approved authoritative fallback works publicly.
- Local build, Folloze save, saved readback, theme, vanity, publication, anonymous rendering, hosted interactions, analytics invocation, analytics delivery, Git commit, and push are reported as separate states.

## Final Response

Return the local source path, artifact hash, activation context, selected shape, brand owner and harvest status, source item and access mode, copy review status, visual and interaction QA status, asset portability status, responsive QA status, board identifier when applicable, theme decision, vanity decision, save state, publish state, anonymous public URL status, analytics state, and Git state.
