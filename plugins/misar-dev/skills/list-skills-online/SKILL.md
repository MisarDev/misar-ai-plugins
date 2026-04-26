---
name: list-skills-online
description: Submit Claude Code skills, plugins, and slash commands to 30+ directories, registries, and communities for maximum discoverability. Use when the user wants to list a Claude Code skill online, publish a plugin, get a Claude skill discovered, or mentions "list skill", "publish plugin", "Claude Code skill directory", "skill registry", "slash command listing", "Claude plugin marketplace".
user-invocable: true
argument-hint: "[--config listing-config.yaml] [--dry-run] [--platforms misar_plugins,github_topics,...]"
---

# List Skills Online

Automated submission of Claude Code skills, plugins, slash commands, and hooks to 30+ directories ranked by Claude developer community reach.

## Trigger
- User says "list skill online", "publish Claude plugin", "submit skill to directories", "get my Claude skill discovered"
- User invokes `/list-skills-online`
- User mentions Claude Code plugin marketplace, awesome-claude-skills, skill registry, misar-ai-plugins

## Execution Protocol

### Phase 1: Prep
1. Collect skill/plugin details: name, GitHub repo, description, skill type (skill/command/hook/agent), category
2. Create tracker: `output/skills-listings-tracker-{date}.md` — columns: Platform | Status | URL | Notes
3. Status values: PENDING / SUBMITTING / SUBMITTED / LIVE / FAILED / SKIPPED / MANUAL

### Phase 2: Submission (per directory)
1. Navigate to submission page or repository
2. Method: web form → fill | GitHub PR → open PR | community post → draft | CLI → run command | paid → **SKIPPED** | CAPTCHA → **MANUAL**
3. Fill all fields; submit; verify; update tracker immediately

### Phase 3: Parallelization
- GitHub API (PR, topics) run first via CLI/API
- **Max 4 browser-based parallel agents** — more causes tab conflicts
- Print full MANUAL list at end

## Priority Skill Directories (Top 15)

| # | Platform | Submit URL | Type | Reach |
|---|----------|-----------|------|-------|
| 1 | misar-ai-plugins | git.misar.io/misaradmin/misar-ai-plugins | PRIMARY registry | Misar.Dev marketplace |
| 2 | Claude Code Plugin Registry | github.com/anthropics/claude-code | GitHub PR | Official Claude Code |
| 3 | awesome-claude-code-skills | GitHub (search) | GitHub PR | Community awesome-list |
| 4 | GitHub Topics | github.com | Repo topics | claude-skill, claude-code |
| 5 | Claude Discord #showcase | discord.gg/anthropic | Community post | High engagement |
| 6 | Reddit r/ClaudeAI | reddit.com/r/ClaudeAI | Post | 100K+ Claude users |
| 7 | Dev.to (Show DEV) | dev.to/new | Tutorial post | 7M+ devs |
| 8 | Hacker News Show HN | news.ycombinator.com/submit | Community | 10M+ |
| 9 | Hashnode | hashnode.com | Blog post | 5M+ |
| 10 | Reddit r/artificial | reddit.com/r/artificial | Post | 2M+ AI users |
| 11 | Product Hunt | producthunt.com/posts/new | Launch | 10M+ |
| 12 | Peerlist | peerlist.io/user/projects/add-project | Dev network | 300K+ |
| 13 | npm registry | npmjs.com | Package | If packaged |
| 14 | BetaList | betalist.com/submit | Beta launches | 500K+ |
| 15 | Uneed.best | uneed.best/submit | Tool directory | 700K+ |

## Error Recovery

| Error | Action |
|-------|--------|
| PR already open | Link existing PR, mark PENDING |
| "Already listed" | Mark ALREADY_LISTED, verify |
| Required field missing | Re-read form snapshot, fill |
| CAPTCHA / reCAPTCHA | Mark **MANUAL** (not FAILED) |
| GitHub API auth | Re-authenticate with token |
| Paid only | Mark **SKIPPED** (note price) |
| Site down | Mark **FAILED** (down) |

## Contact / Form Defaults

```
Name: Gulshan Yadav | Email: gulshan@promo.misar.io | Company: Misar AI
GitHub: github.com/misar-ai | Twitter: @mrgulshanyadav | Location: India
```

## Automation Script

```bash
python ~/.claude/scripts/list_skills_auto.py --config listing-config.yaml
python ~/.claude/scripts/list_skills_auto.py --config listing-config.yaml --dry-run
python ~/.claude/scripts/list_skills_auto.py --config listing-config.yaml --platforms "misar_plugins,github_topics,devto"
```

Full 30-directory database with per-platform submission steps lives in the tracker file generated each run.
