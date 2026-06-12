---
name: owl-validation
description: How to check formal correctness — reasoner consistency, SHACL, and pitfall scan — with honest fallbacks when a reasoner runtime is missing. Used by the validation-agent for /validate.
---

# OWL validation (correctness, not truth)

Answers "is it formally correct?" — never "is it true?" (Limitation 3). Checker ≠ builder: report,
never edit.

## 1. Reasoner (consistency + satisfiability)
Pick by the chosen OWL profile:
- **EL → ELK** (Java) · **QL → Ontop** (Java) · **RL → owlrl** (pure Python on rdflib) · **DL → HermiT**
  (ships with owlready2, Java).
- Report: is the ontology **consistent**? any **unsatisfiable** classes (list them)?
- **Honest fallback:** if the profile's reasoner needs a runtime that isn't present (e.g. Java), say so
  and run the available pure-Python path (owlrl/rdflib) instead. Never report a check that did not run
  (Limitation 5). Example owlrl pass:
  ```python
  import rdflib, owlrl
  g = rdflib.Graph().parse("output/ontology.ttl", format="turtle")
  owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(g)  # materialise; surfaces clashes
  ```

## 2. SHACL (structural constraints)
Validate against the shapes with **pySHACL**:
```python
from pyshacl import validate
conforms, _, report = validate("output/ontology.ttl", shacl_graph="output/shapes.ttl")
```
Report `conforms` + each violation (focus node, constraint, message).

## 3. Pitfall scan
Run **OOPS!** (web API) or a local equivalent; report pitfalls by severity (critical / important /
minor). Common ones: missing domain/range, missing inverses, cycles in the hierarchy, unconnected
classes.

## Output
Short pass/fail per check + detail → `events.jsonl` (via the orchestrator). Critical issues → back to the
modeling-agent (3-attempt bound, then escalate). Remember: green = consistent, not true; and the same
model reviews itself (catches carelessness, not a shared blind spot).
