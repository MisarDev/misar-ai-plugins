---
description: "Testing audit — Unit, Integration, E2E, Beta, Regression test coverage."
argument-hint: "[agents] [--path=src/]"
---

Launch the **tester-agents** agent to analyze test coverage and quality.

1. Parse arguments: agents (`unit`, `integration`, `e2e-black-box`, `e2e-white-box`, `beta`, `regression`), path
2. Launch `tester-agents` with parsed parameters
3. The agent handles test framework detection, coverage mapping, gap analysis, and reporting.
