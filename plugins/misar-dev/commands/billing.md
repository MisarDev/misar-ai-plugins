---
allowed-tools: ["Bash", "Glob", "Grep", "Read", "Write", "Edit", "Agent"]
description: "Billing & subscription audit — subscription lifecycle, pricing centralization, CSRF on payment forms, webhook integrity, Stripe/Paddle integration. Triggers: 'audit my billing', 'check subscription flow', 'is my checkout secure', 'review pricing config', 'find billing bugs'."
argument-hint: "[lifecycle|security|pricing|integrity] [--stack=stripe|paddle] [--path=src/]"
---

# Billing & Subscription Auditor

Launch the **billing-agents** agent to perform billing and subscription analysis.

## Interactive Prompting

Before launching, check which flags were supplied. Ask for any that are missing in a **single `AskUserQuestion` call**.

**Agents** (ask if none provided, multi-select):

- "Which billing audit areas do you want to cover?"
- `lifecycle` — subscription create/upgrade/downgrade/cancel/trial flows
- `security` — CSRF on payment forms, webhook signature verification, PCI exposure
- `pricing` — centralization of plan config, price ID resolution, hardcoded amounts
- `integrity` — webhook event coverage, idempotency guards, DB sync correctness
- Default: all 4 agents

**Stack** (ask only if not inferrable from imports/env vars):

- "Which payment processor?" (`stripe` / `paddle` — default: `stripe`)

**Path** (optional):

- "Scope to a specific directory? (leave blank for full repo scan)"

## Argument Parsing

1. Agent words — any of: `lifecycle`, `security`, `pricing`, `integrity`
2. `--stack=` — payment processor (default: `stripe`)
3. `--path=` — directory scope (default: full repo)

Launch `billing-agents` with all resolved parameters.
