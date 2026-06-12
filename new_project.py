#!/usr/bin/env python3
"""Scaffold a new ontology project from this framework — one command, no install, stdlib only.

    python new_project.py my-onto       # copies the agnostic framework into ./my-onto

Then: put material in my-onto/input/ (or `/ingest-input <path>` in Claude Code), open it in Claude Code,
and run /start. Versioning (git, one commit per gate) is handled by the framework on /start.

Copies only the agnostic framework — never domain content or machine/session state. (On GitHub, the
"Use this template" button does the same with zero commands.)
"""
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DIRS = [".claude", "tools", "mcp", "migration"]
FILES = ["LIMITATIONS.md", "preferences.md", "neon-scenarios.md", "provenance-levels.md",
         "CLAUDE.md", "requirements.txt", ".gitignore"]
INPUT_KEEP = ["adapters", "README.md", "dependencies.md"]
IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc", ".pytest_cache",
                                "settings.local.json", "*.local.json", "*.egg-info")

README = """# {name}

Ontology project built with the domain-agnostic **ontology-creator framework**.

- `input/` — drop your material here (description, DB schema, docs, glossary, existing ontology), or
  point `/ingest-input <path>` at any folder. Domain content lives ONLY in `input/` and `output/`.
- `.claude/`, `tools/`, `mcp/` — the framework (agnostic; don't edit per project).
- `output/` — generated on first run (ORSD, ontology.ttl, docs, evaluation, project memory).

## Three steps
1. (done) you scaffolded this project.
2. Add material to `input/` (or `/ingest-input <path>`).
3. Open in Claude Code and run **`/start`**. Read `LIMITATIONS.md` first.
"""


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: python new_project.py <target_dir> [name]")
    target = os.path.abspath(sys.argv[1])
    name = sys.argv[2] if len(sys.argv) > 2 else os.path.basename(target.rstrip("/\\"))
    if os.path.isdir(target) and os.listdir(target):
        sys.exit(f"refusing: '{target}' exists and is not empty.")
    if target == ROOT:
        sys.exit("refusing: target is the framework itself.")

    for d in DIRS:
        src = os.path.join(ROOT, d)
        if os.path.isdir(src):
            shutil.copytree(src, os.path.join(target, d), ignore=IGNORE, dirs_exist_ok=True)
    for f in FILES:
        src = os.path.join(ROOT, f)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(target, f))
    os.makedirs(os.path.join(target, "input"), exist_ok=True)
    for item in INPUT_KEEP:
        src = os.path.join(ROOT, "input", item)
        dst = os.path.join(target, "input", item)
        if os.path.isdir(src):
            shutil.copytree(src, dst, ignore=IGNORE, dirs_exist_ok=True)
        elif os.path.exists(src):
            shutil.copy2(src, dst)
    with open(os.path.join(target, "README.md"), "w", encoding="utf-8") as fh:
        fh.write(README.format(name=name))

    print(f"Scaffolded '{name}' at {target}")
    print("Next: add material to input/, open the folder in Claude Code, run /start.")


if __name__ == "__main__":
    main()
