---
name: ontology-reuse
description: How to find and judge existing vocabularies/ontologies via key-free registries and recommend reuse/extend/merge/build-new. Used by the researcher-agent for /find-reuse.
---

# Ontology reuse ("reuse before build")

Before drawing a new class, check whether a suitable vocabulary already exists (NeOn Scenarios 3–7,
`neon-scenarios.md`). Reuse aggressiveness follows `preferences.md`.

## Registries (pluggable, key-free)
- Choose the registry **from the input/domain**, never hardcode it. Defaults:
  - **LOV** (Linked Open Vocabularies) — general.
  - **EBI OLS** — life-science/biomedical terminologies.
- **Credential-free only.** A registry needing an API key (e.g. BioPortal) is out of the build — note it
  for Stage-2; do not call it here.

## Judging candidates (NeOn criteria)
For each candidate, assess: **coverage** of the CQs/glossary · **precision** (right granularity) ·
**consensus/adoption** · **quality** (maintenance, documentation) · **licence**. Prefer well-adopted,
permissively licensed vocabularies.

## Recommendation (per concept-cluster)
Map each cluster to one of:
- **reuse as-is** (Scenario 3) — import unchanged.
- **reuse + adapt** (4) — import then modify.
- **reuse + merge** (5/6) — align several overlapping vocabularies; merge if needed.
- **apply a design pattern** (7) — an ODP from ontologydesignpatterns.org.
- **build new** (1) — only when nothing fits the CQ test.

Cite candidate IRIs/prefixes. Never reuse something that fails the CQ-fit test just to avoid building.

## Output
Write the reuse decision to entity memory (vocabulary, mode, prefixes/IRIs) and add reused vocabularies
to semantic memory so the modeling-agent **imports** rather than redraws. Feeds gate H2.
