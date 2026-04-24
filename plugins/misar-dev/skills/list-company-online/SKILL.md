---
name: list-company-online
description: Submit company profiles to 50+ online directories, business listings, and platforms for maximum visibility, off-page SEO boost, and brand authority. Use when the user wants to list a company online, submit business profiles, boost off-page SEO, or mentions "list company", "business directory", "company listing", "off-page SEO", "business visibility", "list business online".
user-invocable: true
argument-hint: "[--config listing-config.yaml] [--dry-run] [--platforms crunchbase,f6s,betalist,...]"
---

# List Company Online

Automated company profile submission to 50+ online directories ranked by SEO authority and visibility impact. Creates business profiles, fills forms, handles errors, and verifies listings for off-page SEO boost and brand discoverability.

## When to Trigger

- User says "list company online", "submit company to directories", "off-page SEO", "business listing"
- User invokes `/list-company-online`
- User mentions company directory submissions, business profiles, brand visibility, off-page SEO

## Execution Protocol

### Phase 1: Preparation

1. Read company details from user input or project context (company name, website, description, industry, team size, founding year, locations, social links)
2. Create a tracking file at `Work/output/company-listings-tracker-{date}.md` with all 50 directories as a checklist
3. Each entry tracks: Platform | DA (Domain Authority) | Status | Profile URL | Notes

### Phase 2: Submission (Per Directory)

For EACH directory:

1. **Navigate** to the directory's submission/signup/add page
2. **Detect** form type and requirements
3. **Fill** company profile completely:
   - Company name, website, description
   - Industry/category selection
   - Location, team size, founding year
   - Social media links
   - Logo upload where supported
4. **Submit** and handle errors
5. **Verify** profile is live (search for company name on platform)

### Phase 3: Update Tracker

After each submission, update tracker with status, profile URL, and DA score.

## Top 50 Company Directories (Ranked by SEO Authority & Reach)

