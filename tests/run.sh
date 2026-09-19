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
if out=$(python3 "$checker" "$here/fixtures/good" --today "$today" --strict --no-vcs-check 2>&1); then
  ok "good fixture passes --strict"
else
  bad "good fixture should pass --strict"
  note "$out"
fi

# --- the bad fixture must fail, and name each rule it breaks -----------------
out=$(python3 "$checker" "$here/fixtures/bad" --today "$today" --no-vcs-check 2>&1)
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
json_out=$(python3 "$checker" "$here/fixtures/bad" --today "$today" --no-vcs-check --json 2>/dev/null)
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

# --- a placement that ran is read, even where the gate was skipped -----------
# Collapsing a skipped rung's dependent fields must not swallow the recording
# error in the placement itself.
if grep -q "G014  GATES.md silence-handling" <<<"$out"; then
  ok "a skipped rung's placement is still validated"
else
  bad "a needed:false rung with an unevidenced placement should still report G014"
  note "$(grep "silence-handling" <<<"$out")"
fi

# --- a sub-skill matches as a whole word, not as a substring ----------------
# 'read' must not pass as the parallel 'reed-readiness' just because the prose
# says 'readiness'.
if grep -q "X001  exemplars/r02" <<<"$out"; then
  ok "a sub-skill that only appears as a substring still reports X001"
else
  bad "sub_skill 'read' should not match 'reed-readiness' in the prose"
fi

# --- a non-string YAML key is a finding, not a traceback --------------------
if grep -q "C008" <<<"$out"; then
  ok "a non-string campaign.yml key is reported"
else
  bad "a non-string campaign.yml key should report C008, not crash"
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
dep_out=$(PYTHONPATH="$stub" python3 "$checker" "$here/fixtures/good" --today "$today" --no-vcs-check 2>&1)
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

# --- one unreadable ladder is one finding, not one per exemplar --------------
broken_out=$(python3 "$checker" "$here/fixtures/broken-gates" --today "$today" --no-vcs-check 2>&1)
g002_count=$(grep -c "G002" <<<"$broken_out")
if [ "$g002_count" -eq 1 ]; then
  ok "an unparseable GATES.md reports G002 once"
else
  bad "an unparseable GATES.md should report G002 once, got $g002_count"
  note "$broken_out"
fi
if grep -q "X001" <<<"$broken_out"; then
  bad "exemplars should not each report X001 when the ladder could not be read"
  note "$broken_out"
else
  ok "no X001 cascade when the ladder could not be read"
fi

# --- an exemplar on a rung that needs no gate is not waiting on one -----------
if grep -q "exemplars/e04" <<<"$out"; then
  bad "X003/X004 should not fire where the rung is needed: false"
  note "$(grep "exemplars/e04" <<<"$out")"
else
  ok "no gate findings for an exemplar on a needed:false rung"
fi

# --- hostile values are findings, not tracebacks -----------------------------
if grep -q "G007  GATES.md rungs\[" <<<"$out" && grep -q "is not a name" <<<"$out"; then
  ok "an unhashable rung name is reported, not raised"
else
  bad "a non-string rung name should report G007"
fi
if grep -q "M009  exemplars/e03" <<<"$out"; then
  ok "a non-string sub_skill is reported, not raised"
else
  bad "a non-string sub_skill should report M009"
fi

# --- links stop going stale once the gate is behind you ----------------------
# The good fixture's rung 1 passed in 2026; its verified_on must not nag forever.
if python3 "$checker" "$here/fixtures/good" --today 2027-01-15 --strict --no-vcs-check >/dev/null 2>&1; then
  ok "a passed gate's links do not go stale"
else
  bad "G024/G025 should not fire on a rung whose gate has passed"
  note "$(python3 "$checker" "$here/fixtures/good" --today 2027-01-15 --no-vcs-check 2>&1)"
fi

# --- the git check names the repo that would be mined, not any ancestor ------
# Built here rather than read off the ambient checkout: asserting against
# "these fixtures happen to live inside a git repo" passes or fails on how the
# tree was obtained, and says nothing about the rule.
vcs_probe=$(mktemp -d)
git -C "$vcs_probe" init -q
mkdir -p "$vcs_probe/nested"
cp -R "$here/fixtures/good" "$vcs_probe/nested/tdd"
vcs_out=$(python3 "$checker" "$vcs_probe/nested/tdd" --today "$today" 2>&1)
if grep -q "R001" <<<"$vcs_out" && grep -q "neither this campaign nor its home" <<<"$vcs_out"; then
  ok "a campaign tracked by a distant repo reports R001"
else
  bad "R001 should fire when the nearest repo is neither the campaign nor its home"
  note "$vcs_out"
fi
# …and stops once the campaign is its own repo.
git -C "$vcs_probe/nested/tdd" init -q
if own_out=$(python3 "$checker" "$vcs_probe/nested/tdd" --today "$today" --strict 2>&1); then
  ok "a campaign that is its own repo does not report R001"
else
  bad "R001 should not fire once the campaign is a git repo"
  note "$own_out"
fi
rm -rf "$vcs_probe"

# --- --all discovers campaigns, not every folder under the home --------------
# franklin-history writes <home>/history/, which is not a campaign and must not
# make --all fail forever.
home_probe=$(mktemp -d)
cp -R "$here/fixtures/good" "$home_probe/tdd"
mkdir -p "$home_probe/history" && printf '# report\n' > "$home_probe/history/2026-09-20.md"
if all_out=$(python3 "$checker" --all --home "$home_probe" --today "$today" --strict --no-vcs-check 2>&1); then
  ok "--all skips the history folder"
else
  bad "--all should not report <home>/history/ as a broken campaign"
  note "$all_out"
fi
rm -rf "$home_probe"

# --- the plugin-root placeholder only substitutes when braced -----------------
# Claude Code rewrites `${CLAUDE_PLUGIN_ROOT}` in skill content and does not put the
# variable in the Bash tool's environment, so an unbraced `$CLAUDE_PLUGIN_ROOT`
# expands to nothing and the command silently runs against `/scripts/...`.
unbraced=$(grep -rn '\$CLAUDE_PLUGIN_ROOT' "$repo/skills" || true)
if [ -z "$unbraced" ]; then
  ok "every CLAUDE_PLUGIN_ROOT in skills/ is braced"
else
  bad "unbraced \$CLAUDE_PLUGIN_ROOT will not be substituted — use \${CLAUDE_PLUGIN_ROOT}"
  note "$unbraced"
fi

# --- the prose schema and the checker must describe the same thing -----------
if drift_out=$(python3 "$repo/tests/schema_drift.py" 2>&1); then
  ok "reference.md and check-campaign.py agree"
else
  bad "the prose schema and the checker have drifted"
  note "$drift_out"
fi

# --- the shipped version must be in the changelog ----------------------------
# A changelog nobody updates is worse than none: it reads as authoritative and
# is quietly wrong.
shipped=$(python3 -c 'import json;print(json.load(open("'"$repo"'/.claude-plugin/plugin.json"))["version"])')
if grep -q "^## ${shipped//./\\.} " "$repo/CHANGELOG.md"; then
  ok "CHANGELOG.md has an entry for $shipped"
else
  bad "CHANGELOG.md has no '## $shipped' entry for the shipped version"
fi

if [ "$fails" -eq 0 ]; then
  printf '\nall checks passed\n'
else
  printf '\n%d check(s) failed\n' "$fails"
fi
exit $(( fails > 0 ))
