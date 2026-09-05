# MD Review Report

## Basic Info

- **Document**: evals/docs/api-test.md | **Scenario**: API | **Size**: 179 lines / 352 words / ~599 tokens
- **Overall**: 80.3/100 | **Risk**: Medium

## Executive Summary

An API reference whose numeric contracts contradict themselves in several places: the rate limit (200/min × 60 = 12,000 ≠ 6,000/h), a P99 latency (0.5 ms) smaller than the average (200 ms), and a signature-failure code (400 AUTH_FAILED) that conflicts with the error-code table (401). Endpoint 4.3 breaks the documented response envelope, and the authentication method is delegated to a nonexistent document. Four blocking (P0) issues; overall 80.3/100 — fix P0s before publishing.

## Bug-Level Issues (P0, may break downstream implementation)

| # | Type | Location | Description | Fix | Impact |
|---|---|---|---|---|---|
| 1 | 🔴 Number contradiction | L142–143 | Rate limit 200/min vs hourly cap 6,000/h (200×60 = 12,000) | Align both to one limit (e.g. 100/min & 6,000/h) | Clients throttle at the wrong rate and get unexpected 429s |
| 2 | 🔴 Number contradiction | L144–145 | P99 response time 0.5 ms is smaller than the 200 ms average — statistically impossible | Correct P99 (e.g. 500 ms) | Capacity planning and client timeouts built on impossible data |
| 3 | 🔴 Interface inconsistency | L49 vs L37 | Signature failure returns "400 AUTH_FAILED", but the table maps AUTH_FAILED to 401 (400 = INVALID_PARAM) | Use 401 AUTH_FAILED at L49 | Integrators branch on the wrong error code |
| 4 | 🔴 Interface inconsistency | L112–118 | Refund response (4.3) uses `{"status", "result"}` and a `state` field, violating the global envelope `{"code", "message", "data"}` (§2.2); 4.4 uses `status` for the same concept | Wrap 4.3 in the envelope and unify `state` → `status` | Parsers written against §2.2 crash on refund responses |

## Missing Scenario Content (api required items)

| # | Missing item | Note | Suggestion |
|---|---|---|---|
| 1 | Basic Information (auth method unclear) | §2.3 delegates the signature algorithm to docs/auth.md, which does not exist in the repo | Inline the auth method (API Key / OAuth2 / JWT / signature) or fix the link |
| 2 | Versioning Strategy | No version-management section (v2.3 appears only in the header) | Add a Versioning section (URL vs header versioning, deprecation policy) |
| 3 | Idempotency | Write operations (create charge/refund) define no idempotency behavior | Add an Idempotency section (Idempotency-Key header, replay semantics) |
| 4 | Authorization | Only authentication is (partially) covered; no roles/scopes/permission model | Add an Authorization subsection |
| 5 | Transport Security | No HTTPS/TLS requirement stated for API calls or the notify_url | State that all calls and callbacks must use HTTPS |
| 6 | Test Cases | §7.2 points to a sandbox only; no input → expected output/status-code cases | Add test cases for key endpoints |
| 7 | Change Log | v2.3 with no version history | Add a Change Log section |
| 8 | Deprecation Strategy | No deprecation handling described | Add a deprecation policy |
| 9 | Boundary conditions (4.1) | amount/order_no have no ranges or length limits (clean counterpart states 1..100000000, 1..64) | State validation ranges per parameter |

## Issue Summary

| # | Level | Dimension | Location | Description | Suggestion | Impact |
|---|---|---|---|---|---|---|
| 1 | 🔴 Error | Logic | L142–143 | Rate-limit numbers contradict | Align limits | Unexpected 429s |
| 2 | 🔴 Error | Logic | L144–145 | P99 (0.5ms) < average (200ms) | Correct P99 | Wrong capacity assumptions |
| 3 | 🔴 Error | Logic | L49 vs L37 | AUTH_FAILED mapped to 400 and 401 in different sections | Use 401 | Broken error handling |
| 4 | 🔴 Error | Logic | L112–118 | Refund response violates the global envelope; `state` vs `status` | Use the envelope; unify field name | Client parser crashes |
| 5 | 🟡 Warning | Logic | §6 vs 附录 | Notification example carries no signature field while the appendix advertises callback signature verification | Add the signature field or explain verification | Unverifiable callbacks |
| 6 | 🟡 Warning | Scenario | L29 | Authentication method delegated to a broken link (docs/auth.md) | Inline or repair | Integrators cannot authenticate |
| 7 | 🟡 Warning | Scenario | §5 | No idempotency, versioning, deprecation, transport-security, or test-case sections (5 missing items) | Add sections | Operational gaps |
| 8 | 🟡 Warning | References | L29, L171 | docs/auth.md and docs/signature.md do not exist | Create or fix the links | Dead documentation path |
| 9 | 🟢 Suggestion | Format | L175 | The appendix HTTP example uses a bare code fence — mark it as `http` | Add language tag | Consistent highlighting |

