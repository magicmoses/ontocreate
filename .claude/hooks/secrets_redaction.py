#!/usr/bin/env python3
"""PreToolUse guardrail: block a Write/Edit that would persist a LITERAL secret into a tracked file.

The build is credential-free, so in normal operation there is nothing to redact. This is a standalone
safety net: if any step (e.g. the optional Neo4j migration) ever tries to hardcode a credential, it is
blocked. Env-var references (the correct pattern) are allowed; only hardcoded literal values are blocked.
Fail-open: any parsing problem exits 0 so the hook can never wedge the harness.
"""
import json
import re
import sys

# Patterns for LITERAL secrets.
PATTERNS = [
    re.compile(r"-----BEGIN (?:[A-Z ]+ )?PRIVATE KEY-----"),
    # scheme://user:password@host  (credentials embedded in a connection string)
    re.compile(r"\b(?:bolt|neo4j|postgres(?:ql)?|mysql|mongodb(?:\+srv)?|redis)://[^\s/@:]+:[^\s/@]+@"),
    re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"),        # OpenAI-style key
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),           # AWS access key id
    # literal assignment: password = "somevalue"
    re.compile(r"(?i)(?:password|passwd|secret|api[_-]?key|token)\s*[:=]\s*['\"][^'\"]{6,}['\"]"),
]
# A value that references an env var is allowed (not a literal secret).
ENV_REF = re.compile(r"(?i)(os\.environ|getenv|process\.env|\$env:|\$\{?[A-Z0-9_]+\}?|%[A-Z0-9_]+%)")


def content_and_path(tool, ti):
    if tool == "Write":
        return ti.get("content", "") or "", ti.get("file_path", "") or ""
    if tool in ("Edit", "MultiEdit"):
        parts = []
        if "new_string" in ti:
            parts.append(ti.get("new_string", "") or "")
        for e in ti.get("edits", []) or []:
            parts.append(e.get("new_string", "") or "")
        return "\n".join(parts), ti.get("file_path", "") or ""
    return "", ""


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)
    content, path = content_and_path(data.get("tool_name", ""), data.get("tool_input", {}) or {})
    if not content:
        sys.exit(0)
    norm = path.replace("\\", "/")
    # Don't scan the secret store itself or the detector definitions.
    if norm.endswith(".env") or "/.env" in norm or "/.claude/hooks/" in norm:
        sys.exit(0)
    for pat in PATTERNS:
        for m in pat.finditer(content):
            start = content.rfind("\n", 0, m.start()) + 1
            end = content.find("\n", m.end())
            line = content[start: end if end != -1 else len(content)]
            if ENV_REF.search(line):
                continue  # env-var reference, allowed
            sys.stderr.write(
                f"BLOCKED by secrets-redaction hook: a literal secret would be written to '{path}'. "
                "The build is credential-free. Reference an env var "
                "(e.g. NEO4J_PASSWORD in .env) instead of a literal value.\n")
            sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
