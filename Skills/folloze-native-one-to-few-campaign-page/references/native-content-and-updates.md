# Native content and incremental updates

## Import a complete item

Discover the available upload/content operations and current item schema. Use official/public or approved source bytes. Record source, title, type, checksum, cover provenance and expected PDF page count or video duration. Do not use an empty web snapshot as a substitute for a PDF.

1. Reconcile an existing import ledger before creating anything. Use a stable source checksum plus board ID as the logical import key; API idempotency keys only where supported.
2. Request an upload destination through the authorized connector, upload the bytes, and retain the returned permanent file identifier. Never save credentials or signed upload/download URLs in a skill or durable report.
3. Create or copy an item using supported operations. If a copied item shares a source record, detach it before changing title, file or cover. Confirm ownership before modifying it.
4. Update the content record and board item as required by the live API. Read back board ID, item ID, type, title, file ID, cover, visibility and source linkage. Reconcile partial/uncertain writes instead of making another copy.
5. Open the item in the native reader. Wait for actual page/player content, verify title and total pages/duration, and test close, fallback and download where enabled.

The content ledger in the [example](../examples/industry-account-contract.json) feeds the readback checks in `scripts/native_contract.py`. These checks require separately captured API/Designer evidence. They do not perform uploads or promise a provider-specific endpoint.

Normalize the captured readback to the contract's `board_id`, `industry_rules`, `logo_rules`, `account_token`, `header`, `variants` and `items` fields. Include observed `reader_pages` on PDFs. Retain raw source receipts alongside it. Preserve rule meaning and identifiers during normalization; do not fill missing readback from the intended configuration. The checker compares saved rules as well as content bindings.

## Leading Item and resources

Use a true native Leading Item section. Inspect the current source selector schema. When it exposes `sources.type: curated`, `sources.options: manual`, and `sources.flz_item_id`, set all three; an item ID left under a dynamic selector may be ignored. Other templates can differ, so use their current schema.

Bind each variant to its selected native board item. Verify both the saved configuration and the loaded cover/reader. Resource collections get explicit approved item sets, ordering and native-reader actions. Verify the actual item count and available content after selecting each section rule.

## Update safely

Capture the latest draft and published configuration separately. Reuse stable board, section, item and public identities. Compare the latest configuration with the intended change and limit the diff to the requested fields. A changed current snapshot stops a stale update. A plan is not an applied change. Immediately before a write, use the platform's concurrency control or recheck the compared state.

Save only within existing authority, reload and read back. A native family upgrade may normalize metadata; compare meaningful fields and retain both raw snapshots. Do not ignore changes to rules, content, theme or actions as normalization. Verify affected visual and behavioral states, then report draft, publication, public targeting and analytics separately.
