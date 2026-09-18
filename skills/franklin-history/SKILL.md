---
name: franklin-history
description: "Analyze every Franklin-method campaign in ~/franklin at once — mine the git logs and fault grids for faults that recur across unrelated subjects, which drill forms actually work for this person, and whether the cold delay is being honored. Use after two or more campaigns."
---

# Franklin — Cross-Campaign History

`franklin-review` looks **within** one campaign: what went wrong this week, what to drill next. This skill looks **across** all of them.

The question it answers is different in kind: *not* "what do I keep getting wrong about basket weaving" but **"what do I keep getting wrong, regardless of subject?"** A fault that shows up in an unrelated second campaign is not a fact about the subject. It is a fact about the learner, and it is the most valuable thing this whole apparatus produces.

**Invocation:** `/franklin-history` for the full report, or `/franklin-history <question>` for a targeted query ("am I actually honoring the cold delay?", "which drill form works for me?").

## Read-only, always

This skill **never writes to a campaign repo**. It reads. Output goes to `~/franklin/history/<date>.md`. If `~/franklin/history/` is itself a git repo, commit there; otherwise just write the file. Campaign history is evidence — corrupting it to make a tidier report destroys the only asset here.

## Check the data first

Before analyzing anything, count: campaigns, completed cycles, total rebuild sessions, and calendar span.

**With fewer than 2 campaigns or fewer than ~20 rebuild sessions, say so up front and scale the claims down.** Report what the data shows, flag it as provisional, and name what would make it conclusive. This skill is one bad habit away from being a horoscope generator; the guard against that is stating n every time.

## Extraction

The commit messages written by `franklin-drill` and `franklin-review` are structured on purpose:

```
drill: prep <id> (<sub-skill>)
drill: rebuild <id> — N faults (<top row>, <next row>)
review: week NN — <finding>
review: cycle N complete — <verdict against aim>
```

So, across every `~/franklin/*/`:

```bash
git -C "$d" log --pretty=format:'%ad|%H|%s' --date=format:'%Y-%m-%d %H:%M'
```

That gives dated, categorized sessions with fault rows and counts. Supplement with each campaign's `FAULTS.md` (the dot grids), `CURRICULUM.md` (drill form and answer key per sub-skill), and `reviews/*.md` (the written findings). Prefer parsing to eyeballing — write a short script rather than reading forty files by hand.

## The six analyses

Run these. Resist adding more; a report with twenty findings gets read as zero.

### 1. Faults that cross subjects — *the headline*

Normalize fault rows across campaigns (different campaigns will have named the same failure differently — "rushed the finish," "skipped the rim," "stopped before the last step" are one row). Then: which normalized faults appear in **two or more unrelated subjects?**

Those are trait-level. Lead the report with them, name them in plain language, and carry them into every future grid as permanent rows.

### 2. Which drill form actually works for this person

For each of reconstruction, constraint-transform, and scramble: did fault rates on the targeted sub-skill actually fall over the campaign? Compute the slope, don't eyeball it.

Franklin built three separate drills because he had three separate deficits. Over several campaigns you learn something he couldn't: which drill *you* convert into progress, and which one you merely perform. Say it directly, including when the answer is "reconstruction works, scramble has never once moved a number for you."

### 3. Is the cold delay real?

From the timestamps: actual `prep` → `rebuild` gap versus the `cold_until` each exemplar was assigned. Then the interesting part — **does a longer actual gap correlate with a lower fault count?**

This is directly measurable from the repo and it is the single mechanic most likely to be quietly hollowed out. If gaps are collapsing toward same-day, that is the finding, stated plainly.

### 4. Adherence shape

Commit timestamps give day-of-week and hour-of-day. Lapses give gap lengths and what immediately preceded them.

The purpose is **design, not shame.** Franklin ran four cycles the first year, then one a year, then none — and still carried the little book for the rest of his life. If the data says Tuesdays and Wednesdays never happen, the answer is a 5-day schedule, not a lecture. Report the real cadence and propose a plan that fits it.

### 5. Answer keys that never bit

For each sub-skill across all campaigns: did its answer key ever actually contradict the user?

**An answer key that never once said "no" is not an answer key.** List them. These are the places where a cycle's worth of self-deception accumulated unchallenged, and they are usually the sub-skills the user feels best about.

### 6. Aim hit rate

Cycle reviews record a verdict against the observable aim. Tally: hit, partial, missed. Then look for the pattern in the misses — were the missed aims vaguer at the outset? Longer ladders? More sub-skills? If aims that named a physical result get hit and aims that named "understanding" don't, that changes how the next campaign gets written.

## Optional: one chart

At most one — fault rate over time, campaigns overlaid. If producing it, load the `dataviz` skill before writing any chart code. Tables are the default; a second chart is almost always worse than no chart.

## Output

`~/franklin/history/<date>.md`:

1. **n** — campaigns, cycles, sessions, span. First line, every time.
2. **Trait-level faults** — the cross-subject recurrences, in plain language.
3. **The five other analyses**, one short section each, numbers before interpretation.
4. **What this changes** — concrete inputs for the next `/franklin` run: rows to carry over permanently, drill forms to favor or drop, a realistic time budget drawn from actual adherence, and any answer key that needs replacing.

Then report back in chat with the headline finding and the single biggest change to make. One paragraph. The file has the rest.

## Rules

- **State n before every claim.** Six sessions is an anecdote.
- **Numbers before interpretation**, in every section. Let the user disagree with your reading without having to re-derive the data.
- **Distinguish "no signal" from "no effect."** Thin data usually means you can't tell yet. Say that instead of manufacturing a pattern.
- **Don't flatter.** The purpose of a multi-campaign history is to surface the durable failure the user has been routing around for a year. If the data shows the cold delay has been fiction since week three, that is the report.
- **Never edit a campaign repo** to make the analysis cleaner.