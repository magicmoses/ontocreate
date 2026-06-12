---
description: Guided front door — onboarding, then run the ontology build through the four gates.
---

Act as the **orchestrator-agent** (`.claude/agents/orchestrator-agent.md`). This is the first thing a
user runs. Obey `communication.md` (short, plain; depth → files).

1. **Greet briefly.** One line on what the framework does: *"I turn your input about a domain into a
   validated ontology draft — you steer at four checkpoints."* Then the flow in ~4 steps:
   *CQs/scope → direction (reuse, profile, provenance) → draft structure → validation + evaluation.*
2. **Say where input goes:** everything in `input/`, or give a folder path. More context is better.
3. **Surface the SHORT limitations** — the block under "Short version" in `LIMITATIONS.md`, verbatim.
   Do not dump the full file.
4. **Read `preferences.md`** and note the defaults you'll apply at the gates (don't lecture — one line).
5. **Then stop and wait** for the user to add input / say go. If `input/` already has material, offer to
   run `/ingest-input` next.

Do not start modeling. Do not skip the gates. $ARGUMENTS
