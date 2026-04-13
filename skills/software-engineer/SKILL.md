---
name: software-engineer
description: "Use when: building a project from PRD/specs/requirements, planning a new app, implementing a feature from a spec document, Next.js 15+ implementation, full-stack development, generating code from requirements, validating generated code. Triggers: 'build this from the PRD', 'implement this feature', 'plan this project', 'generate code for', 'start building', 'create this app', 'implement from spec'."
user-invocable: true
argument-hint: "[agents] [--prd=file.md] [--path=src/] [--framework=nextjs]"
---

# Software Engineer

## When to Invoke

Invoke proactively when the user:
- Provides a PRD, spec document, or requirements list and wants code built
- Says "build this", "implement this feature", "create this app from scratch"
- Needs a project plan before coding, or wants to validate generated code
- Mentions Next.js and needs RSC, Server Actions, or routing guidance
- Has a feature description and no existing code yet

Launch the **software-engineer-agents** agent to build projects from specifications.

## Usage

```
/misar-dev:software-engineer                     # Full pipeline from PRD
/misar-dev:software-engineer prd-analyze         # Analyze PRD only
/misar-dev:software-engineer plan                # Generate project plan
/misar-dev:software-engineer generate            # Generate code from plan
/misar-dev:software-engineer validate            # Validate generated code
/misar-dev:software-engineer recommend           # Next steps recommendations
/misar-dev:software-engineer next-best-practices # Audit against Next.js 15+ best practices
/misar-dev:software-engineer --prd=spec.md       # Use PRD from file
/misar-dev:software-engineer --path=src/         # Generate to specific path
/misar-dev:software-engineer --framework=nextjs  # Framework-specific guidance
```

## Instructions

Parse args: agents (`prd-analyze`, `plan`, `generate`, `validate`, `recommend`, `next-best-practices`), `--prd=`, `--path=`, `--framework=`. Default: all 5 agents. Launch `software-engineer-agents`.

---

## Next.js 15+ Best Practices

### RSC Boundaries
- Default to Server Components; `'use client'` only for interactivity/hooks/browser APIs
- Async client components not supported — put async logic in Server Components or Server Actions
- Non-serializable props (functions, class instances) cannot cross RSC boundary

### Async APIs (Breaking Change in v15)
```typescript
// Always await these in layouts/pages/Server Components:
const { id } = await params
const { q } = await searchParams
const cookieStore = await cookies()
const headersList = await headers()
```

### Directives
- `'use client'` — client-side rendering, hooks, browser APIs
- `'use server'` — Server Actions (called from client, run on server)
- `'use cache'` — persistent caching for functions/components

### Data Fetching Priority
1. **Server Components** — fetch directly, no API route needed
2. **Server Actions** — mutations, form submissions
3. **Route Handlers** — external webhooks, OAuth, third-party integrations only

Avoid waterfalls: use `Promise.all()` for parallel fetches.

### Navigation Hooks
`useRouter()` · `usePathname()` · `useSearchParams()` (wrap in Suspense) · `useParams()`

### Error Files
`error.tsx` (segment, must be `'use client'`) · `global-error.tsx` (root) · `not-found.tsx`

### Image Optimization
```typescript
<Image src={src} alt="..." width={800} height={600}
  placeholder="blur" blurDataURL={blurUrl}
  sizes="(max-width: 768px) 100vw, 50vw" />
```
Never use `<img>` — always `next/image`.

### Font & Metadata
```typescript
import { Inter } from 'next/font/google'
const inter = Inter({ subsets: ['latin'], display: 'swap' })

export const metadata: Metadata = { title: '...', description: '...' }
export async function generateMetadata({ params }): Promise<Metadata> { ... }
```

### Hydration Prevention
- Match server/client render output exactly
- Wrap `useSearchParams()` in `<Suspense>`
- No browser-only APIs in Server Components
- No `Math.random()`/`Date.now()` in render without `suppressHydrationWarning`

### Route Handlers
- Cannot have `page.tsx` in same directory as `route.ts`
- Use only for: external webhooks, OAuth callbacks, third-party integrations

---

## shadcn/ui Management

```bash
npx shadcn@latest add button        # Add component
npx shadcn@latest diff button       # Preview upstream changes
```

- Colors: `bg-primary` not raw hex — semantic tokens
- Spacing: `gap-*` not `space-x-*`; `size-8` not `w-8 h-8`
- Forms: `FieldGroup` + `Field`; `data-invalid` + `aria-invalid` for errors
