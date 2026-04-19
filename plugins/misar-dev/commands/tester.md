---
allowed-tools: ["Bash", "Glob", "Grep", "Read", "Write", "Edit", "Agent"]
description: "Testing audit — Unit, Integration, E2E, Beta, Regression test coverage."
argument-hint: "[agents] [--path=src/]"
---

# Testing Audit

Launch the **tester-agents** agent to analyze test coverage and quality.

## Interactive Prompting

Before launching, check which flags were supplied. Ask for any that are missing in a **single `AskUserQuestion` call**.

**Agents** (ask if not provided, multi-select):

- "Which tester agents do you want to run?"
- `unit` — unit test coverage, mocking patterns, assertion quality
- `integration` — API and service integration test coverage
- `e2e-black-box` — E2E tests from user perspective, happy paths, edge cases
- `e2e-white-box` — E2E tests with internal state knowledge, branch coverage
- `beta` — exploratory testing, usability, real-world scenario simulation
- `regression` — regression suite health, flaky test detection
- Default: all agents

**Path** (ask if `--path=` not provided):

- "Which source path to audit?"
- Default: auto-detect from cwd (uses `src/` if present, else `.`)

## Argument Parsing

1. Agent words — any of: `unit`, `integration`, `e2e-black-box`, `e2e-white-box`, `beta`, `regression`
2. `--path=` — source directory (default: auto-detect)
3. No agents provided → run all six

Launch `tester-agents` with all resolved parameters.
