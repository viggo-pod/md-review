<div align="center">

# 📝 md-review

Scenario-aware Markdown review with weighted scoring.

[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/viggo-pod/md-review)
[![Skills](https://skills.sh/b/viggo-pod/md-review)](https://skills.sh/viggo-pod/md-review/md-review)
[![ModelScope](https://img.shields.io/badge/ModelScope-viggopod%2Fmd--review-6600ff.svg)](https://www.modelscope.cn/skills/viggopod/md-review)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/viggo-pod/md-review/pulls)

**[English](README.md) · [简体中文](README-zh.md)**

</div>

**It finds bugs and logic errors that would break downstream implementation first, then checks scenario-specific completeness** — style and formatting are secondary.

Reviews ONE Markdown document per invocation across 14 document scenarios (PRD, API spec, GDD, TDD, ADR, …) or in generic mode.

## Highlights

- **Bug-first positioning** — Logic (30%) is the top dimension: formula/number contradictions, missing edge cases, broken flows. P0 (blocking) issues are reported regardless of focused dimensions.
- **14 scenarios** — each with its own required-content checklist (acceptance criteria, 5W1H, endpoint contracts, error codes, test cases, …).
- **6 weighted dimensions** — Logic 30%, Scenario completeness 25%, Sections 15%, References 10%, Redundancy 10%, Format 10%. **Overall = Σ(dimension score × weight)**, 100-point scale; each dimension score is the ratio of satisfied items in its checklist or rule index (counted per applicable item) × 100.
- **CI-ready** — `--solo` mode with exit-code gate (`--pass-threshold`, default 75) and a machine-readable `MD-REVIEW-SUMMARY` block as the last line of every report.
- **Self-validating** — ships injected-defect fixtures, a trigger-query set, and a one-command regression harness (`bash evals/run_self_test.sh`); the eval registry was reset for the count-based scoring redesign and new evals are being re-established.

## Scenarios

The scenario is optional; without one, the review runs in generic mode (scenario-completeness is skipped).

| Scenario | Document | Required-content focus |
|---|---|---|
| `prd` | Product Requirements Document | requirement list, user stories, acceptance criteria, 5W1H |
| `adr` | Architecture Decision Record | context / decision / rationale / alternatives / consequences |
| `add` | Architecture Design Description | architecture views, quality attributes, interfaces, data flow |
| `api` | API Document | endpoint contracts, error codes, auth, runnable examples |
| `brd` | Business Requirements Document | business goals, ROI, cost/revenue model, 5W1H |
| `mrd` | Market Requirements Document | market analysis, user personas, value proposition, 5W1H |
| `fsd` | Functional Specification Document | functional behavior, use cases, test cases, acceptance criteria |
| `gdd` | Game Design Document | core loop, numbers, test cases, task lists |
| `gdo` | Game Overview Document | executive summary, core concept, design pillars, USP |
| `tdd` | Technical Design Document | system architecture, tech stack, coding standards, performance goals |
| `ldd` | Level Design Document | level layout, player path, challenge configuration, pacing |
| `concept` | Concept Design Document | game concept, market analysis, core selling points |
| `tld` | Task List Document | task decomposition, dependencies, effort estimates, owners |
| `tcd` | Test Case Document | case IDs, test steps, inputs/outputs, requirement traceability |

## Requirements

- Python 3 (helper scripts: `scripts/probe.py`, `scripts/analyze_structure.py`, `scripts/extract_refs.py`, `scripts/score.py`, `scripts/validate_path.py`)
- A Claude Code / Claude-compatible agent runtime that supports slash commands and skill directories

## Installation

Copy the `skills/md-review` folder into your skills directory:

```bash
# Claude Code (user-global)
cp -r skills/md-review ~/.claude/skills/

# or project-local
cp -r skills/md-review <your-project>/.claude/skills/
```

The skill is defined by `SKILL.md`; it reads `references/` (rules + per-scenario checklists), uses `scripts/` (structural analysis) and `example/` (report templates) at runtime. `evals/` is the development/regression suite and is optional at runtime.

## Usage

```
/md-review <path> [scenario] [--dimensions 1,2,3,4,5,6] [--format full|summary|fix] [--solo] [--pass-threshold N] [--output file] [json]
```

| Option | Effect |
|---|---|
| `<path>` | Markdown file to review (single document; validated by the path gate first) |
| `<scenario>` | One of the 14 scenarios above; omit for generic mode |
| `--dimensions` | Restrict to specific dimensions, e.g. `--dimensions 1,2` (logic + completeness). P0 detection is independent of this flag |
| `--format full` | Complete report (default) |
| `--format summary` | Score table only |
| `--format fix` | Report + auto-fix. Only safe mechanical fixes are applied (link-text repairs, filler-word replacements, echo-title removals, trailing newlines); everything requiring judgment is reported unfixed |
| `--solo` | Non-interactive mode for CI |
| `--pass-threshold N` | Solo-mode exit-code gate on the overall score (default 75) |
| `--output <file>` | Also write the report to a file |
| `json` | Append to also emit machine-readable JSON |

### Modes

- **Interactive (default)** — presents a review plan and requests approval before the full review; files change only after user approval.
- **Solo (`--solo`)** — non-interactive, runs straight through, writes the full report to stdout (and to `--output` when given), always ends with the `MD-REVIEW-SUMMARY` block.

### Exit codes (CI gate)

- `0` — review completed, no P0 (blocking) issues, overall score ≥ `--pass-threshold`
- `1` — review completed, but P0 issues exist or the score is below the threshold
- `2` — error (missing file, invalid arguments, undecodable input)

### Output contract

Every report ends with a machine-readable summary block:

```
MD-REVIEW-SUMMARY
File: <doc> | P0 bugs: N | Scenario gaps: N | Fixable: N | Generated: {timestamp}
```

When `--output` is used, the block is also the last line of the written file, so CI can parse either the stdout handoff or the artifact.

## Examples

```
/md-review docs/requirements.md prd --solo --pass-threshold 75
```

Review a PRD in solo mode; exit 0 if no blocking issues and score ≥ 75.

```
/md-review docs/api-spec.md api --format summary
```

Score-table-only review of an API document.

## Quality evidence

The repo includes its own evaluation suite under `evals/`:

- `bash evals/run_self_test.sh` — regression harness: scripted checks (script function-point verification via `verify_scripts.py`, registry integrity) run always; agent-based checks (clean-doc precision, error-handling protocol, step-numbering detection) re-activate as new eval reports are added.
- `evals/docs/` — 23 fixtures: 15 scenario documents with injected defects, 3 clean documents, plus binary/non-UTF-8/step-numbering edge cases.
- `evals/evals.json` — eval registry, reset to an empty skeleton for the count-based scoring redesign; new evals are being re-established.
- `evals/trigger-eval-set.json` — 20 trigger/no-trigger queries validating skill activation.

In the development benchmark (round 3, 40-run matrix), the skill passed 212/213 runs (99.5%), and 100% of injected defects were detected.

## Repository layout

```
md-review/
├── skills/
│   └── md-review/              # the skill
│       ├── references/         # review rules
│       │   └── scenarios/      # per-scenario checklists
│       ├── scripts/            # python helpers
│       └── example/            # report templates
├── evals/                      # development/regression suite
│   ├── docs/                   # test fixtures
│   ├── reports/                # reference reports
│   └── scripts/                # verification harness
├── README.md
├── LICENSE
└── .gitignore
```

## License

MIT — see [LICENSE](LICENSE).
