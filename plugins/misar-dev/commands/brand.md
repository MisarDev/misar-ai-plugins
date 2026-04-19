---
allowed-tools: ["Bash", "Glob", "Grep", "Read", "Write", "Edit", "Agent"]
description: "Brand and psychology audit — Brand Development, User Psychology, Conversion, Emotional Design."
argument-hint: "[agents]"
---

# Brand Audit

Launch the **brand-agents** agent to analyze brand consistency and behavioral design.

## Interactive Prompting

Before launching, check which flags were supplied. If agents are not specified, ask via a **single `AskUserQuestion` call**.

**Agents** (ask if not provided, multi-select):

- "Which brand agents do you want to run?"
- `development` — brand identity, voice, visual consistency
- `psychology` — user psychology and behavioral design patterns
- `conversion` — CTA effectiveness and conversion design
- `emotional` — emotional design and trust signals
- Default: all agents

## Argument Parsing

1. Agent words — any of: `development`, `psychology`, `conversion`, `emotional`
2. No agents provided → run all four

Launch `brand-agents` with all resolved parameters.
