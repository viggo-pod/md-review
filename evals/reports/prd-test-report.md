# MD Review Report

## Basic Info

- **Document**: evals/docs/prd-test.md | **Scenario**: PRD | **Size**: 86 lines / 272 words / ~382 tokens
- **Overall**: 66.6/100 | **Risk**: Medium

## Executive Summary

A SaaS bookkeeping PRD with a solid skeleton (numbered requirements, milestones, glossary) but blocking logic defects: the concurrency target contradicts itself (1000 vs 5000), the worked retention example computes 600/1000 as 30%, and the refund flow auto-approves high-value refunds (over ¥500) while small ones get manual review. Acceptance criteria are unquantified ("达到目标") and partially missing, and 7 of 22 PRD checklist items are unmet. Overall 66.6/100 — must fix P0s before re-review.

## Bug-Level Issues (P0, may break downstream implementation)

| # | Type | Location | Description | Fix | Impact |
|---|---|---|---|---|---|
| 1 | 🔴 Number contradiction | L45 vs L48 | Concurrency: "1000 并发用户" vs "生产环境压测目标为 5000 并发，架构设计容量以此为准" | Declare 5000 as the requirement and delete/annotate the 1000 figure | Infrastructure sized at 1/5 of the real target |
| 2 | 🔴 Formula error | L52–53 | Worked example: 600/1000 stated as 留存率 30% — it is 60% | Fix to 60% (and define the retention window precisely) | Every team reading the example inherits the wrong formula |
| 3 | 🔴 Broken flow | L37 | 退款金额超过 500 元直接自动通过 — high-value refunds bypass human review while small ones get it | Invert the rule (manual review above a threshold, e.g. ≤500 auto) | Fraud and fund-loss exposure |

## Missing Scenario Content (prd required items)

| # | Missing item | Note | Suggestion |
|---|---|---|---|
| 1 | Dependencies between requirements | REQ-002 (自动分类) vs REQ-005 (发票 OCR) and others — no dependency declared | Add a Depends-on column or notes |
| 2 | Scope Definition | No In-Scope / Out-of-Scope boundary | Add an explicit scope table |
| 3 | Acceptance Criteria (quantified, complete) | §9 covers only REQ-001/002/005, is titled "部分", and uses "达到目标" without a value | Quantify per REQ and cover all five |
| 4 | Edge Cases / failure scenarios | Only 低置信度 → 人工确认 is handled; OCR failure, refund rejection path, payment failures absent | Add failure paths per flow |
| 5 | Test Cases | No test-case section for key flows | Add input → expected output cases |
| 6 | Flow/Sequence Diagrams | 退款流程 is prose-only | Add a diagram for the refund and classification flows |
| 7 | Data Requirements | Data fields/storage not described | Add a Data Requirements subsection |

## Issue Summary

| # | Level | Dimension | Location | Description | Suggestion | Impact |
|---|---|---|---|---|---|---|
| 1 | 🔴 Error | Logic | L45/L48 | 1000 vs 5000 并发 contradiction | Unify on 5000 | Under-provisioned infrastructure |
| 2 | 🔴 Error | Logic | L52–53 | 留存率 example 600/1000 = 30% (should be 60%) | Correct the arithmetic | Wrong analytics formula propagates |
| 3 | 🔴 Error | Logic | L37 | >¥500 refunds auto-approved | Invert the review rule | Fraud/fund-loss risk |
| 4 | 🟡 Warning | Logic | L33 | 分类置信度公式的"总关键词数"未定义范围（凭证的还是规则的），且未处理除零 | Define scope and zero-guard | Implementation ambiguity |
| 5 | 🟡 Warning | Logic | L72 | "OCR 识别准确率达到目标" 无目标值 | Quantify (e.g. ≥95%) | Untestable acceptance |
| 6 | 🟡 Warning | Scenario | §9 | 验收标准标注"部分"且仅覆盖 3/5 REQ | Complete and quantify | Release gate unreliable |
| 7 | 🟡 Warning | References | L78 | docs/launch-checklist.md 不存在 | Create the file or fix the link | Broken pre-launch checklist |
| 8 | 🟢 Suggestion | Sections | L81–86 | 术语表缺"置信度"、"并发"等正文术语 | Extend the glossary | Minor ambiguity |
| 9 | 🟢 Suggestion | Logic | L29 | VIP1/VIP2 与 VIP3 的权益差异未定义（仅 VIP3 有专属客服） | Define per-tier benefits | Tier pricing unimplementable |

