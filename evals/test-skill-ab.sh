#!/usr/bin/env bash
# Offline self-test of skill-ab.py: a stub `claude` answers per scenario, no model calls.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
AB="$HERE/skill-ab.py"
W="$(mktemp -d)"
trap 'rm -rf "$W"' EXIT
export SKILL_AB_CACHE="$W/cache" SKILL_AB_WORKERS=1 CLAUDE_BIN="$W/stub.py"
FAIL=0

cat > "$W/stub.py" <<'PY'
#!/usr/bin/env python3
import json, os, re, sys
if "--version" in sys.argv:
    print("stub 0"); sys.exit(0)
prompt = sys.stdin.read()
state = os.environ["STUB_STATE"]
sc = os.environ.get("SCENARIO", "perfect")
def bump(key):
    p = os.path.join(state, key)
    n = int(open(p).read()) if os.path.exists(p) else 0
    open(p, "w").write(str(n + 1)); return n
bump("calls")
m = re.search(r"CASE:(\w+)", prompt); v = re.search(r"<!-- v:(\w+) -->", prompt)
if not m:  # smoke call
    tok = 99999 if sc == "smoke_heavy" else 100
    print(json.dumps({"is_error": False, "structured_output": {"selected": []}, "usage": {"input_tokens": tok, "output_tokens": 1}, "total_cost_usd": 0}))
    sys.exit(0)
case, var = m.group(1), v.group(1)
n = bump(f"{case}-{var}")
if sc == "all_fail": sys.exit(1)
if sc == "fail_once" and n % 2 == 0 and bump(f"f-{case}-{var}-{n}") == 0:
    sys.exit(1)
must = {"c1": ["n1", "n2"], "c2": ["n3"]}[case]
sel = list(must) + (["n3"] if case == "c1" else [])  # an ok pick must not raise recall above 1
if sc == "no_struct":
    print(json.dumps({"is_error": False, "result": "plain text", "usage": {"input_tokens": 1, "output_tokens": 1}})); sys.exit(0)
