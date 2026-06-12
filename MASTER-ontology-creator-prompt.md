# MASTER PROMPT — Reusable, Domain-Agnostic Ontology-Creator Framework for Claude Code

## 1. What you are building

A **reusable Claude Code project structure** that turns a defined input about *any* scientific domain
into a **validated ontology draft**, with a **human in the loop at clear decision points** and a
**short, guided UX** (the human steers; the framework does the work).

The framework IS the product. It will later be applied to specific domains; the first application
lives in a separate planning document and **must not leak into here**.

**HARD CONSTRAINT — domain-agnostic.** No agent, command, skill, or rule may hardcode knowledge from
any specific domain. All domain specifics enter only through `input/`. If you catch yourself writing
a domain concept into the framework, that is a bug — move it into the input layer.

**The build runs autonomously between the gates and is credential-free, end to end.** The entire loop
runs on an **in-memory RDF store (rdflib)** and serializes to **Turtle (`.ttl`)**. It never connects
to a database, never authenticates against anything, never blocks on a missing credential. The only
stops are the four human gates (H1–H4).

**Two final deliverables (see §11):** (1) a credential-free **OSS artifact** — the validated ontology
as `.ttl` plus HTML docs, the evaluation scorecard, and the project memory; and (2) an **optional
Neo4j migration kit** the user runs *after* the build and *outside* the autonomous loop, only if they
want a property-graph deployment. The `.ttl` is and stays the canonical artifact.

**It is iterative and versioned.** An ontology has versions. When downstream population/use reveals
gaps, a gated **refinement cycle** produces the next version (§20). One-shot is the exception, not the
rule.

**Provided files (do not regenerate — wire/consume them):** `README.md`, `LIMITATIONS.md`,
`preferences.md`, `.gitignore`, `neon-scenarios.md`, `provenance-levels.md`. Generate the `.claude/`
internals yourself.

**UX posture (read §2 + obey `communication.md`).** Every user-facing message is **short and plain**;
technical depth lives in files (LIMITATIONS, ORSD, report), not in the chat. Surface limitations
honestly up front. These caveats are inherent properties of an LLM-driven builder — not bugs to patch
with extra machinery.

**Context & posture.** First knowledge-graph project, built for a thesis-cooperation application. A
pragmatic, studentisch feel is acceptable and intended. Favor a working, honest, well-scoped framework
over a heavyweight one. Where the framework supports paths the first runs don't exercise, implement the
exercised paths fully and **stub the rest as "designed, not yet exercised"** — honest beats theatrical.

**Build order this session.** Claude Code orchestration layer FIRST — agents → commands → skills →
rules (incl. `communication.md`) → wire the provided reference/onboarding files → the memory layer →
the `input-conversion` skill + input-adapter interface → `/start` onboarding flow.
**Verify each layer before starting the next** (see §18). Then prove the whole thing with a **thin
dry-run** on a throwaway prompt input that exercises the full loop, every human gate, the memory
writes, `/start`, and `/visualize` end-to-end. **No real domain modeling this session.**

---

## 2. Honest limitations — surface a SHORT version up front

The **full** five points live in `LIMITATIONS.md`. At run start the orchestrator shows only this short,
plain-language version (no jargon, no wall of text):

> **Before we start — a few honest caveats:**
> - I produce a **draft you steer**, not a finished answer — you decide at the checkpoints.
> - I can check the ontology is **consistent**, not that it's **true** — your judgment at the
>   checkpoints catches that.
> - Re-running may differ slightly; every decision is logged, so each run stays reproducible.
> *(Full details in `LIMITATIONS.md`.)*

The full points (stored, not dumped on the user): (1) the evaluation is internal-only and partly
circular — CQ coverage cannot tell you the questions were right; (2) the gates are best-effort, not an
expert sign-off; (3) validation proves formal correctness, not semantic truth, and the same model
reviews itself; (4) the output is *a* draft, non-deterministic — the project memory makes a run
reproducible; (5) only exercised NeOn paths are proven — the framework stops rather than walk an
untested path. These are inherent; honesty is the mitigation, not more internal metrics.

---

## 3. Guiding principles (the law every agent obeys)

1. **An ontology is only as strong as the questions it must answer.** Competency Questions (CQs)
   come before any class is drawn.
2. **The derivation chain is the backbone:**
   **Motivating Scenario** (narrative) → **Competency Questions** (specific, testable) →
   **Ontology** (the classes/properties that make the CQs answerable) →
   **Evaluation** (each CQ becomes a SPARQL query; % answerable = the headline quality metric).
   Scenarios justify the ontology; CQs are extracted from them; the CQs ARE the evaluation.
