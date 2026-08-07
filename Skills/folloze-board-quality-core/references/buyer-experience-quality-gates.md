# Buyer Experience Quality Gates

Run these gates before local review and again before Folloze MCP save. Fix failures before save unless the user explicitly accepts a clearly reported caveat.

## Brand And Copy

- The first viewport identifies the visible brand and states a useful buyer outcome. For a one-to-one page, include buyer-safe account context when evidence supports it.
- Buyer-facing copy excludes internal staging or production language.
- Every factual claim comes from public evidence, user-approved material, or a clearly labeled local planning assumption.
- No invented metrics, customers, logos, awards, analyst quotes, case studies, testimonials, product facts, speakers, dates, or outcomes.
- Private notes may shape strategy but never become visible claims.

## Structure

- The page does not default to a generic hero, three equal cards, final CTA, and footer unless the brand source supports that rhythm.
- No cards inside cards, floating-card treatment for ordinary sections, fake browser chrome, fake phone frames, fake IDE frames, or decorative product shells.
- Heroes, proof areas, tools, embeds, and section transitions do not clip at common desktop or mobile viewports.
- Situation and solution content is compact and scannable.

## Controls And Analytics

- Every visible button, navigation item, card CTA, resource action, arrow, read-more control, tab, slider, modal opener, form, media control, and calculator control works.
- No `href="#"`, placeholder destination, `javascript:void(0)`, or dead decorative arrow remains.
- External links are real and use `target="_blank" rel="noopener"` when a new tab is intended.
- Primary and resource CTAs emit a useful analytics event with text, area, and destination when the publishing path supports analytics.
- Meaningful interactions emit descriptive events and payloads.
- Do not acknowledge MCP analytics compliance until the saved HTML actually satisfies the current guide.

## Mobile And Accessibility

- Render desktop near `1440 x 900` and mobile near `390 x 844`. Check `320`, `375`, `414`, and `768` widths when tooling allows.
- `document.documentElement.scrollWidth <= window.innerWidth` at mobile widths.
- Buttons, tabs, navigation, footer, breadcrumbs, and CTA labels do not wrap awkwardly.
- Headings allow long-word wrapping without pushing the viewport wider.
- Light and dark sections set readable text colors explicitly.
- Text, buttons, focus rings, muted copy, and interactive states have practical contrast.
- Focus-visible, hover, active, disabled, and reduced-motion states exist where applicable.
- Controls have usable names and keyboard behavior.

## Tokens, Motion, And CSS

- Colors, neutrals, fonts, radii, shadows, and spacing use named tokens or a clearly grouped custom-property block.
- One-off color and font values require source-brand justification.
- Do not use `transition: all`; transition only changed properties.
- Prefer transform and opacity animation over layout properties.
- Every keyframe or non-trivial motion has a `prefers-reduced-motion` fallback.
- Accent color is emphasis, not decoration, unless the source brand uses broad accent surfaces.

## Assets And Proof

- Every logo, image, SVG, embed, and carousel asset loads in local preview.
- Source-owned visual assets are preferred. Generic image search is only a fallback when the source lacks usable material and usage is appropriate.
- Repeated carousel content supports animation continuity only and does not imply more customers or proof.
- Auto-moving content pauses on hover/focus or moves slowly enough not to distract.
- Inspect official SVGs and image variants before use; filenames alone do not prove their visible treatment.

## Save Readiness

- The current Folloze landing-page creation guidance has been read in the active MCP connection.
- The theme mode and save target are confirmed.
- The required stylesheet or shell contract is present exactly as the current guide requires.
- The reviewed local source is the source of truth.
- Existing board identifiers are preserved for updates unless the user explicitly requests a new board.
- The user asked for save, publish, update, or push before any MCP write.
- Local source, successful save, returned edit URL, public deployment, and anonymous verification are reported as separate states.
