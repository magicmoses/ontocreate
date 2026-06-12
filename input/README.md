# input/ — drop your material here

Everything you give the framework goes here (or pass a folder path to `/ingest-input`). Each input gives
**conceptual signal for design — not data to load.** More context is better; start broad.

The **input-agent** auto-detects file types and normalises each via an adapter (`input/adapters/`).
Documents are converted to text by the `input-conversion` skill.

## Accepted (pick whatever you have)
| Put here | Detected as | Example |
|---|---|---|
| project / DB description *(recommended first)* | `description` | a `.md`/`.txt`: what the project is, the goal, the main entities |
| prompt *(minimum)* | `prompt` | one or two sentences: domain + what to answer |
| DB schema | `db_schema` | `CREATE TABLE` DDL, an ERD export, or ORM models (`.sql`/`.txt`) |
| compact data profile *(optional)* | `data_profile` | per categorical column: distinct values + a few sample rows (`.json`/`.csv`) |
| document corpus | `document` | key papers/docs (`.pdf`/`.docx`/`.pptx`/`.xlsx`/`.html`) |
| existing ontology / vocabulary | `ontology` | `.ttl`/`.owl`/`.rdf` to reuse |
| glossary / taxonomy | `glossary` | a term list (`.md`/`.txt`) |
| gap report (for `/refine`) | `gap_report` | emergent terms/relations a downstream use surfaced |

## Not wanted (breaks the credential-free build / wrong granularity)
- A **live DB connection** (a connection string = credentials). Export the **schema** as a file instead.
- A **full data dump / complete dataset** (instance-loading is Stage-2). Provide a **compact profile**.

Files named `README.md` and `dependencies.md` are ignored by the ingester. Adapters live in
`adapters/` (see its README to add a new input type).
