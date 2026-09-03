---
name: Folloze-ROI-Calculator-Builder
description: Build a source-branded, buyer-facing ROI calculator, savings model, value estimator, or business-case tool for a Folloze experience. Use when a customer needs an interactive economic model with explicit assumptions, testable formulas, responsive design, and a clear conversion path. Do not use for unsupported ROI claims, binding quotes, or financial advice.
---

# Folloze ROI Calculator Builder

Build a decision tool that lets buyers test the economic case with their own inputs. Make the model transparent enough for finance to audit, simple enough for a buyer to use without training, and useful enough to move the next conversation forward.

## Fit

Use this skill for:

- A standalone ROI calculator or value-estimation experience.
- An interactive calculator section inside a Folloze campaign page, microsite, sales room, or content experience.
- A savings, productivity, revenue-lift, cost-avoidance, payback, or total-value model built from approved assumptions.
- A buyer-facing version of an approved spreadsheet or business case.

Do not use this skill to create a binding price quote, promise a guaranteed outcome, provide financial advice, or turn an unsupported marketing claim into a number. If the user only needs a static value proposition, use the appropriate campaign or microsite builder.

## Required Foundations

- Run `$abm-strategist` for named-account, one-to-one, and one-to-few work. Use its approved audience, business priorities, proof, and narrative structure. Do not invent an account target for a broad campaign or standalone calculator.
- Run `$brand-harvester` for every build before choosing the visual system or writing CSS.
- Store the harvest inside the active project repository. Require a zero CLI exit and `brand.json.validation.status: ok`.
- Review the resolved source, extraction statuses, desktop and mobile screenshots, `source-dna.md`, `folloze-board-brief.md`, `brand-tokens.css`, `asset-manifest.json`, and `brand.json` before designing.
- If the brand source is blocked or incomplete, stop visual design until the user supplies a screenshot, brand guide, or equivalent approved evidence.

## Minimum Inputs

Gather only what is missing:

- Buyer and decision audience.
- Business outcome the model should estimate.
- Approved baseline, improvement assumptions, and sources.
- Input units, currency, locale, and calculation period.
- Investment or price range when ROI or payback is an output.
- Desired outputs and the decision each output should support.
- Low, working, and high scenarios, if approved.
- Brand source and the parent Folloze experience, if one exists.
- CTA and intended follow-up motion.
- Delivery shape: standalone page, reusable section, or module inside an existing experience.

If the economic basis is missing, ask one concise question before creating formulas. Do not fill the gap with generic industry benchmarks unless the user approves a specific public source.

## Model Contract

Define the model before designing the interface. Record every variable in a compact model specification with:

- Variable name and buyer-facing label.
- Input, fixed assumption, or derived output.
- Unit and valid range.
- Default value and source.
- Formula and dependencies.
- Scenario behavior.
- Rounding and display rule.
- Owner or reviewer.

Keep four categories visually and logically distinct:

1. Buyer inputs: values the visitor can change.
2. Approved defaults: editable starting points with a visible source or explanation.
3. Locked assumptions: reviewed constants that the buyer can inspect but not change.
4. Derived outputs: results calculated only from the first three categories.

Never hide a material assumption inside JavaScript. Put it in the model specification and expose it in the methodology or assumptions view.

## Formula Standards

Use formulas that match the approved business case. Common patterns include:

```text
annual_time_value = users * hours_saved_per_user_per_period * periods_per_year * loaded_hourly_cost * adoption_rate

annual_revenue_lift = eligible_volume * baseline_conversion_rate * relative_conversion_lift * average_value

annual_cost_avoidance = current_annual_cost - future_annual_cost

gross_annual_benefit = annual_time_value + annual_revenue_lift + annual_cost_avoidance

net_annual_benefit = gross_annual_benefit - annual_investment

roi_percent = (net_annual_benefit / annual_investment) * 100

payback_months = one_time_investment / monthly_recurring_net_benefit
```

These are patterns, not default claims. Include only the value categories supported by the approved model.

Guard against common model errors:

- Distinguish a relative percentage lift from a percentage-point increase.
- Convert weekly, monthly, quarterly, and annual values to one explicit period before combining them.
- Keep rates as decimals in calculations and percentages in the interface.
- Prevent division by zero and negative payback results that do not have a valid business meaning.
- Do not count the same benefit in more than one output category.
- Use realistic precision. Do not display cents or excessive decimal places when the assumptions are directional.
- Label directional or hypothetical results as estimates.

## Scenario Design

Use low, working, and high scenarios only when each scenario has approved assumptions. Do not create false confidence by multiplying every input by an arbitrary percentage.

- Keep the working scenario visible by default.
- Show which assumptions change between scenarios.
- Let the buyer override editable values without losing the ability to reset.
- Preserve the buyer's values when switching views unless the model explicitly requires a reset.
- Explain whether the scenario changes the baseline, adoption, improvement, investment, or another real driver.

## Experience Design

Start with one primary outcome headline. Put supporting context in the body, model, caption, or assumption note. Never use an eyebrow, headline, and explanatory dek stack.

