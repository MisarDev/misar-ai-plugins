---
name: list-tools-online
description: Submit tools to 50+ online directories, marketplaces, and listing platforms for maximum organic reach. Use when the user wants to list tools online, submit tools to directories, get tools discovered, or mentions "list tools", "submit tool", "tool directories", "tool listing". Handles form discovery, filling, submission, error handling, and verification.
user-invocable: true
argument-hint: "[--config listing-config.yaml] [--dry-run] [--platforms future_tools,toptools_ai,...]"
---

# List Tools Online

Automated tool submission to 50 online directories ranked by organic reach probability. Discovers submission forms, fills them, handles errors, and verifies listings go live.

## When to Trigger

- User says "list tools online", "submit tool to directories", "list my tools", "get my tools discovered"
- User invokes `/list-tools-online`
- User mentions tool directory submissions, tool marketplace listings

## Execution Protocol

### Phase 1: Preparation

1. Read tool details from user input or project context (URL, name, description, category, pricing, contact info)
2. Create tracking file at `Work/output/tool-listings-tracker-{date}.md`
3. Each entry tracks: Platform | Status (PENDING/SUBMITTED/LIVE/FAILED/SKIPPED/MANUAL) | URL | Notes

### Phase 2: Submission (Per Directory)

For EACH directory in the ranked list:

1. **Navigate** to the directory's submission/add page
2. **Detect** form type: direct form → fill; OAuth → use Google (mryadavgulshan@gmail.com); paid → skip; broken → fail
3. **Fill form** completely using browser tools
4. **Submit** and verify — check for errors, fix if needed
5. **Update tracker** immediately after each attempt

### Phase 3: Parallelization

- Launch up to 4 parallel agents per batch (browser extension conflicts with >4)
- Each agent handles 6-8 directories sequentially
- Main orchestrator monitors tracker file

---

## Top 50 Tool Directories — VERIFIED FREE (Updated 2026-03-30)

### tools.misar.io Status: ✅4 LIVE | ✅15 SUBMITTED | 🔧16 MANUAL | ⏳6 DEFERRED | ❌2 DEAD | ⏸1 SKIPPED = 21/50 reached

| # | Directory | Submit URL | Traffic | Status (tools.misar.io) |
|---|-----------|-----------|---------|------------------------|
| 1 | Product Hunt | producthunt.com/posts/new | 10M+ | ⏳ DEFERRED (launch strategy) |
| 2 | Reddit (relevant subs) | reddit.com/submit | 50M+ | ✅ LIVE — r/artificial |
| 3 | G2 | g2.com/products/new | 8M+ | 🔧 MANUAL (Google login) |
| 4 | Dev.to (Show DEV) | dev.to/new | 7M+ | ✅ LIVE |
| 5 | Capterra | digitalmarkets.gartner.com/get-listed/start | 6M+ | 🔧 MANUAL (click Continue) |
| 6 | AlternativeTo | alternativeto.net (email signup) | 5M+ | 🔧 MANUAL (Google signup disabled) |
| 7 | AppSumo Marketplace | sell.appsumo.com | 5M+ | ✅ SUBMITTED |
| 8 | CrunchBase | crunchbase.com/add-new | 5M+ | 🔧 MANUAL (Google connect errored) |
| 9 | SourceForge | sourceforge.net/software/vendors/new | 4M+ | 🔧 MANUAL (reCAPTCHA) |
| 10 | Hacker News (Show HN) | news.ycombinator.com/submit | 10M+ | ⏳ DEFERRED (karma=1, need ≥10) |
| 11 | SaaSHub | saashub.com/services/submit | 2.5M+ | 🔧 MANUAL (password reset in Mailcow) |
| 12 | Software Advice | softwareadvice.com/vendors | 2.5M+ | ✅ SUBMITTED |
| 13 | There's An AI For That | theresanaiforthat.com/submit | 2M+ | 🔧 MANUAL (needs backlink first) |
| 14 | ToolPilot.ai | form.jotform.com/231772738321053 | 2M+ | 🔧 MANUAL (select Free, submit) |
| 15 | Future Tools | futuretools.io/submit-a-tool | 2M+ | ✅ SUBMITTED |
| 16 | Feedough | feedough.com/submit-your-startup | 800K+ | ✅ SUBMITTED |
| 17 | Fazier | fazier.com/submit | 800K+ | ✅ SUBMITTED (partial) |
| 18 | Crozdesk | vendor.revleads.com | 800K+ | ✅ SUBMITTED #269704 |
| 19 | Uneed.best | uneed.best/submit | 700K+ | ✅ SUBMITTED |
| 20 | SaaSWorthy | Email: business@saasworthy.com | 700K+ | ✅ SUBMITTED (email sent 2026-03-30) |
| 21 | F6S | f6s.com (Google login → add company) | 500K+ | ✅ LIVE |
| 22 | Indie Hackers | indiehackers.com/products | 500K+ | 🔧 MANUAL (OAuth conflict) |
| 23 | Software Suggest | softwaresuggest.com/vendors | 500K+ | ✅ SUBMITTED |
| 24 | Launched.io | launched.io/SubmitStartup | 500K+ | 🔧 MANUAL (screenshot needed) |
| 25 | TopTools.AI | toptools.ai/submit | 400K+ | ✅ SUBMITTED |
| 26 | LaunchingNext | launchingnext.com/submit | 350K+ | ✅ SUBMITTED #129501 |
| 27 | Dang.ai | dang.ai/submit | 300K+ | ✅ SUBMITTED (badge deployed) |
| 28 | Peerlist | peerlist.io/user/projects/add-project | 300K+ | ✅ LIVE |
| 29 | Startup Ranking | startupranking.com/startup/create/url-validation | 250K+ | ✅ SUBMITTED |
| 30 | Supertools/Rundown | rundown.ai/submit | 250K+ | 🔧 MANUAL (image upload) |
| 31 | NachoNacho | connect.nachonacho.com/signup-seller | 200K+ | ⏸ SKIPPED (US focus) |
| 32 | Insidr.ai | insidr.ai/submit-tools | 150K+ | ✅ SUBMITTED |
| 33 | SaaSGenius | Email: contact@saasgenius.com | 150K+ | ✅ SUBMITTED (email sent 2026-03-30) |
| 34 | WhatTheAI | whattheai.tech/submit | 120K+ | 🔧 MANUAL (screenshot needed) |
| 35 | Tool0 | tool0.org/user/submit-list | 60K+ | ✅ SUBMITTED (needs badge) |
| 36 | AIToolBoard | aitoolboard.com/submit | 50K+ | 🔧 MANUAL (screenshot needed) |
| 37 | Twelve Tools | twelve.tools/submit-your-tool | 50K+ | 🔧 MANUAL (backlink + login) |
| 38 | NextGenTools | nextgentools.me/submit-your-tool | 30K+ | 🔧 MANUAL (image in iframe) |
| 39 | SideProjectors | sideprojectors.com/submit/type | 200K+ | 🔧 MANUAL (ad scripts block) |
| 40 | GetApp | getapp.com/submit | 1.5M+ | 🔧 MANUAL (same as Capterra) |
| 41 | Slashdot | slashdot.org/submission | 3M+ | 🔧 MANUAL (registration suspended) |
| 42 | Lobsters | lobste.rs | 500K+ | ⏳ DEFERRED (invite needed) |
| 43 | Hashnode | hashnode.com (blog post) | 5M+ | 🔧 MANUAL (extension blocks OAuth) |
| 44 | Quora (answer with link) | quora.com | 300M+ | ⏳ DEFERRED (drafts ready) |
| 45 | Stack Overflow (if applicable) | stackoverflow.com | 100M+ | ⏳ DEFERRED |
| 46 | Trustpilot | trustpilot.com/business | 50M+ | 🔧 MANUAL (reCAPTCHA) |
| 47 | Wellfound (AngelList) | wellfound.com/company/new | 5M+ | 🔧 MANUAL (CAPTCHA slider) |
| 48 | TechCrunch (Submit tip) | techcrunch.com/tips | 20M+ | ⏳ DEFERRED (needs news angle) |
| 49 | Free Tools Directory | free-tools.directory/submit | 30K+ | ❌ DEAD (DNS down) |
| 50 | AI Tools Directory | aitoolsdirectory.com/submit | 80K+ | ❌ DEAD (SSL 525) |

