# Hooks — guardrails that fire on events (no idle context cost)

These are the framework's guardrails, run as Claude Code hooks instead of always-on context — "red
squigglies for agents": they consume zero context until they fire, and correct at the moment of the
mistake (`memory-policy.md`, spec §12). Wired in `.claude/settings.json`.

| Hook | Event | What it does | Decision |
|---|---|---|---|
| `secrets_redaction.py` | PreToolUse (Write/Edit) | blocks a write that would persist a **literal** secret into a deliverable; env-var references are allowed | **blocks** (exit 2) |
| `domain_leak.py` | PreToolUse (Write/Edit) | blocks domain-specific terms (sourced from the project's *own* `output/project-memory.json`, so the check stays agnostic) from being written into `.claude/**` | **blocks** (exit 2) |
| `scope_check.py` | PostToolUse (Write/Edit) | after `ontology.ttl` is written, nudges to run `/check-scope` + reports class/property counts | advisory (exit 0) |

## Notes
- All three **fail-open**: any parsing error exits 0, so a hook can never wedge the harness.
- `domain_leak.py` no-ops until a project has recorded domain terms, and only fires on `.claude/**`
  writes — so it never interferes with framework building or with output/ work.
- `secrets_redaction.py` skips `.env*` and `.claude/hooks/**` (where the detector patterns live).
- Claude Code requires the user to review/approve project hooks before they run (`/hooks`). That is the
  intended security posture — approve them once and they enforce silently thereafter.
- Python is used (cross-platform; already a framework dependency). Commands assume `python` is on PATH.
