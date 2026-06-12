# Provenance Levels — Internal Reference

Three levels. The scoping-agent selects one per project from the input + CQs (Human Gate). The
ontology declares only the chosen level's properties; the pipeline populates to that depth.
More provenance = more data + extraction cost — pick only what the CQs require.

## L1 — Source-level
Each entity records its origin source / document / dataset. Coarse, cheap.
- When: clean structured input, deterministic mapping, low stakes, no per-fact verifiability needed.
- Libraries: `rdflib` + Dublin Core Terms (`dcterms:source`, `dcterms:created`). Property graph → node properties.

## L2 — Statement-level + evidence + confidence
Each relationship/fact records source + evidence snippet + confidence. Default for LLM-extracted or
scientific graphs where facts must be individually verifiable.
- When: LLM extraction (audit hallucination), scientific/citation domains, CQs about source/conflict/trust.
- Libraries: RDF graph → `rdflib` with RDF-star. Property graph (Neo4j) → relationship/edge properties
  (native, no extra lib). PROV-O subset for the property names.

## L3 — Full PROV-O activity chain
Entity / Activity / Agent: which extraction run, which model/prompt, derivation chains, timestamps.
Auditable end-to-end.
- When: audit / compliance / regulatory, or when a full provenance trail is itself a requirement.
- Libraries: the `prov` Python library (W3C PROV) and/or the PROV-O ontology via `rdflib`.

## Selection rule (input-driven, confirmed at a Human Gate)
- structured DB + deterministic + low stakes → **L1**
- document corpus + LLM extraction, OR scientific/citation, OR CQs about source/conflict → **L2**
- audit / compliance / regulatory, OR provenance trail is a stated requirement → **L3**