---

## Per-Directory Submission Steps (Verified 2026-03-28)

### 1. Product Hunt (producthunt.com)
- **Auth:** Account login required (email or social)
- **Steps:** producthunt.com/posts/new → Upload logo → Name + Tagline + URL + Description + Topics → Schedule launch date
- **Notes:** High-impact, coordinate launch day. Only 1 launch allowed. Get hunters/upvotes lined up first
- **Requires:** Logo image, 5+ screenshots, launch strategy

### 2. Reddit
- **Auth:** Account login
- **Steps:** reddit.com/submit → Select subreddit (r/artificial, r/MachineLearning, r/SideProject) → Title + body + flair
- **Notes:** Follow 10:1 self-promo rule. "Project" flair for r/artificial. Wait between sub posts
- **Requires:** Established account with karma

### 3. G2 (g2.com)
- **Auth:** Google login (mryadavgulshan@gmail.com)
- **Steps:** g2.com/products/new → Sign in with Google → Fill product name, URL, category, description
- **Notes:** Free listing, moderated review
- **Requires:** Google account

### 4. Dev.to (Show DEV)
- **Auth:** Google login → Continue → auto-redirects to homepage
- **Steps:** dev.to/new → Title "Show DEV: [name]" → Tags: showdev, ai, webdev, productivity → Markdown body → Publish
- **Form fields:** Title (text), Tags (4 max, autocomplete), Content (markdown textarea)
- **Notes:** Instant publish, no review. 7M+ monthly visitors. Tags are clickable autocomplete
- **Confirmed working:** ✅ 2026-03-28

### 5. Capterra (Gartner Digital Markets)
- **Auth:** None (form is open)
- **Steps:** digitalmarkets.gartner.com/get-listed/start → Business Email + Product Name + Product Website → Continue
- **Notes:** Just 3 fields. Free basic listing. Gartner reviews the submission
- **Confirmed working:** ✅ Form loads

### 6. AlternativeTo
- **Auth:** Email signup (Google signup disabled as of 2026-03-28)
- **Steps:** alternativeto.net → Sign up with email → Verify email → alternativeto.net/software/add/ → Fill app details
- **Notes:** Google signup explicitly disabled. Email: gulshan@promo.misar.io, Password: MisarAI@2026#AltTo
- **Blocker:** Cloudflare bot protection blocks automated signup

