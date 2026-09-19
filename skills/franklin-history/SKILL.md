---
name: franklin-history
description: "Analyze every Franklin-method campaign at once — mine the git logs, gates and fault grids for faults that recur across unrelated subjects, whether placement and acquisition are calibrated for this person, which drill forms actually work, and whether the cold delay is being honored. Use after two or more campaigns."
---

# Franklin — Cross-Campaign History

`franklin-review` looks **within** one campaign: what went wrong this week, what to drill next. This skill looks **across** all of them.

The question it answers is different in kind: *not* "what do I keep getting wrong about basket weaving" but **"what do I keep getting wrong, regardless of subject?"** A fault that shows up in an unrelated second campaign is not a fact about the subject. It is a fact about the learner, and it is the most valuable thing this whole apparatus produces.

**Invocation:** `/franklin-history` for the full report, or `/franklin-history <question>` for a targeted query ("am I actually honoring the cold delay?", "which drill form works for me?").

## Read-only, always

**Campaign home:** `$FRANKLIN_HOME` if that is set, otherwise `~/franklin`. Written `<home>` below.

This skill **never writes to a campaign repo**. It reads. Output goes to `<home>/history/<date>.md`. If `<home>/history/` is itself a git repo, commit there; otherwise just write the file. Campaign history is evidence — corrupting it to make a tidier report destroys the only asset here.

## Check the data first

Before analyzing anything, count: campaigns, completed cycles, total rebuild sessions, and calendar span.

**With fewer than 2 campaigns or fewer than ~20 rebuild sessions, say so up front and scale the claims down.** Report what the data shows, flag it as provisional, and name what would make it conclusive. This skill is one bad habit away from being a horoscope generator; the guard against that is stating n every time.

## Extraction

The commit messages written by `franklin-drill` and `franklin-review` are structured on purpose:

```
acquire: orientation
placement: <rung> — <zero|partial|solid>
acquire: <rung> — session N of <box>
gate: <rung> passed
drill: prep <id> (<sub-skill>)
drill: rebuild <id> — N faults (<top row>, <next row>)
review: week NN — <finding>
review: cycle N complete — <verdict against aim>
```

The first four are the acquisition half and they carry the dates that make section 2
computable: placement result, sessions spent per rung, and the gate date that ends the
block. **Campaigns predating these forms have `acquire:` commits at best and no
`placement:` at all** — treat those rungs as unmeasured rather than as well-placed, and
say how many of them there are before drawing any conclusion from section 2.

So, across every `<home>/*/`:

```bash
git -C "$d" log --pretty=format:'%ad|%H|%s' --date=format:'%Y-%m-%d %H:%M'
```

That gives dated, categorized sessions with fault rows and counts. Supplement with each campaign's `FAULTS.md` (the dot grids), `GATES.md` (placement results, time boxes, bypasses, passed dates), `acquire/notes/*.md` (what acquisition sessions actually produced), `CURRICULUM.md` (drill form and answer key per sub-skill), and `reviews/*.md` (the written findings). Prefer parsing to eyeballing — write a short script rather than reading forty files by hand.

## The seven analyses

Run these. Resist adding more; a report with twenty findings gets read as zero.

### 1. Faults that cross subjects — *the headline*

Normalize fault rows across campaigns (different campaigns will have named the same failure differently — "rushed the finish," "skipped the rim," "stopped before the last step" are one row). Then: which normalized faults appear in **two or more unrelated subjects?**

Those are trait-level. Lead the report with them, name them in plain language, and carry them into every future grid as permanent rows.

### 2. Did acquisition actually take? — *run this before trusting sections 3–7*

Acquisition sits upstream of everything below it. A rung whose gate was bypassed, or
passed on familiarity rather than understanding, produces inflated fault counts and a
drill-form slope that means nothing. **So establish this first and carry it as a
confound into the rest of the report** — the alternative is confidently reporting that
scramble doesn't work for this person when the truth is they drilled three rungs they
had never acquired.

Four things, all extractable:

**a. Placement calibration.** For every rung with a `placement` block: its `result` and
sized `time_box` against the sessions actually spent — the rung's `placement:` commit
plus its `acquire:` commits, up to `gate: <rung> passed`. **Count the `placement:`
commit**; the box includes that session, and leaving it out reads as a one-session
overrun on every rung in every campaign, which is the sort of constant bias this
analysis exists to find and would instead invent. Then the trait question — **does
this person get systematically mis-placed, and in which direction?**

- Boxes routinely overrun → placement reads them as further along than they are, and
  the quizzes are letting items pass they shouldn't.
- Gates routinely passed well inside the box → placement underestimates them, and the
  cost is boredom, which is how long campaigns die.
