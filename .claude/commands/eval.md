---
description: Fitness — the scorecard (CQ coverage, structural, quality, OntoClean) → evaluation_report.md. Leads to H4.
---

Use the **evaluation-agent** (`.claude/agents/evaluation-agent.md`). Produce `output/evaluation_report.md`:
1. **CQ coverage (headline)** — run each CQ's SPARQL template; report % answerable.
2. **Structural metrics** — depth, breadth, class/property ratio, richness.
3. **Quality dimensions** — accuracy, completeness, conciseness, consistency, clarity (qualitative,
   model-judged — flag as not ground truth).
4. **OntoClean** — rigidity/identity/unity (the one non-circular signal; standard, not optional).
5. **Downstream-task hook** — leave the named slot; do not fill it here.

Write results to `events.jsonl`. **Report the scores; never optimise toward them** (Goodhart). Low
coverage → send findings back to improve the model (or the CQs, at a gate) — never tune the metric.
Pairs with `/validate` for gate **H4** (iterate vs. accept).
