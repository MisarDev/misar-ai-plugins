---
allowed-tools: ["Bash", "Glob", "Grep", "Read", "Write", "Edit", "Agent"]
description: "Billing & subscription audit — lifecycle, payment security, pricing centralization, webhook integrity."
argument-hint: "[lifecycle|security|pricing|integrity] [--stack=stripe|paddle] [--path=src/]"
---

# Billing Audit

Launch the **billing-agents** agent for a deep billing and subscription analysis.

## Interactive Prompting

Before launching, check which flags were supplied. Ask for any that are missing in a **single `AskUserQuestion` call**.

**Agents** (ask if not provided, multi-select):

- "Which billing agents do you want to run?"
- `lifecycle` — subscription signup, trial, upgrade/downgrade, cancellation, payment failure flows
- `security` — price/amount integrity, CSRF on checkout, webhook signature verification, key exposure
- `pricing` — pricing centralization, hardcoded Price IDs, test/prod separation
- `integrity` — webhook idempotency, DB sync, event deduplication, monitoring
- Default: all agents

**Stack** (ask if `--stack=` not provided):

- "Which billing stack are you using?"
- `stripe` (default)
- `paddle`

**Path** (ask if `--path=` not provided):

- "Which source path to audit?"
- Default: auto-detect from cwd (uses `src/` if present, else `.`)

## Argument Parsing

1. Agent words — any of: `lifecycle`, `security`, `pricing`, `integrity`
2. `--stack=` — billing provider: `stripe` or `paddle` (default: `stripe`)
3. `--path=` — source directory (default: auto-detect)
4. No agents provided → run all four

Launch `billing-agents` with all resolved parameters.
