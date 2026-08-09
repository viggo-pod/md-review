# MD Review Report

## Basic Info

- **Document**: evals/docs/clean-api.md | **Scenario**: API | **Size**: 177 lines / 645 words / ~1084 tokens
- **Overall**: 95.0/100 | **Risk**: Low

## Executive Summary

This is a genuinely clean, well-written API reference. The document is internally consistent across every dimension that matters for downstream implementation: the response envelope (`code`/`message`/`data`) is uniform across all five examples, every error code referenced in prose (401 for auth expiry, 429 for rate limits, 409 for duplicate requests) matches the Section 3 error-code table, the rate-limit arithmetic is correct (100/min x 60 = 6,000/hour), P99 (500 ms) is greater than the average (200 ms) as required, authentication is fully defined (Bearer token, 24-hour expiry, 401 on expiry), and there are zero incomplete markers and zero broken references. No P0 (bug-level) or P1 issues were found. Only a handful of P2 polish/completeness suggestions are noted — none of which would break an implementation. Recommend publish.

## Bug-Level Issues (P0, may break downstream implementation)

None found. The document contains no formula errors, number contradictions, broken flows, interface inconsistencies, or undefined terms that would break a downstream implementation.

## Missing Scenario Content (API required items)

| # | Missing item | Note | Suggestion |
|---|---|---|---|
| 1 | Change log | The doc is versioned (v2.4, "Status: Published") but has no changelog recording version changes / breaking changes. | Add a short change log table (version, date, breaking changes). Minor; optional for a reference. |
| 2 | Production base URL | Endpoints are documented as relative paths (`/v1/charges`); only the sandbox URL (`https://sandbox.pay.example.com`) is given in the Appendix. A production base URL is implied (`pay.example.com` from the pay_url example) but never stated explicitly. | State the production base URL (e.g. `https://api.pay.example.com`) in Section 2. Minor. |
| 3 | Test cases | No input → expected-output/status-code test cases for key interfaces. The API checklist requests these; typically supplied in a separate QA doc, not an API reference. | Optional: add a small test-case table for create-charge and refund boundary values. |
| 4 | Per-endpoint error responses / boundary behavior | Global error-code list exists, but each endpoint does not enumerate its specific failure codes (e.g. what a caller receives when `amount > 100000000`). | Optional: add a "Possible errors" row per endpoint. Minor. |
| 5 | JSON request-body examples | POST endpoints (Create Charge, Create Refund) define request parameters in tables but give no example JSON request body. | Optional: add one request-body example per POST endpoint. Minor. |
| 6 | Transport security for the API itself | HTTPS is required for `notify_url`, but TLS enforcement on the API surface is not stated explicitly. | One line in Section 2.1 ("All API traffic uses TLS 1.2+"). Minor. |

## Issue Summary

| # | Level | Dimension | Location | Description | Suggestion | Impact |
|---|---|---|---|---|---|---|
| 1 | 🟢 Suggestion | Scenario | Header / after Section 8 | No change log for a published, versioned API | Add changelog | Low |
| 2 | 🟢 Suggestion | Scenario | Sections 4.x, Appendix | Production base URL not stated (sandbox only) | State base URL | Low |
| 3 | 🟢 Suggestion | Scenario | Section 4 | No test cases for key interfaces | Add test-case table | Low |
| 4 | 🟢 Suggestion | Scenario | Section 4 | Per-endpoint error responses / boundary behavior not enumerated | Add per-endpoint error rows | Low |
| 5 | 🟢 Suggestion | Scenario | Sections 4.1, 4.3 | No JSON request-body examples for POST endpoints | Add request examples | Low |
| 6 | 🟢 Suggestion | Scenario | Section 2.1 | API TLS enforcement not explicit | Add one line | Low |
| 7 | 🟢 Suggestion | Logic | Section 4.2 | Charge state machine (`created → pending → paid → refunded`) has no failed/expired state, although charges carry an `expires_at` | Consider adding `expired`/`failed` states | Low |

Levels: 🔴 Error (must fix) / 🟡 Warning (should fix) / 🟢 Suggestion (optional)

## Dimension Scores

| Dimension | Weight | Score | Weighted | Issues | Severe |
|---|---|---|---|---|---|
| 1. Logic | 30% | 95 | 28.5 | 1 | 0 |
| 2. Scenario completeness | 25% | 90 | 22.5 | 6 | 0 |
| 3. Sections | 15% | 95 | 14.2 | 0 | 0 |
| 4. References | 10% | 100 | 10.0 | 0 | 0 |
| 5. Redundancy | 10% | 98 | 9.8 | 0 | 0 |
| 6. Format | 10% | 100 | 10.0 | 0 | 0 |
| **Overall** | 100% | - | **95.0** | **7** | **0** |

## Top 5 Issues

