# Folloze Release Contract

Use this contract after the model, local calculator, and QA package are complete. It keeps local generation, Folloze mutation, publication, live verification, analytics, and source control from being mistaken for one another.

## Default Boundary

The default deliverable is a self-contained local HTML artifact in the active project repo. Do not save, replace, or publish a Folloze section unless the user explicitly authorizes that action and the current environment exposes a documented capability for it.

Do not infer a custom HTML section tool from a general board editor, a template-section updater, a full-board HTML saver, or observed designer markup. Similar-looking capabilities can have different sanitization, script, analytics, revision, and publication behavior.

## Runtime Capability Preflight

Before any Folloze mutation, inspect the current guide or tool schema and verify all of the following:

- the current `$folloze-analytics-tracking` source was downloaded, read completely, and applied to the approved HTML;
- exact target board ID, page, and section or insertion location;
- whether the action creates, updates, or replaces content;
- accepted payload type and size limits;
- whether inline CSS, inline JavaScript, SVG, forms, and external assets are permitted;
- sanitization and content-security behavior;
- how scripts mount, remount, and clean up when the board rerenders;
- whether custom interactions can emit supported analytics and how delivery is verified;
- save response, returned edit URL, revision behavior, and rollback path;
- whether save and publish are separate calls;
- whether the environment can read the saved section back before publication;
- whether anonymous verification is possible after publication.

If any item that affects functionality or recoverability is undocumented, stop at the local handoff and report the missing contract.

## Authorization Gate

Immediately before the first mutating call:

1. restate the exact board, page, section, and action;
2. confirm that the local artifact and model version are the approved source;
3. confirm that blocking QA issues are resolved or accepted;
4. confirm the user has explicitly authorized that exact save or publish action;
5. preserve the current board identity and any available rollback information.

Authorization to save does not authorize publication. Authorization to publish does not authorize unrelated board edits, analytics configuration, lead collection, messages, or tracker updates.

## Save Sequence

When the documented custom HTML capability exists and the user authorizes it:

1. read the target board and section state;
2. validate the payload against the live schema and host constraints;
3. save only the approved section or artifact;
4. capture the tool response, board ID, page, section identity, and returned edit URL;
5. read the target back and compare it with the approved source;
6. run authenticated preview QA when available;
7. stop before publish unless publish was separately authorized.

If the live capability supports only full-board HTML, do not use it as a substitute for a section-level update without explicit approval of that broader replacement scope.

## Publish And Verification Sequence

After separate publish authorization:

1. publish using the current documented capability;
2. capture the publication response and public URL;
3. open the experience anonymously on desktop and mobile;
4. verify calculator mount, inputs, scenarios, results, assumptions, links, and CTA behavior;
5. inspect for clipping, overflow, host-style collisions, script stripping, duplicate listeners, and rerender failures;
6. verify analytics independently using the approved production method;
7. record discrepancies and fix only within the authorized scope.

Do not call an authenticated preview anonymous verification. Do not call a successful save publication. Do not call a local analytics spy production delivery.

## Analytics Boundary

Use `$folloze-analytics-tracking` as the required instrumentation contract. Read the current Folloze guide and active save schema immediately before mutation. The live guide and save validator control the exact `flzAnalytic` implementation and override conflicting examples from older archives.

Every CTA must emit `cta_click` with safe `text` and `area` fields and the source element. Every meaningful calculator state change must emit a descriptive tracked event. External destinations must use `target="_blank" rel="noopener"`. Do not inject a custom bridge or reach into undocumented Folloze controllers unless the current guide explicitly requires that exact integration.

Never emit raw financial values, account-confidential values, PII, credentials, or free-text input. Prefer safe fields such as calculator version, input ID, scenario, result band, area, CTA label, and validation error type.

Custom interaction instrumentation and standard Folloze page analytics may have different support boundaries. Report them separately.

## Evidence Receipt

For every attempted release, report these fields independently:

```text
Local model version:
Local HTML path:
Local QA status:
Target board ID:
Target page and section:
MCP capability and schema verified:
MCP save status:
Saved-content readback status:
Returned edit URL:
Publish status:
Public URL:
Anonymous desktop status:
Anonymous mobile status:
Analytics adapter status:
Analytics Tracking source and load status:
CTA and custom-interaction coverage:
Production analytics delivery status:
Git commit status:
Git push status:
Open blockers and owners:
```

Use `not attempted`, `blocked`, `failed`, or `verified` rather than leaving a state ambiguous.
