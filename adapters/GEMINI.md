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
TypeScript strict · Zod validation · conventional commits · no hardcoded secrets.
