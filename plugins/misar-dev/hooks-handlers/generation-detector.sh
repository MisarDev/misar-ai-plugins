#!/usr/bin/env bash
# UserPromptSubmit — detects generation/Q&A tasks, pre-computes via MisarCoder (free MoE only)
# Converts expensive Claude output tokens into cheap input tokens
# v8.2.0 — expanded detection: commit msgs, PR descriptions, changelogs, release notes, docs, blog

INPUT=$(cat)
PROMPT=$(echo "$INPUT" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print((d.get('prompt', '') or d.get('user_prompt', '')))
" 2>/dev/null)
PROMPT_LOWER=$(echo "$PROMPT" | tr '[:upper:]' '[:lower:]')

# ── Skip short prompts (cheap anyway) ──
WORD_COUNT=$(echo "$PROMPT" | wc -w | tr -d ' ')
if [[ "${WORD_COUNT:-0}" -lt 5 ]]; then exit 0; fi

# ── HIGH-PRIORITY: Commit / PR / Changelog (bypass IS_COMPLEX — always pre-compute) ──
IS_COMMIT=$(echo "$PROMPT_LOWER" | grep -cE "(write (a |the |me )?(commit|conventional commit|git commit) message|generate (a )?commit message|commit message for|summarize.*for commit)" 2>/dev/null || true)
IS_COMMIT="${IS_COMMIT//[^0-9]/}"; IS_COMMIT="${IS_COMMIT:-0}"

IS_PR=$(echo "$PROMPT_LOWER" | grep -cE "(write (a |the |me )?(pr|pull request|github pr) (description|body|summary)|draft (a |the )?(pr|pull request) (description|body)|generate (a )?pr description|pr description for)" 2>/dev/null || true)
IS_PR="${IS_PR//[^0-9]/}"; IS_PR="${IS_PR:-0}"

IS_CHANGELOG=$(echo "$PROMPT_LOWER" | grep -cE "(write (a |the |me )?(changelog|change log|release notes|version notes)|generate (a )?(changelog|release notes)|draft (a )?(changelog|release notes))" 2>/dev/null || true)
IS_CHANGELOG="${IS_CHANGELOG//[^0-9]/}"; IS_CHANGELOG="${IS_CHANGELOG:-0}"

# High-priority: set task type immediately (skip IS_COMPLEX check)
HIGH_PRIORITY_TYPE=""
if [[ "$IS_COMMIT" -gt 0 ]]; then HIGH_PRIORITY_TYPE="general"; fi
if [[ "$IS_PR" -gt 0 ]] && [[ -z "$HIGH_PRIORITY_TYPE" ]]; then HIGH_PRIORITY_TYPE="general"; fi
if [[ "$IS_CHANGELOG" -gt 0 ]] && [[ -z "$HIGH_PRIORITY_TYPE" ]]; then HIGH_PRIORITY_TYPE="general"; fi

# If high-priority task detected, skip all other checks and go directly to pre-computation
if [[ -n "$HIGH_PRIORITY_TYPE" ]]; then
  TASK_TYPE="$HIGH_PRIORITY_TYPE"
else
  # ── Skip complex reasoning / code tasks (Claude is better for these) ──
  # Broad exclusion: technical/dev/codebase Q&A goes to Claude, not MisarCoder
  IS_COMPLEX=$(echo "$PROMPT_LOWER" | grep -cE "(fix|debug|why is|error|bug|broken|refactor|implement|build|create|add feature|write test|deploy|migrate|how (do|does|can|should) (i|you|we|it)|what (is|are|does|should)|why (does|is|are|do)|how to|difference between|when (should|do|to)|best (way|practice|approach)|explain (how|why|what|the)|help (me|with)|can you (help|fix|add|update|change|remove|show|check|review|look)|review|analyze|check|look at|show me|tell me (how|why|what)|typescript|javascript|react|next|supabase|sql|api|component|function|hook|type|interface|schema|migration|route|middleware|auth|stripe|webhook|cron|redis|docker|deploy|ci|git|npm|pnpm|lint|test)" 2>/dev/null || true)
  IS_COMPLEX="${IS_COMPLEX//[^0-9]/}"; IS_COMPLEX="${IS_COMPLEX:-0}"
  if [[ "$IS_COMPLEX" -gt 0 ]]; then exit 0; fi

  # ── Detect generation tasks ──
  IS_GENERATION=$(echo "$PROMPT_LOWER" | grep -cE "(write (a |an |me |the )?[0-9]?-?(sentence|word|para|paragraph|article|blog|post|essay|guide|tutorial|template|summary|intro|conclusion|outline|section|chapter|copy)|generate [0-9]+|bulk (generate|create|write)|write me [0-9]+|draft (a |an |[0-9]+ )|write (a |the )?readme|write (a |the )?(api |project )?documentation|write (a |the |me )?announcement|write (a |the |me )?email (copy|template|campaign)|write (a |the |me )?newsletter)" 2>/dev/null || true)
  IS_GENERATION="${IS_GENERATION//[^0-9]/}"; IS_GENERATION="${IS_GENERATION:-0}"

  # ── Detect simple Q&A (NON-technical only — no code/dev/product questions) ──
  IS_QA=$(echo "$PROMPT_LOWER" | grep -cE "(^what is (the )?(capital|population|currency|language|history|meaning|definition|origin)|^who (is|was|invented|discovered|founded|created|wrote|built)|^when (was|did|were) .*(born|died|founded|invented|discovered|happened|published)|^where (is|was|are|were) .*(located|born|founded|situated)|^how many (people|countries|continents|planets|elements)|^what year (was|did)|^pros and cons of (cooking|fitness|diet|travel|lifestyle)|^difference between (left|right|liberal|conservative|democrat|republican))" 2>/dev/null || true)
  IS_QA="${IS_QA//[^0-9]/}"; IS_QA="${IS_QA:-0}"

  # ── Detect documentation / changelog tasks (no file context needed) ──
  IS_DOCS=$(echo "$PROMPT_LOWER" | grep -cE "(write (a |the |me )?readme|write (a |the )?changelog|write (a |the )?(api |project )?documentation|write (a |the |me )?release notes|generate (a |the )?(api |project )?docs)" 2>/dev/null || true)
  IS_DOCS="${IS_DOCS//[^0-9]/}"; IS_DOCS="${IS_DOCS:-0}"

  TASK_TYPE=""
  if [[ "$IS_DOCS" -gt 0 ]]; then TASK_TYPE="generation"; fi
  if [[ "$IS_GENERATION" -gt 0 ]] && [[ -z "$TASK_TYPE" ]]; then TASK_TYPE="generation"; fi
  if [[ "$IS_QA" -gt 0 ]] && [[ -z "$TASK_TYPE" ]]; then TASK_TYPE="qa"; fi
fi

# ── Nothing to pre-compute ──
if [[ -z "$TASK_TYPE" ]]; then exit 0; fi

# ── Pre-compute via misarcoder_stream.sh (MisarCoder free MoE) ──
SCRIPTS_DIR="$(dirname "$0")/../scripts"
ANSWER_FILE=$(mktemp)

bash "$SCRIPTS_DIR/misarcoder_stream.sh" "$TASK_TYPE" "You are a helpful, concise assistant." "$PROMPT" 4096 > "$ANSWER_FILE" 2>/dev/null
ANSWER_SIZE=$(wc -c < "$ANSWER_FILE" 2>/dev/null | tr -d ' ')

if [[ -z "$ANSWER_SIZE" ]] || [[ "$ANSWER_SIZE" -lt 30 ]]; then
  rm -f "$ANSWER_FILE"
  # MisarCoder unavailable — let Claude subscription handle it silently
  exit 0
fi

# ── Inject pre-computed answer — Claude just relays it (~50 output tokens) ──
python3 - "$ANSWER_FILE" "$TASK_TYPE" << 'PYEOF'
import json, sys
answer_file = sys.argv[1]
task = sys.argv[2]
answer = open(answer_file, encoding='utf-8', errors='replace').read().strip()
print(json.dumps({'hookSpecificOutput': {'hookEventName': 'UserPromptSubmit',
  'additionalContext': '✅ Pre-computed by misarcoder_stream.sh (' + task + ' task — 0 Claude output tokens used):\n\n' + answer + '\n\n---\nRELAY INSTRUCTION: Output the pre-computed content above to the user directly. Do not re-generate it. Introduce it in 1 line max, then relay it verbatim.'}}))
PYEOF

rm -f "$ANSWER_FILE"
