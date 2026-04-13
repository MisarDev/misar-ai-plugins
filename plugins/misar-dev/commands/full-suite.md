---
description: "Full 35-agent orchestrated audit — 4 phases, Observer Agent, batched parallel execution."
argument-hint: "[--phase=1|2|3|4] [--tier=1|2]"
---

Launch the **orchestrator-agents** agent to run the complete 4-phase audit framework with all 35 agents.

1. Parse arguments: phase filter (`--phase=N`), tier filter (`--tier=1` blocking only, `--tier=2` all)
2. Launch `orchestrator-agents` with parsed parameters
3. The orchestrator handles file discovery, 4-phase execution, Observer Agent token management, compaction, batched parallel processing, and master report generation.
