---
name: security
description: "Use when: security review, vulnerability scanning, hardening a server, SSH setup, Nginx/HTTPS configuration, Let's Encrypt certificates, data privacy audit, penetration testing, checking for XSS/SQLi/CSRF, GDPR compliance, API security. Triggers: 'security audit', 'is my app secure', 'harden my server', 'setup HTTPS', 'check for vulnerabilities', 'SSH setup', 'firewall rules', 'is this safe', 'security review'."
user-invocable: true
argument-hint: "[agents] [--path=src/] [--server=linux]"
---

# Security Audit

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
