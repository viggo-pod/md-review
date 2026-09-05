# MD Review Report

## Basic Info

- **Document**: evals/docs/clean-gdd.md | **Scenario**: GDD (Game Design Document) | **Size**: 185 lines / 993 words / ~1,602 tokens
- **Overall**: 91.4/100 | **Risk**: Low

## Executive Summary

This is a well-constructed Chinese-language GDD for the 2D side-view simulation game 《星港维修员》 (Starport Maintenance Chief, v1.1). Its strengths are a fully cross-consistent numeric system — every quest reward in §5.1 recomputes exactly from the §4.2 income formula, all clamp bounds are documented and reachable, tuning-knob safe ranges (§9) contain the actual values in use, and §8 acceptance criteria align with the §4.3 economy — plus an edge-case section (§6) that covers all four required boundary classes including dual-device login conflict and save rollback. Two genuine value gaps keep it from a higher score: the technician recruitment cost (a core action per §11 "What" and a listed credit sink in §4.3) is defined nowhere, and the part drop-rate for the "订单掉落" acquisition channel is undefined even though §10's margin math assumes purchase-only sourcing. Two minor logic warnings were also found: an arithmetic slip in the star-basis balance comparison (§10) and an ambiguous sentence in §5.3 that literally assigns expansion a reputation gate contradicted elsewhere. No P0 (bug-level) issues; fill the two missing values before implementation hand-off.

## Bug-Level Issues (P0, may break downstream implementation)

None found. All formulas (§4.2: duration, income, success rate) have fully defined variables, explicit clamps, and worked examples that recompute correctly; no contradictory parameter values, no circular dependencies (§5.3 declares the reputation↔unlock loop as one-way accumulating and therefore deadlock-free), and no sensitive information (credentials, internal addresses, PII) is disclosed.

## Missing Scenario Content (gdd required items)

Scenario checklist: 24 of 26 "Required Content" checkboxes satisfied. Both gaps fall under **Numerical Design** ("counted per occurrence" — each undefined key-value category is one unmet item):

| # | Missing item | Note | Suggestion |
|---|---|---|---|
| 1 | Numerical Design — technician recruitment cost | §4.3 lists 招聘 (recruit) as a credit-point sink but gives no cost (only expansion has 300/800); §5.3 states "招聘技师的信用点消耗回馈到经济系统产出" (the cost exists and feeds the economy); §11 "What" lists 招聘 as a core player action; §5.2's "技师 8 名（1-5 星各档位）" does not say how many technicians the player starts with vs. must recruit | Define the recruitment cost per technician tier and the initial roster size, in the §4.1/§4.3 tables |
| 2 | Numerical Design — part drop rate | §4.3 lists "订单掉落" (order drops) as the second part-acquisition channel with no probability or quantity; §10's margin analysis (net = reward − part cost) implicitly assumes every part is purchased, so any real drop rate changes the actual margins and the claimed 30-day simulation inputs | Define drop chance/quantity per order type (普通/精制/特殊) in §4.3 |

## Issue Summary

| # | Level | Dimension | Location | Description | Suggestion | Impact |
|---|---|---|---|---|---|---|
| 1 | 🟡 Warning | Scenario completeness | §4.3/§5.2/§5.3 (lines 78, 104, 113) | Recruitment cost undefined for a core action and economy sink | Add cost per tier + starting roster to §4.3 | Economy cannot be simulated or the recruit feature implemented as specified |
| 2 | 🟡 Warning | Scenario completeness | §4.3 (line 79) | Part drop rate/quantity undefined for the "订单掉落" channel | Define drop chance per order type in §4.3 | Drop channel unusable; §10 margins only valid if all parts purchased |
| 3 | 🟡 Warning | Logic | §10 (line 170) | Star-basis balance comparison lists 普通件 0.33/秒, but the stated basis ("含星级加成后的实际报酬") requires (30×1.1−10)/60 = 23/60 ≈ 0.38/秒; 0.33 is the base-reward-basis value carried over | Recompute as ≈0.38/秒 (ordering 0.40 > 0.39 > 0.38 and the mixed-strategy conclusion are unchanged) | Balance appendix numbers unreliable as written |
| 4 | 🟡 Warning | Logic | §5.3 (line 111) | "扩建与订单解锁均以声望为门槛" is ambiguous: read literally, expansion is reputation-gated — contradicting §4.3 (credit-only costs 300/800, no rep threshold anywhere) and §8 (a new account expands within 15 min after one Q-1, i.e. ~10 rep); the alternative reading ("the order lines that expansion unlocks are rep-gated") is consistent | Reword, e.g. "订单解锁以声望为门槛；扩建以信用点为消耗（见 4.3）；机库等级与声望互不依赖" | An implementer could add an undefined rep gate to expansion, or stall on a missing threshold |

