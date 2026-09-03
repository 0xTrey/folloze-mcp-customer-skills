---
name: folloze-analytics-tracking
description: Apply Folloze click and interaction tracking to customer-facing HTML before any Folloze save or publish. Use for CTAs, links, navigation, calculators, tabs, accordions, media controls, and other meaningful interactions that must appear in Folloze Pulse and supported external analytics.
---

# Folloze Analytics Tracking

Instrument the experience with the current Folloze MCP analytics contract. Track meaningful buyer actions without exposing raw financial inputs, account-confidential values, free text, credentials, or personally identifiable information.

## Authority And Precedence

1. Read the current Folloze board creation guide or landing page creation guide exposed by the active MCP connection.
2. Read the analytics acknowledgement fields required by the active save tool.
3. Apply this skill to the actual interactive HTML.

The current guide and save schema override examples or older catalog archives. Do not inject a custom analytics bridge, reach into `window.board`, or call undocumented Folloze controllers unless the current guide explicitly requires that exact integration.

If the live guide or save schema is unavailable, stop before Folloze save or publish. A local HTML build may continue only when it is clearly labeled as not ready for Folloze analytics verification.

## Required Tracking Contract

Use the global `flzAnalytic(actionName, payload, sourceElement)` interface documented by the current Folloze guide.

For every CTA and external link, use a direct inline call so the Folloze save validator can inspect it:

```html
<a href="https://example.com/demo"
   target="_blank"
   rel="noopener"
   onclick="flzAnalytic('cta_click', {text:this.innerText.trim(), area:'calculator results'}, this)">
  Review the recommendation
</a>
```

Use stable underscore action names. Examples include:

- `cta_click`
- `nav_click`
- `calculator_started`
- `calculator_input_changed`
- `calculator_scenario_changed`
- `calculator_results_viewed`
- `calculator_assumptions_opened`
- `calculator_summary_printed`
- `validation_error`

Every payload must contain:

- `text`: a visible label or a safe stable control label;
- `area`: the page region where the interaction occurred.

Pass the source element as the third argument when one exists. For external destinations, always use `target="_blank" rel="noopener"` so navigation does not interrupt the analytics request.

## Composite And Calculator Controls

Interactive calculators may keep their existing JavaScript and event listeners. Each meaningful state change must also call `flzAnalytic` with a safe payload.

```javascript
function trackCalculatorAction(actionName, text, area, sourceElement) {
  if (typeof window.flzAnalytic !== "function") return;
  window.flzAnalytic(actionName, { text, area }, sourceElement || null);
}

scenarioSelect.addEventListener("change", function () {
  trackCalculatorAction(
    "calculator_scenario_changed",
    this.options[this.selectedIndex].text.trim(),
    "calculator controls",
    this
  );
});
```

Do not place raw currency values, percentages, customer metrics, account names, email addresses, free text, or exact modeled results in analytics payloads. Use safe categories such as input ID, scenario label, result band, validation type, calculator version, and page area.

## Navigation And Internal Movement

Do not use raw `href="#section"` anchors inside Folloze-hosted pages. Use a button with `type="button"` and a stable `data-scroll-target`, then call `scrollIntoView()` and emit a tracked navigation event.

```html
<button type="button"
        data-scroll-target="roi-results"
        onclick="flzAnalytic('nav_click', {text:this.innerText.trim(), area:'calculator navigation'}, this)">
  See modeled results
</button>
```

Decorative images, icons, and containers are not interactive and must not receive analytics handlers. If a card is clickable, make it a semantic link or button, then track that control.

## Pre-Save Audit

Before a Folloze save or publish:

1. Inventory every CTA, link, button, selector, slider, tab, accordion, media control, print action, drawer, and internal navigation control.
2. Confirm every meaningful interaction emits a descriptive event.
3. Confirm every CTA uses `cta_click` with `text`, `area`, and the source element.
4. Confirm every external link uses `target="_blank" rel="noopener"`.
5. Confirm no payload includes raw financial values, PII, credentials, account-confidential values, or free text.
6. Confirm action names use stable underscores.
7. Confirm the HTML satisfies every analytics acknowledgement required by the active save tool.
8. Test locally with an analytics spy, then test the saved Folloze experience independently.

Local spy tests prove event emission only. They do not prove Folloze Pulse delivery. Report local instrumentation and production delivery as separate states.

## Completion Receipt

Report:

- current Folloze guide read status;
- CTA coverage count;
- custom interaction coverage count;
- external link safety count;
- sensitive payload review status;
- local spy test status;
- Folloze save validator status;
- production Folloze Pulse verification status.

Use `not attempted`, `blocked`, `failed`, or `verified` for every state. Do not claim analytics delivery without direct production evidence.
