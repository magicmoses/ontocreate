# Rule: domain-agnostic (HARD CONSTRAINT)

**No agent, command, skill, rule, hook, or tool may hardcode knowledge from any specific domain.**

## Where things live
- **Framework core** (`.claude/`, `tools/`, `mcp/`, the root reference files) — **domain-agnostic only**.
  Generic methodology, generic tooling, generic schema.
- **Domain content** — only `input/` (what the user provides) and `output/` (what the run produces).
- **Memory:** the *schema* is domain-agnostic; the *content* is domain-specific. A glossary of domain
  terms belongs in `output/project-memory.json` (content), never baked into a rule or agent.

## The test
If you catch yourself writing a concrete domain concept (a specific entity, a field name from the user's
schema, a term from their corpus) into a framework file, **that is a bug** — move it to the input/output
layer. Naming a *general-purpose* tool or registry (rdflib, LOV, EBI OLS) is fine; naming the *user's
domain* is not.

## Enforcement
- The `domain-leak` hook (`.claude/hooks/`) scans writes to `.claude/**` for the project's own domain
  terms (pulled from `output/project-memory.json` — so the check itself stays agnostic) and flags leaks.
- `/self-audit` scans all framework files for hardcoded domain terms.

This is what makes the framework **reusable** across domains. Guard it.
