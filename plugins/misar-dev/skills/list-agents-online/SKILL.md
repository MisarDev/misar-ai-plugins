---
name: list-agents-online
description: Submit AI agents to 35+ registries, directories, and community platforms for maximum discoverability. Use when the user wants to list an AI agent online, publish an agent to a registry, get an agent discovered, or mentions "list agent", "publish agent", "agent directory", "agent registry", "agent marketplace", "Hugging Face agent", "CrewAI", "LangChain Hub".
user-invocable: true
argument-hint: "[--config listing-config.yaml] [--dry-run] [--platforms huggingface,crewai,agenthub,...]"
---

# List Agents Online

Automated AI agent submission to 35+ registries, directories, and community platforms ranked by agent-ecosystem reach. Covers dedicated agent registries (Hugging Face, LangChain Hub, CrewAI, AgentHub), Claude-specific channels (misar-ai-plugins, Discord), developer communities, and general AI tool directories.

## When to Trigger

- User says "list agent online", "publish agent to registry", "get my agent discovered", "submit agent"
- User invokes `/list-agents-online`
- User mentions Hugging Face Hub, LangChain Hub, AgentHub, CrewAI templates, AutoGen community, awesome-ai-agents

## Execution Protocol

### Phase 1: Preparation

1. Read agent details from user input: name, description, framework (crewai/autogen/langgraph/claude/custom), category (coding/research/marketing/ops/data), GitHub repo, demo URL
2. Create tracking file at `output/agents-listings-tracker-{date}.md`
3. Each entry tracks: Platform | Status | URL | Notes

### Phase 2: Submission (Per Directory)

For EACH directory below:
1. **Navigate** to submission/upload page
2. **Detect** method: web form → fill; GitHub PR → open; CLI push → run command; community post → draft
3. **Fill** all fields; submit; verify
4. **Update** tracker immediately

### Phase 3: Parallel Batches

- CLI-based (Hugging Face Hub, LangChain Hub) run first via subprocess
- Up to 4 browser-based submissions in parallel
- Print MANUAL list at end with exact instructions

---

## Top 35 AI Agent Directories (Ranked by Agent Ecosystem Reach)

| # | Platform | Submit URL | Type | Reach |
|---|----------|-----------|------|-------|
| 1 | Hugging Face Hub | huggingface.co/new | Model/Space registry | PRIMARY — 5M+ models |
| 2 | LangChain Hub | smith.langchain.com/hub | Prompt/agent hub | 10M+ LangChain users |
| 3 | AgentHub.dev | agenthub.dev | Agent directory | Agent-specific |
| 4 | CrewAI Templates | github.com/crewAIInc/crewAI | GitHub PR | CrewAI ecosystem |
| 5 | AutoGen Community | github.com/microsoft/autogen | GitHub PR to examples | Microsoft AutoGen |
| 6 | FlowiseAI Marketplace | flowiseai.com | Form/GitHub | No-code agent builder |
| 7 | Relevance AI | relevanceai.com/templates | Partner form | Agent templates |
| 8 | awesome-ai-agents | github.com/e2b-dev/awesome-ai-agents | GitHub PR | Community list |
| 9 | LlamaIndex Hub | llamahub.ai | CLI push | LlamaIndex ecosystem |
| 10 | E2B.dev | e2b.dev | Form/PR | Sandboxed agents |
| 11 | misar-ai-plugins agents/ | git.misar.io/misaradmin/misar-ai-plugins | PR to agents/ | Own plugin marketplace |
| 12 | Claude.ai agents | claude.ai | Partner form | Official Anthropic |
| 13 | Claude Discord #showcase | discord.gg/anthropic | Post | High engagement |
| 14 | GitHub Topics | github.com | Repo topics | Auto-discover |
| 15 | Product Hunt | producthunt.com/posts/new | Launch | 10M+ |
| 16 | Hacker News Show HN | news.ycombinator.com/submit | Community | 10M+ |
| 17 | Dev.to (Show DEV) | dev.to/new | Tutorial post | 7M+ |
| 18 | Reddit r/ClaudeAI | reddit.com/r/ClaudeAI | Post | Claude community |
| 19 | Reddit r/LLMAgents | reddit.com/r/LLMAgents | Post | Agent-specific |
| 20 | Reddit r/artificial | reddit.com/r/artificial | Post | 2M+ |
| 21 | Hashnode | hashnode.com | Blog post | 5M+ |
| 22 | LinkedIn | linkedin.com | Article/post | B2B |
| 23 | Twitter/X | x.com | Thread | Viral |
| 24 | Peerlist | peerlist.io/user/projects/add-project | Dev network | 300K+ |
| 25 | BetaList | betalist.com/submit | Beta launches | 500K+ |
| 26 | Uneed.best | uneed.best/submit | Tool directory | 700K+ |
| 27 | LaunchingNext | launchingnext.com/submit | Launch directory | 350K+ |
| 28 | Feedough | feedough.com/submit-your-startup | Startup directory | 800K+ |
| 29 | F6S | f6s.com | Startup platform | 500K+ |
| 30 | TopTools.AI | toptools.ai/submit | AI directory | 400K+ |
| 31 | Insidr.ai | insidr.ai/submit-tools | AI directory | 150K+ |
| 32 | Future Tools | futuretools.io/submit-a-tool | AI directory | 2M+ |
| 33 | There's An AI For That | theresanaiforthat.com/submit | AI directory | 2M+ |
| 34 | Dang.ai | dang.ai/submit | AI directory | 300K+ |
| 35 | ListMyAI | listmyai.net/submit-ai-tools | AI directory | 200K+ |