3. **Reuse before build** — for ontologies (researcher-agent), code/libraries (library-scout-agent),
   AND tooling: reuse a ready-made MCP server before wrapping your own (§9).
4. **Limit the scope — never model more than you need.** The single most important rule. Every class
   and property must trace back to a CQ. If it serves no question, it is out — including during
   refinement (§20).

Process the framework automates (Ontology Development 101):
1. determine domain + scope → 2. reuse → 3. enumerate important terms → 4. define classes + hierarchy
→ 5. define properties → **6. limit the scope (the cardinal step, enforced continuously, not once).**

---

## 4. NeOn scenarios — set the direction

Reference file in repo: **`neon-scenarios.md`** (paraphrased summary; source cited). After input
ingestion, the scoping-agent **classifies** the project into one or more NeOn scenarios — always
including Scenario 1 (the core build path). This determines the workflow: build-from-scratch vs.
reuse-heavy vs. re-engineer-a-resource. Implement the classified paths; stub the rest (Limitation 5).

---

## 5. Input layer (pluggable — what to provide, and what NOT to)

**Every input gives conceptual signal for *design* — not data to *load*.** (Loading instances into the
finished graph is Stage-2, the application; see §20.)

Put everything in `input/`, or give a folder path. The input-agent **auto-detects** types and
normalises each via an adapter — documents are converted by the **`input-conversion` skill**;
structured sources have their own adapters. **More context is better — start broad.**

Accepted inputs:
- **Project / database description (free text)** — a short overview: what the project/domain is, the
  goal, the main entities, what the database holds. *Recommended first input — more info doesn't hurt.*
- **Prompt** — the minimum: domain + goal (if nothing else exists, `/interview` builds the rest).
- **DB schema** — `CREATE TABLE` / DDL, an ERD export, or the ORM models file → tables→classes,
  columns→properties, FKs→relations (NeOn Scenario 2). **This — not the data — is the conceptual signal.**
- **Compact data profile (optional)** — per categorical column the distinct values (→ enumerations /
  controlled vocab), a few sample rows, basic column stats. The useful *compressed* form of DB content.
- **Document corpus** — the key papers/docs (PDF, Word, etc.) to model against; converted to text for
  term/relation extraction.
- **Existing ontologies / vocabularies** — `.ttl` / `.owl` / `.rdf` to reuse.
- **Glossaries / controlled vocabularies / taxonomies** — a term list.
- **Domain-expert notes** — interviews, requirement docs.
- **Refinement candidates / gap report** — emergent terms/relations a downstream population or use
  surfaced; triggers a refinement cycle (§20).
- **Interactive elicitation** via `/interview` — the framework asks structured questions when only a
  prompt exists.

**Explicitly NOT wanted:** a **live DB connection** (a connection string = credentials → breaks the
credential-free build) or a **full data dump / complete dataset** (wrong granularity for design;
instance-loading is Stage-2). Provide a schema export + an optional profile *as files* instead.

Minimum to run: just a prompt. Everything else is optional enrichment. The adapter interface makes new
input types easy to add. Inputs live in `input/`.

---

## 6. Agents (`.claude/agents/`, all domain-agnostic)

- **orchestrator-agent** — the workflow playbook: the 6-step loop, the gates, the human-in-the-loop
  checkpoints H1–H4, and the structure-creation self-checks (§18). Routes work; subagents never call
  each other (routing is top-level only). **Runs first-run onboarding (`/start`)**: a short greeting —
  what the framework does (one line), the flow in ~4 steps, where to put input (everything in `input/`
  or give a path), and the short caveats (§2) — then it waits. **Owns session context** (working +
  summary memory), **writes the persistent episodic run log**, and reads `preferences.md` to set gate
  defaults (§12). Obeys `communication.md` (short, plain, depth→files).
- **input-agent** — **mainly a reader of the user-specified input directory** (`input/` or a given
  path). Auto-detects file types and normalises each: documents via the **`input-conversion` skill**
  (markitdown → text/Markdown; pypdf / python-docx / pandas fallback), structured sources via their
  adapters (DB schema, data profile, CSV/JSON, existing ontology). Owns `/ingest-input` and
  `/interview`. It does not model — it hands a clean, typed input pack to the scenario-and-cq and
  scoping agents.
