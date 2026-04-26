---
name: list-mcp-online
description: Submit MCP (Model Context Protocol) servers to 50+ directories, registries, and marketplaces for maximum discoverability. Use when the user wants to list an MCP server online, publish to MCP registries, get an MCP tool discovered, or mentions "list MCP", "submit MCP server", "MCP registry", "MCP directory", "publish MCP", "MCP marketplace".
user-invocable: true
argument-hint: "[--config listing-config.yaml] [--dry-run] [--platforms smithery,mcp_so,...]"
---

# List MCP Online

Automated MCP server submission to 50+ directories ranked by MCP ecosystem reach + general AI tool visibility.

## Trigger
- User says "list MCP online", "submit MCP server", "publish my MCP", "get my MCP discovered"
- User invokes `/list-mcp-online`
- User mentions MCP registry, MCP marketplace, Smithery, mcp.so, PulseMCP, awesome-mcp-servers

## Execution Protocol

### Phase 1: Prep
1. Collect MCP details: npm/PyPI package name, GitHub repo, tool description, smithery.yaml path, category
2. Create tracker: `output/mcp-listings-tracker-{date}.md` — columns: Platform | Status | URL | Notes
3. Status values: PENDING / SUBMITTING / SUBMITTED / LIVE / FAILED / SKIPPED / MANUAL

### Phase 2: Submission (per directory)
1. Navigate to submit URL
2. Method: direct form → fill+submit | CLI → run command | GitHub PR → open PR | OAuth → Google (mryadavgulshan@gmail.com) | paid → **SKIPPED** | CAPTCHA → **MANUAL**
3. Fill all fields; submit; verify confirmation; update tracker immediately

### Phase 3: Parallelization
- **Max 4 browser-based parallel agents** — more causes tab conflicts
- CLI-based (npm publish, PyPI upload, GitHub API PRs) run sequentially first
- Print full MANUAL list at end

## Priority MCP Directories (Top 15)

| # | Platform | Submit URL | Type | Reach |
|---|----------|-----------|------|-------|
| 1 | Smithery | smithery.ai | MCP registry | PRIMARY — #1 MCP marketplace |
| 2 | MCP.so | mcp.so | MCP directory | 500K+ MCP-focused |
| 3 | Glama.ai/mcp | glama.ai/mcp | MCP explorer | Metrics + listings |
| 4 | PulseMCP | pulsemcp.com | MCP newsletter+DB | Weekly digest |
| 5 | mcpservers.org | mcpservers.org | MCP community | PR-based |
| 6 | mcp-get | mcp-get.com | MCP CLI pkg mgr | Developer install flow |
| 7 | awesome-mcp-servers | github.com/modelcontextprotocol/servers | GitHub PR | Official Anthropic list |
| 8 | npm registry | npmjs.com | Package registry | 15M+ devs |
| 9 | PyPI | pypi.org | Package registry | Python MCP servers |
| 10 | GitHub Topics | github.com | Repo discoverability | Auto-indexed |
| 11 | Cursor Directory | cursor.directory | IDE plugins | 2M+ Cursor users |
| 12 | Continue.dev | continue.dev/extensions | IDE copilot | Open-source IDE |
| 13 | VS Code Marketplace | marketplace.visualstudio.com | IDE extension | 20M+ devs |
| 14 | Open VSX | open-vsx.org | IDE extension | VS Code alt |
| 15 | Cline Community MCPs | github.com/cline/cline | GitHub PR | Cline AI extension |

## Error Recovery

| Error | Action |
|-------|--------|
| "Package name taken" | Add scope (@misar-ai/mcp-name) |
| "Repo already listed" | Mark ALREADY_LISTED, verify |
| Required field missing | Re-read form snapshot, fill |
| CAPTCHA / reCAPTCHA | Mark **MANUAL** (not FAILED) |
| 403 / 429 rate limit | Wait 30s, retry once |
| PR already open | Link existing PR, mark PENDING |
| Paid only | Mark **SKIPPED** (note price) |
| Site down | Mark **FAILED** (down) |

## Contact / Form Defaults

```
Name: Gulshan Yadav | Email: gulshan@promo.misar.io | Company: Misar AI
GitHub: github.com/misar-ai | Twitter: @mrgulshanyadav | Location: India
```

## Automation Script

```bash
python ~/.claude/scripts/list_mcp_auto.py --config listing-config.yaml
python ~/.claude/scripts/list_mcp_auto.py --config listing-config.yaml --dry-run
python ~/.claude/scripts/list_mcp_auto.py --config listing-config.yaml --platforms "smithery,mcp_so,pulsemcp"
```

Full 50-directory database with per-platform submission steps lives in the tracker file generated each run.
