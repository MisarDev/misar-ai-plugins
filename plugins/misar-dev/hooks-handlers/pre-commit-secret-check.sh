#!/usr/bin/env bash
# pre-commit-secret-check.sh
# PreToolUse hook — intercepts Bash tool calls before execution.
# Blocks git commit / git push / git add when staged diff contains likely secrets.
# Exit 0 = allow. Exit 2 = block (Claude Code cancels the tool call).

set -euo pipefail

# ── Read the tool input JSON from stdin ──────────────────────────────────────
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('command',''))" 2>/dev/null || echo "")

# Only intercept git commit / push / add operations
if ! echo "$COMMAND" | grep -qE '^\s*git\s+(commit|push|add)\b'; then
  exit 0
fi

# ── Collect staged diff ───────────────────────────────────────────────────────
DIFF=$(git diff --cached 2>/dev/null || true)

if [[ -z "$DIFF" ]]; then
  exit 0
fi

# ── Secret patterns ───────────────────────────────────────────────────────────
# Matches assignment patterns: KEY=value, KEY: value, KEY="value"
SECRET_PATTERN='(?i)(password|passwd|secret|api[_\-]?key|apikey|access[_\-]?key|auth[_\-]?token|bearer[_\-]?token|private[_\-]?key|client[_\-]?secret|db[_\-]?url|database[_\-]?url|connection[_\-]?string|jwt[_\-]?secret|encryption[_\-]?key|webhook[_\-]?secret|signing[_\-]?secret|stripe[_\-]?secret|sendgrid[_\-]?key|mailgun[_\-]?key|twilio[_\-]?(auth|account)|slack[_\-]?(token|secret)|github[_\-]?(token|secret)|openai[_\-]?key|anthropic[_\-]?key|google[_\-]?api|gemini[_\-]?key|aws[_\-]?(secret|access)[_\-]?key|azure[_\-]?(secret|key)|gcp[_\-]?key)\s*[=:]\s*["\x27]?[A-Za-z0-9_/+\-\.]{16,}'

# Matches well-known token/key prefixes
PREFIX_PATTERN='\b(sk-proj-|sk-ant-|ghp_|gho_|ghs_|github_pat_|xoxb-|xoxp-|xoxa-|ya29\.|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z\-_]{35})[A-Za-z0-9_\-\.\/+]{8,}'

# Matches PEM private keys
PEM_PATTERN='-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----'

# ── Scan ──────────────────────────────────────────────────────────────────────
FINDINGS=""

if echo "$DIFF" | grep -qP "$SECRET_PATTERN" 2>/dev/null; then
  FINDINGS="${FINDINGS}\n  • Credential assignment pattern detected in staged diff"
fi

if echo "$DIFF" | grep -qP "$PREFIX_PATTERN" 2>/dev/null; then
  FINDINGS="${FINDINGS}\n  • Known API key/token prefix detected (sk-*, ghp_*, AKIA*, etc.)"
fi

if echo "$DIFF" | grep -q "$PEM_PATTERN" 2>/dev/null; then
  FINDINGS="${FINDINGS}\n  • PEM private key detected"
fi

# ── Also check for .env files being added to staging ─────────────────────────
STAGED_FILES=$(git diff --cached --name-only 2>/dev/null || true)
ENV_STAGED=$(echo "$STAGED_FILES" | grep -E '^\.env(\.[a-z]+)?$|^\.infra\.secrets$' | grep -v '\.example$\|\.sample$\|\.template$' || true)

if [[ -n "$ENV_STAGED" ]]; then
  FINDINGS="${FINDINGS}\n  • Gitignored env file staged for commit: $ENV_STAGED"
fi

# ── Block if any finding ──────────────────────────────────────────────────────
if [[ -n "$FINDINGS" ]]; then
  echo ""
  echo "╔══════════════════════════════════════════════════════════════╗"
  echo "║  [env-guardian] SECRET DETECTED — git operation BLOCKED     ║"
  echo "╠══════════════════════════════════════════════════════════════╣"
  echo -e "║  Findings:${FINDINGS}"
  echo "╠══════════════════════════════════════════════════════════════╣"
  echo "║  Fix:                                                        ║"
  echo "║  1. Move the secret to a gitignored .env file                ║"
  echo "║  2. Replace inline value with \$ENV_VAR reference            ║"
  echo "║  3. Run: git restore --staged <file>  to unstage             ║"
  echo "║  4. If already committed: rotate the credential NOW          ║"
  echo "║     then: git filter-repo --invert-paths --path .env         ║"
  echo "╚══════════════════════════════════════════════════════════════╝"
  echo ""
  exit 2
fi

exit 0
