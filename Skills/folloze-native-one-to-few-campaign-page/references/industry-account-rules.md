# Industry messaging and account recognition

Use three independent layers for an industry-led demo. An explicitly requested account-specific campaign can use account message rules, but it must declare that different purpose. Do not turn this industry's rule model into a universal ban on account personalization.

1. Industry selects the hero, value proposition, proof, leading content, workflow, resources and closing action.
2. Account Name supplies a supported text token inside each industry banner, with a complete no-name fallback.
3. Exact approved account domains select recognition logos where supported. Preserve header copy, navigation and CTA; mark visibility, sizing and separator presentation belong to the logo layer. Preserve user-selected assets and crops.

Discover the current destination's fields, provider, enabled state, exact allowed values, token support and section schema. Record a capability receipt and access time. Names such as Financial Services and Pharmaceuticals are examples, not universal labels. Never transplant field IDs from another board. Unknown industry means generic messaging even when a known account logo matches. Known industry without account data still receives the industry content. An account outside the illustrative domain list can still receive industry content.

If industry and logo overrides share a widget, verify the platform's merge/precedence behavior. Prefer separate section responsibilities when overrides would replace each other's data. Never rely on rule ordering accidentally preserving the right text.

## Variant completeness

Define the demonstration's section roles before building. A rich demo commonly includes hero, logo carousel, attributed performance, value cards, leading item, workflow visual, customer context, resources and closing action. Adapt to real content and native capability rather than forcing a fixed count. Every configured industry and the generic fallback must satisfy the selected roles. Each has a relevant leading item and useful native resources. Use at least two relevant content types when demonstrating content personalization and approved sources support them.

Use the [rule example](../examples/industry-account-contract.json) and [validator](../scripts/native_contract.py) to check declarations, independent rule scope, allowed values, logo-only differences and expected recognition combinations. Declare `account_token.placement: inside_each_industry_banner`. Each hero supplies `headline` and `image`; industry heroes also supply a token-free `fallback_headline`. The check rejects missing banner callouts, repeated hero messages/images and stale hero readback. Logo effects may adjust `secondary_logo_visible`, `secondary_logo_scale` and `separator_visible` without changing messaging. The resolver models the intended contract for tests; it does not prove that Folloze recognized a visitor.

## Account Name

Read token syntax and replacement support from the destination or a verified current example. Use the supported token in both industry banners and configure a no-value fallback. A separate account strip alone is insufficient for the demo-pack default. Account callout, image and message must all change with the selected industry/account context; proof, resources and CTAs also differ by industry where supported. The native token `{!account_name}` is an example to verify, not a query parameter. Render untrusted account text through the platform's text replacement, never executable HTML. Test apostrophes, ampersands, long names and missing values. Do not leave punctuation gaps or expose a literal token to anonymous visitors.

Test separately: no data, industry only, account only, both, unknown industry, unknown domain, case/format normalization only when supported, and malformed values. Inspect saved rules and Designer sections, then use supported recognized-visitor testing after authorized release. Designer's literal token display is not evidence of runtime substitution.
