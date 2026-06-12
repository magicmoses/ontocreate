---
description: Recommend the OWL profile (EL/QL/RL/DL) from what the CQs need. Confirmed at H2.
---

Use the **scoping-agent** (`.claude/agents/scoping-agent.md`). Recommend an OWL profile from what the
**CQs** actually require, not from habit — consult `owl-profile-tradeoff.md`:
EL (fast/scalable, limited expressivity; ELK) · QL (query answering over large data; Ontop) ·
RL (rule materialisation; owlrl) · DL (most expressive, reasoning can blow up; HermiT).

`preferences.md` may set a default (currently EL); the human still confirms at **H2**. Only the chosen
profile's reasoner is installed. Record the recommendation in entity memory with the tradeoff rationale.
