---
description: Render the ontology + pipeline diagrams — the human's decision surface (primarily at H3).
---

Act as the **orchestrator-agent**, using the **ontology-visualization** skill
(`.claude/skills/ontology-visualization/SKILL.md`). Render, from the current `output/ontology.ttl`:
- an **ontology diagram** — classes, hierarchy, key relationships (pyLODE/WebVOWL, or a TTL→mermaid/
  graphviz fallback when those aren't installed);
- a **pipeline/architecture diagram** — input → scenarios → CQs → reuse → model → validate → evaluate.

Write to `output/docs/` and/or `output/architecture.(svg|mermaid)`. The human should never read raw
Turtle to decide. **Caveat (Limitation 2):** a clean diagram can still hide a semantic error — the render
aids judgment, it does not guarantee it. Say so when presenting at a gate. $ARGUMENTS
