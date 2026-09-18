---
name: franklin-drill
description: "Run one session of a Franklin-method campaign — place the learner and acquire a rung's material against its gate, prep an exemplar into hints, or diff a blind rebuild against the original. Use for daily practice in an existing ~/franklin campaign."
---

# Franklin — Run a Session

The daily driver for a campaign created by `franklin`. Twenty minutes. **Three modes.**

**Invocation:** `/franklin-drill [subject]`

| Mode | When | What happens |
|---|---|---|
| **Mode 0 — Acquire** | The current rung's gate in `GATES.md` is not passed | Place, orient, work the material, run the exit test |
| **Mode A — Prep** | Gate passed, nothing ripe | Compress an exemplar to hints, set the cold delay |
| **Mode B — Rebuild** | Gate passed, something ripe | Hints only, blind rebuild, diff, log faults |

Mode 0 runs in three phases: **0a placement** (measure where they actually stand, per rung — never assume zero, never assume competence), **0b orientation** (once, before rung 1: what the subject is and why, including the honest case against), **0c acquisition sessions** ending in the exit test.

Modes A and B are **refinement** — they sharpen craft on material already understood. Mode 0 is **acquisition**. Running A or B on unacquired material is asking someone to reconstruct an essay in a language they cannot read: the diff is meaningless, the session is miserable, and the user reasonably concludes the method is broken.

## Pick the campaign first

List `~/franklin/*/` and read each `campaign.yml`.

- **Subject named** → use it. If `status: queued`, **do not run a session.** Say what it is blocked on and its planned start, and offer the active campaign instead.
- **No subject named, exactly one `status: active`** → use that one.
- **No subject named, several active** → ask which. A session logged against the wrong campaign corrupts two fault grids at once.
- **No `campaign.yml`** → older campaign. Treat a lone directory as active and write one as part of this session.

**Never serve a session from a queued campaign**, even if asked.

## Orient

Read `campaign.yml`, `README.md`, `SCHEDULE.md`, **`GATES.md`**, and every `exemplars/*/meta.yml`. Then, in order:

1. **Orientation check.** `GATES.md` has an `orientation` block with `covered: null` → **Mode 0b**, before anything else in the campaign. Mechanics with no answer to "what is this and why" lose the user around week 5.
2. **Gate check.** Find the rung this week's schedule is on. If its `GATES.md` entry has `needed: true` and `passed: null` → **Mode 0**. Nothing else runs until that gate is passed.
   - That rung's `placement.status: pending` → **Mode 0a** this session. Do not start on material before the starting point is measured.
   - Older campaign with no `placement` block at all → treat it as pending and add the block as part of the session.
3. Any exemplar `status: cold` with `cold_until` **today or earlier** → **Mode B**. Ripe exemplars go stale.
4. Otherwise → **Mode A**.
5. Fewer than 2 exemplars in flight → **Mode A**, even with something queued behind it.
6. **Ratio guard:** if sources (`r`) are running ahead of artifacts (`e`) — more than a third of recent sessions, or an `r` prepped while an `e` sits unprepped — prep the artifact and say why.
7. If everything is cold but not ripe, say which ripens first and when, then prep. **Never serve a cold exemplar early**, even if asked.

**The gate is not advisory.** If the user asks to skip ahead to drilling, say once, in a line, that the diff will be noise without the material — then respect their call if they insist, and record the bypass in that gate's `notes` so the review can see it.

---

## Mode 0 — Acquire

**Open by naming the mode.** "This rung needs its material first — we're acquiring, not drilling, for about four sessions." A user who expects a drill and gets a reading list assumes something went wrong.

Mode 0 has three phases, in order: **placement**, then **orientation** (campaign start only), then **acquisition sessions** ending in the exit test.

---

### 0a — Placement, before the first acquisition session of a rung

The rung's `placement.status` is `pending` → this session is placement. It runs
**per rung, when that rung's block starts** — never once for the whole campaign, and
never from a self-report.