| Rank | Directory | Submit URL | DA | Type | Focus |
|------|-----------|-----------|-----|------|-------|
| 1 | Google Business Profile | business.google.com | 100 | Business listing | Local + global |
| 2 | LinkedIn Company Page | linkedin.com/company/setup | 99 | Professional network | B2B visibility |
| 3 | CrunchBase | crunchbase.com/add | 91 | Company database | Startups/tech |
| 4 | AngelList / Wellfound | wellfound.com/company/new | 88 | Startup platform | Hiring + investors |
| 5 | Bing Places | bingplaces.com | 93 | Business listing | Search visibility |
| 6 | Apple Maps Connect | mapsconnect.apple.com | 100 | Business listing | iOS users |
| 7 | Yelp | biz.yelp.com/signup | 93 | Business reviews | Local business |
| 8 | Product Hunt | producthunt.com/posts/new | 88 | Product launches | Tech companies |
| 9 | TrustPilot | business.trustpilot.com/signup | 93 | Reviews | Consumer trust |
| 10 | G2 | g2.com/products/new | 89 | Software reviews | SaaS companies |
| 11 | Capterra | capterra.com/vendors/sign-up | 88 | Software reviews | Software vendors |
| 12 | SourceForge | sourceforge.net/software/vendors/new | 88 | Software dir | Tech companies |
| 13 | F6S | f6s.com/company/new | 75 | Startup platform | Startup ecosystem |
| 14 | HackerNews (Show HN) | news.ycombinator.com/submit | 89 | Community | Tech launches |
| 15 | StartupBlink | startupblink.com/submit | 58 | Startup map | Startup ecosystems |
| 16 | SaaSHub | saashub.com/services/submit | 60 | SaaS comparison | SaaS companies |
| 17 | BetaList | betalist.com/submit | 65 | Beta directory | Early-stage |
| 18 | Indie Hackers | indiehackers.com/products | 70 | Indie community | Bootstrapped |
| 19 | Startup Ranking | startupranking.com/startup/create/url-validation | 55 | Rankings | Startup metrics |
| 20 | LaunchingNext | launchingnext.com/submit | 48 | Launch dir | New companies |
| 21 | AlternativeTo | alternativeto.net (email signup) | 78 | Alternatives | Software |
| 22 | Foursquare / Swarm | business.foursquare.com | 88 | Location | Local businesses |
| 23 | Facebook Business | facebook.com/pages/create | 96 | Business page | Social visibility |
| 24 | Twitter/X Profile | x.com | 94 | Social profile | Brand presence |
| 25 | GitHub Organization | github.com/organizations/new | 95 | Dev platform | Open source |
| 26 | Medium Publication | medium.com | 94 | Content platform | Thought leadership |
| 27 | Dev.to Organization | dev.to/settings/organization | 82 | Dev community | Dev companies |
| 28 | Hashnode Team Blog | hashnode.com/teams | 75 | Dev blogs | Tech companies |
| 29 | Yellow Pages | yellowpages.com/free-listing | 85 | Business dir | Local/general |
| 30 | Manta | manta.com/add-business | 72 | Business dir | SMB |
| 31 | Hotfrog | hotfrog.com/add-business | 60 | Business dir | Local business |
| 32 | Alignable | alignable.com/signup | 55 | SMB network | Local business |
| 33 | Startup India | startupindia.gov.in/registration | 70 | Govt platform | Indian startups |
| 34 | IndiaMART | indiamart.com/seller | 82 | B2B marketplace | Indian businesses |
| 35 | JustDial | justdial.com/free-listing | 75 | Business dir | Indian businesses |
| 36 | Sulekha | sulekha.com/list-business | 68 | Business dir | Indian services |
| 37 | TradeIndia | tradeindia.com/seller | 70 | B2B marketplace | Indian businesses |
| 38 | Software Advice | softwareadvice.com/vendors | 85 | Software reviews | Software vendors |
| 39 | Crozdesk | crozdesk.com/vendor | 55 | Software dir | B2B SaaS |
| 40 | Reddit (relevant subs) | reddit.com/submit | 98 | Community | All |
| 41 | Peerlist | peerlist.io/user/projects/add-project | 55 | Dev network | Tech companies |
| 42 | Dev.to Organization | dev.to/settings/organization | 82 | Dev community | Dev companies |
| 43 | Feedough | feedough.com/submit-your-startup | 60 | Startup directory | Startups |
| 44 | TopStartups.io | topstartups.io (submit) | 50 | Startup directory | Tech startups |
| 45 | Startupresources.io | startupresources.io (submit) | 45 | Startup tools | Startup ecosystem |
| 46 | F6S | f6s.com (add company) | 75 | Startup platform | Startups/accelerators |
| 47 | Hashnode Team Blog | hashnode.com/teams | 75 | Dev blogs | Tech companies |
| 48 | StartupBlink | startupblink.com/submit | 58 | Startup map | Global startups |
| 49 | Blastra | blastra.io | 40 | B2B directory | B2B SaaS |
| 50 | Product Directory | productdirectory.io/submit | 35 | Product directory | All products |

NOTE: The following directories were confirmed paid-only or defunct (2026-03) and excluded:
- Better Business Bureau (BBB) — paid accreditation required ($500+/yr)
- Glassdoor Employers — paid employer branding ($199+/mo)
- Clutch.co — paid vendor application ($1000+/yr for featured)
- GoodFirms — $1500+/yr for software/services listing
- NASSCOM — paid industry membership
- DnB (Dun & Bradstreet) — enterprise paid service
- ZoomInfo — paid B2B intelligence platform
- Chamber of Commerce — paid membership
- MicroAcquire/Acquire — acquisition marketplace, not general listing
- StackShare — 500 server error + OAuth-only
- KillerStartups — newsletter signup only, no form
- StartupBase — signups closed
- Capterra duplicate (profile) — same as rank 11

## Company Profile Template

| Field | Value |
|-------|-------|
| Company Name | [from user] |
| Legal Name | [from user or company name] |
| Website | [from user] |
| Description | [from user - max 500 chars for short, full for long] |
| Industry | AI / Technology / SaaS / Software Development |
| Founded | [from user] |
| Team Size | [from user] |
| HQ Location | [from user] |
| Social Links | LinkedIn, Twitter/X, GitHub, etc. |
| Logo | Upload if available |
| Products/Services | List of products |
| Email | Contact email |
| Phone | If provided |

## SEO Benefits Tracking

Each listing provides:
- **Backlink**: Follow/nofollow, DA score
- **NAP Consistency**: Name, Address, Phone match
- **Brand Signal**: Citation in authoritative directory
- **Referral Traffic**: Potential clicks from directory

## Error Recovery Patterns

Same as list-tools-online skill, plus:

