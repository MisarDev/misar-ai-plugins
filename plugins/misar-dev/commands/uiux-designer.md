---
allowed-tools: ["Bash", "Glob", "Grep", "Read", "Write", "Edit", "Agent"]
description: "UI/UX design consultation — Project analysis, design system, brand identity, component specs, design critique."
argument-hint: "[agents] [--platform=web] [--component=button]"
---

# UI/UX Designer

Launch the **uiux-designer-agents** agent to perform design consultation.

## Interactive Prompting

Before launching, check which flags were supplied. Ask for any that are missing in a **single `AskUserQuestion` call**.

**Agents** (ask if not provided, multi-select):

- "Which design consultation agents do you want to run?"
- `analyze` — project structure, existing design patterns, stack detection
- `guidelines` — generate design system rules, spacing, typography, color tokens
- `brand` — brand identity recommendations, visual language, tone
- `component` — component-level specs and usage guidelines
- `critique` — design critique of existing UI against best practices
- Default: all agents

**Platform** (ask if `--platform=` not provided):

- "Which platform are you designing for?"
- `web` — responsive web app (default)
- `mobile` — React Native or Flutter mobile app
- `desktop` — Electron or desktop web app

**Component** (ask if `--component=` not provided — optional):

- "Specific component to focus on? (leave blank for full project scope)"
- Examples: `button`, `form`, `navigation`, `card`, `modal`
- Default: none — full project scope

## Argument Parsing

1. Agent words — any of: `analyze`, `guidelines`, `brand`, `component`, `critique`
2. `--platform=` — target platform (default: `web`)
3. `--component=` — specific component focus (optional)
4. No agents provided → run all five

Launch `uiux-designer-agents` with all resolved parameters.
