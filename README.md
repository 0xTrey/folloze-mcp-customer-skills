# Folloze MCP Customer Skills

Public customer-facing skill pack for building Folloze buyer experiences with the Folloze MCP.

This repo is intentionally separate from Folloze internal skill work. It contains only portable, customer-facing skills that a marketer, intern, partner, or implementation team can QA and adapt without inheriting internal demo-board, account, or deal-room workflows.

## Included Skills

| Skill | Use it for |
| --- | --- |
| `Folloze-Top-Of-Funnel-Campaign-Landing-Page` | Broad demand-gen, paid-media, event-awareness, product-launch, partner, and resource-offer landing pages. |
| `Folloze-One-To-One-Microsite-Builder` | Named-account ABM pages, executive follow-up pages, renewal/expansion microsites, and account-specific buyer experiences. |
| `Folloze-Industry-Campaign-Page-Builder` | Industry, segment, cohort, persona, event-audience, and one-to-few campaign pages. |
| `Folloze-Content-Magic-Builder` | Interactive Folloze experiences created from a whitepaper, report, ebook, webinar, deck, video, guide, or other approved content item. |
| `folloze-narration-sweep` (Folloze Narration Sweep) | AI-provider-neutral final buyer-facing sweep that removes fourth-wall narration, internal demo language, visual production artifacts, placeholders, and dead interactions before a board is saved or published. |

## Deliberately Excluded

These internal workflows are not bundled here:

- Zoom demo-room and post-call deal-room automation skills.
- API/native-template board builders.
- Internal Salesforce, Gmail, Slack, Granola, tracker, or deal-process skills.
- Internal demo-board builder skills.

## Prior Baseline

We previously built a broader campaign-board builder pattern. This repo splits that broad pattern into four narrower customer-facing skills so each workflow is easier to test, explain, and hand off.

## How To QA

For each skill:

1. Read `SKILL.md` and confirm the trigger description matches the intended use case.
2. Confirm `agents/openai.yaml` has a clear display name, short description, and default prompt.
3. Run a sample task with minimal inputs and verify the skill asks only for missing critical information.
4. Confirm output separates local source, Folloze save status, board ID, edit URL, and public URL status.
5. Confirm buyer-facing copy never leaks private notes, internal scoring, tool mechanics, pricing strategy, or unapproved claims.
6. Confirm every board builder invokes `folloze-narration-sweep` before save or publish and blocks release when any required QA layer fails or remains unverified.

## Publishing Assumption

The skills assume the user has access to Folloze MCP publishing tools. They do not hard-code internal tool names. When publishing, follow the current Folloze MCP guide returned by the environment and validate the actual HTML before saving.
