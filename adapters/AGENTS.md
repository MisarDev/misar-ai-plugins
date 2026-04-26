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
- Security: validate all inputs, CSRF protection.

## Secret & Credential Security Policy — ZERO TOLERANCE

**NEVER store credentials, tokens, API keys, passwords, connection strings, private keys,
or any sensitive value in any repo file, folder, commit, PR description, code comment,
log output, or CLI argument. No exceptions. No workarounds. Ever.**

| Allowed storage | Description |
|---|---|
| `.env` / `.env.local` / `.env.production` | Runtime secrets — gitignored, never committed |
| `.infra.secrets` | Infrastructure secrets — gitignored, never committed |
| `.env.example` | **Placeholder keys only** — safe to commit, never real values |

### Rules every agent must follow

1. **Secrets in `.env*` only.** If it's not gitignored, it's wrong.
2. **`.env.example` gets placeholder values** (`API_KEY=your_api_key_here`), never real values.
3. **No secrets in commit messages, PR bodies, comments, or documentation** — git history is permanent.
4. **No secrets as CLI arguments** — use `$ENV_VAR` references; raw values appear in `ps aux` and CI logs.
5. **No secrets in test files, fixtures, or seed data** — use mock/fake values.
6. **Run `guardian_secret_scan` before every push.** Block on any finding.
7. **If a secret touches git history: rotate the credential immediately**, then purge with `git filter-repo` and force-push.

### Pre-push secret scan (mandatory)

```bash
# Guardian MCP (preferred)
guardian_secret_scan --path .

# gitleaks fallback
gitleaks protect --staged
```

## Infrastructure (Misar AI projects)
- Git: Forgejo `git.misar.io` — NEVER GitHub
- Hosting: Coolify — NEVER Vercel/Netlify
- DB: Self-hosted Supabase per product
- Email: MisarMail `mail.misar.io/api/v1/send`