- **scenario-and-cq-agent** — owns the top of the derivation chain. Turns input into motivating
  scenarios, derives CQs, clusters/refines, formalises each CQ as a SPARQL template, and produces the
  **ORSD** (Ontology Requirements Specification Document: purpose, scope, language, intended users/uses,
  CQs, starter glossary). Writes the ORSD + CQ-set to entity memory (§12).
- **scoping-agent** — owns Step 1 and continuously enforces Step 6. Sets project direction from the
  input: (a) NeOn scenario classification, (b) OWL profile recommendation, (c) provenance level
  recommendation. Flags any element that doesn't trace to a CQ as out-of-scope. Guardian against bloat.
- **researcher-agent** — "reuse before build" for ONTOLOGIES. Investigates which vocabularies/
  ontologies underlie the input or fit the domain via a **generic, pluggable registry search**
  (registries chosen from the input, never hardcoded). Recommends reuse / extend / merge / build-new.
- **library-scout-agent** — "reuse before build" for CODE and TOOLING. Searches GitHub/PyPI for the
  best-fitting libraries/repos, and **checks the MCP ecosystem first** — the **awesome-mcp-servers
  catalog** + the **MCP registry** — for a ready-made server before proposing to wrap one of our own
  (§9). Proposes a curated shortlist with rationale. Starts from the fixed baseline toolset (§8).
- **modeling-agent** — owns Steps 3–5: terms → classes + hierarchy → properties, bounded by the frozen
  CQ set and the reuse + OWL-profile + provenance decisions. Declares the provenance properties for the
  chosen level. Produces `output/ontology.ttl`.
- **validation-agent** — owns **correctness**: OWL reasoner consistency + SHACL + pitfall scan.
  Checker ≠ builder; reports, never edits.
- **evaluation-agent** — owns **fitness for purpose**: the multi-dimensional scorecard (§10). Distinct
  from validation: validation asks "is it correct?", evaluation asks "is it good?".

(Optional: **docs-agent** for the evaluation report + thesis framing.)

---

## 7. Direction-setting decisions (scoping-agent; input-driven; confirmed at gate H2)

**Storage backend is deliberately NOT a decision here.** The build is backend-free (in-memory RDF →
Turtle). Where the ontology is ultimately served — an rdflib/Oxigraph file, Apache Jena Fuseki, or
Neo4j — is an **output-packaging** concern handled *after* the build (§11), never a build-time,
credentialed dependency. This keeps the autonomous loop credential-free.

**NeOn scenario(s)** — from the candidate resources found (see `neon-scenarios.md`).

**OWL profile** — choose deliberately from what the CQs need, before modeling:
- **EL** — fast, scalable reasoning; limited expressivity (good default for large/simple ontologies). Reasoner: **ELK**.
- **QL** — optimised for query answering over large data via query rewriting. Reasoner: **Ontop** (OWL 2 QL / OBDA; Java engine, pulled only if QL is chosen).
- **RL** — rule-based reasoning (materialisation). Reasoner: **owlrl** (Python OWL 2 RL on rdflib, in-process; **RDFox** as the high-performance alternative).
- **DL** — most expressive, but reasoning can blow up (exponential). Reasoner: **HermiT** (ships with owlready2).
Rule `owl-profile-tradeoff.md` documents the tradeoff. Decide upfront, not when the reasoner hangs.
(`preferences.md` may set a default profile; the human still confirms at H2.)

**Provenance level** — reference `provenance-levels.md`. Three levels, libraries fixed:
- **L1 Source-level** — `rdflib` + Dublin Core (`dcterms:source`).
- **L2 Statement-level + evidence + confidence** — `rdflib` with **RDF-star** during the build (the
  common default for LLM-extracted / scientific work); becomes Neo4j **edge properties** only *after*
  the optional migration (§11).
- **L3 Full PROV-O activity chain** — the `prov` Python library and/or PROV-O via `rdflib`.
Selection is input-driven and confirmed by the human; only the chosen level's properties are declared.

**Reuse decision** — ontologies (researcher) + libraries + ready-made MCP servers (library-scout).

---

## 8. Fixed baseline toolset (domain-agnostic — installed by default)

- **rdflib** — RDF/OWL graphs + SPARQL in Python; **and the default in-memory store for the whole
  build** (zero credentials)