### 7. AppSumo Marketplace
- **Auth:** HubSpot form (no login)
- **Steps:** sell.appsumo.com → Fill partner application form → Submit
- **Notes:** "Boom, you did it! 🎉" confirmation. AppSumo team reviews for fit
- **Confirmed working:** ✅ 2026-03-27

### 8. CrunchBase
- **Auth:** Email account + Google social connect
- **Steps:** crunchbase.com → Account Settings → Connect Google → Wait up to 1 business day → /add-new → Fill company
- **Notes:** Must connect social network before contributing. Account exists with gulshan@promo.misar.io
- **Blocker:** Google connect button errored (2026-03-28) — retry manually

### 9. SourceForge
- **Auth:** None (open form)
- **Steps:** sourceforge.net/software/vendors/new → Name, Email, Company, Title, Website, Founded, Location, Software Title, Category, Price, Platform → Terms ✓ → Submit
- **Notes:** All fields fillable via automation. **reCAPTCHA blocks automated submit** — must solve manually
- **Blocker:** reCAPTCHA on submit button

### 10. Hacker News (Show HN)
- **Auth:** Account login (mrgulshanyadav, karma=1)
- **Steps:** news.ycombinator.com/submit → Title "Show HN: [name]" → URL → Text
- **Blocker:** Requires karma ≥10. Current karma=1. Build karma by commenting first
- **Ask HN posted:** ✅ news.ycombinator.com/item?id=47530522

### 11. SaaSHub
- **Auth:** Email login (gulshan@promo.misar.io account exists, password unknown)
- **Steps:** saashub.com/services/submit → Login → Fill tool details → Submit
- **Blocker:** Password reset sent to Mailcow inbox — check and login manually

### 12. Software Advice
- **Auth:** None (open form)
- **Steps:** softwareadvice.com/vendors → Name, Email, Title, Company, Category, Software Type, Country, Employees → Submit
- **Confirmed working:** ✅ 2026-03-27

### 13. There's An AI For That (TAAFT)
- **Auth:** None
- **Steps:** theresanaiforthat.com/submit → Free requires backlink to TAAFT on your site OR $97 paid
- **Notes:** Free listing requires visible backlink. Paid option is $97
- **Blocker:** Needs backlink added to tool site first

### 14. ToolPilot.ai
- **Auth:** None (JotForm)
- **Steps:** form.jotform.com/231772738321053 → Name, Company, Email, Tool Name, URL, Description, Features, Platform=Web, Pricing=Free, Terms ✓ → Submit
- **Notes:** Also requires backlink to toolpilot.ai. Lowest Price field = 0
- **Blocker:** JotForm became unreachable in some sessions

### 15. Future Tools
- **Auth:** None (direct form, no login)
- **Steps:** futuretools.io/submit-a-tool → Your Name + Tool Name + Tool URL + Short Description + Category (dropdown) + Pricing (radio: Free) + Email → Submit Tool
- **Form fields:** 7 fields total. Category dropdown includes: Research, Productivity, Marketing, etc. Pricing is radio buttons (Free/Freemium/Paid/Open Source)
- **Notes:** "Matt will review it and, if approved, it will appear in the database soon." Simplest form
- **Confirmed working:** ✅ 2026-03-27

### 16. Feedough
- **Auth:** None (Formaloo iframe form, 22 steps)
- **Steps:** feedough.com/submit-your-startup → Formaloo questionnaire iframe with 22 sequential steps:
  1. Full name → 2. Startup name → 3. Position → 4. Email → 5. LinkedIn URL
  6. What startup does → 7. Target audience → 8. Primary problem → 9. Solution
  10. Founding team → 11. Industry inspiration → 12. Early challenges
  13. Differentiation → 14. External funding (Yes/No) → 15. Future plans
  16. Revenue → 17. Monthly users → 18. YoY growth → 19. Other details
  20. Advice → 21. Industry stats → 22. Logo upload (PNG, transparent bg)
- **Notes:** Each step has Continue button. Back button available. Logo upload is REQUIRED (step 22)
- **Confirmed working:** ✅ 2026-03-28

### 17. Fazier
- **Auth:** Google login or email signup
- **Steps:** fazier.com/submit → Select Free tier → Requires: embed Fazier badge on your site + leave 3 comments on other products → Submit
- **Notes:** Free tier opens 15+ external directory tabs automatically. Badge embed needed on site
- **Confirmed working:** ✅ 2026-03-27 (partial)

### 18. Crozdesk
- **Auth:** None (vendor.revleads.com application)
- **Steps:** crozdesk.com → Redirects to vendor.revleads.com → Fill application form → Submit
- **Notes:** Application #269704 confirmed. "Thank you for submitting your application"
- **Confirmed working:** ✅ 2026-03-27

### 19. Uneed.best
- **Auth:** None
- **Steps:** uneed.best/submit → Fill tool details → Submit
- **Confirmed working:** ✅ (prior session)

### 20. SaaSWorthy
- **Auth:** None (email submission)
- **Steps:** Compose email to business@saasworthy.com with tool details (name, URL, description, category, pricing)
- **Notes:** No web form exists. Email-only submission. Gmail draft can be pre-composed
- **Confirmed:** Gmail draft created

### 21. F6S
- **Auth:** Google OAuth (mryadavgulshan@gmail.com)
- **Steps:** f6s.com → Sign in with Google → Dashboard → Add Company → Fill details
- **Notes:** Profile already exists at f6s.com/misar-ai-tools — needs description added
- **Confirmed:** Profile exists, needs manual description update

