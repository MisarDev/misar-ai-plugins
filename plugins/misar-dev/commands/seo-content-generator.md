---
allowed-tools: ["Bash", "Glob", "Grep", "Read", "Write", "Edit", "Agent"]
description: "AEO/SEO full-stack implementation — technical infrastructure, content generation, and bot crawl health. Run on any Next.js/Nuxt/Astro project to apply the complete AEO/SEO playbook."
argument-hint: "[agents] [--mode=technical|content|audit|full] [--topic=keyword] [--type=blog|guide|comparison|stats|how-to] [--keywords=k1,k2]"
---

# SEO Content Generator

Launch the **seo-content-agents** agent with the full AEO/SEO playbook.

## Defaults (apply silently — never prompt for these)

- `--mode` → `full` (unless `--topic` is provided, then → `content`)

## Interactive Prompting

Before launching, check which flags were supplied. Ask for any that are missing in a **single `AskUserQuestion` call**.

**Mode** (ask if `--mode` not provided and cannot be inferred):

- "Which mode do you want to run?"
- `full` — technical infrastructure fix + content pipeline (default)
- `technical` — infrastructure only: robots.txt, middleware, sitemap, schema, headers
- `content` — 6-agent content pipeline: research → outline → write → humanize → optimize → score
- `audit` — read-only health check, no changes

**Topic** (ask only if `--mode=content` or `--mode=full` and `--topic` not provided):

- "What keyword or topic should the content target? (leave blank to skip content generation)"
- Default: none — skips content agents if blank

## Argument Parsing

1. `--mode=` — execution mode (default: `full`; inferred as `content` if `--topic` given)
2. `--topic=` — target keyword/topic for content generation
3. `--type=` — content type: `blog` | `guide` | `comparison` | `stats` | `how-to` | `tools-list` | `profession`
4. `--keywords=` — comma-separated secondary keywords
5. Remaining words — specific agent names: `research`, `architect`, `write`, `humanize`, `optimize`, `score`, `technical`, `crawlers`, `sitemap`, `schema`

Launch `seo-content-agents` with all resolved parameters.
