---
allowed-tools: ["Bash", "Glob", "Grep", "Read", "Write", "Edit", "Agent"]
description: "UI/UX design audit — Spacing, Typography, Components, Accessibility, Performance, Mobile, Animation, Dark Mode."
argument-hint: "[agents] [--path=src/]"
---

# UI/UX Audit

Launch the **uiux-agents** agent to perform a comprehensive UI/UX design quality audit.

## Interactive Prompting

Before launching, check which flags were supplied. Ask for any that are missing in a **single `AskUserQuestion` call**.

**Agents** (ask if not provided, multi-select):

- "Which UI/UX audit agents do you want to run?"
- `spacing` — 8px grid adherence, padding consistency, layout rhythm
- `typography` — type scale, font pairing, line height, readability
- `components` — component API consistency, Radix/shadcn patterns, reuse
- `accessibility` — WCAG 2.2 AA, contrast ratios, ARIA, keyboard nav, 44px targets
- `performance` — render performance, animation cost, image optimization
- `mobile` — 320px breakpoint, touch targets, responsive layout
- `animation` — `prefers-reduced-motion`, transition timing, CSS keyframes
- `dark-mode` — dark theme completeness, color token usage, contrast in dark
- Default: all agents

**Path** (ask if `--path=` not provided):

- "Which source path to audit?"
- Default: auto-detect from cwd (uses `src/` if present, else `.`)

## Argument Parsing

1. Agent words — any of: `spacing`, `typography`, `components`, `accessibility`, `performance`, `mobile`, `animation`, `dark-mode`
2. `--path=` — source directory (default: auto-detect)
3. No agents provided → run all eight

Launch `uiux-agents` with all resolved parameters.
