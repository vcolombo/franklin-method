---
name: franklin-drill
description: "Run one session of a Franklin-method campaign — acquire a rung's material and test the gate, prep an exemplar into hints, or diff a blind rebuild against the original. Use for daily practice in an existing ~/franklin campaign."
---

# Franklin — Run a Session

The daily driver for a campaign created by `franklin`. Twenty minutes. **Three modes.**

**Invocation:** `/franklin-drill [subject]`

| Mode | When | What happens |
|---|---|---|
| **Mode 0 — Acquire** | The current rung's gate in `GATES.md` is not passed | Work through the material; run the exit test when the time box is up |
| **Mode A — Prep** | Gate passed, nothing ripe | Compress an exemplar to hints, set the cold delay |
| **Mode B — Rebuild** | Gate passed, something ripe | Hints only, blind rebuild, diff, log faults |

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

1. **Gate check first.** Find the rung this week's schedule is on. If its `GATES.md` entry has `needed: true` and `passed: null` → **Mode 0**. Nothing else runs until that gate is passed.
2. Any exemplar `status: cold` with `cold_until` **today or earlier** → **Mode B**. Ripe exemplars go stale.
3. Otherwise → **Mode A**.
4. Fewer than 2 exemplars in flight → **Mode A**, even with something queued behind it.
5. **Ratio guard:** if sources (`r`) are running ahead of artifacts (`e`) — more than a third of recent sessions, or an `r` prepped while an `e` sits unprepped — prep the artifact and say why.
6. If everything is cold but not ripe, say which ripens first and when, then prep. **Never serve a cold exemplar early**, even if asked.

**The gate is not advisory.** If the user asks to skip ahead to drilling, say once, in a line, that the diff will be noise without the material — then respect their call if they insist, and record the bypass in that gate's `notes` so the review can see it.

---

## Mode 0 — Acquire

**Open by naming the mode.** "This rung needs its material first — we're acquiring, not drilling, for about four sessions." A user who expects a drill and gets a reading list assumes something went wrong.

1. **Work the material**, in the order `GATES.md` lists it. Claude can explain, answer questions, and work examples alongside them here — this is the one mode where that helps rather than steals the learning.
2. **Track sessions against the time box.** If the box is spent and the exit test isn't close, say so plainly: either the material is wrong for them, or the rung is too big. Both are findings. Do not silently extend.
3. **Run the exit test** once the material is covered:
   - **Explain it unaided.** They write the explanation from memory, sources closed. Claude checks it against the material and **names what is missing or wrong rather than grading it warmly.** Vague means not landed.
   - **Pass the exercises.** The source's own, or the substitute build task. **The result must run, compile, hold water, or otherwise be externally checkable.** If the only available check is Claude's opinion, the exit test is broken — say so and find a real one.
4. **Record it.** Set `passed: <today>` in `GATES.md`, or leave it null and note what is still missing.
5. **Commit:** `acquire: <rung> — session N of <box>`, or `gate: <rung> passed`.
6. **Close by naming what unlocks.** "Gate passed — tomorrow we prep the first exemplar, first rebuild Monday."

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