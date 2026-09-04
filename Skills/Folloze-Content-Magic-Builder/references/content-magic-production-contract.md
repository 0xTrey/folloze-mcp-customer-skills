# Content Magic Production Contract

Read this reference for every Content Magic build. It turns the skill's design, copy, asset, interaction, and release expectations into reviewable evidence and blocking acceptance tests.

## Contents

1. Production packet
2. Brand ownership gate
3. Concept and visual allocation gate
4. Editorial transformation gate
5. Interaction affordance gate
6. Asset access and portability gate
7. Guided chapter and responsive gate
8. Static, browser, and hosted QA
9. Release receipts

## 1. Production Packet

Keep the following planning evidence in the active project repo. One concise Markdown or JSON file may contain several sections when that is easier to maintain.

### Activation brief

```text
Activation context:
Audience:
Buyer stage:
Why now:
Source promise:
Verified proof hierarchy:
Desired conversion action:
Original asset access mode:
Constraints and approval state:
```

### Claim matrix

For each buyer-facing factual claim, record the claim, approved source, exact supporting passage or location, qualification, and review status. The matrix is internal evidence. Do not paste it into the page.

### Brand ownership declaration

```text
Primary visual owner:
Content and claims authority:
Supporting partner or co-brand:
Approved source page or guide:
Brand Harvester path and validation status:
Surface -> source-system owner:
Allowed component families:
Explicitly excluded brand signals:
```

### Concept selection

When the user asks for options or the strongest composition is unclear, create three materially distinct concepts. Vary the experience shape, first-viewport signal, progression model, and buyer interaction. Do not present three cosmetic variations of the same hero and card stack.

Record the selected concept, why it fits the source and buyer job, and why the alternatives were not selected.

### Scene plan

```text
Scene ID and job:
Buyer question answered:
Primary headline:
Supporting copy:
Verified proof used:
Dominant visual:
Visual source and rights state:
Interaction and target region:
Primary action:
Transition from prior scene:
```

### Visual allocation map

Give each dominant visual one distinct purpose. Record a visual fingerprint such as asset hash, diagram type, or semantic structure. A repeated logo or small navigation mark is not a dominant visual. Reusing the same orbit, photograph, diagram, or card composition in adjacent scenes requires a documented progression purpose.

### Interaction map

```text
Control and accessible name:
Target region:
Direction indicated:
Material properties changed:
Keyboard behavior:
Selected-state behavior:
Reduced-motion behavior:
Analytics event and payload:
```

Material properties include image, alt text, headline, explanatory copy, steps, diagram, calculation, recommendation, or decision output. A small caption, footer note, or isolated sentence does not count by itself.

### Asset manifest

```text
Asset ID:
Scene and purpose:
Source and rights status:
Delivery method:
Expected natural dimensions:
Responsive treatment:
Interactive states using it:
Public fallback:
Local, saved, and hosted QA status:
```

## 2. Brand Ownership Gate

The primary visual owner controls the logo treatment, type hierarchy, palette, component families, imagery, spacing, surfaces, and interaction styling.

Content authority and visual ownership may differ. A source can describe a partnership without granting the supporting partner equal visual ownership.

Pass only when:

- the primary visual owner is explicit;
- Brand Harvester or Folloze Brand Kit evidence is valid;
- the exact source screenshot, product page, campaign page, or approved guide is identified;
- every surface has one declared owner;
- supporting-brand treatment is explicit and limited;
- rendered desktop and mobile controls are compared with measured source families; and
- no unexplained blending or generic approximation remains.

Fail before CSS when brand ownership is ambiguous, the harvest is invalid, the proposed components do not exist in the source system, or a partner has silently become the visual owner.

## 3. Concept And Visual Allocation Gate

Select the page shape before interactions. Choose the shape that best explains the source and advances the buyer, not the shape that is easiest to generate.

The first viewport must communicate the buyer tension or useful outcome in under ten seconds. It needs one primary headline, visible brand identity, one meaningful action, and a clear progression cue. Do not use an eyebrow-headline-dek stack.

Every scene has one primary job: orient, teach, prove, personalize, qualify, route, or convert. A scene may support another job, but it cannot become a collection of unrelated cards.

Pass only when:

- the selected shape is recorded;
- the first viewport has a specific source-faithful concept;
- every dominant visual has a distinct scene-level job;
- repeated visuals have a documented progression purpose;
- important diagrams communicate their semantics; and
- motion has a useful reduced-motion equivalent.

If a model represents orbit, flow, sequence, accumulation, comparison, or feedback, motion or progressive state should make that relationship easier to understand. Decorative motion is not required.

## 4. Editorial Transformation Gate

Use the source for facts and the page for persuasion. The buyer should understand the argument without being reminded that it came from a PDF, brief, page number, or production process.

### Required editorial pass

1. Build the claim matrix.
2. Write a message spine: tension, promise, key ideas, proof, business implication, and action.
3. Write scene-level copy for one job at a time.
4. Read the entire page as one narrative.
5. Repair vague language, repetition, abrupt transitions, excessive stacking, and operational commentary.

### Buyer-facing copy rules

- Use source-grounded, source-invisible language.
- Lead with buyer value, not the asset title or an explanation of the brief.
- Prefer direct, specific language over abstractions such as “you decide what to test next” when no clear test or decision exists.
- Keep a major desktop headline near two or three lines when the source-faithful idea permits it.
- Widen the intended text region or edit the headline before accepting an avoidable six-line stack.
- Do not use source-proof labels, page citations, filenames, evidence notes, partnership-context notes, or internal review language.
- Do not use eyebrow-headline-dek stacks.
- Do not use em dash characters.
- Do not invent claims, proof, outcomes, customers, metrics, quotations, guarantees, or timelines.

