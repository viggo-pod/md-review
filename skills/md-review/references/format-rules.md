# Format Rules — Detailed Rules for Format (Basic Checks Only)

This dimension carries only 10% of the overall weight. Detailed linting (item-by-item MD spec checks) is handled by the editor's linting tooling (e.g., a VS Code extension, if installed); this file covers only **formatting issues that affect rendering correctness** (readability issues are handled by external tooling and are not checked here).

## Rendering-Critical Formatting Issues (must report)

### Headings
- Heading-level skips (H1 → H3 skipping H2) — affects document structure comprehension and table-of-contents generation
- Multiple H1 headings (the document title should be the unique H1)
- Missing blank line before a setext heading that directly follows a paragraph (the heading line is parsed as paragraph text). Do NOT flag ATX headings (`#`) without surrounding blank lines — CommonMark does not require them

### Code Blocks
- Unclosed fenced code blocks — a fence opened with a run of 3+ backticks or 3+ tildes that is never closed; the closing fence must use the same character and be at least as long as the opening fence (a longer closing fence is valid) — subsequent content may be swallowed into the code block
- Unclosed inline code — a code span opened with a run of one or more backticks that is not closed by an equal-length backtick run — affects rendering

### Numbered Lists (step-numbering breaks)
- **Gap in a contiguous ordered list** (1, 2, 4): a step number is skipped — in procedures (test steps, build steps, process flows) this usually means a step was deleted or forgotten; flag it
- **Duplicate number in a contiguous ordered list** (1, 2, 2, 3): numbering error in the source
- **Do NOT flag** (precision): a new list that legitimately restarts at 1 after a reset boundary (blank line, heading, table, or code block); identifier-style numbers (T-1, TC-1, REQ-001) are not ordered lists; single-item lists
- A step-numbering gap in a **semantic procedure** (test steps, build/deploy steps, process flows) should ALSO be reported under Logic as a broken/missing step — the gap often hides a deleted or forgotten step

### Links and Images
- Incomplete `[text](url)` syntax (missing parentheses)
- Relative paths that do not resolve from the current document location (e.g. `README.md` and `docs/guide.md` are valid relative destinations; verify the target exists instead of checking for a `./`/`../` prefix)

## Rule Index (count-based)

Each rule below is one countable item and applies to every document: a rule with at least one finding = 1 unmet item (occurrence counts reported as severity), and a rule with no finding is satisfied. The absence of required content (e.g., a missing overview or conclusion) is itself a finding — never an N/A. N/A is reserved for items that genuinely cannot apply to the document and must be justified in the report. Dimension score = (rules with no finding) ÷ (total rules) × 100.

| # | Rule |
|---|---|
| 1 | Heading-level skip (H1 → H3 skipping H2) |
| 2 | Multiple H1 headings |
| 3 | Missing blank line before a setext heading that directly follows a paragraph |
| 4 | Unclosed fenced code block |
| 5 | Unclosed inline code span |
| 6 | Step-numbering break (gap or duplicate) in an ordered list |
| 7 | Incomplete link syntax |
| 8 | Relative path that does not resolve from the current document location |

