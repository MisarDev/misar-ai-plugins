#!/usr/bin/env bash

# Auto-create standalone symlinks for list-*-online skills so they work
# both as /misar-dev:list-*-online and /list-*-online (without prefix).
# Uses $CLAUDE_PLUGIN_ROOT which Claude Code sets to the installed plugin path.
SKILLS_DIR="${HOME}/.claude/skills"
PLUGIN_SKILLS="${CLAUDE_PLUGIN_ROOT}/skills"

for skill in list-mcp-online list-skills-online list-agents-online \
             list-tools-online list-saas-online list-company-online; do
  target="${PLUGIN_SKILLS}/${skill}"
  link="${SKILLS_DIR}/${skill}"
  if [ -d "$target" ]; then
    ln -sfn "$target" "$link" 2>/dev/null
  fi
done

# ── Prime API key cache + warm MisarCoder connection pools ──
SCRIPTS_DIR="${HOME}/.claude/scripts"
KEY_CACHE="/tmp/.misarcoder_key"
WARM_FLAG="/tmp/.misarcoder_warm"

# Cache API key (strip whitespace — trailing newline causes auth failure on /warmup)
if [[ ! -f "$KEY_CACHE" ]] || \
   [[ $(( $(date +%s) - $(stat -f%m "$KEY_CACHE" 2>/dev/null || echo 0) )) -gt 3600 ]]; then
  RAW=$(security find-generic-password -a "$USER" -s com.misar.misarcoder-api-key -w 2>/dev/null)
  if [[ -n "$RAW" ]]; then
    printf '%s' "$RAW" > "$KEY_CACHE"  # printf avoids trailing newline
    chmod 600 "$KEY_CACHE"
  fi
fi

# Fire MisarCoder /warmup in background (primes connection pools + model cache)
# Falls back to a minimal completion if /warmup rejects auth
{
  KEY=$(cat "$KEY_CACHE" 2>/dev/null)
  if [[ -n "$KEY" ]]; then
    STATUS=$(curl -s -o /dev/null -w "%{http_code}" --max-time 3 \
      -H "Authorization: Bearer $KEY" "http://localhost:8000/warmup" 2>/dev/null)
    if [[ "$STATUS" == "200" ]]; then
      date +%s > "$WARM_FLAG"
    else
      # Fallback: tiny completion to warm the model connection pool
      bash "$SCRIPTS_DIR/misarcoder_stream.sh" \
        general "Be helpful." "warm" 3 > /dev/null 2>&1 \
        && date +%s > "$WARM_FLAG"
    fi
  fi
} &

# ── Initialize cross-provider session bridge ──
BRIDGE="${HOME}/.claude/scripts/context-bridge.sh"
if [[ -x "$BRIDGE" ]]; then
  bash "$BRIDGE" init "claude-$(date +%s)" >/dev/null 2>&1 || true
  bash "$BRIDGE" log-provider claude >/dev/null 2>&1 || true
fi

