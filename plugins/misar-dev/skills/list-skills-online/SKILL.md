---
name: list-skills-online
description: Submit Claude Code skills, plugins, and slash commands to 30+ directories, registries, and communities for maximum discoverability. Use when the user wants to list a Claude Code skill online, publish a plugin, get a Claude skill discovered, or mentions "list skill", "publish plugin", "Claude Code skill directory", "skill registry", "slash command listing", "Claude plugin marketplace".
user-invocable: true
argument-hint: "[--config listing-config.yaml] [--dry-run] [--platforms misar_plugins,github_topics,...]"
---

# List Skills Online

Automated submission of Claude Code skills, plugins, slash commands, and hooks to 30+ directories ranked by Claude developer community reach. Covers skill registries, developer platforms, AI tool directories, and community channels.

## When to Trigger

- User says "list skill online", "publish Claude plugin", "submit skill to directories", "get my Claude skill discovered"
- User invokes `/list-skills-online`
- User mentions Claude Code plugin marketplace, awesome-claude-skills, skill registry, misar-ai-plugins

## Execution Protocol

### Phase 1: Preparation

1. Read skill/plugin details from user input or project context (name, GitHub repo, description, skill type: skill/command/hook/agent)
2. Create tracking file at `output/skills-listings-tracker-{date}.md`
3. Each entry tracks: Platform | Status | URL | Notes

### Phase 2: Submission (Per Directory)

For EACH directory below:
1. **Navigate** to submission page or repository
2. **Detect** method: form → fill; GitHub PR → open PR; community post → draft post; CLI → run command
3. **Fill** completely; submit; verify
4. **Update** tracker immediately

### Phase 3: Parallel Batches

- Up to 4 browser-based submissions in parallel
- GitHub API (PR, topics) run first via CLI/API
- Print MANUAL list at end with exact instructions

---

## Top 30 Claude Skill Directories (Ranked by Developer Reach)

| # | Platform | Submit URL | Type | Reach |
|---|----------|-----------|------|-------|
| 1 | misar-ai-plugins | git.misar.io/misaradmin/misar-ai-plugins | PRIMARY registry | Misar.Dev marketplace |
| 2 | Claude Code Plugin Registry | github.com/anthropics/claude-code | GitHub PR | Official Claude Code |
| 3 | awesome-claude-code-skills | GitHub (search) | GitHub PR | Community awesome-list |
| 4 | GitHub Topics | github.com | Repo topics | claude-skill, claude-code |
| 5 | Claude Discord #showcase | discord.gg/anthropic | Community post | High-engagement |
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
| 16 | LaunchingNext | launchingnext.com/submit | Launch directory | 350K+ |
| 17 | Fazier | fazier.com/submit | Launch platform | 800K+ |
| 18 | Feedough | feedough.com/submit-your-startup | Startup directory | 800K+ |
| 19 | F6S | f6s.com/company/new | Startup platform | 500K+ |
| 20 | TopTools.AI | toptools.ai/submit | AI directory | 400K+ |
| 21 | Insidr.ai | insidr.ai/submit-tools | AI directory | 150K+ |
| 22 | Future Tools | futuretools.io/submit-a-tool | AI directory | 2M+ |
| 23 | There's An AI For That | theresanaiforthat.com/submit | AI directory | 2M+ |
| 24 | Dang.ai | dang.ai/submit | AI directory | 300K+ |
| 25 | ListMyAI | listmyai.net/submit-ai-tools | AI directory | 200K+ |
| 26 | AI Tool Hunt | aitoolhunt.com/submit | AI directory | 150K+ |
| 27 | OpenTools.ai | opentools.ai | AI directory | 400K+ |
| 28 | Medium | medium.com/new-story | Blog article | 100M+ readers |
| 29 | LinkedIn | linkedin.com | Article/post | B2B audience |
| 30 | Twitter/X thread | x.com | Thread | Viral reach |

---

## Per-Platform Submission Steps

### 1. misar-ai-plugins (git.misar.io) — PRIMARY
- **Method:** GitHub PR to misaradmin/misar-ai-plugins
- **Directory structure:**
  ```
  plugins/misar-dev/skills/<skill-name>/SKILL.md
  plugins/misar-dev/commands/<skill-name>.md   (optional)
  plugins/misar-dev/agents/<agent-name>/agent.md (optional)
  ```
