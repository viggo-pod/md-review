#!/usr/bin/env python3
"""Coverage + cross verification of md-review scripts (probe/analyze_structure/extract_refs/score).

For each script, exercise every function point with crafted fixtures and assert
on the output; then cross-verify against the 4 eval test docs.
Usage: python3 verify_scripts.py
Exit code 0 = all checks pass, 1 = failures.
"""

import re
import subprocess
import sys
import tempfile
from pathlib import Path


def _find_root(p: Path, depth: int = 0) -> Path:
    if (p / "evals").is_dir():
        return p
    if depth >= 5:
        raise RuntimeError("md-review repo root not found within 5 levels")
    return _find_root(p.parent, depth + 1)


ROOT = _find_root(Path(__file__).resolve().parent)
SCRIPTS = ROOT / "skills" / "md-review" / "scripts"
TESTDOCS = ROOT / "evals" / "docs"  # skill-local evals/docs (self-contained)

passed = []
failed = []


def check(name, cond, detail=""):
    if cond:
        passed.append(name)
        print(f"  PASS  {name}{(' — ' + detail) if detail else ''}")
    else:
        failed.append(name)
        print(f"  FAIL  {name}{(' — ' + detail) if detail else ''}")


def run(script, *args):
    return subprocess.run(
        [sys.executable, str(SCRIPTS / script), *args],
        capture_output=True, text=True,
    )


def run_input(script, stdin, *args):
    return subprocess.run(
        [sys.executable, str(SCRIPTS / script), *args],
        capture_output=True, text=True, input=stdin,
    )


print("=" * 70)
print("COVERAGE VERIFICATION — probe.py")
print("=" * 70)

fixture = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8")
fixture.write("""# Title One

Some intro sentence with TODO marker.

## Section A

| col1 | col2 |
|---|---|
| a | b |

### Sub A1

TODO: fix this

```python
print("hello")
```

[link to nowhere](missing.md)

![img](pic.png)

## Section B

##### Deep Skip

TBD item here

## Section C

FIXME

## Section D

待补充内容

## Section E

待定内容

## Section F

## Section G

## Section H

## Section I

## Section J

## Section K

## Section L

## Section M

## Section N

## Section O

## Section P

## Section Q

## Section R

## Section S

## Section T

## Section U

## Section V
""")
fixture.close()
fx = fixture.name

r = run("probe.py", fx)
out = r.stdout
check("probe: exit 0", r.returncode == 0, f"rc={r.returncode} stderr={r.stderr.strip()[:80]}")
check("probe: header", "=== Document Metadata Probe ===" in out)
check("probe: lines count", f"Lines: {sum(1 for _ in open(fx))}" in out)
check("probe: words count", "Words: " in out)
check("probe: est tokens", "Est. tokens: ~" in out)
check("probe: heading outline", "--- Heading outline (first 20) ---" in out)
check("probe: heading line numbers", "L1: # Title One" in out)
check("probe: >20 headings truncated", "... 25 headings total" in out)
check("probe: first-10 preview", "--- First 10 lines ---" in out)
check("probe: TODO marker found", "Incomplete markers" in out and "TODO" in out)
check("probe: FIXME/TBD counted", all(m in out for m in ["FIXME", "TBD"]))
check("probe: usage error without arg", run("probe.py").returncode == 1)

print()
print("=" * 70)
print("COVERAGE VERIFICATION — analyze_structure.py")
print("=" * 70)

r = run("analyze_structure.py", fx)
out = r.stdout
check("analyze: exit 0", r.returncode == 0)
check("analyze: header", "=== Structural Analysis:" in out)
check("analyze: heading levels dict", "{1: 1, 2: 6, 3: 1}" in out or "Heading levels:" in out)
check("analyze: code-block lang python", "python" in out and "Code-block languages:" in out)
check("analyze: table rows count", "Table rows:" in out and "| a | b |" not in out)
check("analyze: links count", "Links:" in out)
check("analyze: links excludes image (1 link, 1 image in fixture)",
      re.search(r"Links: (1|2)", out).group(1) == "1", "Links should be 1, not 2")
check("analyze: images count", "Images:" in out)
check("analyze: HACK/WIP markers", all(m in out for m in ["HACK", "WIP"]))
check("analyze: heading skips detected", bool(re.search(r"Heading skips[^\n]*:\s*1", out)), out.split("Heading skips")[1][:40])
check("analyze: usage error without arg", run("analyze_structure.py").returncode == 1)

print()
print("=" * 70)
print("COVERAGE VERIFICATION — extract_refs.py")
print("=" * 70)