- **owlready2** — OWL manipulation + reasoner integration (ships HermiT)
- **ELK** — OWL EL reasoner (EL profile)
- **owlrl** — Python OWL 2 RL rule materialisation on rdflib, in-process (RL profile)
- **Ontop** — OWL 2 QL / OBDA query-rewriting reasoner (QL profile; Java engine, pulled only if QL chosen)
- **pySHACL** — SHACL constraint validation
- **OOPS!** — Ontology Pitfall Scanner (web API) or local equivalent
- **generic ontology registry search** — pluggable, **key-free** backends by default (LOV general;
  EBI OLS biomedical), selected from the input, never hardcoded. Any registry or import that needs a
  credential (e.g. BioPortal's API key) is **not used in the credential-free build** — if needed at
  all, only in Stage-2 (the application)
- **pyLODE** — human-readable HTML docs from an OWL file; **WebVOWL** for interactive
  class/relation visualization (powers `/visualize`)
- **markitdown** — lightweight converter for the input layer (PDF, Word, PowerPoint, Excel, HTML →
  text/Markdown for analysis); **pypdf / python-docx / pandas** as the proven fallbacks. Heavy,
  layout-aware converters (e.g. docling) are a *per-project* library-scout pick, not baseline.
- **Oxigraph** *(optional)* — embeddable, open-source RDF store with Python bindings; the
  credential-free **persistent** option when an in-memory store is not enough
- **prov** — W3C PROV (only when provenance level L3 is selected)
- **FastMCP** — wrap framework tools as MCP servers (§9), only when no ready-made server exists
- **spaCy** *(optional)* — term/phrase extraction to support Step 3
- **Ontology Design Pattern portal** (ontologydesignpatterns.org) — ODPs for NeOn Scenario 7

These are mostly pip libraries, not "starrable" repos — expected; an ontology framework runs on
infrastructure libs. Reasoner and provenance libs are pulled per chosen profile/level — only the
selected profile's reasoner (ELK / Ontop / owlrl / HermiT) is installed.

**Out of the baseline by design:** `neosemantics`/n10s and any Neo4j driver belong to the **optional
migration kit** (§11), because the build never touches a database. Memory **frameworks** (graphiti /
mem0 / Letta) are out too — Stage-2 application tools, not the creator (§12).

---

## 9. Repo integration — domain-agnostic baseline + domain-specific extension + MCP discovery

**Domain-agnostic baseline** (§8) is fixed and always installed.

**Domain-specific repo integration (owned by library-scout-agent):**
1. **Discover** — search GitHub/PyPI for repos/libraries that fit the current input + domain, with
   rationale.
2. **Declare** — approved picks → `input/dependencies.md` (package, version, purpose, why). Nothing
   enters the framework core.
3. **Approve** — the human confirms at gate **H2**.
4. **Install** — into the project environment (`requirements.txt` / `pyproject.toml`), isolated from
   the baseline.
5. **Integrate** — via an **input adapter** (new input type) or by **MCP-wrapping** a reusable tool.

The adapter interface (§5) and the MCP pattern (below) are the two integration seams.

**MCP — discover before you wrap (reuse before build, applied to tooling).** Before MCP-wrapping any
tool, library-scout checks the **awesome-mcp-servers catalog** and the **MCP registry** for an
existing server (Neo4j, databases, document processing, etc.). **Reuse a ready-made server when one
fits; only wrap our own when none exists.** Folds into `/scout-libs`.

**Wrap-your-own fallback (only when no ready-made server covers the capability).** Wrap stable baseline
tools as **MCP servers** (via **FastMCP**). Candidates: `registry_search` · `owl_reasoner` ·
`pitfall_scan` · `ontology_visualize` · `cq_sparql_run` · `structural_metrics` · `cost_report`. Pattern:
```python
from fastmcp import FastMCP
from owlready2 import get_ontology, sync_reasoner
mcp = FastMCP("owl-reasoner")

@mcp.tool()
def check_consistency(ttl_path: str) -> dict:
    onto = get_ontology(ttl_path).load()
    with onto: sync_reasoner()
    bad = list(onto.inconsistent_classes())
    return {"consistent": len(bad) == 0, "unsatisfiable": [c.name for c in bad]}

if __name__ == "__main__": mcp.run()
```
**KISS ordering:** plain Python function first; MCP-wrap only once stable, needed cross-project, and
only if no ready-made server already does the job. Do not wrap everything on day 1.

---

## 10. Validation (correctness) vs. Evaluation (fitness)

**validation-agent — is it correct?**
- OWL reasoner — logical consistency, no unsatisfiable classes
- pySHACL — structural constraints
- pitfall scan (OOPS!) — common modeling mistakes

**evaluation-agent — is it good? (multi-dimensional scorecard, grounded in Gómez-Pérez):**
- **CQ coverage** — % of CQs answerable via SPARQL (the headline metric)
- **structural metrics** — depth, breadth, class/property ratio, richness
- **quality dimensions** — accuracy, completeness, conciseness, consistency, clarity *(qualitative,
  model-judged/heuristic — not ground-truth; per §2 the framework can flag these but not verify
  external correctness)*
- **OntoClean check (included)** — meta-properties (rigidity, identity, unity) to catch taxonomic
  errors. The one **non-circular** quality signal (independent of the CQs), so part of the standard
  scorecard, not optional.
- **downstream-task hook** — a plug-in slot where a domain-specific task evaluation attaches at the
  APPLICATION layer — kept out of the framework core

**Do not add further internal metrics.** External correctness is a documented limitation (§2), not a
feature gap; more internal numbers would be false reassurance, not more rigor.

Output: `output/evaluation_report.md`.

---

## 11. Output packaging — OSS artifact + optional Neo4j migration kit + handoff

**A) OSS artifact (always produced, credential-free):**
- `output/ontology.ttl` — the validated ontology; the **canonical, portable RDF** artifact
- `output/docs/` — pyLODE HTML documentation
- `output/evaluation_report.md` — the scorecard (§10)
- `output/project-memory.json` + `output/events.jsonl` — the decision + run history (§12)
- Runs as-is in **rdflib** (in-memory) or **Oxigraph** (embeddable), serves over **Apache Jena Fuseki**
  (local OSS) — all credential-free.

