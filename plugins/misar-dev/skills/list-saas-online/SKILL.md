---
name: list-saas-online
description: Submit SaaS products and AI products to 50+ online directories, review platforms, and marketplaces for maximum organic reach. Use when the user wants to list SaaS products online, submit AI products to directories, get SaaS discovered, or mentions "list SaaS", "submit SaaS", "SaaS directories", "AI product listing", "list product online".
user-invocable: true
argument-hint: "[--config listing-config.yaml] [--dry-run] [--platforms future_tools,toptools_ai,...]"
---

# List SaaS Online

Automated SaaS/AI product submission to 50+ online directories ranked by organic reach probability. Discovers submission forms, fills them, handles errors, and verifies listings go live.

## When to Trigger

- User says "list SaaS online", "submit SaaS to directories", "list my product", "get my SaaS discovered"
- User invokes `/list-saas-online`
- User mentions SaaS directory submissions, AI product listings, software marketplace listings

## Execution Protocol

### Phase 1: Preparation

1. Read product details from user input or project context (URL, name, description, pricing tiers, category, features, contact info)
2. Create a tracking file at `Work/output/saas-listings-tracker-{date}.md` with all 50 directories as a checklist
3. Each entry tracks: Platform | Status (PENDING/SUBMITTING/SUBMITTED/LIVE/FAILED/SKIPPED) | URL | Notes

### Phase 2: Submission (Per Directory)

For EACH directory in the ranked list below:

1. **Navigate** to the directory's submission/add page
2. **Detect** the form type:
   - Direct form (best) -> fill and submit
   - OAuth-required -> mark SKIPPED with reason
   - Paid-only -> mark SKIPPED with reason
   - Broken/down -> mark FAILED with reason
3. **Fill the form** completely:
   - Use `browser_snapshot` to get all form fields
   - Use `browser_type` / `browser_click` / `browser_select_option` / `browser_fill_form` for each field
   - Match categories/tags to closest available options
   - Include pricing tiers, features, integrations where supported
4. **Submit** the form
5. **Handle errors** (same protocol as list-tools-online)
6. **Verify** listing if instant

### Phase 3: Update Tracker

After each submission attempt, immediately update the tracker file.

## Top 50 SaaS/AI Product Directories (Ranked by Organic Reach)

