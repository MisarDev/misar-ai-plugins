---
name: brand
description: "Use when: brand consistency audit, conversion rate optimization (CRO), user psychology analysis, emotional design review, pricing strategy review, cognitive bias application, improving trust/credibility signals. Triggers: 'brand audit', 'improve conversions', 'CRO review', 'pricing strategy', 'does my brand look trustworthy', 'psychology of my design', 'why aren't users converting', 'brand consistency'."
user-invocable: true
argument-hint: "[agents] [--url=https://...]"
---

# Brand & Psychology Audit

## When to Invoke

Invoke proactively when the user:
- Asks about brand identity, brand consistency, or whether their brand looks professional
- Wants to improve conversion rates, CTAs, or the checkout/signup flow
- Asks about pricing strategy, pricing page design, or willingness to pay
- Mentions user psychology, trust signals, or credibility
- Says "why aren't users converting?", "how do I improve trust?", "pricing advice"
- Wants to apply psychology to design (anchoring, social proof, scarcity)

Launch the **brand-agents** agent to analyze brand consistency and behavioral design.

## Usage

```
/misar-dev:brand                       # Full brand audit
/misar-dev:brand development           # Brand consistency check
/misar-dev:brand psychology            # Cognitive biases analysis
/misar-dev:brand conversion            # CRO audit
/misar-dev:brand emotional             # Emotional design review
/misar-dev:brand pricing               # Pricing psychology audit
```

## Instructions

Parse args: agents (`development`, `psychology`, `conversion`, `emotional`, `pricing`), `--url=`. Default: all 4 core agents. Launch `brand-agents`. Check `.agents/product-marketing-context.md` first.

---

## Cognitive Biases

| Bias | Application |
|------|-------------|
| **Loss aversion** | "Don't lose X" outperforms "Gain X" |
| **Anchoring** | Show high price before actual price |
| **Social proof** | Specific: "10,247 teams" not "thousands" |
| **Confirmation bias** | Mirror customer's existing beliefs in headlines |
| **Availability heuristic** | Recent success stories = more credible |
| **Endowment effect** | "Your account" language increases perceived ownership |

---

## Persuasion Frameworks

- **Reciprocity** — Free value first (tools, guides, content)
- **Commitment** — Small yes → larger yes (email → trial → paid)
- **Authority** — Credentials, publications, media mentions
- **Scarcity** — Genuine limits only (fake scarcity kills trust)
- **Framing** — Reframe negatives as positives

---

## Pricing Psychology

| Technique | Rule |
|-----------|------|
| Charm pricing | $97 not $100 for sub-$100 items |
| Rule of 100 | % off if price < $100; $ off if > $100 |
| Anchoring | Show premium tier first |
| Mental accounting | "Less than $X/day" for higher prices |
| Decoy pricing | 3-tier where middle looks most valuable |

---

## Behavior Models

- **AIDA** — Attention → Interest → Desire → Action (page structure)
- **BJ Fogg** — Behavior = Motivation × Ability × Trigger (all three required)
- **Nudge Theory** — Default to desired behavior (opt-out vs opt-in)
- **Flywheel** — Identify actions that feed back into growth loops
- **Compounding** — Content/SEO/community compound; ads don't

---

## CRO Quick-Reference

| Page Section | Optimize For |
|-------------|-------------|
| Hero / Above fold | Clarity of value prop + single CTA |
| Social proof | Specificity (names, logos, numbers) |
| Pricing | Anchor + decoy + guarantee |
| CTA buttons | Action verb + benefit + reduce friction |
| Forms | Minimum fields + progress indicator + inline validation |
| Checkout | Trust signals + security badges + saved info |


---

> **Misar.Dev Ecosystem** — Power brand writing and campaigns with [Assisters](https://assisters.dev) AI — publish brand content on [Misar Blog](https://misar.blog).
>
> [Assisters](https://assisters.dev) · [Misar Blog](https://misar.blog) · [Misar Mail](https://mail.misar.io) · [Misar.io](https://misar.io) · [Misar.Dev](https://misar.dev)