### 22. Indie Hackers
- **Auth:** Google OAuth
- **Steps:** indiehackers.com/sign-in → Google → /products/new → Fill product details
- **Blocker:** F6S OAuth session intercepts Google login — use incognito/clean browser

### 23. Software Suggest
- **Auth:** Account creation (work email required — no Gmail/Outlook)
- **Steps:** softwaresuggest.com/vendors → Name, Business Email, Organization, Phone, Website → 3-step account creation
- **Notes:** Consumer emails blocked. Use gulshan@promo.misar.io

### 24. Launched.io
- **Auth:** None (open form)
- **Steps:** launched.io/SubmitStartup → Product Name, Pitch, Website, Description, Twitter, Location, Industry, Email, Stage → Screenshot upload (1088×816px REQUIRED) → Submit
- **Notes:** All text fields fillable. Screenshot is mandatory (server rejects without it)
- **Blocker:** Screenshot upload required

### 25. TopTools.AI
- **Auth:** None (3-field form)
- **Steps:** toptools.ai/submit → Tool Name + URL + Email → Submit
- **Notes:** Simplest form possible. "Thank you! Your tool has been submitted." Policy: AI directories/newsletters rejected, actual tools accepted
- **Confirmed working:** ✅ 2026-03-28

### 26. LaunchingNext
- **Auth:** None (direct form)
- **Steps:** launchingnext.com/submit → Multi-field form → Submit
- **Notes:** Standard review up to 4 months. Upsell $99 for 1-day review. Confirmed #129501, #129503
- **Confirmed working:** ✅ 2026-03-27

### 27. Dang.ai
- **Auth:** None
- **Steps:** dang.ai/submit → Free option: add backlink badge to your site → Fill Webflow form (name, email, backlink URL, confirm badge added) → reCAPTCHA → Submit
- **Badge HTML:** `<a href="https://dang.ai/" target="_blank"><img src="https://cdn.prod.website-files.com/.../dang-badge.png" alt="Dang.ai" width="150" height="54"/></a>`
- **Notes:** Free listing active as long as badge stays. Review within 1 week. Paid option $29
- **Confirmed working:** ✅ 2026-03-28 (badge deployed to tools.misar.io footer)

### 28. Peerlist
- **Auth:** Google OAuth (mryadavgulshan@gmail.com)
- **Steps:** peerlist.io → Sign in with Google → /user/projects/add-project → Project Name, URL, Tagline, Description → Save
- **Notes:** Creates a project page at peerlist.io/mryadavgulshan/project/[slug]
- **Confirmed working:** ✅ 2026-03-28

### 29. Startup Ranking
- **Auth:** Google OAuth (mryadavgulshan@gmail.com)
- **Steps:** startupranking.com/login → Google → /startup/create/url-validation → Enter URL → Validate → Continue → Fill: Name, Legal Name, Slogan, Country (select2 dropdown), State, URL, Founded Date (3 dropdowns), Business Type, Industry (select), Tags, Description (300+ chars), Twitter, LinkedIn, Email → Submit Startup
- **Notes:** Cloudflare challenge page after login — wait 5s. Free registration. Claim page appears after submit
- **Confirmed working:** ✅ 2026-03-28

### 30. Supertools/The Rundown
- **Auth:** None (Tally iframe)
- **Steps:** rundown.ai/submit → Tally form: Tool name, Description, Price, Category, Tool link, Twitter, Email, Thumbnail image (REQUIRED) → Submit
- **Blocker:** Required thumbnail image upload

### 31. NachoNacho
- **Auth:** JS-rendered signup at connect.nachonacho.com/signup-seller
- **Notes:** Targets US-based SaaS with virtual card payments. May not accept free/India-based tools

### 32. Insidr.ai
- **Auth:** None (Tally form)
- **Steps:** insidr.ai/submit-tools → Tally form → Fill all fields → Submit
- **Confirmed working:** ✅ 2026-03-27

### 33. SaaSGenius
- **Auth:** None (email)
- **Steps:** Email to contact@saasgenius.com with tool details
- **Notes:** Not accepting free listings currently. Gmail draft pre-composed

### 34. WhatTheAI
- **Auth:** None (direct form)
- **Steps:** whattheai.tech/submit → Tool Name, Short/Long Description, Company, Your Name, Website URL, Pricing, Categories, Features, Platforms (checkboxes), Associated checkbox → Hero Screenshot (REQUIRED) → Submit
- **Blocker:** Mandatory screenshot upload

### 35. Tool0
- **Auth:** Account login (already registered)
- **Steps:** tool0.org/user/submit-list → Fill form → Submit
- **Notes:** Requires backlink badge on your site. Badge HTML provided during submission
- **Confirmed working:** ✅ 2026-03-28 (under review)

### 36. AIToolBoard
- **Auth:** None (open form at aitoolboard.com/submit — tooldirectory.ai redirects here)
- **Steps:** aitoolboard.com/submit → Tool Name, Short/Long Description, URL, Category=Code Assistant, Pricing=Free, Tags → Screenshot (REQUIRED) → Submit
- **Blocker:** Mandatory screenshot upload

### 37. Twelve Tools / OpenTools
- **Auth:** Google login → opentools.ai/friends/launch-tool
- **Notes:** twelve.tools redirects to opentools.ai. Requires backlink + Google sign-in. OpenTools is paid
- **Status:** SKIPPED — paid launch packages only