| Rank | Directory | Submit URL | Type | Focus |
|------|-----------|-----------|------|-------|
| 1 | Product Hunt | producthunt.com/posts/new | Launch platform | All products |
| 2 | G2 | g2.com/products/new | Reviews | B2B SaaS |
| 3 | Capterra | capterra.com/vendors/sign-up | Reviews | Business software |
| 4 | Software Advice | softwareadvice.com/vendors | Reviews | Software selection |
| 5 | SaaSHub | saashub.com/services/submit | Comparison | SaaS comparison |
| 6 | AlternativeTo | alternativeto.net (email signup) | Alternatives | Software alternatives |
| 7 | AppSumo | appsumo.com/partners | Marketplace | Deals/launches |
| 8 | CrunchBase | crunchbase.com/add | Company DB | Startups/products |
| 9 | SourceForge | sourceforge.net/software/vendors/new | Directory | Open source/SaaS |
| 10 | ToolPilot.ai | toolpilot.ai (JotForm) | AI directory | AI tools |
| 11 | Future Tools | futuretools.io/submit-a-tool | AI directory | AI tools |
| 12 | BetaList | betalist.com/submit | Beta launches | Early-stage |
| 13 | SaaSWorthy | saasworthy.com (email to business@) | Reviews | SaaS reviews |
| 14 | Crozdesk | crozdesk.com/vendor | Directory | B2B SaaS |
| 15 | Fazier | fazier.com/submit (free: badge + 3 comments) | Launch platform | SaaS launches |
| 16 | Uneed.best | uneed.best/submit | Tool directory | SaaS/tools |
| 17 | LaunchingNext | launchingnext.com/submit | Launch dir | New products |
| 18 | Startup Ranking | startupranking.com/startup/create/url-validation | Rankings | Startup metrics |
| 19 | Indie Hackers | indiehackers.com/products | Products | Indie SaaS |
| 20 | Hacker News (Show HN) | news.ycombinator.com/submit | Community | Tech products |
| 21 | Reddit (relevant subs) | reddit.com/submit | Community | Tech products |
| 22 | SaaSGenius | saasgenius.com (email to contact@) | Reviews | SaaS comparison |
| 23 | Launching.io | launching.io/submit (→ launchingnext) | Launch platform | New products |
| 24 | NachoNacho | nachonacho.com/vendor | SaaS marketplace | B2B SaaS |
| 25 | Software Suggest | softwaresuggest.com/vendors | Reviews | India-focused |
| 26 | WebAppRater | webapprater.com/submit | Web app reviews | Web apps |
| 27 | SaaS Mag | saasmag.com/submit | SaaS publication | SaaS news |
| 28 | Peerspot | peerspot.com/vendor | Enterprise reviews | Enterprise SaaS |
| 29 | Dev.to (Show DEV) | dev.to/new | Developer community | 7M+ traffic |
| 30 | F6S | f6s.com (add company) | Startup platform | 500K+ traffic |
| 31 | Feedough | feedough.com/submit-your-startup | Startup directory | 800K+ traffic |
| 32 | AIxploria | aixploria.com/en (submit) | AI directory | 500K+ traffic |
| 33 | OpenTools | opentools.ai (submit) | AI directory | 400K+ traffic |
| 34 | Dang.ai | dang.ai (submit) | AI directory | 300K+ traffic |
| 35 | Peerlist Launchpad | peerlist.io/user/projects/add-project | Dev network | 300K+ traffic |
| 36 | Supertools (Rundown) | supertools.therundown.ai/submit | AI directory | 250K+ traffic |
| 37 | ListMyAI | listmyai.net/submit-ai-tools | AI directory | 200K+ traffic |
| 38 | Easy With AI | easywithai.com/submit-tool | AI directory | 200K+ traffic |
| 39 | Insidr.ai | insidr.ai/submit-tools | AI directory | 150K+ traffic |
| 40 | AI Tool Hunt | aitoolhunt.com/submit | AI directory | 150K+ traffic |
| 41 | PoweredbyAI | poweredbyai.app (submit) | AI directory | 120K+ traffic |
| 42 | TopStartups.io | topstartups.io (submit) | Startup directory | 100K+ traffic |
| 43 | AI Scout | aiscout.net (submit) | AI directory | 100K+ traffic |
| 44 | SaaSAITools | saasaitools.com (submit) | AI/SaaS directory | 80K+ traffic |
| 45 | Startupresources.io | startupresources.io (submit) | Startup tool dir | 80K+ traffic |
| 46 | ToolScout | toolscout.ai/submit | AI directory | 80K+ traffic |
| 47 | There's An AI For That | theresanaiforthat.com/submit (free+backlink) | AI directory | 2M+ traffic |
| 48 | Tool0 | tool0.org (submit) | AI directory | 60K+ traffic |
| 49 | Launch AI | launchai.app (submit) | AI launch dir | 50K+ traffic |
| 50 | Product Directory | productdirectory.io/submit | Product directory | 50K+ traffic |

NOTE: The following directories were confirmed paid-only or defunct (2026-03) and excluded:
- Futurepedia ($247+ min), Toolify.ai ($99), TopAI.tools (paid), TAAFT ($97 or backlink)
- DevHunt ($49 launch week), Microlaunch (paid Pro Launch only)
- GoodFirms ($1500+/yr, agency-focused), GetApp (Gartner paid lead-gen plan)
- TrustRadius (auth system broken), Ben's Bites (redirects to AppSumo)
- AI Tool Guru (site down), Slant (500 error), StackShare (500 + OAuth-only)
- MakerLog (defunct → ambitiousfounder.com), StartupLift (SSL error, down)
- KillerStartups (newsletter only, no form), Startup Stash (404)
- BetaPage/PitchWall (OAuth-only), StartupBase (signups closed)
- All Top Startups (paid, no free tier), Tech Pluto (→ Fazier)
- SnapMunk (unsafe/blocked), SideProjectors (marketplace, not SaaS directory)

## Form Field Mapping (SaaS-specific)

