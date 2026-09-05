# MD Review Report

## Basic Info

- **Document**: evals/docs/numbering-break.md | **Scenario**: Generic | **Size**: 43 lines / 137 words / ~221 tokens
- Overall: 89.2/100 | Risk: Medium

## Executive Summary

This production deployment runbook is terse, action-first, and free of redundancy, broken references, and sensitive information — but it contains one bug-level defect: the deploy sequence itself is numbered 1, 2, 4, 5, so step 3 is missing from the exact procedure an operator follows under pressure. A second, warning-level numbering error duplicates "2" in the rollback procedure (1, 2, 2, 3), which is where unambiguous step references matter most. The document also opens with no overview, leaving purpose and scope unstated. Fix the P0 deploy-sequence gap before this runbook is used for a production deployment; the other two fixes are quick.

## Bug-Level Issues (P0, may break downstream implementation)

| # | Type | Location | Description | Fix | Impact |
|---|---|---|---|---|---|
| 1 | 🔴 Broken flow (missing step) | lines 7-10 (§1 Deploy Sequence) | Ordered procedure numbered 1, 2, 4, 5 — step 3 is missing; the gap hides a deleted or forgotten deploy step | Recover the missing step 3 (between "Build the application bundle" and "Run database migrations"), renumber sequentially, and confirm the intended step with the process owner | Operator executes the production deploy without a silently dropped step |

## Issue Summary

| # | Level | Dimension | Location | Description | Suggestion | Impact |
|---|---|---|---|---|---|---|
| 1 | 🔴 Error | Logic | lines 7-10 (§1 Deploy Sequence) | Deploy sequence numbered 1, 2, 4, 5 — step 3 missing (broken/missing step in a semantic deploy procedure, per format-rules.md cross-report rule) | Recover the missing step and renumber 1-5 | Production deploy runs with a step silently omitted |
| 2 | 🟡 Warning | Format | lines 16-19 (§2 Rollback Procedure) | Rollback list numbered 1, 2, 2, 3 — duplicate number "2" in the source | Renumber to 1, 2, 3, 4 | Ambiguous step references during an incident rollback |
| 3 | 🟢 Suggestion | Sections | after line 1 (before §1) | No overview paragraph after the title — document purpose and scope unstated | Add 1-2 sentences stating which service/environment this covers and when to use it | Reader cannot confirm the runbook matches their system before executing it |

Levels: 🔴 Error (must fix) / 🟡 Warning (should fix) / 🟢 Suggestion (optional)

## Dimension Scores

| Dimension | Weight | Score | Weighted | Issues | Severe |
|---|---|---|---|---|---|
| 1. Logic | 30% | 83.3 | 25.0 | 1 | 1 (bug-level) |
| 2. Scenario completeness | 25% | 100 | 25.0 | 0 | 0 |
| 3. Sections | 15% | 83.3 | 12.5 | 1 | 0 |
| 4. References | 10% | 100 | 10.0 | 0 | 0 |
| 5. Redundancy | 10% | 100 | 10.0 | 0 | 0 |
| 6. Format | 10% | 66.7 | 6.7 | 1 | 0 |
| **Overall** | 100% | - | **89.2** | **3** | **1** |

> Generic mode: the "2. Scenario completeness" row is kept at Score 100 / Weighted 25.0 (non-applicable in generic mode, scored 100, consistent with `score.py`).

Count basis (rule-index ratios, N/A rules excluded):

- **Logic 5/6 = 83.3** — rule 1 "Self-contradictory statements" triggered: the sequence promises "these steps in order" while its own numbering shows step 3 missing (reported here as a broken/missing step per format-rules.md). Rules 4/5/6 (logical fallacy / unsourced assertion / unconsidered rebuttal) are N/A — the document contains no argumentation or evidence-bearing claims.
- **Sections 5/6 = 83.3** — rule 1 "Missing overview" triggered; no incomplete markers, undefined key terms, missing required sections, or missing ending.
- **References 100** — the document contains no links, images, or cross-references (0 applicable rules → scored 100 per SKILL.md).
- **Redundancy 100** — no rule triggered (no filler, hedges, echo headings, or padding).
- **Format 2/3 = 66.7** — rule 3 "Step-numbering break" triggered (occurrence count 2: one gap, one duplicate); rules 1-2 met (no heading-level skip, single H1); rule 4 N/A (no links).

## Top 5 Issues

1. 🔴 The deploy sequence (lines 7-10) is numbered 1, 2, 4, 5 — step 3 is missing from the core production procedure; recover the forgotten step and renumber.
2. 🟡 The rollback procedure (lines 16-19) contains a duplicate number: 1, 2, 2, 3 — renumber to 1, 2, 3, 4 so incident-time step references are unambiguous.
3. 🟢 The document has no overview after the title — add 1-2 sentences on purpose and scope.