**B) Optional Neo4j migration kit (`/migrate-neo4j`, AFTER the build, OUTSIDE the autonomous loop):**
- the same canonical `.ttl` — **never modified**; migration is a **one-way, read-only import**
- a **neosemantics (n10s)** import script + config
- a short **mapping note**: RDF resources → nodes, `rdf:type` → labels, literal properties → node
  properties, object properties → relationships. The OWL **reasoning** layer becomes inert structure
  (Neo4j is not a reasoner).
- **Rationale:** reason once on the RDF/OWL at build time, then serve the *checked* graph in a property
  graph for fast traversal. The `.ttl` stays the source of truth; the Neo4j copy is a rebuildable,
  traversal-optimized projection. **Zero risk to the output format.**

**C) Handoff (short closing message — obey `communication.md`):**
> Done. Your ontology: `output/ontology.ttl` · docs: `output/docs/` · scorecard:
> `output/evaluation_report.md`. It runs as-is in rdflib/Oxigraph. Want a Neo4j version? Run
> `/migrate-neo4j` (needs Neo4j credentials). Found gaps while using it? Drop a gap report in `input/`
> and I'll run a refinement cycle (§20).

**Security note — applies ONLY if you run the migration, never to the build.** The build is
credential-free (the strongest measure — zero attack surface). For `/migrate-neo4j`, keep it
proportionate (no enterprise-vault theater): credentials live in `.env` (git-ignored); agents
reference env vars (e.g. `NEO4J_PASSWORD`), **never** the literal value, and never write secrets into
TTL, the decision log, the event log, or a visualization; redact secrets from the memory/cost logs;
use a **least-privilege** DB user / project-scoped key. Rule: `secrets-policy.md`.

---

## 12. Memory architecture — three tiers + interaction/preference memory

**Principle:** do not bolt a memory *framework* into the creator — most "memory types" are already
framework artifacts. Name them, and add the one missing piece: **persistent project memory**. Memory
frameworks (graphiti / mem0 / Letta) belong to the Stage-2 application, never here.

**Tier 1 — static knowledge (procedural + semantic).** *Procedural* = the agents' skills + rules.
*Semantic* = the reference files (`neon-scenarios.md`, `provenance-levels.md`) + reused ontologies.
Domain-agnostic core; domain knowledge enters via `input/`. Already exists.

**Tier 2 — ephemeral session (working + conversational + summary).** *Working* = active context +
in-progress `output/` files. *Conversational* = the live human-in-the-loop dialogue at H1–H4.
*Summary* = rolling compression when a run gets long. Orchestrator-managed; **no persistence** beyond
the session. Decisions from the gate dialogue are **promoted to Tier 3**.

**Tier 3 — persistent project memory (entity + episodic) = the versioning / build-audit layer.**
- **Entity** = the structured decisions: ORSD, frozen CQ-set, NeOn classification, OWL profile,
  provenance level, reuse + scope decisions, **ontology version**. → `output/project-memory.json`.
