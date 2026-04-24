---
name: list-mcp-online
description: Submit MCP (Model Context Protocol) servers to 50+ directories, registries, and marketplaces for maximum discoverability. Use when the user wants to list an MCP server online, publish to MCP registries, get an MCP tool discovered, or mentions "list MCP", "submit MCP server", "MCP registry", "MCP directory", "publish MCP", "MCP marketplace".
user-invocable: true
argument-hint: "[--config listing-config.yaml] [--dry-run] [--platforms smithery,mcp_so,...]"
---

# List MCP Online

Automated MCP server submission to 50 directories ranked by MCP ecosystem reach + general AI tool visibility. Covers dedicated MCP registries, package registries, IDE plugin stores, AI tool directories, and developer communities.

## When to Trigger

- User says "list MCP online", "submit MCP server", "publish my MCP", "get my MCP discovered"
- User invokes `/list-mcp-online`
- User mentions MCP registry, MCP marketplace, Smithery, mcp.so, PulseMCP, awesome-mcp-servers

## Execution Protocol

### Phase 1: Preparation

1. Read MCP server details from user input or project context (npm/PyPI package name, GitHub repo, tool description, smithery.yaml path)
2. Create tracking file at `output/mcp-listings-tracker-{date}.md`
3. Each entry tracks: Platform | Status | URL | Notes

### Phase 2: Submission (Per Directory)

For EACH directory below:
1. **Navigate** to submission/add page
2. **Detect** form type: direct form → fill; OAuth → Google (mryadavgulshan@gmail.com); CLI → run command; PR → open GitHub PR; paid/broken → skip
3. **Fill** completely; submit; verify
4. **Update** tracker immediately after each attempt

### Phase 3: Parallel Batches

- Up to 4 browser-based submissions in parallel
- CLI-based (npm, PyPI, GitHub API) run sequentially before browser submissions
- Print MANUAL list at end

---

## Top 50 MCP Directories (Ranked by MCP + AI Reach)

| # | Platform | Submit URL | Type | Traffic/Reach |
|---|----------|-----------|------|--------------|
| 1 | Smithery | smithery.ai | MCP registry | PRIMARY — #1 MCP marketplace |
| 2 | MCP.so | mcp.so | MCP directory | 500K+ MCP-focused |
| 3 | Glama.ai/mcp | glama.ai/mcp | MCP explorer | Metrics + listings |
| 4 | PulseMCP | pulsemcp.com | MCP newsletter+DB | Weekly digest, searchable |
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
| 16 | Windsurf Plugins | codeium.com/windsurf | IDE integration | Partner form |
| 17 | Product Hunt | producthunt.com/posts/new | Launch platform | 10M+ |
| 18 | There's An AI For That | theresanaiforthat.com/submit | AI directory | 2M+ |
| 19 | Future Tools | futuretools.io/submit-a-tool | AI directory | 2M+ |
| 20 | ToolPilot.ai | form.jotform.com/231772738321053 | AI directory | 2M+ |
| 21 | Dev.to (Show DEV) | dev.to/new | Dev community | 7M+ |
| 22 | Hacker News (Show HN) | news.ycombinator.com/submit | Dev community | 10M+ |
| 23 | Reddit r/ClaudeAI | reddit.com/r/ClaudeAI/submit | Community | Claude-specific |
| 24 | Reddit r/artificial | reddit.com/r/artificial/submit | Community | 2M+ |
| 25 | OpenTools.ai | opentools.ai | AI directory | 400K+ |
| 26 | TopTools.AI | toptools.ai/submit | AI directory | 400K+ |
| 27 | Insidr.ai | insidr.ai/submit-tools | AI directory | 150K+ |
| 28 | Dang.ai | dang.ai/submit | AI directory | 300K+ |
| 29 | ListMyAI | listmyai.net/submit-ai-tools | AI directory | 200K+ |
| 30 | Easy With AI | easywithai.com/submit-tool | AI directory | 200K+ |
| 31 | AI Tool Hunt | aitoolhunt.com/submit | AI directory | 150K+ |
| 32 | Supertools/Rundown | rundown.ai/submit | AI newsletter | 250K+ |
| 33 | PoweredbyAI | poweredbyai.app | AI directory | 120K+ |
| 34 | SaaSHub | saashub.com/services/submit | SaaS comparison | 2.5M+ |
| 35 | AlternativeTo | alternativeto.net | Alternatives | 5M+ |
| 36 | Feedough | feedough.com/submit-your-startup | Startup directory | 800K+ |
| 37 | BetaList | betalist.com/submit | Beta launches | 500K+ |
| 38 | Uneed.best | uneed.best/submit | Tool directory | 700K+ |
| 39 | LaunchingNext | launchingnext.com/submit | Launch directory | 350K+ |
| 40 | Peerlist | peerlist.io/user/projects/add-project | Dev network | 300K+ |
| 41 | Fazier | fazier.com/submit | Launch platform | 800K+ |
| 42 | F6S | f6s.com | Startup platform | 500K+ |
| 43 | Startup Ranking | startupranking.com/startup/create/url-validation | Rankings | 250K+ |
| 44 | Hashnode | hashnode.com | Dev blogging | 5M+ |
| 45 | Software Suggest | softwaresuggest.com/vendors | Software reviews | 500K+ |
| 46 | Crozdesk | vendor.revleads.com | Software dir | 800K+ |
| 47 | LinkedIn | linkedin.com | Professional | B2B |
| 48 | Indie Hackers | indiehackers.com/products | Indie community | 500K+ |
| 49 | AppSumo Marketplace | sell.appsumo.com | Marketplace | 5M+ |
| 50 | ToolScout | toolscout.ai/submit | AI directory | 80K+ |

