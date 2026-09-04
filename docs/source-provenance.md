# Skill Source Provenance

## `abm-strategist`

- Active upstream: user-provided Board MCP QA attachment
- Source filename: `abm-strategist-SKILL.md`
- Received and verified: 2026-08-14
- Upstream `SKILL.md` SHA-256: `9f087a74cf6917bfab91ca319c71af229a3bad6fc5d4b0b248d16c72981805ab`
- Declared upstream version: ABM Strategist 2.0
- Customer-pack hardening version: ABM Strategist 2.1

This QA attachment replaces the original HTML-designer handoff with a template-based Board MCP flow: approve the brief, choose and describe a real template, approve the story-to-section mapping, create and verify a draft board, and publish only after explicit approval.

Historical catalog snapshot, re-verified 2026-08-14:

- Catalog: `https://engage.folloze.com/follozemcp`
- Source archive: `https://cdn.folloze.com/flz/skills/abm-strategist.zip`
- Archive SHA-256: `9a8effd4b60d93569f0ab4313b168ed6ff584a09cabed862c460702181d2f14d`
- Archived `SKILL.md` SHA-256: `38dd381b30791037da9442895750a3d1f83ee8e7dc8da4b51c07363d3adec06a`

The live catalog archive still serves the older pre-2.0 Campaign Brief skill. It is retained here only as a historical provenance checkpoint and should not be used for Board MCP 2.0 QA.

Customer-pack compatibility changes:

- Removed the hard-coded Claude connector UUID and select the active Board MCP by function names; Codex uses `folloze-board-staging` when available.
- Made structured checkpoints portable: Claude `AskUserQuestion`, Codex `request_user_input` when exposed, or a concise inline checkpoint fallback.
- Updated customer builders so a normal Board MCP request stays in `abm-strategist`; local HTML builders run only when explicitly requested.
- Added `agents/openai.yaml` for the repository's existing agent metadata convention.
- Added a three-mode route contract: custom MCP/HTML, template-based MCP, and native traditional Folloze.
- Added a typed builder handoff, parent-account narrative ownership, decision-tool selection, and repair-mode
  approval carry-forward based on Hupo board-build regression evidence.

The QA attachment contains no license file or checksum manifest. Treat it as Folloze-provided QA source and retain this provenance record when repackaging it.

## `brand-harvester`

- Source repository: `https://github.com/0xTrey/Folloze-Skills`
- Source commit: `04d3482064a3ae8083af13ca4557dff515fc9ce1`
- Source date: 2026-06-03
- Upstream `SKILL.md` SHA-256: `0fd1e2f3060270eec7da1d91d19027207d20cf9328afbd766323e7b1cc38d437`
- Upstream `agents/openai.yaml` SHA-256: `4cae1f086b47f39a3b6e989e576f90cc10613e916d248d08eb064ba678219c52`
- Upstream CLI reference SHA-256: `2e1098e6b304abd5b809e462e85f4b0bf24f7e3dd0c9526869064d5832cb8f55`
- Upstream CLI SHA-256: `4af853775a8f7c88994e2aa3c73fd78feb98442536ff1cd5b737d0a24c2e7cea`

The full portable skill tree is bundled: `SKILL.md`, agent metadata, CLI reference, and the standard-library Python CLI. Cache files are excluded.

Customer-pack compatibility changes:

- Removed assumptions about a separate local Folloze-Skills checkout.
- Routed the output to the active customer builder.
- Made blocked-source handling fail closed: the builder waits for approved screenshots or brand evidence instead of inventing a generic visual system.
- Made the CLI return status `incomplete` and exit code `2` when source extraction or required visual evidence is missing; diagnostic output files no longer authorize a build.
- Removed Trey-specific internal wording from the CLI reference.
- Added requirement-aware vendor and target logo acceptance, effective nested button-label extraction,
  headline-punctuation and section-rhythm capture, and a Custom Theme handoff object.
