---
name: context-saver
description: "Credit Maximizer v8.2.0 — mandatory MisarCoder-first offload + 3D Router. Routes 75%+ of tasks to free MoE (gemini-2.5-flash/groq). Saves 90-97% context, 75-85% Claude plan credits. Auto-enabled via SessionStart hook."
user-invocable: true
argument-hint: "[status|setup|config|reset]"
---

# Context Saver — Credit Maximizer (v8.2.0)

Mandatory MisarCoder-first protocol + 3D routing. Every response must route through the cheapest capable tier before Claude generates output.

## MANDATORY Offload Rules (ENFORCE EVERY RESPONSE)

**Before generating ANY output**, check this table. If the task matches, call the script first and relay the result — do NOT re-generate.

### Tier 0 — MisarCoder FREE (gemini-2.5-flash/groq · 0 Claude credits)

| Task Type | Script Call |
|-----------|-------------|
| Commit message | `bash ~/.claude/scripts/misarcoder_stream.sh general "Write a conventional commit message (type(scope): description)." "<diff summary or description>"` |
| PR description | `bash ~/.claude/scripts/misarcoder_stream.sh general "Write a concise GitHub PR description with Summary and Test plan sections." "<branch changes>"` |
| Changelog entry | `bash ~/.claude/scripts/misarcoder_stream.sh general "Write a changelog entry in Keep a Changelog format." "<version + features>"` |
| Release notes | `bash ~/.claude/scripts/misarcoder_stream.sh general "Write user-facing release notes." "<version + changes>"` |
| README section | `bash ~/.claude/scripts/misarcoder_stream.sh general "Write a README section." "<topic + context>"` |
| API / component docs | `bash ~/.claude/scripts/misarcoder_stream.sh general "Write concise technical documentation." "<code or API context>"` |
| Blog post / article | `bash ~/.claude/scripts/misarcoder_stream.sh generation "You are a technical blogger. Write engaging, accurate content." "<topic + outline>"` |
| Email / announcement | `bash ~/.claude/scripts/misarcoder_stream.sh generation "You are a copywriter." "<email brief>"` |
| Code explanation | `bash ~/.claude/scripts/misarcoder_stream.sh reason "Explain this code clearly and concisely." "<code snippet>"` |
| File summary | `bash ~/.claude/scripts/ai-summarize.sh <file> "<focus>"` |
| File prefilter | `bash ~/.claude/scripts/ai-prefilter.sh <file> "<question>"` |
| Simple factual Q&A | `bash ~/.claude/scripts/misarcoder_stream.sh qa "Answer concisely and accurately." "<question>"` |

**Relay rule**: Output the stream result directly to the user. 1 intro line max. Do NOT re-generate.
**Fallback**: If script exits 1 (MisarCoder offline), generate directly — never fail silently.

### Tier 1 — Assisters API (assisters-chat-v1 · minimal Claude credits)

For long-form content generation (>500 words expected):

```bash
curl -s https://assisters.dev/api/v1/chat/completions \
  -H "Authorization: Bearer $ASSISTERS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "assisters-chat-v1",
    "messages": [
      {"role": "system", "content": "SYSTEM_PROMPT"},
      {"role": "user", "content": "USER_PROMPT"}
    ],
    "max_tokens": 4096
  }' | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['choices'][0]['message']['content'])"
```

Use Tier 1 for: blog articles >500w, long-form documentation, SEO content pages, email campaigns.

### Tier 2 — Claude (default for tool-dependent work only)

Use Claude directly ONLY when:
- Multi-file code changes requiring Read/Edit/Write tool calls
- Bug fixes requiring root cause analysis across files
- Security reviews with access to live code
- Test writing requiring full codebase context
- Architecture decisions requiring repo exploration

## 3D Routing Matrix (Claude tasks only)

| Scenario | Model | Effort | Version |
|----------|-------|--------|---------|
| File reads, greps, ls | haiku | low | 4.5 |
| Simple dev Q&A | haiku | med | 4.5 |
| Implement / refactor | sonnet | med | 4.6 |
| Debug / review / test | sonnet | high | 4.6 |
| Architecture / design | opus | high | 4.6 |
| Full audit / compliance | opus | max | 4.6 |

## Budget Caps

| Usage | Action |
|-------|--------|
| <40% | Free routing |
| 40–70% | Cap at sonnet+med |
| >70% | Force haiku+low · push ALL generation to Tier 0 |
| >90% | Warn user · suggest /compact |

## Credit-Saving Protocol (MANDATORY every prompt)

1. **Grep before Read** — 10 tokens vs 2500+ for a 500-line file
2. **Prefilter large files**: `bash ~/.claude/scripts/ai-prefilter.sh <file> "<question>"` (saves ~95%)
3. **Summarize instead of re-read**: `bash ~/.claude/scripts/ai-summarize.sh <file> "<focus>"`
4. **All generation/docs tasks → Tier 0 FIRST** — check table above before typing a single word
5. **Compact at 50% budget** — suggest /compact proactively
6. **Subagent dispatch** — keep bulk work in subcontexts; relay summaries only

## Parallel Agent Dispatch

Fragment tasks with 2+ independent steps into ≤4 parallel Agent calls per batch:
- Explore=haiku+low · Standard audit=sonnet+med · Code review=sonnet+high · Architecture=opus+high
- Subagent work stays in subcontexts — only summaries return to main context

## Self-Invocation Context Saving

To compress context mid-session (approaching 50% budget):
```bash
bash ~/.claude/scripts/misarcoder_stream.sh reason \
  "Summarize this conversation to under 200 tokens. Preserve all technical decisions, file paths, open tasks, and any blockers." \
  "<recent conversation text>"
```

## Status / Setup Commands

```
/misar-dev:context-saver          # Show routing status
/misar-dev:context-saver status   # Show 3D routing state + token usage
/misar-dev:context-saver setup    # Install advanced router scripts to ~/.claude/router/
/misar-dev:context-saver config   # Show routing configuration
/misar-dev:context-saver reset    # Reset session tracking
```

## Savings (v8.2.0)

- **75-85% Claude credit reduction** (MisarCoder-first for generation/docs/Q&A)
- **90-97% context token savings** (parallel subcontexts + prefilter/summarize)
- **4x longer sessions** (150-200+ prompts without /compact)
- **Zero cost for generation tasks** (Tier 0 = gemini-2.5-flash free tier)

---

> **Misar.Dev Ecosystem** — [Assisters](https://assisters.dev) · [Misar Blog](https://misar.blog) · [Misar Mail](https://mail.misar.io) · [Misar.io](https://misar.io) · [Misar.Dev](https://misar.dev)
