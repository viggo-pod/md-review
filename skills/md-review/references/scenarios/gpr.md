# GPR Scenario Checklist — GitHub PR Description

Enabled when the scenario parameter is `gpr`. Checks whether the pull-request description (drafted as a local Markdown file before or while opening the PR) contains the following content and assesses its completeness. Draft/RFC-style PRs (design proposals seeking feedback) are reviewed with the same items; their open questions are covered by the Draft Open Questions item.

## Core Questions (editors must address)
1. Can a reviewer understand what changed and why without reverse-engineering the diff?
2. Is the change safe to merge (test plan, breaking changes, migration path stated)?
3. Is the change traceable (closing keywords on the driving issues, scope matching the stated intent)?

## Key Focus
Change narrative + merge-safety evidence + issue traceability

## Required Content — count-based scoring: each applicable item adds 1 to the denominator, a satisfied item adds 1 to the numerator, a missing or under-specified item is unmet, and N/A items (justified in the report) are excluded from both.

### Change Narrative
- [ ] **Summary**: Does the opening state what this PR does and why (1–3 sentences, not a title restatement)?
- [ ] **What Changed**: Is the change enumerated (files/modules/behavior) rather than "various fixes"?
- [ ] **Out of Scope**: Are intentionally excluded changes stated where applicable?

### Merge Safety
- [ ] **Test Plan**: Is how the change was verified stated (commands, cases, or why no test is needed)?
- [ ] **Breaking Changes**: Are breaking changes and their migration path explicitly marked (or "none")?
- [ ] **Rollback / Risk**: Is the failure story stated where applicable (config flips, data migrations)?
- [ ] **Evidence**: Are UI changes evidenced (before/after screenshots or output) where applicable?

### Traceability
- [ ] **Linked Issues**: Are the driving issues linked with closing keywords (Fixes #N / Closes #N)?
- [ ] **Draft Open Questions**: For a draft/RFC PR, is what feedback is wanted listed?
- [ ] **Template Checkboxes**: Are the repo's PR-template items addressed rather than left untouched?

### 5W1H Check (PR context)
- [ ] **What**: What does this PR change (feature/fix/refactor)?
- [ ] **Why**: Why is the change needed (which issue or problem drives it)?
- [ ] **Who**: Who reviews and owns it (reviewers, code owners)?
- [ ] **When**: When should it merge (milestone, release train, time-sensitive window)?
- [ ] **Where**: Which components/environments does it touch (flags, deploy notes)?
- [ ] **How**: How is it rolled out and verified (test/rollout chain)?

## Completeness Issue Markers
- Summary missing or restating the title only (intent must be reverse-engineered from the diff)
- Breaking changes unstated or buried (merge safety cannot be judged)
- "Fixes #N" absent while the change claims to resolve an issue
- Test plan is a bare "tested locally" without cases or commands
