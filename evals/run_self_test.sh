#!/usr/bin/env bash
# md-review self-test / regression harness.
#
# Deterministic checks (scripts) run automatically; agent-based checks
# (clean-doc precision, error-path protocol) are verified against reports
# when present, otherwise printed as instructions.
#
# Usage: bash evals/run_self_test.sh
set -u
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PASS=0; FAIL=0

ok()   { PASS=$((PASS+1)); echo "  PASS  $1"; }
bad()  { FAIL=$((FAIL+1)); echo "  FAIL  $1"; }

echo "=============================================================="
echo " md-review self-test"
echo "=============================================================="

echo ""
echo "[1/5] Script function-point verification (verify_scripts.py)"
if python3 "$SKILL_DIR/evals/scripts/verify_scripts.py" >/dev/null 2>&1; then
  ok "verify_scripts.py: all checks passed (probe/analyze_structure/extract_refs/score + cross-verification + error paths)"
else
  bad "verify_scripts.py exited non-zero"
fi

echo ""
echo "[2/5] Precision & sensitivity baselines"
PRECISION_ALL_PASS=1
for CLEAN in clean-api clean-prd clean-gdd; do
  CLEAN_REPORT="$SKILL_DIR/evals/reports/${CLEAN}-report.md"
  if [ -f "$CLEAN_REPORT" ]; then
    python3 - "$CLEAN_REPORT" <<'EOF'
import re, sys
t = open(sys.argv[1], encoding="utf-8").read()
m = re.search(r"Overall[^0-9]*([0-9.]+)/100", t)
score = float(m.group(1)) if m else 0.0
p0m = re.search(r"P0 bugs?:?\s*(\d+)", t)
p0 = int(p0m.group(1)) if p0m else -1
print(f"    {sys.argv[1].rsplit('/',1)[-1]}: overall={score}/100  P0-count={p0}")
sys.exit(0 if score >= 85 and p0 == 0 else 1)
EOF
    [ $? -eq 0 ] || PRECISION_ALL_PASS=0
  else
    echo "  SKIP  ${CLEAN}-report.md not found — run an agent review of evals/docs/${CLEAN}.md and save the report to evals/reports/${CLEAN}-report.md"
  fi
done
if [ "$PRECISION_ALL_PASS" -eq 1 ]; then
  ok "clean docs (api/prd/gdd): score>=85 and no P0 (precision baseline)"
else
  bad "clean doc: score<85 or P0 flagged (possible false positive)"
fi

echo "  -- sensitivity baselines (injected-defect docs must be rejected: P0>=1 or score<75) --"
SENS_ALL_PASS=1
for DEFECT in prd-test api-test gdd-test; do
  DEFECT_REPORT="$SKILL_DIR/evals/reports/${DEFECT}-report.md"
  if [ -f "$DEFECT_REPORT" ]; then
    python3 - "$DEFECT_REPORT" <<'EOF'
import re, sys
t = open(sys.argv[1], encoding="utf-8").read()
m = re.search(r"Overall[^0-9]*([0-9.]+)/100", t)
score = float(m.group(1)) if m else 100.0
p0m = re.search(r"P0 bugs?:?\s*(\d+)", t)
p0 = int(p0m.group(1)) if p0m else 0
rejected = (p0 >= 1) or (score < 75)
verdict = "rejected (solo exit 1)" if rejected else "WRONGLY PASSED the gate"
print(f"    {sys.argv[1].rsplit('/',1)[-1]}: overall={score}/100  P0-count={p0}  -> {verdict}")
sys.exit(0 if rejected else 1)
EOF
    [ $? -eq 0 ] || SENS_ALL_PASS=0
  else
    echo "  SKIP  ${DEFECT}-report.md not found — run an agent review of evals/docs/${DEFECT}.md and save the report to evals/reports/${DEFECT}-report.md"
  fi
done
if [ "$SENS_ALL_PASS" -eq 1 ]; then
  ok "defect docs (prd/api/gdd-test): rejected by gate (P0>=1 or score<75)"
else
  bad "defect doc wrongly passed the gate (sensitivity failure)"
fi

echo ""
echo "[3/5] Error-handling protocol (agent-based; checks report when present)"
ERR_REPORT="$SKILL_DIR/evals/reports/error-paths-report.md"
if [ -f "$ERR_REPORT" ]; then
  python3 - "$ERR_REPORT" <<'EOF'
