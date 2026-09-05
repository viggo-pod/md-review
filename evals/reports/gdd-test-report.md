# MD Review Report

## Basic Info

- **Document**: evals/docs/gdd-test.md | **Scenario**: GDD | **Size**: 103 lines / 291 words / ~353 tokens
- **Overall**: 74.0/100 | **Risk**: Medium

## Executive Summary

A platformer GDD with a clear core loop and concrete milestone-style acceptance criteria, but blocking numeric defects: the worked damage example computes 10−5 as 4, movement speed switches units from m/s (5 m/s) to px/s (300 px/s) without conversion, and the stardust key — required to unlock level 3-1 — has no defined acquisition method, locking progression. Death/failure rules are absent even though the monetization section sells revives. Overall 74.0/100 with 4 P0s — must fix before re-review.

## Bug-Level Issues (P0, may break downstream implementation)

| # | Type | Location | Description | Fix | Impact |
|---|---|---|---|---|---|
| 1 | 🔴 Formula error | L37–39 | Worked example: 攻击力 10 − 防御力 5 stated as 实际伤害 4 点 (should be 5); no clamp for 防御 ≥ 攻击 (negative damage undefined) | Fix to 5 and define max(0, atk−def) | Combat math implemented wrong |
| 2 | 🔴 Unit mismatch | L30 vs L47 | Move speed defined as 5 m/s but later levels use 300 px/s — no conversion given | Pick one unit (e.g. px/s) and convert | Movement tuning impossible to reconcile |
| 3 | 🔴 Unimplementable rule | L63–64 | 星尘钥匙 unlocks 3-1 (3 keys required) but no acquisition method is defined anywhere | Define how keys drop/are earned | Progression to 3-1 is blocked |
| 4 | 🔴 Missing edge rules | L32, L92 | 生命值 3 点 with no death/HP=0 rule; 广告复活 implies a failure state whose determination is undefined | Define death/fail/retry behavior | Core fail loop unimplementable |

## Missing Scenario Content (gdd required items)

