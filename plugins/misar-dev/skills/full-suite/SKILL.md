---
name: full-suite
description: "Run all 35 agents across 8 categories in 4 phases — complete codebase audit with orchestration, Observer Agent, and token management."
user-invocable: true
argument-hint: "[--phase=1|2|3|4] [--tier=1|2]"
---

# Full Suite — 35-Agent Orchestrated Audit

Launch the **orchestrator-agents** agent to run the complete 4-phase audit framework.

## Usage

```
/misar-dev:full-suite                  # Run all 35 agents, all 4 phases
/misar-dev:full-suite --phase=1        # Phase 1 only (Static Analysis)
/misar-dev:full-suite --phase=2        # Phase 2 only (Runtime Testing)
/misar-dev:full-suite --tier=1         # Blocking agents only (10 agents)
```

## Phases

| Phase | Name | Agents | Execution |
|-------|------|--------|-----------|
| 1 | Static Analysis | 8 | Parallel (2 batches of 4) |
| 2 | Runtime Testing | 6 | Sequential (dependency chain) |
| 3 | Quality Validation | 12 | Parallel (3 batches of 4) |
| 4 | Final Validation | 4 | Sequential |

## Instructions

1. **Parse arguments**:
   - **Phase filter**: `--phase=N` runs only that phase
   - **Tier filter**: `--tier=1` runs only blocking agents, `--tier=2` includes advisory
   - **Default**: Run everything

2. **Launch the `orchestrator-agents` agent** with parsed parameters

3. **The orchestrator handles everything** — file discovery, 4-phase execution, Observer Agent token management, compaction, batched parallel processing, and master report generation.

## Token Budget

| Phase | Budget/Agent | Max Parallel |
|-------|-------------|-------------|
| 1 | 80k | 4 |
| 2 | 100k | 1 (sequential) |
| 3 | 60k | 4 |
| 4 | 100k | 1 (sequential) |
