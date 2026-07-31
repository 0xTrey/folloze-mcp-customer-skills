# Claude Marketplace: Connector To Plugin Roadmap

## Key Finding

Claude does not document an in-place conversion of an existing Connector listing into a Plugin listing. The Folloze path is a separate Plugin package and submission that combines the current remote MCP connection with the customer skills. Keep the Connector available until the Plugin has been approved, installed from the directory, authenticated, and verified.

## Current State

This repository is a public skill pack. It is not yet a valid Claude Plugin:

- skills live under the repository's existing `Skills/` convention;
- there is no `.claude-plugin/plugin.json`;
- there is no plugin-root `.mcp.json` describing the Folloze remote MCP server and authentication;
- there is no marketplace manifest, release package, or plugin validation workflow;
- the existing Folloze Connector listing and its production authentication details are not stored here.

The skill merge should land independently. Creating a speculative plugin manifest without the production MCP endpoint, auth contract, plugin identity, and marketplace namespace would produce an invalid or misleading listing.

## Target State

Ship one atomic Folloze plugin that bundles:

- the Folloze MCP server connection;
- `abm-strategist`;
- `brand-harvester`;
- the four customer builders;
- dependency validation and source provenance.

The existing Connector listing should stay live until the Plugin listing is installed, authenticated, and verified in production. Treat Connector availability and Plugin availability as separate checkpoints.

## Migration Plan

1. Confirm the marketplace owner, plugin name, support URL, license, privacy URL, production MCP endpoint, and authentication method.
2. Add the standard plugin structure:
   - `.claude-plugin/plugin.json`
   - plugin-root `.mcp.json`
   - lowercase plugin `skills/` packaging or an explicitly validated equivalent
3. Preserve the current `Skills/` paths during migration or provide a tested compatibility installer so existing users are not broken.
4. Add plugin-level versioning, a release archive, checksums, and a machine-readable source lock.
5. Validate locally with `claude plugin validate --strict ./folloze-plugin` and a clean `claude --plugin-dir ./folloze-plugin` install.
6. Authenticate the bundled Folloze MCP connector and perform a read-only guide call.
7. Run sample TOFU, one-to-one, one-to-few, and Content Magic flows to prove:
   - ABM routing is correct;
   - Brand Harvester runs before visual design;
   - skills can locate bundled scripts inside the plugin cache;
   - local HTML and rendered QA remain separate from Folloze save and public deployment.
8. Submit the Plugin listing while keeping the Connector listing available. Use the Team/Enterprise organization directory form when Folloze owns an eligible Claude organization, or the Anthropic Console submission form for an individual publisher.
9. After acceptance, test a clean Marketplace install and separately verify authentication, skill discovery, local build, Folloze save, and public deployment.
10. Only then decide whether the standalone Connector listing should remain, redirect, or be retired.

## Acceptance Gates

- Plugin manifest validation passes.
- No bundled skill references files outside the plugin root.
- All six skills are discoverable after a clean install.
- The Brand Harvester CLI runs from the installed plugin cache.
- Every builder declares both required foundations.
- Account-based flows run `abm-strategist`; broad flows do not fabricate account inputs.
- Every build runs `brand-harvester`, receives `brand.json.validation.status: ok`, or stops for explicitly approved equivalent brand evidence.
- The MCP server authenticates without embedding secrets in the repository.
- Connector listing, Plugin listing, installed plugin, authenticated MCP, saved board, and public deployment are reported as distinct states.

Official references:

- Claude Plugins: `https://code.claude.com/docs/en/plugins`
- Plugin submission guidance: `https://claude.com/docs/plugins/submit`
- Team/Enterprise organization submission: `https://claude.ai/admin-settings/directory/submissions/plugins/new`
- Anthropic Console submission: `https://platform.claude.com/plugins/submit`