---

## Per-Platform Submission Steps

### 1. Smithery (smithery.ai) — PRIMARY
- **Method:** Add `smithery.yaml` to your repo root + open PR to smithery-ai/servers OR use Smithery CLI
- **smithery.yaml minimum:**
  ```yaml
  name: "Your MCP Server Name"
  description: "What it does"
  url: "https://github.com/you/your-mcp"
  ```
- **CLI submit:** `npx @smithery/cli submit --name "Name" --github https://github.com/you/repo`
- **Steps:** Visit smithery.ai → "Submit Server" → fill form → connect GitHub repo
- **Notes:** Smithery is the #1 MCP discovery platform. Must have public GitHub repo.

### 2. MCP.so
- **Auth:** None or GitHub
- **Steps:** mcp.so → Submit/Add button → Tool Name + Description + GitHub URL + Category → Submit
- **Notes:** Dedicated MCP directory, well-indexed by MCP users

### 3. Glama.ai/mcp
- **Auth:** GitHub OAuth
- **Steps:** glama.ai/mcp → "Add MCP Server" → GitHub repo URL → auto-scrapes metadata
- **Notes:** Auto-generates stats (stars, forks, last commit). GitHub OAuth required.

### 4. PulseMCP (pulsemcp.com)
- **Auth:** Email submission
- **Steps:** pulsemcp.com → "Submit a Server" → fill form OR email founders@pulsemcp.com with details
- **Notes:** Weekly newsletter to MCP devs. High quality audience.

### 5. mcpservers.org
- **Method:** GitHub PR
- **Steps:** Fork github.com/mcpservers/mcpservers.org → Add entry to `servers.json` → Open PR
- **Notes:** Community-curated, merges quickly

### 6. mcp-get (mcp-get.com)
- **Method:** npm package registration with `mcp-server` keyword
- **Steps:** Add `"keywords": ["mcp", "mcp-server", "model-context-protocol"]` to package.json → `npm publish` → mcp-get auto-indexes
- **Notes:** mcp-get searches npm for `mcp-server` keyword automatically

### 7. awesome-mcp-servers (github.com/modelcontextprotocol/servers)
- **Method:** GitHub PR to README.md
- **Steps:** Fork modelcontextprotocol/servers → Add to README under correct category → PR with format: `- [Name](URL) - Description`
- **Notes:** Official Anthropic list. High-quality curation, takes 1-2 weeks.

### 8. npm registry
- **Method:** CLI publish
- **Steps:** Ensure `package.json` has `"keywords": ["mcp-server", "claude", "model-context-protocol"]` → `npm publish --access public`
- **Notes:** Auto-discoverable by mcp-get and Smithery. Essential for TypeScript MCPs.

### 9. PyPI
- **Method:** CLI publish
- **Steps:** `python -m build` → `twine upload dist/*` → ensure `pyproject.toml` classifiers include `mcp-server` keyword
- **Notes:** For Python MCP servers. mcp-get and Glama auto-index PyPI packages too.

### 10. GitHub Topics
- **Method:** GitHub API or manual
- **Steps:** Go to your repo → ⚙️ (gear next to About) → Topics: add `mcp-server`, `model-context-protocol`, `claude-mcp`, `anthropic`
- **Notes:** Free, instant, improves discoverability on GitHub search

### 11. Cursor Directory (cursor.directory)
- **Auth:** GitHub OAuth
- **Steps:** cursor.directory → "Submit" → GitHub OAuth → Name + Description + GitHub URL + Category: MCP → Submit
- **Notes:** 2M+ Cursor users. MCP has its own category.

