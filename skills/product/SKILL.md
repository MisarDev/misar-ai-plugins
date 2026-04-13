---
name: product
description: "Use when: product strategy review, feature prioritization, product-market fit analysis, roadmap planning, product design critique, user story review, MVP scoping. Triggers: 'review my product', 'prioritize features', 'is this a good product decision', 'product strategy', 'what should we build next', 'product roadmap', 'feature ideas', 'product audit'."
user-invocable: true
argument-hint: "[agents]"
---

# Product Audit

## When to Invoke

Invoke proactively when the user:
- Discusses product strategy, roadmap, or "what to build next"
- Asks about feature prioritization or MVP scoping
- Wants a product manager or designer perspective on a decision
- Shares a product idea and asks "is this good?", "will users want this?"
- Mentions product-market fit, user research, or competitive analysis
- Is planning a launch, sprint, or quarterly roadmap
- Asks "should we build X or Y?", "what features matter most?"

Launch the **product-agents** agent to analyze product strategy and completeness.

## Usage

```
/misar-dev:product                     # Full product audit
/misar-dev:product pm                  # Product Manager analysis only
/misar-dev:product design              # Product Designer analysis
/misar-dev:product prioritization      # Feature prioritization
```

## Instructions

1. **Parse arguments**:
   - **Agents**: `pm`, `design`, `development`, `prioritization`
   - **Default**: Run all 4 agents

2. **Launch the `product-agents` agent** with parsed parameters

3. **The agent handles everything** — feature discovery, gap analysis, scoring, and reporting.
