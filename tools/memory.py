#!/usr/bin/env python3
"""Tier-3 persistent project memory (memory-policy.md).

Entity   -> output/project-memory.json   (structured decisions; rewritten per gate)
Episodic -> output/events.jsonl          (append-only timeline)

Git-versioned, one commit per gate. Domain-AGNOSTIC schema; domain-SPECIFIC content.
Stdlib only, credential-free. Used by the orchestrator + the /memory command.

Usage:
  python tools/memory.py init
  python tools/memory.py show
  python tools/memory.py log [--tail N]
  python tools/memory.py set KEY VALUE        # VALUE parsed as JSON if possible, else string
  python tools/memory.py event --type T [--phase P] [--note "..."] [--json '{...}']
  python tools/memory.py gate --name H1 --outcome approved [--note "..."] [--no-commit]
"""
import argparse
import datetime
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "output")
MEM = os.path.join(OUT, "project-memory.json")
EVENTS = os.path.join(OUT, "events.jsonl")

SKELETON = {
    "schema": "ontology-creator/project-memory@1",
    "created": None,
    "ontology_version": "v0",
    "orsd_ref": None,
    "cq_set": [],
    "neon_scenarios": [],
    "owl_profile": None,
    "provenance_level": None,
    "reuse_decision": {"ontologies": [], "libraries": [], "mcp_servers": []},
    "scope_rulings": [],
    "glossary": [],
    "domain_terms": [],
}


def now():
    return datetime.datetime.now().isoformat(timespec="seconds")


def load():
    if not os.path.exists(MEM):
        return None
    with open(MEM, "r", encoding="utf-8") as f:
        return json.load(f)


def save(mem):
    os.makedirs(OUT, exist_ok=True)
    with open(MEM, "w", encoding="utf-8") as f:
        json.dump(mem, f, indent=2, ensure_ascii=False)
        f.write("\n")


def append_event(ev):
    os.makedirs(OUT, exist_ok=True)
    with open(EVENTS, "a", encoding="utf-8") as f:
        f.write(json.dumps(ev, ensure_ascii=False) + "\n")


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)


def ensure_repo():
    if not os.path.isdir(os.path.join(ROOT, ".git")):
        git("init")
        git("add", "-A")
        git("commit", "-m", "chore: initial commit (ontology-creator framework)")


def cmd_init(_):
    ensure_repo()
    mem = load() or dict(SKELETON)
    if not mem.get("created"):
        mem["created"] = now()
    save(mem)
    if not os.path.exists(EVENTS):
        open(EVENTS, "a", encoding="utf-8").close()
    append_event({"ts": now(), "type": "init", "note": "project memory initialised"})
    print(f"Initialised project memory at {os.path.relpath(MEM, ROOT)}")


def cmd_show(_):
    mem = load()
    if mem is None:
        print("No project memory yet. Run: python tools/memory.py init")
        return
    print(json.dumps(mem, indent=2, ensure_ascii=False))


def cmd_log(args):
    if not os.path.exists(EVENTS):
        print("No events yet.")
        return
    lines = open(EVENTS, encoding="utf-8").read().splitlines()
    for ln in lines[-args.tail:]:
        print(ln)


def parse_value(v):
    try:
        return json.loads(v)
    except Exception:
        return v


def cmd_set(args):
    mem = load() or dict(SKELETON, created=now())
    mem[args.key] = parse_value(args.value)
    save(mem)
    append_event({"ts": now(), "type": "set", "key": args.key})
    print(f"set {args.key}")


def cmd_event(args):
    ev = {"ts": now(), "type": args.type}
    if args.phase:
        ev["phase"] = args.phase
    if args.note:
        ev["note"] = args.note
    if args.json:
        try:
            ev["data"] = json.loads(args.json)
        except Exception as e:
            print(f"--json not valid JSON: {e}", file=sys.stderr)
            sys.exit(1)
    append_event(ev)
    print(f"event: {args.type}")


def cmd_gate(args):
    ensure_repo()
    ev = {"ts": now(), "type": "gate", "gate": args.name, "outcome": args.outcome}
    if args.note:
        ev["note"] = args.note
    append_event(ev)
    if not args.no_commit:
        git("add", "-A")
        r = git("commit", "-m", f"memory: gate {args.name} ({args.outcome})")
        if r.returncode == 0:
            print(f"gate {args.name} ({args.outcome}) recorded + committed")
        else:
            # nothing to commit is fine
            print(f"gate {args.name} ({args.outcome}) recorded (no commit: "
                  f"{(r.stdout + r.stderr).strip().splitlines()[-1] if (r.stdout+r.stderr).strip() else 'no changes'})")
    else:
        print(f"gate {args.name} ({args.outcome}) recorded (commit skipped)")


def main():
    p = argparse.ArgumentParser(description="Tier-3 project memory")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init").set_defaults(func=cmd_init)
    sub.add_parser("show").set_defaults(func=cmd_show)
    lg = sub.add_parser("log"); lg.add_argument("--tail", type=int, default=20); lg.set_defaults(func=cmd_log)
    st = sub.add_parser("set"); st.add_argument("key"); st.add_argument("value"); st.set_defaults(func=cmd_set)
    ev = sub.add_parser("event")
    ev.add_argument("--type", required=True); ev.add_argument("--phase"); ev.add_argument("--note"); ev.add_argument("--json")
    ev.set_defaults(func=cmd_event)
    gt = sub.add_parser("gate")
    gt.add_argument("--name", required=True); gt.add_argument("--outcome", required=True)
    gt.add_argument("--note"); gt.add_argument("--no-commit", action="store_true")
    gt.set_defaults(func=cmd_gate)
    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
