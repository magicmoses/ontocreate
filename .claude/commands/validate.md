---
description: Correctness — OWL reasoner consistency + SHACL + pitfall scan. Reports, never edits. Leads to H4.
---

Use the **validation-agent** (`.claude/agents/validation-agent.md`). On `output/ontology.ttl` run:
1. **Reasoner** for the chosen profile (EL→ELK, QL→Ontop, RL→owlrl, DL→HermiT) — consistency +
   unsatisfiable classes. If that reasoner's runtime is absent (e.g. Java), say so and fall back to the
   pure-Python path (owlrl/rdflib); never claim a check that did not run (Limitation 5).
2. **pySHACL** — structural constraints.
3. **Pitfall scan** — OOPS! (web API) or local equivalent, by severity.

Report a short pass/fail per check + detail; write results to `events.jsonl`. Critical issues → send
back to the modeling-agent (3-attempt bound, then escalate). A green reasoner means *consistent, not
true*. Checker ≠ builder — report only, never edit. Pairs with `/eval` for gate H4.
