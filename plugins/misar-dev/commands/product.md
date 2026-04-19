---
allowed-tools: ["Bash", "Glob", "Grep", "Read", "Write", "Edit", "Agent"]
description: "Product strategy audit — PM, Designer, Development, Prioritization."
argument-hint: "[agents]"
---

# Product Audit

Launch the **product-agents** agent to analyze product strategy and completeness.

## Interactive Prompting

Before launching, check which flags were supplied. If agents are not specified, ask via a **single `AskUserQuestion` call**.

**Agents** (ask if not provided, multi-select):

- "Which product agents do you want to run?"
- `pm` — product-market fit, feature gaps, user stories, roadmap alignment
- `design` — UX flows, onboarding, information architecture
- `development` — technical feasibility, API design, scalability
- `prioritization` — impact vs effort scoring, MoSCoW framework, backlog health
- Default: all agents

## Argument Parsing

1. Agent words — any of: `pm`, `design`, `development`, `prioritization`
2. No agents provided → run all four

Launch `product-agents` with all resolved parameters.
