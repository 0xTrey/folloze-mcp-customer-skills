# Folloze MCP Publishing Preflight

Run this preflight only after the local source passes the buyer-experience quality gates and the user has asked to save, publish, update, or push to Folloze.

## Connection And Capability

1. Confirm the intended Folloze MCP connection is authenticated in the current agent environment.
2. Read the current capability list or a safe guide endpoint. Do not assume that a tool name, profile name, tenant, or authentication state from another machine or session still applies.
3. Retrieve the current landing-page creation or save guidance exposed by the connected environment.
4. If the connection cannot return a current guide or safe readback, stop and repair authentication before attempting a write.

## Save Inputs

- Confirm whether this is a new board or an update to an existing board.
- For updates, require the caller to supply or confirm the target board identifier. Do not guess it from a title.
- Confirm the theme mode required by the current guide and the user. Do not silently choose a company theme, no-theme mode, or stylesheet.
- Confirm the local HTML path is the reviewed source of truth and contains the current required stylesheet or shell contract.
- Confirm title, slug or vanity preference, visibility intent, and publish intent separately when those choices exist.

## Custom HTML Section Layout

Apply this gate when a custom HTML section is meant to fill the page. Intentionally inset embeds keep their designed spacing.

1. Read the current custom HTML section guide and inspect the saved section in Folloze Designer. Treat the Folloze section, grid, and HTML widget as separate layout layers. Do not assume the local HTML preview shows their padding.
2. Use the native full-width or **Full grid** control when available. Confirm its saved state after reload. Do not infer that MCP exposes the control unless the current guide or tool readback says so.
3. Measure the rendered section and widget padding on all four sides. For an edge-to-edge design, remove unintended left, right, top, and bottom gutters. Prefer native zero-padding controls. If the host retains padding, offset only the measured value on the HTML fragment's scoped root; do not apply a fixed negative margin to every board or change global `body` styles.
4. Check the saved draft and anonymous published page at desktop and mobile widths. The intended edge-to-edge boundaries must meet the viewport or adjacent section, with no theme-colored strip or horizontal overflow. Ignore Designer selection outlines and toolbar chrome when judging the public result.
5. Record the native layout setting, measured host padding, any scoped compensation, and rendered QA evidence. Fix any unintended gutter before publication; report an unresolved platform limit if it cannot be removed.

## Write And Readback

1. Perform the narrowest supported save operation.
2. Record the returned board identifier and edit/designer URL exactly as returned.
3. Re-read the saved board through a safe MCP readback when available.
4. Treat a returned edit URL as proof of save only. It is not proof of public deployment.
5. Publish only when the user explicitly asked for publication and the environment supports it.
6. Verify the public URL anonymously after publication, including identity, critical copy, CTA behavior, assets, responsive layout, and HTTP availability when practical.

## Report States Separately

```text
Publishing state:
- Local source reviewed:
- MCP authenticated and current guide read:
- Board saved:
- Board identifier:
- Edit URL:
- Public deployment requested:
- Public URL:
- Anonymous public verification:
- Custom HTML layout verification, if applicable:
- Caveats:
```

Never hard-code tenant identifiers, operator identities, local profile names, board identifiers, tracker locations, authentication tokens, or private endpoints in a reusable skill.
