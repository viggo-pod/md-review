# MD Review Report

## Basic Info

- **Document**: evals/docs/clean-prd.md | **Scenario**: PRD | **Mode**: solo (--format full) | **Size**: 130 lines / 588 words / ~1085 tokens
- **Review date**: 2026-09-05 | **Language of reviewed doc**: Chinese (report in English)

Overall: 90.8/100 | Risk: Low

## Executive Summary

This is a well-structured, unusually rigorous PRD for the "轻步" fitness check-in app. Its main strengths are a fully numbered requirement list (FR-1..FR-8) with priorities and dependency declarations, quantified acceptance criteria per requirement (exact ranges, latency bounds, retry counts), testable edge cases, key-flow test cases (TC-1..TC-5), and a sourced market background — every item of the PRD scenario checklist is present and properly specified (20/20). No P0 (implementation-breaking) bugs were found. The residual defects are four low-severity consistency/specification gaps: one conflicting data-deletion deadline between the NFR table and the Edge Cases section, one under-specified timeout/auto-sync recovery path, one capability claim ("desktop view-only") that is untracked in Scope/Requirements/Release Plan, and one undefined metric term ("有效打卡") in the North Star indicator. Recommendation: publish-ready after the two Warning-level wording fixes; all four issues are one-line fixes.

## Bug-Level Issues (P0, may break downstream implementation)

None found. All formula-like rules carry defined variables and safe ranges (e.g., the weekly completion rate divisor "每周运动天数目标" is bounded to 1-7 days, so division by zero cannot occur), flows are closed-loop (check-in → validation → storage → streak update → dashboard; idempotency guaranteed by the `daily_checkin(user_id, date)` unique index), and no credentials, internal addresses, or PII appear in the document.

## Missing Scenario Content (PRD required items)

None. All 20 required-content items of the PRD checklist are present and specified:

| Checklist group | Items present |
|---|---|
| Requirements definition | Background (§1, sourced data) / Target Users (§2, 3 personas) / User Stories (§3, 4 well-formed stories) / Requirements List (§4, FR-1..FR-8 with priority) |
| Functional & non-functional | Feature descriptions (§5.1) / NFRs with metrics (§5.2) / Priority P0-P2 (§4) / Dependencies (§4) |
| Scope & acceptance | In/Out-of-Scope (§6) / Acceptance criteria per FR (§7) / Edge cases (§8) / Test cases (§9, TC-1..TC-5) |
| 5W1H | Who / What / When / Where / Why / How (§14, each answered) |
| Supporting documents | Flow with exception branches (§10) / Data requirements (§11) / Release plan (§12) / Tracking metrics (§13) |

## Issue Summary

| # | Level | Dimension | Location | Description | Suggestion | Impact |
|---|---|---|---|---|---|---|
| 1 | 🟡 Warning | Logic (rule 3: data/number inconsistency) | line 56 vs line 84 | Conflicting deletion deadline: NFR says data is thoroughly deleted "账号注销后 30 天内" (within 30 days), Edge Cases say it is physically deleted only "30 天后" (after 30 days) with recovery possible during the window | Align the two — e.g., NFR: "注销后 30 天内可申诉恢复，期满后彻底删除" | A deletion job scheduled from the NFR row fires before the promised recovery window ends; compliance commitment mismatch |
| 2 | 🟡 Warning | Logic (rule 8: unimplementable rule) | line 82 | Timeout path lacks parameters: "打卡提交超时" has no timeout threshold, the "重试 3 次" has no retry interval/backoff, and the promised "稍后自动同步" has no trigger condition (next launch? network recovery?) | Specify: timeout threshold (e.g., 10 s), retry backoff, and the auto-sync trigger (e.g., "网络恢复后或下次启动时自动同步") | Implementers must invent the trigger values; staged-record treatment (streak/dashboard display while unsynced) stays ambiguous |
| 3 | 🟢 Suggestion | Logic (rule 8: unimplementable rule) | line 123 | "支持桌面端仅浏览" (desktop view-only support) is claimed in 5W1H-Where but appears in no FR, neither In-Scope nor Out-of-Scope (§6), and no release (§12) | Track it explicitly (add to Scope + assign a release + one acceptance line) or delete the clause | Scope section and 5W1H disagree on product channels; planning from §6 alone would miss it |
| 4 | 🟡 Warning | Sections (rule 4: key terms undefined) | line 116 | North Star metric uses "人均每周有效打卡天数 ≥ 4 天", but "有效打卡" is never defined; the established term elsewhere is "达标打卡" (§5.1, §7) | Define it (presumably "有效打卡 = 达标打卡") or reuse the defined term | Analytics cannot instrument the headline metric unambiguously |

