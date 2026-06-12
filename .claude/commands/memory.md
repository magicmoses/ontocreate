---
description: View the persistent project memory — the decisions (entity) + the build history (episodic).
---

Act as the **orchestrator-agent**. Show the project's Tier-3 memory (read-only):
- **Entity** (`output/project-memory.json`) — ORSD ref, frozen CQ-set, NeOn classification, OWL profile,
  provenance level, reuse + scope decisions, ontology version. Run `python tools/memory.py show`.
- **Episodic** (`output/events.jsonl`) — the timestamped gate/validation/eval/refinement record. Run
  `python tools/memory.py log --tail 20`.

Present a short, readable summary (obey `communication.md`). This is the audit trail / reproducibility
layer and what tracks the ontology across versions. Do not edit memory here — it is written by the
agents at the gates. $ARGUMENTS