Levels: 🔴 Error (must fix) / 🟡 Warning (should fix) / 🟢 Suggestion (optional)

## Dimension Scores

| Dimension | Weight | Score | Weighted | Issues | Severe |
|---|---|---|---|---|---|
| 1. Logic | 30% | 42.9 | 12.9 | 4 | 3 (bug-level) |
| 2. Scenario completeness | 25% | 68.2 | 17.0 | 7 | 0 |
| 3. Sections | 15% | 66.7 | 10.0 | 2 | 0 |
| 4. References | 10% | 66.7 | 6.7 | 1 | 0 |
| 5. Redundancy | 10% | 100 | 10.0 | 0 | 0 |
| 6. Format | 10% | 100 | 10.0 | 0 | 0 |
| **Overall** | 100% | - | **66.6** | **14** | **3** |

> Count basis: Logic 3/7 rules clean (rules 1, 3, 7, 8 triggered; rules 4 and 6 N/A — no argumentation constructs); Scenario completeness 15/22 items (7 unmet, see table above); Sections 4/6 (incomplete-marker "部分", undefined term 置信度); References 2/3 (broken link; text/URL rules applicable and clean); Redundancy 11/11 applicable rules clean (English-phrase rules N/A for a Chinese document); Format 4/4.

## Top 5 Issues

1. Concurrency requirement contradicts itself (1000 vs 5000) — capacity planning is ambiguous.
2. Retention example computes 600/1000 as 30% instead of 60%.
3. Refund auto-approval applies to high-value (>¥500) refunds — fraud exposure.
4. Acceptance criteria unquantified and incomplete ("部分", "达到目标").
5. No edge-case/failure scenarios beyond the low-confidence queue.

## Detailed Issue List

1. **[🔴 Logic / data-number inconsistency]** L45 vs L48 — concurrency 1000 vs 5000. Rule 3 (instance 1).
2. **[🔴 Logic / formula error]** L52–53 — 留存率 600/1000 stated as 30%. Rule 3 (instance 2); also poisons the formula's usage example.
3. **[🔴 Logic / broken flow]** L37 — refund auto-approval threshold inverted (high-value bypasses review). Reported as P0 per the Logic dimension's broken-flow focus; note: the count-based Rule Index has no dedicated broken-flow row — counted under P0 issue count, not as a rule-index item.
4. **[🟡 Logic / vague statement]** L33 — "总关键词数" undefined; no zero-divisor guard. Rule 7.
5. **[🟡 Logic / unimplementable rule]** L72 — "达到目标" without a value; L29 — VIP1/VIP2 benefits undefined. Rule 8.
6. **[🟡 Sections / incomplete marker]** L68 — checklist titled "（部分）" is itself an incompleteness marker. Rule 3.
7. **[🟡 Sections / key term]** 置信度 (L33) missing from the glossary. Rule 4.
8. **[🟡 References / broken link]** docs/launch-checklist.md does not exist. Rule 1.
9. **[🟢 Sections / terminology]** user story "每周经营报表推送" vs REQ-003 "报表导出" — push vs export mismatch worth clarifying.

### Not flagged (precision)

- 可用性 99.9% ↔ 每年 8.76 小时 is correct arithmetic (8760 × 0.001) — consistent, not flagged.
- Milestone dates (M1–M3) are concrete and properly ordered.
- The link text 上线检查清单 matches its target name — text/URL rule not triggered.

## Fix Priority

**P0 (bug-level / scenario gaps, must fix)**: issues 1–3 | **P1 (strongly recommended)**: issues 4–8 | **P2 (optional)**: issue 9

## Highlights (optional)

- Requirements are uniquely numbered with priorities and statuses — a traceable base to fix against.
- Glossary, milestones, and a quantified availability target (99.9% ↔ 8.76h) show good practices in the skeleton.

## Auto-Fix Summary (--format fix)

- Fixed: 0 | Could not auto-fix: 0 (report produced without `--format fix`)

---

MD-REVIEW-SUMMARY
File: evals/docs/prd-test.md | P0 bugs: 3 | Scenario gaps: 7 | Fixable: 9 | Generated: 2026-09-05T13:20:00Z
