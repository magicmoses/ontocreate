# Rule: methodology

The framework automates **Ontology Development 101** + the **NeOn** methodology. Every agent works
within this process.

## The 6 steps
1. **Determine domain + scope** (scoping-agent).
2. **Reuse** — ontologies (researcher-agent) + tooling (library-scout-agent) before building.
3. **Enumerate important terms** (modeling-agent, Step 3).
4. **Define classes + hierarchy** (modeling-agent, Step 4).
5. **Define properties** (modeling-agent, Step 5).
6. **Limit the scope** — the cardinal step, **enforced continuously**, not once (scoping-agent).

## The four guiding principles (the law)
1. An ontology is only as strong as the questions it must answer — **CQs before classes**.
2. The **derivation chain** is the backbone (`derivation-chain.md`).
3. **Reuse before build** — ontologies, libraries, ready-made MCP servers.
4. **Limit the scope** — every class/property traces to a CQ, or it's out.

## Operating discipline
- **Build → verify → correct**, with **checker ≠ builder**, **bounded to 3 correction attempts** before
  escalating to the human. Applies to both the runtime and the meta-build (`self-verification.md`).
- **NeOn scenarios** (`neon-scenarios.md`) set the workflow path; only exercised paths are proven — stop
  and escalate rather than walk an untested one (Limitation 5).
- Each phase ends at a **human gate** (`human-gates.md`); the build between gates is autonomous and
  credential-free.
