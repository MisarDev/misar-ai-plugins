# Misar.Dev — Claude Code Plugin Suite

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-7.6.0-green.svg)](https://github.com/MisarDev/misar-ai-plugins/releases/tag/v7.6.0)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Plugin-purple.svg)](https://claude.ai/claude-code)
[![npx skills](https://img.shields.io/badge/npx%20skills-compatible-blue.svg)](https://skills.sh)

**48-agent audit and optimization suite for Claude Code.** 16 categories, 3D model routing (model×effort×version), interactive flag prompting, parallel task dispatch, and automatic token budget management. Saves 90–97% context tokens on lightweight tasks.

Works on Claude Code, Cursor, Cline, GitHub Copilot, Windsurf, and any [`npx skills`](https://skills.sh)-compatible agent.

**Built by [Misar.Dev](https://misar.dev)** — Open-source AI developer tools.

---

## Quick Start

### Claude Code

```bash
git clone https://github.com/MisarDev/misar-ai-plugins.git \
  ~/.claude/plugins/marketplaces/misar-ai-plugins
```

Restart Claude Code. All `/misar-dev:*` commands are immediately available.

### Any AI agent — via `npx skills`

Works with Cursor, Cline, GitHub Copilot, Windsurf, and any [`npx skills`](https://skills.sh)-compatible agent:

```bash
# Install all 16 skills
npx skills add MisarDev/misar-ai-plugins

# Or install a specific skill
npx skills add MisarDev/misar-ai-plugins/skills/security
npx skills add MisarDev/misar-ai-plugins/skills/uiux
npx skills add MisarDev/misar-ai-plugins/skills/software-engineer
```

---

## Commands (16)

| Command | Argument Hint | Description |
|---------|--------------|-------------|
| `/misar-dev:full-suite` | `[--phase=1\|2\|3\|4] [--tier=1\|2]` | Full 48-agent orchestrated audit — 4 phases, Observer Agent, batched parallel execution |
| `/misar-dev:security` | `[agents] [--path=src/]` | Security deep-dive — Hardening, Compliance, Penetration Testing, Data Privacy |
| `/misar-dev:qa` | `[agents] [--path=src/]` | Code quality audit — Code Reviewer, Standards, Bug Detective, Technical Debt |
| `/misar-dev:tester` | `[agents] [--path=src/]` | Testing audit — Unit, Integration, E2E Black Box, E2E White Box, Beta, Regression |
| `/misar-dev:uiux` | `[agents] [--path=src/]` | UI/UX design audit — Spacing, Typography, Components, Accessibility, Performance, Mobile, Animation, Dark Mode |
| `/misar-dev:uiux-designer` | `[agents] [--platform=web] [--component=button]` | UI/UX design consultation — Project analysis, design system, brand identity, component specs, critique |
| `/misar-dev:compliance` | `[tier] [framework] [--path=src/]` | Compliance audit — 49 global frameworks across 7 regulatory tiers |
| `/misar-dev:marketing` | `[agents]` | Marketing and growth audit — SEO, SXO, Content Marketing, Growth, Analytics, AI Search |
| `/misar-dev:brand` | `[agents]` | Brand and psychology audit — Brand Development, User Psychology, Conversion, Emotional Design |
| `/misar-dev:product` | `[agents]` | Product strategy audit — PM, Designer, Development, Feature Prioritization |
| `/misar-dev:content` | `[agents]` | Language and content audit — Grammar, Copy, Localization, Documentation |
| `/misar-dev:seo-content-generator` | `[agents] [--mode=technical\|content\|audit\|full] [--topic=keyword] [--type=blog\|guide\|comparison\|stats\|how-to] [--keywords=k1,k2]` | AEO/SEO full-stack implementation — technical infrastructure, content generation, bot crawl health |
| `/misar-dev:software-engineer` | `[agents] [--prd=file.md] [--path=src/] [--framework=nextjs]` | Build from PRD/specs — PRD analysis, planning, code generation, validation, recommendations |
| `/misar-dev:auditor` | `[url] [categories] [--quick\|--deep]` | Website audit — SEO, Accessibility, Performance, Security, Mobile, Content, Compliance |
| `/misar-dev:guidelines` | `[show]` | LLM coding guidelines — Think Before Coding, Simplicity First, Surgical Changes, Goal-Driven Execution |
| `/misar-dev:billing` | `[lifecycle\|security\|pricing\|integrity] [--stack=stripe\|paddle] [--path=src/]` | Billing & subscription audit — lifecycle, CSRF on payment forms, pricing centralization, webhook integrity |
| `/misar-dev:context-saver` | `[status\|setup\|config\|reset]` | 3D Router — manual control over model×effort×version switching and token budget |

### Natural language triggers

Commands also auto-trigger on matching prompts — no slash command needed:

| Say this... | Triggers |
|-------------|----------|
| `"security audit"`, `"is this secure"`, `"harden my server"` | `/misar-dev:security` |
| `"code review"`, `"find bugs"`, `"code quality"` | `/misar-dev:qa` |
| `"write tests"`, `"E2E testing"`, `"test coverage"` | `/misar-dev:tester` |
| `"audit UI"`, `"check accessibility"`, `"review UX"` | `/misar-dev:uiux` |
| `"design system"`, `"UI guidelines"`, `"component advisor"` | `/misar-dev:uiux-designer` |
| `"GDPR"`, `"SOC2"`, `"compliance audit"` | `/misar-dev:compliance` |
| `"SEO audit"`, `"growth strategy"`, `"content marketing"` | `/misar-dev:marketing` |
| `"brand audit"`, `"conversion review"` | `/misar-dev:brand` |
| `"product strategy"`, `"feature prioritization"` | `/misar-dev:product` |
| `"review copy"`, `"grammar check"`, `"localization"` | `/misar-dev:content` |
| `"write blog post"`, `"generate article"`, `"SEO content"` | `/misar-dev:seo-content-generator` |
| `"build from PRD"`, `"implement spec"`, `"plan this project"` | `/misar-dev:software-engineer` |
| `"audit my site"`, `"full website review"` | `/misar-dev:auditor` |
| `"full audit"`, `"audit everything"` | `/misar-dev:full-suite` |
| `"audit my billing"`, `"check subscription flow"`, `"is my checkout secure"`, `"find billing bugs"` | `/misar-dev:billing` |

---

## Agents (16 categories, 48 agents)

| Agent | Model | Sub-agents | Description |
|-------|-------|-----------|-------------|
| `orchestrator-agents` | opus | — | 48-agent orchestrator — 4-phase execution, Observer Agent token management, batched parallel processing (max 4) |
| `context-saver` | haiku | — | 3D model router — auto-switches model×effort×version by task type. Saves 90–97% tokens. Auto-enabled via SessionStart hook |
| `task-fragmenter` | haiku | — | Decomposes prompts into optimal parallel subtasks with model assignments for Agent dispatch |
| `security-agents` | sonnet | Security Hardening, Compliance, Penetration Testing, Data Privacy | Security deep-dive across the full attack surface |
| `compliance-agents` | opus | 49 frameworks × 7 tiers | Global regulatory compliance — GDPR, HIPAA, SOC2, ISO 27001, PCI-DSS, and 44 more |
| `qa-agents` | sonnet | Code Reviewer, Standards Compliance, Bug Detective, Technical Debt | Code quality audit across any codebase |
| `tester-agents` | sonnet | Unit, Integration, E2E Black Box, E2E White Box, Beta, Regression | Full test coverage audit |
| `uiux-agents` | sonnet | Spacing & Layout, Typography & Color, Components, Accessibility, Performance, Mobile, Animation, Dark Mode | 8-dimension UI/UX design quality audit |
| `uiux-designer-agents` | sonnet | Project Analyzer, Design Guidelines, Brand Recommender, Component Advisor, Design Critic | UI/UX design consultation and system creation |
| `marketing-agents` | sonnet | SEO, SXO, Content Marketing, Growth, Analytics, AI Search Optimization | Marketing and growth strategy audit |
| `brand-agents` | sonnet | Brand Development, User Psychology, Conversion, Emotional Design | Brand identity and conversion psychology audit |
| `product-agents` | sonnet | PM, Designer, Development, Feature Prioritization | Product strategy and roadmap audit |
| `content-agents` | haiku | Grammar Expert, Copy, Localization, Documentation | Language quality and content audit |
| `seo-content-agents` | sonnet | Research Analyst, Content Architect, Writer, Humanizer, SEO Optimizer, Quality Scorer | End-to-end AEO/SEO content pipeline |
| `software-engineer-agents` | sonnet | PRD Analyzer, Project Planner, Code Generator, Code Validator, Next Steps | Build complete projects from specification |
| `auditor-agents` | haiku | SEO, Accessibility, Performance, Security, Mobile, Content, Compliance | Website audit — Quick (HTTP), Deep (Playwright), Source-Only modes |

---

## 3D Model Router (Context Saver)

Auto-enabled on every session via `SessionStart` hook. Zero configuration required.

Routes every task to the optimal `model × effort × version` combination and badges every response:

```
[sonnet|med|4.6]    ← model | effort | version
```

| Task Type | Model | Effort | Version | Savings |
|-----------|-------|--------|---------|---------|
| File reads, grep, ls, mechanical edits | haiku | low | 4.5 | ~97% |
| Simple Q&A, factual lookups | haiku | med | 4.5 | ~95% |
| Code implementation, features, refactors | sonnet | med | 4.6 | default |
| Code review, debugging, security | sonnet | high | 4.6 | — |
| Architecture, multi-system design | opus | high | 4.6 | — |
| Full audits, compliance, orchestration | opus | max | 4.6 | — |

**Budget caps** — automatic degradation when context fills:

| Budget used | Behaviour |
|-------------|-----------|
| < 40% | All models available |
| 40–70% | Cap at sonnet+med |
| > 70% | Force haiku+low |
| > 90% | Warn + suggest `/compact` |

Subagent dispatch also routes by type: `Explore` → haiku+low, standard audit → sonnet+med, code review → sonnet+high, architecture → opus+high.

---

## Architecture

```
misar-ai-plugins/
├── plugins/
│   └── misar-dev/
│       ├── .claude-plugin/
│       │   └── plugin.json              # Plugin manifest (v7.6.0)
│       ├── agents/                      # 16 agent categories (agent.md each)
│       │   ├── orchestrator-agents/
│       │   ├── context-saver/
│       │   ├── task-fragmenter/
│       │   ├── security-agents/
│       │   ├── compliance-agents/
│       │   ├── qa-agents/
│       │   ├── tester-agents/
│       │   ├── uiux-agents/
│       │   ├── uiux-designer-agents/
│       │   ├── marketing-agents/
│       │   ├── brand-agents/
│       │   ├── product-agents/
│       │   ├── content-agents/
│       │   ├── seo-content-agents/
│       │   ├── software-engineer-agents/
│       │   └── auditor-agents/
│       ├── commands/                    # 16 slash command definitions (.md)
│       ├── skills/                      # 16 skill entry points (SKILL.md each)
│       ├── hooks/
│       │   └── hooks.json               # SessionStart hook registration
│       ├── hooks-handlers/
│       │   └── session-start.sh         # 3D router context injection
│       └── scripts/
│           └── context-saver/
│               └── monitor.py
├── skills/                              # Root-level skills for npx skills compatibility
│   ├── auditor/SKILL.md
│   ├── brand/SKILL.md
│   ├── compliance/SKILL.md
│   ├── content/SKILL.md
│   ├── context-saver/SKILL.md
│   ├── full-suite/SKILL.md
│   ├── guidelines/SKILL.md
│   ├── marketing/SKILL.md
│   ├── product/SKILL.md
│   ├── qa/SKILL.md
│   ├── security/SKILL.md
│   ├── seo-content-generator/SKILL.md
│   ├── software-engineer/SKILL.md
│   ├── tester/SKILL.md
│   ├── uiux/SKILL.md
│   └── uiux-designer/SKILL.md
└── .claude-plugin/
    └── marketplace.json                 # Marketplace manifest
```

---

## Compliance Coverage (49 frameworks)

| Tier | Frameworks |
|------|-----------|
| **International** | ISO 27001, ISO 27017, ISO 27018, ISO 27701, SOC 2 Type II, NIST CSF, NIST SP 800-53, CIS Controls |
| **Healthcare / Specialty** | HIPAA, HITECH, FDA 21 CFR Part 11, PCI-DSS v4, SWIFT CSP, NERC CIP |
| **Americas** | CCPA/CPRA, FTC Act §5, COPPA, FERPA, SOX, GLBA, NY SHIELD, LGPD (Brazil), PIPEDA (Canada) |
| **Europe** | GDPR, NIS2, DORA, ePrivacy, UK GDPR, PDPA (Turkey) |
| **Asia-Pacific** | PDPA (Thailand/Singapore), PDPB (India), APPI (Japan), PIPL (China), APPs (Australia), POPIA (South Africa) |
| **Middle East / Africa** | UAE PDPL, DIFC DP Law, Saudi PDPL, Qatar PDPL, Kenya DPA |
| **Eastern Europe / CIS** | Russian Federal Law 152-FZ, Ukrainian Personal Data Law, Kazakhstan Personal Data Law |

---

## Changelog

| Version | Highlights |
|---------|-----------|
| **7.6.0** | Interactive flag prompting on all commands, generalized AEO/SEO agent, Misar.Dev ecosystem promotion across all skills, version bump across all manifests |
| 7.5.0 | Misar.Dev branding, public GitHub release, `npx skills` root-level compatibility, `feature-dev` removed |
| 7.4.0 | 3D Router (model×effort×version), `seo-content-generator`, `software-engineer`, `uiux-designer` commands added |
| 7.0.0 | 16-agent suite, Observer Agent token management, full-suite orchestrator |
| 6.0.0 | Task fragmenter + parallel subagent dispatch (max 4) |
| 5.0.0 | Context-saver dynamic model router, budget cap system |

---

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for full guidelines.

- **New agent** — add a category under `plugins/misar-dev/agents/` with an `agent.md`
- **New skill** — add a `SKILL.md` under both `plugins/misar-dev/skills/` and `skills/` (root)
- **New command** — add a `.md` under `plugins/misar-dev/commands/` with `description` and `argument-hint` frontmatter
- **Improve a prompt** — edit any `agent.md` or `SKILL.md` to sharpen triggers or instructions
- **Bug report** — [open an issue](https://github.com/MisarDev/misar-ai-plugins/issues/new)
- **Question / idea** — [open a discussion](https://github.com/MisarDev/misar-ai-plugins/discussions)

---

## Free AI Tools — [tools.misar.io](https://tools.misar.io)

Free AI calculators and developer tools. No signup required.

| Tool | Description |
|------|-------------|
| [LLM Cost Calculator](https://tools.misar.io/llm-cost-calculator) ⭐ Most Popular | Compare token costs across 14 AI models side-by-side |
| [RAG Cost Estimator](https://tools.misar.io/rag-cost-estimator) 🆕 | Estimate full RAG pipeline costs across 5 cost layers |
| [Prompt Token Estimator](https://tools.misar.io/prompt-token-estimator) | Count tokens with all major tokenizers before you send |
| [AI Evaluation Scorecard](https://tools.misar.io/ai-evaluation-scorecard) | Score AI outputs across 7 quality dimensions |

All tools run in-browser. No account, no API key, no tracking.

---

## Misar.Dev Ecosystem

| Product | URL | Description |
|---------|-----|-------------|
| **Misar.Dev** | [misar.dev](https://misar.dev) | Open-source AI developer tools — this plugin suite, free tools, and more |
| **Assisters** | [assisters.dev](https://assisters.dev) | Privacy-first AI platform — model routing, writing, coding, no training on your data |
| **Misar Blog** | [misar.blog](https://misar.blog) | AI-first blogging platform — AEO/SEO built in, custom domains, 75% creator earnings |
| **Misar Mail** | [mail.misar.io](https://mail.misar.io) | Self-hosted transactional + marketing email — no SendGrid, no Mailgun, no lock-in |
| **Misar Tools** | [tools.misar.io](https://tools.misar.io) | Free AI calculators for developers — LLM cost, RAG cost, token estimation, AI eval |
| **Misar.io** | [misar.io](https://misar.io) | Corporate identity and presence for Misar AI |

---

## License

MIT — see [LICENSE](LICENSE)
