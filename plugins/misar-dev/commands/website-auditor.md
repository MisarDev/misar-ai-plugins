---
allowed-tools: ["Bash", "Glob", "Grep", "Read", "WebFetch", "Agent"]
description: "Comprehensive website audit — SEO, Accessibility, Performance, Security, Mobile, Content, Compliance. Supports Deep (Playwright), Quick (HTTP), and Source-Only modes."
argument-hint: "[url] [seo|accessibility|performance|security|mobile|content|compliance] [--quick|--deep]"
---

# Website Auditor

Launch the **website-auditor-agents** agent for a comprehensive website audit.

## Interactive Prompting

Before launching, check which flags were supplied. Ask for any missing in a **single `AskUserQuestion` call**.

**Target** (ask if not provided):
- "What should I audit? Provide a URL or say 'codebase' to scan the current project."
- Default: current codebase

**Categories** (optional — ask if unclear):
- `seo` · `accessibility` · `performance` · `security` · `mobile` · `content` · `compliance`
- Default: all categories

**Mode** (optional):
- `--deep` — Playwright browser-based (requires Playwright MCP)
- `--quick` — HTTP-only via WebFetch
- Default: auto-detect (deep if Playwright available + URL given)

## Argument Parsing

1. First positional arg that starts with `http` → URL target
2. Category words from the valid list → selected categories
3. `--deep` / `--quick` → mode override
4. No categories → run all

## Instructions

1. Run `scripts/detect-framework.sh` via Bash to detect framework
2. Launch `website-auditor-agents` with all resolved parameters
3. Report includes: overall score (0-100), grade (A-F), per-category scores, top priorities, JSON output