- **PR title:** `feat(skills): add <skill-name> skill`
- **Steps:** Fork → add skill files → PR to develop branch
- **Notes:** This is the canonical home for misar-dev plugin skills. Gets distributed to all misar-ai-plugins users.

### 2. Claude Code Plugin Registry (github.com/anthropics)
- **Method:** GitHub PR or discussions
- **Steps:** Check github.com/anthropics/claude-code for community examples → open PR or discussion
- **Notes:** Official Anthropic repo — high visibility if accepted

### 3. awesome-claude-code-skills (GitHub)
- **Method:** Search GitHub for "awesome-claude-code" or "awesome-claude-skills" → PR
- **Steps:** Find most-starred list → Fork → Add entry: `- [Skill Name](URL) - Description`
- **Notes:** Community-maintained, check for most-active repo first

### 4. GitHub Topics
- **Method:** Add topics to your skill's GitHub repo
- **Topics to add:** `claude-skill`, `claude-code-skill`, `claude-code-plugin`, `claude-code`, `anthropic`
- **Steps:** Repo → ⚙️ (gear icon near About) → Topics → add all → Save

### 5. Claude Discord #showcase
- **Method:** Post in Claude community Discord
- **Steps:** discord.gg/anthropic → Find #showcase or #tools → Post message:
  ```
  🔧 New Claude Code skill: [Name]
  What it does: [description]
  Install: /list-skills-online or [GitHub link]
  ```
- **Notes:** High engagement, Claude team often notices good skills

### 6. Reddit r/ClaudeAI
- **Auth:** Reddit account
- **Steps:** reddit.com/r/ClaudeAI/submit → "Show r/ClaudeAI" flair → Title: "Show r/ClaudeAI: [Skill Name] — [tagline]" → Body with demo, install steps, link
- **Notes:** Strong community for Claude tools. Add screenshots/demo GIF for more upvotes.

### 7. Dev.to (Show DEV)
- **Auth:** GitHub OAuth
- **Steps:** dev.to/new → Title: "Show DEV: [Skill Name] for Claude Code" → Tags: `claude`, `ai`, `devtools`, `showdev` → Markdown body with install + demo → Publish
- **Notes:** 7M+ developers. Good for tutorial-style posts showing the skill in action.

### 8. Hacker News Show HN
- **Auth:** HN account (mrgulshanyadav, karma=1 — needs ≥10)
- **Steps:** news.ycombinator.com/submit → Title: "Show HN: [Skill Name] – [one-line description]" → URL → Text: technical context
- **Blocker:** Karma ≥ 10 required. Build karma by commenting first.

### 9. Hashnode
- **Auth:** GitHub OAuth
- **Steps:** hashnode.com → New Story → Write technical post: "Building [Skill Name] for Claude Code" → Publish → Cross-post to dev.to
- **Notes:** Good for longer tutorial posts with code examples

### 10. Reddit r/artificial
- **Auth:** Reddit account
- **Steps:** reddit.com/r/artificial/submit → "Project" or "Tool" flair → Link post to GitHub or demo

### 11. Product Hunt
- **Auth:** Product Hunt account
- **Steps:** producthunt.com/posts/new → Upload logo → Name + tagline + URL → Topics: "Developer Tools", "Artificial Intelligence" → Schedule launch
- **Notes:** Coordinate launch day for upvotes. One launch only.

### 12. Peerlist
- **Auth:** Google OAuth (mryadavgulshan@gmail.com)
- **Steps:** peerlist.io → Sign in → /user/projects/add-project → Name + URL + tagline + description → Save

### 13. npm registry
- **Method:** CLI publish (if packaged as npm module)
- **Steps:** Add keywords: `["claude-code-skill", "claude-skill", "claude-plugin"]` → `npm publish --access public`
- **Notes:** Only relevant if your skill is distributed as a package

