---
allowed-tools: ["Bash", "Read", "Grep"]
description: "Git branch and PR workflow manager for G1 / Misar AI repos. Enforces canonical flow: branch from develop → commit → PR → merge → cleanup → release → preview → develop→main PR (CI auto-merges) → tag → cleanup. Also handles multi-repo sweeps."
argument-hint: "[start|pr|release|cleanup|tag|sweep]"
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
| `sweep` | Multi-repo sweep: merge open feature PRs → develop, delete merged branches, open develop→main PR for each of the 7 G1 / Misar AI repos. **Use Forgejo API only** (local git can deadlock on concurrent fetches). |
| _(none)_ | Show the full workflow reference |

## Secret Scan — Mandatory Pre-Commit/Pre-Push Check

**Before any `git add`, `git commit`, or `git push` operation, run a secret scan. STOP if any finding.**

```bash
# Option 1: Guardian MCP (preferred when available)
guardian_secret_scan --path .

# Option 2: gitleaks
gitleaks protect --staged        # scans staged changes
gitleaks detect --source . --no-git  # scans working tree

# Option 3: staged diff pattern check (fallback)
git diff --cached | grep -iE \
  "(password|secret|token|api.?key|private.?key|access.?key)\s*[=:]\s*[\"']?[A-Za-z0-9_/+\-\.]{16,}"
```

If **any** finding is returned: abort the git operation, remove the secret, move it to a gitignored `.env` file, then re-stage and re-scan.

> Secrets in git history are permanently exposed — even in private repos. Treat any committed credential as compromised and rotate it immediately.

## Instructions

1. **Always run the secret scan pre-check above before any commit or push step.**
2. Parse the argument (if any).
3. Load and follow the `git-manager` skill exactly.
4. For `start`: ask for branch type (bugfix/feature/chore) and slug if not provided; output the exact `git checkout` commands.
5. For `cleanup`: confirm which branch was merged, then output both `git push origin --delete <branch>` and `git branch -d <branch>`.
6. Always remind: **NEVER merge to `main` via API — Forgejo UI only by misaradmin.**
7. Always remind: **Delete branches after merge — remote first, then local.**