## Detailed Issue List

### 1. Deploy sequence skips step 3 (P0, Logic + Format)

- **Location**: lines 7-10, §1 Deploy Sequence
- **Evidence**: `1. Back up the database / 2. Build the application bundle / 4. Run database migrations / 5. Restart the application` — literal sequence: 1, 2, 4, 5
- **Level**: 🔴 Error | **Dimension**: Logic (also Format rule 3, gap)
- **Description**: The intro asserts "The deployment follows these steps in order", but the ordered list jumps from 2 to 4. Per format-rules.md, a step-numbering gap in a semantic procedure (build/deploy steps) is additionally a Logic finding: the gap often hides a deleted or forgotten step, and here the procedure is the document's core deployment flow.
- **Fix**: Identify the missing step 3 (contextually, something between the bundle build and the database migrations — e.g., tag/release or staging promotion), restore it, and renumber 1-5.
- **Impact**: An operator following the runbook executes a deploy with a step silently dropped; the self-contradiction between the "in order" claim and the broken sequence also undermines trust in the rest of the runbook.

### 2. Duplicate number in rollback procedure (Format)

- **Location**: lines 16-19, §2 Rollback Procedure
- **Evidence**: `1. Restore the database backup / 2. Restore the previous application bundle / 2. Verify the application health endpoint / 3. Notify the operations team` — literal sequence: 1, 2, 2, 3
- **Level**: 🟡 Warning | **Dimension**: Format (rule 3, duplicate)
- **Description**: Two consecutive items share the number 2 — a numbering error in the source. Unlike the gap above, format-rules.md assigns duplicates to Format only (they signal a numbering typo rather than a deleted step). Rendered output renumbers automatically, but the source numbers are what gets quoted when steps are referenced ("do step 2 again").
- **Fix**: Renumber to 1, 2, 3, 4.
- **Impact**: During a failed-deployment rollback, verbal/written step references become ambiguous exactly when coordination matters most.

### 3. Missing overview (Sections)

- **Location**: after line 1 — the document goes straight from the H1 title to "## 1. Deploy Sequence"
- **Level**: 🟢 Suggestion | **Dimension**: Sections (rule 1)
- **Description**: No paragraph states the document's purpose and scope: which system or service this deploys, which environment, and when the runbook applies. The first 1-3 paragraphs should establish this before the first procedure.
- **Fix**: Add 1-2 sentences after the title, e.g. scope (service, environment), intended executor, and prerequisites pointer. Related, not scored: §3 Pre-Deployment Checklist logically belongs before §1 Deploy Sequence — moving it first would match execution order.
- **Impact**: A reader cannot verify the runbook matches their service/environment before running production commands.

### Not flagged (precision)

Per format-rules.md "Do NOT flag (precision)" guidance, the following were explicitly **"Not flagged"**:

- **Sequential lists were "Not flagged"**: the ordered lists in §3 Pre-Deployment Checklist (1, 2, 3) and §5 Post-Deployment Verification (1, 2, 3) each legitimately restart at 1 after a reset boundary (a heading), which is valid; no other ordered list in the document breaks its sequence.
- **Identifier-style IDs were "Not flagged"**: the task identifiers in §4 Change Management Tasks (T-101, T-102, T-104) are dash-prefixed identifier-style numbers (T-1, TC-1, REQ-001 class), not an ordered list — the absence of T-103 from an ID scheme is not a step-numbering break and was not flagged.

## Fix Priority

**P0 (bug-level, must fix)**: #1 — restore the missing step 3 in §1 Deploy Sequence and renumber (confirm the intended step with the process owner). | **P1 (strongly recommended)**: #2 — renumber the rollback procedure to 1, 2, 3, 4. | **P2 (optional)**: #3 — add a purpose/scope overview and consider moving §3 Pre-Deployment Checklist before §1.

## Highlights (optional)

- Action-first, zero-padding runbook style — every section does exactly one job; nothing to cut.
- Verification criteria are concrete and testable (HTTP 200, error rate below 0.5%).
- Clean hygiene: single H1 with no heading skips, no incomplete markers, no links to break, no redundancy, no sensitive information.
- Task IDs (T-1xx) give change-management items stable, citable handles.

## Auto-Fix Summary (--format fix)

- Fixed: 0 | Could not auto-fix: 0 (review ran with full format — `--format fix` was not requested; renumbering the two sequences and writing the overview require human judgment)

---

MD-REVIEW-SUMMARY
File: evals/docs/numbering-break.md | P0 bugs: 1 | Scenario gaps: 0 | Fixable: 3 | Generated: 2026-09-05 12:00 UTC
