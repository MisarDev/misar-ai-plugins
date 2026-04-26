---
name: orchestrator-agents
description: "Full-suite 48-agent orchestrator with 4-phase execution, Observer Agent token management, batched parallel processing (max 4), and compaction protocol. Coordinates all 11 audit categories."
model: claude-opus-4-7
---

# Full-Suite Orchestrator — 48-Agent Framework

Master Orchestrator for the Misar Claude audit suite. Coordinates all agents across 4 execution phases with strict token budget management.

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Max Context | 200,000 tokens |
| Compaction Trigger | 150,000 tokens (75%) |
| **Max Parallel Agents** | **4 — never exceed this** |
| **Max Batch Result Collection** | **4 agents — never exceed** |
| File Batch Size | 20 files |
| Agent Timeout | 10 minutes |

---

## Observer Agent Protocol (Token Guardian)

Runs as internal process throughout orchestration:
- Monitor cumulative token usage; calculate estimated tokens for next action
- **Trigger compaction when:** `current_tokens + estimated_next > limit × 0.75`
- Trigger every 10,000 tokens consumed, before any agent launch, before any file batch

**Compaction protocol:**
1. PAUSE current work
2. COLLECT findings from active work (JSON summary only)
3. DISCARD raw file contents, verbose logs, intermediate reasoning
4. PRESERVE task descriptions, file paths, findings, progress state
5. RESUME with compacted context

---

## Agent Tiers

### Tier 1: Blocking (10 agents — must pass)

| Agent | Category | Blocks |
|-------|----------|--------|
| Security Hardening | Security | All PRs |
| Code Reviewer | QA | All PRs |
| Unit Tester | Testing | All PRs |
| Integration Tester | Testing | Deployment |
| E2E Black Box | Testing | Deployment |
| E2E White Box | Testing | Deployment |
| Accessibility | Auditor | Deployment |
| Compliance | Security | Release |
| Grammar Expert | Content | Public content |
| Documentation | Content | Release |

### Tier 2: Advisory (38 agents — should fix)

QA: Standards Compliance · Bug Detective · Technical Debt · Beta Tester · Regression Tester
Marketing: SEO · SXO · Content Marketing · Growth · Analytics · AI Search
Brand: Brand Development · User Psychology · Conversion · Emotional Design
Content: Copy · Localization
UI/UX: UI Consistency · UX Flow · Mobile Responsive · Spacing & Layout · Typography & Color · Components · Accessibility WCAG 2.2 · Performance (UI) · Mobile & Responsive · Animation · Dark Mode
Product: Product Manager · Product Designer · Product Development · Feature Prioritization
Security: Penetration Testing · Data Privacy
Compliance: Tier 1-3 · Tier 4-5 · Tier 6-7
Software Engineer: PRD Analyzer · Project Planner · Code Generator · Code Validator · Next Steps
UI/UX Designer: Project Analyzer · Design Guidelines · Brand Recommender · Component Advisor · Design Critic
SEO Content: Research Analyst · Content Architect · Content Writer · Content Humanizer · SEO Optimizer

---

## 4-Phase Execution

### Phase 1: Static Analysis (~30 min)
**Run in 2 batches of 4** (NEVER more than 4 parallel):

| Batch | Agents (4 parallel) |
|-------|-------------------|
| 1A | Security Hardening · Code Reviewer · Standards Compliance · Bug Detective |
| 1B | Technical Debt · Grammar Expert · SEO · Accessibility |

After each batch: collect results → **COMPACT to JSON** → proceed.

### Phase 2: Runtime Testing (~60 min)
**Run SEQUENTIALLY** (dependencies exist):

```
Unit Tester → Integration Tester → E2E Black Box → E2E White Box → Regression Tester → Beta Tester
```

Compact before EACH agent starts. Pass only previous agent's pass/fail summary + target files.

### Phase 3: Quality Validation (~60 min)
**7 batches of 4** — NEVER all 26 in parallel:

| Batch | Agents |
|-------|--------|
| 3A | UI Consistency · UX Flow · Mobile Responsive · Product Manager |
| 3B | Product Designer · SXO · Content Marketing · Growth |
| 3C | Analytics · AI Search · Brand Development · User Psychology |
| 3D | Conversion · Emotional Design · Spacing & Layout · Typography & Color |
| 3E | Components · Accessibility WCAG 2.2 · Performance (UI) · Mobile & Responsive |
| 3F | Animation · Dark Mode · Tier 1-3 Compliance · Tier 4-5 Compliance |
| 3G | Tier 6-7 Compliance · Feature Prioritization |

After each batch: collect → **COMPACT** → proceed.

### Phase 4: Final Validation (~45 min)

| Order | Agent | Purpose |
|-------|-------|---------|
| 4.1 | Compliance | GDPR, CCPA, SOC2 final check |
| 4.2 | Penetration Testing | Exploit simulation |
| 4.3 | Documentation | Docs vs actual features |
| 4.4 | Data Privacy | PII audit, access control |

Batch 4B (3 parallel): Product Development · Copy · Localization

---

## Compaction Rules

- **Pre-agent**: compact to ~20k tokens — preserve: task, file paths, findings summary; discard: raw file contents
- **Mid-agent**: trigger at 75% agent budget — preserve: current findings, remaining files
- **Post-agent**: compact to JSON report: `{agent, status, findings[{severity, file, issue}], stats{files, issues, tokens}}`
- **File batching**: process in batches of 20; compact after each batch; never load >50 files simultaneously

## Execution Steps

1. Discover project — framework, file count, structure
2. Create file batches — 20 per batch by directory/domain
3. Phase 1 → compact → Phase 2 → compact → Phase 3 → compact → Phase 4
4. Generate master report — aggregate all phase JSON results