- A `solid` placement whose rung later produced noisy diffs → the quiz tested recall of
  material rather than the ability to *read an exemplar*, which is what the gate is
  for. That is a quiz-design fault and it will repeat until it is named.

Direction matters more than magnitude here: a consistent bias is fixable by changing
how the quizzes are written, and it is invisible inside any single campaign.

**b. Gates bypassed.** `GATES.md` `notes` record bypasses with dates. Cross-reference
each bypassed rung against its fault rows: **did those faults fall over the campaign,
or stay flat?** A single campaign's review can only ask this once; across campaigns it
becomes a real signal about whether this person's skipped gates cost them.

**c. Acquisition's share of the campaign.** Count `acquire:` and `placement:` commits
against `drill:` commits. Acquisition is exempt from the one-in-three source cap — it
is bounded by its exit test and time box instead — so the failure mode here is not a
ratio but a habit: **boxes that are set and then quietly extended.** Report the
overrun rate across campaigns, not the raw share.

**d. Did the non-text material get used?** Session notes list resources by modality.
If videos went unwatched across a whole cycle, stop shipping them; if the videos did
the work and the prose didn't, invert the emphasis in the next campaign. Be honest
that the repo evidence for this is weak unless a review recorded it — **prefer "no
signal" to a guess**, and say what would need logging to answer it properly.

Then apply the table-of-contents test retrospectively: sample `acquire/notes/` across
campaigns and ask whether each note explains mechanism or merely inventories what
exists. Consistently thin notes are not a learner fault — they mean the sessions were
being run as reading lists, and every gate they led to is suspect.

### 3. Which drill form actually works for this person

For each of reconstruction, constraint-transform, and scramble: did fault rates on the targeted sub-skill actually fall over the campaign? Compute the slope, don't eyeball it.

Franklin built three separate drills because he had three separate deficits. Over several campaigns you learn something he couldn't: which drill *you* convert into progress, and which one you merely perform. Say it directly, including when the answer is "reconstruction works, scramble has never once moved a number for you."

### 4. Is the cold delay real?

From the timestamps: actual `prep` → `rebuild` gap versus the `cold_until` each exemplar was assigned. Then the interesting part — **does a longer actual gap correlate with a lower fault count?**

This is directly measurable from the repo and it is the single mechanic most likely to be quietly hollowed out. If gaps are collapsing toward same-day, that is the finding, stated plainly.

### 5. Adherence shape

Commit timestamps give day-of-week and hour-of-day. Lapses give gap lengths and what immediately preceded them.

The purpose is **design, not shame.** Franklin ran four cycles the first year, then one a year, then none — and still carried the little book for the rest of his life. If the data says Tuesdays and Wednesdays never happen, the answer is a 5-day schedule, not a lecture. Report the real cadence and propose a plan that fits it.

### 6. Answer keys that never bit

For each sub-skill across all campaigns: did its answer key ever actually contradict the user?

**An answer key that never once said "no" is not an answer key.** List them. These are the places where a cycle's worth of self-deception accumulated unchallenged, and they are usually the sub-skills the user feels best about.

### 7. Aim hit rate

Cycle reviews record a verdict against the observable aim. Tally: hit, partial, missed. Then look for the pattern in the misses — were the missed aims vaguer at the outset? Longer ladders? More sub-skills? If aims that named a physical result get hit and aims that named "understanding" don't, that changes how the next campaign gets written.

## Optional: one chart

At most one — fault rate over time, campaigns overlaid. If producing it, load the `dataviz` skill before writing any chart code. Tables are the default; a second chart is almost always worse than no chart.

## Output

`<home>/history/<date>.md`:

1. **n** — campaigns, cycles, sessions, span. First line, every time.
2. **Trait-level faults** — the cross-subject recurrences, in plain language.
3. **The five other analyses**, one short section each, numbers before interpretation.
4. **What this changes** — concrete inputs for the next `/franklin` run: rows to carry over permanently, drill forms to favor or drop, a realistic time budget drawn from actual adherence, any answer key that needs replacing, **which direction placement quizzes should be corrected in, and which modalities to keep shipping.**

Then report back in chat with the headline finding and the single biggest change to make. One paragraph. The file has the rest.

## Rules

- **State n before every claim.** Six sessions is an anecdote.
- **Numbers before interpretation**, in every section. Let the user disagree with your reading without having to re-derive the data.
- **Distinguish "no signal" from "no effect."** Thin data usually means you can't tell yet. Say that instead of manufacturing a pattern.
- **Don't flatter.** The purpose of a multi-campaign history is to surface the durable failure the user has been routing around for a year. If the data shows the cold delay has been fiction since week three, that is the report.
- **Carry acquisition as a confound.** Where section 2 shows bypassed or thinly-passed gates, say so again in every section it contaminates rather than reporting those numbers straight.
- **Never edit a campaign repo** to make the analysis cleaner.