**Never assume a starting point.** Assuming zero bores an experienced user out of a
fourteen-week campaign; assuming competence strands a beginner in drills whose diff
is noise. Both read to the user as the method being broken.

1. **Write the key first.** Before showing the user anything, write down what a
   correct answer to each question contains. A quiz scored against a key written
   afterward is scored against the answers received, which measures nothing.
2. **Ask 5–8 questions, cold, in one batch**, ordered easy → hard, specific to this
   rung. Good items have a *right answer* the user either has or hasn't got — "what
   does this code print", "what would you check first when X", "name the difference
   between A and B". Bad items are "how comfortable are you with X" and anything
   answerable by vibes.
   - Include at least one item that a confident non-expert typically gets wrong. The
     gap between claimed and actual level is the thing being measured.
   - **No looking anything up. No hints while they answer.** If they ask for one,
     say why not in a line and wait.
3. **Score it against the key and say the result plainly**, item by item, without
   softening. Then classify:

   | Result | Means | What happens |
   |---|---|---|
   | **zero** | little or nothing lands | full time box, start from first principles |
   | **partial** | some items solid, named gaps | box narrowed; material scoped to the gaps, and say which items are being skipped and why |
   | **solid** | the rung's material is already in hand | **mark the gate passed on the spot**, record the evidence, and go to Mode A |

4. **Record it** in `GATES.md`: `placement.status: done`, `run_on`, `result`,
   `evidence` naming the missed items in one line. Narrow `time_box` from its range
   to a number.

   **This session counts against that number.** Placement is a session spent — a box
   narrowed to three means two acquisition sessions remain, and the user should be
   told which it is. A box that quietly excludes placement runs one session long on
   every rung, and the overrun then gets misread as placement having mis-sized it.
   (A `solid` result is the one case where the accounting barely matters: the session
   is still spent, but the gate is passed and the rest of the box goes back to the
   calendar.)
5. **Commit:** `placement: <rung> — <result>`.

A `solid` result is a real outcome, not a failure of the campaign design. Say so and
move on — the user just saved four sessions, and the evidence is in the file if the
review wants to argue with it.

---

### 0b — Orientation, once, before rung 1

`GATES.md` has an `orientation` block with `covered: null` → this session is
orientation, and it comes **before rung 1's placement**.

It is ungated and has no exit test. It covers what the `must_cover` list names: what
the subject *is*, the separable mechanisms it buys, **the honest case against it**,
and how the rungs map onto it. A learner who can execute the mechanics but cannot say
what they are for drops the campaign around week 5, and is right to.

**Respect `held_back`.** If a source exemplar argues for the subject, do not
paraphrase its argument, its ordering, or the misreadings it names — reconstructing it
later requires recall, and a summary now converts that into recognition. Orient from
the field's common ground and **say out loud which text is being held back and why**;
the user seeing the discipline applied to their own campaign is worth more than the
paragraph it costs.

Set `covered: <today>`. **Commit:** `acquire: orientation`.

---

### 0c — Acquisition sessions

1. **Work the material**, in the order `GATES.md` lists it, scoped by the placement
   result. Claude can explain, answer questions, and work examples alongside them
   here — this is the one mode where that helps rather than steals the learning.
2. **Teach the mechanism, not the surface.** The test:

   > **If the session's output could have been assembled from the source's table of
   > contents, it was not acquisition.**

   A list of what exists is a reference sheet; the user can get that from the docs
   index in less time than the session took. Acquisition explains **how the thing
   works underneath, why it was built that way, and what goes wrong when it is
   misunderstood** — with worked examples, and with the failure modes named. Where a
   mechanism explains a fault-grid row, say which row and why.
3. **Every session produces a written note** at `acquire/notes/session-NN.md`,
   committed. Not a summary of what was said — the material itself, at mechanism
   level, so it is re-readable in week 12 without re-watching anything. It ends with
   the hands-on for that session and the resources below.
