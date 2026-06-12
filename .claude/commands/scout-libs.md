---
description: "Reuse before build" for code/tooling — scout libraries + check the MCP ecosystem before wrapping.
---

Use the **library-scout-agent** (`.claude/agents/library-scout-agent.md`). Start from the fixed baseline
(`requirements.txt`, spec §8) — do not re-propose it. Discover domain/task-specific repos/libraries on
GitHub/PyPI with rationale (gap, maturity, licence).

**MCP — discover before you wrap:** check the awesome-mcp-servers catalog + the MCP registry for a
ready-made server first; reuse one when it fits; only wrap our own (FastMCP, plain function first) when
none exists. Declare approved picks to `input/dependencies.md` and write the decision to entity memory.
This feeds gate **H2**. Do not add a credentialed tool to the build path.
