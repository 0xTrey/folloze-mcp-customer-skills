# Folloze Analytics Tracking Skill

Use `folloze-analytics-tracking` before saving or publishing customer-facing HTML through the Folloze MCP. It covers CTA clicks, calculator interactions, navigation, tabs, accordions, media controls, external-link safety, sensitive payload exclusions, and production verification boundaries.

## Public Source

- Readable source: `https://github.com/0xTrey/folloze-mcp-customer-skills/blob/main/Skills/folloze-analytics-tracking/SKILL.md`
- Raw source: `https://raw.githubusercontent.com/0xTrey/folloze-mcp-customer-skills/main/Skills/folloze-analytics-tracking/SKILL.md`
- Complete skill pack: `https://github.com/0xTrey/folloze-mcp-customer-skills`

The GitHub source is authoritative for Folloze MCP work. The current guide and active save schema override any conflicting example from an older downloaded archive.

## Install The Skill

Install the complete customer skill pack when possible:

```bash
git clone https://github.com/0xTrey/folloze-mcp-customer-skills.git
cd folloze-mcp-customer-skills
python3 scripts/install_customer_skills.py --target both
```

To install only Analytics Tracking for Codex:

```bash
mkdir -p ~/.codex/skills/folloze-analytics-tracking
curl -fL \
  https://raw.githubusercontent.com/0xTrey/folloze-mcp-customer-skills/main/Skills/folloze-analytics-tracking/SKILL.md \
  -o ~/.codex/skills/folloze-analytics-tracking/SKILL.md
```

To install only Analytics Tracking for Claude:

```bash
mkdir -p ~/.claude/skills/folloze-analytics-tracking
curl -fL \
  https://raw.githubusercontent.com/0xTrey/folloze-mcp-customer-skills/main/Skills/folloze-analytics-tracking/SKILL.md \
  -o ~/.claude/skills/folloze-analytics-tracking/SKILL.md
```

Restart or refresh the client after installation so it reloads the skill catalog.
