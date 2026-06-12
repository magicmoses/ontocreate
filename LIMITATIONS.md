# Limitations

These are **inherent** properties of an LLM-driven, semi-autonomous ontology builder — not defects to
be patched with more internal metrics or "mitigation features." That would be false reassurance. The
honesty IS the mitigation. The orchestrator shows a short, plain-language version of this at the start
of a run; the full reasoning lives here.

## Short version (shown to the user at run start)

> **Before we start — a few honest caveats:**
> - I produce a **draft you steer**, not a finished answer — you decide at the checkpoints.
> - I can check the ontology is **consistent**, not that it's **true** — your judgment at the
>   checkpoints catches that.
> - Re-running may differ slightly; every decision is logged, so each run stays reproducible.

## The full picture

**1. The evaluation is internal-only.**
CQ coverage confirms the ontology answers *its own* questions; it cannot tell you those were the right
questions or that the model matches reality. The scenario → CQ → ontology → evaluation chain is partly
circular (the CQs are both the specification and the test), so the ontology can be *coherently wrong*
and the evaluation will still pass. External correctness stays a human / domain-expert judgment.

**2. The human gates are best-effort, not an expert sign-off.**
At H1 (competency questions) and H3 (the drawn structure) you approve while still building your own
ontology judgment. A clean diagram can hide a wrong subsumption — `is-a` vs. `part-of` looks identical
in boxes-and-arrows. The render aids your judgment; it does not guarantee correctness.

**3. Validation proves formal correctness, not semantic truth.**
The reasoner + SHACL + pitfall scan catch *formal* problems (inconsistency, unsatisfiable classes,
common modeling pitfalls). They do not catch a model that is perfectly consistent and perfectly wrong
about the world. And the same model type that built the ontology also reviews it — `checker ≠ builder`
catches carelessness, not a shared blind spot. A green reasoner means *consistent*, not *true* or
*useful*.

**4. The output is *a* draft, not a deterministic answer.**
Two runs of the same input can differ. This is expected for an LLM-driven builder. The git-versioned
project memory (`project-memory.json` + `events.jsonl`, one commit per gate) is what keeps an
individual run reproducible and auditable, and what tracks the ontology across refinement versions.

**5. Only the NeOn paths you actually exercise are proven.**
Paths the framework supports but a run does not take are *designed, not tested*. The framework **stops
and escalates** rather than silently walking an untested path.

## What this means in practice

- Treat the result as a **strong first draft** to review and refine, not as ground truth.
- Your judgment at the gates is the real quality control — slow down at H1 and H3.
- For anything high-stakes, have a domain expert glance at the competency questions and the taxonomy.
- Use the refinement loop (`/refine`) as data and use reveal what the initial design missed — that is
  the intended lifecycle, not a sign something went wrong.
