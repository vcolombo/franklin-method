# Campaign file schemas

The three machine-read files a campaign carries. `franklin` writes them at campaign
start; `franklin-drill` and `franklin-review` update them every session.

This file is the one prose source for their shape. `scripts/check-campaign.py`
enforces the same shape in code, and `tests/schema_drift.py` fails the suite if the
two stop agreeing — so a field added here without teaching the checker about it, or
the reverse, is caught rather than discovered later by a campaign that validates
against nothing.

---

## `campaign.yml`

The machine-readable header. How every skill knows what is live.

```yaml
subject: test-driven-development
status: active            # active | queued | complete | abandoned
aim: <the observable aim, one line>
week_1: 2026-09-21
blocked_on: null
planned_start: null
curriculum_is_draft: false
```

`subject`, `status` and `aim` are required. A campaign may carry its own extra keys —
a title, a cadence, the ladder repeated for convenience — and the checker leaves them
alone unless one looks like a misspelling of a key above.

---

## `GATES.md`

An ungated orientation block, then one block per rung. **`franklin-drill` reads this
before serving any drill.**

```yaml
orientation:
  covered: null           # null | YYYY-MM-DD
  must_cover:
    - "<what the subject is — the loop/process/form, concretely>"
    - "<the separable mechanisms it buys>"
    - "<the honest case against: weak evidence, bad fits, live disputes>"
    - "<the rungs mapped onto the thing>"
  held_back: "<the r-exemplar whose argument must NOT be paraphrased, and why>"

rungs:
- rung: assertions-and-fixtures
  needed: true
  placement:
    status: pending       # pending | done
    run_on: null          # YYYY-MM-DD
    result: null          # zero | partial | solid
    evidence: ""          # which items were missed, one line
  material:               # gathered and verified by franklin-drill when the block starts
    text:
      - url: <named page, not a site root>
        note: <what it covers>
    video:
      - url: <specific video>
        segment: <mm:ss-mm:ss>
        note: <what it covers>
      # or: none_found: "<why — searched, nothing usable exists>"
    interactive:
      - url: <tutorial with exercises, playground, kata, runnable repo>
    deeper:               # explicitly beyond the gate
      - url: <chapter, paper, long talk>
    verified_on: null     # YYYY-MM-DD the links were last checked to resolve
  time_box: "2-6 sessions, set by placement"
  exit_test:
    explain: "<the thing they must explain unaided>"
    exercise: "<the source's exercises, or a small build task with a runnable result>"
  passed: null            # null | YYYY-MM-DD
  notes: ""
```

Notes that are easy to get wrong:

- **`needed` is written `true` with placement pending, always.** A rung can turn out
  not to need its gate, but that is placement's call, not the interview's. On a
  `solid` result `franklin-drill` sets `passed` with the evidence recorded — it does
  not set `needed: false`.
- **`time_box` is a range until placement narrows it,** and it counts the placement
  session itself.
- **`material` needs two modalities.** Text and a video with a timestamped segment,
  or `none_found` with the reason a search turned nothing up. A single resource may
  be written as a lone mapping instead of a one-item list.
- **`verified_on` is set when the block starts,** by searching and checking the links
  resolve — never recalled.

---

## `exemplars/<id>/meta.yml`

One per exemplar.

```yaml
id: e01
kind: artifact              # artifact | reading | video
sub_skill: coil-tension
drill: reconstruction
source: <where it came from>
url: <if applicable>
segment: <timestamps, page or chapter range — for sources>
prepped: null
cold_until: null
status: awaiting-material   # awaiting-material | ready-to-prep | cold | rebuilt | diffed
```

- **`id` must match the directory name.**
- **`sub_skill` names a rung in `GATES.md`,** or a parallel judgment sub-skill scored
  in `PREDICTIONS.md` — the judgment rung has no gate and never appears under `rungs`.
- **`cold_until` is at least four days after `prepped`.** Rebuilding from fresh
  memory is transcription.
- **Nothing is prepped before its rung's gate has passed.** Compressing an exemplar
  to hints requires understanding it first.
