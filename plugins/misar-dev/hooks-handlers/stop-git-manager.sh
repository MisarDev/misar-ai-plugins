#!/usr/bin/env bash
# Injects compact git workflow rules after every Claude response so the
# branch/PR/cleanup flow is always in context for the next turn.

cat << 'EOF'
{
  "hookSpecificOutput": {
    "hookEventName": "Stop",
    "additionalContext": "## Git Branch & PR Rules (always active)\n\n- **Branch from `develop`**: `bugfix/<slug>` | `feature/<slug>` | `chore/<slug>`\n- **PR always → `develop`** (NEVER directly to `main`)\n- **After merge**: `git push origin --delete <branch>` + `git branch -d <branch>`\n- **Release flow**: `develop` → `release/vX.Y.Z` → preview deploy → PR to `main` (Forgejo UI only, misaradmin)\n- **After release merge**: delete `release/vX.Y.Z` remote + local\n- **NEVER merge to `main` via API/CLI** — Forgejo UI only by misaradmin\n- **Before push**: `pnpm tsc --noEmit` must pass\n- **Commit format**: `<type>(<scope>): <description>`\n\nFull reference: `/misar-dev:git-manager`"
  }
}
EOF

exit 0