import sys
t = open(sys.argv[1], encoding="utf-8").read()
checks = {
    "missing-file exit 2": ("missing" in t.lower() and "**2**" in t),
    "binary detected/skipped": ("binary" in t.lower() and ("skip" in t.lower() or "detect" in t.lower())),
    "non-utf8 encoding detected": ("latin-1" in t.lower() or "encoding" in t.lower() or "utf-8" in t.lower()),
    "invalid scenario lists all 14 valid values with exit 2": all(s in t for s in ("prd", "adr", "add", "api", "brd", "mrd", "fsd", "gdd", "gdo", "tdd", "ldd", "concept", "tld", "tcd")) and "code **2**" in t,
}
for name, okv in checks.items():
    print(f"    {'PASS' if okv else 'FAIL'}  {name}")
sys.exit(0 if all(checks.values()) else 1)
EOF
  [ $? -eq 0 ] && ok "error-handling protocol satisfied" || bad "error-handling protocol check failed"
else
  echo "  SKIP  error-paths-report.md not found — run an agent review exercising: missing file (exit 2), binary file, non-UTF-8 file, invalid scenario value; save findings to evals/reports/error-paths-report.md"
fi

echo ""
echo "[4/5] Dev-toolchain registry integrity"
python3 - "$SKILL_DIR/evals/evals.json" "$SKILL_DIR/evals/trigger-eval-set.json" <<'EOF'
import json, sys
ok_reg = ok_trig = False
try:
    evals = json.load(open(sys.argv[1]))
    ev = evals.get("evals", [])
    ids = sorted(e["id"] for e in ev)
    fields_ok = all(e.get(k) for e in ev for k in ("name", "prompt", "expected_output", "expectations"))
    ok_reg = (evals.get("skill_name") == "md-review" and isinstance(ev, list) and len(ev) == 12
              and ids == list(range(12)) and fields_ok)
    print(f"    evals.json: skill_name={evals.get('skill_name')}, {len(ev)} count-based evals, ids 0-11, required fields present -> {'PASS' if ok_reg else 'FAIL'}")
except Exception as e:
    print(f"    evals.json: FAIL ({e})")
try:
    trig = json.load(open(sys.argv[2]))
    n_t = sum(1 for q in trig if q.get("should_trigger"))
    n_n = sum(1 for q in trig if not q.get("should_trigger"))
    ok_trig = len(trig) == 20 and n_t == 10 and n_n == 10
    print(f"    trigger-eval-set.json: {len(trig)} queries ({n_t} trigger / {n_n} no-trigger) -> {'PASS' if ok_trig else 'FAIL'}")
except Exception as e:
    print(f"    trigger-eval-set.json: FAIL ({e})")
sys.exit(0 if ok_reg and ok_trig else 1)
EOF
[ $? -eq 0 ] && ok "dev-toolchain registries valid (evals.json + trigger-eval-set.json)" \
             || bad "dev-toolchain registry check failed"

echo ""
echo "[5/5] Step-numbering-break detection"
NUM_REPORT="$SKILL_DIR/evals/reports/numbering-break-report.md"
if [ -f "$NUM_REPORT" ]; then
  python3 - "$NUM_REPORT" <<'EOF'
import sys
t = open(sys.argv[1], encoding="utf-8").read()
checks = {
    "gap flagged (Deploy 1,2,4,5)": "gap" in t.lower() and "1, 2, 4, 5" in t,
    "duplicate flagged (Rollback 1,2,2,3)": "duplicate" in t.lower() and "1, 2, 2, 3" in t,
    "sequential lists not flagged": "sequential" in t.lower() and "Not flagged" in t,
    "T-IDs not flagged as break": "identifier-style" in t.lower() and "Not flagged" in t,
}
for name, okv in checks.items():
    print(f"    {'PASS' if okv else 'FAIL'}  {name}")
sys.exit(0 if all(checks.values()) else 1)
EOF
  [ $? -eq 0 ] && ok "step-numbering-break detection: gap+duplicate flagged, no false positives" \
               || bad "step-numbering-break detection check failed"
else
  echo "  SKIP  numbering-break-report.md not found — run an agent review of evals/docs/numbering-break.md (generic solo) and save to evals/reports/numbering-break-report.md"
fi

echo ""
echo "=============================================================="
echo " RESULT: $PASS passed, $FAIL failed"
echo "=============================================================="
[ "$FAIL" -eq 0 ]
