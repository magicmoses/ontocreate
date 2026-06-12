---
name: ontology-evaluation
description: How to produce the fitness scorecard — CQ coverage, structural metrics, quality dimensions, OntoClean — without adding circular internal metrics. Used by the evaluation-agent for /eval.
---

# Ontology evaluation (fitness, not correctness)

Answers "is it good (fit for purpose)?", grounded in Gómez-Pérez. Distinct from validation. Output:
`output/evaluation_report.md`.

## 1. CQ coverage (the headline)
Run each CQ's SPARQL template against the ontology; a CQ "passes" if its query is well-formed and returns
a non-empty, on-shape answer. Report **% answerable** + the per-CQ table.
```python
import rdflib
g = rdflib.Graph().parse("output/ontology.ttl", format="turtle")
ok = sum(1 for q in cq_templates if len(list(g.query(q))) > 0)
coverage = ok / len(cq_templates)
```

## 2. Structural metrics
Depth (max subclass chain), breadth (avg children), class/property ratio, richness (relations per class).
Report the numbers plainly; they describe shape, not quality.

## 3. Quality dimensions (qualitative — flag as such)
Accuracy, completeness, conciseness, consistency, clarity — **model-judged/heuristic, NOT ground truth**
(Limitation 1). Present as a reasoned opinion, never as verified external correctness.

## 4. OntoClean (the one non-circular signal — standard, not optional)
Check meta-properties on the taxonomy: **rigidity**, **identity**, **unity**. Flag taxonomic errors
(e.g. a rigid class subclassing an anti-rigid one). Independent of the CQs, so it's the non-circular
check — always include it.

## 5. Downstream-task hook
Leave a **named slot** where a domain-specific task evaluation attaches at the APPLICATION layer. Do not
fill it in the framework core.

## Discipline
**Do not add further internal metrics** — more numbers = false reassurance, not rigor. **Report scores;
never optimise toward them** (Goodhart). Low coverage → send findings back to improve the model (or the
CQs, at a gate). Write results to `events.jsonl`. Pairs with `/validate` for gate H4.
