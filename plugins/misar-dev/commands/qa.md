---
allowed-tools: ["Bash", "Glob", "Grep", "Read", "Write", "Edit", "Agent"]
description: "Code quality audit — Code Reviewer, Standards, Bug Detective, Technical Debt."
argument-hint: "[agents] [--path=src/]"
---

# Code Quality Audit

Launch the **qa-agents** agent to perform code quality analysis.

## Interactive Prompting

Before launching, check which flags were supplied. Ask for any that are missing in a **single `AskUserQuestion` call**.

**Agents** (ask if not provided, multi-select):

- "Which QA agents do you want to run?"
- `code-review` — logic errors, anti-patterns, security smells, readability
- `standards` — linting compliance, naming conventions, project style guide
- `bugs` — bug detection, edge cases, null handling, error boundaries
- `tech-debt` — complexity hotspots, dead code, dependency health
- Default: all agents

**Path** (ask if `--path=` not provided):

- "Which source path to audit?"
- Default: auto-detect from cwd (uses `src/` if present, else `.`)

## Argument Parsing

1. Agent words — any of: `code-review`, `standards`, `bugs`, `tech-debt`
2. `--path=` — source directory (default: auto-detect)
3. No agents provided → run all four

Launch `qa-agents` with all resolved parameters.
