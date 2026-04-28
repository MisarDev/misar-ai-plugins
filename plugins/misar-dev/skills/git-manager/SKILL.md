---
name: git-manager
description: "Use when doing ANY git work in G1 / Misar AI repos: creating branches, committing, pushing, opening PRs, merging, tagging, cleaning up branches, or sweeping a repo (or all 7 repos) to land everything in develop and ship develop→main. Enforces the canonical workflow defined in CLAUDE.md. Triggers: 'git', 'branch', 'PR', 'pull request', 'merge', 'push', 'commit', 'release', 'tag', 'deploy', 'sweep', 'clean branches', 'sync repos', 'develop to main'."
user-invocable: true
argument-hint: "[step] [branch-type] [slug]"
---

# Git Branch & PR Manager

Single source of truth for all git operations across G1 / Misar AI repos.

## When to Invoke

Invoke **automatically** whenever you are about to:
- Create a branch / commit / push
- Open or merge a pull request
- Cut a release branch
- Tag a release
- Clean up branches after a merge
- **Sweep a repo (or all repos)**: merge feature branches → develop → main, delete merged branches

---

## Repos & Forgejo slugs

| Dir | Forgejo slug |
|-----|-------------|
| MisarBlog | `MisarBlog` |
| MisarDev | `MisarDev` |
| MisarIO | `misar-io` ← hyphen |
| MisarMail | `MisarMail` |
| MisarSocial | `MisarSocial` |
| assisters | `assisters` |
| MisarCoder | `MisarCoder` |

---

## Branch Types

| Work type | Pattern | Example |
|-----------|---------|---------|
| Bug fix | `bugfix/<slug>` | `bugfix/search-tabs-scroll` |
| Feature | `feature/<slug>` | `feature/ai-image-gen` |
| Chore / deps / docs | `chore/<slug>` | `chore/update-deps` |

## Permanent Branches

| Branch | Purpose | Merge mechanism |
|--------|---------|-----------------|
| `main` | Production (Coolify auto-deploys on push) | **CI auto-merge** of `develop → main` PR when all required checks pass |
| `develop` | Integration — all feature PRs land here | Manual merge via API or UI |
| `release/vX.Y.Z` | Release candidate — preview deploy | Push whitelist: misaradmin only; protected, can't be deleted via API |

**Auto-merge is real**: every repo's `.forgejo/workflows/ci.yml` has an `auto-merge` job at the end. When a `develop → main` PR has all required checks green, that job fires and merges automatically. **You do not need to (and cannot via API) force-merge to main** — wait for CI, or fix the failing checks.

---

## 10-step single-feature workflow

```
1. Start from develop
   git checkout develop && git pull origin develop
   git checkout -b bugfix/<slug>

2. Build and commit
   git add <files>                        # NEVER `git add -A` (catches secrets/large files)
   git commit -m "fix(<scope>): <description>"
   pnpm tsc --noEmit                      # must pass before push

3. Push + open PR → develop via Forgejo API
   git push -u origin bugfix/<slug>
   # POST /pulls  head=bugfix/<slug>  base=develop

4. Validate
   pnpm dev + Playwright MCP / DevTools — golden path + edge cases

5. Merge PR into develop (API)
   POST /pulls/<n>/merge  Do=merge

6. Sync local + delete branch (remote + local)
   git checkout develop && git pull origin develop
   git branch -d bugfix/<slug>            # SAFE delete — never -D unless certain
   git push origin --delete bugfix/<slug>

7. Open develop → main PR via Forgejo API
   # CI auto-merge will fire when checks pass

8. (Optional) Cut release branch from develop
   git checkout -b release/vX.Y.Z && git push -u origin release/vX.Y.Z
   # CI auto-deploys preview at https://vXYZ-<product>.preview.misar.io

9. After main merge: pull main + tag
   git pull origin main
   git tag vX.Y.Z && git push origin vX.Y.Z

10. After tag, clean up release branch (Forgejo branch protection blocks
    delete — that's expected; release/* branches stay until manually pruned).
```

---

## Multi-repo sweep workflow

