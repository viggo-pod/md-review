# DECQ Scenario Checklist — Durable Decision Queue

Enabled when the scenario parameter is `decq`. Checks whether the decision queue converts an uncertain point in loop execution into a durable, human-intervenable, machine-resumable decision flow. DECQ is not an ordinary ADR or decision summary: it must describe the input before suspension, the decision state completed by the human, and the route and output after resumption.

## Core Questions (editors must address)

1. Does the document record the loop state, ambiguous question, context, and constraints that triggered the decision so the human does not have to redesign the problem?
2. Is the decision artifact persisted at a declared local path, with an explicit human editing location, state, and closure condition?
3. Does an unresolved blocking decision end the current execution instead of blocking a background process or polling, with later runs recovering from disk state?
4. Can a closed decision be read and validated by a machine and determine the next loop/BPMN route?
5. Are the resume checkpoint, inputs and outputs, dependencies, consumers, and final ADR/archive disposition recorded for traceability?

## Key Focus

Decision input + durable human handoff + machine-judgeable state + deterministic resume and routing

## Required Content — count-based scoring: each applicable item adds 1 to the denominator, a satisfied item adds 1 to the numerator, a missing or under-specified item is unmet, and N/A items (justified in the report) are excluded from both.

### Register Skeleton
- [ ] **Purpose & Parties**: Does the header state what the register decides and who does what (agent writes entries / human fills decision results)?
- [ ] **Entry IDs**: Does every entry carry a unique stable ID, with any workflow-specific ID namespace declared by the adapter?
- [ ] **Status Field**: Does every entry carry an explicit open/closed status?
- [ ] **Closure Criterion**: Is the machine-judgeable closed condition stated (decision-result field non-empty and free of placeholder residue)?
- [ ] **Durable Artifact**: Is the decision register or linked ADR path declared, writable by the human, and authoritative over chat/session state?

### Per-Entry Content (each checkbox in this section counts once per decision entry defined in the document)
- [ ] **Background**: Does each entry state which step blocked and why it is ambiguous?
- [ ] **Blocking Impact / Priority**: Is each entry marked blocking (its branch suspends until the result is filled) or defaultable (the branch proceeds with the prefilled recommendation if left unfilled)?
- [ ] **Options**: Does each entry list at least 2 options?
- [ ] **Prefilled Recommendation**: Is one option marked as recommended with a reason?
- [ ] **Decision Result Field**: Does each entry reserve an explicit field for the human decision (A / B / other: free text)?
- [ ] **Decision Artifact Link**: Does each entry link to its ADR or explain why no separate ADR is needed?
- [ ] **Dependency Declaration**: Are dependencies between entries declared where consumption order requires them?

### Handoff & Resume Protocol
- [ ] **Consumption Order**: Is the rule stated for consuming closed entries, including idempotency and any adapter-specific ordering?
- [ ] **Partial Resume Rule**: Is the rule stated when only some entries are filled, including which independent branches may continue?
- [ ] **Invalid Answer Rule**: Is an uninterpretable result (matching no option, with no "other" text) treated as still-open and re-asked, never guessed?
- [ ] **User Authority**: Is it stated that "other: ..." answers or rejected recommendations are followed as-is (decision power stays with the human)?
- [ ] **Final Disposition**: When the queue lifecycle ends, is its disposition defined (archived; architecture-relevant entries promoted to formal ADRs with the promotion cross-referenced)? An active queue may mark this item N/A with its closure trigger.
- [ ] **Resume Input/Output**: Are the resume checkpoint, state read, selected route, updated state, and produced downstream artifacts explicit?

### Relationships with Other Documents
- [ ] Are the blocked workflow steps / skills (where the decisions will be applied) referenced?
- [ ] Are promoted entries cross-referenced to their ADR numbers where applicable?
- [ ] Are workflow-specific paths, state enums, ID namespaces, and BPMN/WS-HumanTask mappings declared by an external adapter rather than silently assumed by this checklist?

## Completeness Issue Markers
- Entries without options or without a prefilled recommendation (the human must design the solution themselves)
- Status shown but no machine-judgeable closure criterion (the agent cannot decide resumability without re-asking)
- Placeholder residue left in decision-result fields ("TBD", empty template text, or any declared placeholder token)
- No consumption order or dependency rules (parallel branches cannot resume independently)
