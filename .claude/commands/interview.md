---
description: Structured elicitation when only a prompt exists — ask questions to build the rest of the input.
---

Use the **input-agent** (`.claude/agents/input-agent.md`) in interview mode. When the input is thin,
ask **structured** questions, one focused batch at a time (obey `communication.md` — short):
domain & goal · intended users/uses · the key entities · the questions the ontology must answer ·
existing vocabularies to reuse · stakes / audit needs (this informs the provenance level).

Capture the answers into `input/` as notes the input-agent can normalise. Keep it tight; stop when you
have enough to draft motivating scenarios. Do not model. $ARGUMENTS