Levels: 🔴 Error (must fix) / 🟡 Warning (should fix) / 🟢 Suggestion (optional)

## Dimension Scores

| Dimension | Weight | Score | Weighted | Issues | Severe |
|---|---|---|---|---|---|
| 1. Logic | 30% | 77.8 | 23.3 | 2 | 0 (bug-level) |
| 2. Scenario completeness | 25% | 92.3 | 23.1 | 2 | 0 |
| 3. Sections | 15% | 100 | 15.0 | 0 | 0 |
| 4. References | 10% | 100 | 10.0 | 0 | 0 |
| 5. Redundancy | 10% | 100 | 10.0 | 0 | 0 |
| 6. Format | 10% | 100 | 10.0 | 0 | 0 |
| **Overall** | 100% | - | **91.4** | **4** | **0** |

Item counts behind the ratios (N/A constructs excluded from both numerator and denominator):

- **Logic 7/9**: 9 index rules applicable; rules 3 (data/number inconsistency) and 7 (vague statement) triggered once each (Issues 3–4). Fallacy/rebuttal/assertion constructs exist (§10's strategy argument) and are satisfied; no sensitive information disclosed.
- **Scenario 24/26**: 26 "Required Content" checkboxes (4 Core Design + 5 Systems/Mechanics incl. the parent Edge Cases + 4 Edge-Case sub-items + 3 Content Scope + 4 Experience/Quality + 6 5W1H); 2 unmet (Issues 1–2). All four Edge-Case sub-checkboxes (failure determination, fail/retry, extreme values, concurrent conflicts) are satisfied by §6.
- **Sections 6/6**, **References 4/4** (rules 1/2/3/7 N/A — no internal file links, anchors, images, or heading links), **Redundancy 16/16**, **Format 3/3** (rule 3 N/A — no ordered lists).

## Top 5 Issues

1. Technician recruitment cost is undefined although 招聘 is a core player action (§11) and a listed credit sink (§4.3) — the economy cannot be completed without it.
2. The "订单掉落" part-acquisition channel has no drop rate, and §10's margin math silently assumes purchase-only sourcing.
3. §10's star-basis comparison reuses the base-basis value 0.33/秒 for 普通件 where ≈0.38/秒 is required by its own stated basis (conclusion unaffected).
4. §5.3's "扩建与订单解锁均以声望为门槛" admits two readings, one of which contradicts §4.3 and §8 — needs a one-line reword.

## Detailed Issue List

**Issue 1 — Recruitment cost undefined** (🟡, Scenario completeness)
- Location: §4.3 economy table (line 78), §5.2 (line 104), §5.3 (line 113), §11 (line 176)
- Original text: "信用点 | 交付订单、每日委托奖励 | 采购零件、扩建（1→2 级 300 / 2→3 级 800）、招聘" and "招聘技师的信用点消耗回馈到经济系统产出"
- Description: 招聘 appears as a credit sink, a dependency edge, and a core action, but no cost value and no initial-vs-recruited roster split exist anywhere in the document.
- Fix: add a recruitment cost per technician tier and the starting roster count to §4.1/§4.3.
- Impact: the recruit feature and the economy balance cannot be implemented/simulated as specified.

**Issue 2 — Part drop rate undefined** (🟡, Scenario completeness)
- Location: §4.3 parts row (line 79)
- Original text: "零件（普通/精制/特殊） | 采购（普通 10 / 精制 25 / 特殊 60 信用点）、订单掉落 | 维修消耗，失败不返还"
- Description: the drop channel has no probability or quantity; §10's per-order margins (net = reward − full part cost) hold only if every part is purchased.
- Fix: define drop chance/amount per order type in §4.3 (and note how drops interact with the §10 analysis).
- Impact: acquisition economics under-determined; 30-day simulation inputs incomplete.

**Issue 3 — §10 star-basis arithmetic slip** (🟡, Logic)
- Location: §10 Balance, first bullet (line 170)
- Original text: "按含星级加成后的实际报酬口径：特殊件（3 星 96/240 = 0.40/秒）> 精制件（2 星 47/120 ≈ 0.39/秒）> 普通件 0.33/秒（纯特殊最优）"
- Description: 特殊 96 = 120×1.3−60 and 精制 47 = 60×1.2−25 both apply the star bonus; 普通件 at 1 star should be (30×1.1−10)/60 = 23/60 ≈ 0.38/秒, not 0.33/秒 (which is the base-reward-basis 20/60 from the preceding clause).
- Fix: correct to ≈0.38/秒; the ordering 0.40 > 0.39 > 0.38 and the mixed-strategy conclusion stand.
- Impact: minor — the balance conclusion is unchanged, but the comparison figures are internally inconsistent.

**Issue 4 — §5.3 expansion-gate ambiguity** (🟡, Logic)
- Location: §5.3, first bullet (line 111)
- Original text: "扩建与订单解锁均以声望为门槛（扩建消耗见 4.3），两者互不依赖、无循环。"
- Description: read literally, expansion is reputation-gated; §4.3 defines only credit costs (300/800) and no expansion rep threshold exists, while §8's acceptance (new account expands within 15 min after one Q-1, ≈10 rep) rules out any meaningful rep gate. The alternative reading — the order lines unlocked by expansion are rep-gated (consistent with §5.1's "机库 2 级 + 声望 300" style conditions) — is coherent.
- Fix: reword to separate the two gates (order unlock = reputation; expansion = credit cost) and keep the no-cycle claim.
- Impact: low-to-moderate — an implementer following the literal reading would block on a threshold that is nowhere defined.