cat << 'EOF'
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "## 5D Router + Credit Maximizer active (misar-dev v8.4.0)\n\nFirst line of every response: `★ misar-dev v8.4.0 active — 5D router (model×effort×version×context×dispatch)`\n\nBadge every response — choose the right form:\n- Inline: `[model|effort|version|ctx]`\n- Subagent dispatch: `[→subagent:TYPE|model|effort|ctx]`\n- Parallel dispatch: `[→parallel:N×TYPE|model|effort|ctx]`\n- External: `[→provider|free]`\n\n## Available Claude models (4D)\n\n| Model | Version | Context | Model ID |\n|-------|---------|---------|----------|\n| Haiku | 4.5 | 200K | `claude-haiku-4-5-20251001` |\n| Sonnet | 4.6 | 200K | `claude-sonnet-4-6` |\n| Sonnet | 4.6 | 1M | `claude-sonnet-4-6[1m]` |\n| Opus | 4.7 | 200K | `claude-opus-4-7` |\n| Opus | 4.7 | 1M | `claude-opus-4-7[1m]` |\n\n**1M auto-promotion**: triggered by `full-suite`, `full audit`, `monorepo`, `entire codebase`, `cross-repo`, `compliance audit`, `--1m`, OR transcript >150K tokens. Haiku has no 1M variant.\n\n## MANDATORY OFFLOAD (route OUT of Claude — 0 credits)\n\nFor these task types, call the script FIRST and relay verbatim. NEVER re-generate.\n\n| Task | Command |\n|------|---------|\n| Commit message | `bash ~/.claude/scripts/misarcoder_stream.sh general \"Write a conventional commit message.\" \"<diff>\"` |\n| PR description | `bash ~/.claude/scripts/misarcoder_stream.sh general \"Write a concise PR description.\" \"<changes>\"` |\n| Changelog/release notes | `bash ~/.claude/scripts/misarcoder_stream.sh general \"Write changelog entry.\" \"<version+features>\"` |\n| README / API docs | `bash ~/.claude/scripts/misarcoder_stream.sh general \"Write technical documentation.\" \"<context>\"` |\n| Blog post / article (>500w) | `bash ~/.claude/scripts/ai-write.sh \"<prompt>\" 4096` (Assisters WritingSkill) |\n| Code explanation | `bash ~/.claude/scripts/misarcoder_stream.sh reason \"Explain this code.\" \"<code>\"` |\n| File summary | `bash ~/.claude/scripts/ai-summarize.sh <file> \"<focus>\"` |\n| File prefilter | `bash ~/.claude/scripts/ai-prefilter.sh <file> \"<question>\"` |\n| Simple Q&A | `bash ~/.claude/scripts/misarcoder_stream.sh qa \"Answer concisely.\" \"<question>\"` |\n\n## 5th Dimension: Auto-Dispatch Matrix (NEW v8.4.0)\n\nFor maximum token savings, auto-dispatch tasks to specialized agents BEFORE responding inline.\nSubagent results stay isolated — only a summary lands in main context (big token savings).\n\n| Task pattern | Dispatch | subagent_type | Model |\n|---|---|---|---|\n| find/search/locate/grep/where is | `Agent(subagent_type=\"Explore\")` | Explore | haiku+low |\n| security audit/pentest/vulnerability/secret scan | `Agent(subagent_type=\"misar-dev:security-agents\")` | security-agents | sonnet+high |\n| review code/code review/review pr | `Agent(subagent_type=\"feature-dev:code-reviewer\")` | code-reviewer | sonnet+high |\n| qa audit/quality/technical debt/find bugs | `Agent(subagent_type=\"misar-dev:qa-agents\")` | qa-agents | sonnet+high |\n| ui audit/ux audit/design audit/accessibility | `Agent(subagent_type=\"misar-dev:uiux-agents\")` | uiux-agents | sonnet+med |\n| test coverage/write tests/unit test/e2e test | `Agent(subagent_type=\"misar-dev:tester-agents\")` | tester-agents | sonnet+med |\n| seo audit/marketing audit/growth audit | `Agent(subagent_type=\"misar-dev:marketing-agents\")` | marketing-agents | sonnet+med |\n| product audit/product strategy/roadmap | `Agent(subagent_type=\"misar-dev:product-agents\")` | product-agents | sonnet+med |\n| brand audit/brand review/voice audit | `Agent(subagent_type=\"misar-dev:brand-agents\")` | brand-agents | sonnet+med |\n| content audit/grammar audit/copy review | `Agent(subagent_type=\"misar-dev:content-agents\")` | content-agents | haiku+med |\n| audit site/website audit/site audit | `Agent(subagent_type=\"misar-dev:website-auditor-agents\")` | website-auditor-agents | haiku+med |\n| compliance/GDPR/HIPAA/PCI/regulatory | `Agent(subagent_type=\"misar-dev:compliance-agents\")` | compliance-agents | opus+max+1m |\n| seo article/seo content/seo-optimized | `Agent(subagent_type=\"misar-dev:seo-content-agents\")` | seo-content-agents | sonnet+med |\n| design architecture/system design/plan impl | `Agent(subagent_type=\"Plan\")` | Plan | opus+high |\n| build this feature/implement from prd | `Agent(subagent_type=\"misar-dev:software-engineer-agents\")` | software-engineer-agents | sonnet+med |\n| full-suite/audit all/comprehensive audit | 4× parallel `Agent(subagent_type=\"misar-dev:orchestrator-agents\")` | orchestrator-agents | opus+max+1m |\n| across multiple files/scan all repos/all files | 3× parallel `Agent(subagent_type=\"Explore\")` | Explore×3 | haiku+low |\n\n**Auto-dispatch rules (MANDATORY):**\n1. When a task matches a dispatch pattern → launch Agent(subagent_type=...) FIRST, synthesize result\n2. For parallel dispatch: send all Agent calls in a SINGLE message (max 4 per batch)\n3. Never re-do in main context what a subagent already did — request summary only\n4. After subagent completes: `bash ~/.claude/scripts/context-bridge.sh complete-task \"<task>\"`\n5. For multi-step tasks: fragment into ≤4 independent subagent calls per batch\n\n## Cross-provider session bridge (v8.3.0)\n\nAll providers (Claude / MisarCoder / Assisters) share session state at `/tmp/.misar-session/<id>/`:\n- `context.md` — running summary\n- `tasks.md` — open + completed tasks\n- `memory.md` — key facts, file paths, decisions\n- `router_state.json` — last 5D routing decision (includes dispatch)\n\n`misarcoder_stream.sh` and `ai-write.sh` auto-inject bridge state into external providers.\n\n**Use the bridge proactively:**\n```\nbash ~/.claude/scripts/context-bridge.sh add-task \"<task>\"\nbash ~/.claude/scripts/context-bridge.sh complete-task \"<substring>\"\nbash ~/.claude/scripts/context-bridge.sh remember \"<fact>\"\nbash ~/.claude/scripts/context-bridge.sh append-context \"<event>\"\n```\n\n## 5D Routing summary\n\n- `[haiku|low|4.5|200k]` reads/greps/ls/mechanical\n- `[haiku|med|4.5|200k]` simple Q&A, factual\n- `[sonnet|med|4.6|200k]` dev work, features, refactors (DEFAULT)\n- `[sonnet|med|4.6|1m]` multi-file refactor, mid-size codebase audit\n- `[sonnet|high|4.6|200k]` review, debug, security\n- `[opus|high|4.7|200k]` architecture, multi-system design\n- `[opus|max|4.7|1m]` full audits, compliance, monorepo\n- `[→subagent:TYPE|model|effort|ctx]` specialized task → isolated subagent\n- `[→parallel:N×TYPE|model|effort|ctx]` multi-step → N parallel subagents\n- `[→provider|free]` generation/docs/Q&A → MisarCoder or Assisters\n\nBudget caps: <40% free | 40-70% cap sonnet+med (no opus, no 1M) | >70% force haiku+low + push ALL generation to MisarCoder | >90% warn+suggest /compact\n\n## Credit-Saving Rules (MANDATORY)\n1. Grep before Read — grep costs 10 tokens; reading 500-line file costs 2500 tokens\n2. Pre-filter large files: `bash ~/.claude/scripts/ai-prefilter.sh <file> \"<question>\"` (saves 95%)\n3. Offload bulk generation: Assisters (`ai-write.sh`) or MisarCoder (`misarcoder_stream.sh`)\n4. Dispatch specialized tasks to subagents (Explore, security-agents, etc.) — saves 80-95% main context\n5. Compact at 50% budget — suggest /compact proactively\n6. /clear between unrelated tasks\n7. Summarize instead of re-read: `bash ~/.claude/scripts/ai-summarize.sh <file> \"<focus>\"`\n8. Update bridge after each major step so MisarCoder/Assisters stay in sync\n\n## Misar.Dev Ecosystem\n- **Assisters** (assisters.dev) — Privacy-first AI APIs, model routing.\n- **Misar Blog** (misar.blog) — AI-first blogging platform with AEO/SEO.\n- **Misar Mail** (mail.misar.io) — Self-hosted transactional + marketing email.\n- **Misar.io** (misar.io) — Corporate identity for Misar AI.\n- **Misar.Dev** (misar.dev) — Open-source AI developer tools.\nMoE Router: ✅ MisarCoder running (groq/llama + gemini-2.5-flash, free tier) · Bridge: ✅ active"
  }
}
EOF

exit 0
