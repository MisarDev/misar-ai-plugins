---
name: marketing
description: "Use when: SEO audit, reviewing landing pages, writing marketing copy, content strategy, social media content, CRO/conversion optimization, growth hacking, programmatic SEO, analytics check, AI search optimization, marketing effectiveness. Triggers: 'improve SEO', 'write landing page copy', 'content strategy', 'get more traffic', 'social media strategy', 'marketing audit', 'improve conversions', 'why isn't my site ranking', 'write a headline', 'CTA ideas'."
user-invocable: true
argument-hint: "[agents] [--url=https://...] [--stage=early|growth|scale]"
---

# Marketing Audit

## When to Invoke

Invoke proactively when the user:
- Mentions SEO, ranking, traffic, keywords, backlinks, or Google Search Console
- Wants to improve a landing page, homepage, or product page
- Asks about marketing copy, headlines, CTAs, or value propositions
- Mentions content strategy, blog, social media, or growth
- Asks "why isn't my site ranking?", "how do I get more traffic?", "improve my conversion rate"
- Wants programmatic SEO, AI search optimization, or content at scale

Launch the **marketing-agents** agent to analyze growth and marketing effectiveness.

## Usage

```
/misar-dev:marketing                    # Full 6-agent audit
/misar-dev:marketing seo               # Technical + on-page + E-E-A-T
/misar-dev:marketing sxo               # CWV + E-E-A-T
/misar-dev:marketing growth            # Growth + conversion audit
/misar-dev:marketing analytics         # Analytics implementation
/misar-dev:marketing content-marketing # Content strategy + copywriting
/misar-dev:marketing ai-search         # llms.txt, AEO, GEO
/misar-dev:marketing copywriting       # CTA, headlines, value props
/misar-dev:marketing copy-editing      # 7-sweeps quality pass
/misar-dev:marketing programmatic-seo  # 12-playbook analysis
/misar-dev:marketing social-content    # Platform content strategy
/misar-dev:marketing ideas             # 139-idea brainstorm by stage
/misar-dev:marketing --stage=early     # Stage-appropriate recommendations
```

## Instructions

Parse args: agents (`seo`, `sxo`, `content-marketing`, `growth`, `analytics`, `ai-search`, `copywriting`, `copy-editing`, `programmatic-seo`, `social-content`, `ideas`), `--url=`, `--stage=` (early/growth/scale). Default: all 6 core agents. Launch `marketing-agents`.

---

## SEO Audit (Priority Order)

Check `.agents/product-marketing-context.md` first if present.

1. **Crawlability** — robots.txt, XML sitemap, ≤3-click architecture, index status
2. **Technical** — LCP < 2.5s, INP < 200ms, CLS < 0.1, HTTPS, mobile-first
3. **On-Page** — unique titles (50-60 chars), meta (150-160 chars), one H1, keyword in first 100 words
4. **Content** — E-E-A-T: Experience (first-hand), Expertise (accurate detail), Authority (cited), Trust (HTTPS, contact, privacy)
5. **Authority** — internal linking, descriptive anchors, no orphan pages

**Warning:** `web_fetch` strips `<script>` — can't detect JS-injected JSON-LD. Use browser/Rich Results Test for schema.

---

## Conversion Copy

- Clarity > cleverness. Benefits > features. Specific > vague (never "streamline"/"optimize" without proof).
- Mirror customer language from reviews/interviews/support.
- CTA formula: `[Action Verb] + [What They Get] + [Qualifier]`

| Weak | Strong |
|------|--------|
| Submit | Start Free Trial |
| Sign Up | Get [Specific Thing] |
| Learn More | See [Product] in Action |

**7 Sweeps:** Clarity → Voice & Tone → So What → Prove It → Specificity → Heightened Emotion → Zero Risk. Run independently; verify previous sweeps intact after each.

---

## Content Strategy

- **Searchable** — targets existing demand (use-case, hub-and-spoke, templates)
- **Shareable** — creates new demand (original data, thought leadership, expert roundups)
- Score: Customer Impact (40%) + Content-Market Fit (30%) + Search Potential (20%) + Resource Cost (10%)

---

## Programmatic SEO (12 Playbooks)

Every page must provide value specific to that page — not just variable substitution.
Data: Proprietary > Product-derived > UGC > Licensed > Public. URL rule: subfolders not subdomains.

Playbooks: Templates · Curation · Conversions · Comparisons · Examples · Locations · Personas · Integrations · Glossary · Translations · Directories · Profiles

5 phases: Keyword pattern research → Data requirements → Template design → Internal linking → Indexation strategy.

---

## Social Content

| Platform | Format | Frequency | Hook Rule |
|----------|--------|-----------|-----------|
| LinkedIn | Carousels, text | 3-5x/week | First 2 lines stand alone |
| Twitter/X | Threads | 3-10x/day | First tweet = headline |
| Instagram | Reels, carousels | 1-2/day | Caption supports visual |
| TikTok | Video | 1-4x/day | First 3 seconds hook |

Hook formulas: Curiosity ("I was wrong about X") · Story ("Last week, X happened") · Value ("How to Y without Z") · Contrarian ("Unpopular opinion: X")

---

## Psychology

**Biases:** Loss aversion ("Don't lose X" > "Gain X") · Anchoring (high price first) · Social proof (specific: "10,247 teams") · Commitment (small yes → bigger yes)

**Pricing:** Charm ($97 not $100) · Rule of 100 (% off if < $100; $ off if > $100) · Reframe as daily cost

**Ideas by stage:** Early → Content/SEO, community, founder-led, free tools. Growth → Paid, partnerships, referral, PLG. Scale → Brand campaigns, international, analyst relations.
