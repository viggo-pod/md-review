# DECQ Scenario Checklist — Pending Decision Register (Decision Queue)

Enabled when the scenario parameter is `decq`. Checks whether the pending-decision register (a file-based human-in-the-loop decision queue: the agent writes entries and suspends, the human fills in the decision results, the agent reads them back and resumes) contains the following content and assesses its completeness.

## Core Questions (editors must address)
1. Is the closed state machine-judgeable (decision-result field non-empty, no placeholder residue) so resuming never depends on the display status alone?
2. Does every open entry let the human decide by selection (at least 2 options with a prefilled recommendation) instead of designing the solution themselves?
3. Are consumption order and partial-resume rules explicit enough that parallel branches can proceed without re-asking?

## Key Focus
Entry-level decision fields + machine-judgeable state + async handoff resumability

## Required Content — count-based scoring: each applicable item adds 1 to the denominator, a satisfied item adds 1 to the numerator, a missing or under-specified item is unmet, and N/A items (justified in the report) are excluded from both.

### Register Skeleton
- [ ] **Purpose & Parties**: Does the header state what the register decides and who does what (agent writes entries / human fills decision results)?
- [ ] **Entry IDs**: Does every entry carry a unique stable ID (D-001, D-002...)?
- [ ] **Status Field**: Does every entry carry an explicit open/closed status?
- [ ] **Closure Criterion**: Is the machine-judgeable closed condition stated (decision-result field non-empty and free of placeholder residue such as "（人工填写）", "TBD", "待定")?

### Per-Entry Content (each checkbox in this section counts once per decision entry defined in the document)
- [ ] **Background**: Does each entry state which step blocked and why it is ambiguous?
- [ ] **Options**: Does each entry list at least 2 options?
- [ ] **Prefilled Recommendation**: Is one option marked as recommended with a reason?
- [ ] **Decision Result Field**: Does each entry reserve an explicit field for the human decision (A / B / other: free text)?
- [ ] **Dependency Declaration**: Are consumption-order dependencies between entries declared (依赖: D-001) where applicable?

### Handoff & Resume Protocol
- [ ] **Consumption Order**: Is the rule stated for consuming closed entries (ascending D-number, each consumed once — idempotent)?
- [ ] **Partial Resume Rule**: Is the rule stated when only some entries are filled (branches without dependencies continue; the unfilled list is reported back)?
- [ ] **Invalid Answer Rule**: Is an uninterpretable result (matching no option, with no "other" text) treated as still-open and re-asked, never guessed?
- [ ] **User Authority**: Is it stated that "other: ..." answers or rejected recommendations are followed as-is (decision power stays with the human)?
- [ ] **Final Disposition**: Is the register's end state defined (archived; architecture-relevant entries promoted to formal ADRs with the promotion cross-referenced)?

### Relationships with Other Documents
- [ ] Are the blocked workflow steps / skills (where the decisions will be applied) referenced?
- [ ] Are promoted entries cross-referenced to their ADR numbers where applicable?

## Completeness Issue Markers
- Entries without options or without a prefilled recommendation (the human must design the solution themselves)
- Status shown but no machine-judgeable closure criterion (the agent cannot decide resumability without re-asking)
- Placeholder residue left in decision-result fields ("待定", "TBD", unfilled template text)
- No consumption order or dependency rules (parallel branches cannot resume independently)
