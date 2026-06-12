#!/usr/bin/env python3
"""Input-adapter interface (spec §5, §9) — the pluggable seam where domain input enters the agnostic
framework. Every input gives CONCEPTUAL SIGNAL FOR DESIGN, not data to load.

An adapter detects an input type and normalises it into a typed `InputItem` for the input pack. Add a
new input type by subclassing `InputAdapter`, registering it with `@register`, and (if in a new file)
importing it below — nothing in the framework core changes.

Refused by design (credential-free build): a live DB connection (a connection string = credentials) or a
full data dump / complete dataset (wrong granularity — instance-loading is Stage-2). Provide a schema
export + an optional compact profile as files instead.

Run:  python input/adapters/base.py [input_dir]   ->  prints the typed input pack as JSON.
"""
from __future__ import annotations

import json
import os
import re
import sys
from dataclasses import asdict, dataclass, field

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_INPUT_DIR = os.path.dirname(HERE)  # the input/ folder


@dataclass
class InputItem:
    path: str
    type: str                       # prompt|description|db_schema|data_profile|document|ontology|glossary|gap_report|unknown
    text: str = ""                  # normalised text/markdown signal for design
    structure: dict = field(default_factory=dict)  # structured signal (tables, value sets, counts, ...)
    note: str = ""
    status: str = "ok"              # ok | designed-not-exercised | refused


class InputAdapter:
    type = "generic"

    def detect(self, path: str, name: str, ext: str) -> bool:
        raise NotImplementedError

    def normalize(self, path: str) -> InputItem:
        raise NotImplementedError


REGISTRY: list[InputAdapter] = []


def register(cls):
    REGISTRY.append(cls())
    return cls


def _read(path, limit=200_000):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read(limit)


# --------------------------------------------------------------------------- refusal guard
FULL_DUMP_HINTS = (".dump", ".bak", ".sql.gz", ".tar", ".zip")


def refused_full_dump(path, name, ext):
    if ext in (".dump", ".bak") or name.endswith(".sql.gz"):
        return True
    # a .sql with many INSERTs is a data dump, not a schema export
    if ext == ".sql":
        try:
            txt = _read(path, 50_000)
            return txt.upper().count("INSERT INTO") > 25 and "CREATE TABLE" not in txt.upper()
        except Exception:
            return False
    return False


# --------------------------------------------------------------------------- concrete adapters
@register
class TextAdapter(InputAdapter):
    """Prompt / project-or-DB description / glossary / gap report (plain text & Markdown). EXERCISED."""
    type = "text"

    def detect(self, path, name, ext):
        return ext in (".txt", ".md", ".markdown", ".text")

    def normalize(self, path):
        text = _read(path)
        name = os.path.basename(path).lower()
        if "gap" in name:
            t = "gap_report"
        elif "glossary" in name or "taxonomy" in name or "terms" in name:
            t = "glossary"
        elif "prompt" in name or len(text) < 600:
            t = "prompt"
        else:
            t = "description"
        return InputItem(path, t, text=text.strip(),
                         note=f"{len(text)} chars; routed as '{t}'")


@register
class OntologyAdapter(InputAdapter):
    """Existing ontology / vocabulary to reuse (.ttl/.owl/.rdf). Loaded as-is. EXERCISED where rdflib present."""
    type = "ontology"

    def detect(self, path, name, ext):
        return ext in (".ttl", ".owl", ".rdf", ".n3", ".jsonld")

    def normalize(self, path):
        try:
            import rdflib
            from rdflib.namespace import RDF, RDFS, OWL
            fmt = {"ttl": "turtle", "owl": "xml", "rdf": "xml", "n3": "n3", "jsonld": "json-ld"}.get(
                os.path.splitext(path)[1].lstrip("."), None)
            g = rdflib.Graph().parse(path, format=fmt)
            ncls = len(set(g.subjects(RDF.type, OWL.Class)) | set(g.subjects(RDF.type, RDFS.Class)))
            nprop = len(set(g.subjects(RDF.type, OWL.ObjectProperty)) |
                        set(g.subjects(RDF.type, OWL.DatatypeProperty)) |
                        set(g.subjects(RDF.type, RDF.Property)))
            return InputItem(path, "ontology",
                             structure={"triples": len(g), "classes": ncls, "properties": nprop},
                             note="loaded for reuse (researcher-agent will assess fit)")
        except Exception as e:
            return InputItem(path, "ontology", note=f"rdflib not available / parse error: {e}",
                             status="designed-not-exercised")


