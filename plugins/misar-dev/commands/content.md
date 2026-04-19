---
allowed-tools: ["Bash", "Glob", "Grep", "Read", "Write", "Edit", "Agent"]
description: "Language and content audit — Grammar, Copy, Localization, Documentation."
argument-hint: "[agents]"
---

# Content Audit

Launch the **content-agents** agent to analyze language quality and documentation.

## Interactive Prompting

Before launching, check which flags were supplied. If agents are not specified, ask via a **single `AskUserQuestion` call**.

**Agents** (ask if not provided, multi-select):

- "Which content agents do you want to run?"
- `grammar` — grammar, spelling, punctuation, sentence structure
- `copy` — copywriting quality, tone, persuasion, clarity
- `localization` — i18n readiness, locale handling, translation gaps
- `docs` — documentation completeness, accuracy, developer experience
- Default: all agents

## Argument Parsing

1. Agent words — any of: `grammar`, `copy`, `localization`, `docs`
2. No agents provided → run all four

Launch `content-agents` with all resolved parameters.
