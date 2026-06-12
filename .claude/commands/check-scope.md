---
description: Scope gate — verify every class/property traces to a CQ; flag orphans for removal.
---

Use the **scoping-agent** (`.claude/agents/scoping-agent.md`). Query the frozen CQ-set in entity memory.
For every class and property in `output/ontology.ttl`, identify **which CQ it serves**. List any element
that serves none as **out-of-scope** and recommend removal (honour the `scope_posture` preference).

This is the cardinal rule (limit the scope), enforced continuously — at draft time, before H3, and
during every refinement cycle. Report a short table: element → serving CQ (or ✗ out-of-scope).
