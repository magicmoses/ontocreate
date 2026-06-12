---
name: scenarios-and-cqs
description: How to turn input into motivating scenarios and testable competency questions (CQs), cluster them, and formalise each as a SPARQL template. Used by the scenario-and-cq-agent for /scenarios and /elicit-cqs.
---

# Scenarios & Competency Questions

The top of the derivation chain (`derivation-chain.md`): **scenario → CQ → ontology → evaluation**. Do
this before any class is drawn.

## Motivating scenarios
- A scenario is a **short narrative** of a real situation the ontology must support — who needs what
  answer, in what context. Not a class list, not a feature list.
- Ground every scenario in the input pack. If the input can't support a scenario, don't invent it —
  recommend `/interview`.
- A handful of focused scenarios beats a sprawl. Each should imply several CQs.

## Competency questions
- A CQ is a **specific, testable question** the ontology must answer (e.g. "Which X relate to Y under
  condition Z?"). If you can't imagine a query that answers it, it's too vague — sharpen or drop it.
- **Cluster** CQs into themes; merge duplicates; split compound questions; remove any CQ no scenario
  motivates.
- Keep the set tight. More CQs = more scope to justify later (`scope-discipline`). Quality over quantity.

## Formalisation (SPARQL templates)
- For each CQ, write the **query shape** that will answer it once the ontology exists — the variables,
  the class/property placeholders, the expected result form. Mark placeholders that the modeling-agent
  must supply.
- These templates **are** the evaluation: `/eval` runs them for CQ-coverage. Write them now so the test
  is fixed before the model exists.

## ORSD
Assemble `output/ORSD.md`: purpose · scope · proposed language/OWL profile · intended users & uses · the
CQ set (with themes + templates) · a starter glossary of terms lifted from the input.

## Gate H1
Present the short summary; iterate on the human's add/cut/refine until they accept. The frozen CQ-set is
the contract for everything downstream. Nothing is modeled before acceptance.
