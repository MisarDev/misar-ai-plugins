---
name: list-tools-online
description: Submit tools to 50+ online directories, marketplaces, and listing platforms for maximum organic reach. Use when the user wants to list tools online, submit tools to directories, get tools discovered, or mentions "list tools", "submit tool", "tool directories", "tool listing". Handles form discovery, filling, submission, error handling, and verification.
user-invocable: true
argument-hint: "[--config listing-config.yaml] [--dry-run] [--platforms future_tools,toptools_ai,...]"
---

# List Tools Online

Automated tool submission to 50+ online directories. Discovers forms, fills them, handles errors, verifies listings.

## Trigger
- User says "list tools online", "submit tool to directories", "list my tools", "get my tools discovered"
- User invokes `/list-tools-online`
- User mentions tool directory submissions or marketplace listings

## Execution Protocol

### Phase 1: Prep
1. Collect tool details: name, URL, description (short + long), category, pricing, contact info
2. Create tracker: `output/tool-listings-tracker-{date}.md` — columns: Platform | Status | URL | Notes
3. Status values: PENDING / SUBMITTING / SUBMITTED / LIVE / FAILED / SKIPPED / MANUAL

### Phase 2: Submission (per directory)
1. Navigate to submit URL
2. Form type: direct form → fill+submit | OAuth → Google (mryadavgulshan@gmail.com) | CAPTCHA → **MANUAL** | paid → **SKIPPED** | down → **FAILED**
3. Fill all fields completely; submit; verify confirmation message; update tracker immediately

### Phase 3: Parallelization
- **Max 4 browser-based parallel agents** — more causes tab conflicts and session cookie errors
- CLI/API-based submissions run sequentially before browser submissions
- Print full MANUAL list at end with exact instructions per platform

## Priority Tool Directories (Top 15)

| # | Directory | Submit URL | Status (tools.misar.io) |
|---|-----------|-----------|------------------------|
| 1 | Product Hunt | producthunt.com/posts/new | ⏳ DEFERRED (launch strategy needed) |
| 2 | Reddit (r/artificial, r/SideProject) | reddit.com/submit | ✅ LIVE |
| 3 | G2 | g2.com/products/new | 🔧 MANUAL (Google login) |
| 4 | Dev.to (Show DEV) | dev.to/new | ✅ LIVE |
| 5 | Capterra | digitalmarkets.gartner.com/get-listed/start | 🔧 MANUAL (click Continue) |
| 6 | AlternativeTo | alternativeto.net (email signup) | 🔧 MANUAL (Cloudflare blocks) |
| 7 | AppSumo Marketplace | sell.appsumo.com | ✅ SUBMITTED |
| 8 | CrunchBase | crunchbase.com/add-new | 🔧 MANUAL (Google connect errored) |
| 9 | SourceForge | sourceforge.net/software/vendors/new | 🔧 MANUAL (reCAPTCHA) |
| 10 | Hacker News (Show HN) | news.ycombinator.com/submit | ⏳ DEFERRED (karma ≥10 required) |
| 11 | SaaSHub | saashub.com/services/submit | 🔧 MANUAL (password reset in Mailcow) |
| 12 | Software Advice | softwareadvice.com/vendors | ✅ SUBMITTED |
| 13 | Future Tools | futuretools.io/submit-a-tool | ✅ SUBMITTED |
| 14 | TopTools.AI | toptools.ai/submit | ✅ SUBMITTED |
| 15 | LaunchingNext | launchingnext.com/submit | ✅ SUBMITTED #129501 |

## Error Recovery

| Error | Action |
|-------|--------|
| "Email already registered" | Try login or password reset |
| "URL already submitted" | Mark ALREADY_LISTED, verify |
| Required field missing | Re-read form snapshot, fill missing field |
| CAPTCHA / reCAPTCHA | Mark **MANUAL** (not FAILED) |
| 403 / 429 rate limit | Wait 30s, retry once |
| 500 server error | Retry once, then FAILED |
| Paid only | Mark **SKIPPED** (note price) |
| Site down / DNS dead | Mark **FAILED** (down) |

## Contact / Form Defaults

```
Name: Gulshan Yadav | Email: gulshan@promo.misar.io | Company: Misar AI
Title: Founder | Twitter: @mrgulshanyadav | Location: India | Founded: 2024
```

## Automation Script

```bash
python ~/.claude/scripts/list_tools_auto.py --config listing-config.yaml
python ~/.claude/scripts/list_tools_auto.py --config listing-config.yaml --dry-run
python ~/.claude/scripts/list_tools_auto.py --config listing-config.yaml --platforms "future_tools,toptools_ai"
```

Full 50-directory database with per-platform steps and status history lives in the tracker file generated each run.
