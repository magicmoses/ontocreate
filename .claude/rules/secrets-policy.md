# Rule: secrets policy

**The build is credential-free — that is the strongest security measure (zero attack surface).** This
rule is referenced by **`/migrate-neo4j` only**; nothing in the autonomous loop touches a secret.

## In the build (always)
- No DB connections, no API keys, no auth. If a step seems to need a credential, it is in the wrong
  stage — stop. Credentialed registries/tools are Stage-2, not the build.
- Never write a secret into `ontology.ttl`, `project-memory.json`, `events.jsonl`, the cost log, or a
  visualization.

## For `/migrate-neo4j` (the only credentialed step — keep it proportionate, no vault theater)
- Credentials live in **`.env`** (git-ignored — see `.gitignore`).
- Agents/scripts reference **env vars** (e.g. `NEO4J_PASSWORD`), **never** the literal value.
- **Redact** secrets from any memory/cost logs.
- Use a **least-privilege** DB user / project-scoped key.

## Enforcement
The `secrets-redaction` hook (`.claude/hooks/`) scans Write/Edit content for secret-shaped strings
(passwords, connection strings, API keys, private keys) and **blocks** a write that would persist one
into a deliverable. Fail-safe: if unsure, block and ask.
