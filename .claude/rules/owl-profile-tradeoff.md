# Rule: OWL profile tradeoff

Choose the OWL profile **deliberately, from what the CQs need — before modeling**, not when the reasoner
hangs. `preferences.md` may set a default (currently EL); the human confirms at **H2**.

| Profile | Strength | Cost | Reasoner | Pick when |
|---|---|---|---|---|
| **EL** | fast, scalable reasoning | limited expressivity | **ELK** (Java) | large/simple ontologies; good default |
| **QL** | query answering over large data (rewriting) | limited expressivity | **Ontop** (Java, OBDA) | data-access / OBDA over big sources |
| **RL** | rule-based reasoning (materialisation) | limited expressivity | **owlrl** (pure Python on rdflib; RDFox for scale) | rule/inference-driven, want in-process |
| **DL** | most expressive | reasoning can blow up (exponential) | **HermiT** (ships with owlready2, Java) | rich axioms genuinely required by the CQs |

## Discipline
- Only the **chosen profile's reasoner** is installed. EL/QL/DL reasoners need **Java**; RL (owlrl) is
  pure Python. In a credential-free, Java-free environment, RL/owlrl + rdflib is the always-available
  path — the validation-agent falls back to it honestly if a Java reasoner is absent (Limitation 5).
- The modeling-agent must not use constructs outside the chosen profile.
- Record the choice + the tradeoff rationale in entity memory at H2.
