# Rule: provenance policy

The provenance level is **input-driven** and **confirmed by the human at H2**. The ontology declares
**only the chosen level's** properties; the pipeline populates to that depth. More provenance = more
data + extraction cost — pick only what the CQs require. Full reference: `provenance-levels.md`.

| Level | What it records | Libraries | Pick when |
|---|---|---|---|
| **L1** source-level | each entity's origin source/document/dataset | `rdflib` + Dublin Core (`dcterms:source`, `dcterms:created`) | clean structured input, deterministic mapping, low stakes |
| **L2** statement-level + evidence + confidence | per fact: source + evidence snippet + confidence | `rdflib` with **RDF-star** | LLM extraction (audit hallucination), scientific/citation, CQs about source/conflict/trust — the common default |
| **L3** full PROV-O activity chain | Entity/Activity/Agent: which run, model/prompt, derivation chains, timestamps | the `prov` library and/or PROV-O via `rdflib` | audit / compliance / regulatory, or a provenance trail is itself a requirement |

## Discipline
- **L2 during the build uses RDF-star** in the in-memory rdflib store; it becomes Neo4j **edge
  properties** only *after* the optional migration (§11) — never a build-time DB dependency.
- The build's **process-provenance** (the git-versioned project memory, one commit per gate) is
  symmetric to this data-provenance — see `memory-policy.md`.
- Don't over-declare: an L1 project must not carry L2/L3 properties.