4. **Every session note carries external resources, in at least two modalities.**
   People do not all learn the same way, and a session that ships only prose fails
   the half of users who need to watch someone do it.
   - **Canonical text** — named pages, never a site root.
   - **A video with a timestamped segment** — a specific talk, screencast, or
     demonstration, not a channel or playlist. For anything with tacit motion this is
     the *primary* resource, not a supplement. If none exists, say so; the absence is
     information.
   - **Interactive where it exists** — a playground, kata, or runnable repo.
   - **One deeper dive, flagged explicitly as beyond the gate**, so curiosity has
     somewhere to go without inflating the time box.

   **Search for these; never recall them.** Verify each link resolves before writing
   it down — a dead link destroys confidence in the whole plan — and update
   `material.verified_on`. Note anything paywalled, borrow-only, or account-gated.
5. **Track sessions against the time box**, counting the placement session as the first one against it. If the box is spent and the exit test isn't close, say so plainly: either the material is wrong for them, or the rung is too big. Both are findings. Do not silently extend. If placement said `zero` and the box was set for `partial`, that is a placement miss — record it, because the review looks for that pattern.
6. **Run the exit test** once the material is covered:
   - **Explain it unaided.** They write the explanation from memory, sources closed. Claude checks it against the material and **names what is missing or wrong rather than grading it warmly.** Vague means not landed.
   - **Pass the exercises.** The source's own, or the substitute build task. **The result must run, compile, hold water, or otherwise be externally checkable.** If the only available check is Claude's opinion, the exit test is broken — say so and find a real one.
7. **Record it.** Set `passed: <today>` in `GATES.md`, or leave it null and note what is still missing.
8. **Commit:** `acquire: <rung> — session N of <box>`, or `gate: <rung> passed`.
9. **Close by naming what unlocks.** "Gate passed — tomorrow we prep the first exemplar, first rebuild Monday."

**Do not let acquisition drift into drilling.** No cold delays, no hints, no fault logging in Mode 0. Different mode, different rules.

---

## Mode A — Prep an exemplar

**Open by saying why this is a prep session** — "nothing ripens until Sunday, so today we prep" — and what ripens when. A user who thinks prep is filler will quietly stop showing up on prep days.

1. **Get the exemplar.** The user supplies it. If they haven't, name what's needed for this rung and stop — don't substitute something easier.
2. **Store the original** at `exemplars/<id>/original.md`. For non-text, the link/photo path plus a factual description. Keep it out of their way until the diff.
3. **Compress to hints.** One terse hint per unit of meaning — per sentence for prose, per technique step for a craft, per component for a system. Hints are *pointers, not summaries*. If a hint could be expanded into the original almost verbatim, it's too fat. Write to `hints.md`.
4. **Set the delay.** `cold_until` = today + 4 days minimum, 7 for dense material.
5. **Commit:** `drill: prep <id> (<rung>)`.
6. **Close with the next two sessions**, not just this one.

**If the hints are hard to write — if the material's parts don't yet mean anything to the user — that is a gate failure surfacing late.** Say so, stop, and send that rung back to Mode 0. It is far cheaper than a meaningless rebuild.

### Prepping a source (reading or video)

Same loop, different unit of meaning. An argument decomposes into **claims**, not sentences.

- **Hints are the claim skeleton**: what the author asserts, in what order, what each claim rests on. Not their phrasing.
- **Scope to one session.** A chapter, an essay, a 10–15 minute segment. Record the range as `segment`.
- **Video:** note timestamps. If a transcript exists, store it as `original.md` so the diff can quote both sides; if not, say plainly that a diff against memory is weaker.
- **Demonstration video** is procedure, not argument: hints are the steps and decision points — especially what the expert does when something goes wrong.

---

## What "cold" forbids — and what it doesn't

