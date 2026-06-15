---
name: Folloze-One-To-One-Microsite-Builder
description: Build named-account Folloze one-to-one microsites and follow-up pages for ABM, enterprise sales, post-event follow-up, renewal, expansion, and executive outreach. Use when the user wants a buyer-facing page tailored to one target account, one opportunity, or one named customer.
---

# Folloze One-To-One Microsite Builder

Use this skill to build a Folloze-ready page for one named account or customer. The page should feel like the seller or vendor understands the account's public business context, not like an internal account plan was pasted into a page.

## Fit

Use this skill for named-account pages, executive follow-up, post-event one-to-one pages, account-specific ABM, renewal/expansion stories, and deal-room-style microsites. If the user wants a broad campaign page, use `Folloze-Top-Of-Funnel-Campaign-Landing-Page`.

## Minimum Inputs

Gather only what is missing:

- Vendor or seller organization.
- Target account name and public website.
- The trigger: meeting, event, campaign, opportunity, renewal, expansion, or outreach.
- CTA: continue the conversation, book a workshop, review resources, register, evaluate a solution, or another clear next step.
- Approved sources: public account research, call notes, CRM, Drive assets, content links, screenshots, or pasted notes.

## Source Boundaries

- Private notes, CRM, email, Slack, and meeting summaries are strategy inputs only.
- Buyer-facing claims must come from public account evidence, approved content, or user-approved wording.
- Never expose contact-level intent data, private notes, known-contact counts, internal objections, budget comments, sales stage, pricing, or procurement details unless the user explicitly approves that visible copy.
- For any personalized detail, read `references/personalized-not-creepy.md` and classify it as Safe, Risky, or Prohibited before it appears on the page. Keep Safe, fix or cut Risky, and never include Prohibited.

## Workflow

1. Write an internal account brief: account context, trigger, likely buyer priority, why now, vendor promise, proof, and CTA.
2. Capture source design context from the vendor brand first. Use the target-account brand only as a respectful secondary accent unless the user asks for co-branding.
3. List the personalized elements you plan to show, name each source in one sentence, and apply the personalized-not-creepy rubric before drafting buyer-facing copy.
4. Choose a page shape: executive narrative, account-specific workflow, event follow-up, role-based buying committee, or resource-led follow-up.
5. Build one self-contained local HTML file in the active repo.
6. Include real resources, anchors, modals, videos, or CTA links. Do not include decorative dead controls.
7. QA desktop/mobile, buyer-safe copy, personalization provenance, source-brand fidelity, and CTA behavior.
8. For Folloze save/publish, use the available Folloze MCP publishing tools and current Folloze guide. Keep local source path, board ID, returned edit URL, and public URL status separate.

## Page Standards

- First viewport must name the target account or make the account context obvious.
- Use the account's real operating context, public priorities, industry, event trigger, or known initiative to sharpen the story.
- The page should make the next seller action easier: a precise follow-up, a buyer-ready link, or a focused meeting ask.
- Do not over-personalize in a way that feels watched. Recognize the account; do not reveal surveillance.
- The page should feel prepared from professional homework, never like the account is being watched.

## QA Gates

Before final response or publish:

- Account identity is correct and not confused with a similarly named entity.
- Public-facing claims are sourced or user-approved.
- Private context has been translated into public-safe problem language.
- Every visible personalized element has a named source and has passed the Safe/Risky/Prohibited rubric.
- Any Risky personalized element has been generalized, explicitly confirmed by the user, or removed.
- CTA is specific and functional.
- Vendor and account logo treatment is verified.
- Mobile and desktop layouts are readable.
- The final response includes the list of personalized elements and sources for explicit confirmation before any live publish.
- If saved through Folloze, report local source path, board ID, returned designer URL, and public URL status separately.

## Final Response

Return the local file path, account/page angle, CTA, source boundary caveats, QA status, and Folloze save/publish status.