### Minor observations (informational, not counted in scores)

- §4.1 labels the stat "效率" (5 星 180%) while §4.2 applies the bonus as additive time reduction (1−E, E≤0.8); the mapping +20%/星 ↔ +0.2 is stated and all examples agree, but a one-line note that the bonus reduces time additively rather than multiplying work speed would prevent misreading.
- §2.3 "3 单维修 + 1 单精制" vs §5.1 "3 单普通 + 1 单精制": §5.1's precise definition governs; unify the wording.
- §4.2 calls the 0.95 matched-case rate "保底" while §9's "成功率保底 / success_floor" is the 0.80 clamp floor; both carry explicit numbers, but renaming one avoids conflation.
- Micro-edge behaviors unspecified (each resolvable by a one-line rule): part drops arriving at the 999/class inventory cap; 临时高额订单 spawning when the 5-slot pending area is full; the same random event drawing twice in one day (M_R stacking).
- The verbatim sentence "余额不足时采购/扩建被拦截（余额最低为 0，不产生负余额）" appears in both §2.3 and §4.3 — keep one authoritative copy (§4.3) and cross-reference.
- The appendix link targets the IANA-reserved example domain `https://docs.example.com/starport-balance` (curl: unreachable). All MUST-level link checks pass and example-domain anonymization is deliberate; replace with the real wiki URL before publishing.

## Fix Priority

**P0 (bug-level / scenario gaps, must fix)**: none at bug level; the two scenario gaps (Issues 1–2) must be filled before implementation hand-off. | **P1 (strongly recommended)**: correct §10's 0.33 → ≈0.38; reword §5.3's expansion-gate sentence. | **P2 (optional)**: the six minor observations above.

## Highlights

- Numeric system is genuinely cross-consistent: the five numeric credit rewards recompute exactly from the income formula (§5.1 note pins the basis; Q-6's 通关 reward is non-numeric and outside the check), the exchange ratios (2.5×/6×) and 50–67% margins in §4.3 recompute correctly, every tuning-knob safe range in §9 contains the value in use, and TC-1..TC-5 match their formulas.
- §6 covers all four required edge-case classes with concrete values (24h timeout with no penalty, unlimited retry with a 3-fail hint, credit cap 99999 with overflow protection, part cap 999, dual-device read-only mode, save points and rollback with overwrite warning), and the clamp notes even prove the bounds are reachable (E=0.8 → factor 0.1).
- §10 argues balance properly: it tests the dominant-strategy question under two accounting bases and concludes no single all-time-optimal strategy exists, cross-linked to the supply-cut event that constrains the pure-special route.
- Inter-system dependencies (§5.3) are declared bidirectionally with an explicit no-deadlock argument (reputation only accumulates).
- The externalized-config commitment (§9 → `config/values.yaml`, "代码不硬编码") is exactly what the Tuning Knobs checklist item wants.

## Auto-Fix Summary (--format fix)

Not run — this review executed with the default full format in solo mode; no mechanical fixes were applied. Fixed: 0 | Could not auto-fix: 0

---

MD-REVIEW-SUMMARY
File: evals/docs/clean-gdd.md | P0 bugs: 0 | Scenario gaps: 2 | Fixable: 4 | Generated: 2026-09-05T12:11:01Z
