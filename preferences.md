# Preferences

Your personal defaults, read by the framework to pre-fill choices at the gates. **Edit freely.**

These only **set defaults** — you still decide at every gate, and any choice here can be overridden in
the moment. They are user-scoped (they carry across projects), unlike the per-project decision log in
`output/`.

```yaml
# Default OWL profile suggestion at H2 (EL | QL | RL | DL). EL is a safe default.
owl_profile: EL

# How aggressively to limit scope. "aggressive" = cut anything that doesn't clearly earn a CQ.
scope_posture: aggressive

# Storage preference. "oss" keeps everything credential-free (rdflib / Oxigraph / Fuseki).
# Neo4j is still available any time via /migrate-neo4j.
storage: oss

# How much the framework writes to you. "terse" = short summaries, depth goes to files.
explanation_length: terse

# How eagerly to reuse existing ontologies/vocabularies before building new (low | medium | high).
reuse_aggressiveness: high
```

---

**Guardrail (do not change the intent):** preferences may set defaults and tone, but must **never**
encode anything that suppresses honest feedback, hides problems, or forces agreement. The framework
stays direct even when a preference would make it more comfortable to soften things.
