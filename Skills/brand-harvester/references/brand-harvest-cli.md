# Brand Harvester CLI

Use `scripts/brand_harvest.py` when a Folloze board, ABM page, or GTM asset needs a fast, structured source-brand capture before writing or revising HTML.

## When To Use

- The input is a vendor domain, source URL, or account name.
- The board needs vendor-faithful styling, source-site buttons, source-owned assets, and visual rhythm before copy/layout work starts.
- The user has a GoFullPage screenshot or wants a repeatable full-page visual capture.
- A future workflow needs machine-readable brand inputs rather than only working notes.

## Command

```bash
python3 "${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}/brand-harvester/scripts/brand_harvest.py" \
  forcepoint.com \
  --target "Mayo Clinic"
```

For a specific source page:

```bash
python3 "${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}/brand-harvester/scripts/brand_harvest.py" \
  forcepoint.com \
  --source-url https://www.forcepoint.com/platform
```

To include a GoFullPage or other manual screenshot:

```bash
python3 "${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}/brand-harvester/scripts/brand_harvest.py" \
  forcepoint.com \
  --manual-screenshot ./screenshots/forcepoint-gofullpage.png
```

By default, output goes to a timestamped directory under `/tmp/folloze-brand-harvest/`. For durable board work, pass an output directory inside the active board repo, for example:

```bash
python3 "${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}/brand-harvester/scripts/brand_harvest.py" \
  forcepoint.com \
  --out research/brand-harvest/forcepoint
```

For a vendor page where the source page is the visual truth but the home page may carry broader brand patterns, run both harvests:

```bash
python3 "${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}/brand-harvester/scripts/brand_harvest.py" \
  younion.live \
  --source-url https://www.younion.live/our-work/aws-gen-ai-loft \
  --target AWS \
  --out research/brand-harvest/younion-aws-gen-ai-loft
python3 "${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}/brand-harvester/scripts/brand_harvest.py" \
  younion.live \
  --source-url https://www.younion.live/ \
  --target AWS \
  --out research/brand-harvest/younion-home
```

For co-branding, require the target logo and provide at least one official candidate:

```bash
python3 "${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}/brand-harvester/scripts/brand_harvest.py" \
  vendor.example \
  --target "Target Account" \
  --require-logo target \
  --target-logo https://target.example/assets/official-wordmark.svg \
  --target-logo-source https://target.example/brand-center \
  --out research/brand-harvest/vendor-target
```

Vendor logo is always required. `--require-logo target` adds the co-brand requirement. Repeat
`--target-logo` when several official dark, light, or horizontal variants should be tested. Record the
official brand-center, press-kit, or user-provided provenance with `--target-logo-source`.

## Outputs

- `brand.json`: full structured capture, including the structured brain pool.
- `source-dna.md`: working note in the Source Design DNA format.
- `folloze-board-brief.md`: board-builder-ready design and asset brief.
- `brand-tokens.css`: candidate CSS variables for colors, fonts, buttons, and cards.
- `asset-manifest.json`: logo, image, background, Brandfetch, screenshot, and manual screenshot candidates.
- `screenshots/homepage-desktop-full.png`: Chrome full-page capture when available.
- `screenshots/homepage-mobile-full.png`: Chrome mobile full-page capture when available.

The CLI writes diagnostic outputs even when evidence is incomplete. A successful gate requires:

- exit code `0`;
- top-level summary status `ok`;
- `brand.json.validation.status` equal to `ok`;
- a resolved source URL;
- successful basic HTML or complete desktop/mobile DevTools extraction;
- a desktop/mobile screenshot pair or at least one copied manual screenshot.
- every required logo role accepted under `brand.json.validation.asset_requirements`.

Exit code `2` and status `incomplete` mean the bundle is diagnostic only and must not authorize visual design.

## Harvest Layers

1. Input resolver:
   - Accepts domain, source URL, or account name.
   - For account names, tries likely domains and a bounded search fallback.

2. Brandfetch:
   - Uses `BRANDFETCH_API_KEY` or `--brandfetch-token` when available.
   - Calls the Brandfetch domain endpoint for logos, colors, fonts, and brand metadata.
   - Skips cleanly when no token is available.

3. Basic HTML:
   - Fetches source HTML with standard library tooling.
   - Extracts title, meta tags, headings, links, images, stylesheets, colors, fonts, and CSS variables.

4. Chrome DevTools:
   - Uses local Chrome/Chromium directly through DevTools Protocol.
   - Extracts computed colors, fonts, CSS variables, role-specific button families, effective rendered label
     styles, cards, full-width section rhythm, headline punctuation, logos, proof links, CTA text, interaction
     patterns, and responsive metrics.
   - Captures desktop and mobile full-page screenshots.

5. Manual screenshot intake:
   - Copies GoFullPage or other manual screenshots into the bundle when `--manual-screenshot` is supplied.

## Board Builder Use

Use `source-dna.md`, `folloze-board-brief.md`, `brand-tokens.css`, `asset-manifest.json`, `theme_handoff`, and screenshots before writing page HTML or a Folloze Custom Theme. The output is working context, not buyer-facing copy.

Brand harvest is the required first visual step for new vendor-branded boards and material redesigns unless the user explicitly provides an approved equivalent evidence bundle. Preserve the harvest bundle with the board source and QA artifacts so future updates can reuse the same brand evidence.

Before saving through Folloze MCP, still run the normal gates:

- official logo verification
- required vendor and target logo acceptance for co-branding
- source-site button treatment verification
- rendered nested-label style verification
- headline-punctuation and full-width section-rhythm verification
- link and CTA analytics checks
- mobile overflow checks
- asset render checks
- MCP theme/link requirements

## Known Limits

- Account-name resolution is best effort. A domain or source URL is higher confidence.
- Screenshots require a local Chrome, Chromium, or Edge executable.
- Brandfetch enrichment requires an API token.
- The tool extracts design facts from public pages; it should not copy a source page pixel-for-pixel.
