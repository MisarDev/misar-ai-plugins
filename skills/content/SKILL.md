---
name: content
description: "Use when: reviewing/editing copy or text, grammar check, improving writing quality, localization/i18n audit, documentation review, social media content, copy-editing marketing text, content strategy. Triggers: 'check my copy', 'grammar review', 'improve my writing', 'edit this text', 'documentation audit', 'is this well-written', 'review my content', 'fix the copy', 'i18n check'."
user-invocable: true
argument-hint: "[agents] [--type=marketing|docs|social]"
---

# Content Audit

## When to Invoke

Invoke proactively when the user:
- Asks to review, edit, proofread, or improve existing text/copy
- Shares marketing copy, a landing page, or product description and wants feedback
- Asks about grammar, tone, clarity, or writing quality
- Mentions documentation, README, or technical writing review
- Wants to check localization readiness or i18n coverage
- Says "review my copy", "is this well-written?", "improve this text", "fix the writing"

Launch the **content-agents** agent to analyze language quality and documentation.

## Usage

```
/misar-dev:content                     # Full content audit
/misar-dev:content grammar             # Grammar and spelling
/misar-dev:content copy                # Marketing copy (CTA, headlines, value props)
/misar-dev:content copy-editing        # 7-sweeps quality pass
/misar-dev:content localization        # i18n readiness
/misar-dev:content docs                # Documentation completeness
/misar-dev:content social              # Social media content review
/misar-dev:content strategy            # Content strategy + pillar analysis
```

## Instructions

Parse args: agents (`grammar`, `copy`, `copy-editing`, `localization`, `docs`, `social`, `strategy`), `--type=` (marketing/docs/social/all). Default: all 4 core agents. Launch `content-agents`.

---

## Conversion Copy

- Clarity > cleverness. Benefits > features. Specific > vague ("streamline" needs proof).
- Mirror customer language from reviews/interviews/support.
- Active > passive. Confident > qualified. Show > tell.
- CTA formula: `[Action Verb] + [What They Get] + [Qualifier]`

---

## 7-Sweeps Copy-Editing

Run each independently; verify earlier sweeps intact after each pass.

1. **Clarity** — One idea per sentence; can a 10-year-old understand?
2. **Voice & Tone** — Consistent brand personality throughout
3. **So What** — Every feature connected to a reader benefit
4. **Prove It** — Every claim backed by evidence or specifics
5. **Specificity** — "streamline" → "cuts 3 hours/week"; "many" → "1,200+"
6. **Heightened Emotion** — Appropriate resonance (pain → empathy → relief)
7. **Zero Risk** — Remove all barriers (money-back, free trial, no credit card)

---

## Content Strategy

Check `.agents/product-marketing-context.md` before analysis.

- **Searchable** — existing demand (use-case content, hub-and-spoke, templates)
- **Shareable** — new demand (original data, thought leadership, expert roundups)
- Score: Customer Impact (40%) + Content-Market Fit (30%) + Search Potential (20%) + Resource Cost (10%)

| Pillar | % | Topics |
|--------|---|--------|
| Industry insights | 30% | Trends, data, predictions |
| Behind-the-scenes | 25% | Process, lessons learned |
| Educational | 25% | How-tos, frameworks, tips |
| Personal/Brand | 15% | Stories, values, hot takes |
| Promotional | 5% | Product updates, offers |

---

## Social Content

| Platform | Format | Hook Rule |
|----------|--------|-----------|
| LinkedIn | 3000 chars, carousels | First 2 lines must stand alone |
| Twitter/X | 280 chars, threads | First tweet = headline |
| Instagram | 2200 chars, visual-first | Caption supports visual |
| TikTok | Video description | First 3 seconds hook |

**AI writing red flags:** Em dash overuse · "It's worth noting that" · "Dive into"/"Delve into" · "Robust"/"leverage"/"streamline" without specifics · Passive voice chains · Filler intros ("In today's fast-paced world…")
