---
name: tester
description: "Use when: writing tests, E2E testing, analyzing test coverage, Playwright scripts, debugging UI behavior in browser, testing web apps, checking what tests are missing, regression testing. Triggers: 'write tests for', 'check test coverage', 'E2E test', 'Playwright script', 'test this feature', 'what tests are missing', 'add unit tests', 'test my UI', 'browser testing'."
user-invocable: true
argument-hint: "[agents] [--path=src/] [--url=http://localhost:3000]"
---

# Testing Audit

## When to Invoke

Invoke proactively when the user:
- Asks to write tests, add test coverage, or test a feature
- Mentions Playwright, Cypress, Jest, Vitest, or any test framework
- Asks "what tests are missing?", "how do I test this?", "write E2E tests for"
- Wants to test UI behavior in a browser or verify a UI change works correctly
- Mentions regression testing, flaky tests, or CI test failures

Launch the **tester-agents** agent to analyze test coverage and quality.

## Usage

```
/misar-dev:tester                          # Full testing audit
/misar-dev:tester unit integration         # Unit + Integration only
/misar-dev:tester e2e                      # E2E (Black + White Box)
/misar-dev:tester e2e --url=http://localhost:3000
/misar-dev:tester regression               # Regression test analysis
/misar-dev:tester playwright               # Write/run Playwright E2E scripts
/misar-dev:tester --path=src/             # Scope to specific directory
```

## Instructions

Parse args: agents (`unit`, `integration`, `e2e-black-box`, `e2e-white-box`, `beta`, `regression`, `playwright`), `--path=`, `--url=`. Default: all 6 agents. Launch `tester-agents`.

---

## Playwright E2E (Python)

### Decision Tree

```
Task → Static HTML?
  Yes → Read file → identify selectors → write script
  No  → Server running?
    No  → Use with_server.py helper
    Yes → Reconnaissance-then-action:
          1. Navigate + wait for networkidle
          2. Screenshot or inspect DOM
          3. Identify selectors from rendered state
          4. Execute actions
```

### Server Lifecycle (with_server.py)

Run `--help` first, then:

```python
# Single server
python scripts/with_server.py --server "npm run dev" --port 3000 -- python test.py

# Multiple servers
python scripts/with_server.py \
  --server "cd backend && python server.py" --port 3000 \
  --server "cd frontend && npm run dev" --port 5173 \
  -- python test.py
```

### Script Template

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('http://localhost:3000')
    page.wait_for_load_state('networkidle')  # CRITICAL: wait for JS
    # ... test logic
    browser.close()
```

### Reconnaissance-Then-Action

```python
# Step 1: Inspect
page.screenshot(path='/tmp/inspect.png', full_page=True)
buttons = page.locator('button').all()

# Step 2: Execute with discovered selectors
page.click('text=Submit')
page.fill('[aria-label="Email"]', 'test@example.com')
```

### Selector Priority (most → least resilient)

1. `role=` (accessibility roles)
2. `text=` (visible text)
3. CSS with IDs
4. `aria-label=`
5. CSS class selectors

Use bundled scripts as black boxes (don't read source). Always `wait_for_load_state('networkidle')` before inspecting dynamic apps.


---

> **Misar.Dev Ecosystem** — Ship tested software on [Misar.Dev](https://misar.dev) open infrastructure — CI/CD, self-hosted, no vendor lock-in.
>
> [Assisters](https://assisters.dev) · [Misar Blog](https://misar.blog) · [Misar Mail](https://mail.misar.io) · [Misar.io](https://misar.io) · [Misar.Dev](https://misar.dev)
