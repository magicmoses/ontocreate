# input/adapters/ — the pluggable input seam

`base.py` is the adapter interface + registry + auto-detection + a runnable ingester. It turns whatever
is in `input/` into a typed **input pack** (a list of `InputItem`s) for the scenario-and-cq and scoping
agents.

```bash
python input/adapters/base.py            # ingest ./input
python input/adapters/base.py path/to/folder
```

## Built-in adapters
`text` (prompt / description / glossary / gap report) · `ontology` (.ttl/.owl/.rdf, loaded for reuse) ·
`db_schema` (CREATE TABLE → tables/columns/FKs) · `data_profile` (categorical value sets → enumerations)
· `document` (PDF/Word/PPT/Excel/HTML via the `input-conversion` skill).

Status: `text`, `ontology`, `db_schema`, `data_profile` are exercised; `document` works when a converter
(markitdown / pypdf / python-docx / pandas) is installed, else it records `designed-not-exercised`
honestly rather than emitting empty text.

## Add a new input type (no framework-core change)
1. Subclass `InputAdapter`, implement `detect(path, name, ext)` and `normalize(path) -> InputItem`.
2. Decorate the class with `@register`.
3. If you put it in a new file, import that file at the bottom of `base.py` so it registers.

`InputItem` fields: `path`, `type`, `text` (design signal), `structure` (structured signal), `note`,
`status` (`ok` | `designed-not-exercised` | `refused`). Keep adapters domain-agnostic — they normalise
*form*, never inject domain knowledge. Refuse credentials and full dumps (see `base.py`).
