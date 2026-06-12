---
description: Start a gated refinement cycle from a gap report — produce the next ontology version.
argument-hint: [path to gap report in input/]
---

Act as the **orchestrator-agent** to run a **content/semantic refinement cycle** (§20a) — human-gated,
never silent mutation. A gap report (unmapped terms, frequent co-occurrences, clusters with no class,
implied relations) has re-entered as an `input/` type.

1. **input-agent** ingests + ranks the gap report (by frequency / how much data doesn't fit).
2. **scenario-and-cq-agent**: does a candidate warrant a **new CQ**? If yes, draft it. If it earns no
   CQ, it stays out — scope discipline holds.
3. **GATE H1** — the human decides on scope expansion (data proposes, the human disposes).
4. On accept → modeling-agent extends → `/validate` → `/eval` → bump the **ontology version** in entity
   memory; commit. Each refinement cycle is an auditable set of commits.

Stage-2 only reports gaps; it never edits the model directly. Input: $ARGUMENTS
