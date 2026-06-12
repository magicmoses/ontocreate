---
description: Consistency pass over the whole framework structure (run before the dry-run / after changes).
---

Act as the **orchestrator-agent**. Run the structural consistency checks in `self-verification.md`
against the repo (this is the framework checking itself — checker ≠ builder, 3-attempt bound). Report a
short PASS/FAIL table:

- `LIMITATIONS.md` exists; the orchestrator surfaces the **short** version at run start.
- `/start` is wired and runs onboarding; `communication.md` brevity holds for user-facing output.
- Every gate H1–H4 names existing agents/commands; the gate format is applied.
- Every link in the derivation chain (scenario→CQ→ontology→evaluation) has an owning agent.
- Every one of the 6 process steps maps to exactly one owner; no orphan steps; no duplicated ownership.
- **Domain-agnostic invariant** — scan all framework files (`.claude/`, root refs) for hardcoded domain
  terms; flag leaks (run `python tools/check_domain_agnostic.py` if present).
- **Build path is backend-free** — no DB/credential dependency in the loop; `secrets-policy.md` is
  referenced only by `/migrate-neo4j`.
- Baseline (§8), integration seam (§9), OSS packaging (§11), refinement+versioning (§20a) all wired.
- Guardrails run as hooks (`.claude/hooks/`); feedback-agent is bounded (process-only, project-scoped).
- Every command maps to an owning agent; every skill is referenced; no dead skills/orphan commands.

Fix any FAIL before the dry-run. $ARGUMENTS
