# Misar Dev — Claude Code Plugin Suite

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-7.5.0-green.svg)](CHANGELOG.md)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Plugin-purple.svg)](https://claude.ai/claude-code)

48-agent audit + optimization suite for Claude Code. Covers 12 audit categories with dynamic 3D model routing (model×effort×version), parallel task dispatch, and token budget management.

**Built by [Misar.Dev](https://misar.dev)** — Open-source tools for developers.

---

## Agents (13)

| Agent | Model | Description |
| ----- | ----- | ----------- |
| `orchestrator-agents` | opus | Full-suite 48-agent orchestrator — 4-phase execution, Observer Agent token management, batched parallel processing (max 4) |
| `context-saver` | haiku | Dynamic model router — auto-switches between opus/sonnet/haiku by task complexity. Saves 85-95% context tokens, 60-70% cost. Auto-enabled via SessionStart hook |
| `task-fragmenter` | haiku | Decomposes prompts into optimal parallel subtasks with model assignments for Agent dispatch |
| `auditor-agents` | sonnet | Website audit — SEO, Accessibility, Performance, Security, Mobile, Content, Compliance (7 categories) |
| `uiux-agents` | sonnet | UI/UX design audit — Spacing & Layout, Typography & Color, Components, Accessibility, Performance, Mobile, Animation, Dark Mode |
| `qa-agents` | sonnet | Code quality audit — Code Reviewer, Standards Compliance, Bug Detective, Technical Debt |
| `security-agents` | opus | Security deep-dive — Hardening, Compliance, Penetration Testing, Data Privacy |
| `marketing-agents` | sonnet | Marketing and growth audit — SEO, SXO, Content Marketing, Growth, Analytics, AI Search Optimization |
| `brand-agents` | sonnet | Brand and psychology audit — Brand Development, User Psychology, Conversion, Emotional Design |
| `compliance-agents` | opus | Compliance audit — 49 global regulatory frameworks across 7 tiers |
| `tester-agents` | sonnet | Testing audit — Unit, Integration, E2E Black Box, E2E White Box, Beta, Regression |
| `product-agents` | sonnet | Product strategy audit — PM, Designer, Development, Feature Prioritization |
| `content-agents` | sonnet | Language and content audit — Grammar, Copy, Localization, Documentation |

---

## Skills & Commands (12)

| Command | Description |
| ------- | ----------- |
| `/misar-dev:auditor` | Website audit — SEO, Accessibility, Performance, Security, Mobile, Content, Compliance |
| `/misar-dev:uiux` | UI/UX design audit across 8 dimensions |
| `/misar-dev:qa` | Code quality — reviewer, standards, bug detection, technical debt |
| `/misar-dev:security` | Security hardening, compliance, penetration testing, data privacy |
| `/misar-dev:marketing` | Marketing and growth audit |
| `/misar-dev:brand` | Brand and psychology audit |
| `/misar-dev:compliance` | 49 global regulatory frameworks |
| `/misar-dev:tester` | Full testing audit — unit through regression |
| `/misar-dev:product` | Product strategy audit |
| `/misar-dev:content` | Language and content audit |
| `/misar-dev:context-saver` | Manual control of dynamic model router |
| `/misar-dev:full-suite` | Run all 35 agents across 8 categories — 4-phase orchestrated execution |

---

## Context Saver

Auto-enabled on every session via `SessionStart` hook. No configuration needed.

| Trigger | Model |
| ------- | ----- |
| Simple lookups, formatting | haiku |
| Code generation, analysis | sonnet |
| Architecture, security, orchestration | opus |

Saves 85-95% context tokens by routing lightweight tasks to cheaper models.

---

## Quick Start

### Install — Claude Code plugin (full suite)

```bash
git clone https://github.com/MisarDev/misar-ai-plugins.git \
  ~/.claude/plugins/marketplaces/misar-ai-plugins
```

### Install — individual skills via `npx skills` (any AI agent)

Works with Claude Code, Cursor, Cline, Copilot, Windsurf, and any `npx skills`-compatible agent:

```bash
# Install all 16 skills at once
npx skills add MisarDev/misar-ai-plugins

# Or install a specific skill
npx skills add MisarDev/misar-ai-plugins/skills/security
npx skills add MisarDev/misar-ai-plugins/skills/uiux
npx skills add MisarDev/misar-ai-plugins/skills/qa
```

### Use (Claude Code)

Run a full audit:

```text
/misar-dev:full-suite
```

Run a targeted audit:

```text
/misar-dev:security
/misar-dev:uiux
/misar-dev:qa
```

Or just ask naturally — agents auto-trigger on matching prompts.

---

## Architecture

```text
plugins/misar-dev/
├── agents/
│   ├── orchestrator-agents/   # 48-agent orchestrator
│   ├── context-saver/         # Dynamic model router
│   ├── task-fragmenter/       # Parallel subtask decomposer
│   ├── auditor-agents/
│   ├── uiux-agents/
│   ├── qa-agents/
│   ├── security-agents/
│   ├── marketing-agents/
│   ├── brand-agents/
│   ├── compliance-agents/
│   ├── tester-agents/
│   ├── product-agents/
│   └── content-agents/
├── skills/                    # 12 skill entry points
├── commands/                  # 12 slash commands
├── hooks/
│   └── hooks.json             # SessionStart (context-saver), UserPromptSubmit, Stop
└── scripts/
```

---

## Versions

| Version | Highlights |
| ------- | ---------- |
| **7.5.0** | Misar.Dev branding, `feature-dev` dependency removed, GitHub public release |
| 7.4.0 | 3D Router (model×effort×version), seo-content-generator + software-engineer + uiux-designer |
| 7.0.0 | 12-category suite, Observer Agent token management |
| 6.0.0 | Task fragmenter + parallel subagent dispatch |
| 5.0.0 | Context-saver dynamic model router |

---

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Repository: [github.com/MisarDev/misar-ai-plugins](https://github.com/MisarDev/misar-ai-plugins)

---

## License

MIT — see [LICENSE](LICENSE)

---

**More from [Misar.Dev](https://misar.dev)**: [Misar Mail](https://mail.misar.io) | [Assisters](https://assisters.dev) | [Misar.io](https://misar.io)