---

## Per-Platform Submission Steps

### 1. Hugging Face Hub — PRIMARY
- **Method:** CLI push or web UI
- **Create Model Card:** `huggingface-cli login` → create repo → push with README.md (model card)
- **Model card minimum:**
  ```markdown
  ---
  tags: [agent, claude, ai-agent, crewai]
  ---
  # Agent Name
  Description...
  ## Usage
  ...
  ```
- **Steps (web):** huggingface.co/new → New Model → Fill name + description → Upload files
- **CLI:**
  ```bash
  huggingface-cli login
  huggingface-cli repo create my-agent-name --type model
  git clone https://huggingface.co/your-org/my-agent-name
  # Add agent files + README.md → git push
  ```
- **Notes:** Add tags: `agent`, `claude`, `mcp`, your framework name. Creates auto-page at huggingface.co/your-org/my-agent-name.

### 2. LangChain Hub (smith.langchain.com/hub)
- **Method:** Python CLI push
- **Steps:**
  ```bash
  pip install langsmith
  export LANGCHAIN_API_KEY="your-api-key"
  python -c "from langsmith import Client; c = Client(); c.push_prompt('your-agent-name', object=agent_runnable, description='...')"
  ```
- **Notes:** Best for LangChain/LangGraph agents. Creates page at smith.langchain.com/hub/org/agent-name.

### 3. AgentHub.dev
- **Auth:** GitHub OAuth
- **Steps:** agenthub.dev → Submit Agent → GitHub OAuth → Name + Description + Framework + GitHub URL + Demo URL → Submit
- **Notes:** Agent-specific directory. Good discoverability with the autonomous agent community.

### 4. CrewAI Templates (github.com/crewAIInc/crewAI)
- **Method:** GitHub PR to examples or templates directory
- **Steps:** Fork crewAIInc/crewAI → Add to `examples/` directory → PR with your agent as a template
- **Notes:** Only for CrewAI framework agents. Good exposure with CrewAI users.

### 5. AutoGen Community (github.com/microsoft/autogen)
- **Method:** GitHub PR or discussion
- **Steps:** Fork microsoft/autogen → Add to `samples/` or `notebooks/` → PR
- **Notes:** Large Microsoft-backed community. Good for complex multi-agent systems.

