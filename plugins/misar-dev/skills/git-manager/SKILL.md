---
name: git-manager
description: "Use when doing ANY git work in G1 / Misar AI repos: creating branches, committing, pushing, opening PRs, merging, tagging, or cleaning up branches. Enforces the canonical 10-step branch/PR/merge/cleanup workflow defined in CLAUDE.md. Triggers: 'git', 'branch', 'PR', 'pull request', 'merge', 'push', 'commit', 'release', 'tag', 'deploy'."
user-invocable: true
argument-hint: "[step] [branch-type] [slug]"
---

# Git Branch & PR Manager

## When to Invoke

Invoke **automatically** whenever you are about to:
- Create a branch or checkout
- Make commits and push
- Open or merge a pull request
- Cut a release branch
- Tag a release
- Clean up branches after a merge

This skill is the single source of truth for all git operations in G1 / Misar AI repositories.

---

## Canonical Workflow (10 Steps — follow every time, no exceptions)

### Branch Types

| Work type | Pattern | Example |
|-----------|---------|---------|
| Bug fix | `bugfix/<slug>` | `bugfix/search-tabs-scroll` |
| Feature | `feature/<slug>` | `feature/ai-image-gen` |
| Chore / deps / docs | `chore/<slug>` | `chore/update-deps` |

### Permanent Branches

| Branch | Purpose | Rule |
|--------|---------|------|
| `main` | Production (Coolify deploys on push) | **Forgejo UI only** — misaradmin merges manually. NEVER via API/CLI. |
| `develop` | Integration — all PRs land here | Open to misaradmin |
| `release/vX.Y.Z` | Release candidate — preview deploy | Push whitelist: misaradmin only |

---

### Step-by-Step

```
1. Start from develop
   git checkout develop && git pull origin develop
   git checkout -b bugfix/<slug>     # or feature/ or chore/

2. Build and commit
   git add <files>
   git commit -m "fix(<scope>): <description>"
   pnpm tsc --noEmit                 # must pass before push

3. Push + open PR → develop
   git push -u origin bugfix/<slug>
   # Open PR via Forgejo API: head=bugfix/<slug>, base=develop

4. Validate on develop
   - pnpm dev + Playwright MCP or DevTools mobile/desktop
   - Confirm fix works; confirm no regressions

5. Merge PR into develop (API or UI)
   git push origin --delete bugfix/<slug>   # delete remote branch after merge
   git branch -d bugfix/<slug>              # delete local branch

6. Cut a release branch (when ready to ship)
   git checkout develop && git pull
   git checkout -b release/v1.2.3
   git push -u origin release/v1.2.3
   # → CI auto-deploys preview: https://v123-{product}.preview.misar.io

7. Validate on preview URL
   - Smoke-test the live preview deployment
   - Run E2E against preview domain

8. Open PR: release/v1.2.3 → main  ← FORGEJO UI ONLY
   # Claude/agents MUST NOT merge to main. Open the PR and STOP.

9. misaradmin approves + merges in Forgejo UI
   → Coolify auto-deploys to production

10. Tag the release (optional but recommended)
    git tag v1.2.3 && git push origin v1.2.3
    git push origin --delete release/v1.2.3  # clean up release branch after main merge
    git branch -d release/v1.2.3
```

---

## Forgejo API Quick-Reference

```bash
TOKEN="${FORGEJO_TOKEN}"  # store in ~/.zshrc or macOS Keychain — never hardcode
BASE="https://git.misar.io/api/v1/repos/misaradmin/<repo>"

# Open PR to develop
curl -s -X POST "$BASE/pulls" -H "Authorization: token $TOKEN" -H "Content-Type: application/json" \
  -d '{"title":"...","head":"bugfix/<slug>","base":"develop","body":"..."}'

# Merge PR into develop or release/*
curl -s -X POST "$BASE/pulls/<n>/merge" -H "Authorization: token $TOKEN" -H "Content-Type: application/json" \
  -d '{"Do":"merge","merge_message_field":"..."}'

# Open PR to main (open it, then STOP — misaradmin merges in UI)
curl -s -X POST "$BASE/pulls" -H "Authorization: token $TOKEN" -H "Content-Type: application/json" \
  -d '{"title":"release/vX.Y.Z → main","head":"release/vX.Y.Z","base":"main","body":"..."}'
```

**Repos:** `MisarBlog` · `MisarIO` · `MisarDev` · `MisarMail` · `MisarSocial` · `assisters` · `MisarCoder`

---

## Commit Message Format

```
<type>(<scope>): <description>
```

Types: `feat` `fix` `chore` `docs` `style` `refactor` `perf` `test` `ci` `build`

---

## Hard Rules (never break these)

1. **NEVER push directly to `main`** — Forgejo UI + misaradmin only
2. **NEVER merge to `main` via API/CLI** — open the PR and stop
3. **Always delete short-lived branches** after merge (remote + local)
4. **Always delete release branches** after main merge (remote + local)
5. **Always run `pnpm tsc --noEmit`** before pushing
6. **Always start from `develop`** — never branch off `main`
7. **PRs always target `develop`** (or `release/*` → `develop` for hotfixes)

---

## Usage

```
/misar-dev:git-manager              # Show full workflow reference
/misar-dev:git-manager start        # Guide: create branch from develop
/misar-dev:git-manager pr           # Guide: open PR to develop
/misar-dev:git-manager release      # Guide: cut release branch + preview
/misar-dev:git-manager cleanup      # Guide: delete merged branches
/misar-dev:git-manager tag          # Guide: tag + delete release branch
```