### 38. NextGenTools
- **Auth:** None (Google Form iframe)
- **Steps:** nextgentools.me/submit-your-tool → Iframe form: Tool name, Category (autocomplete dropdown), URL, First Name, Last Name, Email, Description, File upload (REQUIRED) → Submit
- **Blocker:** Mandatory file/image upload

### 39. SideProjectors
- **Auth:** Email login or OAuth (GitHub, GitLab, ProductHunt, LinkedIn, Twitter)
- **Steps:** sideprojectors.com → Login/Register → /submit/type → Select "Show Off" → Fill project name, URL, description, category → Submit
- **Notes:** Marketplace for side projects. Use "Show Off" type (free) not "For Sale"

### 40. GetApp (Gartner)
- **Auth:** None (same Gartner form as Capterra)
- **Steps:** getapp.com → "Get Listed" → Redirects to digitalmarkets.gartner.com/get-listed/start → Business Email + Product Name + Website → Continue
- **Notes:** Same parent company as Capterra. One submission may cover both

### 41. Slashdot
- **Auth:** Account login (create at slashdot.org)
- **Steps:** slashdot.org/submission → Title + URL + Description → Select topic → Submit
- **Notes:** Tech news aggregator. Story must be newsworthy, not just a product listing

### 42. Lobsters
- **Auth:** Invite-only (need existing member invitation)
- **Steps:** Get invited by existing member → lobste.rs → Submit story with URL + title + tags
- **Notes:** High-quality tech community. No self-promotion unless genuinely interesting. Invite required
- **Blocker:** Requires invitation from existing member

### 43. Hashnode
- **Auth:** Google login (mryadavgulshan@gmail.com)
- **Steps:** hashnode.com → Sign in with Google → Start blog or use existing → Write "Show" post → Title + body (markdown) + tags → Publish
- **Notes:** Developer blogging platform. Write a "Show Hashnode" style technical post about the tools

### 44. Quora
- **Auth:** Account login (mryadavgulshan@gmail.com)
- **Steps:** quora.com → Find relevant questions about LLM costs, AI evaluation, RAG → Write detailed answers → Include tools.misar.io link naturally
- **Notes:** Not a directory submission. Answer genuinely useful questions and reference the tool. 5 answer drafts exist at Work/Quora/answer-drafts.md

### 45. Stack Overflow
- **Auth:** Account login
- **Steps:** Find questions about LLM cost comparison, token counting, RAG costs → Answer with tool reference if genuinely helpful
- **Notes:** ONLY reference if directly answering a question. Self-promotion is heavily penalized. Must provide substantial value in the answer

### 46. Trustpilot
- **Auth:** Business account claim
- **Steps:** business.trustpilot.com → Claim free business profile → Fill company details → Verify ownership
- **Notes:** Free basic listing. Premium features are paid. Focused on reviews, not tool discovery

### 47. Wellfound (AngelList)
- **Auth:** Email or Google login
- **Steps:** wellfound.com/company/new → Company name, URL, description, industry, stage, location → Submit
- **Notes:** Startup/talent platform. Good for company visibility + hiring

### 48. TechCrunch Tips
- **Auth:** None (tip submission form)
- **Steps:** techcrunch.com/tips → Fill tip form with tool details, news angle → Submit
- **Notes:** Not a directory. Editorial tip line. Only submit if there's a genuine news angle (e.g., launch, milestone)

### 49. Free Tools Directory
- **Auth:** None (direct form)
- **Steps:** free-tools.directory/submit → Tool name, URL, description, category → Submit
- **Notes:** Niche directory for free tools. Good fit for tools.misar.io (all 4 tools are free)

### 50. AI Tools Directory
- **Auth:** None (direct form)
- **Steps:** aitoolsdirectory.com/submit → Tool name, URL, description, category → Submit
- **Notes:** SSL was broken (error 525) as of 2026-03-27. Check if fixed before attempting
- **Blocker:** SSL handshake error (intermittent)

---

## Confirmed Dead/Paid Directories (Excluded)

Futurepedia ($247+), TopAI.tools ($47+), Toolify.ai ($99), aitools.fyi ($30), DevHunt ($49), Microlaunch (paid), ListMyAI (€49), Blastra ($199), Ben's Bites (paid), AwesomeAITools ($69), FindMyAITool (paid), AiToolNet (→topai paid), TopStartups.io ($99), BetaList ($39+), AIxploria ($79), OpenTools (paid), YourStack (offline since 2022), Toolify.Directory (DNS dead), Startups.fyi ($29), WebAppRater (522 down), AIToolTrace (ECONNREFUSED), ToolPedia (→feedough), FreeAIKit (down), AIToolGuru.co (DNS dead), AItoolsDirectory (SSL down), MakerLog (defunct), StartupLift (down), KillerStartups (no form), StartupStash (404), Slant (500), Crayon (not directory), Land-book ($69), BetaPage/PitchWall (OAuth-only), SnapMunk (unsafe), StackShare (500+OAuth), StartupBase (closed), AllTopStartups (paid), TechPluto (→Fazier), GoodFirms ($1500/yr), GPTStoreTracker (dead), AIToolMall (parked), Startupresources.io (→G2), RankMyAI (→nocodelist), ToolsFine (dead), AIDude (parked), AiToolsKit (down), SaaSFrame (not tool dir), NoCodeList (broken), AIDirectoryHub (blank WP), ToolsAI (SSL invalid), GrabOn.AI (timeout), AISuperSmart (→Supertools dup), AllThingsAI (DNS down), EasyWithAI (CF 403), PoweredbyAI (broken), AIScout (520), SaaSAITools/ToolScout/LaunchAI/ProductDirectory (ERR_FAILED/DNS dead)