Build one coherent workbench:

- Put the highest-impact inputs first.
- Pair sliders with accessible numeric fields when ranges are useful.
- Display units in or beside each field.
- Group inputs by business logic, not by arbitrary card count.
- Make the primary result visible without forcing the buyer to scroll through every assumption.
- Show supporting outputs only when they help explain the result or advance the decision.
- Include a plain-language methodology or assumptions view.
- Provide a reset control and a clear empty or invalid state.
- Keep the CTA tied to the modeled decision, such as reviewing assumptions, validating the business case, or planning the next step.
- Match the harvested source's typography, color, spacing, buttons, surfaces, imagery, and interaction language.

Do not use a generic dashboard shell, decorative gradients, fake charts, unexplained gauges, or a grid of equal-weight metrics. The calculator should feel native to the source brand and focused on one economic argument.

## Build Workflow

1. Confirm the calculator's audience, decision, output, delivery shape, and approval boundary.
2. For account-based work, run `$abm-strategist` and inherit the approved account narrative. For broader work, write a short calculator brief covering audience, problem, value hypothesis, proof, model owner, CTA, and constraints.
3. Collect the approved assumptions and their sources. Flag every missing or disputed value.
4. Write the model specification and test it with hand-calculated examples before writing interface code.
5. Run `$brand-harvester`, require `brand.json.validation.status: ok`, and inspect the complete evidence bundle.
6. Choose the interaction model, information hierarchy, and output emphasis.
7. Build one self-contained local HTML file in the active project repository. Keep the model functions separate from rendering and event handlers so formulas can be tested directly.
8. Add input validation, accessible labels, keyboard behavior, reset behavior, methodology disclosure, and responsive states.
9. Add buyer-safe analytics when the environment supports them.
10. Render and inspect desktop near `1440 x 900`, mobile near `390 x 844`, and any width required by the parent Folloze section.
11. Verify the model independently, then complete design, interaction, content, and link QA.
12. Save or publish only when the user has authorized that state change.

## Buyer-Safe Analytics

When publishing through Folloze, follow the current analytics guidance returned by the environment. Useful events can include:

- Calculator opened.
- Input field changed.
- Scenario changed.
- Result calculated.
- Methodology opened.
- CTA clicked.

Track the field name, interaction type, scenario, and result state when useful. Do not capture personal information or raw confidential financial values unless the user has explicitly approved that data collection. Prefer ranges, buckets, or completion states for sensitive inputs.

## Custom HTML Section Capability

Treat custom HTML section placement as a runtime capability, not a guaranteed tool.

- Discover the current Folloze guide and available capabilities at runtime.
- If the environment supports creating or updating a custom HTML section, use that capability only after local model and responsive QA pass and the user authorizes the save.
- Do not hard-code a current or future MCP tool name into the skill.
- If the capability is unavailable, deliver the self-contained HTML and concise placement notes for the Folloze owner.
- Do not replace an entire native board when the user asked for one reusable calculator section.

## State Boundaries

Report these as separate checkpoints:

1. Local model specification complete.
2. Local HTML complete.
3. Formula and responsive QA complete.
4. Folloze draft or save complete.
5. Returned designer or edit URL confirmed.
6. Board published.
7. Public URL confirmed.
8. Anonymous live verification complete.
9. Analytics observed after a real interaction, when requested.

Never describe a local file, saved draft, designer preview, or authenticated browser view as a live public experience.

## QA Gates

Before delivery or publish, verify:

- Every material assumption has an approved source, owner, or explicit review flag.
- Inputs, assumptions, outputs, units, periods, ranges, defaults, and rounding rules match the model specification.
- Zero, minimum, working, maximum, and invalid inputs behave correctly.
- Low, working, and high scenarios match hand-calculated expected results when scenarios exist.
- Relative lifts, percentage-point changes, currency conversion, adoption rates, and time-period conversions are correct.
- ROI and payback formulas handle zero or missing investment safely.
- Reset restores the documented defaults.
- The methodology view explains the calculation without exposing confidential internal notes.
- The primary result and CTA are understandable within one scan.
- The page follows the harvested brand evidence and does not use the prohibited eyebrow, headline, and dek stack.
- Keyboard navigation, visible focus, field labels, contrast, error messages, and reduced-motion behavior are usable.
- Desktop and mobile have no clipping, overlap, horizontal overflow, dead controls, broken links, or console errors from page code.
- Analytics events fire once per intended action and do not leak raw sensitive values.
- The local file, Folloze save, publish state, public URL, and live verification are reported independently.

## Final Response

Return:

- Local HTML path and model-specification path.
- Audience, decision, calculation period, currency, and delivery shape.
- Assumption sources and unresolved review flags.
- Core formulas and scenario status.
- `$abm-strategist` status when applicable.
- `$brand-harvester` path, `brand.json.validation.status`, and visual review status.
- Formula test results and responsive QA status.
- Analytics status and sensitive-data treatment.
- Folloze draft or save status, board ID, edit URL, publish status, public URL, and anonymous verification as separate fields.
