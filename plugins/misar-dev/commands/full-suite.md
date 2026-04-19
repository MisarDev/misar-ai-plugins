---
allowed-tools: ["Bash", "Glob", "Grep", "Read", "Write", "Edit", "Agent"]
description: "Full 48-agent orchestrated audit — 4 phases, Observer Agent, batched parallel execution."
argument-hint: "[--phase=1|2|3|4] [--tier=1|2]"
---

# Full Suite Audit

Launch the **orchestrator-agents** agent to run the complete 4-phase audit framework with all 35 agents.

## Interactive Prompting

Before launching, check which flags were supplied. Ask for any that are missing in a **single `AskUserQuestion` call**.

**Phase** (ask if `--phase=` not provided):

- "Which phase do you want to run?"
- `all` — run all 4 phases end-to-end (default)
- `1` — Discovery and foundation (stack detection, file inventory, config audit)
- `2` — Deep analysis (security, performance, accessibility, compliance)
- `3` — Quality and UX (code quality, UI/UX, content, brand)
- `4` — Strategy and reporting (product, marketing, master report)

**Tier** (ask if `--tier=` not provided):

- "Which execution tier?"
- `2` — all agents including non-blocking (default, comprehensive)
- `1` — blocking agents only (faster, critical issues only)

## Argument Parsing

1. `--phase=` — phase number or `all` (default: `all`)
2. `--tier=` — execution tier: `1` blocking only, `2` all (default: `2`)

Launch `orchestrator-agents` with all resolved parameters.