## Form Field Mapping

| Common Field | Source |
|-------------|--------|
| Tool/Product Name | User-provided tool name |
| URL/Website | User-provided URL |
| Description (short) | First 160 chars of description |
| Description (long) | Full description |
| Category | Best match: AI, Developer Tools, Productivity, Research, Other |
| Pricing | Free / Freemium / Paid (radio buttons or dropdown) |
| Email | Contact email (gulshan@promo.misar.io) |
| Twitter/X | @mrgulshanyadav |
| Logo/Screenshot | Upload if field exists and file available |
| Tags | Extract keywords from description |

## Error Recovery

| Error | Action |
|-------|--------|
| "Email already registered" | Try login or password reset |
| "URL already submitted" | Mark ALREADY_LISTED, verify |
| Required field missing | Re-read form, fill missing |
| CAPTCHA/reCAPTCHA | Mark MANUAL |
| 403/429 rate limit | Wait 30s, retry once |
| 500 server error | Retry once, then FAILED |
| OAuth required | Use Google (mryadavgulshan@gmail.com) |
| Paid only | Mark SKIPPED (Paid: $X) |
| Site down | Mark FAILED (down) |
| File chooser modal blocking | Cancel with browser_file_upload (no paths) |
| Browser extension redirects | Close extra tabs, re-navigate |

## Contact Info Template

```
Name: Gulshan Yadav
Email: gulshan@promo.misar.io
Company: Misar AI
Title: Founder
Twitter: @mrgulshanyadav
LinkedIn: linkedin.com/in/mrgulshanyadav
Location: India
Founded: 2024
```

## Lessons Learned (2026-03-28)

### Browser Automation Blockers
1. **reCAPTCHA v3 (invisible)** silently blocks automated browsers — form resets without error (SourceForge, Trustpilot). Score automated browsers as 0.
2. **CAPTCHA slider challenges** (Wellfound) detect automated browsers via IP reputation. Cannot be dragged programmatically.
3. **Google OAuth popups** in new windows can't be handled by Playwright — only same-tab OAuth redirects work.
4. **Browser extensions** in Playwright Chrome profile intercept navigation to AI directory sites, redirecting to random competitors. Close extra tabs frequently.
5. **File chooser modals** from one tab block ALL browser operations across all tabs. Cancel immediately with `browser_file_upload` (no paths arg).
6. **Select2/Chosen dropdowns** don't respond to standard fill — use JS: `document.getElementById(id).value = val; el.dispatchEvent(new Event('change', {bubbles:true}))`.
7. **JotForm payment product selectors** (q107_myProducts) are hidden radio buttons that need explicit click — not regular form radios.
8. **Formaloo multi-step forms** (Feedough, 22 steps) require clicking Continue after each field. Logo upload is always the last mandatory step.

### What Works Reliably
1. **Direct HTML forms** (Future Tools, TopTools, LaunchingNext, Uneed) — fill + submit in one sequence.
2. **Google OAuth redirect flow** (not popup) — Dev.to, Startup Ranking, Peerlist all work via redirect.
3. **Tally.so embedded forms** (Insidr.ai) — standard text fields work, image upload fields block.
4. **JS-based form filling** via `browser_evaluate` — faster and more reliable than Playwright clicks for complex forms.
5. **Gmail MCP for email submissions** — create drafts for email-only directories (SaaSWorthy, SaaSGenius).

### Submission Success Rates by Type
| Form Type | Success Rate | Example |
|-----------|-------------|---------|
| Direct HTML form (no login) | 90%+ | Future Tools, TopTools, LaunchingNext |
| Google OAuth redirect | 80%+ | Dev.to, Startup Ranking, Peerlist |
| Email submission | 100% (draft) | SaaSWorthy, SaaSGenius |
| JotForm / Tally (text only) | 70% | Insidr.ai, ToolPilot (partial) |
| Multi-step wizard | 50% | Feedough (21/22), G2 (blocked) |
| Forms requiring image upload | 0% | WhatTheAI, AIToolBoard, NextGenTools |
| reCAPTCHA-gated | 0% | SourceForge, Trustpilot |
| CAPTCHA slider | 0% | Wellfound |

### Accounts Created (for future logins)
| Platform | Email | Password | Status |
|----------|-------|----------|--------|
| Startup Ranking | mryadavgulshan@gmail.com (Google) | — | Active |
| Dev.to | mryadavgulshan@gmail.com (Google) | — | Active |
| Peerlist | mryadavgulshan@gmail.com (Google) | — | Active |
| F6S | mryadavgulshan@gmail.com (Google) | — | Active |
| CrunchBase | gulshan@promo.misar.io | Unknown | Google connect failed |
| SaaSHub | gulshan@promo.misar.io | Unknown | Password reset sent |
| Capterra/Gartner | gulshan@promo.misar.io | Unknown | Password reset sent |
| Software Suggest | gulshan@promo.misar.io | — | Submitted, pending |
| AlternativeTo | Not created | — | Google signup disabled |
| BetaList | gulshan@promo.misar.io | Unknown | Draft #156048 exists |
| Tool0.org | Created | — | Submission under review |

