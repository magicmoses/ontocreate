# mcp/ — ready-made servers first, our own only when none exists

Applies "reuse before build" to tooling (§9, `mcp-tooling` skill). **Discover before you wrap.**

## Policy
1. Before wrapping anything, the library-scout-agent checks the **awesome-mcp-servers catalog** and the
   **MCP registry** for a ready-made server (Neo4j, databases, document processing, …).
2. **Reuse a ready-made server** when one fits — reference it here (config + source).
3. **Wrap our own** only when none exists — and only after a plain Python function (in `tools/`) is
   stable and needed cross-project (KISS). Do not wrap everything on day one.

## Candidates to wrap (only when justified)
`registry_search` · `owl_reasoner` · `pitfall_scan` · `ontology_visualize` · `cq_sparql_run` ·
`structural_metrics` · `cost_report`.

## Status
`owl_reasoner_server.py` is the **reference FastMCP pattern** — **designed, not yet exercised** (FastMCP
is an optional baseline dependency, pulled only when we actually wrap a server). The build itself never
needs an MCP server: the equivalent logic runs as plain functions in `tools/` and in the agents.

## Credential note
No credentialed MCP server belongs on the build path. A Neo4j MCP server (if reused) is part of the
optional `/migrate-neo4j` step only, outside the autonomous loop.
