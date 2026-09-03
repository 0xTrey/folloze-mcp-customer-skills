# Folloze MCP Customer Skills

Public customer-facing skill pack for planning and building source-branded Folloze buyer experiences with the Folloze MCP.

This repo is intentionally separate from Folloze internal skill work. It contains only portable, customer-facing skills that a marketer, partner, or implementation team can inspect, QA, and adapt without inheriting internal board, tracker, account, or deal-room operations.

## Included Skills

### Required foundations

| Skill | Use it for |
| --- | --- |
| `abm-strategist` | The **ABM Strategist / Campaign Brief** skill from the live Folloze MCP catalog. It researches a named account or one-to-few cluster, produces the brief, and gets the narrative structure approved before design. |
| `brand-harvester` | Captures the vendor's public design system, source screenshots, reusable brand tokens, approved asset candidates, and a Folloze-ready visual brief before CSS or HTML. |

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
- `brand-harvester` runs for every build. If the public source cannot be inspected, visual design stops until the user supplies a screenshot, brand guide, or equivalent approved evidence.

## Required Workflow

1. Route the campaign motion and complete the correct brief.
2. For account-based work, run `abm-strategist` and get both the brief and narrative structure approved.
3. Run `brand-harvester` and save its durable output under the active project repo, normally `research/brand-harvest/<slug>/`.
4. Require a zero Brand Harvester exit and `brand.json.validation.status: ok`; inspect the resolved source, extraction statuses, and desktop/mobile screenshot pair or approved manual evidence.
5. Review the harvested screenshots, `source-dna.md`, `folloze-board-brief.md`, `brand-tokens.css`, `asset-manifest.json`, and `brand.json`.
6. Build the local HTML only after the required strategy and brand gates pass.
7. Render desktop and mobile, compare the result with the brand evidence, and complete buyer-facing functional QA.
8. Keep local source, Folloze save, returned edit URL, public deployment, and live verification as separate states.

## Install The Current Skill Pack

Clone or update this repository, then copy all seven skill directories into Claude's user skill directory:

```bash
git clone https://github.com/0xTrey/folloze-mcp-customer-skills.git
cd folloze-mcp-customer-skills
mkdir -p ~/.claude/skills
for skill in Skills/*; do cp -R "$skill" ~/.claude/skills/; done
```

The live Folloze MCP catalog currently distributes `abm-strategist` as a `.zip`, not a `.tar.gz`:

```bash
curl -fL https://cdn.folloze.com/flz/skills/abm-strategist.zip -o /tmp/abm-strategist.zip
printf '%s  %s\n' \
  '9a8effd4b60d93569f0ab4313b168ed6ff584a09cabed862c460702181d2f14d' \
  '/tmp/abm-strategist.zip' | shasum -a 256 -c -
unzip -q /tmp/abm-strategist.zip -d ~/.claude/skills
```

The repository install is preferred because it includes the mandatory Brand Harvester dependency and the customer-builder routing that the standalone catalog archive does not include.

## How To Validate

```bash
python3 scripts/validate_customer_skills.py
PYTHONPYCACHEPREFIX=/tmp/folloze-customer-skills-pyc \
  python3 -m py_compile Skills/brand-harvester/scripts/brand_harvest.py
python3 Skills/brand-harvester/scripts/brand_harvest.py --help
```

The validator checks manifest/frontmatter parity, dependency closure, source-lock checksums, mandatory builder hooks, packaged Brand Harvester components, agent prompts, relative Markdown links, and accidental local-path or cache leakage.

## Deliberately Excluded

- Zoom demo-room and post-call deal-room automation skills.
- API/native-template board builders.
- Internal Salesforce, Gmail, Slack, Granola, tracker, or deal-process skills.
- Internal demo-board builder skills.

## Distribution And Marketplace

- [Source provenance](docs/source-provenance.md) records the exact Folloze catalog archive and the Brand Harvester source commit used by this pack.
- [Claude Plugin roadmap](docs/claude-marketplace-plugin-roadmap.md) separates this skill merge from the later Connector-to-Plugin marketplace conversion.

The skills assume the user has access to Folloze MCP publishing tools. They do not hard-code internal tool names. When publishing, follow the current guide returned by the environment and validate the actual HTML before saving.
