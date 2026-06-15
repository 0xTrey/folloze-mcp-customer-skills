# Missing Campaign Asset Fallbacks

## Governing Principle

Never fabricate a real destination, credential, or fact. When an asset is missing, degrade to a safe, clearly labeled placeholder and surface every substitution to the user before anything publishes. A provisional page must never look finished; unflagged placeholders can become live test artifacts.

Before publishing or saving to a live Folloze board, present one summary of every fallback applied and every placeholder still present. Require explicit user confirmation before proceeding.

## Fallback Rules

### Registration or Form URL Missing

- Render a local form on the page with name, email, company, and any campaign-relevant fields.
- Route the interim form destination to `https://www.folloze.com/request-demo`.
- Add a visible note near the form or an inline markup comment stating that the final form URL is pending and must be swapped before launch.
- Do not point the form at a guessed endpoint.

### Primary CTA Destination Missing

- Default the CTA to `https://www.folloze.com/request-demo` as the interim request/demo route.
- Flag the route as provisional in the fallback inventory and, when appropriate, near the CTA in the source markup.
- Keep the button label tied to the offer, such as `Register`, `Get the guide`, or `Save my seat`, instead of a generic `Learn more`.

### Offer Headline or Body Copy Missing

- Generate placeholder copy only from campaign context that actually exists, such as offer type, audience, or product.
- Bracket placeholder messaging visibly with `[DRAFT - confirm with campaign owner]` so it cannot be mistaken for approved copy.

### Hero Image, Logo, or Visual Assets Missing

- Use a neutral themed treatment such as brand colors, a simple gradient, or a solid block from the company theme.
- Leave a labeled placeholder region for the real asset.
- Never hotlink an unverified external image or invent a stock-like image.

### Event Details Missing for Webinars or Events

- Do not invent date, time, location, timezone, join link, speaker, or venue details.
- Insert bracketed placeholders such as `[DATE]`, `[TIME + TZ]`, and `[LOCATION / JOIN LINK]`.
- Omit countdowns, calendar links, and add-to-calendar actions until real values exist.

### Brand Theme or Colors Missing

- Fall back to the default company theme via `get_company_theme`.
- If the company theme is unavailable, use a neutral accessible palette.
- Note that brand styling is unconfirmed in the fallback inventory.

### Privacy, Consent, or Footer Text Missing

- Include a generic placeholder consent line flagged for legal review.
- Do not omit consent language on a public lead-capture page.
- Do not present placeholder consent language as final approved wording.
