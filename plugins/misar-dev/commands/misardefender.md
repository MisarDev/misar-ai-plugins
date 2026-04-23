---
allowed-tools: ["Bash", "Read"]
description: "MisarDefender local macOS security daemon manager — start, stop, status, scan, logs, dashboard."
argument-hint: "[start|stop|status|scan|logs|dashboard]"
---

# MisarDefender

Manage the MisarDefender local security daemon.

## Argument Parsing

| Arg | Action |
|-----|--------|
| `start` | Start daemon via `python3 scripts/misardefender/defender.py start` |
| `stop` | Stop daemon |
| `status` | Show daemon status |
| `scan` | Run one-shot manual scan |
| `logs` | Show last 20 events from `defender.db` |
| `dashboard` | Open `http://localhost:9876` |
| _(none)_ | Show status + last 5 critical/high events |

## Instructions

1. Load and follow the `misardefender` skill.
2. Run the appropriate `python3 scripts/misardefender/defender.py <cmd>` via Bash.
3. For `logs`: `sqlite3 defender.db "SELECT timestamp,layer,severity,title FROM events ORDER BY timestamp DESC LIMIT 20;"` — format as a table.
4. Always note: daemon runs locally; `defender.db` and `defender.log` are runtime-only files, never to be committed.
