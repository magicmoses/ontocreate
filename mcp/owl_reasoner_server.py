#!/usr/bin/env python3
"""Reference FastMCP server (spec §9) — DESIGNED, NOT YET EXERCISED.

KISS ordering: a plain Python function comes first; wrap as MCP only once it is stable, needed
cross-project, and no ready-made server already does the job (see mcp/README.md). This file documents
the wrapping pattern so a future run can lift it verbatim. It is not imported by the build.

Run (only after `pip install fastmcp owlready2`, and with a Java runtime for HermiT):
    python mcp/owl_reasoner_server.py
"""

try:
    from fastmcp import FastMCP
    from owlready2 import get_ontology, sync_reasoner

    mcp = FastMCP("owl-reasoner")

    @mcp.tool()
    def check_consistency(ttl_path: str) -> dict:
        """Load an ontology and report consistency + unsatisfiable classes."""
        onto = get_ontology(ttl_path).load()
        with onto:
            sync_reasoner()
        bad = list(onto.inconsistent_classes())
        return {"consistent": len(bad) == 0, "unsatisfiable": [c.name for c in bad]}

    if __name__ == "__main__":
        mcp.run()

except ImportError:
    if __name__ == "__main__":
        print("Designed, not yet exercised: install `fastmcp` and `owlready2` (and a Java runtime for "
              "HermiT) to run this reference server. The build does not require it — equivalent logic "
              "runs as plain functions in tools/ and in the validation-agent.")
