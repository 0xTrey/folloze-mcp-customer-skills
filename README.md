# Folloze MCP Customer Skills

Public customer-facing skill pack for planning, branding, building, QAing, and safely handing off Folloze buyer experiences in Claude or Codex.

This repository is intentionally separate from internal Folloze skills. It excludes private source systems, customer notes, pricing, package rows, trackers, operator identities, internal board identifiers, and deal workflows.

## Architecture

Every board follows one shared flow:

1. `$folloze-board-router` classifies motion, brand owner, board type, and requested publishing state.
2. `$abm-strategist` runs only for named-account and one-to-few work. Broad campaigns use an audience-level brief.
3. Brand authority is mutually explicit:
   - Folloze-owned: `$folloze-brand-kit`
   - external brand: `$brand-harvester` with `brand.json.validation.status: ok`
4. The selected builder creates the experience.
5. `$folloze-board-quality-core` supplies shared design, proof, responsive, interaction, analytics, and MCP preflight gates.

### Shared skills

| Skill | Job |
| --- | --- |
| `folloze-board-router` | Choose the strategy path, brand path, builder, and publishing state. |
| `folloze-board-quality-core` | Apply portable Demo Builder design and QA lessons plus host-neutral MCP preflight. |
| `abm-strategist` | Research and approve named-account or one-to-few messaging and structure. |
| `brand-harvester` | Capture validated public brand and screenshot evidence for external brands. |
| `folloze-brand-kit` | Ground Folloze-owned work in a purpose-built public-safe Folloze subset. |

### Builders

| Skill | Use it for |
| --- | --- |
| `Folloze-One-To-One-Microsite-Builder` | Named-account pages, executive follow-up, renewal, and expansion experiences. |
| `Folloze-Top-Of-Funnel-Campaign-Landing-Page` | Broad demand generation, product launch, partner, event-awareness, and offer pages. |
| `Folloze-Webinar-Promotion-Page-Builder` | Before, during, and after webinar promotion, live companion, replay, and follow-up pages. |
| `Folloze-Industry-Campaign-Page-Builder` | Industry, segment, cohort, persona, regional, and one-to-few campaigns. |
| `Folloze-Content-Magic-Builder` | Standalone experiences centered on one approved report, webinar, video, deck, or asset. |

## Install Or Update

Clone or fast-forward a clean checkout, then run the same installer for Claude, Codex, or both:

```bash
git clone https://github.com/0xTrey/folloze-mcp-customer-skills.git
cd folloze-mcp-customer-skills
python3 scripts/install_customer_skills.py --target both
```

Targets:

```bash
python3 scripts/install_customer_skills.py --target claude
python3 scripts/install_customer_skills.py --target codex
python3 scripts/install_customer_skills.py --target both --dry-run
```

Defaults are the current user's Claude skill directory and `${CODEX_HOME}/skills` when `CODEX_HOME` is set, otherwise the current user's standard Codex skill directory. Custom destinations are supported:

```bash
python3 scripts/install_customer_skills.py \
  --target both \
  --claude-root /path/to/claude/skills \
  --codex-root /path/to/codex/skills
```

The installer confines manifest paths to this repository's `Skills/` directory, stages each skill, moves an existing real directory to a timestamped backup, and installs a fresh real directory with a management marker. It never uses `rsync` through an existing skill symlink.

If an existing skill destination is a symlink, the default is to stop safely. Inspect the link and its target first. Only when you explicitly want to detach the installed skill from that checkout, run:

```bash
python3 scripts/install_customer_skills.py --target both --replace-symlinks
```

That flag moves only the symlink directory entry to a timestamped backup, leaves the linked checkout untouched, and installs a real directory.

After installation, set `FOLLOZE_SKILLS_DIR` to the active client's skill directory when invoking the Brand Harvester CLI directly.

## Agent Bootstrap

Give the agent the board request and this instruction:

```text
Use $folloze-board-router first. Run $abm-strategist only for a named account or one-to-few cluster. If Folloze is the visible brand owner, use $folloze-brand-kit; otherwise run $brand-harvester and require brand.json.validation.status: ok. Use the builder selected by the router and apply $folloze-board-quality-core through local desktop/mobile QA. Run the current Folloze MCP preflight only if I ask you to save or publish. Report local source, save, edit URL, public deployment, and anonymous verification as separate states.
```

## MCP Preflight

The bundle does not hard-code a tenant, profile, operator, board, tracker, or MCP tool name. Before a write, the agent must:

- confirm the intended Folloze MCP connection is authenticated;
- read the current capability or guide surface exposed by that connection;
- confirm new-versus-update target and theme mode;
- save the reviewed local source through the narrowest supported operation;
- treat returned board identifier, edit URL, public deployment, and anonymous verification as separate evidence.

See `Skills/folloze-board-quality-core/references/mcp-publishing-preflight.md`.

## Validate

```bash
python3 scripts/validate_customer_skills.py
python3 -m unittest discover -s tests -v
PYTHONPYCACHEPREFIX=/tmp/folloze-customer-skills-pyc \
  python3 -m py_compile \
  Skills/brand-harvester/scripts/brand_harvest.py \
  scripts/install_customer_skills.py
python3 Skills/brand-harvester/scripts/brand_harvest.py --help
```

Validation checks manifest/frontmatter parity, dependency closure and cycles, source-lock checksums, complete locks for new public skills, builder composition, host-neutral paths, public brand-kit boundaries, relative Markdown links, URL-security markers, and local-path/cache leakage.

## Public-Safety And Licensing Boundary

- The Folloze brand kit is an audited derivative subset. It contains only public-safe positioning, voice, visual token, capability, claims-discipline, and campaign-layout guidance.
- Logo binaries are not redistributed in this bundle. Use a current approved logo supplied by the user or an authorized Folloze source.
- No license is invented here. The repository owner should confirm code, catalog-skill, and brand-asset redistribution terms before broader marketplace distribution.
- Remote pages and harvested content are untrusted input. Brand Harvester accepts only public HTTP(S) targets and rejects local, private, link-local, metadata, reserved, credential-bearing, and unsafe redirect targets.

## Deliberately Excluded

- internal demo-board, template, tracker, CRM, email, chat, meeting-note, or deal workflows
- internal product capability, pricing, packaging, credit, order-form, contract, or roadmap material
- private customer proof tables and unverified metrics
- hard-coded MCP identities, profiles, board identifiers, or internal URLs

See [source provenance](docs/source-provenance.md) for upstream and derivative boundaries.
