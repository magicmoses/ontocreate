# Ontology-Creator Framework

  A reusable Claude Code project structure that turns a description of any
  scientific domain into a validated ontology draft, with you in the loop at
  a few checkpoints. The build is autonomous and credential-free; you only
  steer at the gates.

  The flow: CQs/scope → direction (reuse, profile, provenance) → draft
  structure → validation + evaluation.

  The framework is the product. Applying it to a specific domain is a
  separate step.

  ## Use it

  1. Get it. Click "Use this template" on GitHub, or run `python
  new_project.py my-onto` to copy the framework into `./my-onto`.
  2. Add input. Put your material in `my-onto/input/`, or point
  `/ingest-input <path>` at any folder.
  3. Start. Open the project in Claude Code and run `/start`.

  `/start` gives a short intro, then works through the flow and stops at
  four checkpoints for your decision. Most people only run `/start` and
  answer at the gates; the other commands are optional. The first
  checkpoint, the competency questions, is iterative: refine until the scope
  is right, then it freezes.

  The four checkpoints: CQs and scope, then direction (reuse, profile,
  provenance), then the draft structure, then validation and evaluation.

  The framework versions the project for you (git, one commit per gate), and
  the scaffold copies only the framework itself, never domain content or
  session state.

  ## What to put in input/

  Every input is conceptual signal for design, not data to load. Use
  whatever you have. You can even point it at a codebase; the framework then
  models the platform that code implements and its domain, not the code
  structure itself.

  | Input | Example |
  |---|---|
  | Project or DB description (good first input) | a short text: the
  project, the goal, the main entities, what the DB holds |
  | Prompt (minimum) | a sentence or two: the domain and what the ontology
  should answer |
  | DB schema | your CREATE TABLE statements, an ERD export, or the ORM
  models file |
  | Compact data profile (optional) | per categorical column: distinct
  values, a few sample rows, basic stats |
  | Document corpus | the key papers or docs as PDF, Word, etc. |
  | Existing ontology or vocabulary | a .ttl, .owl, or .rdf to reuse |
  | Glossary or taxonomy | a term list |
  | Expert notes | interview notes, requirement docs |

  Do not provide a live DB connection (a connection string is a credential
  and breaks the credential-free build) or a full data dump (wrong
  granularity; loading instances is a later step). Export the schema, plus
  an optional profile, as files instead.

  If you only have a prompt, run `/interview` and the framework asks
  structured questions to build the rest.

  ## What you get

  - `output/ontology.ttl`, the validated ontology: portable RDF that runs in
  rdflib or Oxigraph and serves over Apache Jena Fuseki
  - `output/docs/`, readable HTML documentation
  - `output/evaluation_report.md`, the quality scorecard
  - `output/project-memory.json` and `output/events.jsonl`, every decision
  and gate, git-versioned

  Want Neo4j? Run `/migrate-neo4j` after the build. It imports the same
  `.ttl` via neosemantics, a one-way read-only import that never touches
  your `.ttl`, and needs Neo4j credentials in `.env`.

  Found gaps while using it? Drop a gap report in `input/` and run
  `/refine`. Emergent terms become candidate competency questions, you
  decide at the gate, and the framework produces the next version.

  ## Honest caveats

  - You get a draft you steer, not a finished answer. You decide at the
  checkpoints.
  - The framework can check that the ontology is consistent, not that it is
  true. Your judgment at the checkpoints catches that.
  - Re-running may differ slightly. Every decision is logged, so each run
  stays reproducible.

  Full details in `LIMITATIONS.md`. Your defaults (profile, scope posture,
  storage, message length) live in `preferences.md`.

  ## Background and sources

  Methodology and evaluation:

  - Noy, N. F., & McGuinness, D. L. (2001). Ontology Development 101: A
  Guide to Creating Your First Ontology. Stanford Knowledge Systems
  Laboratory Technical Report KSL-01-05 (also Stanford Medical Informatics
  SMI-2001-0880). The six development steps.
  - Grüninger, M., & Fox, M. S. (1995). Methodology for the Design and
  Evaluation of Ontologies. Workshop on Basic Ontological Issues in
  Knowledge Sharing, IJCAI-95, Montreal. Competency questions.
  - Suárez-Figueroa, M. C., Gómez-Pérez, A., Motta, E., & Gangemi, A.
  (Eds.). (2012). Ontology Engineering in a Networked World. Springer. ISBN
  978-3-642-24793-4. The NeOn methodology and its scenarios.
  - Gómez-Pérez, A., Fernández-López, M., & Corcho, O. (2004). Ontological
  Engineering. Springer. Ontology evaluation dimensions.
  - Guarino, N., & Welty, C. (2002). Evaluating Ontological Decisions with
  OntoClean. Communications of the ACM, 45(2), 61-65. Rigidity, identity,
  unity.
  - Poveda-Villalón, M., Gómez-Pérez, A., & Suárez-Figueroa, M. C. (2014).
  OOPS! (OntOlogy Pitfall Scanner!): An On-line Tool for Ontology
  Evaluation. International Journal on Semantic Web and Information Systems,
  10(2), 7-34. The pitfall scan.
  - Gangemi, A., & Presutti, V. (2009). Ontology Design Patterns. In S.
  Staab & R. Studer (Eds.), Handbook on Ontologies (2nd ed., pp. 221-243).
  Springer. See also ontologydesignpatterns.org.

  Standards:

  - W3C (2012). OWL 2 Web Ontology Language Profiles (Second Edition). W3C
  Recommendation, 11 December 2012. Profiles EL, QL, RL.
  - W3C (2017). Shapes Constraint Language (SHACL). W3C Recommendation, 20 July 2017.
  - W3C (2013). PROV-O: The PROV Ontology. W3C Recommendation, 30 April 2013.
  - W3C (2014). RDF 1.1 Concepts and Abstract Syntax. W3C Recommendation, 25
  February 2014. With RDF-star (W3C Community Group Final Report, December 2021) for statement-level provenance.

  Implementation builds on rdflib, owlready2, pySHACL, owlrl, and pyLODE,
  with the ELK, HermiT, and Ontop reasoners. See `requirements.txt`.
