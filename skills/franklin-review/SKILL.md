---
name: franklin-review
description: "Run the weekly or end-of-cycle review for a Franklin-method learning campaign — read the fault log, find recurring failures, check the study-to-drill balance and prediction hit rate, revise the grid rows, and hand off to the next queued campaign. Use on Sundays or at cycle end."
---

# Franklin — Review

The drills generate data. This is where the data changes the plan. Without it the campaign is just repetition, and repetition without re-aiming is how people practice a mistake for thirteen weeks.

**Invocation:** `/franklin-review [subject]`

## Orient

List `~/franklin/*/` and read each `campaign.yml` to pick the campaign: the named subject, or the single `status: active` one. If several are active, ask. **Never review a queued campaign** — it has no data; say what it is blocked on instead.

Then read `FAULTS.md`, `SCHEDULE.md`, `CURRICULUM.md`, `PREDICTIONS.md` if present, every `rebuilds/*/diff-*.md` since the last review, and `git log --oneline` for the period. Decide which review this is:

- **Weekly** (default) — 45 minutes, adjusts next week.
- **Cycle** (week 13, or whenever the ladder is finished) — closes this campaign and starts the next.

---

## Weekly review

### 1. Tally, honestly

Dots per row for the week. Compare against the previous two weeks. Report the actual numbers before any interpretation — the trend is the finding, not your reading of it.

### 2. Answer the three questions in writing

Franklin's diff loop only pays if the gap gets named:

1. **What did the reconstructions lose this week?** Be specific and concrete.
2. **Is it the same loss as last week?** A fault appearing three weeks running is no longer a fault — it's the next drill's target.
3. **Where did they match or beat the original?** Log it. Real wins only.

### 3. Check the study-to-drill balance

Count the week's sessions: artifact preps and rebuilds (`e`) against source preps and rebuilds (`r`). The cap is roughly one source session in three.

**Sources current while drills slip is a campaign failing while feeling successful.** Consuming is comfortable and costs nothing; reconstructing is neither. If the ratio has drifted, say so directly and **cut sources, not drills** — that is the order, every time.

The reverse is worth naming too: drills grinding with no source in weeks usually shows up as mechanically clean rebuilds that miss the point of the material.

### 3b. Check placement against what actually happened

Only where an acquisition block ran this week. Read the rung's `placement.result` and
its `time_box`, then compare with the sessions it actually took to pass the gate.

- **Box overran** — placement read the user as further along than they were. Which
  items did the quiz let pass that it shouldn't have?
- **Gate passed well inside the box** — placement underestimated them, and the cost
  is boredom, which is how fourteen-week campaigns die.
- **A `solid` result that later produced noisy diffs** — the quiz tested recall of
  the material rather than the ability to *read an exemplar*, which is what the gate
  is actually for. That is a quiz-design fault, not a learner fault.

Name the miss and what the next rung's quiz should ask differently. Placement that is
never checked against outcomes is a guess wearing a score.

### 4. Check the prediction hit rate

If the campaign has a `PREDICTIONS.md`, count: hits, partials, blind misses, false alarms. Report the rate and the trend.

- **Rising** — the judgment sub-skill is coming. Say so; it's the hardest progress to feel.
- **Flat after three weeks** — the sources aren't reaching their hands. Change the drill, not the reading list.
- **Blind misses clustering on one cause** — that's a fault-grid row waiting to be named. Add it.
- **Log empty** — the answer key for that sub-skill has gone missing. Say it plainly; a sub-skill with no evidence is being taken on faith.

### 5. Handle the stuck row

Every campaign develops one row that is spotted every single day. Franklin's was Order: *"My scheme of Order gave me the most trouble... I made so little progress in amendment and had such frequent relapses, that I was almost ready to give up the attempt."* He never fixed it, and the system still worked.

**Do not respond to a stuck row with more willpower.** Shrink its scope until it is winnable this week, then widen it later. "Keep the workspace ordered" → "put the tools back in the box before standing up." If a row has been fully spotted for three weeks and shrinking hasn't moved it, say directly that it may be a structural constraint rather than a discipline problem, and ask whether the drill or the environment should change instead.