Users routinely over-read this and stop studying entirely. The prohibition is narrow:

- **Forbidden:** re-reading or re-watching *the specific exemplar under cold* before rebuilding it. That converts recall into recognition.
- **Fine, and encouraged:** reading around the subject, docs, other people's work, adjacent material, throwaway practice. Franklin read constantly while drilling — he simply never re-read the paper he was about to reconstruct.

State this plainly the first time a delay is set.

---

## Mode B — Rebuild and diff

1. **Hand over the hints only.** Never the original. No looking anything up, no notes, one pass.
2. **They rebuild.** Claude does not draft it, suggest phrasing mid-attempt, or "help get started." The reconstruction *is* the learning. If they ask Claude to draft it, say why not, in one line, and wait.
3. **Store the attempt** at `rebuilds/<id>/attempt-NN.md`.
4. **Diff it.** This is where Claude earns its place.

### How to diff

Name **specific, categorized losses**. For each:

- **Quote both sides**, verbatim. For physical work, point at the region of each photo.
- **Name the category** — a fault-grid row, or a new candidate row.
- **Say what it cost.** Not "less elegant" — *"the original's transition carries the reader from cause to consequence; yours restates the cause, so the paragraph stalls."*

Then, separately and honestly:

- **Where they matched or beat the original.** Franklin logged these deliberately — *"I sometimes had the pleasure of fancying that in certain particulars of small import I had been lucky enough to improve the method or the language, and this encouraged me."* Don't manufacture it; don't omit it when real.

**If the rebuild is mostly blank or wildly off**, that is usually not a fault-grid finding — it is the gate having been passed too early or bypassed. Say so instead of logging thirteen faults, and send that rung back to Mode 0.

### Diffing an argument

For a source exemplar the losses have their own shapes:

- **Claims dropped** — which assertions vanished, and was it load-bearing?
- **Claims reversed or softened** — the author said X causes Y; the rebuild says they're related.
- **Support detached** — the claim survived, the reason didn't. Most common and most costly.
- **Misreadings the author explicitly named** — if the piece warns against a misunderstanding and the rebuild reproduces it, that is the single most valuable finding. Lead with it.
- **Order** — wrong sequence usually means the dependency between claims wasn't understood.

### Hard rules for the diff

- **Never rewrite their attempt into the original.** Name the loss and stop.
- **Rank by cost, not by count.** Three structural losses beat fifteen word choices.
- **Cap it at five.** The rest goes in the log for pattern-finding.
- **Don't soften.** Franklin's reaction to honest tallying: *"I was surprised to find myself so much fuller of faults than I had imagined; but I had the satisfaction of seeing them diminish."* Both halves depend on the tally being accurate.

5. **Log it.** Append to `FAULTS.md`: date, exemplar id, one dot per fault against its row, one line per fault.
6. **Write** `rebuilds/<id>/diff-NN.md`.
7. **Commit:** `drill: rebuild <id> — N faults (<top row>, <next row>)`.
8. **Check what's next.** Fewer than 2 in flight → say tomorrow is a prep and name the material to have ready. **Next rung's gate unpassed → say the next block is acquisition**, so it isn't a surprise.

---

## The prediction log

If the campaign has a `PREDICTIONS.md`, it runs continuously — not only on drill days. Remind them once a week, not every session: predict in writing, act, score it hit / partial / blind miss / false alarm. **Blind misses are the valuable entries.** Never score it for them.

---

## Session end

One short message: the top two losses (or, in Mode 0, what the exit test still needs), the one thing to carry into tomorrow, and **what tomorrow's session will be** — acquire, prep, or rebuild, and of what. Do not summarize the diff; it's in the file and they just read it.

If the user has lapsed — nothing committed for weeks — **restart cold with no penance**. Franklin tapered from four cycles a year to one, then to none, and still credited the system; he kept the little book on him for life. Lapsing is part of the method, not the end of it. Never open a session with a guilt tally.