- **Episodic** = the timestamped build record: each gate outcome (approved / sent back / changed),
  validation + eval results, attempt counts, escalations, **refinement cycles**. →
  `output/events.jsonl` (append-only).
- **Git-versioned, append-only, one commit per gate.** The build's **process-provenance** — symmetric
  to the data-provenance levels (§7); also what makes a non-deterministic run reproducible
  (Limitation 4) and tracks the ontology across versions (§20).
- **Schema is domain-agnostic; content is domain-specific.**

**Interaction / preference memory (a thin combination).** User interaction is *conversational* (Tier 2,
live) + *episodic* (Tier 3, outcomes) + a small, **user-scoped, persistent** `preferences.md` —
default OWL profile, scope posture, OSS-vs-cloud, explanation length, reuse aggressiveness. It **sets
defaults** at the gates, **never overrides** the human's decision, and may **never** encode "suppress
honest feedback." A *file*, not a learning engine. User-scoped (persists across projects), unlike the
project-scoped Tier-3 memory.

**Per-agent memory map:** orchestrator → manages working+summary, writes episodic, reads preferences ·
scenario-and-cq → writes entity (ORSD, CQ-set) · scoping → reads entity (CQ-set) + preferences, writes
entity (decisions); scope-discipline = querying entity memory · researcher → writes entity (reuse) +
extends semantic · library-scout → writes entity (`dependencies.md`) · modeling → reads entity +
semantic, writes the ontology · validation → writes episodic · evaluation → writes episodic.

**Context-management policy (the harness knob).** The orchestrator gives each subagent the frozen
CQ-set + the relevant decisions, **not** the whole history, and summarises prior phases when a run
grows. Summary memory is lossy (risk: drift), which is exactly why the **authoritative decisions live
in Tier-3 entity memory**, not only in the rolling context. Rule: `memory-policy.md`.

**On the agent harness.** Claude Code IS the harness (the loop, tool plumbing, context management, stop
conditions, observability). You **configure** it; you do not build one. Knobs: context management (this
section), stop conditions (3-attempt bound §19), guardrails (gates §16 + the domain-agnostic scan §18),
observability (`/cost` §14 + the episodic log).

---

## 13. Visualization aid (the human's decision surface)

`/visualize` renders, primarily at gate H3:
- an **ontology diagram** (classes, hierarchy, key relationships) from the current TTL (pyLODE/WebVOWL
  or a TTL→mermaid/graphviz renderer)
- a **pipeline/architecture diagram** (input → scenarios → CQs → reuse → model → validate → evaluate)
The human should never read raw Turtle to decide. (Caveat — Limitation 2: a clean diagram can still
hide a semantic error; the render aids judgment, it does not guarantee it.)

---

## 14. Cost tracker

`/cost` — a lightweight logger of tokens, $ estimate, and reasoner time per run. Provenance level, OWL
profile, and corpus size drive cost; surface it so scope decisions are made with cost in view. (A
logger, not a hard cap — it informs the human, who decides at the gates.)

---

## 15. Commands (`.claude/commands/`)

`/start` (guided front door) · `/ingest-input` · `/interview` · `/scenarios` · `/elicit-cqs` ·
`/classify-scenario` · `/find-reuse` · `/scout-libs` · `/set-owl-profile` · `/set-provenance` ·
`/draft-ontology` · `/check-scope` · `/validate` · `/eval` · `/visualize` · `/cost` ·
`/memory` (view project memory) · `/self-audit` (§18) · `/refine` (start a refinement cycle from a gap
report, §20) · `/migrate-neo4j` (optional; after the build, outside the autonomous loop)

**Most users only run `/start` and then respond at the gates.** The granular commands are optional
manual controls.

---

## 16. Human-in-the-loop gates (explicit STOP points — the human decides before proceeding)

**Gate format (every gate, obey `communication.md`):** the same short shape —
**[what I produced] · [what you decide] · [how to reply]**. Example H1: *"18 CQs in 4 themes [render].
They fix the scope. Reply `ok` to freeze, or tell me what to add / cut / refine."* No walls of text;
depth (ORSD, report) lives in files.

- **H1 — after `/scenarios` + `/elicit-cqs`:** review scenarios + CQ set + ORSD. **Iterative, not a
  one-shot approval** — send the CQs back for another round (refine / add / cut) as often as needed;
  **scope only freezes once you accept.** Nothing is modeled until H1 is accepted.
