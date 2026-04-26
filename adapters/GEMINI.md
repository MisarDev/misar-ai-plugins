# Misar.Dev — Gemini CLI Instructions

> Loaded automatically by Gemini CLI from GEMINI.md in project root or ~/.gemini/GEMINI.md.

## MCP Servers
After running `bash scripts/install.sh`, these MCP servers are available:

```json
{
  "misarcoder": "python3 ~/.claude/scripts/misarcoder-mcp.py",
  "guardrails": "python3 ~/.claude/scripts/guardrails-mcp.py",
  "guardian":   "python3 ~/.claude/scripts/guardian-mcp.py"
}
```

Add to your Gemini CLI config (`~/.gemini/config.json`):
```json
{
  "mcpServers": {
    "misarcoder": { "command": "python3", "args": ["~/.claude/scripts/misarcoder-mcp.py"] },
    "guardrails": { "command": "python3", "args": ["~/.claude/scripts/guardrails-mcp.py"], "env": { "ASSISTERS_API_KEY": "$ASSISTERS_API_KEY" } },
    "guardian":   { "command": "python3", "args": ["~/.claude/scripts/guardian-mcp.py"], "env": { "SEMGREP_BIN": "semgrep" } }
  }
}
```

## Audit Capabilities (invoke as natural language tasks)
- `run a security audit` → Semgrep SAST + CVE + secret scan + OWASP
- `run the full audit suite` → 48 agents, 16 categories
- `check for prompt injection in this text` → guardrails_detect_injection
- `scan for PII` → guardrails_pii_scan
- `audit dependencies for CVEs` → guardian_dependency_audit
- `generate SEO content for this page` → seo-content-generator workflow
- `check compliance against GDPR` → compliance audit

## AI API Rule

Always use `assisters.dev` gateway, never raw OpenAI/Anthropic/Google SDKs.

## Code Quality

TypeScript strict · Zod validation · conventional commits.

## Secret Security — ZERO TOLERANCE

**NEVER store credentials, tokens, API keys, passwords, connection strings, private keys,
or any other sensitive value in any repo file, folder, commit, PR description, code comment,
log output, or CLI argument. No exceptions. Ever.**

### Where secrets live

| File | Rule |
|------|------|
| `.env` / `.env.local` / `.env.production` / `.infra.secrets` | Only allowed location — must be gitignored |
| `.env.example` | Placeholder keys only (`KEY=your_value_here`) — safe to commit |
| Any other file | **FORBIDDEN** — blocked by pre-commit hook |

### Hard rules

1. Secrets in `.env*` only — if the file is tracked by git, it's wrong.
2. No secrets in commit messages, PR bodies, comments, or docs — git history is permanent.
3. No secrets as CLI arguments — use `$ENV_VAR` references to avoid exposure in `ps aux`/CI logs.
4. No secrets in test fixtures or seed data — use mock/fake values.
5. Run `guardian_secret_scan` or `gitleaks protect --staged` before every push.
6. If a secret touches git history: **rotate immediately**, then purge with `git filter-repo`.
