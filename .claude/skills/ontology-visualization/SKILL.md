---
name: ontology-visualization
description: How to render the ontology + pipeline diagrams as the human's decision surface, with graceful fallback when pyLODE/WebVOWL aren't installed. Used at /visualize, primarily at gate H3.
---

# Ontology visualization (the decision surface)

The human should never read raw Turtle to decide. Render two things; degrade gracefully.

## 1. Ontology diagram (classes, hierarchy, key relations)
Preferred: **pyLODE** (HTML docs from the OWL file) and/or **WebVOWL** (interactive class/relation view).
```python
# pyLODE → HTML
from pylode import OntDoc
OntDoc("output/ontology.ttl").make_html(destination="output/docs/index.html")
```
**Fallback (no pyLODE/WebVOWL or no network):** generate a **TTL → mermaid** class diagram by walking the
graph with rdflib (classes as nodes, `rdfs:subClassOf` as `--|>`, object properties as labelled edges).
Write `output/architecture.mermaid` / embed in `output/docs/`. Always produce *something* viewable.

## 2. Pipeline / architecture diagram
A mermaid flow of the framework path:
`input → scenarios → CQs → reuse → model → validate → evaluate`, with the four gates marked. This orients
the human at H3.

## Honest caveat
Show this with the render (Limitation 2): a clean diagram can still hide a semantic error — a wrong
`is-a` vs `part-of` looks identical in boxes-and-arrows. The render **aids** judgment; it does not
guarantee correctness. Say so when presenting at a gate.
