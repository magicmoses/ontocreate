# Rule: self-verification (build the framework with its own discipline)

The meta-build obeys the same loop it preaches: **build → verify → correct, checker ≠ builder, 3-attempt
bound before escalating**. These checks are run by `/self-audit` and must be re-run after any change to
the framework.

## Verify each layer before starting the next
- **agents** — valid frontmatter; single clear responsibility; no domain leakage; no two agents claim the
  same responsibility; no responsibility unowned.
- **commands** — every command maps to an owning agent; no orphans; `/start` exists and runs onboarding.
- **skills** — every skill is referenced by an agent or command (incl. `input-conversion`); no dead skills.
- **rules + reference files** — rules mutually consistent; `communication.md` governs user-facing output;
  the provided files (`neon-scenarios.md`, `provenance-levels.md`, `memory-policy.md`, `secrets-policy.md`,
  `preferences.md`) are referenced by the agents/steps that consume them.
- **memory layer** — entity (`project-memory.json`) + episodic (`events.jsonl`) writers exist;
  one-commit-per-gate wired; `preferences.md` read for gate defaults; agents write to the assigned tiers.

## `/self-audit` consistency pass (before the dry-run)
- `LIMITATIONS.md` exists; the short version is surfaced at run start.
- Every gate H1–H4 names existing agents/commands; the gate format is applied.
- Every derivation-chain link (scenario→CQ→ontology→evaluation) has an owning agent.
- Every one of the 6 process steps maps to exactly one owner; no orphan steps.
- **Domain-agnostic invariant** — scan all framework files for hardcoded domain terms; flag leaks.
- **Build path is backend-free** — no DB/credential dependency in the loop; `secrets-policy.md` referenced
  only by `/migrate-neo4j`.
- Baseline (§8), integration seam (§9), OSS packaging (§11), refinement+versioning (§20a) all wired.
- Guardrails run as **hooks** (no idle context cost); context structured stable-first for cache reuse.
- **feedback-agent is bounded** — process-only, project-scoped (`output/refinements/`), git-reversible,
  never writes `.claude/`, never optimises eval scores, never touches semantic decisions.

## The dry-run (final integration self-test)
Run the full path on a throwaway prompt input; stop at each gate; **commit project memory at each gate**;
produce all OSS-artifact outputs; exercise `/feedback`. Fix any failing step/gate before declaring done.
Honesty rule: only claim a check that actually ran (Limitation 5).
