---
description: Log/show tokens, $ estimate, and reasoner time per run — so scope decisions see cost.
---

Act as the **orchestrator-agent** (observability). Run `python tools/cost.py show` to display the current
run's cost log (`output/cost-log.jsonl`): tokens, $ estimate, reasoner time, plus the OWL profile and
provenance level (which drive cost). To record an entry: `python tools/cost.py log --phase <phase>
--note "<note>"`.

This is a **logger, not a hard cap** — it informs the human, who decides at the gates. Surface cost when
scope or provenance is being chosen, so heavier choices are made with their cost in view. $ARGUMENTS
