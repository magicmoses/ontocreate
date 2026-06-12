# Rule: memory policy

Three tiers + a thin user-scoped preference file. Do not bolt on a memory *framework* (graphiti / mem0 /
Letta — those are Stage-2 application tools). Most "memory types" are already framework artifacts; the
one piece we add is **persistent project memory**.

## The tiers
- **Tier 1 — static** (procedural + semantic): the agents' skills + rules; the reference files
  (`neon-scenarios.md`, `provenance-levels.md`) + reused ontologies. Domain-agnostic core.
- **Tier 2 — ephemeral session** (working + conversational + summary): active context, in-progress
  `output/` files, the live gate dialogue, rolling compression. Orchestrator-managed; **no persistence**.
  Gate decisions are **promoted to Tier 3**.
- **Tier 3 — persistent project memory** (entity + episodic): the versioning / audit layer.
  - **Entity** → `output/project-memory.json` (rewritten per gate): ORSD ref, frozen CQ-set, NeOn class,
    OWL profile, provenance level, reuse + scope decisions, **ontology version**.
  - **Episodic** → `output/events.jsonl` (**append-only**): each gate outcome, validation/eval results,
    attempt counts, escalations, refinement cycles.
  - **Git-versioned, one commit per gate** — the build's process-provenance; what makes a
    non-deterministic run reproducible (Limitation 4) and tracks the ontology across versions.

## Per-agent map
orchestrator → working+summary, writes episodic, reads preferences · scenario-and-cq → writes entity
(ORSD, CQ-set) · scoping → reads entity (CQ-set) + preferences, writes entity (decisions) · researcher →
writes entity (reuse) + extends semantic · library-scout → writes entity (`dependencies.md`) · modeling →
reads entity + semantic, writes the ontology · validation/evaluation → write episodic.

## Context & KV-cache discipline (target ≥80% cache-hit)
- **Stable first, volatile last** — agent prompts, rules, reference files, frozen CQ-set + decisions go
  to the front; the current TTL draft, latest tool output, live gate dialogue go last.
- **Append, don't rewrite** — `events.jsonl` is append-only (cache-safe); `project-memory.json` is
  rewritten per gate, so keep it late in context / pass deltas.
- **Summarise only at gate boundaries**, never mid-phase (compression busts the cache prefix).
- Give each subagent the **frozen CQ-set + relevant decisions**, not the whole history. Summary memory is
  lossy — the **authoritative decisions live in Tier-3 entity memory**, not only in rolling context.

## Tooling
Reads/writes go through `tools/memory.py` (entity update + episodic append + commit-per-gate). The
`/memory` command views it. `preferences.md` is user-scoped (carries across projects); Tier-3 is
project-scoped.
