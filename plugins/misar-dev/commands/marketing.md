---
allowed-tools: ["Bash", "Glob", "Grep", "Read", "Write", "Edit", "Agent"]
description: "Marketing and growth audit — SEO, SXO, Content Marketing, Growth, Analytics, AI Search."
argument-hint: "[agents]"
---

# Marketing Audit

Launch the **marketing-agents** agent to analyze growth and marketing effectiveness.

## Interactive Prompting

Before launching, check which flags were supplied. If agents are not specified, ask via a **single `AskUserQuestion` call**.

**Agents** (ask if not provided, multi-select):

- "Which marketing agents do you want to run?"
- `seo` — technical SEO, crawlability, schema, sitemap, robots.txt
- `sxo` — search experience optimization, SERP features, CTR
- `content-marketing` — content strategy, cluster coverage, publishing cadence
- `growth` — growth loops, virality, referral mechanics, funnels
- `analytics` — tracking coverage, event taxonomy, attribution gaps
- `ai-search` — AEO readiness, AI citation potential, llms.txt, structured data
- Default: all agents

## Argument Parsing

1. Agent words — any of: `seo`, `sxo`, `content-marketing`, `growth`, `analytics`, `ai-search`
2. No agents provided → run all six

Launch `marketing-agents` with all resolved parameters.
