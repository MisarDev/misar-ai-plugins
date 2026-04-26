---
name: list-saas-online
description: Submit SaaS products and AI products to 50+ online directories, review platforms, and marketplaces for maximum organic reach. Use when the user wants to list SaaS products online, submit AI products to directories, get SaaS discovered, or mentions "list SaaS", "submit SaaS", "SaaS directories", "AI product listing", "list product online".
user-invocable: true
argument-hint: "[--config listing-config.yaml] [--dry-run] [--platforms future_tools,toptools_ai,...]"
---

# List SaaS Online

Automated SaaS/AI product submission to 50+ online directories ranked by organic reach probability.

## Trigger
- User says "list SaaS online", "submit SaaS to directories", "list my product", "get my SaaS discovered"
- User invokes `/list-saas-online`
- User mentions SaaS directory submissions, AI product listings, software marketplace listings

## Execution Protocol

### Phase 1: Prep
1. Collect product details: name, URL, description (short + long), pricing tiers, category, features, contact info
2. Create tracker: `output/saas-listings-tracker-{date}.md` — columns: Platform | Status | URL | Notes
3. Status values: PENDING / SUBMITTING / SUBMITTED / LIVE / FAILED / SKIPPED / MANUAL

### Phase 2: Submission (per directory)
1. Navigate to submit URL
2. Form type: direct form → fill+submit | OAuth → Google (mryadavgulshan@gmail.com) | CAPTCHA → **MANUAL** | paid → **SKIPPED** | down → **FAILED**
3. Fill all fields completely including pricing tiers and features; submit; verify confirmation; update tracker immediately

### Phase 3: Parallelization
- **Max 4 browser-based parallel agents** — more causes tab conflicts
- CLI/email-based submissions run sequentially first
- Print full MANUAL list at end

## Priority SaaS Directories (Top 15)

| # | Directory | Submit URL | Focus |
|---|-----------|-----------|-------|
| 1 | Product Hunt | producthunt.com/posts/new | All products — high impact, coordinate launch |
| 2 | G2 | g2.com/products/new | B2B SaaS reviews |
| 3 | Capterra | capterra.com/vendors/sign-up | Business software |
| 4 | Software Advice | softwareadvice.com/vendors | Software selection |
| 5 | SaaSHub | saashub.com/services/submit | SaaS comparison |
| 6 | AlternativeTo | alternativeto.net (email signup) | Software alternatives |
| 7 | AppSumo | sell.appsumo.com | Deals / launches |
| 8 | CrunchBase | crunchbase.com/add | Startups / products |
| 9 | SourceForge | sourceforge.net/software/vendors/new | Open source / SaaS |
| 10 | Future Tools | futuretools.io/submit-a-tool | AI tools |
| 11 | BetaList | betalist.com/submit | Early-stage launches |
| 12 | SaaSWorthy | email: business@saasworthy.com | SaaS reviews |
| 13 | Crozdesk | vendor.revleads.com | B2B SaaS |
| 14 | Fazier | fazier.com/submit | SaaS launches (badge required) |
| 15 | Uneed.best | uneed.best/submit | SaaS / tools |

## Error Recovery

| Error | Action |
|-------|--------|
| "Email already registered" | Try login or password reset |
| "URL already submitted" | Mark ALREADY_LISTED, verify |
| Required field missing | Re-read form snapshot, fill |
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
python ~/.claude/scripts/list_saas_auto.py --config listing-config.yaml
python ~/.claude/scripts/list_saas_auto.py --config listing-config.yaml --dry-run
python ~/.claude/scripts/list_saas_auto.py --config listing-config.yaml --platforms "g2,capterra,saashub"
```

Full 50-directory database with per-platform submission steps lives in the tracker file generated each run.
