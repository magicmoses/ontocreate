---
description: Recommend the provenance level (L1/L2/L3) from the input + CQs. Confirmed at H2.
---

Use the **scoping-agent** (`.claude/agents/scoping-agent.md`). Recommend a provenance level using the
selection rule in `provenance-levels.md` and `provenance-policy.md`:
L1 source-level (clean structured input, low stakes) · L2 statement-level + evidence + confidence
(LLM-extracted / scientific — the common default) · L3 full PROV-O activity chain (audit/compliance).

Only the chosen level's properties get declared by the modeling-agent. Confirmed by the human at **H2**.
Record the recommendation + rationale in entity memory.
