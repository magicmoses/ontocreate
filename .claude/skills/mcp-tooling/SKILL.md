---
name: mcp-tooling
description: How to apply "reuse before build" to MCP servers — discover a ready-made server before wrapping our own, and the FastMCP pattern + KISS ordering when we must. Used by the library-scout-agent.
---

# MCP tooling (functions first, wrap last)

## Discover before you wrap
Before wrapping any tool as MCP, search the **awesome-mcp-servers catalog** and the **MCP registry** for
a ready-made server (Neo4j, databases, document processing, …). Ready-made servers referenced first live
under `mcp/`. **Reuse one when it fits; only wrap our own when none exists.**

## KISS ordering
1. **Plain Python function** first (e.g. in `tools/`). Most needs end here.
2. MCP-wrap **only** once the function is stable, needed cross-project, **and** no ready-made server does
   the job. Do not wrap everything on day one.

## Candidates to wrap (only when justified)
`registry_search` · `owl_reasoner` · `pitfall_scan` · `ontology_visualize` · `cq_sparql_run` ·
`structural_metrics` · `cost_report`.

## FastMCP pattern
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

if __name__ == "__main__":
    mcp.run()
```
Own servers live in `mcp/`. See `mcp/README.md` for the discover-before-wrap policy and the reference
example. Status of our own servers: **designed, not yet exercised** (KISS — added when a run needs them).
