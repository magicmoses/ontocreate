---
name: ontology-modeling
description: How to build classes, hierarchy, and properties bounded by the frozen CQs, the OWL profile, and the provenance level, and serialise to Turtle. Used by the modeling-agent for /draft-ontology.
---

# Ontology modeling (Steps 3–5)

Only after H1 (CQs frozen) + H2 (direction confirmed). Bounded by the frozen CQ-set and the H2 decisions.
Read `ttl-conventions.md` and `owl-profile-tradeoff.md`. Keep everything in-memory (rdflib) — no DB.

## Step 3 — enumerate terms
Pull candidate terms from the ORSD glossary + input pack (spaCy can help extract phrases). List before
you commit to classes.

## Step 4 — classes + hierarchy
- Create classes for terms that **answer a CQ**; set `rdfs:subClassOf` for the taxonomy.
- **Import/align reused vocabularies** (researcher's decision) — `owl:imports` or map with
  `rdfs:subClassOf`/`owl:equivalentClass`; do not redraw what you can reuse.
- Watch `is-a` vs `part-of` — a wrong subsumption looks fine in a diagram (Limitation 2).

## Step 5 — properties
- Object + datatype properties with `rdfs:domain`/`rdfs:range`, bounded by the **OWL profile** (don't use
  constructs the profile forbids — see `owl-profile-tradeoff.md`).
- Add characteristics (functional, transitive, …) only when a CQ needs the inference and the profile
  allows it.

## Provenance (chosen level only — `provenance-policy.md`)
- **L1:** `dcterms:source`, `dcterms:created`.
- **L2:** RDF-star statement-level evidence + confidence.
- **L3:** PROV-O Entity/Activity/Agent.
Declare only the chosen level. Don't over-declare.

## Limit the scope (continuous)
Before finishing, run the `scope-discipline` check: every class/property must trace to a CQ; remove
orphans. This is the cardinal rule, enforced at draft time too — not once at the end.

## Serialise
Write `output/ontology.ttl` per `ttl-conventions.md` (prefixes, CamelCase classes, lowerCamel
properties, `rdfs:label` + `rdfs:comment` on every term). Hand to `/validate` + `/eval` — never
self-judge (checker ≠ builder).