Use this when the user says **"merge all branches into develop and ship to main across all repos"** or similar. Today's lessons learned, codified.

### Phase A — Survey

For each of the 7 repos, in parallel where possible:

```bash
git status --short
git branch --no-color | grep -v -E "^[ *]+(develop|main)$"
git log --oneline @{u}..HEAD                  # unpushed
git log --oneline origin/develop..<branch>    # ahead-of-develop
```

Tabulate: dirty? unpushed? branches ahead? open PRs?

### Phase B — Per-repo sweep (in this order)

For **each non-clean repo**:

1. **Check for an existing open PR** for the branch before creating one:
   ```
   GET /pulls?state=open
   ```
   If one exists, reuse it — don't create a duplicate.

2. **Verify the PR actually has content**:
   ```
   GET /compare/develop...<headSha>      # total_commits > 0?
   ```
   If `total_commits == 0`, the branch is already fully merged — close the PR (`PATCH /pulls/<n> {state:"closed"}`) and delete the branch instead of trying to merge.

3. **Verify CI status**:
   ```
   GET /commits/<headSha>/statuses
   ```
   Required for `main`-targeted PRs. For develop-targeted PRs, develop usually has no required checks — but Forgejo may still 405 the merge until CI completes.

4. **Merge feature → develop**:
   ```
   POST /pulls/<n>/merge {Do:"merge", merge_message_field:"<conventional msg> (#<n>)"}
   ```
   - HTTP 200 = merged
   - HTTP 405 + `"Please try again later"` = transient Forgejo lock OR the PR is a no-op (no commits ahead). Wait 30s and retry once. If still 405, run the `compare` check from step 2 — if 0 commits, close the PR.
   - HTTP 405 + `"Not all required status checks successful"` = CI failure on a `main`-targeted PR. **Do NOT force-merge.** Tell the user which checks failed and link the run.

5. **Delete branch (remote first, then local)**:
   ```
   DELETE /branches/<urlEncodedBranchName>     # remote
   git branch -d <branch>                      # local, safe-delete
   ```
   `release/*` branches are Forgejo-protected; DELETE returns 403 — that's expected, skip.

6. **Sync local develop**:
   ```
   git checkout develop && git pull origin develop
   ```

### Phase C — develop → main per repo

For each repo where `develop != main`:

1. Compare divergence:
   ```
   GET /compare/main...develop      # total_commits > 0?
   ```
2. If develop is ahead, open PR (or reuse open one):
   ```
   POST /pulls {head:"develop", base:"main", title:"release: develop -> main"}
   ```
3. **Walk away.** CI auto-merge will fire when required checks pass. Do not poll-spam the merge API — it just adds Forgejo locks.

---

## Pitfalls — gotchas seen in real sweeps

- **Auto-commit hooks bundle scope creep**. The local auto-commit pre/post hooks may bake unrelated working-tree changes into your feature commit with a junk message like `"l"` or `"aq"`. Always `git log -3 --stat` BEFORE pushing. Fix by `git reset --soft <base>`, restage only the files you mean, recommit with a real conventional message, force-push the feature branch (own branch only).
- **Concurrent git fetches deadlock**. Multiple background hooks can spawn `git fetch` simultaneously, and they queue / hang. Symptoms: `git pull` never returns, `ps` shows several `git fetch` processes from earlier minutes. Don't kill arbitrary git processes — use the Forgejo API instead (it doesn't depend on local git).
- **Forgejo 405 "Please try again later"** has three meanings:
  1. Transient lock (CI just ran) — wait 30s, retry once.
  2. PR is a no-op (already-merged content) — `compare` shows 0 commits — close it.
  3. CI required checks haven't completed yet for develop→main — wait for auto-merge.
  The error message itself doesn't disambiguate; always check `compare` and `statuses` to tell which case applies.
- **Don't bundle unrelated changes into one commit**. If a sweep finds dirty `layout.tsx` in the OAuth feature branch, split into two commits: `feat(oauth): ...` and `chore(layout): ...`. Two commits in one PR is fine; mixing scopes in one commit is not.
- **Local-only branches with unpushed commits**: when you find one, check whether origin/develop already has equivalent content via `git log <branch> ^origin/develop` and `compare` API. If yes, the local commits are duplicates — safe to drop after `git fetch origin develop && git reset --hard origin/develop` (only after verifying!).

