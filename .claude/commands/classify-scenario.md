---
description: Classify the project into one or more NeOn scenarios (always incl. Scenario 1).
---

Use the **scoping-agent** (`.claude/agents/scoping-agent.md`). From the candidate resources found in the
input, classify the project into NeOn scenario(s), consulting `neon-scenarios.md`. Always include
Scenario 1 (the core build). A DB schema → Scenario 2; an existing ontology to reuse → 3/4/5/6; design
patterns → 7; restructuring/localization → 8/9.

Implement only classified paths; if a needed path is untested, **stop and escalate** (Limitation 5).
Record the classification in entity memory. This feeds gate **H2**.
