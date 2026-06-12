# Rule: human-in-the-loop gates

Four explicit STOP points. The framework drafts; **the human decides** before proceeding. No silent
progression past a gate. Each gate uses the one gate format (`communication.md`) and **commits project
memory** (`memory-policy.md`) before stopping.

| Gate | After | The human reviews / decides |
|---|---|---|
| **H1** | `/scenarios` + `/elicit-cqs` | scenarios + CQ set + ORSD. **Iterative** — refine/add/cut as often as needed; **scope freezes only on accept**. Nothing is modeled before H1. |
| **H2** | direction commands | NeOn scenario(s) · reuse (ontologies + libraries + which ready-made MCP servers to reuse vs. wrap) · OWL profile · provenance level. **No storage/credential decision — the build is backend-free.** |
| **H3** | `/draft-ontology` + `/visualize` | the rendered ontology structure. |
| **H4** | `/validate` + `/eval` | correctness + the evaluation scorecard; iterate vs. accept. |

## Discipline
- At each gate: short summary + a `/visualize` render where useful → **commit project memory** → STOP
  and wait.
- The gates are **best-effort, not an expert sign-off** (Limitation 2). A clean diagram can hide a wrong
  subsumption. Slow down at H1 and H3.
- Defaults at the gates come from `preferences.md` but **never override** the human's decision.
- Semantic/content decisions are **only** made here (and in `/refine`) — never by an autonomous loop.
