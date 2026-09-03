---
name: folloze-roi-calculator-builder
description: Build, revise, audit, or package a buyer-facing ROI or value calculator for a Folloze experience. Use when a user needs a finance-defensible value model, a stakeholder interview, a reusable Qwen or ChatGPT builder prompt, an on-brand self-contained HTML calculator, calculator QA, or a gated handoff for a future Folloze custom HTML section.
---

# Folloze ROI Calculator Builder

Create an evidence-backed decision tool, not a decorative lead form. Establish the economics first, obtain approval for the model, then design and build a source-branded interactive experience.

## Choose The Operating Mode

Use the narrowest mode that satisfies the request:

1. **Prompt package**: adapt the [master builder prompt](references/master-builder-prompt.md) into a shareable prompt that interviews the stakeholder and produces the full calculator package.
2. **Model discovery**: interview the stakeholder, register evidence and assumptions, define the formulas, and stop at an approvable model contract.
3. **Local calculator build**: complete discovery, brand harvest, design, implementation, deterministic tests, and responsive QA in the active project repo.
4. **Audit or revision**: inspect an existing prompt, model, or calculator; identify unsupported claims, financial errors, double counting, broken interactions, design drift, or release gaps; change only the requested scope.
5. **Folloze handoff**: prepare or execute an authorized MCP save only after the local build and release gates pass. Follow the [Folloze release contract](references/folloze-release-contract.md).

Do not force a build when the user only needs the reusable prompt or model. Do not call a value estimate an ROI calculator when investment is missing.

## Required Foundations

- Run `$abm-strategist` before design when the calculator is for a named account, one-to-few campaign, or named account cluster. Use its approved brief and narrative structure. Do not invent a target account for one-to-many work.
- Run `$brand-harvester` for every HTML build before choosing the visual system or writing CSS. Store the evidence bundle in the active project repo, require a zero CLI exit and `brand.json.validation.status: ok`, and review the resolved source, extraction statuses, desktop and mobile screenshots, `source-dna.md`, `folloze-board-brief.md`, `brand-tokens.css`, `asset-manifest.json`, and `brand.json`.
- If `$brand-harvester` cannot inspect the approved source, stop visual design until the user supplies screenshots, a brand guide, or equivalent approved evidence.
- Prompt-package mode does not require a live harvest. The delivered prompt must still require `$brand-harvester` or equivalent approved brand evidence before its model generates HTML.

## Source And Evidence Rules

Use sources in this order:

1. customer facts from an owned system of record or a named owner;
2. vendor facts and product claims approved for this calculator;
3. dated published benchmarks with traceable scope and methodology;
4. explicitly chosen scenario values;
5. clearly labeled provisional assumptions.

Never invent pricing, baselines, benchmarks, product capabilities, customer outcomes, citations, approval, or publication state. Do not treat an example calculator as evidence. Classify every material number as `CUSTOMER_FACT`, `VENDOR_FACT`, `PUBLISHED_BENCHMARK`, `SCENARIO_CHOICE`, `EXPLICIT_ASSUMPTION`, or `DERIVED_VALUE`.

For each material number, record:

- label and stable input ID;
- value, unit, period, currency, and eligible scope;
- classification and direct source;
- named owner and as-of date;
- confidence and validation status;
- notes, limitations, and where the value is used.

Mark unavailable evidence `unverified`. If conflicting sources would materially change the result, show the conflict and stop for the named owner to decide.

## Workflow

### 1. Establish The Decision

Ask questions in short rounds. Combine source and capability intake with the highest-priority decision questions, and ask no more than seven questions total in any round. First resolve:

- vendor, product, bundle, or use case;
- primary buyer and calculator user;
- one-to-one, one-to-few, or one-to-many motion;
- decision the buyer should make;
- one or two leading business outcomes;
- placement in the buying journey and next action;
- owners for economics, product claims, brand, legal, privacy, technical delivery, and release.

Accept `unknown`. Identify the likely owner instead of guessing.

### 2. Select The Value Streams

Use only value streams with an explainable causal and financial link. Common candidates include:

- retained recurring revenue or reduced churn;
- expansion or customer-qualified pipeline;
- productivity capacity and coverage;
- avoided hiring, overtime, or contractor spend;
- software and service consolidation;
- support deflection and self-service;
- education and training delivery;
- onboarding, adoption, or time-to-value, only when tied to an approved financial outcome.

Keep separate streams separate. Do not monetize health scores, engagement, NPS, adoption, time-to-value, forecast accuracy, or risk signals without an approved causal and financial link.

### 3. Build The Model Contract

Define the model before writing copy or code. For every value stream specify:

- eligible population or economic base;
- current baseline and proposed change;
- attribution, adoption, confidence, and ramp factors;
- timing and realization period;
- formula, units, dependencies, and output label;
- excluded overlap with other streams;
- owner and approval state.

Register all investment categories a finance reviewer would expect: subscription, implementation, services, integration, internal labor, enablement, change management, ongoing administration, and transition or exit costs when applicable.

Keep these outputs distinct:

```text
Gross benefit
Realized benefit
Investment
Net benefit
ROI
Benefit-cost ratio
Payback period
NPV, when requested and supported
```

