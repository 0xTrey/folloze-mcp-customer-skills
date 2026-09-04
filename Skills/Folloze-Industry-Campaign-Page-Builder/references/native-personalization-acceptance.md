# Native Traditional Personalization Acceptance

Use this contract for a traditional or U3-style Folloze campaign board with account-domain personalization.

## Board Boundary

- Build one native board for the campaign.
- Treat the generic fallback and personalized variants as views of that board.
- Do not save an HTML preview as the final native deliverable.
- Keep local wireframe, native build, Designer configuration, draft, publish, and anonymous verification as
  separate states.

## Personalization Matrix

Record one row per view:

```yaml
variant_key: ""
account_domain: fallback | exact-domain.example
recognition_logo: ""
hero_copy_key: ""
supporting_copy_key: ""
content_item_ids: []
content_types: []
cta_context: ""
```

Rules:

- Define the generic fallback first.
- Use exact approved domains. Do not use broad substring matching.
- Missing, malformed, unapproved, and unexpected inputs resolve to the generic fallback.
- Do not emit raw account domains in analytics. Use stable `variant_key` and fallback state.
- Each personalized view changes logo, hero or supporting copy, content selection, and CTA context.
- Content sets must be materially different. Identical content lists with a logo swap fail.
- Use multiple approved native content types across the campaign. When the campaign is intended to showcase
  content personalization, each view must contain at least two native types.

## Competitive Replacement

For a replacement campaign, the first viewport must identify the incumbent or current operating model, the
reason to reconsider it, the seller's different mechanism, and the next evaluation step. Avoid unsupported
claims that the seller is categorically cheaper, faster, safer, or better.

Use one signature decision tool. A readiness diagnostic or migration comparison is preferred when economic
assumptions are incomplete. Use an ROI calculator only when its inputs, formulas, scenarios, and owner are
approved.

## Theme And Visual System

- Apply a board-scoped Custom Theme derived from the vendor's accepted Brand Harvester bundle.
- Record the theme identifier or returned object and read it back after mutation.
- Verify primary, secondary, and dark-surface buttons, including the effective rendered label color.
- Follow the harvested headline punctuation and section-band rhythm.
- Avoid consecutive equal-card grids unless the source design requires them.

## Required Readback And Preview

Read back and compare:

1. Board sections and order.
2. Native content item IDs and types.
3. Custom Theme state.
4. Exact-domain rules and generic fallback.
5. Generic and personalized view content.

Preview the generic fallback and every approved domain variant in the authenticated Designer at desktop and
mobile sizes. Do not claim anonymous routing until the board is published and tested from a signed-out or
otherwise anonymous session.
