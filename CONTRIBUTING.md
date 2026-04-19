# Contributing to misar-ai-plugins

Thank you for helping make this better.

## Ways to contribute

- **New agent** — Add a new audit category under `plugins/misar-dev/agents/`
- **Improve a skill** — Edit any `skills/*/SKILL.md` to sharpen triggers or instructions
- **Fix a bug** — Open an issue, then a PR
- **New plugin** — Add a new plugin alongside `misar-dev/` in `plugins/`

## Structure

```
plugins/misar-dev/
├── agents/          # Agent definitions (agent.md per agent)
├── skills/          # Skill entry points (SKILL.md per skill)
├── commands/        # Slash command definitions
├── hooks/           # Hook configuration (hooks.json)
├── hooks-handlers/  # Hook shell scripts
└── scripts/         # Supporting scripts
```

## Adding an agent

1. Create `plugins/misar-dev/agents/<name>/agent.md`
2. Add frontmatter: `name`, `description`, `model`
3. Register it in `plugins/misar-dev/.claude-plugin/plugin.json`
4. Add a corresponding skill in `skills/<name>/SKILL.md`
5. Add a slash command in `commands/<name>.md`

## Code style

- Agent footers: `*Built by [Misar.Dev](https://misar.dev)*`
- No external brand names (other than technical tool names)
- Keep SKILL.md descriptions under 400 chars for token efficiency

## Pull requests

- One PR per agent/skill/fix
- Title: `feat(agent): add <name>` or `fix(skill): <what>`
- No breaking changes to existing agent frontmatter without discussion

## License

MIT — contributions are licensed under the same terms.
