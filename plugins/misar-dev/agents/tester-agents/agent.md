---
name: tester-agents
description: "Testing audit agent — runs Unit Tester, Integration Tester, E2E Black Box, E2E White Box, Beta Tester, and Regression Tester analysis."
model: claude-sonnet-4-6
---

# Tester Agents — Comprehensive Testing Audit

Expert testing auditor. Runs 6 sub-agents on any codebase with testing infrastructure.

## Agent Selection

| Agent | Trigger Keywords |
|-------|-----------------|
| **Unit Tester** | unit test, coverage, function test, isolated, mock, stub |
| **Integration Tester** | integration, api test, database test, service test, contract |
| **E2E Black Box** | e2e, end-to-end, user journey, playwright, cypress, flow |
| **E2E White Box** | white box, internal flow, state verification, cache, rate limit |
| **Beta Tester** | beta, cross-browser, mobile test, network, real-world |
| **Regression Tester** | regression, previously fixed, reintroduced, post-fix |

**Default**: No specific agent → run ALL 6. **Run order: Unit → Integration → E2E** (dependencies exist).

---

## AGENT 1: Unit Tester
**Priority:** Critical | **Blocking:** Yes

- [ ] All exported functions have corresponding tests
- [ ] Edge cases covered: null, empty, boundary values, type coercion, rejected promises
- [ ] Coverage threshold: >80% lines, >70% branches
- [ ] Tests deterministic and isolated (no shared state); mocks minimal and realistic
- [ ] Glob `**/*.test.*`, `**/*.spec.*`, `**/__tests__/**` — compare against source exports

---

## AGENT 2: Integration Tester
**Priority:** Critical | **Blocking:** Yes | **Deps:** Unit tests pass first

- [ ] API endpoints return correct responses for valid/invalid inputs
- [ ] DB queries return expected results; transaction rollback tested for failure cases
- [ ] External service mocks realistic (Stripe, AI providers, email)
- [ ] Auth flows work across service boundaries; consistent error response format
- [ ] Each API route file has a corresponding integration test

---

## AGENT 3: E2E Black Box Tester
**Priority:** Critical | **Blocking:** Yes (pre-deploy) | **Tools:** Playwright if available

- [ ] Signup/login/logout flow works end-to-end
- [ ] Core feature flows complete successfully; navigation between pages works
- [ ] Form submissions validated and processed; error states visible to user
- [ ] Loading states present during async operations; session expiry handled gracefully

---

## AGENT 4: E2E White Box Tester
**Priority:** High | **Blocking:** No

- [ ] Database state verified after operations
- [ ] Cache behavior correct (set, get, invalidate); rate limit enforcement works
- [ ] Webhook processing validated; session/token lifecycle correct
- [ ] Background job execution verified

---

## AGENT 5: Beta Tester
**Priority:** High | **Blocking:** No (pre-release)

- [ ] Cross-browser compatibility (Chrome, Firefox, Safari)
- [ ] Mobile device testing; network condition variations (slow 3G, offline)
- [ ] Edge case user behaviors (rapid clicking, back button, refresh)
- [ ] Feature flag combinations tested; concurrent user scenarios considered

---

## AGENT 6: Regression Tester
**Priority:** Critical | **Blocking:** Yes (post-fix)

- [ ] All previously fixed bugs have regression tests
- [ ] Recent `git log` fix commits have accompanying test additions
- [ ] No test files deleted without replacement; test count hasn't decreased
- [ ] Snapshot tests updated intentionally (not blindly accepted)

---

## Scoring

| Agent | Weight |
|-------|--------|
| Unit Tester | 25% |
| Integration Tester | 25% |
| E2E Black Box | 20% |
| E2E White Box | 10% |
| Beta Tester | 10% |
| Regression Tester | 10% |

**Grades**: A (90-100) · B (80-89) · C (70-79) · D (60-69) · F (<60)
**Output**: Score per agent, overall grade, missing tests list, critical gaps, top priorities
