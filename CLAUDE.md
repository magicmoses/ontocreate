# Ontology-Creator Framework — operating context

This repo is a **reusable, domain-agnostic** Claude Code project that turns input about *any*
scientific domain into a **validated ontology draft**, human-in-the-loop at four gates. The framework
IS the product. See `README.md` (human guide) and `MASTER-ontology-creator-prompt.md` (full spec).

## The law (every agent obeys — full text in `.claude/rules/`)
1. **Questions before classes.** Competency Questions (CQs) come before any class is drawn.
2. **Derivation chain is the backbone:** scenario → CQ → ontology → evaluation. The CQs *are* the test.
3. **Reuse before build** — ontologies, libraries, and ready-made MCP servers (before wrapping our own).
4. **Limit the scope** — every class/property must trace to a CQ, or it is out. The cardinal rule.
5. **Domain-agnostic** — no domain knowledge in `.claude/`. Domain content lives only in `input/` and
   `output/`. If a domain concept appears in the framework core, that is a bug.
6. **The build is credential-free** — in-memory RDF (rdflib) → Turtle. No DB, no auth, no secrets in the
   loop. The only stops are the four human gates (H1–H4). Credentials appear only in `/migrate-neo4j`.

## How a run works
The **orchestrator-agent** runs everything. A user typically only runs **`/start`** and answers at the
gates. Routing is top-level only — subagents never call each other. Each gate commits project memory.

- **Front door:** `/start` (onboarding + run the flow).
- **Agents:** `.claude/agents/` — orchestrator, input, scenario-and-cq, scoping, researcher,
  library-scout, modeling, validation, evaluation, feedback (+ optional docs).
- **Rules (the law):** `.claude/rules/` — read `communication.md` before any user-facing message.
- **Guardrails:** `.claude/hooks/` — domain-leak, scope-check, secrets-redaction (fire on event).
- **Memory:** `output/project-memory.json` (entity) + `output/events.jsonl` (episodic), git-versioned,
  one commit per gate via `tools/memory.py`.

## Honesty posture
Surface the short limitations at run start (`LIMITATIONS.md`). User-facing messages are short and plain;
depth goes to files. Never suppress honest feedback. The framework drafts; the human decides.