Levels: 🔴 Error (must fix) / 🟡 Warning (should fix) / 🟢 Suggestion (optional)

## Dimension Scores

| Dimension | Weight | Score | Weighted | Items (satisfied/applicable) | Issues | Severe |
|---|---|---|---|---|---|---|
| 1. Logic | 30% | 77.78 | 23.3 | 7/9 (rules 3, 8 triggered) | 3 instances / 2 rules | 0 (no P0) |
| 2. Scenario completeness | 25% | 100 | 25.0 | 20/20 | 0 | 0 |
| 3. Sections | 15% | 83.33 | 12.5 | 5/6 (rule 4 triggered) | 1 | 0 |
| 4. References | 10% | 100 | 10.0 | 1/1 (rules 1-7 N/A: no links/images/anchors; rule 8 satisfied) | 0 | 0 |
| 5. Redundancy | 10% | 100 | 10.0 | 14/14 (rules 4, 5 N/A: no examples, no emoji) | 0 | 0 |
| 6. Format | 10% | 100 | 10.0 | 2/2 (rules 3, 4 N/A: no ordered lists, no links) | 0 | 0 |
| **Overall** | 100% | - | **90.8** | - | **4** | **0** |

N/A items are excluded from both numerator and denominator per the count-based rule indexes; a dimension with 0 applicable items would score 100.

## Top 5 Issues

1. [Warning] The 30-day data-deletion deadline is stated inconsistently — "deleted within 30 days" (NFR, line 56) vs "physically deleted after 30 days" (Edge Cases, line 84).
2. [Warning] The submission-timeout recovery path (line 82) lacks its timeout threshold and the trigger for the promised "稍后自动同步" behavior.
3. [Warning] The North Star metric "有效打卡" (line 116) is never defined; the document's established term is "达标打卡".
4. [Suggestion] The "desktop view-only" capability (line 123) is untracked in Scope, Requirements, and Release Plan.

## Detailed Issue List

**Issue 1 — Conflicting data-deletion deadline** 🟡 | Logic (rule 3: data/number inconsistency) | line 56 vs line 84
- Evidence: line 56 (§5.2 NFR 安全): "账号注销后 30 天内彻底删除数据"; line 84 (§8 边界与异常): "账号注销：注销后立即停用账号；30 天内可申诉恢复，30 天后数据物理删除。"
- Description: The same parameter (post-cancellation deletion deadline) has different values: the NFR commits to thorough deletion within 30 days, while the edge-case flow keeps data restorable during the 30-day window and physically deletes only after day 30. "内" (within) and "后" (after) cannot both hold.
- Fix: Reword the NFR row to "账号注销后 30 天内可申诉恢复，期满后彻底删除数据" (or move deletion to exactly day 30 in the edge case).
- Impact: Low. A scheduled deletion job built from the NFR row would destroy data inside the promised recovery window; the two statements also disagree as compliance commitments.

