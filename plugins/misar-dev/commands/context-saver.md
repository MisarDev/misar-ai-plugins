---
allowed-tools: ["Bash", "Glob", "Grep", "Read", "Write", "Edit", "Agent"]
description: "Credit Maximizer v8.2.0 — mandatory MisarCoder-first offload + 3D Router. Reduces Claude credits 75-85% by routing generation/docs/Q&A to free MoE (gemini-2.5-flash/groq)."
argument-hint: "[status|setup|config|reset]"
---

Run the Context Saver Credit Maximizer (v8.2.0).

**Arguments:**
- `status` (default) — Show current routing state, token usage, and MisarCoder availability
- `setup` — Install advanced router scripts to ~/.claude/router/
- `config` — Show routing configuration and offload table
- `reset` — Reset session tracking and model state

**Auto-Enabled:** The mandatory MisarCoder-first protocol + 3D routing is automatically active via SessionStart hook when misar-dev is installed. This command provides manual control and visibility.

**Key feature (v8.2.0):** Before generating ANY output, Claude checks the offload table. Commit messages, PR descriptions, changelogs, README sections, blog posts, email copy, code explanations, and simple Q&A are all routed to MisarCoder (free, gemini-2.5-flash) FIRST. Long-form content (>500w) uses the Assisters API (assisters-chat-v1).
