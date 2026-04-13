---
name: uiux-designer
description: "Use when: designing UI/UX, creating design systems, choosing colors/fonts/layouts, improving visual design, building product interfaces, reviewing UI code, asking about design direction, brand identity, component specs, dark mode, mobile design, shadcn/ui, color palette, typography. Triggers: 'make it look better', 'design a dashboard', 'what colors should I use', 'improve the UI', 'create a design system', 'choose fonts', 'design critique', 'UI looks generic'."
user-invocable: true
argument-hint: "[agents] [--project=desc] [--platform=web] [--component=button] [--style=brutalist]"
---

# UI/UX Designer

## When to Invoke

Invoke proactively when the user:
- Asks about visual design, UI, or "how it looks" in any project
- Mentions colors, fonts, typography, spacing, layouts, or visual hierarchy
- Says "make it look better", "redesign", "refresh the UI", "design this"
- Starts building a new product or component without a defined design system
- Shares a Figma link or screenshot for implementation guidance
- Mentions shadcn/ui, Tailwind, Radix, or any UI library setup

Launch the **uiux-designer-agents** agent for comprehensive design consultation.

## Usage

```
/misar-dev:uiux-designer                             # Full consultation
/misar-dev:uiux-designer analyze                     # Project analysis
/misar-dev:uiux-designer guidelines                  # Design system generation
/misar-dev:uiux-designer brand                       # Brand identity recommendations
/misar-dev:uiux-designer component --component=modal # Component-specific advice
/misar-dev:uiux-designer critique                    # Critique existing design
/misar-dev:uiux-designer colorize                    # 60-30-10 color introduction
/misar-dev:uiux-designer audit-guidelines            # Audit against Vercel Web Interface Guidelines
/misar-dev:uiux-designer --platform=mobile-ios       # iOS HIG guidance
/misar-dev:uiux-designer --platform=mobile-android   # Material Design 3 guidance
/misar-dev:uiux-designer --style=brutalist           # Set aesthetic direction
```

## Instructions

Parse args: agents (`analyze`, `guidelines`, `brand`, `component`, `critique`, `colorize`, `audit-guidelines`), `--platform=` (web/mobile-ios/mobile-android/desktop), `--component=`, `--style=` (brutalist/maximalist/retro-futuristic/luxury/playful/minimal). Default: full consultation. Launch `uiux-designer-agents`.

---

## Aesthetic Direction

**Establish bold direction BEFORE writing code. Reject cookie-cutter defaults.**
Avoid: Inter/Roboto overuse, purple gradient clichés, generic shadcn defaults.

Styles: **Brutalist** (raw structure, functional type) · **Maximalist** (layered complexity, bold patterns) · **Retro-futuristic** (nostalgic tech, modern execution) · **Luxury** (restraint, whitespace, editorial) · **Playful** (rounded forms, color pops, kinetic type)

**5 design pillars:**
1. **Typography** — Distinctive font pairs, strategic size hierarchy, not defaults
2. **Color & Theme** — Cohesive CSS variable palettes; one dominant + secondary + sharp accent
3. **Motion** — CSS animations, scroll effects; respect `prefers-reduced-motion`
4. **Spatial Composition** — Asymmetrical layouts, deliberate grid-breaking, whitespace tension
5. **Backgrounds & Details** — Gradient meshes, texture, patterns

---

## Color Strategy (60-30-10)

**Max 2–4 colors beyond neutrals. OKLCH color space.**

- **60%** — Dominant: backgrounds, large surfaces
- **30%** — Secondary: cards, sections, supporting UI
- **10%** — Accent: CTAs, links, icons, hover states

Order: semantic (state) → accent (primary actions) → background tinting → data viz → typography/borders → decorative.

Avoid: pure grays (use tinted neutrals), color-only indicators, pure black/white for large areas.

---

## UI/UX Priority Rules

| Priority | Category | Key Rules |
|----------|----------|-----------|
| 1 | **Accessibility** | 4.5:1 text contrast, 3:1 UI contrast, keyboard nav, ARIA |
| 2 | **Touch & Interaction** | 44×44px min targets, tap feedback |
| 3 | **Performance** | LCP < 2.5s, CLS < 0.1, INP < 200ms |
| 4 | **Style Consistency** | No emoji icons, match style to product type |
| 5 | **Layout & Responsive** | Mobile-first, 320/768/1024/1440px breakpoints |
| 6 | **Typography & Color** | Fluid scaling, semantic tokens, WCAG contrast |
| 7 | **Animation** | 150–300ms, meaning-driven, ease-out entrances |
| 8 | **Forms & Feedback** | Visible labels, inline errors, real-time validation |
| 9 | **Navigation** | Bottom nav ≤5 items, deep linking, consistent back |
| 10 | **Charts & Data** | Match chart type, accessible palettes, always legend |

**Platform:** iOS — SF Pro, 44pt targets, HIG. Android — Material Design 3, 48dp, dynamic color.

---

## shadcn/ui Enforcement

Lifecycle: search registries → add → `--dry-run`/`--diff` → apply.
- Colors: `bg-primary` not raw hex; semantic tokens
- Spacing: `gap-*` not `space-x-*`; `size-8` not `w-8 h-8`
- Forms: `FieldGroup` + `Field`; `data-invalid` + `aria-invalid`
- Icons: `data-icon` attribute; pass as objects not strings
- Registries: @shadcn, @magicui, @tailark

---

## Vercel Guidelines Audit

When running `audit-guidelines`:
1. Fetch: `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`
2. Read specified files (prompt if none given)
3. Output `file:line` format — design, accessibility, UX issues
