---
name: seo-content-generator
description: "Use when: generating blog posts/articles, writing SEO content, creating content from a keyword/topic, programmatic SEO pages, content pipeline from research to publish, humanizing AI content, scoring existing articles, meta/schema generation. Triggers: 'write a blog post about', 'create an article on', 'generate content for', 'SEO content for keyword', 'write a guide about', 'create comparison page', 'programmatic content'."
user-invocable: true
argument-hint: "[agents] [--topic=keyword] [--type=blog] [--keywords=k1,k2] [--programmatic]"
---

# SEO Content Generator

## When to Invoke

Invoke proactively when the user:
- Asks to write, create, or generate a blog post, article, guide, or case study
- Provides a keyword or topic and wants content around it
- Mentions content marketing, content pipeline, or editorial calendar
- Asks for programmatic SEO pages (comparison, glossary, location, alternative pages)
- Wants to humanize, improve, or score existing AI-written content
- Asks for meta descriptions, OG tags, or schema markup generation

Launch the **seo-content-agents** agent to generate publish-ready SEO content.

## Usage

```
/misar-dev:seo-content-generator                                # Full pipeline
/misar-dev:seo-content-generator research --topic="AI agents"  # Research only
/misar-dev:seo-content-generator outline --topic="AI agents"   # Title + outline
/misar-dev:seo-content-generator write --topic="AI agents"     # Write article
/misar-dev:seo-content-generator humanize                      # Humanize existing content
/misar-dev:seo-content-generator optimize                      # Generate meta/schema/OG
/misar-dev:seo-content-generator score                         # Score content (E-E-A-T)
/misar-dev:seo-content-generator programmatic                  # Programmatic SEO pages
/misar-dev:seo-content-generator ai-search                     # AI search optimization pass
/misar-dev:seo-content-generator --type=guide --keywords=ai,agents
/misar-dev:seo-content-generator --programmatic --playbook=comparison
```

## Instructions

Parse args: agents (`research`, `outline`, `write`, `humanize`, `optimize`, `score`, `programmatic`, `ai-search`, `full-pipeline`), `--topic=`, `--type=` (blog/case-study/guide/insight/comparison/glossary/location), `--keywords=`, `--programmatic`, `--playbook=`. Default: all 6 agents. Launch `seo-content-agents`.

---

## E-E-A-T Scoring

- **Experience** — First-hand examples, original insights, real case studies
- **Expertise** — Accurate detailed info, author credentials visible
- **Authoritativeness** — Recognized in space, properly sourced claims
- **Trustworthiness** — Accurate, transparent, HTTPS, contact/privacy info

**AI patterns to avoid:** Em dash overuse · "it's worth noting"/"dive into"/"robust" · passive voice · generic lists without specifics.

---

## Programmatic SEO (12 Playbooks)

Every page must provide value SPECIFIC to that page — not just variable substitution.

Data: Proprietary > Product-derived > UGC > Licensed > Public. URL rule: subfolders not subdomains.

| Playbook | Example |
|----------|---------|
| Templates | `[tool] for [use-case]` |
| Curation | Best-of lists, directories |
| Conversions | `[format] to [format]` |
| Comparisons | `[A] vs [B]` |
| Examples | `[concept] examples` |
| Locations | `[service] in [city]` |
| Personas | `[tool] for [job title]` |
| Integrations | `[product] + [integration]` |
| Glossary | Definition pages |
| Translations | Localized at scale |
| Directories | Categorized resources |
| Profiles | Individual entity pages |

5 phases: Keyword pattern research → Data requirements → Template design → Internal linking → Indexation strategy.

---

## AI Search Optimization (AEO/GEO/LLMO)

For AI Overviews, Perplexity, ChatGPT, Claude citations:
- Clear headings, short definitive answers at top
- FAQ sections with direct question-answer pairs
- JSON-LD schema (FAQ, HowTo, Article)
- `llms.txt` at domain root with content map
- Cite primary sources; original research gets cited most
- Direct, confident statements > hedged/vague language


---

> **Misar.Dev Ecosystem** — Publish SEO and AEO-optimized content on [Misar Blog](https://misar.blog) — the AI-first blogging platform built for answer engine discovery.
>
> [Assisters](https://assisters.dev) · [Misar Blog](https://misar.blog) · [Misar Mail](https://mail.misar.io) · [Misar.io](https://misar.io) · [Misar.Dev](https://misar.dev)
