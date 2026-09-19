# The Franklin Method

Four Claude skills that turn *any* subject into a 13-week self-teaching campaign, using the loop Benjamin Franklin invented to teach himself prose — and the mode he used for everything else.

No teacher. No grading by an LLM. Every check in the system is external: a test that runs, a basket that holds water, an original text you diff against, a prediction that reality settles.

---

## The idea

Franklin taught himself writing, arithmetic, four languages, and enough natural philosophy to do original work in electricity — while working a full-time trade. His *Autobiography* records the methods, and they are unusually specific.

The famous one is the *Spectator* drill:

> "I took some of the papers, and, making short hints of the sentiment in each sentence, laid them by a few days, and then, without looking at the book, tried to complete the papers again... Then I compared my 'Spectator' with the original, discovered some of my faults, and corrected them."

Compress to hints → let it go cold → rebuild blind → **diff**. The gap between your version and the original is the lesson.

### The two modes

Franklin worked in two modes, and conflating them is the single most common way to misapply him:

| Mode | What it does | His example |
|---|---|---|
| **Acquisition** | Gets material into your head the first time | Cocker's arithmetic — *"went through the whole by myself with great ease."* Locke, the Port-Royal Logic, Xenophon. French, then Italian, then Spanish. |
| **Refinement** | Sharpens craft on material you already comprehend | The *Spectator* drill |

The reconstruct-and-diff loop is **refinement only**. When Franklin ran it he already read English fluently — what he lacked was "elegance of expression, method, and perspicuity," in his father's words. He was not learning the language.

**Reconstructing material you have not acquired is reconstructing a Spectator essay in a language you cannot read.** So every rung of a campaign gets acquisition first, gated by an exit test, then drills. This distinction is enforced in the skills, not just documented here.

### Acquisition is measured, not assumed

A gate sized by guesswork fails in both directions: assume zero and an experienced
user is bored out of a fourteen-week campaign; assume competence and a beginner is
stranded in drills whose diff is noise. So acquisition runs in three phases.

**Placement** happens per rung, immediately before that rung's block — a short quiz
scored against a key written *before* the user answers. A `solid` result passes the
gate on the spot and saves the sessions; `partial` narrows the material to the named
gaps. Self-report sizes the calendar, never the gate.

**Orientation** happens once, before rung 1: what the subject is, the separable
mechanisms it buys, **the honest case against it**, and how the rungs map onto it. A
learner who can execute the mechanics but cannot say what they are for drops the
campaign around week 5, and is right to. Where a source exemplar argues for the
subject, orientation deliberately does not paraphrase it — reconstructing it later
requires recall, not recognition.

**Acquisition sessions** teach mechanism rather than inventory, against one test:
*if the session's output could have been assembled from the source's table of
contents, it was not acquisition.* Each one writes a committed note, and each note
carries verified external resources in **at least two modalities** — canonical text
and a video with a timestamped segment — because people do not all learn by reading.
Links are searched and checked to resolve when the block starts, never recalled.

---

## The four skills

| Skill | Cadence | What it does |
|---|---|---|
| **`franklin`** | Once per subject | Interviews the goal, decomposes it into independently-failing sub-skills, assigns each a real answer key, writes an orientation block and a placement-sized acquisition gate per rung, orders the ladder easiest-first, and writes a git repo |
| **`franklin-drill`** | Daily, 20 min | Three modes: **acquire** (place the learner, orient, work the material, pass the exit test), **prep** (compress an exemplar to hints, set the cold delay), **rebuild** (hints only, blind reconstruction, then the diff) |
| **`franklin-review`** | Weekly + at cycle end | Checks the campaign against the schema, tallies the fault grid, finds recurring losses, checks study-to-drill balance and prediction hit rate, revises the rows, and hands off to the next queued campaign |
| **`franklin-history`** | After 2+ campaigns | Mines the git logs across every campaign for faults that recur across *unrelated* subjects — those are facts about the learner, not the subject |

They chain:

```
/franklin I want to learn X
        │
        ├─> designs the campaign, writes ~/franklin/x/, git init
        │
        ▼
/franklin-drill x          (daily)
   acquire ──> [exit test] ──> prep e01 ──┐
                              prep e02 ──┼── 4+ days cold ──> rebuild ──> diff ──> log fault
                              prep e03 ──┘
        │
        ▼
/franklin-review x         (Sundays; and week 13)
        │
        ▼
/franklin-history          (once two campaigns exist)
```

---

## What a campaign looks like on disk