### 12. Continue.dev (continue.dev/extensions)
- **Method:** GitHub PR to continuedev/continue repo
- **Steps:** Submit to config/extensions registry OR write a tutorial at continue.dev
- **Notes:** Open-source IDE copilot. Growing rapidly.

### 13. VS Code Marketplace
- **Auth:** Microsoft publisher account
- **Steps:** Only if your MCP is wrapped as a VS Code extension → `vsce publish` with valid publisher account
- **Notes:** Skip if pure npm/Python package. Use Open VSX as free alternative.

### 14. Open VSX (open-vsx.org)
- **Method:** `ovsx publish` CLI
- **Steps:** Create account at open-vsx.org → `npm install -g ovsx` → `ovsx publish`
- **Notes:** Free alternative to VS Code Marketplace. Eclipse Theia, Gitpod, etc. use this.

### 15. Cline Community MCPs (github.com/cline/cline)
- **Method:** GitHub PR
- **Steps:** Fork cline/cline → Add MCP to `docs/mcp-servers.md` or community list → PR
- **Notes:** Cline has large community. Check repo for current contribution guide.

### 16. Windsurf Plugins (codeium.com/windsurf)
- **Auth:** Partner form
- **Steps:** codeium.com/windsurf → Developers/Partners → Submit integration form
- **Notes:** Manual review, takes ~1 week

### 17–50. See `list-tools-online` + `list-saas-online` skill for detailed steps
Platforms 17–50 follow the same submission protocol as documented in those skills. MCP servers are accepted by all general AI tool directories — use your MCP's website URL + description.

---

## Automation Scripts (Python + Playwright)

### Prerequisites
```bash
pip install playwright pyyaml
playwright install chromium
```

### Run Instructions
```bash
# Save base script to ~/.claude/scripts/listing_base.py (block below)
# Save platform script to ~/.claude/scripts/list_mcp_auto.py (second block below)
# Create listing-config.yaml with your MCP details
python ~/.claude/scripts/list_mcp_auto.py --config listing-config.yaml
python ~/.claude/scripts/list_mcp_auto.py --config listing-config.yaml --dry-run
python ~/.claude/scripts/list_mcp_auto.py --config listing-config.yaml --platforms "future_tools,toptools_ai,insidr"
```

### Block 1 — Base Classes (save as `~/.claude/scripts/listing_base.py`)

```python
#!/usr/bin/env python3
"""Shared base for all listing automation scripts."""
import asyncio, yaml, argparse
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Callable, Awaitable
from playwright.async_api import Page, BrowserContext

@dataclass
class ListingConfig:
    name: str
    url: str
    tagline: str
    description_short: str
    description_long: str
    category: str
    pricing_model: str
    pricing_tiers: str
    contact_email: str
    contact_name: str
    twitter: str
    linkedin: str
    github: str
    logo_path: Optional[str] = None
    screenshot_path: Optional[str] = None
    npm_package: Optional[str] = None
    pypi_package: Optional[str] = None
    smithery_yaml_path: Optional[str] = None
    agent_framework: Optional[str] = None
    agent_category: Optional[str] = None

class SubmissionTracker:
    ICONS = {"SUBMITTED": "✅", "LIVE": "🟢", "FAILED": "❌",
             "MANUAL": "🔧", "SKIPPED": "⏸", "PENDING": "⏳"}

    def __init__(self, output_path: str):
        self.path = Path(output_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.entries: dict[str, dict] = {}

    def update(self, platform: str, status: str, url: str = "", notes: str = ""):
        self.entries[platform] = {"status": status, "url": url, "notes": notes}
        self._write()
        icon = self.ICONS.get(status, "")
        print(f"  {icon} {platform}: {status}" + (f" — {notes}" if notes else ""))

    def _write(self):
        lines = [
            "# Listing Tracker\n",
            f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n",
            "| Platform | Status | URL | Notes |\n",
            "|----------|--------|-----|-------|\n",
        ]
        for name, e in self.entries.items():
            icon = self.ICONS.get(e["status"], "")
            lines.append(f"| {name} | {icon} {e['status']} | {e['url']} | {e['notes']} |\n")
        self.path.write_text("".join(lines))

def load_config(path: str) -> ListingConfig:
    data = yaml.safe_load(Path(path).read_text())
    fields = {f for f in ListingConfig.__dataclass_fields__}
    filtered = {k: v for k, v in data.items() if k in fields}
    for f, fi in ListingConfig.__dataclass_fields__.items():
        if fi.default is not fi.default_factory and f not in filtered:  # type: ignore
            filtered[f] = fi.default
    return ListingConfig(**filtered)

async def run_batch(context: BrowserContext, batch: list[tuple[str, Callable]], cfg: ListingConfig, tracker: SubmissionTracker, dry_run: bool):
    if dry_run:
        for name, _ in batch:
            tracker.update(name, "SKIPPED", notes="dry-run")
        return
    tasks = []
    for name, fn in batch:
        page = await context.new_page()
        tasks.append(fn(page, cfg, tracker))
    results = await asyncio.gather(*tasks, return_exceptions=True)
    for (name, _), result in zip(batch, results):
        if isinstance(result, Exception):
            tracker.update(name, "FAILED", notes=f"Unhandled: {str(result)[:80]}")
```