@register
class DBSchemaAdapter(InputAdapter):
    """DDL / CREATE TABLE schema export -> tables/columns/FKs (NeOn Scenario 2). The SCHEMA is the
    conceptual signal, never the data. Light regex parse; functional."""
    type = "db_schema"

    def detect(self, path, name, ext):
        if ext == ".sql":
            return "CREATE TABLE" in _read(path, 50_000).upper()
        return ("schema" in name or "ddl" in name) and ext in (".sql", ".txt")

    def normalize(self, path):
        txt = _read(path)
        tables = {}
        for m in re.finditer(r"CREATE\s+TABLE\s+[`\"\[]?(\w+)[`\"\]]?\s*\((.*?)\)\s*;",
                             txt, re.IGNORECASE | re.DOTALL):
            tname, body = m.group(1), m.group(2)
            cols = [c.strip().split()[0].strip('`"[]')
                    for c in body.split(",")
                    if c.strip() and not c.strip().upper().startswith(("PRIMARY", "FOREIGN", "CONSTRAINT", "UNIQUE", "KEY"))]
            fks = re.findall(r"FOREIGN\s+KEY.*?REFERENCES\s+[`\"\[]?(\w+)", body, re.IGNORECASE | re.DOTALL)
            tables[tname] = {"columns": cols, "references": fks}
        return InputItem(path, "db_schema", structure={"tables": tables},
                         note=f"{len(tables)} table(s) -> classes; columns -> properties; FKs -> relations")


@register
class DataProfileAdapter(InputAdapter):
    """Compact data profile (per categorical column: distinct values; sample rows; basic stats).
    The useful *compressed* form of DB content -> enumerations / controlled vocab. JSON or small CSV."""
    type = "data_profile"

    def detect(self, path, name, ext):
        return ("profile" in name and ext in (".json", ".csv")) or ext == ".csv"

    def normalize(self, path):
        ext = os.path.splitext(path)[1].lower()
        try:
            if ext == ".json":
                data = json.loads(_read(path))
                return InputItem(path, "data_profile", structure={"profile": data},
                                 note="categorical value sets -> candidate enumerations")
            import pandas as pd
            df = pd.read_csv(path, nrows=5000)
            prof = {}
            for col in df.columns:
                vals = df[col].dropna().unique()
                if 0 < len(vals) <= 50:  # categorical -> enumeration candidate
                    prof[col] = {"distinct": [str(v) for v in vals[:50]], "n_distinct": int(len(vals))}
                else:
                    prof[col] = {"n_distinct": int(len(vals))}
            return InputItem(path, "data_profile",
                             structure={"columns": prof, "sample_rows": df.head(3).to_dict("records")},
                             note="compact profile: categorical columns -> candidate enumerations")
        except Exception as e:
            return InputItem(path, "data_profile", note=f"profile parse error: {e}",
                             status="designed-not-exercised")


@register
class DocumentAdapter(InputAdapter):
    """Document corpus (PDF/Word/PPT/Excel/HTML) -> text via the input-conversion skill."""
    type = "document"

    def detect(self, path, name, ext):
        return ext in (".pdf", ".docx", ".doc", ".pptx", ".ppt", ".xlsx", ".xls", ".html", ".htm")

    def normalize(self, path):
        ext = os.path.splitext(path)[1].lower()
        # 1) markitdown (baseline)
        try:
            from markitdown import MarkItDown
            text = MarkItDown().convert(path).text_content
            return InputItem(path, "document", text=text.strip(), note="converted via markitdown")
        except Exception:
            pass
        # 2) proven fallbacks
        try:
            if ext == ".pdf":
                from pypdf import PdfReader
                text = "\n".join((p.extract_text() or "") for p in PdfReader(path).pages)
                return InputItem(path, "document", text=text.strip(), note="converted via pypdf fallback")
            if ext in (".docx", ".doc"):
                import docx
                text = "\n".join(p.text for p in docx.Document(path).paragraphs)
                return InputItem(path, "document", text=text.strip(), note="converted via python-docx fallback")
            if ext in (".xlsx", ".xls"):
                import pandas as pd
                text = pd.read_excel(path).to_markdown()
                return InputItem(path, "document", text=text, note="converted via pandas fallback")
        except Exception as e:
            return InputItem(path, "document", note=f"no converter succeeded: {e}",
                             status="designed-not-exercised")
        return InputItem(path, "document", note="no converter available for this format; install markitdown",
                         status="designed-not-exercised")


# --------------------------------------------------------------------------- dispatch
def normalize_path(path) -> InputItem:
    name = os.path.basename(path).lower()
    ext = os.path.splitext(name)[1]
    if refused_full_dump(path, name, ext):
        return InputItem(path, "unknown", status="refused",
                         note="looks like a full data dump — provide a schema export + compact profile instead "
                              "(instance-loading is Stage-2).")
    for a in REGISTRY:
        try:
            if a.detect(path, name, ext):
                return a.normalize(path)
        except Exception as e:
            return InputItem(path, "unknown", status="refused", note=f"adapter {a.type} error: {e}")
    return InputItem(path, "unknown", status="refused", note="no adapter matched this file type")


def normalize_dir(input_dir=DEFAULT_INPUT_DIR) -> list[InputItem]:
    items = []
    for root, dirs, files in os.walk(input_dir):
        dirs[:] = [d for d in dirs if d not in ("adapters", "__pycache__", ".git")]
        for fn in files:
            if fn in ("README.md", "dependencies.md"):
                continue
            items.append(normalize_path(os.path.join(root, fn)))
    return items


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # real inputs contain non-ASCII (≤, –, é, …)
    except Exception:
        pass
    target = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_INPUT_DIR
    pack = [asdict(i) for i in normalize_dir(target)]
    print(json.dumps({"input_dir": target, "count": len(pack), "items": pack},
                     indent=2, ensure_ascii=False))
