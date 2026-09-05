# Error-Paths Protocol Report

Exercise of the md-review error-handling and exit-code protocol defined in `skills/md-review/SKILL.md` (Error Handling section) and enforced by `skills/md-review/scripts/validate_path.py`. Every result below is the captured output of an actual run against the repository's own fixtures.

## Exercise Results

| # | Path exercised | Target | Result | Exit code |
|---|---|---|---|---|
| 1 | Missing file | `/nonexistent/ghost.md` | `Error: missing target — expected a single Markdown (*.md) file` | **2** |
| 2 | Directory target | `evals/docs` | `Error: directory target — expected a single Markdown (*.md) file` | **2** |
| 3 | Non-md extension | `evals/run_self_test.sh` (`.sh`) | `Error: not a *.md file (got extension '.sh')` | **2** |
| 4 | Binary file (path gate) | `evals/docs/binary-file.md` | `Error: binary file (contains NUL bytes)` — detected and rejected | **2** |
| 5 | Binary file (probe.py) | `evals/docs/binary-file.md` | Same NUL-byte detection; no traceback, no partial output | **2** |
| 6 | Non-UTF-8 file (probe.py) | `evals/docs/latin1-file.md` | Decoded as latin-1 per the encoding fallback and processed normally (5 lines probed) | 0 |
| 7 | Valid document | `evals/docs/clean-api.md` | `OK: single Markdown document` — review proceeds | 0 |

## Invalid Scenario Protocol

An invalid scenario value (not one of the 14 defined scenarios) must **not** fall back to a generic review. Per SKILL.md Error Handling, the reviewer lists the 14 valid values — `prd, adr, add, api, brd, mrd, fsd, gdd, gdo, tdd, ldd, concept, tld, tcd` — and exits with code **2**, so a typo can never silently skip the scenario-completeness dimension.

## Conclusion

- The path gate rejects every invalid target class (missing / directory / non-md / binary) with a clear stderr message and exit **2**, before any probe or review runs.
- The helper scripts fail gracefully (no tracebacks) on binary input and apply the documented latin-1 encoding fallback for non-UTF-8 text.
- The solo exit-code contract: this protocol exercised and captured exit codes `0` and `2` only; exit code `1` (findings below threshold) is covered by the defect-fixture sensitivity reviews, not by this protocol.

MD-REVIEW-SUMMARY
File: (error-path protocol exercise) | P0 bugs: 0 | Scenario gaps: 0 | Fixable: 0 | Generated: 2026-09-05
