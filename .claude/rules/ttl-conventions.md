# Rule: Turtle (.ttl) conventions

`output/ontology.ttl` is the **canonical artifact**. Keep it clean, portable, and human-reviewable.

## Prefixes & namespace
- Declare a clear base/ontology IRI and a short project prefix; reuse standard prefixes (`rdf:`, `rdfs:`,
  `owl:`, `xsd:`, `dcterms:`, `skos:`, plus any reused vocabularies' prefixes).
- Import reused vocabularies with `owl:imports`; align with `rdfs:subClassOf` / `owl:equivalentClass`.

## Naming
- **Classes:** `UpperCamelCase`. **Properties:** `lowerCamelCase`. Individuals: `lowerCamelCase` or a
  stable id. Be consistent; no spaces.
- Every class and property gets an **`rdfs:label`** (human-readable) and an **`rdfs:comment`** (a
  one-sentence definition). This is what `pyLODE` turns into readable docs.

## Structure
- Set `rdfs:domain` / `rdfs:range` on properties (bounded by the OWL profile).
- Add an ontology header: `owl:Ontology` with `owl:versionInfo`, `dcterms:created`, `rdfs:comment`.
- Stay within the chosen **OWL profile** (`owl-profile-tradeoff.md`).
- Declare only the chosen **provenance level's** properties (`provenance-policy.md`).

## Hygiene
- Parse-clean (must load in rdflib without error) before any gate.
- No domain terms hardcoded anywhere except this output file, which is *meant* to be domain-specific
  (it lives in `output/`, not the framework core).
