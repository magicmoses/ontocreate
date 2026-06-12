---
description: "Reuse before build" for ontologies — search key-free registries, recommend reuse/extend/merge/build.
---

Use the **researcher-agent** (`.claude/agents/researcher-agent.md`). Search **key-free** registries
chosen from the input (defaults: LOV, EBI OLS) for vocabularies/ontologies that fit the CQs + starter
glossary. Judge candidates on coverage / precision / consensus / quality / licence.

Recommend per concept-cluster: reuse as-is · reuse + adapt · reuse + merge · apply a design pattern ·
build new — with the candidate IRIs/prefixes and the matching NeOn scenario. Never pull a credentialed
registry (e.g. BioPortal key) in the credential-free build. Write the reuse decision to entity memory.
This feeds gate **H2**.