Use the formulas, scenarios, and anti-double-counting checks in the [master builder prompt](references/master-builder-prompt.md). Use `ROI_READY` only when the required investment and benefit evidence are sufficiently complete. Use `VALUE_ESTIMATE_ONLY` when gross value can be modeled but investment cannot. Use `BLOCKED` when a material unknown or conflict prevents an honest estimate.

### 4. Review Before Experience Design

Return an approval packet containing:

- calculator thesis and buyer decision;
- model status;
- source and assumption ledger;
- formula registry with plain-language explanations;
- conservative, expected, and upside scenarios;
- sensitivity drivers;
- double-counting review;
- unresolved evidence and named owners;
- versioned approval checklist.

Do not generate HTML until the stakeholder approves the model direction or explicitly asks for a labeled prototype based on provisional assumptions.

### 5. Create A Prompt Package

When the user asks for a prompt they can give another model:

1. Read the complete [master builder prompt](references/master-builder-prompt.md).
2. Replace generic language only with approved vendor, product, buyer, and source details.
3. Keep the evidence, finance, security, brand, accessibility, analytics, QA, and action boundaries intact.
4. Remove research seeds or defaults that are not approved for the customer.
5. Preserve the short-round interview behavior and the requirement to approve the model before code generation.
6. Save the result as a standalone Markdown file in the active project repo.
7. Provide a short share note that explains what the recipient should attach and what the prompt will produce.

The prompt must be usable in Qwen, ChatGPT, or another capable coding model without relying on hidden context.

### 6. Design The Experience

After model approval, run the required strategy and brand foundations. Design around the buyer's decision and the strongest sensitivity drivers.

- Use one primary headline. Do not use an eyebrow, headline, and dek stack.
- Prefer a focused workbench when it fits the buyer job.
- Keep the main experience to four to six high-value controls; move secondary assumptions into a labeled detail panel.
- Show what changed, why it changed, how it was calculated, and which assumptions matter most.
- Provide conservative, expected, and upside scenarios without implying certainty.
- Show useful value before requesting contact information.
- Use direct language such as `modeled`, `potential`, `estimated`, or `directional`.
- Match the approved source brand's typography, spacing, color, controls, imagery, section rhythm, and responsive behavior.
- Do not create or modify logos, average two brands into one system, or copy a public page pixel for pixel.

### 7. Build The Local Artifact

Create one self-contained HTML document or one namespaced HTML fragment, according to the requested placement. Keep CSS and JavaScript inline unless the approved host contract says otherwise. Use no build step and no external runtime dependencies by default.

For a fragment:

- mount inside one namespaced root;
- prefix IDs, classes, data attributes, CSS variables, and custom events;
- avoid global selectors and host assumptions;
- keep calculation functions pure and separate from rendering;
- expose one idempotent mount function plus cleanup behavior;
- use event listeners, not inline handlers;
- reject `eval`, dynamic code execution, and unsafe `innerHTML`;
- make network requests, storage, cookies, PII capture, and external libraries opt-in only;
- use real approved destinations for every CTA and link;
- fail safely if the host strips scripts.

Preserve the local HTML and model files as the source of truth. Never invent a deployment or Folloze URL.

### 8. Test And Review

Before handoff, verify:

- formula test vectors for conservative, expected, and upside scenarios;
- zero, missing, negative, extreme, and locale-formatted inputs;
- percentage-point versus relative-percentage behavior;
- currency and period consistency;
- rounding and visible reconciliation from components to totals;
- no double counting across value streams;
- no raw financial inputs or PII in analytics payloads;
- every slider, selector, drawer, print action, link, and CTA works;
- semantic labels, keyboard access, visible focus, contrast, live-region behavior, and reduced motion;
- desktop near `1440 x 900` and mobile near `390 x 844` render cleanly;
- no clipping, overlap, layout shift, horizontal overflow, placeholder destinations, or dead controls;
- buyer-facing claims and caveats match the approved evidence ledger.

Run both a design-fidelity review against the `$brand-harvester` evidence and a separate buyer-facing functional review. Fix blocking issues or report them explicitly.

### 9. Prepare The Folloze Handoff

Read and follow the [Folloze release contract](references/folloze-release-contract.md). At runtime, use the current Folloze guide returned by the environment. If no current guide or tool schema is exposed, stop at the local handoff and report that limitation. Do not hard-code or infer an MCP tool that is not actually available.

Never collapse these states into one completion claim:

1. model approved;
2. local artifact generated;
3. local QA passed;
4. Folloze MCP draft or section saved;
5. board published;
6. anonymous live experience verified;
7. analytics delivery verified;
8. source committed;
9. source pushed.

An explicit request to build locally is not authorization to save or publish in Folloze. An MCP save is not publication. Publication is not anonymous verification. Local event tests are not production analytics delivery.

## Final Receipt

Report:

- operating mode and model status;
- vendor, product or use case, buyer, and primary decision;
- approved value streams and formula version;
- source ledger and unresolved assumptions;
- prompt, model, HTML, and QA artifact paths;
- strategy and brand evidence paths and review status;
- deterministic, responsive, accessibility, interaction, and claim QA status;
- exact Folloze board, page, and section only if verified and in scope;
- Folloze save, publish, anonymous verification, and analytics states separately;
- Git commit and push states separately;
- blockers, owners, and the next safe action.

Do not say `production ready`, `finance approved`, `brand approved`, `published`, or `verified` without direct evidence for that exact state.