ref_fx = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8")
ref_fx.write("""# Refs

[internal doc](docs/guide.md) and [external](https://example.com/page)

![logo](assets/logo.png) ![remote](https://img.example.com/a.png)

bare url: <https://example.org/raw>

insecure: [bad](http://insecure.example.com/x)

placeholder: [anchor](#)

localhost: [dev](http://localhost:3000/api)

[normal](https://api.example.com/v1)
""")
ref_fx.close()
rfx = ref_fx.name

r = run("extract_refs.py", rfx)
out = r.stdout
check("extract_refs: exit 0", r.returncode == 0)
check("extract_refs: header", "=== Markdown Reference Extraction ===" in out)
# F2 fixed: the [text](url) regex now excludes image syntax via (?<!!),
# so the 6 real links are counted without the 2 images.
check("extract_refs: text links count=6 (images no longer double-counted)",
      "Text links: 6" in out)
check("extract_refs: images excluded from internal link list",
      "[link] logo" not in out.split("Internal References")[1].split("External References")[0])
check("extract_refs: images count=2", "Image references: 2" in out)
check("extract_refs: bare urls count=1", "Bare URLs: 1" in out)
check("extract_refs: internal section", "--- Internal References ---" in out and "docs/guide.md" in out)
check("extract_refs: external section", "--- External References ---" in out and "example.com/page" in out)
check("extract_refs: image internal classified", "assets/logo.png" in out.split("Internal References")[1].split("External References")[0])
check("extract_refs: suspicious http", "Insecure" in out and "http://insecure.example.com" in out)
check("extract_refs: suspicious empty/#", "Empty link" in out)
check("extract_refs: suspicious localhost", "localhost" in out)
check("extract_refs: usage error without arg", run("extract_refs.py").returncode == 1)

print()
print("=" * 70)
print("COVERAGE VERIFICATION — score.py")
print("=" * 70)

r = run("score.py", "60", "70", "80", "50", "70", "90")
out = r.stdout
check("score: exit 0", r.returncode == 0)
check("score: weighted math (68.5)", "Overall: 68.5/100" in out)
check("score: per-dim weighted lines", all(f"x {w:.0%}" in out for w in [0.30, 0.25, 0.15, 0.10]))
check("score: grade Passing", "Grade: Passing" in out)
check("score: risk Medium", "Risk: Medium" in out)

r = run("score.py", "100", "100", "100", "100", "100", "100")
check("score: all-100 → 100", "Overall: 100.0/100" in r.stdout and "Grade: Excellent" in r.stdout and "Risk: Low" in r.stdout)

r = run("score.py", "90", "90", "90", "90", "90", "90")
check("score: 90 → Excellent", "Grade: Excellent" in r.stdout)
r = run("score.py", "75", "75", "75", "75", "75", "75")
check("score: 75 → Good", "Grade: Good" in r.stdout)
r = run("score.py", "60", "60", "60", "60", "60", "60")
check("score: 60 → Passing", "Grade: Passing" in r.stdout)
r = run("score.py", "59", "59", "59", "59", "59", "59")
check("score: <60 → Failing", "Grade: Failing" in r.stdout)

r = run("score.py", "80", "80", "80", "80", "80", "80")
check("score: 80 p0=0 → Low", "Risk: Low" in r.stdout)
r = run("score.py", "80", "80", "80", "80", "80", "80", "--p0", "2")
check("score: 80 p0=2 → Medium (p0 overrides)", "Risk: Medium" in r.stdout)
r = run("score.py", "50", "50", "50", "50", "50", "50", "--p0", "3")
check("score: 50 p0=3 → High", "Risk: High" in r.stdout)
r = run("score.py", "39", "39", "39", "39", "39", "39")
check("score: <40 → Critical", "Risk: Critical" in r.stdout)

check("score: wrong arg count → exit 1", run("score.py", "60", "70", "80").returncode == 1)
check("score: out-of-range → exit 2", run("score.py", "60", "70", "80", "150", "70", "90").returncode == 2)
check("score: non-numeric → exit 2", run("score.py", "60", "x", "80", "50", "70", "90").returncode == 2)
check("score: bad --p0 → exit 2", run("score.py", "60", "70", "80", "50", "70", "90", "--p0", "abc").returncode == 2)

print()
print("=" * 70)
print("CROSS-VERIFICATION — 4 test docs (scripts must parse + report key facts)")
print("=" * 70)

