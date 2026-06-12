---
description: Run the within-project PROCESS feedback loop on the trajectory — process refinements only.
---

Use the **feedback-agent** (`.claude/agents/feedback-agent.md`). Read the trajectory
(`output/events.jsonl` + `project-memory.json`), diagnose **operational** failures only (tool misuse,
parse errors, wasted/repeated attempts, methodology slips, repeated scope violations), and propose /
auto-apply **process** refinements to **`output/refinements/`** (a dated note: symptom → diagnosis →
the process change).

Hard bounds: project-scoped (never the `.claude/` core), git-reversible, process-signals only — **never**
optimise eval scores or CQ-coverage (Goodhart), **never** touch semantic-modelling decisions (those stay
human-gated). Self-improvement here is operational, not content (Limitation 6) — say so. $ARGUMENTS
