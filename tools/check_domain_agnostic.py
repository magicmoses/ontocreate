#!/usr/bin/env python3
"""Domain-agnostic invariant scanner (domain-agnostic.md, /self-audit).

Scans the framework core for the PROJECT'S OWN domain terms (sourced from output/project-memory.json:
glossary + domain_terms). The check stays agnostic because the term list comes from the project's
memory, not a hardcoded list. Reports any leak of domain content into the agnostic core.

Scanned (agnostic core): .claude/, tools/, mcp/, and the root framework reference files.
Not scanned (domain layer, allowed to be specific): input/, output/.
Exit 0 = clean / nothing to check; exit 1 = leak found.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE_DIRS = [".claude", "tools", "mcp"]
# Reusable framework reference docs. The MASTER prompt is the build SPEC (generic methodology prose,
# not a reusable artifact) and is deliberately excluded — its ordinary verbs collide with domain
# property names. NOTE: this scan is a heuristic advisory; a domain term that is also a common English
# word (a generic verb, say) can false-positive against framework prose. Treat hits as candidates for
# human review, not proof of a leak.
CORE_FILES = ["CLAUDE.md", "README.md", "LIMITATIONS.md", "preferences.md",
              "neon-scenarios.md", "provenance-levels.md"]
SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv"}
# Machine-generated local state (Claude Code settings.local.json records session commands verbatim,
# which legitimately contain domain terms) — not authored framework content, so not scanned.
SKIP_FILE_SUFFIXES = (".local.json",)


def load_terms():
    mem_path = os.path.join(ROOT, "output", "project-memory.json")
    if not os.path.exists(mem_path):
        return []
    try:
        mem = json.load(open(mem_path, encoding="utf-8"))
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


def iter_files():
    for d in CORE_DIRS:
        base = os.path.join(ROOT, d)
        for root, dirs, files in os.walk(base):
            dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
            for fn in files:
                if fn.endswith(SKIP_FILE_SUFFIXES):
                    continue
                if fn.endswith((".md", ".py", ".json", ".txt", ".yaml", ".yml")):
                    yield os.path.join(root, fn)
    for fn in CORE_FILES:
        p = os.path.join(ROOT, fn)
        if os.path.exists(p):
            yield p


def main():
    terms = load_terms()
    if not terms:
        print("No domain terms recorded in project memory yet - nothing to check. "
              "The framework core is agnostic by construction.")
        sys.exit(0)
    pats = [(t, re.compile(r"(?i)\b" + re.escape(t) + r"\b")) for t in terms]
    leaks = []
    for path in iter_files():
        try:
            text = open(path, encoding="utf-8", errors="ignore").read()
        except Exception:
            continue
        for t, pat in pats:
            if pat.search(text):
                leaks.append((os.path.relpath(path, ROOT), t))
    if leaks:
        print(f"DOMAIN LEAK: {len(leaks)} occurrence(s) of project domain terms in the agnostic core:")
        for rel, t in leaks:
            print(f"  {rel}: '{t}'")
        sys.exit(1)
    print(f"Clean: none of the {len(terms)} recorded domain term(s) appear in the framework core.")
    sys.exit(0)


if __name__ == "__main__":
    main()
