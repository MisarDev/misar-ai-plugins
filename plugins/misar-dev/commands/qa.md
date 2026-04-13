---
description: "Code quality audit — Code Reviewer, Standards, Bug Detective, Technical Debt."
argument-hint: "[agents] [--path=src/]"
---

Launch the **qa-agents** agent to perform code quality analysis.

1. Parse arguments: agents (`code-review`, `standards`, `bugs`, `tech-debt`), path (`--path=`)
2. Launch `qa-agents` with parsed parameters
3. The agent handles stack detection, file discovery, analysis, scoring, and reporting.
