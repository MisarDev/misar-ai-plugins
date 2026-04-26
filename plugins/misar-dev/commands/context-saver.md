---
allowed-tools: ["Bash", "Glob", "Grep", "Read", "Write", "Edit", "Agent"]
description: "Credit Maximizer v8.3.0 — 4D Router (model×effort×version×context) + cross-provider session bridge (Claude ⇄ MisarCoder ⇄ Assisters). Auto-promotes 1M context for full-suite/monorepo. 80-90% Claude credit reduction."
argument-hint: "[status|setup|config|reset|bridge]"
---

Run the Context Saver Credit Maximizer (v8.3.0).

**Arguments:**
- `status` (default) — Show 4D routing state (model+effort+version+context), token usage, MisarCoder availability, providers used this session
- `setup` — Install router scripts to ~/.claude/router/
- `config` — Show 4D routing configuration + offload table + 1M-context triggers
- `reset` — Reset session tracking, model state, and clear shared session bridge
- `bridge` — Show cross-provider session bridge contents (tasks/memory/context shared with MisarCoder/Assisters)

**Auto-Enabled:** The mandatory MisarCoder-first protocol + 4D routing + session bridge are automatically active via SessionStart hook when misar-dev is installed.

**Available Claude models (v8.3.0):**

| Model | Version | Context | When |
|-------|---------|---------|------|
| Haiku | 4.5 | 200K | Mechanical work, file reads, simple Q&A |
| Sonnet | 4.6 | 200K | Default for dev work, refactors, reviews |
| Sonnet | 4.6 | **1M** | Multi-file refactor, mid-size codebase audit |
| Opus | 4.7 | 200K | Architecture, complex reasoning |
| Opus | 4.7 | **1M** | Full-suite audit, monorepo, compliance |

**1M auto-promotion** triggers on: `full-suite`, `full audit`, `audit all`, `monorepo`, `entire codebase`, `cross-repo`, `compliance audit`, `--1m`, OR transcript >150K tokens.

**External offload (0 Claude credits):**
- MisarCoder (`gemini-2.5-flash` / `groq`) — commit msgs, PR descriptions, changelogs, READMEs, code explanations, simple Q&A
- Assisters (`assisters-chat-v1`) — blog posts, articles, tutorials, newsletters, marketing copy, long-form docs

**Cross-provider session bridge (NEW):** Shared state at `/tmp/.misar-session/<id>/` (`context.md`, `tasks.md`, `memory.md`, `router_state.json`) is auto-injected into MisarCoder/Assisters system prompts so all 3 providers stay in sync within a session.

```bash
bash ~/.claude/scripts/context-bridge.sh add-task "<task>"
bash ~/.claude/scripts/context-bridge.sh remember "<fact>"
bash ~/.claude/scripts/context-bridge.sh status
```
