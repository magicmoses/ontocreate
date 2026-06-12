#!/usr/bin/env python3
"""Lightweight cost logger (spec §14). A logger, not a hard cap — it informs the human, who decides at
the gates. Provenance level, OWL profile, and corpus size drive cost; surface it so scope decisions are
made with cost in view. Stdlib only, credential-free.

Usage:
  python tools/cost.py log --phase modeling [--tokens 12000] [--dollars 0.18] [--reasoner-seconds 2.4] [--note "..."]
  python tools/cost.py show
"""
import argparse
import datetime
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "output")
LOG = os.path.join(OUT, "cost-log.jsonl")
MEM = os.path.join(OUT, "project-memory.json")


def now():
    return datetime.datetime.now().isoformat(timespec="seconds")


def cmd_log(args):
    os.makedirs(OUT, exist_ok=True)
    entry = {"ts": now(), "phase": args.phase}
    if args.tokens is not None:
        entry["tokens"] = args.tokens
    if args.dollars is not None:
        entry["dollars"] = args.dollars
    if args.reasoner_seconds is not None:
        entry["reasoner_seconds"] = args.reasoner_seconds
    if args.note:
        entry["note"] = args.note
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(f"cost logged: {args.phase}")


def cmd_show(_):
    profile = provenance = None
    if os.path.exists(MEM):
        try:
            mem = json.load(open(MEM, encoding="utf-8"))
            profile, provenance = mem.get("owl_profile"), mem.get("provenance_level")
        except Exception:
            pass
    print(f"OWL profile: {profile or '-'} | provenance level: {provenance or '-'} "
          "(these drive cost)")
    if not os.path.exists(LOG):
        print("No cost entries yet.")
        return
    rows = [json.loads(l) for l in open(LOG, encoding="utf-8").read().splitlines() if l.strip()]
    tok = sum(r.get("tokens", 0) for r in rows)
    usd = sum(r.get("dollars", 0.0) for r in rows)
    sec = sum(r.get("reasoner_seconds", 0.0) for r in rows)
    print(f"\n{'phase':<16}{'tokens':>10}{'$':>10}{'reasoner_s':>12}")
    for r in rows:
        print(f"{r.get('phase',''):<16}{r.get('tokens',0):>10}{r.get('dollars',0.0):>10.4f}{r.get('reasoner_seconds',0.0):>12.2f}")
    print(f"{'TOTAL':<16}{tok:>10}{usd:>10.4f}{sec:>12.2f}")


def main():
    p = argparse.ArgumentParser(description="Cost logger")
    sub = p.add_subparsers(dest="cmd", required=True)
    lg = sub.add_parser("log")
    lg.add_argument("--phase", required=True)
    lg.add_argument("--tokens", type=int)
    lg.add_argument("--dollars", type=float)
    lg.add_argument("--reasoner-seconds", type=float, dest="reasoner_seconds")
    lg.add_argument("--note")
    lg.set_defaults(func=cmd_log)
    sub.add_parser("show").set_defaults(func=cmd_show)
    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
