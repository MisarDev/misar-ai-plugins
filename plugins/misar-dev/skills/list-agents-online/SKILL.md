---
name: list-agents-online
description: Submit AI agents to 35+ registries, directories, and community platforms for maximum discoverability. Use when the user wants to list an AI agent online, publish an agent to a registry, get an agent discovered, or mentions "list agent", "publish agent", "agent directory", "agent registry", "agent marketplace", "Hugging Face agent", "CrewAI", "LangChain Hub".
user-invocable: true
argument-hint: "[--config listing-config.yaml] [--dry-run] [--platforms huggingface,crewai,agenthub,...]"
---

# List Agents Online

Automated AI agent submission to 35+ registries and community platforms ranked by agent-ecosystem reach.

## Trigger
- User says "list agent online", "publish agent to registry", "get my agent discovered", "submit agent"
- User invokes `/list-agents-online`
- User mentions Hugging Face Hub, LangChain Hub, AgentHub, CrewAI templates, AutoGen, awesome-ai-agents

## Execution Protocol

### Phase 1: Prep
1. Collect agent details: name, description, framework (crewai/autogen/langgraph/claude/custom), category (coding/research/marketing/ops/data), GitHub repo, demo URL
2. Create tracker: `output/agents-listings-tracker-{date}.md` — columns: Platform | Status | URL | Notes
3. Status values: PENDING / SUBMITTING / SUBMITTED / LIVE / FAILED / SKIPPED / MANUAL

### Phase 2: Submission (per directory)
1. Navigate to submission/upload page
2. Method: web form → fill | GitHub PR → open PR | CLI push → run command | community post → draft | paid → **SKIPPED** | CAPTCHA → **MANUAL**
3. Fill all fields; submit; verify; update tracker immediately

### Phase 3: Parallelization
- CLI-based (Hugging Face Hub, LangChain Hub) run first via subprocess
- **Max 4 browser-based parallel agents** — more causes tab conflicts
- Print full MANUAL list at end

## Priority Agent Directories (Top 15)

| # | Platform | Submit URL | Type | Reach |
|---|----------|-----------|------|-------|
| 1 | Hugging Face Hub | huggingface.co/new | Model/Space registry | 5M+ models |
| 2 | LangChain Hub | smith.langchain.com/hub | Prompt/agent hub | 10M+ LangChain users |
| 3 | AgentHub.dev | agenthub.dev | Agent directory | Agent-specific |
| 4 | CrewAI Templates | github.com/crewAIInc/crewAI | GitHub PR | CrewAI ecosystem |
| 5 | AutoGen Community | github.com/microsoft/autogen | GitHub PR to examples | Microsoft AutoGen |
| 6 | FlowiseAI Marketplace | flowiseai.com | Form / GitHub | No-code agent builder |
| 7 | Relevance AI | relevanceai.com/templates | Partner form | Agent templates |
| 8 | awesome-ai-agents | github.com/e2b-dev/awesome-ai-agents | GitHub PR | Community list |
| 9 | LlamaIndex Hub | llamahub.ai | CLI push | LlamaIndex ecosystem |
| 10 | E2B.dev | e2b.dev | Form / PR | Sandboxed agents |
| 11 | misar-ai-plugins agents/ | git.misar.io/misaradmin/misar-ai-plugins | PR to agents/ | Misar.Dev marketplace |
| 12 | Claude.ai agents | claude.ai | Partner form | Official Anthropic |
| 13 | Claude Discord #showcase | discord.gg/anthropic | Post | High engagement |
| 14 | GitHub Topics | github.com | Repo topics | Auto-discover |
| 15 | Product Hunt | producthunt.com/posts/new | Launch | 10M+ |

## Error Recovery

| Error | Action |
|-------|--------|
| "Repo already listed" | Mark ALREADY_LISTED, verify |
| PR already open | Link existing PR, mark PENDING |
| Required field missing | Re-read form snapshot, fill |
| CAPTCHA / reCAPTCHA | Mark **MANUAL** (not FAILED) |
| CLI auth error | Re-authenticate, retry |
| Paid only | Mark **SKIPPED** (note price) |
| Site down | Mark **FAILED** (down) |

## Contact / Form Defaults

```
Name: Gulshan Yadav | Email: gulshan@promo.misar.io | Company: Misar AI
GitHub: github.com/misar-ai | Twitter: @mrgulshanyadav | Location: India
```

## Automation Script

```bash
python ~/.claude/scripts/list_agents_auto.py --config listing-config.yaml
python ~/.claude/scripts/list_agents_auto.py --config listing-config.yaml --dry-run
python ~/.claude/scripts/list_agents_auto.py --config listing-config.yaml --platforms "huggingface,agenthub,crewai"
```

Full 35-directory database with per-platform submission steps lives in the tracker file generated each run.