| # | Missing item | Note | Suggestion |
|---|---|---|---|
| 1 | Player Fantasy | §1 describes mechanics and audience, not the intended player experience/feeling | Add a one-paragraph fantasy statement |
| 2 | Numerical Design: 暴击倍率 | "由关卡难度决定" — no per-difficulty values | Add a difficulty→multiplier table |
| 3 | Numerical Design: 星尘钥匙获取 | Acquisition undefined (see P0 #3) | Define drop sources |
| 4 | Edge Cases: Death/Respawn | HP=0 behavior, respawn state undefined | Define per the Edge-Case checklist |
| 5 | Edge Cases: Fail/retry base rules | Only the ad-revival add-on exists; the base retry behavior is undefined | Define base fail/retry first |
| 6 | Edge Cases: Extreme values | Negative-damage clamp, overflow caps for stardust counters absent | Add clamps/caps to the formulas |
| 7 | Inter-system Dependencies | Economy ↔ levels ↔ items dependencies are implied but never declared bidirectionally | Add a dependency declaration section |
| 8 | Economy System (star-dust packs) | 礼包 6/30/68 元 sold but stardust amounts per pack undefined — earn-vs-buy exchange undefined | Define pack contents and the exchange rate |

## Issue Summary

| # | Level | Dimension | Location | Description | Suggestion | Impact |
|---|---|---|---|---|---|---|
| 1 | 🔴 Error | Logic | L37–39 | 10−5=4 arithmetic error; no negative-damage clamp | Fix example; add clamp | Combat implementation wrong |
| 2 | 🔴 Error | Logic | L30/L47 | m/s vs px/s unit mismatch | Unify units | Movement design irreconcilable |
| 3 | 🔴 Error | Logic | L63–64 | 星尘钥匙 acquisition undefined while gating 3-1 | Define acquisition | Progression blocked |
| 4 | 🔴 Error | Logic | L32/L92 | Death/failure rules missing; ad-revival implies an undefined failure state | Define the fail loop | Core loop unimplementable |
| 5 | 🟡 Warning | Logic | L43 | 暴击倍率 "由关卡难度决定" with no values; crit applied to incoming damage is conceptually undefined | Add a value table and clarify the crit subject | Combat feel unpredictable |
| 6 | 🟡 Warning | Logic | L76 vs L70 | Magnet obtainable via 1-2 全星 reward AND purchasable for 50 星尘 — exclusivity/pricing intent unclear | State whether channels are exclusive | Economy balance ambiguity |
| 7 | 🟡 Warning | Sections | L13, L63 | 连击倍率、星尘钥匙 used but not defined in the glossary/数值设计 | Define terms | Reader ambiguity |
| 8 | 🟡 Warning | References | L102–103 | docs/balance-table.md and docs/level-details.md do not exist in the repository | Create or fix the links | Broken configuration reference |
| 9 | 🟢 Suggestion | Scenario | L86 | 好友排行 "通关总分" computation undefined | Define the score formula | Leaderboard ambiguity |
| 10 | 🟢 Suggestion | Logic | L33 | 无敌时间 1 秒 — trigger condition (post-hit?) undefined | State the trigger | Feel/implementation detail |

Levels: 🔴 Error (must fix) / 🟡 Warning (should fix) / 🟢 Suggestion (optional)

## Dimension Scores

| Dimension | Weight | Score | Weighted | Issues | Severe |
|---|---|---|---|---|---|
| 1. Logic | 30% | 57.1 | 17.1 | 4 | 4 (bug-level) |
| 2. Scenario completeness | 25% | 65.5 | 16.4 | 8 | 0 |
| 3. Sections | 15% | 83.3 | 12.5 | 1 | 0 |
| 4. References | 10% | 80.0 | 8.0 | 1 | 0 |
| 5. Redundancy | 10% | 100 | 10.0 | 0 | 0 |
| 6. Format | 10% | 100 | 10.0 | 0 | 0 |
| **Overall** | 100% | - | **74.0** | **14** | **4** |

> Count basis: Logic 4/7 rules clean (rules 3, 7, 8 triggered; rules 4 and 6 N/A); Scenario completeness 19/29 items (Core Design 3/4, Systems and Mechanics 6/12 — Numerical Design counted per occurrence with 暴击倍率/星尘钥匙 categories unmet and 3 of 4 Edge-Case sub-items unmet — Content Scope 2/3, Experience and Quality 2/4, 5W1H 6/6; Concurrent-conflicts sub-item N/A for a single-player game); Sections 5/6 (undefined term 星尘钥匙); References 4/5 (broken links; anchor/image rules N/A); Redundancy 11/11 applicable rules clean (English-phrase rules N/A for a Chinese document); Format 4/4.

## Top 5 Issues

1. Damage example 10−5=4 and no negative-damage clamp.
2. Movement speed unit mismatch (5 m/s vs 300 px/s).
3. 星尘钥匙 gates level 3-1 but has no acquisition method.
4. Death/failure rules missing while monetization sells revives.
5. Star-dust packs (6/30/68 元) have undefined stardust contents.

## Detailed Issue List

1. **[🔴 Logic / formula error]** L37–39 — 10−5 stated as 4; missing clamp for atk ≤ def. Rule 3.
2. **[🔴 Logic / unit inconsistency]** L30 (5 m/s) vs L47 (300 px/s). Rule 3.
3. **[🔴 Logic / unimplementable rule]** L63–64 — key acquisition undefined; 3-1 requires 3 keys. Rule 8; the term is also undefined (Sections rule 4).
4. **[🔴 Logic / missing edge rules]** L32 + L92 — no HP=0/death/respawn determination; the ad-revival references an undefined failure state. Edge-Case sub-items.
5. **[🟡 Logic / vague statement]** L43 — crit multiplier "由关卡难度决定" without values; crit subject undefined. Rule 7.
6. **[🟡 Logic / vague statement]** L76 vs L70 — magnet dual-acquisition exclusivity unclear. Rule 7.
7. **[🟡 Sections / undefined term]** 星尘钥匙 (L63), 连击倍率 (L13) not defined. Rule 4.
8. **[🟡 References / broken link]** docs/balance-table.md, docs/level-details.md do not exist. Rule 1.
9. **[🟢 Scenario / acceptance]** 好友排行 total-score formula undefined.
10. **[🟢 Logic / boundary]** 无敌时间 1 秒 trigger condition unstated.

### Not flagged (precision)

- 可用性-style claims: none present — N/A.
- Internal consistency that holds: stardust prices (50/80/120) are ordered and coherent with earn rates implied by 关卡星尘目标 (100–350) — no contradiction flagged.
- The two appendix links use descriptive anchor text — link-text rules not triggered.

## Fix Priority

**P0 (bug-level / scenario gaps, must fix)**: issues 1–4 | **P1 (strongly recommended)**: issues 5–8 | **P2 (optional)**: issues 9–10

## Highlights (optional)

- The core loop (collect → buy → clear harder levels) is stated crisply with a per-mechanic table.
- Acceptance criteria (§9) are quantified (2–5 min clear time, 60/30 FPS) — testable as written.

## Auto-Fix Summary (--format fix)

- Fixed: 0 | Could not auto-fix: 0 (report produced without `--format fix`)

---

MD-REVIEW-SUMMARY
File: evals/docs/gdd-test.md | P0 bugs: 4 | Scenario gaps: 8 | Fixable: 10 | Generated: 2026-09-05T13:35:00Z
