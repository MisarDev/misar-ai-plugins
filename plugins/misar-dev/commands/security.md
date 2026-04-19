---
allowed-tools: ["Bash", "Glob", "Grep", "Read", "Write", "Edit", "Agent"]
description: "Security deep-dive — Hardening, Compliance, Penetration Testing, Data Privacy."
argument-hint: "[agents] [--path=src/]"
---

# Security Audit

Launch the **security-agents** agent for a deep security analysis.

## Interactive Prompting

Before launching, check which flags were supplied. Ask for any that are missing in a **single `AskUserQuestion` call**.

**Agents** (ask if not provided, multi-select):

- "Which security agents do you want to run?"
- `hardening` — security headers, CSP, HSTS, cookie flags, XSS vectors
- `compliance` — OWASP Top 10, CWE/CVE patterns, input validation
- `pentest` — attack surface mapping, injection points, auth weaknesses
- `privacy` — data exposure, PII handling, GDPR/CCPA readiness
- Default: all agents

**Path** (ask if `--path=` not provided):

- "Which source path to audit?"
- Default: auto-detect from cwd (uses `src/` if present, else `.`)

## Argument Parsing

1. Agent words — any of: `hardening`, `compliance`, `pentest`, `privacy`
2. `--path=` — source directory (default: auto-detect)
3. No agents provided → run all four

Launch `security-agents` with all resolved parameters.