### 14–30. Form-based directories
Use the same protocol as documented in `list-tools-online` skill. Key fields:
- **Name**: Skill name
- **URL**: GitHub repo or demo page
- **Description**: What the skill does in Claude Code
- **Category**: Developer Tools / AI Assistant / Productivity
- **Pricing**: Free (open source)

---

## Automation Scripts (Python + Playwright)

### Prerequisites
```bash
pip install playwright pyyaml
playwright install chromium
```

### Run Instructions
```bash
# Save listing_base.py from list-mcp-online skill to ~/.claude/scripts/
# Save block below to ~/.claude/scripts/list_skills_auto.py
python ~/.claude/scripts/list_skills_auto.py --config listing-config.yaml
python ~/.claude/scripts/list_skills_auto.py --config listing-config.yaml --dry-run
python ~/.claude/scripts/list_skills_auto.py --config listing-config.yaml --platforms "future_tools,toptools_ai,uneed"
```

### Block — Skills Platform Scripts (save as `~/.claude/scripts/list_skills_auto.py`)

```python
#!/usr/bin/env python3
"""
Claude Code Skill Listing Automation — 30 platforms
Usage: python list_skills_auto.py --config listing-config.yaml [--dry-run] [--platforms p1,p2]
Requires: pip install playwright pyyaml && playwright install chromium
Also requires: listing_base.py in ~/.claude/scripts/
"""
import asyncio, sys, argparse
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright, Page

sys.path.insert(0, str(Path.home() / ".claude/scripts"))
from listing_base import ListingConfig, SubmissionTracker, load_config, run_batch


# ── Automatable platforms ────────────────────────────────────────────────────

async def submit_future_tools(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """futuretools.io — 7-field form"""
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
        await page.locator('input[name*="tool"], input[placeholder*="name" i]').first.fill(cfg.name)
        await page.locator('input[type="url"]').first.fill(cfg.url)
        await page.locator('input[type="email"]').fill(cfg.contact_email)
        await page.locator('button[type="submit"]').click()
        await page.wait_for_selector('text=/thank|success/i', timeout=15000)
        tracker.update(p, "SUBMITTED", "https://toptools.ai")
    except Exception as e:
        tracker.update(p, "FAILED", notes=str(e)[:120])

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
    """launchingnext.com — direct form, no login. Has anti-spam: 'What is 2+3?' → '5'"""
    p = "LaunchingNext"
    tracker.update(p, "PENDING")
    try:
        await page.goto("https://www.launchingnext.com/submit/", wait_until="domcontentloaded", timeout=20000)
        await page.locator('input[name="startupName"], input[name*="name"]').first.fill(cfg.name)
        await page.locator('input[name="startupURL"], input[type="url"]').first.fill(cfg.url)
        await page.locator('textarea').first.fill(cfg.description_short)
        await page.locator('input[type="email"]').fill(cfg.contact_email)
        antispam = page.locator('input[name*="spam"], input[name*="antispam"], input[placeholder*="2+3"]')
        if await antispam.count() > 0:
            await antispam.first.fill("5")
        await page.locator('button[type="submit"], input[type="submit"]').click()
        await page.wait_for_selector('text=/submit|thank|review/i', timeout=15000)
        tracker.update(p, "SUBMITTED", "https://www.launchingnext.com")
    except Exception as e:
        tracker.update(p, "FAILED", notes=str(e)[:120])

async def submit_uneed(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """uneed.best — REQUIRES LOGIN (verified live)"""
    p = "Uneed.best"
    tracker.update(p, "MANUAL", "https://www.uneed.best/submit-a-tool",
        "Login required — create account at uneed.best then submit at /submit-a-tool")

async def submit_betalist(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """betalist.com — REQUIRES LOGIN (verified live)"""
    p = "BetaList"
    tracker.update(p, "MANUAL", "https://betalist.com/submit",
        "Login required — sign up at betalist.com first, then submit")

async def submit_listmyai(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """listmyai.net — PAID €49 via Stripe (verified live)"""
    p = "ListMyAI"
    tracker.update(p, "MANUAL", "https://listmyai.net/submit-ai-tools/",
        "Paid listing €49 — submit manually and pay via Stripe on site")

async def submit_aitoolhunt(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """aitoolhunt.com — SITE DOWN (verified: 522 Cloudflare error)"""
    p = "AI Tool Hunt"
    tracker.update(p, "MANUAL", "https://www.aitoolhunt.com/submit",
        "Site returns 522 Cloudflare error — check if recovered before attempting")

async def submit_feedough(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """feedough.com — 22-step Formaloo (auto-fills first 4 steps)"""
    p = "Feedough"
    tracker.update(p, "PENDING")
    try:
        await page.goto("https://www.feedough.com/submit-your-startup/", wait_until="networkidle", timeout=30000)
        frame = page.frame_locator('iframe[src*="formaloo"]').first
        await frame.locator('input[type="text"]').first.fill(cfg.contact_name)
        await frame.locator('button:has-text("Next"), button:has-text("Continue")').click()
        await page.wait_for_timeout(800)
        await frame.locator('input[type="text"]').first.fill(cfg.name)
        await frame.locator('button:has-text("Next"), button:has-text("Continue")').click()
        await page.wait_for_timeout(800)
        await frame.locator('input[type="text"]').first.fill("Founder")
        await frame.locator('button:has-text("Next"), button:has-text("Continue")').click()
        await page.wait_for_timeout(800)
        await frame.locator('input[type="email"]').first.fill(cfg.contact_email)
        await frame.locator('button:has-text("Next"), button:has-text("Continue")').click()
        tracker.update(p, "MANUAL", "https://www.feedough.com", "Steps 1-4 filled; complete steps 5-21 manually")
    except Exception as e:
        tracker.update(p, "FAILED", notes=str(e)[:120])

async def submit_github_topics(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """GitHub repo topics — manual instruction"""
    p = "GitHub Topics"
    repo_url = cfg.github.rstrip("/")
    tracker.update(p, "MANUAL", repo_url,
        "Add topics: claude-skill claude-code-plugin claude-code anthropic — go to repo > ⚙️ > Topics")

async def submit_dev_to(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """dev.to — draft Show DEV post"""
    p = "Dev.to"
    tracker.update(p, "PENDING")
    try:
        await page.goto("https://dev.to/new", wait_until="domcontentloaded", timeout=20000)
        title_field = page.locator('#article_title, [data-testid="title"], input[placeholder*="title" i]')
        if await title_field.count() == 0:
            tracker.update(p, "MANUAL", "https://dev.to/new", "Login first, then post Show DEV article")
            return
        title = f"Show DEV: {cfg.name} — Claude Code Skill"
        slug = cfg.name.lower().replace(' ', '-')
        body = (
            f"## What is {cfg.name}?\n\n{cfg.description_long}\n\n"
            f"## Installation\n\nCopy SKILL.md to ~/.claude/skills/{slug}/\n\n"
            f"    # If packaged via misar-ai-plugins:\n"
            f"    /install-skill {slug}\n\n"
            f"## Usage\n\n    /{slug} [args]\n\n"
            f"**GitHub:** {cfg.github}\n"
        )
        await title_field.fill(title)
        body_field = page.locator('#article_body, [data-testid="editor"]')
        if await body_field.count() > 0:
            await body_field.fill(body)
        tags = page.locator('#article_tags, [placeholder*="tag" i]')
        if await tags.count() > 0:
            await tags.fill("claude, ai, devtools, showdev")
        tracker.update(p, "MANUAL", "https://dev.to/new", "Draft pre-filled — login and publish manually")
    except Exception as e:
        tracker.update(p, "FAILED", notes=str(e)[:120])


# ── Manual platforms ──────────────────────────────────────────────────────────

MANUAL_PLATFORMS = [
    ("misar-ai-plugins", "PR to git.misar.io/misaradmin/misar-ai-plugins → plugins/misar-dev/skills/<name>/SKILL.md"),
    ("Claude Code Registry", "Check github.com/anthropics/claude-code for community submission process"),
    ("awesome-claude-skills", "Search GitHub 'awesome-claude-code-skills' → PR to most-starred repo"),
    ("Claude Discord #showcase", "discord.gg/anthropic → #showcase → Post skill announcement with GitHub link"),
    ("Reddit r/ClaudeAI", "reddit.com/r/ClaudeAI/submit → 'Show r/ClaudeAI' flair → title + description + link"),
    ("Reddit r/artificial", "reddit.com/r/artificial/submit → Project flair → link to GitHub/demo"),
    ("Hacker News", "news.ycombinator.com/submit → 'Show HN: [Name]' — requires karma ≥ 10"),
    ("Product Hunt", "producthunt.com/posts/new → full launch (logo, screenshots, Hunter strategy needed)"),
    ("Hashnode", "hashnode.com → New Story → Technical tutorial showing skill in action"),
    ("F6S", "f6s.com → Google OAuth → Add Company/Product"),
    ("Fazier", "fazier.com/submit → embed badge on GitHub README → submit"),
    ("Startup Ranking", "startupranking.com → Google OAuth → fill all fields"),
    ("Peerlist", "peerlist.io/user/projects/add-project → Google OAuth"),
    ("Dang.ai", "Add backlink badge to README/site → dang.ai/submit → form + reCAPTCHA"),
    ("TAAFT", "Add backlink to theresanaiforthat.com on site/README → submit form"),
    ("LinkedIn", "Post: 'Just published [Name], a Claude Code skill that...' + article with demo"),
    ("Twitter/X", "Thread: 'Just built [Name] for Claude Code 🧵' → demo GIFs → GitHub link"),
    ("Medium", "medium.com/new-story → 'Building a Claude Code Skill: [Name]' tutorial"),
    ("npm registry", "Add keywords: claude-code-skill, claude-skill → npm publish --access public"),
]


# ── Orchestrator ──────────────────────────────────────────────────────────────

AUTOMATABLE = [
    ("future_tools", submit_future_tools),
    ("toptools_ai", submit_toptools_ai),
    ("insidr", submit_insidr),
    ("launchingnext", submit_launchingnext),
    ("uneed", submit_uneed),
    ("betalist", submit_betalist),
    ("listmyai", submit_listmyai),
    ("aitoolhunt", submit_aitoolhunt),
    ("feedough", submit_feedough),
    ("github_topics", submit_github_topics),
    ("dev_to", submit_dev_to),
]

async def main():
    parser = argparse.ArgumentParser(description="Claude Skill Listing Automation")
    parser.add_argument("--config", default="listing-config.yaml")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--platforms", default="")
    args = parser.parse_args()

    cfg = load_config(args.config)
    date_str = datetime.now().strftime("%Y%m%d-%H%M")
    tracker = SubmissionTracker(f"output/skills-listings-{date_str}.md")

    platforms = AUTOMATABLE
    if args.platforms:
        keys = set(args.platforms.split(","))
        platforms = [(n, f) for n, f in AUTOMATABLE if n in keys]

    print(f"\n🧩 Claude Skill Listing Automation — {cfg.name}")
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
    print(f"\n📋 Tracker: output/skills-listings-{date_str}.md")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Config Template (`listing-config.yaml`)

```yaml
# Claude Code Skill listing config
name: "my-skill-name"
url: "https://github.com/your-org/your-skill"
tagline: "One-line description of what the skill does in Claude Code (max 80 chars)"
description_short: "Brief description of the skill's purpose and key capabilities (max 160 chars)."
description_long: |
  Full description: what the skill does, when to use it, key features,
  how to install, example usage, and what problems it solves.
category: "Developer Tools"
pricing_model: "Free"
pricing_tiers: "Free (open source)"
contact_email: "gulshan@promo.misar.io"
contact_name: "Gulshan Yadav"
twitter: "@mrgulshanyadav"
linkedin: "linkedin.com/in/mrgulshanyadav"
github: "https://github.com/misar-ai/your-skill"
logo_path: "./assets/logo.png"
screenshot_path: "./assets/screenshot.png"
```

## Contact Info Template
```
Name: Gulshan Yadav
Email: gulshan@promo.misar.io
Company: Misar AI / Misar.Dev
Title: Founder
Twitter: @mrgulshanyadav
LinkedIn: linkedin.com/in/mrgulshanyadav
GitHub: github.com/misar-ai
Location: India
Founded: 2024
```
