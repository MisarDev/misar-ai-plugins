---
name: security
description: "Use when: security review, vulnerability scanning, hardening a server, SSH setup, Nginx/HTTPS configuration, Let's Encrypt certificates, data privacy audit, penetration testing, checking for XSS/SQLi/CSRF, GDPR compliance, API security. Triggers: 'security audit', 'is my app secure', 'harden my server', 'setup HTTPS', 'check for vulnerabilities', 'SSH setup', 'firewall rules', 'is this safe', 'security review'."
user-invocable: true
argument-hint: "[agents] [--path=src/] [--server=linux]"
---

# Security Audit

---

## Credential & Secret Security — ABSOLUTE RULE

> **ZERO TOLERANCE. No exceptions. No workarounds. Ever.**

### What is forbidden — in every repo, every file, every commit, forever

| Category | Examples |
|---|---|
| API keys & tokens | `sk-proj-...`, `ghp_...`, `xoxb-...`, bearer tokens, JWT secrets |
| Passwords | DB passwords, admin passwords, SSH passphrases |
| Connection strings | `postgresql://user:password@host/db`, `redis://:password@host` |
| Cloud credentials | AWS access keys, GCP service account JSON, Azure client secrets |
| Webhook secrets | Stripe webhook signing secrets, Slack signing secrets |
| Private keys | RSA/EC private keys (`.pem`, `-----BEGIN ...-----`) |
| OTP/MFA seeds | TOTP base32 seeds, recovery codes |
| Any other sensitive value | Internal hostnames+ports, UUIDs tied to billing, revenue figures |

### Hard rules — apply to ALL files, branches, commits, PRs, and messages

1. **Secrets live ONLY in `.env*` files** — `.env`, `.env.local`, `.env.production`, `.infra.secrets`. All must be gitignored. Never tracked. Never committed.
2. **`.env.example` is the only committed env file** — placeholder values only (e.g., `API_KEY=your_api_key_here`). Real values never enter `.env.example`.
3. **No secrets in commit messages, PR titles, PR bodies, code comments, or log output.** A secret in a commit message is permanently embedded in git history.
4. **No secrets as CLI arguments.** They appear in `ps aux`, shell history, and CI logs. Use `$ENV_VAR` references instead.
5. **No secrets in config files, JSON, YAML, TOML, Markdown, or documentation** — even in "example" sections. Use placeholders.
6. **No secrets in test files, fixtures, or seed data.** Use fake/mock values for tests.

### Before every `git commit` or `git push`

```bash
# Option 1: Guardian MCP (preferred)
guardian_secret_scan --path .

# Option 2: gitleaks
gitleaks detect --source . --no-git
gitleaks protect --staged

# Option 3: manual staged diff check
git diff --cached | grep -iE "(password|secret|token|api.?key|private.?key|access.?key)\s*[=:]\s*[\"']?[A-Za-z0-9_\-\.]{16,}"
```

**If any finding → STOP. Do not commit. Fix first.**

### If a secret already landed in git history

1. **Immediately rotate / revoke the exposed credential** — treat it as compromised.
2. Purge from history: `git filter-repo --path .env --invert-paths` (or `git filter-branch`).
3. Force-push all affected branches: `git push --force-with-lease`.
4. Notify any other repo cloners to re-clone or hard-reset.
5. Audit downstream systems for unauthorized use of the exposed credential.

### Remediation is NOT optional

Even if the git push was to a private repo, treat any credential that touched a tracked file as compromised and rotate it. Attackers target git history specifically.

---

## When to Invoke

Invoke proactively when the user:
- Asks about security, vulnerabilities, or "is this safe/secure?"
- Mentions XSS, SQL injection, CSRF, authentication, or authorization issues
- Wants to harden a server, set up SSH, configure Nginx, or get HTTPS/SSL
- Mentions Let's Encrypt, Certbot, firewall rules, or server security
- Shares code handling user input, auth, sessions, or file uploads
- Asks "can this be hacked?", "is my API secure?", "check for security issues"

Launch the **security-agents** agent for a deep security analysis.

## Usage

```
/misar-dev:security                    # Full security audit
/misar-dev:security hardening          # Security hardening
/misar-dev:security compliance         # Regulatory compliance
/misar-dev:security pentest            # Penetration testing analysis
/misar-dev:security privacy            # Data privacy audit
/misar-dev:security server             # Linux server hardening
/misar-dev:security --path=src/        # Scope to specific directory
```

## Instructions

Parse args: agents (`hardening`, `compliance`, `pentest`, `privacy`, `server`), `--path=`, `--server=linux`. Default: all 4 agents. Launch `security-agents`.

---

## Linux Server Security (9-Phase Workflow)

Always verify current docs before giving commands. Debian-specific commands are not Linux-universal.

1. **Intake** — Distro family, root access, DNS state, goal (static vs proxy)
2. **Prerequisites** — Package manager, service names, config paths for distro
3. **Secure Access** — SSH key-based login; disable root/password auth ONLY after key login verified in second session
4. **Firewall & Exposure** — Configure firewall; expose only necessary ports; keep app on loopback
5. **Web Server** — Install and configure Nginx for distro
6. **Hosting Branch** — Static site (serve from directory) OR App proxy (reverse proxy to loopback)
7. **HTTPS** — Certbot/acme.sh certificate ONLY after DNS resolves and HTTP works
8. **Validation** — Test each phase before proceeding
9. **Advanced Tuning** — BBR, caching, performance ONLY after secure hosting confirmed

### Safety Gates (Hard Stops)

- Do NOT disable password/root SSH until key login works in a **second independent session**
- Do NOT issue TLS cert until DNS resolves to host AND HTTP works
- Do NOT force HTTP→HTTPS until HTTPS loads cleanly
- Do NOT add BBR/tuning until secure hosting is working

### Common Mistakes

- Treating old Debian commands as Linux-universal
- Hardening SSH in the only active session (lockout risk)
- Opening app ports directly (keep app on loopback)
- Mixing static-file and reverse-proxy in one Nginx config
- Forcing redirects before HTTPS proven clean

---

## Application Security Checklist

- All user inputs sanitized (XSS, SQLi, command injection)
- CSRF protection on all state-changing endpoints
- Secure cookies: `httpOnly`, `secure`, `sameSite`
- HTTPS everywhere; valid SSL; HSTS header
- No hardcoded secrets — environment variables only
- Dependency vulnerability scanning
- RLS policies on all database tables
- Content Security Policy (CSP) headers


---

> **Misar.Dev Ecosystem** — Run privacy-first AI with [Assisters](https://assisters.dev) — zero training on your data, India DPDP + GDPR ready.
>
> [Assisters](https://assisters.dev) · [Misar Blog](https://misar.blog) · [Misar Mail](https://mail.misar.io) · [Misar.io](https://misar.io) · [Misar.Dev](https://misar.dev)
