---
description: Build the ontology (classes → hierarchy → properties) bounded by the frozen CQs + H2 decisions → ontology.ttl. Leads to H3.
---

Use the **modeling-agent** (`.claude/agents/modeling-agent.md`). Only run after H1 (CQs frozen) and H2
(direction confirmed). Steps 3–5: enumerate terms → define classes + hierarchy → define properties,
**import/align reused vocabularies** instead of redrawing them, bounded by the chosen **OWL profile**.
Declare provenance properties for the **chosen level only**.

Every element must trace to a CQ — self-check with `/check-scope` and drop orphans. Serialise to
`output/ontology.ttl` per `ttl-conventions.md`. Keep the build in-memory (rdflib); no DB, no credentials.
Then run `/visualize` and present **gate H3** (review the rendered structure). Do not self-judge
correctness or fitness — that is `/validate` and `/eval`.