1. No change log for a published, versioned API (minor completeness gap; optional for a reference).
2. Production base URL not explicitly stated — only the sandbox URL is given.
3. No test cases for key interfaces (typically lives in a separate QA doc; optional).
4. Per-endpoint error responses / boundary behavior not enumerated (global error list exists and is consistent).
5. Charge state machine omits failed/expired states even though `expires_at` exists (enhancement, not an error).

## Detailed Issue List

1. **Location**: Header (line 3) / end of document. **Original text**: "> Version: v2.4 | Status: Published". **Level**: 🟢 Suggestion. **Dimension**: Scenario completeness. **Description**: A published, versioned API reference has no change log recording what changed per version or whether any change was breaking (Section 8 does mention a 12-month deprecation window, but no history). **Fix**: Add a small version/date/breaking-change table. **Impact**: Low — integration engineers cannot diff versions, but nothing breaks.

2. **Location**: Sections 4.x + Appendix (lines 48, 97, 174-177). **Original text**: "`POST /v1/charges`"; "Sandbox environment: https://sandbox.pay.example.com". **Level**: 🟢 Suggestion. **Dimension**: Scenario completeness. **Description**: All endpoints are relative paths; only the sandbox base URL is given. The production host is only implied by the example `pay_url`. **Fix**: State the production base URL in Section 2. **Impact**: Low — an implementer can infer it from the pay_url example.

3. **Location**: Section 4. **Level**: 🟢 Suggestion. **Dimension**: Scenario completeness. **Description**: No input → expected-output/status-code test cases. The API scenario checklist requests them. **Fix**: Add a compact test-case table (boundary amounts, invalid order_no, duplicate request). **Impact**: Low — QA testing lives elsewhere for most integration teams.

4. **Location**: Section 4 (each endpoint). **Level**: 🟢 Suggestion. **Dimension**: Scenario completeness. **Description**: Endpoints do not enumerate which specific error codes they return for invalid input / missing auth / not-found / duplicate (the global Section 3 list is correct and referenced consistently by prose). **Fix**: Add a per-endpoint "Possible errors" row. **Impact**: Low.

5. **Location**: Sections 4.1, 4.3 (lines 54-62, 103-110). **Level**: 🟢 Suggestion. **Dimension**: Scenario completeness. **Description**: POST endpoints document request parameters in tables but give no JSON request-body example. **Fix**: Add one request-body JSON block per POST endpoint. **Impact**: Low.

6. **Location**: Section 2.1 (line 13). **Level**: 🟢 Suggestion. **Dimension**: Scenario completeness. **Description**: `notify_url` is required to be HTTPS, but TLS enforcement on the API surface itself is never stated. **Fix**: One sentence ("All API traffic uses TLS"). **Impact**: Low.

7. **Location**: Section 4.2 (line 81). **Original text**: "States: `created` → `pending` → `paid` → `refunded`." **Level**: 🟢 Suggestion. **Dimension**: Logic. **Description**: The charge state machine has no failed/expired state, even though charges carry an `expires_at` and a payment can fail (card declined). This is NOT a contradiction within the document — the states listed are a correct happy-path progression. It is an enhancement suggestion, not a defect. **Fix**: Consider adding `failed`/`expired` states. **Impact**: None today; purely additive.

## Fix Priority

**P0 (bug-level / scenario gaps, must fix)**: none.
**P1 (strongly recommended)**: none.
**P2 (optional)**: items 1-7 above, all low-impact polish. If only one is picked, add the change log (item 1) and the production base URL (item 2), as those are the most reader-visible gaps.

## Highlights

- Consistent response envelope across all five examples (`code: 0`, `message`, `data`).
- Error codes in prose match the Section 3 table exactly (401 auth, 409 duplicate, 429 rate limit).
- Rate-limit arithmetic is correct: 100 req/min × 60 = 6,000 req/hour.
- P99 (500 ms) > average (200 ms) — a realistic and correct performance claim.
- Authentication fully defined: Bearer token, 24-hour expiry, 401 on expiry, cross-referenced to the error table.
- Field naming is consistent (snake_case everywhere: `charge_id`, `order_no`, `notify_url`, `paid_at`, `refund_id`).
- The 24-hour window is used consistently across token expiry, notification retry horizon, and idempotency replay window.
- No incomplete markers, no orphan headings, no heading-level skips, no broken or placeholder links (0 links in total).
- Concise prose (645 words); no filler words, hedges, echo headings, emoji, or redundant examples.

## Auto-Fix Summary (--format fix)

- Fixed: 0 | Could not auto-fix: 7 (all need judgment; none are mechanical)

```
MD-REVIEW-SUMMARY
Files: 1 reviewed, 0 critical | P0 bugs: 0 | P1: 0 | P2 suggestions: 7 | Scenario gaps: 0 | Fixable: 0 | Generated: 2026-08-08
```