```
~/franklin/<subject>/
  campaign.yml       # status: active | queued | complete — how the skills know what's live
  README.md          # aim, ladder, the two modes, what "cold" forbids
  CURRICULUM.md      # per rung: acquisition gate, exit test, drill form, answer key
  SCHEDULE.md        # weeks, orientation and acquisition blocks marked
  GATES.md           # orientation, placement, material by modality, exit tests, passed dates
  acquire/notes/     # one committed note per acquisition session, with resources
  FAULTS.md          # a 13-row grid, one dot per fault, one focus row per week
  PREDICTIONS.md     # the resolving-prediction log for the judgment rung
  exemplars/<id>/    # original.md, hints.md, meta.yml (cold_until lives here)
  rebuilds/<id>/     # attempt-NN.md, diff-NN.md
  reviews/           # week-NN.md
```

One commit per session. `git log` becomes a queryable history of what keeps going wrong — which is what `franklin-history` reads.

---

## The rules that make it work

**Every sub-skill needs an answer key that isn't an opinion.** Valid kinds: the original artifact, a physical result, an executable check, an expert's version revealed after yours is committed, or a resolving prediction. A sub-skill that can only be checked by "reflecting on it" is not drillable — it gets converted or cut. This is the constraint that keeps the method honest, and it applies to Claude too: **Claude never grades the work.**

**Check what that gate just dropped.** Applied carelessly, the answer-key rule selects for whatever is mechanically checkable and silently discards the judgment at the centre of the subject — hearing what a hard-to-write test is telling you, feeling when the clay is wrong. That judgment *is* drillable: predict in writing before acting, then score it hit / partial / blind miss / false alarm. **Blind misses are the signal** — they name the cues you can't yet read.

**The cold delay is the method, not overhead.** Four days minimum. Rebuilding from fresh memory is transcription, and transcription teaches nothing. The skill refuses to serve a cold exemplar early.

**Claude never writes the rebuild.** It preps, enforces the delay, and diffs — quoting both sides, capping findings at five, ranked by cost. It never rewrites your attempt into the original, because a corrected version you didn't produce teaches nothing and steals the next attempt.

**Sources are drilled, not consumed.** Reading and video enter as exemplars — reconstruct the argument, diff claim by claim — and are capped at one session in three. Consuming feels like progress and costs nothing; a campaign where every source is current and every drill is behind has failed while feeling successful.

**Reference docs are banned from drilling and ideal for acquisition.** The media are opposite because the modes are opposite.

**One active campaign.** Twenty minutes is what survives a working week. Two campaigns is forty, and loses both. A second campaign is designed fully and marked `queued`.

**Lapsing is part of the method.** Franklin went from four cycles a year to one, then to none, and still carried the little book for life. The skills restart cold with no penance and never open a session with a guilt tally.

---

## A worked example

From a real campaign — *"learn TDD, coming from barely testing at all."*

- **Aim (observable):** ship a real feature test-first, from empty file to merged PR, without reaching for the debugger.
- **Ladder:** assertions & fixtures → test-first inversion → next-test decomposition → refactor under green → seams & test doubles, with **design feedback** running in parallel and scored as predictions.
- **Acquisition gate, rung 1:** pytest docs, 8 sessions. Exit test — explain what a fixture is and when it runs, unaided; then write a parametrized suite from scratch that passes **and goes red when you deliberately break the function.** A suite that stays green is the real exam.
- **Drill, rung 1:** reconstruct a reference test suite from intent-hints. Answer key: the same mutation check.
- **Judgment rung:** before each test, predict in writing whether it will be awkward to write and why. Score it. Rising hit rate is the evidence.
- **Week 12 Junto:** a real PR at work, test-first commit history intact, one named colleague asked to review *the test sequence* — "where did I take too big a step?"

---

## Install

This repo is both a plugin and its own marketplace, so it installs in two commands:

```
/plugin marketplace add vcolombo/franklin-method
/plugin install franklin-method@franklin-method
```

Or copy the skills in by hand:

```bash
git clone https://github.com/vcolombo/franklin-method.git
cp -r franklin-method/skills/franklin* ~/.claude/skills/
```

Then start a campaign:

```
/franklin I want to learn underwater basket weaving
```

The campaign repo defaults to `~/franklin/<subject>/`. Set `$FRANKLIN_HOME` to keep
them somewhere else — all four skills and the checker read it. Pick one home and stay
there: two copies on two machines diverge, and the git log stops being trustworthy.

### Repo layout

```
.claude-plugin/
  plugin.json          # plugin manifest
  marketplace.json     # marketplace manifest — source "./" (plugin is the repo root)
skills/
  franklin/SKILL.md
  franklin-drill/SKILL.md
  franklin-review/SKILL.md
  franklin-history/SKILL.md
scripts/
  check-campaign.py    # the campaign schema, as a script
tests/
  run.sh               # fixture suite for the checker
  fixtures/{good,bad}/ # one campaign that follows the schema, one that breaks it
.github/workflows/
  validate.yml         # manifests + skills + the fixture suite, on every push
```

Validate before publishing a change:

```bash
claude plugin validate . --strict      # manifests
claude plugin validate ./skills --strict
```

With a `marketplace.json` present, `claude plugin validate .` validates the
marketplace manifest **and recurses into every plugin it lists**, so both manifests
are covered by the one command — errors in `plugin.json` are reported as
`plugins[0] plugin.json → …`. Point it at a directory with no marketplace manifest
and it validates the plugin manifest alone. `--strict` promotes warnings (unknown
fields, missing metadata) to failures, which is what CI runs.

## Checking a campaign

The rules above are prose, and prose gates get talked past — in one real session a
rung's gate was passed on a self-reported "essentially none", which is precisely the
input placement exists to refuse. So the schema is also a script:

```bash
scripts/check-campaign.py ~/franklin/tdd     # one campaign
scripts/check-campaign.py --all              # every campaign under the home
scripts/check-campaign.py --all --strict     # warnings count as failures
scripts/check-campaign.py ~/franklin/tdd --json
```

It reads `campaign.yml`, `GATES.md` and every `exemplars/*/meta.yml`, and reports
where the campaign has drifted from what `franklin-drill` expects to find. Exit 0
clean, 1 findings, 2 couldn't run.

It needs PyYAML. The file carries a [PEP 723](https://peps.python.org/pep-0723/)
header, so `uv` supplies it without installing anything:

```bash
uv run scripts/check-campaign.py ~/franklin/tdd
```

Otherwise `python3 -m pip install --user pyyaml` once. (PyYAML is a library with no
entry point, so `pipx run` cannot supply it.)

`--all` looks in `~/franklin` unless `$FRANKLIN_HOME` or `--home` says otherwise —
the same home the skills use. It treats a directory as a campaign only if it holds a
`campaign.yml` or a `GATES.md`, so `franklin-history`'s `history/` folder is passed
over rather than reported as a campaign missing everything. A path you name
explicitly is always checked in full: there you have asserted it is a campaign, and a
missing `campaign.yml` is the finding.

`--no-vcs-check` skips the git check, for a campaign you have not `git init`ed yet.

`franklin-review` runs this as its step 0, so Sunday's review opens with the schema
findings rather than depending on someone remembering to look.

The findings it exists for:

| Code | What it catches |
|---|---|
| `G016` | a gate marked passed while its placement is still `pending` — the self-report bypass |
| `G014` | a `partial` or `solid` placement whose `evidence` names no missed items |
| `G010` | a rung with no `placement` block at all — an older campaign, unmeasured rather than well-placed |
| `G021` `G022` | one modality only, or a video with no timestamped segment |
| `G024` `G025` | links never verified, or verified over 45 days ago |
| `G017` | a `time_box` still a range after placement ran |
| `M007` | a cold delay under four days |
| `X002` | an exemplar prepped before its rung's gate opened |
| `X003` `X004` | an exemplar that ripens — or has already ripened — while its gate is still shut, and is going stale where it sits |
| `R001` | a campaign whose nearest git repo is neither itself nor its home — `franklin-history` would mine that repo's log instead |

Run it before a Sunday review, and after any hand-edit of a campaign file. It is a
schema check, not a judgement: it will not tell you whether the campaign is teaching
you anything.

## Provenance

Built from Benjamin Franklin's *Autobiography* (O. Leon Reid edition, [Project Gutenberg #36151](https://www.gutenberg.org/ebooks/36151)). Every quotation in the skills was verified verbatim against that text.

The specific practices the skills encode:

- **The Spectator drill** — hints, cold delay, blind rebuild, diff
- **Prose → verse → prose** — a constraint transform, invented to force the exact deficit he'd diagnosed (a thin vocabulary)
- **Scrambled hints** — *"This was to teach me method in the arrangement of thoughts."*
- **The thirteen virtues and the little book** — one focus row per week, a dot per fault, four cycles a year
- **The Junto** — a club with enforced norms, including a cash fine for expressing positiveness or flatly contradicting someone
- **French before Latin** — *"if you begin with the lowest you will with more ease ascend to the top"*

And the failure modes, which he documented as honestly as the successes: he never fixed Order, tapered his cycles to nothing, and only added Humility because a friend told him plainly that he was proud.

---

## Known gaps

- **Campaigns started before the placement changes have no `placement` blocks**, so `franklin-history`'s acquisition analysis reads those rungs as unmeasured rather than well-placed. It says so before drawing conclusions, but the calibration finding needs a campaign or two run under the new shape before it means anything.
- **No campaign has completed a full cycle yet.** Everything here is designed rather than validated. The cycle review is built to revise itself from real fault data, and should be trusted over the original plan.
- **Blind-tested on four subjects** (TDD, pottery, negotiation, FPGA), by running the skills in fresh contexts and grading the output. That catches design errors, not whether the method teaches anyone anything.

## License

MIT
