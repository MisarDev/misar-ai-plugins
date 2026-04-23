---
allowed-tools: ["Bash", "Read", "Grep"]
description: "Git branch and PR workflow manager for G1 / Misar AI repos. Enforces canonical 10-step flow: branch from develop → commit → PR → merge → cleanup → release → preview → PR to main (UI only) → tag → cleanup."
argument-hint: "[start|pr|release|cleanup|tag]"
---

# Git Manager

Invoke the **git-manager** skill to enforce the canonical branch/PR/merge/cleanup workflow.

## Argument Parsing

| Arg | Action |
|-----|--------|
| `start` | Guide user to create the right branch type from `develop` |
| `pr` | Guide opening a PR to `develop` via Forgejo API |
| `release` | Guide cutting `release/vX.Y.Z` from `develop` + preview deploy |
| `cleanup` | Guide deleting merged short-lived or release branches (remote + local) |
| `tag` | Guide tagging the release and cleaning up the release branch |
| _(none)_ | Show the full 10-step workflow reference |

## Instructions

1. Parse the argument (if any).
2. Load and follow the `git-manager` skill exactly.
3. For `start`: ask for branch type (bugfix/feature/chore) and slug if not provided; output the exact `git checkout` commands.
4. For `cleanup`: confirm which branch was merged, then output both `git push origin --delete <branch>` and `git branch -d <branch>`.
5. Always remind: **NEVER merge to `main` via API — Forgejo UI only by misaradmin.**
6. Always remind: **Delete branches after merge — remote first, then local.**
