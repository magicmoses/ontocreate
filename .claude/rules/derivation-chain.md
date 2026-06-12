# Rule: the derivation chain (the backbone)

Every artifact exists because of the link before it. Never skip a link.

```
Motivating Scenario  →  Competency Question  →  Ontology  →  Evaluation
   (narrative)            (specific, testable)    (classes/props      (each CQ → a SPARQL query;
                                                   that answer CQs)    % answerable = headline metric)
```

- **Scenarios justify** the ontology. A class with no scenario behind it is unmotivated.
- **CQs are extracted from scenarios.** A CQ with no scenario is suspect — drop it or add the scenario.
- **The ontology exists to make the CQs answerable.** Every class/property traces to a CQ
  (`scope-discipline`). No CQ → out of scope.
- **The CQs ARE the evaluation.** Each CQ becomes a SPARQL query; CQ-coverage is the headline quality
  metric — but it is **reported, never optimised toward** (Goodhart; `memory-policy.md`).

## The circularity caveat (Limitation 1)
The chain is partly circular: the CQs are both the specification and the test. So an ontology can be
**coherently wrong** and still pass. That is why:
- the human gates (H1, H3, H4) are the real semantic check, and
- **OntoClean** is in the scorecard as the one **non-circular** signal.
External correctness stays a human/expert judgment — the framework is honest about this, it does not
paper over it with more internal metrics.