### 6. FlowiseAI Marketplace
- **Auth:** Account creation
- **Steps:** flowiseai.com → Templates or Marketplace → Submit template → Upload exported flow JSON
- **Notes:** Good for no-code agent builders who use Flowise. Requires exporting your agent as Flowise JSON.

### 7. Relevance AI Templates
- **Auth:** Partner/account form
- **Steps:** relevanceai.com → Tools/Templates → Submit your template form
- **Notes:** Manual review, B2B-focused. Takes ~1 week to review.

### 8. awesome-ai-agents (github.com/e2b-dev/awesome-ai-agents)
- **Method:** GitHub PR
- **Steps:** Fork e2b-dev/awesome-ai-agents → Add entry: `| [Agent Name](URL) | Framework | Description |` → PR
- **Notes:** Widely referenced community list for AI agents. Fast merge.

### 9. LlamaIndex Hub (llamahub.ai)
- **Method:** CLI push
- **Steps:**
  ```bash
  pip install llama-hub
  # Follow llamahub.ai contributor guide
  ```
- **Notes:** Best for LlamaIndex-based agents and tools.

### 10. E2B.dev
- **Auth:** GitHub OAuth
- **Steps:** e2b.dev → Showcase or templates → Submit your sandboxed agent
- **Notes:** E2B provides code execution sandboxes for agents. Good for coding agents.

### 11. misar-ai-plugins agents/
- **Method:** GitHub PR to git.misar.io/misaradmin/misar-ai-plugins
- **Directory:** `plugins/misar-dev/agents/<agent-name>/agent.md`
- **agent.md format:**
  ```markdown
  ---
  name: my-agent
  description: "What it does"
  type: agent
  ---
  # Agent Name
  ...instructions...
  ```
- **Steps:** Fork → add agent file → PR to develop

### 12. Claude.ai agents
- **Auth:** Anthropic partner program
- **Steps:** claude.ai → Settings → Agents (if available) OR email partners@anthropic.com
- **Notes:** Official listing; currently limited to select partners.

### 13–35. See `list-tools-online` + platform-specific steps
Platforms 13–35 follow the same protocol as documented in `list-tools-online` and `list-skills-online` skills.

---

## Automation Scripts (Python + Playwright)

### Prerequisites
```bash
pip install playwright pyyaml huggingface-hub
playwright install chromium
```

### Run Instructions
```bash
# Save listing_base.py from list-mcp-online skill to ~/.claude/scripts/
# Save block below to ~/.claude/scripts/list_agents_auto.py
python ~/.claude/scripts/list_agents_auto.py --config listing-config.yaml
python ~/.claude/scripts/list_agents_auto.py --config listing-config.yaml --dry-run
python ~/.claude/scripts/list_agents_auto.py --config listing-config.yaml --platforms "future_tools,toptools_ai,uneed,agenthub"
```

### Block — Agent Platform Scripts (save as `~/.claude/scripts/list_agents_auto.py`)

