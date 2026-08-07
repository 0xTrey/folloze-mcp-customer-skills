---
name: folloze-board-quality-core
description: Apply shared public-safe design, copy, interaction, responsive QA, analytics, and Folloze MCP publishing gates to every customer-facing Folloze board builder. Use after routing and throughout local build, review, save, and publish readiness.
---

# Folloze Board Quality Core

This skill is the portable production contract shared by all customer builders. It distills reusable design and QA lessons from the internal Demo Builder while excluding internal account systems, trackers, operator identities, and deal workflows.

## Required References

Use these at the matching stage:

- `references/source-design-dna.md` before visual design for external brands, using the validated Brand Harvester bundle as the evidence source.
- `references/experience-shapes.md` before layout or interaction selection.
- `references/buyer-experience-quality-gates.md` before local review and again before MCP save.
- `references/mcp-publishing-preflight.md` before any Folloze save or publish action.

For a Folloze-owned page, `$folloze-brand-kit` replaces external Source DNA capture. Its visual and voice references remain the brand authority.

## Production Sequence

1. Confirm the router handoff: motion, brand owner, approved strategy, brand evidence, selected builder, and conversion job.
2. Write the message spine and proof plan. Every visible factual claim must trace to user-approved material or a public source.
3. Choose one experience shape and record the section order, first-viewport signal, navigation approach, proof requirements, and final CTA.
4. Build one self-contained local HTML source in the active Git repo unless the environment explicitly requires another portable format.
5. Use named design tokens. Make every visible control functional, accessible, and analytically meaningful.
6. Render and visually inspect desktop near `1440 x 900` and mobile near `390 x 844`. Add `320`, `375`, `414`, and `768` width checks when tooling allows.
7. Fix copy, links, interactions, overflow, placeholders, dead controls, contrast, focus, reduced motion, and asset failures.
8. Run the MCP preflight only when the user asked to save, publish, update, or push to Folloze.
9. After save or publish, verify each returned state independently. Never infer public deployment from a successful save.

## Hard Stops

- The required strategy approval is missing for named-account or one-to-few work.
- The required brand source is missing or invalid.
- A claim, customer name, logo, metric, quote, or proof point cannot be sourced.
- The local page has broken controls, placeholder links, horizontal overflow, unreadable content, or unverified assets.
- The current MCP guide, authentication state, theme decision, or save target is unclear.

## Completion Report

Report the local source path, selected shape, strategy approval, brand source, QA evidence, MCP preflight status, board identifier if returned, edit URL if returned, and public deployment verification as separate fields.
