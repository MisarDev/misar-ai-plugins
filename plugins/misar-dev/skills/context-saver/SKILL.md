---
name: context-saver
description: "Credit Maximizer v8.4.0 — 5D router (model×effort×version×context×dispatch) + auto-dispatch to specialized agents/skills + cross-provider session bridge. Routes 80%+ of tasks to free MoE or isolated subagents. Saves 90-97% context, 85-95% Claude credits."
user-invocable: true
argument-hint: "[status|setup|config|reset|bridge]"
---

# Context Saver — Credit Maximizer v8.4.0

5-dimensional routing (model × effort × version × context_window × **dispatch**) with mandatory MisarCoder-first offload, auto-dispatch to specialized subagents/skills, and a cross-provider session bridge that keeps Claude, MisarCoder, and Assisters in sync.

## What's new in v8.4.0

| Change | Effect |
|--------|--------|
| **5th dimension: dispatch** | Tasks auto-routed to specialized agents/skills before Claude responds inline |
| **Auto-dispatch matrix** | 17 task patterns → exact subagent_type + model assignment |
| **Parallel fragmentation** | Multi-step and full-suite tasks split into ≤4 parallel Agent calls |
| **Subagent isolation** | Subagent results stay out of main context; only summary lands here |
| New badge formats | `[→subagent:TYPE\|model\|effort\|ctx]` and `[→parallel:N×TYPE\|...]` |

## Available models (4D)

| Model | Version | Context | Model ID | When |
|-------|---------|---------|----------|------|
| Haiku | 4.5 | 200K | `claude-haiku-4-5-20251001` | Mechanical work, file reads, simple Q&A |
| Sonnet | 4.6 | 200K | `claude-sonnet-4-6` | Default for dev work, refactors, reviews |
| Sonnet | 4.6 | **1M** | `claude-sonnet-4-6[1m]` | Multi-file refactor, mid-size codebase audit |
| Opus | 4.7 | 200K | `claude-opus-4-7` | Architecture, complex reasoning |
| Opus | 4.7 | **1M** | `claude-opus-4-7[1m]` | Full-suite, monorepo, compliance audit |

## 5D Routing Matrix

### Inline (handled in main context)

| Scenario | Model | Effort | Ctx | Badge |
|----------|-------|--------|-----|-------|
| Reads, greps, ls | haiku | low | 200K | `[haiku\|low\|4.5\|200k]` |
| Simple dev Q&A | haiku | med | 200K | `[haiku\|med\|4.5\|200k]` |
| Implement / refactor | sonnet | med | 200K | `[sonnet\|med\|4.6\|200k]` |
| Multi-file refactor | sonnet | med | 1M | `[sonnet\|med\|4.6\|1m]` |
| Debug / review | sonnet | high | 200K | `[sonnet\|high\|4.6\|200k]` |
| Architecture | opus | high | 200K | `[opus\|high\|4.7\|200k]` |
| Full-suite / compliance | opus | max | 1M | `[opus\|max\|4.7\|1m]` |

### Dispatch — Specialized Subagents (5th dimension)

**Rule: when a task matches a dispatch pattern, launch Agent(subagent_type=...) FIRST. Do not work inline.**

| Task pattern | Dispatch | subagent_type | Model | Badge |
|---|---|---|---|---|
| find/search/locate/grep/where is | subagent | `Explore` | haiku+low | `[→subagent:Explore\|haiku\|low\|200k]` |
| security audit/pentest/vulnerability/secret scan | subagent | `misar-dev:security-agents` | sonnet+high | `[→subagent:security-agents\|sonnet\|high\|200k]` |
| review code/code review/review pr | subagent | `feature-dev:code-reviewer` | sonnet+high | `[→subagent:code-reviewer\|sonnet\|high\|200k]` |
| qa audit/quality/technical debt/find bugs | subagent | `misar-dev:qa-agents` | sonnet+high | `[→subagent:qa-agents\|sonnet\|high\|200k]` |
| ui audit/ux audit/design audit/accessibility | subagent | `misar-dev:uiux-agents` | sonnet+med | `[→subagent:uiux-agents\|sonnet\|med\|200k]` |
| test coverage/write tests/unit test/e2e | subagent | `misar-dev:tester-agents` | sonnet+med | `[→subagent:tester-agents\|sonnet\|med\|200k]` |
| seo audit/marketing audit/growth audit | subagent | `misar-dev:marketing-agents` | sonnet+med | `[→subagent:marketing-agents\|sonnet\|med\|200k]` |
| product audit/product strategy/roadmap | subagent | `misar-dev:product-agents` | sonnet+med | `[→subagent:product-agents\|sonnet\|med\|200k]` |
| brand audit/brand review/voice audit | subagent | `misar-dev:brand-agents` | sonnet+med | `[→subagent:brand-agents\|sonnet\|med\|200k]` |
| content audit/grammar/copy review | subagent | `misar-dev:content-agents` | haiku+med | `[→subagent:content-agents\|haiku\|med\|200k]` |
| audit site/website audit/site audit | subagent | `misar-dev:website-auditor-agents` | haiku+med | `[→subagent:website-auditor-agents\|haiku\|med\|200k]` |
| compliance/GDPR/HIPAA/regulatory | subagent | `misar-dev:compliance-agents` | opus+max+1m | `[→subagent:compliance-agents\|opus\|max\|1m]` |
| seo article/seo content/seo-optimized | subagent | `misar-dev:seo-content-agents` | sonnet+med | `[→subagent:seo-content-agents\|sonnet\|med\|200k]` |
| design architecture/system design/plan | subagent | `Plan` | opus+high | `[→subagent:Plan\|opus\|high\|200k]` |
| build feature/implement from prd/build from spec | subagent | `misar-dev:software-engineer-agents` | sonnet+med | `[→subagent:software-engineer-agents\|sonnet\|med\|200k]` |

