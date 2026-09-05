# MD Review Report

## Basic Info

- **Document**: evals/docs/clean-api.md | **Scenario**: API | **Size**: 177 lines / 645 words / ~1084 tokens
- **Overall**: 93.8/100 | **Risk**: Low

## Executive Summary

A well-built payment-gateway API reference: response envelope, error-code table, and endpoint contracts are consistent (100/min × 60 = 6,000/h holds; refund cap and state machines are coherent), and the API-scenario checklist is 39/44 items satisfied under count-based scoring. Five checklist items are unmet — two POST endpoints lack request-body examples, authorization (roles/scopes) is never defined, and test cases plus a change log are absent. No P0 bugs; publish-ready after minor polish.

## Bug-Level Issues (P0, may break downstream implementation)

| # | Type | Location | Description | Fix | Impact |
|---|---|---|---|---|---|
| — | none | — | No P0 (blocking) issues found | — | — |

## Missing Scenario Content (api required items)

| # | Missing item | Note | Suggestion |
|---|---|---|---|
| 1 | Request example (4.1 Create Charge) | Parameters are specified in a table but no copy-paste request body example is given | Add a JSON request example next to the response example |
| 2 | Request example (4.3 Create Refund) | Same table-only specification | Add a JSON request example |
| 3 | Authorization | Authentication (bearer token) is defined, but permission levels / role-based access control are never mentioned | Add an Authorization subsection listing scopes or roles per endpoint |
| 4 | Test cases | No test cases for key interfaces (input → expected output/status code) | Add a Testing section or link to the conformance suite |
| 5 | Change log | Version v2.4 is stated but no version history with breaking-change marks | Add a Change Log section |

## Issue Summary

| # | Level | Dimension | Location | Description | Suggestion | Impact |
|---|---|---|---|---|---|---|
| 1 | 🟡 Warning | Logic | L168 | Idempotency replay sentence is ambiguous: "returns the original response and code 409 only when a concurrent duplicate is detected" admits two readings (original response with 409 attached vs. 409 replacing the original response) | Split into two sentences: normal replay → original response; concurrent duplicate → 409 | Implementers may return the wrong payload on replay |
| 2 | 🟡 Warning | Scenario | §4.1/§4.3 | Missing request examples (see Missing Scenario Content #1–2) | Add JSON request examples | Integration friction |
| 3 | 🟡 Warning | Scenario | — | Missing Authorization definition (see Missing Scenario Content #3) | Define roles/scopes | Access-control design gap |
| 4 | 🟡 Warning | Scenario | — | Missing test cases and change log (see Missing Scenario Content #4–5) | Add sections | QA and upgrade planning gap |
| 5 | 🟢 Suggestion | Scenario | §3 | Error-code table lists codes and names but no fix suggestions, and per-endpoint trigger conditions are not mapped | Add a "fix suggestion" column or per-endpoint error mapping | Faster merchant troubleshooting |
| 6 | 🟢 Suggestion | Scenario | §5/§2.3 | TLS for API calls is implied (HTTPS notify_url required) but never stated for the API base | State "All API requests must use HTTPS" | Explicit transport guarantee |

Levels: 🔴 Error (must fix) / 🟡 Warning (should fix) / 🟢 Suggestion (optional)

## Dimension Scores

| Dimension | Weight | Score | Weighted | Issues | Severe |
|---|---|---|---|---|---|
| 1. Logic | 30% | 88.9 | 26.7 | 1 | 0 |
| 2. Scenario completeness | 25% | 88.6 | 22.1 | 5 | 0 |
| 3. Sections | 15% | 100 | 15.0 | 0 | 0 |
| 4. References | 10% | 100 | 10.0 | 0 | 0 |
| 5. Redundancy | 10% | 100 | 10.0 | 0 | 0 |
| 6. Format | 10% | 100 | 10.0 | 0 | 0 |
| **Overall** | 100% | - | **93.8** | **6** | **0** |

> Count basis: Logic 8/9 rules clean (Rule 7 vague-statement triggered); Scenario completeness 39/44 items (4 endpoints × 6 endpoint-definition checks; Pagination and Sensitive-Data rules N/A — no list endpoints or sensitive personal fields); Sections 6/6, References 8/8 N/A (no links/images), Redundancy 16/16, Format 4/4.

## Top 5 Issues

1. Idempotency replay sentence at L168 is ambiguous — split normal replay from concurrent-duplicate handling.
2. No request-body examples for the two POST endpoints (4.1, 4.3).
3. Authorization (roles/scopes) is undefined — only authentication is covered.
4. No test cases for key interfaces.
5. No change log for v2.4.

## Detailed Issue List

1. **[🟡 Logic / vague statement]** L168 — the replay sentence admits two readings (see Issue Summary #1). Counted as 1 unmet item of the logic Rule Index (rule 7).
2. **[🟡 Scenario / examples]** 4.1 and 4.3 — parameter tables specify the request but no request example; "each endpoint has request/response examples" is unmet for these two endpoints (2 of 24 endpoint-definition items).
3. **[🟡 Scenario / authorization]** Security section covers authentication only; no roles, scopes, or per-endpoint permissions (1 of 44 items).
4. **[🟡 Scenario / test cases]** No interface test cases (1 of 44 items).
5. **[🟡 Scenario / change log]** No version history (1 of 44 items).
6. **[🟢 Scenario / error codes]** Global table + envelope define error responses; per-endpoint triggers and fix suggestions would strengthen it (not counted — satisfied at doc level).

### Not flagged (precision)

- Rate limits are internally consistent (100/min × 60 = 6,000/h) — no contradiction flagged.
- Pagination rule: the document defines no list endpoints — N/A, not flagged.
- Sensitive-data masking rule: no sensitive personal/credential fields beyond the auth token (which is never printed in examples) — N/A, not flagged.
- External URLs use the IANA-reserved `example.com` / `pay.example.com` — placeholder-safe, not flagged.

## Fix Priority

**P0 (bug-level / scenario gaps, must fix)**: none | **P1 (strongly recommended)**: issues 1–5 | **P2 (optional)**: issue 6

## Highlights (optional)

- Internally consistent numbers throughout (rate limits, timeouts, state machines, refund caps all reconcile).
- Uniform response envelope with a single business error-code table — clean integration contract.
- Per-endpoint boundary conditions explicitly stated (amount ranges, string lengths, state transitions).

## Auto-Fix Summary (--format fix)

- Fixed: 0 | Could not auto-fix: 0 (report produced without `--format fix`)

---

MD-REVIEW-SUMMARY
File: evals/docs/clean-api.md | P0 bugs: 0 | Scenario gaps: 5 | Fixable: 6 | Generated: 2026-09-05T12:30:00Z