| Error Type | Action |
|-----------|--------|
| "Company already claimed" | Try to claim or verify ownership |
| Verification required (phone/mail) | Mark MANUAL with verification method |
| Industry mismatch | Try closest alternative category |
| Geographic restriction | Skip if not applicable |

## Contact Info Template

```
Name: Gulshan Yadav
Email: gulshan@promo.misar.io
Company: Misar AI
Title: Founder
Twitter: @mrgulshanyadav
LinkedIn: linkedin.com/in/mrgulshanyadav
Website: [company URL provided by user]
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

### Step 1 — Save base script
Extract the BASE SCRIPT block below to `~/.claude/scripts/listing_base.py`

### Step 2 — Save platform script
Extract the PLATFORM SCRIPT block to `~/.claude/scripts/list_company_auto.py`

### Step 3 — Create config
Save the CONFIG TEMPLATE to `listing-config.yaml` and fill in your company details.

### Step 4 — Run
```bash
cd your-project
python ~/.claude/scripts/list_company_auto.py --config listing-config.yaml
# Dry run (no submissions):
python ~/.claude/scripts/list_company_auto.py --config listing-config.yaml --dry-run
# Specific platforms only:
python ~/.claude/scripts/list_company_auto.py --config listing-config.yaml --platforms "crunchbase,f6s,toptools_ai"
```

---

### BASE SCRIPT (`listing_base.py`)

```python
#!/usr/bin/env python3
"""
Auto-submitter base. Save to ~/.claude/scripts/listing_base.py
"""
import asyncio, yaml, argparse, sys
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional
from playwright.async_api import async_playwright, Page, BrowserContext

@dataclass
class ListingConfig:
    name: str
    url: str
    tagline: str
    description_short: str       # ≤160 chars
    description_long: str
    category: str
    pricing_model: str           # Free / Freemium / Subscription
    pricing_tiers: str
    contact_email: str
    contact_name: str
    twitter: str
    linkedin: str
    github: str
    company_name: str
    company_industry: str
    company_size: str            # 1-10 / 11-50 / 51-200 / 201-500 / 500+
    company_founded: str         # YYYY
    company_location: str        # City, Country
    logo_path: Optional[str] = None
    screenshot_path: Optional[str] = None

