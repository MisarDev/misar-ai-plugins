---
description: "3D Router — auto-switches between model (opus/sonnet/haiku) x effort (low/med/high/max) x version (4.5/4.6) based on task complexity and token budget."
argument-hint: "[status|setup|config|reset]"
---

Run the Context Saver 3D router (model x effort x version).

**Arguments:**
- `status` (default) — Show current routing state and token usage
- `setup` — Install advanced router scripts to ~/.claude/router/
- `config` — Show routing configuration and model assignments
- `reset` — Reset session tracking and model state

**Auto-Enabled:** The routing protocol is automatically active via SessionStart hook when the misar-dev plugin is installed. This command provides manual control and visibility.