if sc == "lost" and var == "B" and case == "c1": sel = ["n2", "n3"]
if sc == "flicker" and var == "B" and case == "c1" and n < 3: sel = ["n2", "n3"]
if sc == "cap" and var == "A" and case == "c1": sel = ["n1", "n2", "n3", "n4"]
print(json.dumps({"is_error": False, "structured_output": {"selected": sel},
                  "usage": {"input_tokens": len(prompt) // 4, "output_tokens": 10}, "total_cost_usd": 0.001}))
PY
chmod +x "$W/stub.py"

mk_suite() {  # $1 = dir, $2 = B moc body extra, $3 = extra json for case c1
  local d="$1"; local c1must='["n1","n2"]'; [ -n "${3:-}" ] && c1must="$3"; mkdir -p "$d/pool"
  for i in 1 2 3 4; do printf -- '---\nstatus: emerging\n---\n# Note n%s thesis\nbody %s\n' "$i" "$i" > "$d/pool/n$i.md"; done
  printf '<!-- v:A -->\n## S\n- [[n1]] long hand hook one\n- [[n2]] long hand hook two\n- [[n3]] long hand hook three\n- [[n4]] long hand hook four with a lot of extra words to make A expensive\n' > "$d/A.md"
  printf '<!-- v:B -->\n## S\n- [[n1]] t1\n- [[n2]] t2\n- [[n3]] t3\n%s\n' "${2:-- [[n4]] t4}" > "$d/B.md"
  cp "$d/A.md" "$d/CTRL.md"; sed -i '' 's/v:A/v:CTRL/' "$d/CTRL.md"
  printf 'spec text\n' > "$d/spec.md"; printf 'system\n' > "$d/prompt.md"
  cat > "$d/suite.json" <<JSON
{"name": "t$(basename "$d")", "model": "stub", "pool_dir": "$d/pool", "system": "prompt.md",
 "template": "CASE:{problem}\n{spec}\n{moc}", "coverage_input": "moc", "reps": 3, "escalate_reps": 5,
 "inputs": {"spec": {"file": "$d/spec.md"},
            "moc": {"A": {"file": "$d/A.md"}, "B": {"file": "$d/B.md"}, "CTRL": {"file": "$d/CTRL.md"}}},
 "decision": {"recall_tolerance": 0.05, "recall_reject": 0.10, "noise_tolerance": 1.0, "min_token_saving": 0.15,
              "ctrl_min_drop": 0.15, "max_error_rate": 0.10, "smoke_max_input_tokens": 8000},
 "cases": [{"id": "c1", "problem": "c1", "must": $c1must, "ok": ["n3"], "max_selected": 3},
           {"id": "c2", "problem": "c2", "must": ["n3"], "ok": ["n4"]}]}
JSON
}

run() {  # $1 name, $2 scenario, $3.. args ; sets RC, OUT, CALLS
  local name="$1" sc="$2"; shift 2
  export STUB_STATE="$W/state-$name" SCENARIO="$sc"; rm -rf "$STUB_STATE"; mkdir -p "$STUB_STATE"
  python3 "$AB" "$@" > "$W/out-$name.txt" 2>&1; RC=$?
  OUT="$(cat "$W/out-$name.txt")"; CALLS="$(cat "$STUB_STATE/calls" 2>/dev/null || echo 0)"
}
check() {  # $1 label, $2 condition result (0 = pass)
  if [ "$2" -eq 0 ]; then echo "ok   $1"; else echo "FAIL $1"; FAIL=1; sed 's/^/     | /' "$W/out-$3.txt" | head -40; fi
}
has() { grep -q -- "$2" "$W/out-$1.txt"; }

mk_suite "$W/s1"
run a perfect run "$W/s1"
check "a perfect picks (+ an ok note), B cheaper -> recall exactly 1, ADOPT" $([ $RC -eq 0 ] && has a "VERDICT: ADOPT B" && grep -E -q "^A +1\.000±" "$W/out-a.txt" && grep -E -q "^B +1\.000±" "$W/out-a.txt"; echo $?) a

run b lost run "$W/s1"
check "b B always drops n1 -> escalated, confirmed lost, REJECT" $([ $RC -eq 0 ] && has b "escalating" && has b "CONFIRMED LOST NOTES" && has b "VERDICT: REJECT B"; echo $?) b

run b2 lost run "$W/s1" --no-escalate
check "b2 lost note without escalation -> unresolved candidate, not ADOPT" $([ $RC -eq 0 ] && has b2 "lost-note candidates" && has b2 "\[ \] no unresolved lost-note candidate" && ! has b2 "VERDICT: ADOPT"; echo $?) b2

run c flicker run "$W/s1"
check "c B misses n1 only at stage 1 -> no confirmed lost note, not REJECT" $([ $RC -eq 0 ] && has c "escalating" && ! has c "CONFIRMED LOST" && ! has c "VERDICT: REJECT"; echo $?) c

run d all_fail run "$W/s1"
check "d every call fails -> exit 3, verdict INVALID" $([ $RC -eq 3 ] && ! has d "0.000±" && has d "VERDICT: INVALID"; echo $?) d

run d2 no_struct run "$W/s1"
check "d2 answers without structured_output -> errors, exit 3" $([ $RC -eq 3 ]; echo $?) d2

run e fail_once run "$W/s1"
check "e first attempt fails -> retried, run counts" $([ $RC -eq 0 ] && has e "VERDICT: ADOPT B"; echo $?) e

mk_suite "$W/s2" "" '["n1","nX"]'
run f perfect run "$W/s2"
check "f gold id not in pool -> exit 2 before any call" $([ $RC -eq 2 ] && [ "$CALLS" = 0 ] && has f "nX"; echo $?) f

mk_suite "$W/s3" " "
run g perfect run "$W/s3"
check "g pool note missing from B -> exit 2 naming it" $([ $RC -eq 2 ] && has g "n4"; echo $?) g

mk_suite "$W/s4" "- [[n4]] $(printf 'x%.0s' $(seq 1 3000))"
run h perfect run "$W/s4"
check "h B more expensive -> not ADOPT" $([ $RC -eq 0 ] && ! has h "VERDICT: ADOPT"; echo $?) h

RUN_A="$(sed -n 's/^run dir: //p' "$W/out-a.txt")"
run i perfect report "$RUN_A" --suite "$W/s1"
check "i report re-grades with zero calls, same verdict" $([ $RC -eq 0 ] && [ "$CALLS" = 0 ] && has i "VERDICT: ADOPT B"; echo $?) i

run j smoke_heavy run "$W/s1"
check "j smoke over token ceiling -> exit 2" $([ $RC -eq 2 ] && has j "leaked"; echo $?) j

run k perfect calibrate "$W/s1"
check "k CTRL identical to A -> calibration fails" $([ $RC -eq 1 ] && has k "control not caught"; echo $?) k
run k2 perfect run "$W/s1"
check "k2 failed calibration -> ADOPT marked NOT TRUSTWORTHY" $(has k2 "NOT TRUSTWORTHY: calibration failed"; echo $?) k2

printf 'system v2\n' > "$W/s1/prompt.md"
run k3 perfect run "$W/s1"
check "k3 prompt changed after calibration -> calibration no longer applies" $(has k3 "no calibration for these inputs" && ! has k3 "calibration failed"; echo $?) k3

run l cap run "$W/s1"
check "l A over max_selected -> cap violation counted" $([ $RC -eq 0 ] && grep -E -q '^A +[0-9.]+±[0-9.]+ +[0-9.]+±[0-9.]+ +[0-9]+ +[1-9]' "$W/out-l.txt"; echo $?) l

[ $FAIL -eq 0 ] && echo "ALL PASS" || echo "SOME FAILED"
exit $FAIL