**Issue 2 — Timeout/auto-sync path under-specified** 🟡 | Logic (rule 8: unimplementable rule) | line 82
- Evidence: line 82 (§8): "服务器超时：打卡提交超时 → 本地暂存并重试 3 次，重试仍失败则提示'稍后自动同步'。"
- Description: The mechanism is deliberately detailed (staging, retry count 3, user message) but lacks a judgment standard at its edges: no timeout duration defines when "超时" fires, no retry interval/backoff is given, and the promised "稍后自动同步" (auto-sync later) has no trigger condition (network recovery? next launch?). The rule-file timeout check requires timeout duration, retry count, and backoff strategy — only the retry count is present.
- Fix: Add the missing parameters, e.g., "超时 10 秒 → 本地暂存，按 5s/15s/60s 重试 3 次，仍失败则提示'稍后自动同步'（网络恢复或下次启动时自动同步，同步成功后刷新看板）".
- Impact: Low. Implementers must invent the trigger values; the behavior of staged-but-unsynced records (does the record show in "今日" view, does the streak update locally) also remains open.

**Issue 3 — Untracked "desktop view-only" capability** 🟢 | Logic (rule 8: unimplementable rule) | line 123
- Evidence: line 123 (§14 Where): "手机 App（iOS/Android），支持桌面端仅浏览。"
- Description: A product-channel capability is claimed in the 5W1H answer but exists nowhere else: not in In-Scope/Out-of-Scope (§6), not in the FR list (§4), not in any release (§12), with no acceptance criterion (§7). As stated it has no implementable definition (what platform/mechanism, what content, which release).
- Fix: Either track it (add to Scope, assign a release, add one acceptance line) or delete the clause from the Where answer.
- Impact: Low. A plan built from §6 alone would omit it; a plan built from §14 would include an unspecified feature.

**Issue 4 — North Star metric term undefined** 🟡 | Sections (rule 4: key terms undefined) | line 116
- Evidence: line 116 (§13): "北极星指标：人均每周有效打卡天数 ≥ 4 天。"
- Description: "有效打卡" (valid check-in) appears only here and is never defined. The document's established, precisely defined term is "达标打卡" (§5.1 达标判定; §7 FR-3). If the two are the same concept, the naming is inconsistent; if not, the difference is unspecified — either way the headline metric cannot be unambiguously instrumented.
- Fix: Define at first use, e.g., "有效打卡（即达标打卡）", or reuse "达标打卡天数".
- Impact: Low. Data/analytics would have to guess what counts toward the North Star.

## Fix Priority

**P0 (bug-level / scenario gaps, must fix)**: none.
**P1 (strongly recommended)**: Issue 1 (unify the deletion deadline), Issue 2 (specify timeout threshold, retry backoff, auto-sync trigger), Issue 4 (define "有效打卡").
**P2 (optional)**: Issue 3 (track or drop the desktop view-only clause).

## Highlights

- Count-based discipline is excellent: every FR has an ID, priority, and individually testable acceptance criteria with concrete values (1-180 min, 3 make-ups/month, 7-day window, 1-7 days/week, P95 ≤ 500 ms, 99.9% availability, iOS 15+/Android 10+).
- Edge-case coverage goes beyond the usual: timezone-boundary semantics, duplicate submission with an explicit idempotency key matching the declared unique index, retry-with-staging, and account-deletion recovery window.
- Cross-section consistency is mostly airtight — the weekly completion-rate formula is textually identical in §5.1 and §7, the make-up quota (3/month) is consistent across user story, FR-6, §5.1, §7, and TC-3, and every FR cross-reference resolves.
- All market/statistical claims in §1 carry named sources, and 5W1H is answered with concrete values rather than platitudes.

## Auto-Fix Summary (--format fix)

Not applicable — review ran with the default full format; no auto-fixes were applied and no files were modified.

---

MD-REVIEW-SUMMARY
File: evals/docs/clean-prd.md | P0 bugs: 0 | Scenario gaps: 0 | Fixable: 4 | Generated: 2026-09-05 20:07
