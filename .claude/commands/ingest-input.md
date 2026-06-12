---
description: Read input/ (or a given path), auto-detect and normalise every input into a typed input pack.
argument-hint: [optional folder path]
---

Use the **input-agent** (`.claude/agents/input-agent.md`). Scan `input/` (or the path in $ARGUMENTS),
auto-detect each file's type, and normalise it via the right adapter — documents through the
**input-conversion** skill, structured sources through their adapters.

Refuse the wrong granularity plainly: a live DB connection (credentials) or a full data dump
(instance-loading is Stage-2) — ask for a schema export + optional compact profile as files instead.

Output a short typed inventory (file → type → one-line note) and hand the clean pack to the
scenario-and-cq and scoping agents. Record what was ingested in the episodic log. If only a prompt (or
too little) exists, recommend `/interview`. Do not model.