class SubmissionTracker:
    def __init__(self, output_path: str):
        self.path = Path(output_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.entries: list[dict] = []

    def update(self, platform: str, status: str, url: str = "", notes: str = ""):
        self.entries.append({"platform": platform, "status": status,
                             "url": url, "notes": notes, "ts": datetime.now().isoformat()})
        self._write()

    def _write(self):
        lines = ["# Company Listing Tracker\n",
                 f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n",
                 "| Platform | Status | URL | Notes |\n",
                 "|----------|--------|-----|-------|\n"]
        for e in self.entries:
            lines.append(f"| {e['platform']} | {e['status']} | {e['url']} | {e['notes']} |\n")
        self.path.write_text("".join(lines))

def load_config(path: str) -> ListingConfig:
    data = yaml.safe_load(Path(path).read_text())
    return ListingConfig(**data)
```

---

### PLATFORM SCRIPT (`list_company_auto.py`)

```python
#!/usr/bin/env python3
"""
Company directory auto-submitter.
Save to ~/.claude/scripts/list_company_auto.py
Usage: python list_company_auto.py --config listing-config.yaml [--dry-run] [--platforms p1,p2]
"""
import asyncio, sys, argparse
from datetime import datetime
from pathlib import Path
sys.path.insert(0, str(Path.home() / ".claude/scripts"))
from listing_base import ListingConfig, SubmissionTracker, load_config
from playwright.async_api import async_playwright, Page, BrowserContext

# ─── AUTOMATABLE PLATFORMS ───────────────────────────────────────────────────

async def submit_crunchbase(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """CrunchBase — free company profile. DA 91."""
    try:
        await page.goto("https://www.crunchbase.com/add-new/company", timeout=15000)
        await page.wait_for_selector("input[placeholder*='company name'], input[name*='name']", timeout=8000)
        name_input = page.locator("input[placeholder*='company name'], input[name*='name']").first
        await name_input.fill(cfg.company_name)
        url_input = page.locator("input[placeholder*='website'], input[name*='website']").first
        await url_input.fill(cfg.url)
        await page.wait_for_timeout(1500)
        tracker.update("CrunchBase", "FILLED", "https://crunchbase.com", "Complete form + submit manually")
    except Exception as e:
        tracker.update("CrunchBase", "FAILED", "", str(e))

async def submit_f6s(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """F6S — startup community. DA 68. Google OAuth required → semi-auto."""
    try:
        await page.goto("https://www.f6s.com/company/new", timeout=15000)
        await page.wait_for_selector("input[name='name'], input[placeholder*='company']", timeout=8000)
        await page.fill("input[name='name']", cfg.company_name)
        try:
            await page.fill("input[name='url'], input[name='website']", cfg.url)
        except Exception:
            pass
        try:
            await page.fill("textarea[name='description'], textarea[name='tagline']", cfg.description_short)
        except Exception:
            pass
        tracker.update("F6S", "PARTIAL", "https://f6s.com", "Login via Google required to complete")
    except Exception as e:
        tracker.update("F6S", "FAILED", "", str(e))

async def submit_betalist(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """BetaList — MANUAL: login required (verified live)."""
    tracker.update("BetaList", "MANUAL", "https://betalist.com/submit",
        "Login required — create account at betalist.com then submit at /submit")

async def submit_toptools_ai(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """TopTools.AI — AI tool directory. DA 38. 400K+ visitors."""
    try:
        await page.goto("https://www.toptools.ai/submit-tool/", timeout=15000)
        await page.wait_for_selector("input[placeholder*='name'], input[name*='name']", timeout=8000)
        name_field = page.locator("input[placeholder*='Tool Name'], input[placeholder*='Product']").first
        await name_field.fill(cfg.name)
        url_field = page.locator("input[placeholder*='URL'], input[placeholder*='website']").first
        await url_field.fill(cfg.url)
        desc_field = page.locator("textarea").first
        await desc_field.fill(cfg.description_short)
        email_field = page.locator("input[type='email']").first
        await email_field.fill(cfg.contact_email)
        await page.wait_for_timeout(1000)
        tracker.update("TopTools.AI", "FILLED", "https://toptools.ai", "Check form then submit")
    except Exception as e:
        tracker.update("TopTools.AI", "FAILED", "", str(e))

async def submit_insidr(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """Insidr.ai — Tally-based AI directory form. DA 34. 150K+ visitors."""
    try:
        await page.goto("https://www.insidr.ai/submit-tools/", timeout=15000)
        await page.wait_for_selector("a[href*='tally'], iframe[src*='tally']", timeout=6000)
        tally_link = page.locator("a[href*='tally.so']").first
        href = await tally_link.get_attribute("href")
        await page.goto(href, timeout=15000)
        await page.wait_for_selector("input[data-tally-node], input[placeholder]", timeout=8000)
        inputs = page.locator("input[placeholder]")
        count = await inputs.count()
        if count > 0: await inputs.nth(0).fill(cfg.name)
        if count > 1: await inputs.nth(1).fill(cfg.url)
        if count > 2: await inputs.nth(2).fill(cfg.contact_email)
        tracker.update("Insidr.ai", "FILLED", "https://insidr.ai", "Review Tally form + submit")
    except Exception as e:
        tracker.update("Insidr.ai", "FAILED", "", str(e))

async def submit_launchingnext(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """LaunchingNext — 350K+ visitors. DA 41. Verified live: anti-spam field 'What is 2+3?'"""
    try:
        await page.goto("https://www.launchingnext.com/submit/", timeout=15000)
        await page.wait_for_selector("input[name='name'], input[id='name']", timeout=8000)
        await page.fill("input[name='name'], input[id='name']", cfg.name)
        await page.fill("input[name='url'], input[id='url'], input[type='url']", cfg.url)
        try:
            await page.fill("input[type='email']", cfg.contact_email)
        except Exception:
            pass
        try:
            await page.fill("textarea", cfg.description_short)
        except Exception:
            pass
        # Anti-spam field verified live: "What is 2+3?" → answer "5"
        antispam = page.locator('input[name*="spam"], input[name*="antispam"], input[placeholder*="2+3"], input[placeholder*="spam"]')
        if await antispam.count() > 0:
            await antispam.first.fill("5")
        tracker.update("LaunchingNext", "FILLED", "https://launchingnext.com", "Review + submit")
    except Exception as e:
        tracker.update("LaunchingNext", "FAILED", "", str(e))

async def submit_uneed(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """Uneed.best — MANUAL: login required (verified live). Submit URL: /submit-a-tool"""
    tracker.update("Uneed.best", "MANUAL", "https://www.uneed.best/submit-a-tool",
        "Login required — create account at uneed.best then submit at /submit-a-tool")

async def submit_listmyai(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """ListMyAI — MANUAL: €49 paid submission (verified live Stripe payment gate)."""
    tracker.update("ListMyAI", "MANUAL", "https://listmyai.net/submit-ai-tools",
        "Paid listing — €49 via Stripe (verified live). Pay at listmyai.net/submit-ai-tools")

async def submit_startup_ranking(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """StartupRanking — DA 50. Startup metrics tracker."""
    try:
        await page.goto("https://www.startupranking.com/startup/new", timeout=15000)
        await page.wait_for_selector("input[name='name'], input[placeholder*='startup name']", timeout=8000)
        await page.fill("input[name='name']", cfg.company_name)
        await page.fill("input[name='url'], input[name='website']", cfg.url)
        tracker.update("StartupRanking", "PARTIAL", "https://startupranking.com", "Login required to finalize")
    except Exception as e:
        tracker.update("StartupRanking", "FAILED", "", str(e))

async def submit_fazier(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """Fazier — MANUAL: login required (verified live). Free listing with badge after login."""
    tracker.update("Fazier", "MANUAL", "https://fazier.com/submit",
        "Login required — create account at fazier.com then submit at /submit for free badge listing")

async def submit_feedough(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """Feedough — Formaloo-based form. 800K+ visitors. DA 59."""
    try:
        await page.goto("https://www.feedough.com/submit-your-startup/", timeout=15000)
        await page.wait_for_selector("a[href*='formaloo'], iframe[src*='formaloo']", timeout=6000)
        try:
            formaloo_link = page.locator("a[href*='formaloo.me']").first
            href = await formaloo_link.get_attribute("href")
            await page.goto(href, timeout=15000)
        except Exception:
            pass
        await page.wait_for_selector("input[placeholder], input[type='text']", timeout=8000)
        inputs = page.locator("input[type='text'], input[placeholder]")
        count = await inputs.count()
        if count > 0: await inputs.nth(0).fill(cfg.name)
        if count > 1: await inputs.nth(1).fill(cfg.url)
        if count > 2: await inputs.nth(2).fill(cfg.description_short[:160])
        tracker.update("Feedough", "PARTIAL", "https://feedough.com", "Complete remaining Formaloo fields + submit")
    except Exception as e:
        tracker.update("Feedough", "FAILED", "", str(e))

async def submit_toolpilot(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """ToolPilot.ai — JotForm submission. 2M+ visitors."""
    try:
        await page.goto("https://form.jotform.com/231772738321053", timeout=15000)
        await page.wait_for_selector("input[id*='first'], input[placeholder*='Tool']", timeout=8000)
        name_inputs = page.locator("input[id*='text'], input[placeholder]")
        count = await name_inputs.count()
        if count > 0: await name_inputs.nth(0).fill(cfg.name)
        if count > 1: await name_inputs.nth(1).fill(cfg.url)
        if count > 2: await name_inputs.nth(2).fill(cfg.contact_email)
        try:
            await page.fill("textarea", cfg.description_short)
        except Exception:
            pass
        tracker.update("ToolPilot.ai", "FILLED", "https://toolpilot.ai", "Review + submit JotForm")
    except Exception as e:
        tracker.update("ToolPilot.ai", "FAILED", "", str(e))

# ─── ORCHESTRATOR ────────────────────────────────────────────────────────────

AUTOMATABLE = [
    ("crunchbase", submit_crunchbase),
    ("f6s", submit_f6s),
    ("betalist", submit_betalist),
    ("toptools_ai", submit_toptools_ai),
    ("insidr", submit_insidr),
    ("launchingnext", submit_launchingnext),
    ("uneed", submit_uneed),
    ("listmyai", submit_listmyai),
    ("startup_ranking", submit_startup_ranking),
    ("fazier", submit_fazier),
    ("feedough", submit_feedough),
    ("toolpilot", submit_toolpilot),
]

MANUAL_PLATFORMS = [
    "Google Business Profile — business.google.com — Google account + phone verification required",
    "LinkedIn Company Page — linkedin.com/company/setup — LinkedIn login required; fill Name/URL/Industry/Size/Founded",
    "AngelList / Wellfound — wellfound.com/company/new — Login required; fill name, website, tagline, team size, stage",
    "Product Hunt — producthunt.com/posts/new — PH account required; schedule for Tuesday 12:01 AM PST",
    "Glassdoor — glassdoor.com/employers/sign-up — HR email required for verification",
    "Yelp for Business — biz.yelp.com/claim — Phone + address verification required",
    "Bing Places — bingplaces.com — Microsoft account + postcard/phone verification",
    "Apple Maps — mapsconnect.apple.com — Apple ID + business verification",
    "Foursquare / Swarm — foursquare.com/add-listing — OAuth required",
    "Clutch.co — clutch.co/get-listed — Agency/company verification process",
    "G2 — g2.com/products/new — Manual review + vendor profile completion",
    "Trustpilot — business.trustpilot.com — Business email verification required",
    "Capterra — capterra.com/vendors/sign-up — Manual review + contract for paid listings",
    "HackerNews — news.ycombinator.com/submit — 10+ karma required; 'Show HN' post",
    "Reddit r/startups — reddit.com/r/startups — Read rules; no blatant promotion",
    "Reddit r/entrepreneur — reddit.com/r/entrepreneur — Community post format required",
    "Twitter/X — x.com — Manual announcement thread with product screenshots",
    "GitHub — github.com — Create org page, add topics: ai-company, saas, startup",
    "Press Hunt (HARO alternative) — presshunt.co — Register as source for PR opportunities",
    "Startup.info — startup.info/submit-startup — Email submission required",
]

async def run_batch(context: BrowserContext, batch, cfg, tracker):
    tasks = [fn(await context.new_page(), cfg, tracker) for _, fn in batch]
    await asyncio.gather(*tasks, return_exceptions=True)

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="listing-config.yaml")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--platforms", default="")
    args = parser.parse_args()

    cfg = load_config(args.config)
    tracker = SubmissionTracker(f"output/company-listings-{datetime.now():%Y%m%d}.md")

    platforms = AUTOMATABLE
    if args.platforms:
        names = set(args.platforms.split(","))
        platforms = [(n, f) for n, f in AUTOMATABLE if n in names]

    if args.dry_run:
        print("DRY RUN — platforms that would be submitted:")
        for name, _ in platforms:
            print(f"  ✓ {name}")
        print(f"\nManual platforms ({len(MANUAL_PLATFORMS)}):")
        for p in MANUAL_PLATFORMS:
            print(f"  - {p}")
        return

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=False)
        context = await browser.new_context()
        for i in range(0, len(platforms), 4):
            await run_batch(context, platforms[i:i+4], cfg, tracker)
        await browser.close()

    print(f"\nTracker saved → {tracker.path}")
    print(f"\n🔧 Manual platforms requiring human action ({len(MANUAL_PLATFORMS)}):")
    for p in MANUAL_PLATFORMS:
        print(f"  - {p}")

if __name__ == "__main__":
    asyncio.run(main())
```

---

### CONFIG TEMPLATE (`listing-config.yaml`)

```yaml
name: "Misar AI"
url: "https://misar.io"
tagline: "AI-first developer tools for the modern web"
description_short: "Misar AI builds open-source AI developer tools: Misar.Blog, MisarMail, MisarDev Studio, and MisarCoder."
description_long: |
  Misar AI is a suite of AI-first developer products — Misar.Blog (AI blogging),
  MisarMail (self-hosted email), MisarDev Studio (AI webapp builder), and MisarCoder
  (MoE AI engine). Built with Next.js 15, Supabase, and M.A.N.A.V. ethical AI principles.
  Privacy-first. No training on user data. Open-source core.
category: "AI Developer Tools"
pricing_model: "Freemium"
pricing_tiers: "Free, Pro $4.99/mo, Business $19.99/mo"
contact_email: "gulshan@promo.misar.io"
contact_name: "Gulshan Yadav"
twitter: "@mrgulshanyadav"
linkedin: "linkedin.com/in/mrgulshanyadav"
github: "github.com/misar-ai"
company_name: "Misar AI Technology Pvt. Ltd."
company_industry: "Artificial Intelligence / SaaS"
company_size: "1-10"
company_founded: "2024"
company_location: "India"
logo_path: "./assets/logo.png"
screenshot_path: "./assets/screenshot.png"
```