Levels: 🔴 Error (must fix) / 🟡 Warning (should fix) / 🟢 Suggestion (optional)

## Dimension Scores

| Dimension | Weight | Score | Weighted | Issues | Severe |
|---|---|---|---|---|---|
| 1. Logic | 30% | 57.1 | 17.1 | 3 | 3 (bug-level) |
| 2. Scenario completeness | 25% | 79.5 | 19.9 | 9 | 0 |
| 3. Sections | 15% | 100 | 15.0 | 0 | 0 |
| 4. References | 10% | 83.3 | 8.3 | 1 | 0 |
| 5. Redundancy | 10% | 100 | 10.0 | 0 | 0 |
| 6. Format | 10% | 100 | 10.0 | 0 | 0 |
| **Overall** | 100% | - | **80.3** | **13** | **4** |

> Count basis: Logic 4/7 rules clean (rules 1, 2, 3 triggered; rules 4 and 6 N/A — no argumentation constructs); Scenario completeness 35/44 items (4 endpoints × 6 endpoint checks; Pagination and Sensitive-Data rules N/A); References 5/6 rules clean (rule 1 triggered; anchor/image rules N/A); Sections 6/6, Redundancy 16/16, Format 4/4.

## Top 5 Issues

1. Rate-limit contradiction (200/min vs 6,000/h) — clients cannot pick a safe call rate.
2. Impossible latency figures (P99 0.5 ms below the 200 ms average).
3. AUTH_FAILED mapped to both 400 and 401 in different sections.
4. Refund response breaks the global envelope and renames `status` to `state`.
5. Authentication method unusable — delegated to a nonexistent document.

## Detailed Issue List

1. **[🔴 Logic / data-number inconsistency]** L142–143 — 200/min and 6,000/h cannot both hold. Counted once under Rule 3 (instances: 1).
2. **[🔴 Logic / data-number inconsistency]** L144–145 — P99 must be ≥ the average; 0.5 ms vs 200 ms. Same Rule 3 item (second instance, reported as severity).
3. **[🔴 Logic / self-contradictory statement]** L49 vs L37 — "400 AUTH_FAILED" contradicts the error-code table (401 AUTH_FAILED, 400 INVALID_PARAM). Rule 1.
4. **[🔴 Logic / self-contradictory statement]** L112–118 — §2.2 promises the same envelope for every endpoint; 4.3 returns a different structure. Rule 1 (second instance). Additionally `state` (4.3) vs `status` (4.4) is a terminology inconsistency (Rule 2).
5. **[🟡 Logic / data inconsistency]** §6 — the callback example has no signature field while 附录 advertises callback signature verification. Rule 3 instance.
6. **[🟡 Scenario / auth]** §2.3 + Missing Scenario Content #1 — auth method not stated in-document. 1 unmet item.
7. **[🟡 Scenario / structure]** Missing Versioning Strategy, Idempotency, Transport Security, Test Cases, Change Log, Deprecation Strategy; boundary conditions missing for 4.1 (amount/order_no limits). 8 unmet items total (see Missing Scenario Content).
8. **[🟡 References / broken link]** docs/auth.md and docs/signature.md are referenced but do not exist in the repository. Rule 1, counted once (2 instances).

### Not flagged (precision)

- `https://sandbox.pay.example.com` and `github.com/example/pay-sdk` use IANA-reserved example domains — not flagged as real endpoints.
- `Authorization: Bearer sk_test_xxx` (L178) is a clearly-labeled test token — not flagged as credential disclosure.
- snake_case naming is consistent across fields — naming rule not triggered.

## Fix Priority

**P0 (bug-level / scenario gaps, must fix)**: issues 1–4 | **P1 (strongly recommended)**: issues 5–8 | **P2 (optional)**: issue 9

## Highlights (optional)

- Envelope-first design intent (§2.2) and a centralized error-code table are the right structure — they just need the endpoints to comply.
- State machines for charges and refunds are clearly written.

## Auto-Fix Summary (--format fix)

- Fixed: 0 | Could not auto-fix: 0 (report produced without `--format fix`)

---

MD-REVIEW-SUMMARY
File: evals/docs/api-test.md | P0 bugs: 4 | Scenario gaps: 9 | Fixable: 13 | Generated: 2026-09-05T13:05:00Z
