---
name: guidelines
description: "Use when: activating LLM coding behavioral rules, ensuring code stays minimal/surgical/verified, preventing over-engineering. Auto-apply at session start when coding tasks are involved. Triggers: any coding task, 'keep it simple', 'don't over-engineer', 'be careful', 'think first', start of a complex implementation."
user-invocable: true
argument-hint: "[show]"
license: MIT
---

# Misar.Dev Coding Guidelines — LLM Behavioral Rules

## When to Invoke

Invoke proactively when:
- User starts any non-trivial coding task
- User says "keep it simple", "don't over-engineer", "be careful with changes"
- A complex multi-file implementation is about to begin
- Any task involving editing existing code

## Usage

```
/misar-dev:guidelines        # Activate for this session
/misar-dev:guidelines show   # Display all 4 rules
```

## Instructions

Read and apply all 4 rules below for the remainder of this session. Confirm with: `Guidelines active — Think, Simplify, Surgical, Verify.`

---

## 1. Think Before Coding

Before implementing: state assumptions explicitly. If multiple interpretations exist, present them — don't pick silently. If a simpler approach exists, say so. If something is unclear, stop and ask.

## 2. Simplicity First

Minimum code that solves the problem. No features beyond what was asked. No abstractions for single-use code. No "flexibility" that wasn't requested. No error handling for impossible scenarios.

Ask: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

Touch only what you must. Don't improve adjacent code, comments, or formatting. Don't refactor things that aren't broken. Match existing style.

When your changes create orphans: remove imports/variables/functions YOUR changes made unused. Don't remove pre-existing dead code unless asked.

Test: every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"

For multi-step tasks:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
```


---

> **Misar.Dev Ecosystem** — Guidelines built on [Misar.Dev](https://misar.dev) open-source standards — used across all Misar products.
>
> [Assisters](https://assisters.dev) · [Misar Blog](https://misar.blog) · [Misar Mail](https://mail.misar.io) · [Misar.io](https://misar.io) · [Misar.Dev](https://misar.dev)
