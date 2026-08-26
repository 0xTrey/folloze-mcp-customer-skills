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
- Replaced product-specific question-tool mandates with a host-neutral structured-checkpoint contract and concise chat fallback.
- Routed brand selection through `folloze-board-router`: Folloze-owned work uses the public-safe brand kit; external-brand work uses Brand Harvester.

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
- Replaced Claude-only installed paths with the host-neutral `FOLLOZE_SKILLS_DIR` convention.
- Restricted sources and redirects to public HTTP(S) targets. The CLI rejects credentials, localhost, loopback, private, link-local, cloud-metadata, reserved, and unsafe redirect targets before external fetch or browser request continuation.

## Public Quality Core

- Source repository: `https://github.com/0xTrey/Folloze-Skills`
- Source commit: `3c37cc8c4a6938fb7eaa76760e70d83252d1ccfd`
- Source area: `Skills/Folloze-MCP-Demo-Builder/references/`

The customer `folloze-board-quality-core` is a derivative, not a copy of the internal Demo Builder. It retains portable Source Design DNA, experience-shape, copy/proof, responsive, interaction, analytics, accessibility, and save-readiness gates. It excludes internal account systems, board identities, trackers, operator identities, sales systems, and deal workflows. Current derivative checksums are recorded in `skills-source-lock.json`.

## Public-Safe Folloze Brand Kit

- Source repository: `https://github.com/0xTrey/Folloze-Skills`
- Source commit: `3c37cc8c4a6938fb7eaa76760e70d83252d1ccfd`
- Source area: `Skills/folloze-brand-kit/`

This is a purpose-built, rewritten public subset. It contains positioning, voice, visual color tokens, generic product-capability definitions, claims discipline, and campaign-layout guidance. It excludes private document links, internal and customer-ready capability sources, pricing, package rows, credits, order forms, customer proof tables, unverified metrics, competitive strategy, roadmap context, local paths, trackers, and operator details.

Logo binaries are intentionally not redistributed. The user or agent must obtain a current approved Folloze logo from an authorized source for each asset.

## Bundle V3 Authored Skills

The following skills are authored in this customer repository from base commit `2676ae73232caf6aaee3471e887cb2da32a01390`:

- `folloze-board-router`
- `folloze-board-quality-core` wrapper and MCP preflight
- `Folloze-Webinar-Promotion-Page-Builder`

Their file checksums are recorded in `skills-source-lock.json`.

## Webinar Portal Builder

The public `folloze-webinar-portal-builder` was derived from the reusable architecture and staged release gates in the ForgeX-specific live Zoom package at source commit `7c7323ae4b8e42121c831c545aef5d5c9901f104`. All ForgeX event facts, customer naming, source URLs, board identifiers, and assumptions were removed.

The public derivative adds customer-neutral single-event, series-hub, and webinar-platform modes; verified-real versus illustrative-demo source contracts; provider-neutral live routing; public-network protections for the optional Zoom source helper; visual hierarchy rules; and portable Folloze MCP capability discovery. It does not redistribute internal board schemas, template identities, account data, credentials, or provider join tokens. Its file checksums are recorded in `skills-source-lock.json`.

## Licensing Review Required

This repository currently has no license file. Do not infer MIT, Apache, proprietary, or brand-asset redistribution rights from its public visibility. The repository owner should confirm the intended license for original code, terms for repackaging the catalog skill, and Folloze brand-asset permissions before marketplace or third-party redistribution.
