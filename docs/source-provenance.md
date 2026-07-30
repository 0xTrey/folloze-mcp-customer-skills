# Skill Source Provenance

## `abm-strategist`

- Catalog: `https://engage.folloze.com/follozemcp`
- Source archive: `https://cdn.folloze.com/flz/skills/abm-strategist.zip`
- Download verified: 2026-07-30
- Archive SHA-256: `9a8effd4b60d93569f0ab4313b168ed6ff584a09cabed862c460702181d2f14d`
- Upstream `SKILL.md` SHA-256: `38dd381b30791037da9442895750a3d1f83ee8e7dc8da4b51c07363d3adec06a`
- Last-Modified: `2026-07-09T07:27:26Z`
- ETag: `a3c00783ef7768ce6536708d0226cf93`
- S3 version ID: `7s4Jwbu5LSVwUgWjGuo8DQXeiTdTyqiZ`

The live catalog labels this package “Plan the campaign.” It is the catalog's Campaign Brief capability and is scoped to one-to-one and one-to-few account campaigns. No separate broad Campaign Brief package was listed on the catalog when verified.

Customer-pack compatibility changes:

- Added an explicit routing section so broad one-to-many builders do not invent a target account.
- Routed approved briefs to this repo's one-to-one or industry/one-to-few customer builder instead of the separately distributed `abm-page-designer`.
- Added `agents/openai.yaml` for the repository's existing agent metadata convention.

The upstream archive contains no license file, checksum manifest, or semantic version. Treat it as Folloze-distributed source and retain this provenance record when repackaging it.

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
