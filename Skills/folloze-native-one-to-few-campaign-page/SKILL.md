---
name: folloze-native-one-to-few-campaign-page
description: Build a traditional Folloze board with native sections, content readers, industry messaging, independent account recognition, and a complete generic fallback. Use for industry-led one-to-few demos or customer workflows requiring saved native personalization, rather than an HTML picker.
---

# Native Folloze industry and account personalization

Build views of one board using current native controls. Choose customer handoff or live demonstration as the delivery mode. Do not assume a live demo is a customer leave-behind.

## Route and scope

- Confirm the destination instance and existing board identity. Preserve its public identity and theme scope. Use instance-routing guidance when installed; never choose another instance to recover a failed operation.
- Apply `$abm-strategist` to named one-to-few work. Inherit an existing brief and authorized repair scope. For an audience-level industry experience, infer a compact brief without inventing target accounts.
- Use `$folloze-board-quality-core`. For Folloze-owned work use `$folloze-brand-kit`; for an external brand use `$brand-harvester` with `brand.json.validation.status: ok` and source evidence before design.
- Keep native construction explicit. No custom HTML page, manual picker or guessed targeting URL can substitute for the requested native board.
- Carry existing authority for named-board draft updates. Publication, external delivery, Git push and changes to shared themes need their own applicable authority. A supported UI readback can prove fields the API does not expose; tool limitations do not automatically require renewed approval. Respect browser security refusals.

## Native custom branding

When native sections or a hybrid native shell need custom branding in theme-controlled components, invoke `$folloze-theme-builder` automatically before styling. Read `reference/native-board-routing.md` from that installed skill and pass the existing brand evidence, target theme, and task authority. Reuse a verified matching theme; skip this route for HTML-only or logo/copy/layout-only changes. Keep native construction and the existing save/publish boundaries. If the skill is unavailable, report the theme-stage gap and continue independent work.

## Plan the content and recognition

Read [industry and account rules](references/industry-account-rules.md) before choosing conditions. For an industry-led demo, industry data controls messages and content. Where supported, require Account Name inside each industry banner and exact-domain logo rules. Each industry swap must change the account callout, imagery and message. Logo recognition remains independent of industry selection. Explicit account-message campaigns can use a declared account layer; do not silently substitute that for industry targeting.

Discover the actual fields, operators, provider values, replacement tokens, native section gallery and content schemas. Record the receipt and date. The [example contract](examples/industry-account-contract.json) uses synthetic IDs; replace them with current discoveries. Create a complete generic view and all industry variants before editing.

Lead with call-specific industry, segment or account information. Without it, use vendor industry/solutions pages and relevant customer stories, then map choices to the destination's exact supported values. Choose native sections around the buying job and strongest assets. Judge the header, headline and imagery first, because the initial demo may last only 30 seconds. A rich demo can include customer logos, attributed performance, value cards, a true Leading Item, workflow, customer context, curated resources and closing action. Every selected role must be complete in every variant. Avoid repeated equal-card rows and text-only journeys. Use validated brand evidence and measure rendered native button geometry.

## Build and read back

Read [native content and updates](references/native-content-and-updates.md) before imports, Leading Item configuration or revisions. Use current tools for supported operations and Designer for allowed gaps. Preserve board/item ownership, detach shared copies before editing, reconcile uncertain writes, and bind actions to real native board item IDs.

Apply the narrow update, then read back sections, order, sources, leading selections, theme, rules and fallback. Account-logo overrides preserve header copy, navigation and CTAs; logo visibility, scale and separator presentation may change with the mark. Preserve user-selected logo assets and crops during unrelated revisions. Save anonymous fallback copy without raw name tokens. An account without industry data must not receive an industry inferred from its domain.

Run the portable offline check:

```bash
python3 scripts/native_contract.py path/to/industry-contract.json
python3 scripts/native_contract.py path/to/industry-contract.json --readback path/to/readback.json
```

Run from this installed skill directory or resolve the script relative to it. These checks inspect declarations and supplied readback; they do not contact Folloze or prove live targeting.

## Verify and hand off

- Inspect generic and both/all industry section views in Designer. Wait for loaded images and reader content; verify Leading Item selection, resource ordering, all account marks, carousel movement and actual actions.
- Check desktop, 390px and 320px, plus tablet when layout changes. Check keyboard/focus, visible button dimensions and long callout text.
- Test generic, industry-only, account-only, combined and unknown inputs through supported visitor tools after authorized publication. Keep Designer sections, token definitions and real token substitution separate.
- Verify anonymous route, media/readers and analytics ingestion with their own receipts. Do not infer them from a successful save or configured event.
- For customer use, explain content ownership, rule layers, safe account/logo additions and how to verify a view. Exclude private source IDs, credentials and internal notes from distributed handoffs.

Report instance/board, native template/theme, rule matrix, generic fallback, content IDs, Designer evidence, save/readback, publication, recognized-visitor checks, analytics and Git state separately. Name the remaining unverified conditions. Use the shared inventory helper for concise review links.