### 6. Revise the grid

The rows drafted at campaign start were guesses. Now there's evidence.

- A row never spotted in three weeks → **retire it** (it's not a real failure mode for this person).
- A recurring named loss with no row → **add it**.
- Keep it at 13 rows. If adding means cutting, cut the cheapest.

### 7. Set next week

Name the focus row, the sub-skill, the drill form, the exemplar to obtain, and whether a source is due. Check off the week in `SCHEDULE.md`. If the schedule has drifted from reality, **rewrite the schedule, not the history** — an aspirational plan nobody is following is worse than a corrected one.

### 8. Write and commit

`reviews/week-NN.md`, then `git commit -m "review: week NN — <the one finding>"`.

---

## Cycle review (week 13)

Everything above, plus:

### Did the aim get hit?

Go back to the observable aim in `README.md` and answer against the **answer key**, not against feeling. If the aim was "weave a watertight coiled basket unassisted," the question is whether a basket holds water. Say plainly if it doesn't.

### What did the ladder get wrong?

With hindsight, was the ordering right? Franklin's whole argument for French-before-Latin was that sequencing errors waste years. Name specifically which rung was placed too early or too late, and why.

### Which drills earned their time?

Per sub-skill: did the fault rate actually fall? A drill with a flat fault curve over 13 weeks is either mis-targeted or its answer key isn't biting. Kill it or rebuild it — don't carry it forward out of tidiness.

### Which sources earned their time?

Per source: did drilling it change anything downstream — a fault rate, a prediction hit rate, a diff that got sharper afterwards? A source that was pleasant and changed nothing is a source to drop. Be specific about which ones those were; "it was all useful" is the answer that keeps a bloated reading list alive for another cycle.

### Did acquisition actually acquire?

Per rung with a gate: read the session notes in `acquire/notes/`. Two questions,
neither of them about effort.

- **Could any note have been assembled from the source's table of contents?** If so
  that session taught what exists rather than how it works, and the gate passed on
  familiarity rather than understanding. Expect it to show up downstream as rebuilds
  that reproduce shape without mechanism.
- **Did the user actually use the non-text resources?** If every video went unwatched
  across a whole cycle, stop shipping them and say so; if the videos did the work and
  the prose didn't, invert the emphasis next cycle. Either finding is worth more than
  continuing to offer both out of even-handedness.

### Check the answer keys held

For each sub-skill, did the answer key actually contradict the user at some point? **An answer key that never once said "no" is not an answer key.** Flag those; they're where self-deception accumulated over the cycle.

### The Junto obligation

Week 12 was a presentation to a real audience. If it happened, fold the outside criticism in — outside readers see what self-review structurally cannot. Franklin only added Humility to his list of virtues because a Quaker friend told him flatly that he was proud.

If it didn't happen, say so, and make it week 1 of the next cycle rather than week 12.

### Close this campaign, then hand off

Set `status: complete` in this campaign's `campaign.yml` and commit.

Then check whether another campaign has `blocked_on: <this subject>`. **If one is queued, the handoff is the most valuable half of this review** — that curriculum was written before any evidence existed and says so. Go and revise it now, with what the cycle just produced:

- **Carry the fault rows that proved real**, especially the cross-cutting ones. Replace the ones that were never spotted — they were borrowed from Franklin, not observed in this person.
- **Drop the drill forms that didn't move a number.** If scramble never shifted the fault rate here, do not schedule a scramble there.
- **Rewrite its schedule against the real cadence**, read from `git log`, not the one the plan assumed.
- **Re-verify its sources are still reachable.** They were checked months ago.
- Then set its `status` to `active`, `curriculum_is_draft` to `false`, remove the README status banner, and commit.

If nothing is queued, hand back to `franklin` for a fresh campaign: new aim, revised ladder, carried-over rows, retired drills, the sources worth keeping.

`git commit -m "review: cycle N complete — <verdict against aim>"`

---

## Tone

The review is the one place in this system where flattery does real damage — it corrupts the data the next thirteen weeks are planned from. Give the numbers, name the stuck row, and say when the aim wasn't hit. Then note the genuine wins, which after a full cycle of honest tallying are usually larger than the user expects.