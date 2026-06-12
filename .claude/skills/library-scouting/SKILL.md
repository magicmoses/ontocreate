---
name: library-scouting
description: How to scout code/libraries (GitHub/PyPI) and ready-made MCP servers, starting from the fixed baseline. Used by the library-scout-agent for /scout-libs.
---

# Library scouting ("reuse before build", for tooling)

## Start from the baseline (spec §8 / `requirements.txt`)
Always-installed, domain-agnostic: rdflib · owlready2 · the profile's reasoner (ELK/owlrl/Ontop/HermiT)
· pySHACL · OOPS! · key-free registry search · pyLODE/WebVOWL · markitdown (+ pypdf/python-docx/pandas)
· prov (L3 only) · FastMCP · spaCy (optional). **Do not re-propose baseline tools.**

## Discover (domain/task-specific)
Search GitHub/PyPI for repos/libraries that fill a real gap in the current input/domain. For each:
state the **gap it fills**, maturity (stars/commits/releases), and **licence**. Heavy, layout-aware
document converters (e.g. docling) are a per-project pick, not baseline.

## MCP — discover before you wrap
Before MCP-wrapping anything, check the **awesome-mcp-servers catalog** and the **MCP registry** for a
ready-made server (Neo4j, databases, document processing, …).
- **Reuse a ready-made server** when one fits.
- **Wrap our own** (FastMCP) only when none exists — and only after a plain Python function is stable
  and needed cross-project (`mcp-tooling`, KISS). Don't wrap everything on day one.

## Declare + integrate
Approved picks → `input/dependencies.md` (package, version, purpose, why) and `requirements.txt` /
`pyproject.toml`, isolated from the baseline. Integrate via an **input adapter** (new input type) or by
MCP-wrapping. Nothing enters the framework core. Write decisions to entity memory. Feeds gate H2.
**No credentialed tool on the build path** — credentialed tooling is Stage-2 / migration only.
