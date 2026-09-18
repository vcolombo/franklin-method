#!/usr/bin/env bash
# Checks the campaign checker against two fixtures: one campaign that follows the
# schema, and one that breaks it the ways real campaigns actually break it.
set -uo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo="$(dirname "$here")"
checker="$repo/scripts/check-campaign.py"
today="2026-09-25"   # fixed, so the date-sensitive rules stay deterministic

fails=0
note() { printf '  %s\n' "$*"; }
ok()   { printf 'ok   %s\n' "$*"; }
bad()  { printf 'FAIL %s\n' "$*"; fails=$((fails + 1)); }

# --- the good fixture must come back clean, warnings included ----------------
# It carries benign extra keys in campaign.yml and an exemplar whose sub-skill is
# the parallel judgment rung — scored by prediction, with no gate in GATES.md.
# Neither is a fault, and neither may produce a finding.
if out=$(python3 "$checker" "$here/fixtures/good" --today "$today" --strict 2>&1); then
  ok "good fixture passes --strict"
else
  bad "good fixture should pass --strict"
  note "$out"
fi

# --- the bad fixture must fail, and name each rule it breaks -----------------
out=$(python3 "$checker" "$here/fixtures/bad" --today "$today" 2>&1)
status=$?
if [ "$status" -eq 1 ]; then
  ok "bad fixture exits 1"
else
  bad "bad fixture should exit 1, got $status"
  note "$out"
fi

expected=(
  C003  # no aim
  C004  # status outside the enum
  C005  # week_1 is not a date
  G004  # orientation covers nothing
  G014  # a solid placement with no evidence
  G016  # gate passed while placement is still pending
  G021  # only one modality
  G022  # video with no timestamped segment
  G024  # links never verified
  G026  # exit test with no exercise
  M004  # exemplar kind outside the enum
  M007  # cold delay under four days
  X001  # exemplar points at no rung
  X002  # prepped before the gate opened
  X004  # ripe while the gate is shut
)
for code in "${expected[@]}"; do
  if grep -qE "(^| )$code  " <<<"$out"; then
    ok "bad fixture reports $code"
  else
    bad "bad fixture should report $code"
  fi
done

# --- the JSON report has to be JSON ------------------------------------------
json_out=$(python3 "$checker" "$here/fixtures/bad" --today "$today" --json 2>/dev/null)
if python3 -c 'import json,sys; d=json.load(sys.stdin); assert d["campaigns"][0]["errors"] > 0' <<<"$json_out"; then
  ok "--json emits a parseable report"
else
  bad "--json should emit a parseable report"
fi

# --- one finding per fault, not a cascade ------------------------------------
# A rung written off as not needed has no material, box or exit test either.
# Each of those reported separately buries the finding that matters.
skipped=$(grep -c "walk-away-power" <<<"$out")
if [ "$skipped" -eq 1 ]; then
  ok "a needed:false rung reports once, not six times"
else
  bad "a needed:false rung should report once, got $skipped findings"
  note "$(grep "walk-away-power" <<<"$out")"
fi

# An entry with no video cannot also be faulted for having no segment of one.
urlless=$(grep -c 'material.video\[1\]' <<<"$out")
if [ "$urlless" -eq 1 ]; then
  ok "a video entry with no url reports once, not twice"
else
  bad "a urlless video entry should report once, got $urlless findings"
fi

# --- extra keys are the campaign's business; misspellings are not ------------
if grep -q "C007" <<<"$out" && grep -q "weak_1" <<<"$out"; then
  ok "a misspelled campaign.yml key is caught"
else
  bad "C007 should catch 'weak_1' as a misspelling of 'week_1'"
fi
if grep -q "unknown key 'notes'" <<<"$out"; then
  bad "an extra campaign.yml key should not be reported at all"
else
  ok "an extra campaign.yml key is left alone"
fi

# --- a missing PyYAML must exit 2 with usable advice, not a traceback ---------
stub="$(mktemp -d)"
printf 'raise ImportError("simulated: PyYAML not installed")\n' > "$stub/yaml.py"
dep_out=$(PYTHONPATH="$stub" python3 "$checker" "$here/fixtures/good" --today "$today" 2>&1)
dep_status=$?
rm -rf "$stub"
if [ "$dep_status" -eq 2 ]; then
  ok "a missing PyYAML exits 2, not 0 or 1"
else
  bad "a missing PyYAML should exit 2, got $dep_status"
  note "$dep_out"
fi
if grep -q "uv run" <<<"$dep_out" && ! grep -q "pipx run --spec" <<<"$dep_out"; then
  ok "the dependency message points somewhere that works"
else
  bad "the dependency message should name a command that can actually supply PyYAML"
  note "$dep_out"
fi

if [ "$fails" -eq 0 ]; then
  printf '\nall checks passed\n'
else
  printf '\n%d check(s) failed\n' "$fails"
fi
exit $(( fails > 0 ))