### Block 2 — MCP Platform Scripts (save as `~/.claude/scripts/list_mcp_auto.py`)

```python
#!/usr/bin/env python3
"""
MCP Server Listing Automation — 50 platforms
Usage: python list_mcp_auto.py --config listing-config.yaml [--dry-run] [--platforms p1,p2]
Requires: pip install playwright pyyaml && playwright install chromium
"""
import asyncio, subprocess, sys, argparse
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright, Page

# Import base (expects listing_base.py in same dir or ~/.claude/scripts/)
sys.path.insert(0, str(Path.home() / ".claude/scripts"))
from listing_base import ListingConfig, SubmissionTracker, load_config, run_batch


# ── Automatable platforms ────────────────────────────────────────────────────

async def submit_future_tools(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """futuretools.io — 7-field form, no login, confirmed working"""
    p = "Future Tools"
    tracker.update(p, "PENDING")
    try:
        await page.goto("https://www.futuretools.io/submit-a-tool", wait_until="domcontentloaded", timeout=20000)
        await page.locator('input').nth(0).fill(cfg.contact_name)          # Your Name
        await page.locator('input').nth(1).fill(cfg.name)                  # Tool Name
        await page.locator('input[type="url"], input').nth(2).fill(cfg.url) # Tool URL
        await page.locator('textarea').first.fill(cfg.description_short)
        # Pricing radio — Free
        free_btn = page.locator('label:has-text("Free"), input[value="Free"]').first
        if await free_btn.count() > 0:
            await free_btn.click()
        await page.locator('input[type="email"]').fill(cfg.contact_email)
        await page.locator('button[type="submit"], input[type="submit"]').click()
        await page.wait_for_selector('text=/review|thank|submit/i', timeout=15000)
        tracker.update(p, "SUBMITTED", "https://www.futuretools.io", "Pending Matt's review")
    except Exception as e:
        tracker.update(p, "FAILED", notes=str(e)[:120])

async def submit_toptools_ai(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """toptools.ai — 3-field form, no login"""
    p = "TopTools.AI"
    tracker.update(p, "PENDING")
    try:
        await page.goto("https://toptools.ai/submit", wait_until="domcontentloaded", timeout=20000)
        await page.locator('input[name*="tool"], input[placeholder*="name" i]').first.fill(cfg.name)
        await page.locator('input[type="url"], input[name*="url" i]').first.fill(cfg.url)
        await page.locator('input[type="email"]').fill(cfg.contact_email)
        await page.locator('button[type="submit"]').click()
        await page.wait_for_selector('text=/thank|submit|success/i', timeout=15000)
        tracker.update(p, "SUBMITTED", "https://toptools.ai")
    except Exception as e:
        tracker.update(p, "FAILED", notes=str(e)[:120])

async def submit_insidr(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """insidr.ai — Tally iframe form, no login"""
    p = "Insidr.ai"
    tracker.update(p, "PENDING")
    try:
        await page.goto("https://www.insidr.ai/submit-tools/", wait_until="domcontentloaded", timeout=20000)
        # Tally forms use iframe or embedded form
        tally = page.frame_locator('iframe[src*="tally"]').first
        await tally.locator('input[name*="tool"], input').nth(0).fill(cfg.name)
        await tally.locator('input[type="url"], input').nth(1).fill(cfg.url)
        await tally.locator('textarea').first.fill(cfg.description_short)
        await tally.locator('input[type="email"]').fill(cfg.contact_email)
        await tally.locator('button[type="submit"]').click()
        await page.wait_for_timeout(3000)
        tracker.update(p, "SUBMITTED", "https://www.insidr.ai")
    except Exception as e:
        tracker.update(p, "FAILED", notes=str(e)[:120])

async def submit_launchingnext(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """launchingnext.com — direct form, no login. Has anti-spam: 'What is 2+3?' → '5'"""
    p = "LaunchingNext"
    tracker.update(p, "PENDING")
    try:
        await page.goto("https://www.launchingnext.com/submit/", wait_until="domcontentloaded", timeout=20000)
        await page.locator('input[name="startupName"], input[name*="name"]').first.fill(cfg.name)
        await page.locator('input[name="startupURL"], input[type="url"]').first.fill(cfg.url)
        desc = page.locator('textarea[name*="desc"], textarea[name="description"], textarea').first
        await desc.fill(cfg.description_short)
        email = page.locator('input[type="email"]').first
        await email.fill(cfg.contact_email)
        # Anti-spam field: "What is 2+3?" — answer is always "5"
        antispam = page.locator('input[name*="spam"], input[name*="antispam"], input[placeholder*="2+3"], input[placeholder*="spam"]')
        if await antispam.count() > 0:
            await antispam.first.fill("5")
        await page.locator('button[type="submit"], input[type="submit"]').click()
        await page.wait_for_selector('text=/submit|thank|success|review/i', timeout=15000)
        tracker.update(p, "SUBMITTED", "https://www.launchingnext.com")
    except Exception as e:
        tracker.update(p, "FAILED", notes=str(e)[:120])

async def submit_uneed(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """uneed.best — REQUIRES LOGIN (verified live). Submit manually after account login."""
    p = "Uneed.best"
    tracker.update(p, "MANUAL", "https://www.uneed.best/submit-a-tool",
        "Login required — create account at uneed.best then submit at /submit-a-tool")

async def submit_betalist(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """betalist.com — REQUIRES LOGIN (verified live). Submit manually."""
    p = "BetaList"
    tracker.update(p, "MANUAL", "https://betalist.com/submit",
        "Login required — sign up / log in at betalist.com first, then submit")

async def submit_toolpilot(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """toolpilot.ai — JotForm, no login. Note: add backlink to toolpilot.ai on your site"""
    p = "ToolPilot.ai"
    tracker.update(p, "PENDING")
    try:
        await page.goto("https://form.jotform.com/231772738321053", wait_until="networkidle", timeout=30000)
        await page.locator('input[id*="name"]').nth(0).fill(cfg.contact_name)
        company_f = page.locator('input[id*="company"]')
        if await company_f.count() > 0:
            await company_f.fill("Misar AI")
        await page.locator('input[type="email"]').fill(cfg.contact_email)
        await page.locator('input[id*="toolname"], input[id*="tool_name"]').fill(cfg.name)
        await page.locator('input[id*="toolurl"], input[id*="tool_url"], input[type="url"]').fill(cfg.url)
        desc = page.locator('textarea').first
        await desc.fill(cfg.description_short)
        platform_checkbox = page.locator('label:has-text("Web")')
        if await platform_checkbox.count() > 0:
            await platform_checkbox.click()
        # Pricing: Free
        free_opt = page.locator('label:has-text("Free")').first
        if await free_opt.count() > 0:
            await free_opt.click()
        # Terms
        terms = page.locator('input[type="checkbox"]').last
        if await terms.count() > 0 and not await terms.is_checked():
            await terms.click()
        await page.locator('button[type="submit"], input[type="submit"]').click()
        await page.wait_for_selector('text=/thank|submit/i', timeout=20000)
        tracker.update(p, "SUBMITTED", "https://www.toolpilot.ai")
    except Exception as e:
        tracker.update(p, "FAILED", notes=str(e)[:120])

async def submit_aitoolhunt(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """aitoolhunt.com — SITE DOWN (verified: 522 Cloudflare error)"""
    p = "AI Tool Hunt"
    tracker.update(p, "MANUAL", "https://www.aitoolhunt.com/submit",
        "Site returns 522 Cloudflare error — check if recovered before attempting")

async def submit_listmyai(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """listmyai.net — PAID €49 via Stripe (verified live)"""
    p = "ListMyAI"
    tracker.update(p, "MANUAL", "https://listmyai.net/submit-ai-tools/",
        "Paid listing €49 Stripe — submit manually and pay on site")

async def submit_easywithai(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """easywithai.com — blocked by Cloudflare bot protection (verified)"""
    p = "Easy With AI"
    tracker.update(p, "MANUAL", "https://easywithai.com/submit-tool/",
        "Cloudflare bot challenge blocks automation — submit manually in a regular browser")

async def submit_mcp_so(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """mcp.so — 3-field form (Type, Name, GitHub URL). Verified live DOM."""
    p = "MCP.so"
    tracker.update(p, "PENDING")
    try:
        await page.goto("https://mcp.so/submit", wait_until="domcontentloaded", timeout=20000)
        # Type selector: "MCP Server" is default selected
        type_select = page.locator('select').first
        if await type_select.count() > 0:
            await type_select.select_option("MCP Server")
        # Name field (verified: textbox with placeholder "Input the name of...")
        await page.locator('input[placeholder*="name"]').first.fill(cfg.name)
        # URL field (verified: textbox with placeholder "https://github.com/...")
        github_url = cfg.github or cfg.url
        await page.locator('input[placeholder*="github"]').first.fill(github_url)
        # Server Config JSON (optional)
        config_field = page.locator('textarea[placeholder*="mcpServers"]')
        if await config_field.count() > 0 and cfg.smithery_yaml_path:
            config_json = f'{{"mcpServers": {{"{cfg.name.lower().replace(" ", "-")}": {{"command": "npx", "args": ["{cfg.npm_package or cfg.name.lower()}"]}}}}}}'
            await config_field.fill(config_json)
        await page.locator('button:has-text("Submit")').click()
        await page.wait_for_timeout(3000)
        tracker.update(p, "SUBMITTED", "https://mcp.so", "May require account verification after submit")
    except Exception as e:
        tracker.update(p, "FAILED", notes=str(e)[:120])

async def submit_dev_to(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """dev.to — Show DEV post, Google OAuth login"""
    p = "Dev.to"
    tracker.update(p, "PENDING")
    try:
        await page.goto("https://dev.to/enter", wait_until="domcontentloaded", timeout=20000)
        # Sign in with GitHub (more reliable than Google on dev.to)
        gh_btn = page.locator('a:has-text("GitHub"), button:has-text("GitHub")')
        if await gh_btn.count() > 0:
            tracker.update(p, "MANUAL", "https://dev.to/new", "Login with GitHub first, then post Show DEV")
            return
        title = f"Show DEV: {cfg.name} — MCP Server for Claude"
        npm_pkg = cfg.npm_package or cfg.name.lower().replace(' ', '-')
        npm_url = f"https://npmjs.com/package/{cfg.npm_package}" if cfg.npm_package else cfg.url
        body = (
            f"I built **{cfg.name}**, an MCP server that {cfg.description_short.lower()}\n\n"
            f"## What it does\n{cfg.description_long}\n\n"
            f"## Install\n\n    npx {npm_pkg} --help\n\n"
            f"Or add to Claude Code .mcp.json:\n"
            f'    {{"name": "{cfg.name}", "command": "npx", "args": ["{npm_pkg}"]}}\n\n'
            f"**Links:** [GitHub]({cfg.github}) | [npm]({npm_url})\n"
        )
        await page.goto("https://dev.to/new", wait_until="domcontentloaded", timeout=20000)
        await page.locator('#article_title, [data-testid="title"]').fill(title)
        await page.locator('#article_body, [data-testid="editor"]').fill(body)
        await page.locator('#article_tags, [placeholder*="tag" i]').fill("mcp, claude, ai, devtools")
        # Don't auto-publish — let user review
        tracker.update(p, "MANUAL", "https://dev.to/new", "Draft created — review and publish manually")
    except Exception as e:
        tracker.update(p, "FAILED", notes=str(e)[:120])

async def submit_software_suggest(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """softwaresuggest.com — work email required (use gulshan@promo.misar.io)"""
    p = "Software Suggest"
    tracker.update(p, "PENDING")
    try:
        await page.goto("https://www.softwaresuggest.com/vendors", wait_until="domcontentloaded", timeout=20000)
        await page.locator('input[name*="name"], input[placeholder*="name" i]').nth(0).fill(cfg.contact_name)
        await page.locator('input[type="email"]').fill(cfg.contact_email)
        org = page.locator('input[name*="org"], input[name*="company"]')
        if await org.count() > 0:
            await org.fill("Misar AI")
        phone = page.locator('input[type="tel"]')
        if await phone.count() > 0:
            await phone.fill("+919999999999")
        await page.locator('input[type="url"], input[name*="website"]').fill(cfg.url)
        await page.locator('button[type="submit"]').click()
        await page.wait_for_selector('text=/thank|submit|success/i', timeout=15000)
        tracker.update(p, "SUBMITTED", "https://www.softwaresuggest.com")
    except Exception as e:
        tracker.update(p, "FAILED", notes=str(e)[:120])

async def submit_feedough(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """feedough.com — 22-step Formaloo iframe (complex multi-step)"""
    p = "Feedough"
    tracker.update(p, "PENDING")
    try:
        await page.goto("https://www.feedough.com/submit-your-startup/", wait_until="networkidle", timeout=30000)
        frame = page.frame_locator('iframe[src*="formaloo"]').first
        # Step 1: Full name
        name_field = frame.locator('input[type="text"]').first
        await name_field.fill(cfg.contact_name)
        await frame.locator('button:has-text("Next"), button:has-text("Continue")').click()
        await page.wait_for_timeout(1000)
        # Step 2: Startup name
        await frame.locator('input[type="text"]').first.fill(cfg.name)
        await frame.locator('button:has-text("Next"), button:has-text("Continue")').click()
        await page.wait_for_timeout(800)
        # Step 3: Position
        await frame.locator('input[type="text"]').first.fill("Founder")
        await frame.locator('button:has-text("Next"), button:has-text("Continue")').click()
        await page.wait_for_timeout(800)
        # Step 4: Email
        await frame.locator('input[type="email"]').first.fill(cfg.contact_email)
        await frame.locator('button:has-text("Next"), button:has-text("Continue")').click()
        await page.wait_for_timeout(800)
        # Note: Steps 5–21 require manual completion — trigger MANUAL
        tracker.update(p, "MANUAL", "https://www.feedough.com/submit-your-startup/", "Steps 1-4 filled, complete 5-21 manually")
    except Exception as e:
        tracker.update(p, "FAILED", notes=str(e)[:120])

async def submit_github_topics(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """GitHub repo topics — non-browser, uses note for user to add manually"""
    p = "GitHub Topics"
    # Extract repo from github URL
    repo_url = cfg.github.rstrip("/")
    topics = "mcp-server model-context-protocol claude-mcp anthropic"
    tracker.update(p, "MANUAL", repo_url,
        f"Add topics: {topics} — go to {repo_url} > ⚙️ > Topics")

async def submit_npm_publish(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """npm publish — CLI, not browser. Runs subprocess."""
    p = "npm (publish)"
    import subprocess, shutil
    tracker.update(p, "PENDING")
    if not cfg.npm_package:
        tracker.update(p, "SKIPPED", notes="npm_package not set in config")
        return
    if not shutil.which("npm"):
        tracker.update(p, "MANUAL", "https://npmjs.com", "npm not found — run: npm publish --access public")
        return
    result = subprocess.run(["npm", "publish", "--access", "public", "--dry-run"],
                            capture_output=True, text=True)
    if result.returncode == 0:
        tracker.update(p, "MANUAL", f"https://npmjs.com/package/{cfg.npm_package}",
                      "Dry-run OK — run: npm publish --access public (without --dry-run)")
    else:
        tracker.update(p, "FAILED", notes=result.stderr[:120])


# ── Manual platforms (with instructions) ─────────────────────────────────────

MANUAL_PLATFORMS = [
    ("Smithery", "Visit smithery.ai → Submit Server → connect GitHub repo + add smithery.yaml"),
    ("Glama.ai/mcp", "Visit glama.ai/mcp → Add Server → GitHub OAuth"),
    ("PulseMCP", "Email founders@pulsemcp.com with: name, URL, description, GitHub repo"),
    ("mcpservers.org", "PR: fork github.com/mcpservers/mcpservers.org → add to servers.json"),
    ("awesome-mcp-servers", "PR: fork modelcontextprotocol/servers → add to README.md"),
    ("Cursor Directory", "Visit cursor.directory → Submit → GitHub OAuth"),
    ("Uneed.best", "LOGIN REQUIRED — sign up at uneed.best then submit at uneed.best/submit-a-tool"),
    ("BetaList", "LOGIN REQUIRED — sign up at betalist.com then submit at betalist.com/submit"),
    ("AI Tool Hunt", "SITE DOWN (522 error) — retry after checking site recovery"),
    ("ListMyAI", "PAID €49 — submit manually at listmyai.net/submit-ai-tools/ and pay via Stripe"),
    ("Easy With AI", "CLOUDFLARE BLOCK — submit manually in a regular browser at easywithai.com/submit-tool/"),
    ("Dang.ai", "PAID ($29) or free with backlink badge — dang.ai/submit → fill form + reCAPTCHA"),
    ("TAAFT", "PAID ($49–$347) — theresanaiforthat.com/launch/ → select package → Stripe payment"),
    ("OpenTools.ai", "LOGIN REQUIRED — opentools.ai/friends/launch-tool → sign in first"),
    ("Product Hunt", "Visit producthunt.com/posts/new → full launch strategy needed"),
    ("Reddit r/ClaudeAI", "Post in r/ClaudeAI: 'Show r/ClaudeAI: [Name] - MCP server that...'"),
    ("Hacker News", "Show HN: needs karma ≥ 10 — submit at news.ycombinator.com/submit"),
    ("SaaSHub", "Login at saashub.com/services/submit (password reset may be needed)"),
    ("AlternativeTo", "Email signup at alternativeto.net — Cloudflare blocks automation"),
    ("LinkedIn", "Post: 'Just launched [Name], an MCP server for Claude that...' + article"),
    ("VS Code Marketplace", "Requires VSIX extension — vsce publish (if applicable)"),
    ("Fazier", "LOGIN REQUIRED — fazier.com/submit → create account → embed badge on site first"),
    ("Startup Ranking", "startupranking.com → Google OAuth → fill all fields (300+ char description)"),
    ("Peerlist", "peerlist.io/user/projects/add-project → Google OAuth"),
    ("F6S", "f6s.com → Google OAuth → Add Company"),
    ("Indie Hackers", "indiehackers.com/products → Google OAuth (use incognito to avoid OAuth conflict)"),
]


# ── Orchestrator ──────────────────────────────────────────────────────────────

AUTOMATABLE = [
    ("future_tools", submit_future_tools),
    ("toptools_ai", submit_toptools_ai),
    ("insidr", submit_insidr),
    ("launchingnext", submit_launchingnext),
    ("mcp_so", submit_mcp_so),
    ("toolpilot", submit_toolpilot),
    ("uneed", submit_uneed),           # reports MANUAL — login required
    ("betalist", submit_betalist),     # reports MANUAL — login required
    ("aitoolhunt", submit_aitoolhunt), # reports MANUAL — site down
    ("listmyai", submit_listmyai),     # reports MANUAL — paid €49
    ("easywithai", submit_easywithai), # reports MANUAL — Cloudflare block
    ("dev_to", submit_dev_to),
    ("software_suggest", submit_software_suggest),
    ("feedough", submit_feedough),
    ("github_topics", submit_github_topics),
    ("npm_publish", submit_npm_publish),
]

async def main():
    parser = argparse.ArgumentParser(description="MCP Server Listing Automation")
    parser.add_argument("--config", default="listing-config.yaml")
    parser.add_argument("--dry-run", action="store_true", help="Print only, no submissions")
    parser.add_argument("--platforms", default="", help="Comma-separated platform keys")
    args = parser.parse_args()

    cfg = load_config(args.config)
    date_str = datetime.now().strftime("%Y%m%d-%H%M")
    tracker = SubmissionTracker(f"output/mcp-listings-{date_str}.md")

    platforms = AUTOMATABLE
    if args.platforms:
        keys = set(args.platforms.split(","))
        platforms = [(n, f) for n, f in AUTOMATABLE if n in keys]

    print(f"\n🚀 MCP Listing Automation — {cfg.name}")
    print(f"   URL: {cfg.url}")
    print(f"   Platforms: {len(platforms)} automatable + {len(MANUAL_PLATFORMS)} manual\n")

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=False)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )
        for i in range(0, len(platforms), 4):
            batch = platforms[i:i+4]
            await run_batch(context, batch, cfg, tracker, args.dry_run)
            await asyncio.sleep(2)
        await browser.close()

    print(f"\n🔧 Manual platforms ({len(MANUAL_PLATFORMS)}) — complete these yourself:")
    for name, instruction in MANUAL_PLATFORMS:
        print(f"  • {name}: {instruction}")
    print(f"\n📋 Tracker saved to: output/mcp-listings-{date_str}.md")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Config Template (`listing-config.yaml`)

```yaml
# MCP Server listing config — fill all fields before running
name: "@misarblog/mcp"
url: "https://github.com/misaradmin/misarblog-mcp"
tagline: "MCP server for Misar.Blog — manage blog posts via Claude"
description_short: "Publish, edit, and manage Misar.Blog articles directly from Claude using 12 MCP tools."
description_long: |
  @misarblog/mcp is a Model Context Protocol server that connects Claude to Misar.Blog.
  Features: create/edit/publish/delete articles, manage categories and tags, generate
  SEO titles, upload media, and manage author profiles — all from your Claude conversation.
  Works with Claude Desktop, Claude Code, Cursor, and any MCP-compatible client.
category: "Developer Tools"
pricing_model: "Free"
pricing_tiers: "Free"
contact_email: "gulshan@promo.misar.io"
contact_name: "Gulshan Yadav"
twitter: "@mrgulshanyadav"
linkedin: "linkedin.com/in/mrgulshanyadav"
github: "https://github.com/misaradmin"
logo_path: "./assets/logo.png"
screenshot_path: "./assets/screenshot.png"
npm_package: "@misarblog/mcp"
pypi_package: ""
smithery_yaml_path: "./smithery.yaml"
```

## Contact Info Template
```
Name: Gulshan Yadav
Email: gulshan@promo.misar.io
Company: Misar AI
Title: Founder
Twitter: @mrgulshanyadav
LinkedIn: linkedin.com/in/mrgulshanyadav
GitHub: github.com/misar-ai
Location: India
Founded: 2024
```
