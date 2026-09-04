# Builder Handoff Contract

Use this contract after account research and before implementation. It keeps the account argument binding
across custom HTML, template-based MCP, and native traditional Folloze builds.

## Required Fields

```yaml
seller: ""
target_account: ""
account_scope:
  parent_company: ""
  allowed_supporting_business_units: []
offering: ""
campaign_motion: one_to_one | one_to_few | competitive_displacement | renewal_expansion | new_logo
build_mode: mcp_html | mcp_template | native_traditional
campaign_hook: ""
why_now: ""
buyer_pain: ""
seller_mechanism: ""
leadership_outcome: ""
headline_direction: ""
primary_cta:
  label: ""
  destination_type: form | email | url | anchor | pending
  destination: ""
signature_interaction:
  type: calculator | scenario_model | diagnostic | readiness_assessment | maturity_score | comparison | role_path
  buying_question: ""
  assumption_source: ""
proof: []
required_logos:
  vendor: true
  target: true
brand_source: ""
prohibited_visible_language: []
approval_state: new | approved | repair_mode
```

## Build Mode Rules

- `mcp_html`: hand off to `Folloze-One-To-One-Microsite-Builder`. The strategist does not pick a Folloze
  template or force the account argument into native template sections.
- `mcp_template`: continue in `abm-strategist`, select and describe a real template, map the argument, and
  create a draft through the Board MCP.
- `native_traditional`: hand off to `Folloze-Industry-Campaign-Page-Builder`. The final experience must use
  native sections and content. HTML can be a wireframe only when the user explicitly requests one.

## Account Narrative Gate

The parent target company must own the headline, primary CTA, and leadership outcome unless the user
explicitly scopes the campaign to a business unit. Supporting business units can supply evidence but cannot
silently become the campaign subject.

The first viewport must make four things clear:

1. Why this target should care now.
2. What the seller does differently.
3. What changes operationally for the target.
4. What action leadership should take next.

Fail the handoff if another peer account could be substituted without rewriting the hook, mechanism,
leadership outcome, and CTA.

## Competitive Displacement Gate

For a displacement motion, name the incumbent in the internal contract and make the visible transition case
specific. Explain the current operating limitation, the seller's different mechanism, the leadership outcome,
and a credible next step. Do not publish unsupported superiority, savings, or performance claims.

## Approval Carry-Forward

Set `approval_state: repair_mode` when the user is fixing an existing approved experience and the seller,
target, offering, CTA, motion, and build mode remain unchanged. Repair mode skips the brief checkpoint and
goes directly to implementation and QA.
