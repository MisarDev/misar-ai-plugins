---
name: qa
description: "Use when: code review, finding bugs, code quality check, technical debt analysis, standards compliance, reviewing a PR/diff, Next.js pattern validation, TypeScript strict mode audit, checking for anti-patterns. Triggers: 'review my code', 'find bugs in', 'code quality', 'technical debt', 'review this PR', 'check for issues', 'audit the codebase', 'code review'."
user-invocable: true
argument-hint: "[agents] [--path=src/] [--framework=nextjs]"
---

# QA Audit

## When to Invoke

Invoke proactively when the user:
- Asks for a code review on any file, function, or PR diff
- Says "review my code", "find bugs", "check this for issues", "code quality"
- Mentions technical debt, dead code, or refactoring candidates
- Completes a feature and wants it reviewed before committing
- Mentions Next.js and wants pattern validation (RSC, hydration, async)
- Says "is this code good?", "any issues with this?", "review before I push"

Launch the **qa-agents** agent to perform code quality analysis.

## Usage

```
/misar-dev:qa                          # Full QA audit
/misar-dev:qa code-review              # Code review only
/misar-dev:qa bugs tech-debt           # Bug detection + tech debt
/misar-dev:qa standards                # Standards compliance
/misar-dev:qa next-patterns            # Next.js 15+ pattern validation
/misar-dev:qa --path=src/lib/          # Scope to specific directory
/misar-dev:qa --framework=nextjs       # Framework-specific rules
```

## Instructions

Parse args: agents (`code-review`, `standards`, `bugs`, `tech-debt`, `next-patterns`), `--path=`, `--framework=`. Default: all 4 agents. Launch `qa-agents`.

---

## Next.js 15+ Quality Rules

### RSC Boundary Violations (Bugs)
- `'use client'` component importing server-only code → build error
- Non-serializable props (functions, class instances) across RSC boundary → runtime error
- `async` client components → not supported
- Server Actions without `'use server'` directive → silent failures

### Async API Patterns (Breaking Change in v15)
```typescript
// ❌ Old (breaks in v15)
const { id } = params
const cookieStore = cookies()

// ✅ New
const { id } = await params
const cookieStore = await cookies()
```
Affected: `params`, `searchParams`, `cookies()`, `headers()`, `draftMode()`

### Hydration Error Sources
- Server/client render mismatch (`Date.now()`, `Math.random()` in render)
- `useSearchParams()` without `<Suspense>` wrapper
- Browser-only APIs (`window`, `document`, `localStorage`) in Server Components

### TypeScript Rules
- `as any` → banned; use `as unknown as TargetType` or fix the type
- Missing return types on exported functions
- Prefer `interface` for object shapes, `type` for unions
- Non-null assertion (`!`) requires comment explaining why it's safe

### General Code Quality
- No `console.log` in production (use proper logging)
- No hardcoded URLs, tokens, or credentials
- Error boundaries around async component trees
- Loading states for all async operations
- No `useEffect` for data fetching (use Server Components or SWR/React Query)
