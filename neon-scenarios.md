# NeOn Scenarios — Internal Reference

Paraphrased, in our own words, for agents to consult. **Source (cite, do not copy):**
NeOn Methodology — Suárez-Figueroa, Gómez-Pérez, Fernández-López, Villazón-Terrazas et al.,
*Ontology Engineering in a Networked World*, Springer, 2012. Consult the original for the
authoritative, detailed guidelines.

## Meta-rules
- Scenarios are not exclusive — a real project usually combines several.
- Any combination always includes **Scenario 1**, which holds the core build activities.
- Early step: list candidate resources for the domain (existing ontologies, non-ontology resources,
  design patterns). What you find determines which scenarios apply.
- The framework classifies the active scenario(s) right after input ingestion; that classification
  sets the workflow path.

## Scenario 1 — Build from scratch (the core)
Develop without reuse. Start with a requirements spec (purpose, scope, target language, intended
users and uses, competency questions, a starter term list), then conceptualize → formalize →
implement. Every other scenario feeds its result back into this one.

## Scenario 2 — Re-engineer non-ontological resources
Convert existing non-ontology assets (databases, glossaries, thesauri, taxonomies, folksonomies)
into ontology fragments. Find candidates, judge them on coverage / precision / consensus, pick the
best, then reverse-engineer their structure, restate it as a conceptual model, and forward-engineer
it into an ontology. *(For us: the Motus DB schema is exactly this.)*

## Scenario 3 — Reuse ontologies as-is
A suitable ontology already exists. Search registries, check it against the requirements, compare
candidates on cost / clarity / quality, select, integrate unchanged. *(For us: MeSH, OBO.)*

## Scenario 4 — Reuse + adapt ontologies
Like 3, but the chosen ontology doesn't fit as-is, so modify it. The change can happen at any
abstraction level — requirements, conceptual model, formalization, or implementation — depending on
what needs adjusting.

## Scenario 5 — Reuse + merge ontologies
Several overlapping ontologies cover the domain. Align them, then optionally merge into one combined
resource.

## Scenario 6 — Reuse + merge + adapt ontologies
Like 5, but the merged result still needs re-engineering afterward to fit the purpose.

## Scenario 7 — Reuse design patterns
Apply proven modeling solutions (Ontology Design Patterns) from pattern libraries to recurring
modeling problems, instead of solving them ad hoc.

## Scenario 8 — Restructure
Reorganize the model to better fit the requirements: modularize, prune unneeded branches, extend
(add concepts/relations in breadth), or specialize (add depth/granularity).

## Scenario 9 — Localize
Make the ontology multilingual by translating its labels/terms into other languages using
multilingual linguistic resources.
