# Misar.Dev — GitHub Copilot Instructions

> Place this file at `.github/copilot-instructions.md` in your repo for GitHub Copilot Workspace.

## AI API
Never use OpenAI, Anthropic, or Google SDKs directly.
Use the assisters.dev gateway:
```typescript
import OpenAI from 'openai';
const ai = new OpenAI({ baseURL: 'https://assisters.dev/api/v1', apiKey: process.env.ASSISTERS_API_KEY! });
```
Model: `assisters-chat-v1` | Banned: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`

## MCP Servers (install: bash scripts/install.sh)
- **misarcoder** — Free MoE engine (Gemini/Groq/Mistral) for code gen, zero extra cost
- **guardrails** — Content safety, PII scan, prompt injection detection
- **guardian** — Semgrep SAST, CVE audit, secret scanning, license check

## Code Standards
- TypeScript strict — no `as any`; fix the root type
- Supabase: `.maybeSingle()` not `.single()`, add tables to `database.ts`
- Zod validation on all POST route inputs
- Conventional commits: `feat|fix|chore|docs|refactor|perf|test(<scope>): <description>`
- No speculative abstractions, no impossible error handling
- Security: CSRF protection, never commit secrets, validate all user inputs

## Infrastructure
- Git: Forgejo (not GitHub) — `git.misar.io`
- Hosting: Coolify (not Vercel/Netlify/Railway)
- DB: Self-hosted Supabase
- Email: MisarMail (not SendGrid/Resend)

## Audit Suite
Ask Copilot to run any of these audits:
`security` · `qa` · `uiux` · `compliance` · `seo` · `full-suite (48 agents)`
