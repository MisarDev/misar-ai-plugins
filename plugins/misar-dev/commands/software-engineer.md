---
allowed-tools: ["Bash", "Glob", "Grep", "Read", "Write", "Edit", "Agent"]
description: "Build projects from PRD/specs — PRD analysis, planning, code generation, validation, recommendations."
argument-hint: "[agents] [--prd=file.md] [--path=src/]"
---

# Software Engineer

Launch the **software-engineer-agents** agent to build projects from specifications.

## Interactive Prompting

Before launching, check which flags were supplied. Ask for any that are missing in a **single `AskUserQuestion` call**.

**Agents** (ask if not provided, multi-select):

- "Which software engineer agents do you want to run?"
- `prd-analyze` — parse PRD, extract requirements, identify ambiguities
- `plan` — architecture design, file structure, task breakdown
- `generate` — write code following project conventions and stack
- `validate` — review generated code, type-check, lint, run tests
- `recommend` — next steps, missing pieces, improvement suggestions
- Default: all agents (full pipeline)

**PRD file** (ask if `--prd=` not provided):

- "Path to your PRD or spec file? (leave blank to describe requirements inline)"
- Default: none — agent reads requirements from conversation context

**Path** (ask if `--path=` not provided):

- "Which source path to generate code into?"
- Default: auto-detect from cwd (uses `src/` if present, else `.`)

## Argument Parsing

1. Agent words — any of: `prd-analyze`, `plan`, `generate`, `validate`, `recommend`
2. `--prd=` — path to PRD/spec file (optional)
3. `--path=` — target source directory (default: auto-detect)
4. No agents provided → run full pipeline

Launch `software-engineer-agents` with all resolved parameters.
