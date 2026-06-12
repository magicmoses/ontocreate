---
description: Extract, cluster, and formalise competency questions (CQs) + write the ORSD. Leads to gate H1.
---

Use the **scenario-and-cq-agent** (`.claude/agents/scenario-and-cq-agent.md`). From the motivating
scenarios, extract **competency questions** — specific, testable, each answerable by a query. Cluster
into themes; merge/split/refine; drop CQs no scenario motivates. For each CQ write a **SPARQL template**
(these templates ARE the later evaluation).

Write the **ORSD** to `output/ORSD.md` (purpose, scope, proposed language/profile, users/uses, the CQ
set, starter glossary). Then present **gate H1** in the standard format: *[N CQs in M themes] · [they
fix the scope] · [reply `ok` to freeze, or what to add/cut/refine]*. **H1 is iterative** — revise until
the human accepts; nothing is modeled before then. On accept, the orchestrator freezes the CQ-set to
entity memory and commits.