- **H2 — direction:** confirm NeOn scenario(s), reuse decision (ontologies + libraries incl.
  domain-specific dependencies, and which **ready-made MCP servers** to reuse vs. wrap), OWL profile,
  provenance level. **No storage/credential decision here — the build is backend-free (§11).**
- **H3 — after `/draft-ontology` + `/visualize`:** review the rendered ontology structure.
- **H4 — after `/validate` + `/eval`:** review correctness + the evaluation scorecard; iterate vs. accept.
At each gate the orchestrator presents the short summary + (where useful) a `/visualize` render,
**commits the project memory (§12)**, then STOPS and waits. No silent progression.

---

## 17. `.claude/` structure + project files

```
.claude/
  agents/    orchestrator, scenario-and-cq, scoping, researcher, library-scout,
             modeling, validation, evaluation  (+ optional docs)
  commands/  the commands in §15
  skills/    scenarios-and-cqs/, ontology-reuse/, library-scouting/, ontology-modeling/,
             owl-validation/, ontology-evaluation/, scope-discipline/, ontology-visualization/,
             mcp-tooling/, input-conversion/   (each a SKILL.md)
  rules/     methodology.md, derivation-chain.md, domain-agnostic.md, human-gates.md,
             owl-profile-tradeoff.md, provenance-policy.md, ttl-conventions.md,
             memory-policy.md, secrets-policy.md, communication.md, self-verification.md
README.md                provided — setup + input guide (human entry point)
LIMITATIONS.md           provided — full caveats; orchestrator surfaces the short version (§2)
preferences.md           provided — user-scoped defaults (§12); editable; never overrides the human
.gitignore               provided — ignores .env + caches
neon-scenarios.md        provided reference
provenance-levels.md     provided reference
input/                   per-project input pack + adapters + dependencies.md
output/                  ORSD, ontology.ttl, docs/ (pyLODE), evaluation_report.md,
                         architecture.(svg|mermaid), project-memory.json, events.jsonl, cost log
migration/               Neo4j n10s import script + config + mapping note (generated by /migrate-neo4j)
mcp/                     ready-made servers referenced first; own FastMCP servers only when none exists
```

---

## 18. Self-verification DURING structure creation (build the framework with its own discipline)

Bootstrap with the same **build → verify → correct** rigor it preaches. Apply **checker ≠ builder** and
a **3-attempt bound before escalating to the human** to the meta-build too.

**Verify each layer before starting the next:**
- after **agents**: valid frontmatter, single clear responsibility, no domain leakage
- after **commands**: every command maps to an owning agent; no orphans; `/start` exists and runs onboarding
- after **skills**: every skill is referenced by an agent or command (incl. `input-conversion`); no dead skills
- after **rules + reference files**: rules mutually consistent; `communication.md` governs user-facing
  output; the provided files (`neon-scenarios.md`, `provenance-levels.md`, `memory-policy.md`,
  `secrets-policy.md`, `preferences.md`) are referenced by the agents/steps that consume them
- after **the memory layer**: entity (`project-memory.json`) + episodic (`events.jsonl`) writers exist;
  one-commit-per-gate is wired; `preferences.md` is read for gate defaults; agents write to the tiers
  the §12 map assigns

**`/self-audit` — a consistency pass over the whole structure (before the dry-run):**
- `LIMITATIONS.md` exists; the orchestrator surfaces the **short** version (§2) at run start
- `/start` onboarding is wired; `communication.md` brevity holds across user-facing messages
- every Gate (H1–H4) names the agents/commands it depends on, and they exist; the gate format is applied
- every link in the derivation chain (scenario→CQ→ontology→evaluation) has an owning agent
- every one of the 6 process steps maps to an owner; no orphan steps
- no two agents claim the same responsibility; no responsibility is unowned
- **domain-agnostic invariant**: scan all framework files for hardcoded domain terms; flag any leak
  (domain knowledge — and domain-specific memory *content* — belongs only in `input/` and `output/`;
  the memory *schema* stays agnostic)
- **the build path is backend-free**: the loop uses the in-memory store only; no DB/credential
  dependency anywhere in the loop; `secrets-policy.md` is referenced **only** by `/migrate-neo4j`
- the baseline (§8), the integration seam (§9), the OSS packaging (§11), and the **refinement
  cycle + versioning** (§20) are all wired