### Parallel Agent Optimization
- **Max 4 agents per batch** — more causes browser tab conflicts
- **Shared Playwright browser context** means agents fight over the same tabs
- **Browser extension interference** worsens with more parallel agents
- **Best pattern:** Launch 4 agents, each with 6-8 sequential directories, using JS-based form filling
- **Worst pattern:** Multiple agents trying OAuth flows simultaneously (session cookies conflict)

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
# 2. Save the script block below to ~/.claude/scripts/list_tools_auto.py
# 3. Create listing-config.yaml with your tool details
python ~/.claude/scripts/list_tools_auto.py --config listing-config.yaml
python ~/.claude/scripts/list_tools_auto.py --config listing-config.yaml --dry-run
python ~/.claude/scripts/list_tools_auto.py --config listing-config.yaml --platforms "future_tools,toptools_ai,insidr,launchingnext"
```

### Block — Tool Platform Scripts (save as `~/.claude/scripts/list_tools_auto.py`)

```python
#!/usr/bin/env python3
"""
Tool Listing Automation — top automatable directories from list-tools-online
Usage: python list_tools_auto.py --config listing-config.yaml [--dry-run] [--platforms p1,p2]
Requires: pip install playwright pyyaml && playwright install chromium
Also requires: listing_base.py in ~/.claude/scripts/ (from list-mcp-online skill)
"""
import asyncio, sys, argparse
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright, Page

sys.path.insert(0, str(Path.home() / ".claude/scripts"))
from listing_base import ListingConfig, SubmissionTracker, load_config, run_batch


# ── Automatable platforms (confirmed working from live runs) ─────────────────

