---
name: scope-discipline
description: How to enforce the cardinal rule — every class/property must trace to a CQ, or it is out. Used by the scoping-agent for /check-scope and continuously during modeling/refinement.
---

# Scope discipline (the cardinal rule)

"Limit the scope — never model more than you need." The single most important rule. Enforced
**continuously**, not once.

## The trace test
For every class and property, ask: **which frozen CQ does this serve?**
- Query the frozen CQ-set in **entity memory** (`project-memory.json`) — don't re-derive it from chat.
- Map each element → the CQ(s) it helps answer.
- An element that serves **no** CQ is **out-of-scope** → recommend removal.

## When to run
- During `/draft-ontology` (the modeling-agent self-checks before finishing).
- At `/check-scope` before gate H3.
- During every **refinement cycle** (§20a) — new elements still need a CQ; scope discipline doesn't relax
  because data proposed them. Data proposes, the human disposes at the gate.

## Posture
Honour `preferences.md` `scope_posture`. **aggressive** = cut anything that doesn't *clearly* earn a CQ;
**lenient** = keep borderline elements but flag them. When in doubt, cut — a smaller ontology that
answers its CQs beats a sprawling one that mostly doesn't.

## Output
A short table: element → serving CQ, or ✗ out-of-scope (with a one-line reason). The scoping-agent flags;
the modeling-agent removes (checker ≠ builder).