```python
#!/usr/bin/env python3
"""
AI Agent Listing Automation — 35 platforms
Usage: python list_agents_auto.py --config listing-config.yaml [--dry-run] [--platforms p1,p2]
Requires: pip install playwright pyyaml huggingface-hub && playwright install chromium
Also requires: listing_base.py in ~/.claude/scripts/
"""
import asyncio, sys, argparse, subprocess, shutil
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright, Page

sys.path.insert(0, str(Path.home() / ".claude/scripts"))
from listing_base import ListingConfig, SubmissionTracker, load_config, run_batch


# ── Automatable platforms ────────────────────────────────────────────────────

async def submit_huggingface(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """Hugging Face Hub — web UI upload (CLI preferred, see MANUAL)"""
    p = "Hugging Face Hub"
    if not shutil.which("huggingface-cli"):
        tracker.update(p, "MANUAL", "https://huggingface.co/new",
            "pip install huggingface-hub && huggingface-cli login && huggingface-cli repo create <name> --type model")
        return
    # If CLI available, guide through steps
    tracker.update(p, "MANUAL", "https://huggingface.co/new",
        "Run: huggingface-cli login && huggingface-cli repo create <name> --type model → push files")

async def submit_agenthub(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """agenthub.dev — DEAD: acquired by Gumloop (verified live, redirects to gumloop.com)"""
    p = "AgentHub.dev"
    tracker.update(p, "SKIP", "https://agenthub.dev",
        "Site acquired by Gumloop — redirects to gumloop.com, no longer an agent directory")

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
        # Anti-spam: "What is 2+3?" → answer "5"
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
    """GitHub repo topics"""
    p = "GitHub Topics"
    repo_url = cfg.github.rstrip("/")
    framework = cfg.agent_framework or "ai-agent"
    category = cfg.agent_category or "automation"
    tracker.update(p, "MANUAL", repo_url,
        f"Add topics: claude-agent ai-agent {framework} {category} anthropic — repo > ⚙️ > Topics")

async def submit_dev_to(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """dev.to — draft Show DEV post"""
    p = "Dev.to"
    tracker.update(p, "PENDING")
    try:
        await page.goto("https://dev.to/new", wait_until="domcontentloaded", timeout=20000)
        title_field = page.locator('#article_title, [data-testid="title"]')
        if await title_field.count() == 0:
            tracker.update(p, "MANUAL", "https://dev.to/new", "Login first, then draft Show DEV post")
            return
        framework = cfg.agent_framework or "Claude"
        title = f"Show DEV: {cfg.name} — AI Agent built with {framework}"
        body = (
            f"## What is {cfg.name}?\n\n{cfg.description_long}\n\n"
            f"## Framework\n\nBuilt with **{framework}**.\n\n"
            f"## Getting Started\n\n"
            f"    pip install -r requirements.txt\n"
            f"    python agent.py\n\n"
            f"**GitHub:** {cfg.github}\n"
        )
        await title_field.fill(title)
        body_field = page.locator('#article_body, [data-testid="editor"]')
        if await body_field.count() > 0:
            await body_field.fill(body)
        tags_field = page.locator('#article_tags, [placeholder*="tag" i]')
        if await tags_field.count() > 0:
            await tags_field.fill("ai, agent, claude, automation")
        tracker.update(p, "MANUAL", "https://dev.to/new", "Draft pre-filled — login and publish manually")
    except Exception as e:
        tracker.update(p, "FAILED", notes=str(e)[:120])


# ── Manual platforms ──────────────────────────────────────────────────────────

MANUAL_PLATFORMS = [
    ("Hugging Face Hub", "huggingface-cli login && huggingface-cli repo create <name> --type model → push agent files + README"),
    ("LangChain Hub", "pip install langsmith → from langsmith import Client; c.push_prompt('name', object=agent) → smith.langchain.com/hub"),
    ("CrewAI Templates", "PR to github.com/crewAIInc/crewAI → add your agent to examples/ directory"),
    ("AutoGen Community", "PR to github.com/microsoft/autogen → add to samples/ or notebooks/"),
    ("awesome-ai-agents", "PR to github.com/e2b-dev/awesome-ai-agents → add row to table"),
    ("misar-ai-plugins", "PR to git.misar.io/misaradmin/misar-ai-plugins → plugins/misar-dev/agents/<name>/agent.md"),
    ("Claude Discord #showcase", "discord.gg/anthropic → #showcase → post agent announcement with GitHub + demo"),
    ("Reddit r/ClaudeAI", "reddit.com/r/ClaudeAI/submit → 'Show r/ClaudeAI' flair → agent description + link"),
    ("Reddit r/LLMAgents", "reddit.com/r/LLMAgents/submit → post with framework, use case, GitHub link"),
    ("Hacker News", "news.ycombinator.com/submit → 'Show HN: [Name]' — requires karma ≥ 10"),
    ("Product Hunt", "producthunt.com/posts/new → full launch (logo, screenshots, Hunter strategy)"),
    ("Hashnode", "hashnode.com → tutorial post: 'Building [Name] with [Framework]'"),
    ("Peerlist", "peerlist.io/user/projects/add-project → Google OAuth"),
    ("F6S", "f6s.com → Google OAuth → Add Company/Product"),
    ("Fazier", "fazier.com/submit → embed badge on site → submit form"),
    ("Startup Ranking", "startupranking.com → Google OAuth → fill all fields (300+ char description required)"),
    ("Dang.ai", "Add backlink badge to site → dang.ai/submit → reCAPTCHA"),
    ("TAAFT", "Add backlink to theresanaiforthat.com → submit form"),
    ("LinkedIn", "Post: 'Built [Name] — AI agent that [does X]' + tutorial article"),
    ("Twitter/X", "Thread: 'Built [Name] 🧵' + demo video/GIF + GitHub link"),
    ("FlowiseAI", "flowiseai.com → export agent JSON → submit as template"),
    ("Relevance AI", "relevanceai.com → partner form → manual review"),
    ("LlamaIndex Hub", "pip install llama-hub → follow llamahub.ai contributor guide"),
    ("E2B.dev", "e2b.dev → sandbox template showcase → GitHub OAuth"),
]


# ── Orchestrator ──────────────────────────────────────────────────────────────

AUTOMATABLE = [
    ("huggingface", submit_huggingface),
    ("agenthub", submit_agenthub),
    ("future_tools", submit_future_tools),
    ("toptools_ai", submit_toptools_ai),
    ("insidr", submit_insidr),
    ("launchingnext", submit_launchingnext),
    ("uneed", submit_uneed),
    ("betalist", submit_betalist),
    ("listmyai", submit_listmyai),
    ("feedough", submit_feedough),
    ("github_topics", submit_github_topics),
    ("dev_to", submit_dev_to),
]

async def main():
    parser = argparse.ArgumentParser(description="AI Agent Listing Automation")
    parser.add_argument("--config", default="listing-config.yaml")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--platforms", default="")
    args = parser.parse_args()

    cfg = load_config(args.config)
    date_str = datetime.now().strftime("%Y%m%d-%H%M")
    tracker = SubmissionTracker(f"output/agents-listings-{date_str}.md")

    platforms = AUTOMATABLE
    if args.platforms:
        keys = set(args.platforms.split(","))
        platforms = [(n, f) for n, f in AUTOMATABLE if n in keys]

    print(f"\n🤖 AI Agent Listing Automation — {cfg.name}")
    print(f"   URL: {cfg.url}")
    print(f"   Framework: {cfg.agent_framework or 'not specified'}")
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
    print(f"\n📋 Tracker: output/agents-listings-{date_str}.md")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Config Template (`listing-config.yaml`)

```yaml
# AI Agent listing config
name: "my-agent-name"
url: "https://github.com/your-org/your-agent"
tagline: "One-line: what your agent does and for whom (max 80 chars)"
description_short: "Brief description: framework, use case, key capabilities (max 160 chars)."
description_long: |
  Full description: what the agent does, the problem it solves, key features,
  how to install/use it, example outputs, and technical architecture.
category: "AI Agent"
pricing_model: "Free"
pricing_tiers: "Free (open source)"
contact_email: "gulshan@promo.misar.io"
contact_name: "Gulshan Yadav"
twitter: "@mrgulshanyadav"
linkedin: "linkedin.com/in/mrgulshanyadav"
github: "https://github.com/misar-ai/your-agent"
logo_path: "./assets/logo.png"
screenshot_path: "./assets/screenshot.png"
agent_framework: "claude"       # claude / crewai / autogen / langgraph / custom
agent_category: "productivity"  # coding / research / marketing / ops / data / productivity
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
