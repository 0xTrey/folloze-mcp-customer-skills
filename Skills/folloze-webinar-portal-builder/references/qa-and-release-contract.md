# QA and Release Contract

Track each evidence layer independently:

1. Source and brand verification.
2. Planning manifest validation.
3. Build-ready validation.
4. Folloze capability and target discovery.
5. Save and structured readback.
6. Desktop, mobile, and functional QA.
7. Publication authorization and publish action.
8. Draft and published state comparison.
9. Anonymous public-route verification.
10. Registration submission and notification status.
11. Analytics configuration and observed delivery.
12. Git commit and remote push.

## Pre-Mutation Checks

- Source mode is consistent across every event.
- Event facts, lifecycle, and primary actions agree.
- External brand evidence has `brand.json.validation.status: ok`.
- Source and target board identities are distinct when a template is used.
- Connection, theme mode, access model, target name, and allowed names are explicit.
- Each requested native provider component has current capability and schema evidence.
- Every native provider surface has a tested direct fallback.
- Five or six resources have verified titles, URLs, images or fallback decisions, and explicit order.
- Apply and publish default to false.

## Structured Readback

After save, require:

- board identifier, name, connection, edit URL, access model, and public route if returned
- event order, navigation, lifecycle, primary action, and direct route for every event
- registration mode, board-owned form identity when used, redirect, success copy, and notification state
- native provider component identity, schema source, destination, schedule, view state, and fallback when used
- resource item identifiers, titles, canonical URLs, types, images, categories, and order
- saved state or hash when available

If the MCP cannot expose a field, record Designer evidence and the limitation. Do not mark it verified by inference.

## Visual Matrix

Inspect real renders at desktop near `1440 x 900` and mobile near `390 x 844`. Add `320`, `375`, `414`, and `768` widths when tooling allows.

Verify:

- one clear primary headline, without an eyebrow-headline-dek stack
- lifecycle, date, time zone, and action clarity
- event navigation and direct routes
- provider pre-live, live, or replay state plus fallback
- speaker rows and event cards
- filters, tabs, or carousels at mobile widths
- form labels, validation affordances, and redirect configuration without submission
- resource ordering and every visible action
- contrast, focus states, reduced motion, alt text, and horizontal overflow

## Release Sequence

1. Run audit-only discovery.
2. Pass build-ready validation.
3. Save with publish off.
4. Read back the result.
5. Run desktop, mobile, and functional QA.
6. Fix and repeat save, readback, and QA until clean.
7. Obtain explicit publication authorization.
8. Record the authorization and pass release-ready validation.
9. Publish through the current authorized operation.
10. Compare draft and published state when supported.
11. Verify the public route anonymously.
12. Record analytics delivery only after observing it in the configured destination.

Do not submit a registration form, enable notifications, or expose a personal join link merely to prove the portal works.