Store legally required attribution where it reads as natural customer-facing context. Keep ordinary provenance in the internal packet and release receipt.

## 5. Interaction Affordance Gate

An affordance makes a promise. Its direction, label, target, and state change must agree.

### Direction rules

- A left-pointing control changes a primary region to its left.
- A right-pointing control changes a primary region to its right.
- Story transport may point in the navigation direction when it clearly represents previous or next.
- Do not point an arrow off the page or toward a region that remains materially unchanged.

### Material change rules

A selector passes when it changes one or more dominant properties and the result is obvious without hunting for microcopy. Strong changes often update several related properties together, such as image, alt text, overlaid message, selected state, and supporting explanation.

If the content is only a list of value propositions, use static cards, an accordion, or another honest presentation. Do not add arrows to make static content appear interactive.

### Browser verification

For each control:

1. Capture the target fingerprint before activation.
2. Activate with pointer input.
3. Confirm selected state, target content, and analytics invocation.
4. Repeat with keyboard input.
5. Verify all resulting images and media load.
6. Confirm the arrow direction matches target geometry.
7. Capture the changed state when the change is visually significant.

A target fingerprint may include effective image source, natural dimensions, alt text, heading, body copy, step labels, computed visibility, and selected-state attributes.

## 6. Asset Access And Portability Gate

Every asset must survive Folloze save, public publication, cache refresh, and anonymous loading.

### Allowed delivery

- Embedded data asset when size and rights permit
- Stable public HTTPS asset controlled by an approved source
- Folloze-hosted asset with saved and public readback
- Native or accessible reader delivery for the original content item

### Blocked delivery

- `file:` URLs
- localhost or loopback hosts
- user-directory paths
- temporary directories
- private workspace URLs
- session-only blob URLs
- expiring signed URLs
- source paths that only work in the local preview

### Unavailable original asset exception

When the original file cannot be safely embedded, hosted, framed, or publicly accessed, stop before shipping a broken reader. If the user approves substitution, use the closest authoritative public source as the asset action. Record the missing original, reason, approved public URL, and validation result in the internal receipt.

The public fallback must use HTTPS, open with `target="_blank" rel="noopener"`, and emit the intended analytics event. Do not add a buyer-facing evidence warning.

### Runtime image verification

At local, saved, and anonymous public stages, inspect every base and interactive image state:

```text
complete === true
naturalWidth > 0
naturalHeight > 0
currentSrc is portable and expected
alt text matches the selected state
```

Also verify aspect ratio, object fit, cropping, container height, and layout shift at each required viewport.

## 7. Guided Chapter And Responsive Gate

Use the pinned-stage contract only for a selected chapter-path composition.

### Desktop invariant

- One stationary viewport
- One active scene
- One chapter per accepted wheel, keyboard, or transport action
- Inactive scenes hidden, inert, and noninteractive
- Visible progress and previous or next transport
- Page scroll position remains stable during chapter navigation

### Height resilience

Treat height separately from width. Use `100dvh`, compact-height bands, measured active-scene content, and remeasurement after resize, font settlement, scene entry, image load, and interaction changes. Compact spacing and type first. If necessary, allow only the active scene to scroll internally.

Do not use one hard maximum-height cutoff that clips the middle desktop range.

### Mobile invariant

At `900px` and below, use ordinary document flow. Remove desktop-only inert and hidden state, keep every scene available to assistive technology, hide desktop transport when it no longer represents the reading model, and keep horizontal overflow at zero.

### Required viewports

- `1440 x 900` desktop
- `1366 x 768` compact desktop
- `390 x 844` mobile

Add `320`, `375`, `414`, and `768` width checks when tooling permits.

## 8. Static, Browser, And Hosted QA

### Static QA

Run the bundled validator against the exact artifact. It blocks known source-proof language, internal paths, dead links, unsafe asset references, missing image alt text, mislabeled directional controls, prohibited composition markers, missing reduced-motion handling, and other deterministic failures.

Static success does not prove rendering, interaction materiality, public images, Folloze parser behavior, or publication.

### Local browser QA

Verify:

- brand fidelity against approved desktop and mobile evidence;
- headline line count and text width;
- every scene and control;
- every base and changed image state;
- direction and target geometry;
- clipping, overlap, layout shift, and horizontal overflow;
- focus, keyboard behavior, selected state, and reduced motion;
- link destinations and safe new-tab behavior;
- page-authored console errors; and
- analytics invocation where supported.

### Saved readback

Verify the board identifier, saved HTML or configuration, theme decision, expected copy, embedded or hosted assets, analytics wiring, and unchanged vanity state when no vanity operation was requested.

### Anonymous hosted QA

Open the public URL without relying on the authenticated Designer session. Use a cache-fresh request when necessary. Repeat the required desktop, compact-height, and mobile checks. Exercise the most important interaction states and inspect effective image sources plus natural dimensions.

Do not infer anonymous success from Designer preview, save response, publication controls, or prior public state.

## 9. Release Receipts

Report these states independently:

1. Local artifact path and hash
2. Static QA
3. Local rendered QA
4. Folloze save
5. Saved readback
6. Theme mode
7. Vanity operation
8. Publication state
9. Anonymous public response
10. Hosted interaction behavior
11. Hosted image delivery
12. Analytics invocation
13. Analytics delivery or downstream receipt
14. Git status and commit
15. Remote push

A pass in one state is not evidence for another. If a state was not requested, supported, or independently verified, report it as such rather than inferring success.
