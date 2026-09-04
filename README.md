# Folloze MCP Customer Skills

Public customer-facing skill pack for planning and building source-branded Folloze buyer experiences with the Folloze MCP.

This repo is intentionally separate from Folloze internal skill work. It contains only portable, customer-facing skills that a marketer, partner, or implementation team can inspect, QA, and adapt without inheriting internal board, tracker, account, or deal-room operations.

## Included Skills

### Required foundations

| Skill | Use it for |
| --- | --- |
| `abm-strategist` | The **ABM Strategist 2.1** skill. It researches a named account, creates a leadership-grade account argument, chooses the construction mode, and hands a binding contract to the correct builder. It builds directly only for template-based MCP boards. |
| `brand-harvester` | Captures the vendor's public design system, required co-brand assets, source screenshots, role-specific button families, headline conventions, reusable tokens, and Custom Theme candidates. |

### Customer builders

| Skill | Use it for |
| --- | --- |
| `Folloze-Top-Of-Funnel-Campaign-Landing-Page` | Broad demand-gen, paid-media, event-awareness, product-launch, partner, and resource-offer landing pages. |
| `Folloze-One-To-One-Microsite-Builder` | Named-account ABM pages, executive follow-up pages, renewal/expansion microsites, and account-specific buyer experiences. |
| `Folloze-Industry-Campaign-Page-Builder` | Industry, segment, cohort, persona, event-audience, and one-to-few campaign pages. |
| `Folloze-Content-Magic-Builder` | Interactive Folloze experiences created from a whitepaper, report, ebook, webinar, deck, video, guide, or other approved content item. |
| `Folloze-ROI-Calculator-Builder` | Source-branded ROI calculators, savings models, value estimators, and business-case tools with explicit assumptions and tested formulas. |

Every builder declares both foundations as install dependencies. Runtime routing stays honest:

- `abm-strategist` runs for one-to-one, one-to-few, and named account-cluster work. Broad one-to-many and standalone content motions do not invent a target account just to satisfy an ABM intake.
- `mcp_html` routes to the one-to-one builder for a custom MCP/HTML experience.
- `mcp_template` stays in `abm-strategist` for template selection, section mapping, and Board MCP draft creation.
- `native_traditional` routes to the industry builder for native sections, native content, Custom Theme, and Designer personalization. HTML cannot replace that deliverable.
- `brand-harvester` runs before every material design build. If required vendor or target logos, source evidence, or visual evidence are incomplete, visual design stops.
- Personalized domain variants are views of one board, not additional board builds.

## Required Workflow

1. Route the campaign motion, choose `mcp_html`, `mcp_template`, or `native_traditional`, and complete the builder handoff.
2. For account-based work, run `abm-strategist`. In repair mode, carry forward the approved brief unless seller, target, offering, CTA, motion, or build mode changes.
3. Run `brand-harvester`, save its durable output under the active project repo, and require `brand.json.validation.status: ok`. Co-branded work must also pass target-logo acceptance.
4. Build through the selected mode. Never substitute HTML for native traditional work or force custom HTML through a template path.
5. Include one decision-advancing interaction. Use the ROI Calculator skill only when approved assumptions and a model owner exist.
6. Verify account narrative ownership, header co-branding, copy specificity, composition variety, rendered button labels, desktop/mobile behavior, and CTA actions.
7. For domain personalization, verify the generic fallback and each exact-domain view have different logos, copy, native content, and CTA context.
8. Keep local source, save, readback, draft preview, publish, anonymous verification, install, commit, and push as separate states.

## Install The Current Skill Pack

Clone or update this repository, then copy all seven skill directories into the client skill directory.

Claude:

```bash
git clone https://github.com/0xTrey/folloze-mcp-customer-skills.git
cd folloze-mcp-customer-skills
mkdir -p ~/.claude/skills
for skill in Skills/*; do cp -R "$skill" ~/.claude/skills/; done
```

Codex:

```bash
git clone https://github.com/0xTrey/folloze-mcp-customer-skills.git
cd folloze-mcp-customer-skills
for skill in Skills/*; do
  name="${skill##*/}"
  mkdir -p "$HOME/.codex/skills/$name"
  cp -R "$skill/." "$HOME/.codex/skills/$name/"
done
```

As verified on 2026-08-14, the live catalog archive still serves the older pre-2.0 Campaign Brief skill. Do not use that archive for Board MCP 2.0 QA. The repository install carries the reviewed QA attachment, the client-portability adaptations, Brand Harvester, and the updated customer-builder routing.

## How To Validate

```bash
python3 scripts/validate_customer_skills.py
PYTHONPYCACHEPREFIX=/tmp/folloze-customer-skills-pyc \
  python3 -m py_compile Skills/brand-harvester/scripts/brand_harvest.py
python3 Skills/brand-harvester/scripts/brand_harvest.py --help
```

The validator checks manifest/frontmatter parity, dependency closure, source-lock checksums, mandatory builder
hooks, packaged Brand Harvester components, agent prompts, relative Markdown links, accidental local-path or
cache leakage, build-mode hardening, and the Bank of America and FinServ Highspot-replacement regression
fixtures.

## Deliberately Excluded

- Zoom demo-room and post-call deal-room automation skills.
- Internal tenant-specific API implementations, credentials, IDs, and browser automation details. The public
  native-traditional contract remains portable and tool-agnostic.
- Internal Salesforce, Gmail, Slack, Granola, tracker, or deal-process skills.
- Internal demo-board builder skills.

## Distribution And Marketplace

- [Source provenance](docs/source-provenance.md) records the exact Folloze catalog archive and the Brand Harvester source commit used by this pack.
- [Claude Plugin roadmap](docs/claude-marketplace-plugin-roadmap.md) separates this skill merge from the later Connector-to-Plugin marketplace conversion.

The skills assume the user has access to the relevant Folloze MCP, native board, or Designer capabilities.
They do not hard-code internal tenant tools. Before saving, validate the actual artifact for its selected
construction mode.