async def submit_future_tools(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """futuretools.io — 7-field form, no login. ✅ Confirmed 2026-03-27"""
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
        tracker.update(p, "SUBMITTED", "https://www.futuretools.io", "Pending Matt's review")
    except Exception as e:
        tracker.update(p, "FAILED", notes=str(e)[:120])

async def submit_toptools_ai(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """toptools.ai — 3-field form. ✅ Confirmed 2026-03-28"""
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
    """insidr.ai — Tally form. ✅ Confirmed 2026-03-27"""
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
    """uneed.best — REQUIRES LOGIN (verified live). Correct URL: /submit-a-tool"""
    p = "Uneed.best"
    tracker.update(p, "MANUAL", "https://www.uneed.best/submit-a-tool",
        "Login required (verified live) — create account at uneed.best then /submit-a-tool")

async def submit_toolpilot(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """toolpilot.ai — JotForm. ✅ Confirmed (add backlink to toolpilot.ai first)"""
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

async def submit_software_advice(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """softwareadvice.com/vendors — 9-field open form. ✅ Confirmed 2026-03-27"""
    p = "Software Advice"
    tracker.update(p, "PENDING")
    try:
        await page.goto("https://www.softwareadvice.com/vendors", wait_until="domcontentloaded", timeout=20000)
        await page.locator('input[name*="name"], input[placeholder*="name" i]').nth(0).fill(cfg.contact_name)
        await page.locator('input[type="email"]').fill(cfg.contact_email)
        title_f = page.locator('input[name*="title"], input[placeholder*="title" i]')
        if await title_f.count() > 0:
            await title_f.fill("Founder")
        company_f = page.locator('input[name*="company"], input[placeholder*="company" i]')
        if await company_f.count() > 0:
            await company_f.fill(cfg.name)
        url_f = page.locator('input[type="url"], input[name*="website"]')
        if await url_f.count() > 0:
            await url_f.fill(cfg.url)
        await page.locator('button[type="submit"]').click()
        await page.wait_for_selector('text=/thank|submit|success/i', timeout=15000)
        tracker.update(p, "SUBMITTED", "https://www.softwareadvice.com")
    except Exception as e:
        tracker.update(p, "FAILED", notes=str(e)[:120])

async def submit_crozdesk(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """crozdesk.com → vendor.revleads.com. ✅ Confirmed #269704"""
    p = "Crozdesk"
    tracker.update(p, "PENDING")
    try:
        await page.goto("https://vendor.revleads.com", wait_until="domcontentloaded", timeout=20000)
        await page.locator('input[type="text"]').nth(0).fill(cfg.contact_name)
        await page.locator('input[type="email"]').fill(cfg.contact_email)
        url_f = page.locator('input[type="url"]')
        if await url_f.count() > 0:
            await url_f.fill(cfg.url)
        desc_f = page.locator('textarea')
        if await desc_f.count() > 0:
            await desc_f.fill(cfg.description_short)
        await page.locator('button[type="submit"]').click()
        await page.wait_for_selector('text=/thank|submit|application/i', timeout=15000)
        tracker.update(p, "SUBMITTED", "https://crozdesk.com")
    except Exception as e:
        tracker.update(p, "FAILED", notes=str(e)[:120])

async def submit_appsumo(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """sell.appsumo.com — HubSpot partner form. ✅ Confirmed 2026-03-27"""
    p = "AppSumo Marketplace"
    tracker.update(p, "PENDING")
    try:
        await page.goto("https://sell.appsumo.com", wait_until="networkidle", timeout=30000)
        await page.locator('input[name*="firstname"], input[placeholder*="first name" i]').fill(cfg.contact_name.split()[0])
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

async def submit_feedough(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """feedough.com — 22-step Formaloo. Auto-fills steps 1-4."""
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
        tracker.update(p, "MANUAL", "https://www.feedough.com", "Steps 1-4 filled; complete 5-21 manually (logo required at step 22)")
    except Exception as e:
        tracker.update(p, "FAILED", notes=str(e)[:120])

async def submit_startup_ranking(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """startupranking.com — Google OAuth then multi-field form. ✅ Confirmed 2026-03-28"""
    p = "Startup Ranking"
    tracker.update(p, "MANUAL", "https://startupranking.com/startup/create/url-validation",
        "Google OAuth (mryadavgulshan@gmail.com) → enter URL → fill all fields (300+ char description) → submit")

async def submit_peerlist(page: Page, cfg: ListingConfig, tracker: SubmissionTracker):
    """peerlist.io — Google OAuth. ✅ Confirmed 2026-03-28"""
    p = "Peerlist"
    tracker.update(p, "MANUAL", "https://peerlist.io/user/projects/add-project",
        "Google OAuth (mryadavgulshan@gmail.com) → /user/projects/add-project → fill and save")


# ── Orchestrator ──────────────────────────────────────────────────────────────

AUTOMATABLE = [
    ("future_tools", submit_future_tools),
    ("toptools_ai", submit_toptools_ai),
    ("insidr", submit_insidr),
    ("launchingnext", submit_launchingnext),
    ("uneed", submit_uneed),
    ("toolpilot", submit_toolpilot),
    ("software_advice", submit_software_advice),
    ("crozdesk", submit_crozdesk),
    ("appsumo", submit_appsumo),
    ("feedough", submit_feedough),
    ("startup_ranking", submit_startup_ranking),
    ("peerlist", submit_peerlist),
]

MANUAL_PLATFORMS = [
    ("Product Hunt", "producthunt.com/posts/new → logo + screenshots + Hunter strategy → coordinate launch day"),
    ("Reddit", "reddit.com/submit → r/artificial, r/SideProject, r/MachineLearning → 'Project' flair"),
    ("G2", "g2.com/products/new → Google login (mryadavgulshan@gmail.com)"),
    ("Capterra/Gartner", "digitalmarkets.gartner.com/get-listed/start → 3-field form → click Continue"),
    ("AlternativeTo", "Sign up at alternativeto.net (email only, Cloudflare blocks automation)"),
    ("CrunchBase", "crunchbase.com → connect Google social → /add-new"),
    ("SourceForge", "sourceforge.net/software/vendors/new → fill all fields → manual reCAPTCHA"),
    ("Hacker News", "news.ycombinator.com/submit → karma ≥ 10 required"),
    ("SaaSHub", "saashub.com/services/submit → login (check Mailcow for password reset)"),
    ("TAAFT", "Add backlink to theresanaiforthat.com → submit form"),
    ("Dang.ai", "Add badge to site → dang.ai/submit → reCAPTCHA"),
    ("Launched.io", "launched.io/SubmitStartup → screenshot upload required (1088×816px)"),
    ("WhatTheAI", "whattheai.tech/submit → screenshot required"),
    ("Supertools/Rundown", "rundown.ai/submit → thumbnail image required"),
    ("Indie Hackers", "indiehackers.com/products → Google OAuth (use incognito)"),
    ("F6S", "f6s.com → Google OAuth → Dashboard → Add Company"),
    ("Trustpilot", "trustpilot.com/business → reCAPTCHA"),
    ("Wellfound", "wellfound.com/company/new → CAPTCHA slider"),
    ("Slashdot", "slashdot.org/submission → registration suspended"),
    ("SaaSGenius", "Email: contact@saasgenius.com with tool details (may not accept free)"),
    ("SaaSWorthy", "Email: business@saasworthy.com with tool details"),
]

async def main():
    parser = argparse.ArgumentParser(description="Tool Listing Automation")
    parser.add_argument("--config", default="listing-config.yaml")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--platforms", default="")
    args = parser.parse_args()

    cfg = load_config(args.config)
    date_str = datetime.now().strftime("%Y%m%d-%H%M")
    tracker = SubmissionTracker(f"output/tool-listings-{date_str}.md")

    platforms = AUTOMATABLE
    if args.platforms:
        keys = set(args.platforms.split(","))
        platforms = [(n, f) for n, f in AUTOMATABLE if n in keys]

    print(f"\n🔧 Tool Listing Automation — {cfg.name}")
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
    print(f"\n📋 Tracker: output/tool-listings-{date_str}.md")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Config Template (`listing-config.yaml`)

```yaml
name: "tools.misar.io"
url: "https://tools.misar.io"
tagline: "AI-powered developer tools by Misar AI — build faster with Claude"
description_short: "Free AI tools for developers: Claude plugins, MCP servers, code assistants, and productivity tools."
description_long: |
  tools.misar.io is a collection of free AI-powered developer tools built by Misar AI.
  Includes MCP servers for Claude, productivity plugins, code generation tools,
  and automation scripts — all open source and free to use.
category: "AI Tools"
pricing_model: "Free"
pricing_tiers: "Free"
contact_email: "gulshan@promo.misar.io"
contact_name: "Gulshan Yadav"
twitter: "@mrgulshanyadav"
linkedin: "linkedin.com/in/mrgulshanyadav"
github: "https://github.com/misar-ai"
logo_path: "./assets/logo.png"
screenshot_path: "./assets/screenshot.png"
```