| Common Field | Source |
|-------------|--------|
| Product Name | User-provided product name |
| URL/Website | User-provided URL |
| Tagline | One-line value prop (max 80 chars) |
| Description (short) | First 160 chars |
| Description (long) | Full product description with features |
| Category | Best match: AI, Productivity, Marketing, Sales, Dev Tools, etc. |
| Pricing Model | Free / Freemium / Subscription / One-time |
| Pricing Tiers | List tiers (Free, Pro $X/mo, Enterprise) |
| Features | Bullet list of key features |
| Integrations | List of integrations |
| Platform | Web, iOS, Android, Desktop |
| Email | Contact email |
| Twitter/X | User's handle |
| Logo | Upload if available |
| Screenshots | Upload if available |

## Error Recovery Patterns

Same as list-tools-online skill.

## Contact Info Template

```
Name: Gulshan Yadav
Email: gulshan@promo.misar.io
Company: Misar AI
Title: Founder
Twitter: @mrgulshanyadav
LinkedIn: linkedin.com/in/mrgulshanyadav
Website: [product URL provided by user]
Location: India
Founded: 2024
```

---

## Automation Scripts (Python + Playwright)

### Prerequisites
```bash
pip install playwright pyyaml
playwright install chromium
```

### Run Instructions
```bash
# 1. Save listing_base.py (from list-mcp-online skill) to ~/.claude/scripts/listing_base.py
# 2. Save the script block below to ~/.claude/scripts/list_saas_auto.py
# 3. Create listing-config.yaml with your SaaS product details
python ~/.claude/scripts/list_saas_auto.py --config listing-config.yaml
python ~/.claude/scripts/list_saas_auto.py --config listing-config.yaml --dry-run
python ~/.claude/scripts/list_saas_auto.py --config listing-config.yaml --platforms "future_tools,toptools_ai,saashub,launchingnext"
```

### Block — SaaS Platform Scripts (save as `~/.claude/scripts/list_saas_auto.py`)