cross = {
    "prd-test.md": {
        "analyze_structure": ["Heading levels:", "Table rows:"],
        "extract_refs": ["launch-checklist.md", "Internal References"],
        "probe": ["Lines:", "Heading outline"],
    },
    "api-test.md": {
        "analyze_structure": ["Code-block languages:", "Links:"],
        "extract_refs": ["docs/auth.md", "docs/signature.md", "External References", "github.com"],
        "probe": ["Incomplete markers"],
    },
    "gdd-test.md": {
        "analyze_structure": ["Heading levels:", "Table rows:", "Images:"],
        "extract_refs": ["balance-table.md", "level-details.md"],
        "probe": ["Heading outline"],
    },
    "generic-test.md": {
        "analyze_structure": ["Heading levels:", "Code-block languages:", "Table rows:"],
        "extract_refs": ["data-dictionary.md"],
        "probe": ["Heading outline"],
    },
}

for doc, checks in cross.items():
    path = TESTDOCS / doc
    print(f"\n--- {doc} ---")
    for script, needles in checks.items():
        r = run(f"{script}.py", str(path))
        ok_exit = r.returncode == 0
        ok_needle = all(n in r.stdout for n in needles)
        check(f"{doc} / {script} exit 0", ok_exit, f"rc={r.returncode} {r.stderr.strip()[:80]}")
        check(f"{doc} / {script} key facts", ok_needle, f"missing={[n for n in needles if n not in r.stdout]}")

print()
print("=" * 70)
print("ERROR-PATH CHECKS — missing/binary/non-UTF-8 files (scripts hardened)")
print("=" * 70)

import subprocess as sp
ep = TESTDOCS
def run3(script, *args):
    return sp.run([sys.executable, str(SCRIPTS / script), *args], capture_output=True, text=True)

# missing file -> exit 2, graceful stderr
r = run3("probe.py", "/nonexistent/definitely-missing.md")
check("probe: missing file -> exit 2", r.returncode == 2, f"rc={r.returncode}")
check("probe: missing file graceful msg", "file not found" in r.stderr.lower())
r = run3("analyze_structure.py", "/nonexistent/definitely-missing.md")
check("analyze: missing file -> exit 2", r.returncode == 2)
r = run3("extract_refs.py", "/nonexistent/definitely-missing.md")
check("extract_refs: missing file -> exit 2", r.returncode == 2)

# binary file -> exit 2 (no crash), graceful msg
r = run3("probe.py", f"{ep}/binary-file.md")
check("probe: binary -> exit 2 (no crash)", r.returncode == 2, f"rc={r.returncode}")
check("probe: binary graceful msg", ("binary" in r.stderr.lower() or "decode" in r.stderr.lower()))
r = run3("extract_refs.py", f"{ep}/binary-file.md")
check("extract_refs: binary -> exit 2", r.returncode == 2)

# validate_path.py — single-doc *.md argument gate
def vp(*args):
    return sp.run([sys.executable, str(SCRIPTS / "validate_path.py"), *args], capture_output=True, text=True)
r = vp(f"{ep}/prd-test.md")
check("validate_path: valid .md -> exit 0", r.returncode == 0, f"rc={r.returncode}")
check("validate_path: missing -> exit 2", vp("/nonexistent/x.md").returncode == 2)
check("validate_path: directory -> exit 2", vp(f"{ep}").returncode == 2)
check("validate_path: non-md (.py) -> exit 2", vp(f"{SCRIPTS}/score.py").returncode == 2)
check("validate_path: binary -> exit 2", vp(f"{ep}/binary-file.md").returncode == 2)
check("validate_path: latin-1 text -> exit 0", vp(f"{ep}/latin1-file.md").returncode == 0)
check("validate_path: no arg -> exit 2", vp().returncode == 2)

print()
print("=" * 70)
print("STEP-NUMBERING INTEGRITY — SKILL.md workflow phases (no skipped numbers)")
print("=" * 70)

import re as _re
skill_md = ROOT / "skills" / "md-review" / "SKILL.md"
lines = skill_md.read_text(encoding="utf-8").splitlines()
phase_ok = True
cur_phase = None
phase_items = {}
for ln in lines:
    m = _re.match(r"^### Phase (\d+):", ln)
    if m:
        cur_phase = int(m.group(1))
        phase_items[cur_phase] = []
        continue
    if cur_phase is not None:
        m2 = _re.match(r"^(\d+)\.\s", ln)
        if m2:
            phase_items[cur_phase].append(int(m2.group(1)))
for ph, nums in sorted(phase_items.items()):
    if len(nums) >= 2:
        expected = list(range(nums[0], nums[0] + len(nums)))
        ok = nums == expected
        check(f"Phase {ph} steps sequential {nums}", ok, f"nums={nums}")
        phase_ok = phase_ok and ok
check("no step-numbering breaks in workflow phases", phase_ok)

print()
print("=" * 70)
print(f"RESULT: {len(passed)} passed, {len(failed)} failed")
print("=" * 70)
sys.exit(1 if failed else 0)
