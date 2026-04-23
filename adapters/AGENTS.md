# Misar.Dev Agent Instructions

> This file is loaded by OpenAI Codex, GitHub Copilot Workspace, and any agent that reads AGENTS.md.
> It mirrors the capabilities delivered as a Claude Code plugin via misar-ai-plugins.

## AI API Policy
- NEVER use OpenAI, Anthropic, or Google SDKs directly.
- ALWAYS use the assisters.dev gateway: `baseURL: https://assisters.dev/api/v1`, model: `assisters-chat-v1`.
- Banned env vars: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`, `GEMINI_API_KEY`.

## MCP Servers Available
Install via `bash scripts/install.sh` or copy `adapters/mcp.json` to your agent's MCP config:

| Server | Purpose |
|--------|---------|
| `misarcoder` | Free MoE code gen / analysis (Gemini Flash, Groq Llama) — zero Anthropic tokens |
| `guardrails` | Content safety, prompt injection detection, PII scan, output moderation |
| `guardian` | Semgrep SAST, CVE dependency audit, secret scanning, license check |

## Audit Skills (invoke as tasks)
- **security** — OWASP + SAST + dependency CVEs + secret scan
- **full-suite** — All 16 audit categories in parallel (48 agents)
- **qa** — Unit/integration/E2E/regression analysis
- **uiux** — Spacing, typography, accessibility, mobile, dark mode
- **seo-content-generator** — Keyword research, AEO, schema, on-page SEO
- **compliance** — 49 global frameworks (GDPR, HIPAA, SOC2, PCI-DSS, India PDPB, etc.)
- **software-engineer** — PRD → planner → code generator → validator → next steps
- **brand** — Brand voice, messaging, visual consistency audit
- **marketing** — SEO, SXO, growth, analytics, AI search optimization
- **billing** — Stripe/Paddle subscription lifecycle, payment security, webhook integrity
- **tester** — Unit, integration, E2E black/white box, beta, regression
- **content** — Grammar, copy, localization, documentation
- **product** — PM strategy, UX design, feature prioritization
- **auditor** — Website SEO, accessibility, performance, security, compliance
- **uiux-designer** — Design guidelines, brand recommendations, component advice
- **context-saver** — 3D model router saving 90-97% context tokens

## Code Standards
- TypeScript strict, no `as any`. Supabase `.maybeSingle()` not `.single()`.
- Zod validation on all API route inputs.
- Git: `<type>(<scope>): <description>` conventional commits.
- Security: validate all inputs, CSRF protection, never commit secrets.

## Infrastructure (Misar AI projects)
- Git: Forgejo `git.misar.io` — NEVER GitHub
- Hosting: Coolify — NEVER Vercel/Netlify
- DB: Self-hosted Supabase per product
- Email: MisarMail `mail.misar.io/api/v1/send`