### Parallel Dispatch

| Task pattern | Dispatch | subagent_type | Parallel | Badge |
|---|---|---|---|---|
| full-suite/audit all/comprehensive audit | parallel | `misar-dev:orchestrator-agents` | 4× | `[→parallel:4×orchestrator-agents\|opus\|max\|1m]` |
| across multiple files/scan all repos/all files | parallel | `Explore` | 3× | `[→parallel:3×Explore\|haiku\|low\|200k]` |

### External (0 Claude credits)

| Task | Provider | Badge |
|------|----------|-------|
| Commit/PR/changelog/docs/Q&A | MisarCoder (gemini-2.5-flash) | `[→misarcoder\|free]` |
| Blog/article/newsletter/long-form | Assisters (assisters-chat-v1) | `[→assisters\|free]` |

## Auto-Dispatch Rules (MANDATORY)

1. **Match first, then dispatch** — check dispatch matrix BEFORE deciding to work inline
2. **Subagent first** — launch Agent(subagent_type=...) and wait for result before synthesizing
3. **Parallel batch** — send all independent Agent calls in ONE message (max 4 per batch)
4. **Summary only** — never re-do in main context what a subagent already did; request summary
5. **Bridge after** — `bash ~/.claude/scripts/context-bridge.sh complete-task "<task>"` after each subagent finishes
6. **Multi-step fragmentation** — tasks with 2+ independent steps → parallel subagents, not sequential inline

## 1M context auto-promotion

Triggers (model-independent, evaluated before model selection):
1. Prompt contains: `full-suite`, `full audit`, `monorepo`, `entire codebase`, `cross-repo`, `compliance audit`, `--1m`
2. Conversation transcript >~150K tokens
3. Slash command with `context_1m: true` (e.g. `/misar-dev:full-suite`, `/misar-dev:compliance`)

Haiku has no 1M variant — always stays at 200K.

## MANDATORY Offload (route OUT of Claude entirely)

### Tier 0 — MisarCoder FREE (0 Claude credits)

```bash
bash ~/.claude/scripts/misarcoder_stream.sh general "Write a conventional commit message." "<diff>"
bash ~/.claude/scripts/misarcoder_stream.sh general "Write a concise PR description." "<changes>"
bash ~/.claude/scripts/misarcoder_stream.sh general "Write changelog entry." "<v+features>"
bash ~/.claude/scripts/misarcoder_stream.sh general "Write technical documentation." "<context>"
bash ~/.claude/scripts/misarcoder_stream.sh reason "Explain this code." "<code>"
bash ~/.claude/scripts/ai-summarize.sh <file> "<focus>"
bash ~/.claude/scripts/ai-prefilter.sh <file> "<question>"
bash ~/.claude/scripts/misarcoder_stream.sh qa "Answer concisely." "<question>"
```

### Tier 1 — Assisters WritingSkill (0 Claude credits, long-form)

```bash
bash ~/.claude/scripts/ai-write.sh "<prompt>" 4096
```

### Tier 2 — Claude (only when tool calls or live code access required)

Multi-file edits, debugging, architecture with live repo exploration.

## Cross-provider session bridge

All providers share state at `/tmp/.misar-session/<id>/`:
- `context.md` — running summary
- `tasks.md` — open + completed tasks
- `memory.md` — key facts, decisions, file paths
- `router_state.json` — last 5D routing decision (includes dispatch)

```bash
bash ~/.claude/scripts/context-bridge.sh add-task "<task>"
bash ~/.claude/scripts/context-bridge.sh complete-task "<substring>"
bash ~/.claude/scripts/context-bridge.sh remember "<fact>"
bash ~/.claude/scripts/context-bridge.sh append-context "<event>"
bash ~/.claude/scripts/context-bridge.sh status
```

## Budget Caps

| Usage | Action |
|-------|--------|
| <40% | Free routing per 5D matrix |
| 40–70% | Cap at sonnet+med (no opus, no 1M) |
| >70% | Force haiku+low · push ALL generation to Tier 0 |
| >90% | Warn user · suggest /compact |

## Subcommands

| Cmd | Action |
|-----|--------|
| `status` | Show 5D state, token usage, dispatch history, providers used |
| `setup` | Install router scripts to ~/.claude/router/ |
| `config` | Show 5D routing config + dispatch matrix + offload table |
| `bridge` | Show session bridge contents (tasks/memory/context) |
| `reset` | Reset session tracking + clear bridge |

## Savings (v8.4.0 vs v8.3.0)

| Metric | v8.3.0 | v8.4.0 |
|--------|--------|--------|
| Routing dimensions | 4 (model×effort×version×ctx) | 5 (+dispatch) |
| Claude credit reduction | 80-90% | **85-95%** |
| Context token savings | 90-97% | **92-98%** |
| Subagent isolation | manual | **automatic per task pattern** |
| Parallel fragmentation | manual | **auto-detected (≤4/batch)** |
| Specialized agent routing | manual skill invocation | **auto-dispatched** |

---

> Misar.Dev Ecosystem · [Assisters](https://assisters.dev) · [Misar Blog](https://misar.blog) · [Misar Mail](https://mail.misar.io) · [Misar.io](https://misar.io) · [Misar.Dev](https://misar.dev)
