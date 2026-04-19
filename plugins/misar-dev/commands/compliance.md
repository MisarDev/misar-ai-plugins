---
allowed-tools: ["Bash", "Glob", "Grep", "Read", "Write", "Edit", "Agent"]
description: "Compliance audit — 49 global frameworks across 7 tiers: International, Healthcare, Americas, Europe, Asia-Pacific, Middle East/Africa, Eastern Europe."
argument-hint: "[tier] [framework] [--path=src/]"
---

# Compliance Audit

Launch the **compliance-agents** agent to audit against global regulatory compliance frameworks.

## Interactive Prompting

Before launching, check which flags were supplied. Ask for any that are missing in a **single `AskUserQuestion` call**.

**Tier** (ask if not provided):

- "Which compliance tier do you want to audit?"
- `tier-1` — International Standards (GDPR, ISO 27001, SOC 2, WCAG)
- `tier-2` — Healthcare and Specialty (HIPAA, PCI-DSS, COPPA, FERPA)
- `tier-3` — Americas (CCPA, LGPD, PIPEDA, Brazil, Canada)
- `tier-4` — Europe (UK GDPR, ePrivacy, German TTDSG, French DSA)
- `tier-5` — Asia-Pacific (PDPA, DPDP India, PIPL China, APPs Australia)
- `tier-6` — Middle East and Africa (PDPL Saudi, POPIA South Africa)
- `tier-7` — Eastern Europe and CIS (Russian FZ-152, Kazakhstan)
- Default: `tier-1`

**Framework** (ask if not provided — optional, narrows to one framework):

- "Which specific framework? (leave blank to audit the full tier)"
- Examples: `gdpr`, `ccpa`, `soc2`, `hipaa`, `dpdp`, `pipl`, `popia`
- Default: all frameworks in the selected tier

**Path** (ask if `--path=` not provided):

- "Which source path to audit?"
- Default: auto-detect from cwd (uses `src/` if present, else `.`)

## Argument Parsing

1. Tier word — `tier-1` through `tier-7`
2. Framework word — specific framework name
3. `--path=` — source directory (default: auto-detect)

Launch `compliance-agents` with all resolved parameters.
