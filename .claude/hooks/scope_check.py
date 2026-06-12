#!/usr/bin/env python3
"""PostToolUse advisory: after output/ontology.ttl is written, nudge to run /check-scope against the
frozen CQ-set and report quick class/property counts. Non-blocking (exit 0). Fail-open.

This is the "red squiggly" for scope discipline — it costs no idle context and fires only on the one
event that matters (a TTL write).
"""
import json
import sys


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)
    ti = data.get("tool_input", {}) or {}
    path = (ti.get("file_path") or "").replace("\\", "/")
    if not path.endswith("ontology.ttl"):
        sys.exit(0)
    counts = ""
    try:
        import rdflib
        from rdflib.namespace import RDF, RDFS, OWL
        g = rdflib.Graph().parse(path, format="turtle")
        ncls = len(set(g.subjects(RDF.type, OWL.Class)) | set(g.subjects(RDF.type, RDFS.Class)))
        nop = len(set(g.subjects(RDF.type, OWL.ObjectProperty)))
        ndp = len(set(g.subjects(RDF.type, OWL.DatatypeProperty)))
        counts = f" ({ncls} classes, {nop} object + {ndp} datatype properties)"
    except Exception:
        pass
    sys.stderr.write(
        f"[scope-check] ontology.ttl updated{counts}. Reminder: run /check-scope — every class/"
        "property must trace to a frozen CQ (scope-discipline.md); remove orphans before gate H3.\n")
    sys.exit(0)


if __name__ == "__main__":
    main()
