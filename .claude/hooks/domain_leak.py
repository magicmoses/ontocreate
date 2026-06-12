#!/usr/bin/env python3
"""PreToolUse guardrail: keep domain-specific terms OUT of the agnostic framework core (.claude/).

The HARD CONSTRAINT (domain-agnostic.md): domain content lives only in input/ and output/. This hook
stays agnostic itself by sourcing the term list from the PROJECT'S OWN memory
(output/project-memory.json: glossary + domain_terms) rather than any hardcoded list. It therefore
no-ops until a project has recorded domain terms, and only fires on writes to .claude/**.
Fail-open: any problem exits 0.
"""
import json
import os
import re
import sys


def load_domain_terms():
    path = os.path.join("output", "project-memory.json")
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            mem = json.load(f)
    except Exception:
        return []
    terms = set()
    glossary = mem.get("glossary") or mem.get("starter_glossary") or []
    if isinstance(glossary, dict):
        glossary = list(glossary.keys())
    for src in (glossary, mem.get("domain_terms", []) or []):
        for t in src:
            if isinstance(t, str) and len(t.strip()) > 3:
                terms.add(t.strip())
    return sorted(terms)


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
    norm = path.replace("\\", "/")
    if norm.endswith(".local.json"):
        sys.exit(0)  # machine-generated local state (records session commands verbatim) — not authored
    if "/.claude/" not in norm and not norm.startswith(".claude/"):
        sys.exit(0)  # only guard the framework core
    if not content:
        sys.exit(0)
    terms = load_domain_terms()
    hits = [t for t in terms if re.search(r"(?i)\b" + re.escape(t) + r"\b", content)]
    if hits:
        sys.stderr.write(
            f"BLOCKED by domain-leak hook: domain term(s) {hits[:8]} would be written into the "
            f"agnostic framework core ('{path}'). Domain content belongs in input/ and output/, not "
            ".claude/ (domain-agnostic.md). Move it to the input/output layer.\n")
        sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
