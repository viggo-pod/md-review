All invocations executed. Here is the report.

## Error-Handling Self-Test Report — md-review skill (solo mode)

**Protocol verified against** SKILL.md: `0` = no P0 & score ≥ threshold / `1` = P0 or below / `2` = error (missing file, invalid arguments). Error Handling section: *"Missing file / binary file / non-UTF-8 encoding: report and skip (try to detect the encoding first)"; "extract_refs.py failure: fall back to manual link checking"; "Invalid scenario value: list the valid values and review as generic."*

| # | Invocation | What the skill did | Outcome | Exit code | Verdict |
|---|---|---|---|---|---|
| 1 | `/md-review /nonexistent/path/does-not-exist.md --solo` | Phase 0 probe crashes (`FileNotFoundError`, raw rc=1); agent caught it, reported "Missing file: …", skipped review (no scoring), emitted `MD-REVIEW-SUMMARY` with 0 files | Reported and skipped, no crash | **2** (set via shell) | **PASS** |
| 2 | `/md-review …/binary-file.md --solo` | utf-8 decode failed at byte `0xff`; agent tried encoding detection first (latin-1 decodes all 256 bytes) then detected NUL bytes (`00 01 02 03 …`, 3 NULs) → classified binary; reported and skipped, no crash | Binary detected, reported and skipped | **2** | **PASS** |
| 3 | `/md-review …/latin1-file.md --solo` | utf-8 decode failed at `0xe9`; agent tried detection first → latin-1/ISO-8859-1 decoded cleanly (`'# Café Data Report\n## Résumé…'`); reported the encoding and skipped gracefully, no crash | latin-1 detected, reported and skipped | **2** | **PASS** |
| 4 | `/md-review …/clean-api.md foobar --solo` | `foobar` not in the 14 scenarios → listed all valid values (`prd|adr|add|api|brd|mrd|fsd|gdd|gdo|tdd|ldd|concept|tld|tcd`) and reviewed as **generic** (scenario dimension skipped, scored 100). extract_refs: 0 links. `score.py 100 100 100 100 95 100` → Overall 99.5, Grade Excellent, Risk Low | Listed valid values, reviewed as generic | **0** (no P0, 99.5 ≥ 75) | **PASS** |
| 5 | `extract_refs.py` on binary-file.md | `UnicodeDecodeError: 0xff in position 8`, raw rc=1 → per SKILL.md "extract_refs.py failure: fall back to manual link checking", the agent catches it and falls back to manual checking (0 links found to verify) | Fallback triggered cleanly | — | **PASS** |

### Key findings (evidence)

- **The helper scripts do NOT self-handle edge cases** — `probe.py` and `extract_refs.py` exit 1 with unhandled `FileNotFoundError`/`UnicodeDecodeError` on missing/binary/latin-1 input. The Error Handling behavior lives entirely in the skill agent wrapper (it must catch the Phase 0 probe crash, attempt encoding detection, and report+skip). This works as specified, but is a fragility point: any invocation that forgets the wrapper logic will crash the pipeline.
- **Exit code 2 for cases 2/3 is an inference.** SKILL.md only literally lists "missing file, invalid arguments" for code 2; binary/non-UTF-8 files are not explicitly mapped. I assigned 2 (error category, consistent with "report and skip" + no score) — protocol-compatible but worth documenting explicitly in SKILL.md.
- **Probe error-path exit codes are inconsistent** with the solo protocol: `probe.py` (no arg) and script crashes exit 1, while solo protocol says 2 for errors. No script currently distinguishes these, so CI parsing must rely on the agent's wrapper exit, not the scripts'.
- `clean-api.md` genuinely has no injected defects (rate-limit 100/min × 60 = 6,000/hr is consistent; P99 500 ms > avg 200 ms is sane; refund ≤ original amount; 0 extractable links), so the generic review legitimately scores 99.5 with 0 P0 → exit 0.

**Files examined:** `SKILL.md`, `scripts/{probe,analyze_structure,extract_refs,score}.py`, `evals/docs/{binary-file,latin1-file,clean-api}.md`, `evals/scripts/verify_scripts.py`. No skill files were modified.