```python
#!/usr/bin/env python3
"""
SaaS / AI Product Listing Automation — top automatable directories
Usage: python list_saas_auto.py --config listing-config.yaml [--dry-run] [--platforms p1,p2]
Requires: pip install playwright pyyaml && playwright install chromium
Also requires: listing_base.py in ~/.claude/scripts/ (from list-mcp-online skill)
"""
import asyncio, sys, argparse
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright, Page

sys.path.insert(0, str(Path.home() / ".claude/scripts"))
from listing_base import ListingConfig, SubmissionTracker, load_config, run_batch


async def submit_future_tools(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """futuretools.io — 7-field form, no login"""
    p = "Future Tools"
    tracker.update(p, "PENDING")
    try:
        await page.goto("https://www.futuretools.io/submit-a-tool", wait_until="domcontentloaded", timeout=20000)
        await page.locator('input').nth(0).fill(cfg.contact_name)
        await page.locator('input').nth(1).fill(cfg.name)
        await page.locator('input[type="url"], input').nth(2).fill(cfg.url)
        await page.locator('textarea').first.fill(cfg.description_short)
        free_btn = page.locator('label:has-text("Free"), input[value="Free"]').first
        if await free_btn.count() > 0:
            await free_btn.click()
        await page.locator('input[type="email"]').fill(cfg.contact_email)
        await page.locator('button[type="submit"]').click()
        await page.wait_for_selector('text=/review|thank|submit/i', timeout=15000)
        tracker.update(p, "SUBMITTED", "https://www.futuretools.io")
    except Exception as e:
        tracker.update(p, "FAILED", notes=str(e)[:120])

async def submit_toptools_ai(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """toptools.ai — 3-field form"""
    p = "TopTools.AI"
    tracker.update(p, "PENDING")
    try:
        await page.goto("https://toptools.ai/submit", wait_until="domcontentloaded", timeout=20000)
        await page.locator('input[placeholder*="name" i]').first.fill(cfg.name)
        await page.locator('input[type="url"]').first.fill(cfg.url)
        await page.locator('input[type="email"]').fill(cfg.contact_email)
        await page.locator('button[type="submit"]').click()
        await page.wait_for_selector('text=/thank|success/i', timeout=15000)
        tracker.update(p, "SUBMITTED", "https://toptools.ai")
    except Exception as e:
        tracker.update(p, "FAILED", notes=str(e)[:120])

async def submit_saashub(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """saashub.com — requires account login (email: gulshan@promo.misar.io)"""
    p = "SaaSHub"
    tracker.update(p, "MANUAL", "https://saashub.com/services/submit",
        "Login at saashub.com (email: gulshan@promo.misar.io — check Mailcow for password) → /services/submit")

async def submit_insidr(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """insidr.ai — Tally form"""
    p = "Insidr.ai"
    tracker.update(p, "PENDING")
    try:
        await page.goto("https://www.insidr.ai/submit-tools/", wait_until="domcontentloaded", timeout=20000)
        tally = page.frame_locator('iframe[src*="tally"]').first
        await tally.locator('input').nth(0).fill(cfg.name)
        await tally.locator('input[type="url"]').first.fill(cfg.url)
        await tally.locator('textarea').first.fill(cfg.description_short)
        await tally.locator('input[type="email"]').fill(cfg.contact_email)
        await tally.locator('button[type="submit"]').click()
        await page.wait_for_timeout(3000)
        tracker.update(p, "SUBMITTED", "https://www.insidr.ai")
    except Exception as e:
        tracker.update(p, "FAILED", notes=str(e)[:120])

async def submit_launchingnext(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """launchingnext.com — direct form. Verified live: has anti-spam field 'What is 2+3?'"""
    p = "LaunchingNext"
    tracker.update(p, "PENDING")
    try:
        await page.goto("https://www.launchingnext.com/submit/", wait_until="domcontentloaded", timeout=20000)
        await page.locator('input[name="name"], input[id="name"]').first.fill(cfg.name)
        await page.locator('input[name="url"], input[id="url"], input[type="url"]').first.fill(cfg.url)
        await page.locator('textarea').first.fill(cfg.description_short)
        await page.locator('input[type="email"]').first.fill(cfg.contact_email)
        # Anti-spam field verified live: "What is 2+3?" → answer "5"
        antispam = page.locator('input[name*="spam"], input[name*="antispam"], input[placeholder*="2+3"], input[placeholder*="spam"]')
        if await antispam.count() > 0:
            await antispam.first.fill("5")
        await page.locator('button[type="submit"], input[type="submit"]').first.click()
        await page.wait_for_selector('text=/submit|thank|review/i', timeout=15000)
        tracker.update(p, "SUBMITTED", "https://www.launchingnext.com")
    except Exception as e:
        tracker.update(p, "FAILED", notes=str(e)[:120])

async def submit_uneed(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """Uneed.best — MANUAL: login required (verified live). Submit URL: /submit-a-tool"""
    tracker.update("Uneed.best", "MANUAL", "https://www.uneed.best/submit-a-tool",
        "Login required — create account at uneed.best then submit at /submit-a-tool")

async def submit_betalist(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """BetaList — MANUAL: login required (verified live)."""
    tracker.update("BetaList", "MANUAL", "https://betalist.com/submit",
        "Login required — create account at betalist.com then submit at /submit")

async def submit_toolpilot(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """toolpilot.ai — JotForm (add backlink first)"""
    p = "ToolPilot.ai"
    tracker.update(p, "PENDING")
    try:
        await page.goto("https://form.jotform.com/231772738321053", wait_until="networkidle", timeout=30000)
        await page.locator('input[id*="name"]').nth(0).fill(cfg.contact_name)
        company_f = page.locator('input[id*="company"]')
        if await company_f.count() > 0:
            await company_f.fill("Misar AI")
        await page.locator('input[type="email"]').fill(cfg.contact_email)
        tool_name_f = page.locator('input[id*="toolname"], input[id*="tool_name"]')
        if await tool_name_f.count() > 0:
            await tool_name_f.fill(cfg.name)
        await page.locator('input[type="url"]').fill(cfg.url)
        await page.locator('textarea').first.fill(cfg.description_short)
        web_check = page.locator('label:has-text("Web")')
        if await web_check.count() > 0:
            await web_check.click()
        free_opt = page.locator('label:has-text("Free")').first
        if await free_opt.count() > 0:
            await free_opt.click()
        terms = page.locator('input[type="checkbox"]').last
        if await terms.count() > 0 and not await terms.is_checked():
            await terms.click()
        await page.locator('button[type="submit"]').click()
        await page.wait_for_selector('text=/thank|submit/i', timeout=20000)
        tracker.update(p, "SUBMITTED", "https://www.toolpilot.ai")
    except Exception as e:
        tracker.update(p, "FAILED", notes=str(e)[:120])

async def submit_feedough(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """feedough.com — 22-step Formaloo"""
    p = "Feedough"
    tracker.update(p, "PENDING")
    try:
        await page.goto("https://www.feedough.com/submit-your-startup/", wait_until="networkidle", timeout=30000)
        frame = page.frame_locator('iframe[src*="formaloo"]').first
        await frame.locator('input[type="text"]').first.fill(cfg.contact_name)
        await frame.locator('button:has-text("Next"), button:has-text("Continue")').click()
        await page.wait_for_timeout(900)
        await frame.locator('input[type="text"]').first.fill(cfg.name)
        await frame.locator('button:has-text("Next"), button:has-text("Continue")').click()
        await page.wait_for_timeout(800)
        await frame.locator('input[type="text"]').first.fill("Founder")
        await frame.locator('button:has-text("Next"), button:has-text("Continue")').click()
        await page.wait_for_timeout(800)
        await frame.locator('input[type="email"]').first.fill(cfg.contact_email)
        await frame.locator('button:has-text("Next"), button:has-text("Continue")').click()
        tracker.update(p, "MANUAL", "https://www.feedough.com", "Steps 1-4 filled; complete 5-21 manually")
    except Exception as e:
        tracker.update(p, "FAILED", notes=str(e)[:120])

async def submit_software_suggest(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """softwaresuggest.com — work email required"""
    p = "Software Suggest"
    tracker.update(p, "PENDING")
    try:
        await page.goto("https://www.softwaresuggest.com/vendors", wait_until="domcontentloaded", timeout=20000)
        await page.locator('input[placeholder*="name" i]').nth(0).fill(cfg.contact_name)
        await page.locator('input[type="email"]').fill(cfg.contact_email)
        org = page.locator('input[name*="org"], input[name*="company"]')
        if await org.count() > 0:
            await org.fill("Misar AI")
        phone = page.locator('input[type="tel"]')
        if await phone.count() > 0:
            await phone.fill("+919999999999")
        url_f = page.locator('input[type="url"]')
        if await url_f.count() > 0:
            await url_f.fill(cfg.url)
        await page.locator('button[type="submit"]').click()
        await page.wait_for_selector('text=/thank|submit|success/i', timeout=15000)
        tracker.update(p, "SUBMITTED", "https://www.softwaresuggest.com")
    except Exception as e:
        tracker.update(p, "FAILED", notes=str(e)[:120])

async def submit_appsumo(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """sell.appsumo.com — HubSpot partner form. ✅ Confirmed 2026-03-27"""
    p = "AppSumo Marketplace"
    tracker.update(p, "PENDING")
    try:
        await page.goto("https://sell.appsumo.com", wait_until="networkidle", timeout=30000)
        await page.locator('input[name*="firstname"]').fill(cfg.contact_name.split()[0])
        lastname_f = page.locator('input[name*="lastname"]')
        if await lastname_f.count() > 0 and len(cfg.contact_name.split()) > 1:
            await lastname_f.fill(cfg.contact_name.split()[-1])
        await page.locator('input[type="email"]').fill(cfg.contact_email)
        url_f = page.locator('input[name*="website"], input[type="url"]')
        if await url_f.count() > 0:
            await url_f.fill(cfg.url)
        await page.locator('button[type="submit"]').click()
        await page.wait_for_selector('text=/Boom|thank|submit/i', timeout=15000)
        tracker.update(p, "SUBMITTED", "https://sell.appsumo.com", "AppSumo team reviews for fit")
    except Exception as e:
        tracker.update(p, "FAILED", notes=str(e)[:120])

async def submit_listmyai(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """ListMyAI — MANUAL: €49 paid submission (verified live Stripe payment gate)."""
    tracker.update("ListMyAI", "MANUAL", "https://listmyai.net/submit-ai-tools",
        "Paid listing — €49 via Stripe (verified live). Pay at listmyai.net/submit-ai-tools")


# ── Orchestrator ──────────────────────────────────────────────────────────────

AUTOMATABLE = [
    ("future_tools", submit_future_tools),
    ("toptools_ai", submit_toptools_ai),
    ("saashub", submit_saashub),
    ("insidr", submit_insidr),
    ("launchingnext", submit_launchingnext),
    ("uneed", submit_uneed),
    ("betalist", submit_betalist),
    ("toolpilot", submit_toolpilot),
    ("feedough", submit_feedough),
    ("software_suggest", submit_software_suggest),
    ("appsumo", submit_appsumo),
    ("listmyai", submit_listmyai),
]

MANUAL_PLATFORMS = [
    ("Product Hunt", "producthunt.com/posts/new → full launch strategy; logo + screenshots required"),
    ("G2", "g2.com/products/new → Google login (mryadavgulshan@gmail.com)"),
    ("Capterra/Gartner", "digitalmarkets.gartner.com/get-listed/start → 3-field form → click Continue"),
    ("AlternativeTo", "alternativeto.net → email signup only (Google disabled)"),
    ("CrunchBase", "crunchbase.com → connect Google social first → /add-new"),
    ("SourceForge", "sourceforge.net/software/vendors/new → reCAPTCHA blocks automation"),
    ("Hacker News", "news.ycombinator.com/submit → karma ≥ 10 required"),
    ("TAAFT", "Add backlink to theresanaiforthat.com on site → submit form"),
    ("Dang.ai", "Add badge to site → dang.ai/submit → reCAPTCHA"),
    ("SaaSGenius", "Email: contact@saasgenius.com — may not accept free listings"),
    ("SaaSWorthy", "Email: business@saasworthy.com with SaaS details"),
    ("Crozdesk", "vendor.revleads.com → fill application form"),
    ("NachoNacho", "connect.nachonacho.com/signup-seller → US-focus; verify eligibility"),
    ("Software Advice", "softwareadvice.com/vendors → open 9-field form"),
    ("Peerlist", "peerlist.io/user/projects/add-project → Google OAuth"),
    ("F6S", "f6s.com → Google OAuth → Add Company"),
    ("Indie Hackers", "indiehackers.com/products → Google OAuth (incognito)"),
    ("Startup Ranking", "startupranking.com → Google OAuth → 300+ char description required"),
    ("Fazier", "fazier.com/submit → embed badge → submit"),
    ("Dang.ai", "Add badge → dang.ai/submit → reCAPTCHA"),
]

async def main():
    parser = argparse.ArgumentParser(description="SaaS Listing Automation")
    parser.add_argument("--config", default="listing-config.yaml")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--platforms", default="")
    args = parser.parse_args()

    cfg = load_config(args.config)
    date_str = datetime.now().strftime("%Y%m%d-%H%M")
    tracker = SubmissionTracker(f"output/saas-listings-{date_str}.md")

    platforms = AUTOMATABLE
    if args.platforms:
        keys = set(args.platforms.split(","))
        platforms = [(n, f) for n, f in AUTOMATABLE if n in keys]

    print(f"\n📦 SaaS Listing Automation — {cfg.name}")
    print(f"   URL: {cfg.url}")
    print(f"   Platforms: {len(platforms)} automatable + {len(MANUAL_PLATFORMS)} manual\n")

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=False)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )
        for i in range(0, len(platforms), 4):
            await run_batch(context, platforms[i:i+4], cfg, tracker, args.dry_run)
            await asyncio.sleep(2)
        await browser.close()

    print(f"\n🔧 Manual platforms ({len(MANUAL_PLATFORMS)}):")
    for name, instruction in MANUAL_PLATFORMS:
        print(f"  • {name}: {instruction}")
    print(f"\n📋 Tracker: output/saas-listings-{date_str}.md")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Config Template (`listing-config.yaml`)

```yaml
name: "Misar.Blog"
url: "https://misar.blog"
tagline: "AI-first blogging platform with built-in SEO and AEO optimization"
description_short: "Misar.Blog is an AI-powered blogging platform with built-in SEO/AEO, smart editor, and MCP server integration."
description_long: |
  Misar.Blog is an AI-first blogging platform that helps writers and developers
  publish better content faster. Features: AI writing assistant, SEO/AEO optimizer,
  custom domains, MCP server for Claude integration, Draft Wizard,
  and real-time analytics. Free to start, Pro plans for power users.
category: "Blogging / Content / AI"
pricing_model: "Freemium"
pricing_tiers: "Free, Pro $4.99/mo, Business $19.99/mo"
contact_email: "gulshan@promo.misar.io"
contact_name: "Gulshan Yadav"
twitter: "@mrgulshanyadav"
linkedin: "linkedin.com/in/mrgulshanyadav"
github: "https://github.com/misar-ai"
logo_path: "./assets/logo.png"
screenshot_path: "./assets/screenshot.png"
```
