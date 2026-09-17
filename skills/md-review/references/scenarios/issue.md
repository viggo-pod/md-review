# ISSUE Scenario Checklist — GitHub Issue Draft

Enabled when the scenario parameter is `issue`. Checks whether the GitHub issue draft (work ticket / open clarification / lightweight decision entry / defect report — one issue carries one declared sub-form) contains the following content and assesses its completeness. Sub-form sections apply only when the issue uses that form; the other sub-form sections are N/A (justified in the report).

## Core Questions (editors must address)
1. Can a maintainer triage the issue without asking follow-ups (type, state, and expected outcome explicit)?
2. Is the body self-contained (problem statement, reproduction or decision context, expected vs. actual)?
3. Is the lifecycle traceable and closable (labels/assignee/milestone, Fixes #N linkage, decidable closure criteria)?

## Key Focus
Ticket-state semantics + self-contained body + traceability & closure criteria

## Required Content — count-based scoring: each applicable item adds 1 to the denominator, a satisfied item adds 1 to the numerator, a missing or under-specified item is unmet, and N/A items (justified in the report) are excluded from both.

### Ticket Skeleton (all sub-forms)
- [ ] **Title**: Is the title a one-line summary that distinguishes this issue from any other?
- [ ] **Number & State**: Are the issue number and state (open/closed) marked, with the close reason (completed / not planned / duplicated) when closed?
- [ ] **Sub-form Declared**: Is the form declared (work ticket / clarification / decision entry / defect report)?
- [ ] **Labels / Assignee / Milestone**: Are labels, assignee, and milestone stated (or explicitly deferred) so the issue is traceable to a plan?
- [ ] **Environment / Scope Context**: Are version, platform, or scope context stated where applicable?

### Work Ticket Form (when the issue is a work ticket)
- [ ] **Task Statement**: Is the work to be done described (goal and scope boundaries)?
- [ ] **Acceptance Criteria**: Are the completion conditions verifiable (checklist or measurable outcomes)?
- [ ] **Dependencies**: Are blocking issues or prerequisites linked (#N)?

### Clarification Form (when the issue is an open question)
- [ ] **Question Statement**: Is the unclear point formulated as an answerable question?
- [ ] **Blocking Impact**: Is what stays blocked until the clarification lands stated?
- [ ] **Candidate Answers**: Are candidate answers or options listed where applicable?

### Decision Entry Form (when the issue records a decision — lightweight-ADR style)
- [ ] **Decision & Rationale**: Is the decision stated with its trade-off rationale?
- [ ] **Alternatives Considered**: Are rejected options recorded with rejection reasons?
- [ ] **Consequences / Impact Scope**: Are affected modules and follow-ups stated?

### Defect Report Form (when the issue is a bug report)
- [ ] **Reproduction Steps**: Are the steps minimal, ordered, and complete?
- [ ] **Expected vs. Actual**: Are expected and actual behavior both stated?
- [ ] **Severity / Impact**: Is the blast radius stated (who is affected, how badly)?

### Traceability & Closure (all sub-forms)
- [ ] **Linked Artifacts**: Are related PRs, commits, or discussions linked (Fixes #N / Refs #N)?
- [ ] **Closure Criteria**: Is "when can this be closed" decidable (acceptance met / question answered / decision recorded / fix verified)?

## Completeness Issue Markers
- No reproduction evidence or decision context (maintainers must ask follow-ups before triage)
- State/labels/milestone absent (the issue cannot be tracked to a plan)
- "Fixes #N" linkage missing while the body claims the problem is resolved
- Closure criteria missing (the issue can never be verifiably closed)
