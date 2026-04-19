---
allowed-tools: ["Bash", "Glob", "Grep", "Read", "Write", "Edit", "Agent"]
description: "Website audit — SEO, Accessibility, Performance, Security, Mobile, Content, Compliance."
argument-hint: "[url] [categories] [--quick|--deep]"
---

# Website Auditor

Launch the **auditor-agents** agent to perform a comprehensive website audit.

## Interactive Prompting

Before launching, check which flags were supplied. Ask for any that are missing in a **single `AskUserQuestion` call**.

**URL** (ask if not provided — required):

- "Which URL do you want to audit?"
- Free-text input (e.g. `https://www.misar.blog`)
- No default — must be provided

**Categories** (ask if not provided, multi-select):

- "Which audit categories do you want to run?"
- `seo` — on-page SEO, meta tags, schema, crawlability
- `accessibility` — WCAG 2.1 AA, contrast, ARIA, keyboard nav
- `performance` — Core Web Vitals, LCP, CLS, FID, asset loading
- `security` — headers, HTTPS, CSP, XSS exposure
- `mobile` — responsive layout, touch targets, viewport
- `content` — copy quality, grammar, readability
- `compliance` — GDPR, cookie consent, privacy policy
- Default: all categories

**Mode** (ask if not provided):

- "Which audit mode?"
- `deep` — full Playwright-powered analysis (default)
- `quick` — HTTP-only, faster, no browser rendering

## Argument Parsing

1. URL — first bare argument starting with `http`
2. Category words — any of: `seo`, `accessibility`, `performance`, `security`, `mobile`, `content`, `compliance`
3. `--quick` / `--deep` — audit depth (default: `deep`)

Launch `auditor-agents` with all resolved parameters.
