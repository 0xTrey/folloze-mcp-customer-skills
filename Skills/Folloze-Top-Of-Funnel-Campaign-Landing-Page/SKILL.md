---
name: Folloze-Top-Of-Funnel-Campaign-Landing-Page
description: Build public-safe top-of-funnel Folloze campaign landing pages for broad demand generation, paid media, event awareness, partner campaigns, product launches, and resource offers. Use when the user wants a Folloze-ready landing page that introduces a campaign, explains the offer, captures interest, and routes visitors to the next step.
---

# Folloze Top-Of-Funnel Campaign Landing Page

Use this skill to turn a broad campaign idea into a buyer-facing Folloze landing page that can support paid media, social, web, events, partner marketing, or nurture entry points.

## Fit

Use this skill when the page is one-to-many and should avoid named-account assumptions. If the request is for a named account, use `Folloze-One-To-One-Microsite-Builder`. If it is for a vertical or segment page, use `Folloze-Industry-Campaign-Page-Builder`.

## Minimum Inputs

Gather only what is missing:

- Campaign goal and primary CTA.
- Audience segment or persona.
- Offer, event, product story, or resource.
- Source brand page, brand guide, screenshot, or approved design direction.
- Required content links, forms, calendar links, videos, or resources.

If the user only provides a URL and goal, infer the first draft from the source page and clearly label assumptions.

## Workflow

1. Build a short campaign brief: goal, audience, offer, promise, CTA, source inputs, and constraints.
2. Capture design context from the approved source page or brand input. Use `brand-harvester` when available.
3. Choose a simple landing-page shape: hero, why now, value proof, how it works, resource/offer module, CTA.
4. Create a single self-contained HTML file in the active repo.
5. Keep buyer-facing copy public-safe. Do not expose internal notes, sales scoring, intent data, private meeting notes, or tool mechanics.
6. Add real buttons, anchors, resource links, forms, video embeds, and analytics hooks where supported.
7. QA desktop and mobile before Folloze save or handoff.

## Copy Standards

- Make the first viewport explain the offer in under 10 seconds.
- Use plain campaign language: what the visitor gets, why it matters now, and what to do next.
- Avoid visible words like `demo`, `template`, `wireframe`, `test`, `internal`, `generated`, or `placeholder`.
- Do not make Folloze the visible brand unless the campaign is Folloze-owned.
- Use proof only when sourced from public pages, approved materials, or user-provided facts.

## Recommended Page Shapes

- Offer landing page: hero, problem, offer, proof, resource preview, CTA.
- Event awareness page: hero, audience promise, agenda/outcomes, speakers or proof, registration CTA.
- Product launch page: hero, shift in market, capability story, use cases, proof, request CTA.
- Partner campaign page: co-branded hero, joint value, workflow, resources, shared CTA.

## QA Gates

Before final response or publishing:

- The page has one clear CTA path and no dead controls.
- Desktop and mobile layouts are readable with no horizontal overflow.
- External links and embedded media load or have a deliberate fallback.
- Copy is public-safe and not account-specific unless approved.
- Styling follows the source design context instead of generic AI gradients or decorative filler.
- If publishing through Folloze MCP, use the available Folloze MCP publishing tools and current Folloze guide. Report the exact board ID, returned edit URL, and public URL status separately.

## Final Response

Return the local file path, the campaign goal, the CTA, QA status, and whether the page is local-only, ready for Folloze publish, or already saved/published.