**Final integration self-test — the dry-run:** run on a throwaway prompt input forcing the full path:
`/start` → `/ingest-input` → `/interview` → `/scenarios` → `/elicit-cqs` (H1, iterate at least once) →
`/classify-scenario` + `/find-reuse` + `/scout-libs` + `/set-owl-profile` + `/set-provenance` (H2) →
`/draft-ontology` + `/visualize` (H3) → `/validate` + `/eval` (H4) → `/cost`. The run must stop at each
gate, **commit the project memory at each gate**, and produce all OSS-artifact outputs. If any step or
gate fails, fix the structure before declaring it done.

Rule `self-verification.md` records these checks so they are repeatable on every future change.

---

## 19. The runtime loop + gates (operational discipline, once the framework is used)

Run as **build → verify → correct**, **checker ≠ builder**, bounded to **3 correction attempts**
before escalating:
- **CQ gate** — a frozen CQ set covering the scope (H1, iterative until accepted)
- **Reuse gate** — ontology + library + ready-made-MCP decisions recorded before modeling
- **Scope gate** — `/check-scope`: every element traces to a CQ; orphans removed
- **Validation gate** — reasoner consistent, no critical pitfalls
- **Evaluation gate** — `/eval`: CQ coverage + scorecard (incl. OntoClean) meet the agreed bar
Every gate commits the project memory (§12). An untested NeOn path is never entered silently — the
loop stops and escalates (Limitation 5).

---

## 20. Iteration & versioning — the refinement loop

An ontology built from a schema + samples is **v1**. When the full data is loaded/used (Stage-2, the
application), it reveals concepts/relations/themes the thin sample didn't show (the instances expose
gaps in the model). This is normal, iterative ontology development — handled in a controlled, gated
way, **never as silent mutation**.

- Stage-2 collects **refinement candidates** — unmapped terms, frequent co-occurrences, clusters with
  no class, implied relations — into a **gap report**.
- The gap report re-enters as an `input/` type (§5) and `/refine` triggers a **refinement cycle**: does
  a candidate warrant a new CQ? If yes → new CQ → **H1 (the human decides on scope expansion)** →
  model → validate → eval → the **next version**. If it earns no CQ, it stays out (scope discipline holds).
- **Data proposes, the human disposes.** The framework surfaces and ranks gaps (by frequency / how much
  data doesn't fit) but cannot decide whether a theme *matters* — that is the human's call at the gate
  (Limitation 1).
- The **git-versioned project memory** (§12) tracks the ontology across versions; each refinement cycle
  is an auditable set of commits.
- **Stage-2 never edits the model directly** — it reports gaps that re-enter Stage-1. The
  Stage-1/Stage-2 split stays intact.

---

## 21. Principles (consolidated)

- domain-agnostic: zero domain knowledge outside `input/`; memory schema agnostic, content domain-specific
- derivation chain (scenario→CQ→ontology→evaluation) is the backbone
- reuse before build — ontologies, libraries, AND ready-made MCP servers (before wrapping your own)
- limit the scope — the cardinal rule (scoping-agent enforces continuously, incl. during refinement)
- validation (correct?) is separate from evaluation (good?); OntoClean is in the standard scorecard
  (the one non-circular signal); no extra internal metrics
- input = **conceptual signal for design**, not data to load; DB → schema + compact profile, never a
  live connection or a full dump
- provenance level, OWL profile, and NeOn scenario are input-driven, confirmed at H2
- the build is **credential-free**; output = a credential-free **OSS artifact** + an **optional Neo4j
  migration kit** (the `.ttl` stays canonical; migration is a one-way, read-only import)
- **iterative & versioned**: downstream gaps feed a gated refinement cycle → the next version
- memory = three tiers; **persistent project memory (entity + episodic) is git-versioned, one commit
  per gate** — the build's process-provenance; interaction adds a thin user-scoped `preferences.md`
  (sets defaults, never overrides, never suppresses honest feedback)
- **UX**: guided front door (`/start`); short, plain user-facing messages, depth → files
  (`communication.md`); limitations surfaced up front — honesty over mitigation-theater
- human-in-the-loop at H1–H4 — the framework drafts, the human decides; H1 is iterative; one gate format
- checker ≠ builder, 3-attempt bound — applied to BOTH the meta-build and the runtime
- Claude Code is the agent harness — configure context / stop conditions / guardrails / observability;
  don't build one
- functions first, MCP-wrap once stable and only if no ready-made server fits
- Claude Code layer before any pipeline code; verify each layer; prove it with a throwaway dry-run
