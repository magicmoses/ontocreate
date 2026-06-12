---
description: (Optional, AFTER the build, OUTSIDE the loop) Generate a one-way, read-only Neo4j import kit. Needs credentials.
---

Act as the **orchestrator-agent**, but this runs **after** the build and **outside** the autonomous,
credential-free loop. Read `secrets-policy.md` first (it is referenced **only** here).

Generate into `migration/` (do **not** modify `output/ontology.ttl` — migration is one-way, read-only):
- a **neosemantics (n10s)** import script + config that imports the canonical `.ttl`;
- a short **mapping note**: RDF resources → nodes, `rdf:type` → labels, literal properties → node
  properties, object properties → relationships; the OWL reasoning layer becomes inert structure (Neo4j
  is not a reasoner).

**Secrets:** credentials live in `.env` (git-ignored); reference env vars (e.g. `NEO4J_PASSWORD`), never
the literal value; never write secrets into TTL, the logs, memory, or a visualization; least-privilege
DB user. The `.ttl` stays canonical; the Neo4j copy is a rebuildable, traversal-optimized projection.
$ARGUMENTS