---

## Forgejo API quick-reference

```bash
TOKEN="$(security find-generic-password -a "$USER" -s com.misar.forgejo-api-token -w)"
BASE="https://git.misar.io/api/v1/repos/misaradmin/<repo>"

# Open PR (any base)
curl -s -X POST "$BASE/pulls" -H "Authorization: token $TOKEN" -H "Content-Type: application/json" \
  -d '{"title":"...","head":"<branch>","base":"<develop|main>","body":"..."}'

# Find existing open PR for a branch
curl -s "$BASE/pulls?state=open" -H "Authorization: token $TOKEN" \
  | python3 -c "import sys,json;[print(p['number'],p['title']) for p in json.load(sys.stdin) if p.get('head',{}).get('ref')=='<branch>']"

# Merge PR (develop or release/*; main is auto-merged by CI)
curl -s -X POST "$BASE/pulls/<n>/merge" -H "Authorization: token $TOKEN" -H "Content-Type: application/json" \
  -d '{"Do":"merge","merge_message_field":"<conventional msg> (#<n>)"}'

# Compare branches (commits + files)
curl -s "$BASE/compare/<base>...<head>" -H "Authorization: token $TOKEN" \
  | python3 -c "import sys,json;d=json.load(sys.stdin);print('commits:',d.get('total_commits',0),'files:',len(d.get('files',[])))"

# Commit CI statuses
curl -s "$BASE/commits/<sha>/statuses" -H "Authorization: token $TOKEN" \
  | python3 -c "import sys,json;[print(s.get('status'),s.get('context')) for s in json.load(sys.stdin)]"

# Close PR (without merging)
curl -s -X PATCH "$BASE/pulls/<n>" -H "Authorization: token $TOKEN" -H "Content-Type: application/json" \
  -d '{"state":"closed"}'

# Delete remote branch (URL-encode slashes: feature/x → feature%2Fx)
curl -s -X DELETE "$BASE/branches/<urlEncodedBranch>" -H "Authorization: token $TOKEN"
```

---

## Commit Message Format

```
<type>(<scope>): <description>
```

Types: `feat` `fix` `chore` `docs` `style` `refactor` `perf` `test` `ci` `build`

**Never** mention "Claude", "AI", "Anthropic", "Copilot", "GPT", or any LLM in commit messages, PR titles, branch names, or `Co-Authored-By` — commits appear as solely human-authored.

---

## Hard Rules

1. **`develop → main` merges through CI auto-merge only.** Don't try to force-merge via API; if CI fails, fix the failing checks (or have the user fix them) and let CI re-run.
2. **Always delete short-lived branches** (remote + local) after merge.
3. **`release/*` branches are protected** — `DELETE /branches` returns 403. That's expected; skip.
4. **Always run `pnpm tsc --noEmit`** before pushing.
5. **Always start from `develop`** — never branch off `main`.
6. **PRs always target `develop`** (except the release `develop → main` PR).
7. **Use `git branch -d` (safe), not `-D`**. If `-d` refuses, the branch has unmerged work — investigate, don't override.
8. **Never `git add -A` / `git add .`** — explicit file paths only. Auto-commit hooks may add unrelated changes; verify with `git diff --cached` before committing.
9. **For sweeps, prefer Forgejo API over local git.** Local git can deadlock on concurrent fetches; the API is cheap, idempotent, and shows you the actual remote truth.

---

## Usage

```
/misar-dev:git-manager              # full workflow reference
/misar-dev:git-manager start        # guide: create branch from develop
/misar-dev:git-manager pr           # guide: open PR to develop
/misar-dev:git-manager release      # guide: cut release branch + preview
/misar-dev:git-manager cleanup      # guide: delete merged branches
/misar-dev:git-manager sweep        # guide: full multi-repo sweep
/misar-dev:git-manager tag          # guide: tag + delete release branch
```
