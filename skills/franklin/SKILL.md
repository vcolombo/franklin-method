---
name: franklin
description: "Start a Franklin-method learning campaign for any subject: interview the goal, decompose it into sub-skills with real answer keys, build an orientation block, a placement-sized acquisition gate and drills for each rung, and init a git repo to track it. Use when the user says they want to learn something."
---

# Franklin — Start a Learning Campaign

## The two modes — read this before anything else

Franklin worked in **two** modes, and confusing them wrecks a curriculum.

| Mode | What it does | His example |
|---|---|---|
| **Acquisition** | Gets material into your head the first time | Cocker's arithmetic — *"went through the whole by myself with great ease."* Locke, the Port-Royal Logic, Xenophon. French, then Italian, then Spanish. |
| **Refinement** | Sharpens craft on material you already comprehend | The *Spectator* drill — hints, cold delay, blind rebuild, diff |

> **Take an exemplar apart → let it go cold → rebuild it blind → diff → log what you lost → repeat.**

That loop is **refinement only**. When Franklin ran it he already read English fluently; what he lacked was elegance, method and perspicuity — his father's words. He was not learning the language. He was sharpening craft in a language he already had.

**Reconstructing material you have not yet acquired is reconstructing a Spectator essay in a language you cannot read.** It produces frustration, a meaningless diff, and a user who reasonably concludes the method is broken.

So every rung gets **acquisition first, gated by an exit test, then drills.** Acquisition is not optional, not supplementary, and not the same thing as the source track in step 9 — sources explain *why*, acquisition teaches *what*.

**Invocation:** `/franklin <subject>` — e.g. "/franklin I want to learn about underwater basket weaving"

## Step 0 — Start, resume, or queue?

**Campaign home:** `$FRANKLIN_HOME` if that is set, otherwise `~/franklin`. Written `<home>` below.

List `<home>/*/` and read each `campaign.yml`.

- **This subject already exists** → a resume, not a start. Read its `README.md` and hand off to `franklin-drill` or `franklin-review`. Do not re-run the interview.
- **Another campaign is `status: active`** → this one is **queued**, not started. See below.
- **Nothing active** → a normal start.

### One active campaign at a time

Twenty minutes is the number because it is what survives a working week. Two campaigns is forty, and the reliable outcome is losing both. So when an active campaign already exists, **design the new one fully and mark it queued** — do not offer to run them in parallel, and do not make the user argue for the queue.

Say plainly: which campaign is active, when it ends, and that this one starts after. Then design it anyway — the design is useful now, the sessions are not.

**Pick a start date that is not the week after a holiday.** The first fortnight is what sets the habit; losing it to Christmas costs more than the two weeks.

### A queued curriculum is a draft — say so in the README

It is being written before a single drill has run. The active campaign's **cycle review will produce evidence this plan cannot have yet**:

- Which fault rows are real for this person, especially the cross-cutting ones carried into every campaign
- Which drill forms actually moved their fault rate — if scramble never shifted a number, don't schedule a scramble
- Their real cadence, from `git log` rather than from the plan

Write into the queued README: **re-run `franklin-review` on the active campaign first, then revise this before week 1.** The schedule is not settled.

## Step 1 — Interview, one round only

Ask 3–5 questions in a **single batch**, then proceed. Do not drip-feed follow-ups.

1. **Aim:** what does "I can do this" look like concretely? Push for an observable result — "weave a watertight coiled basket unassisted" not "understand basket weaving."
2. **Current level:** what can they already do in this area, and what's the nearest adjacent skill they already have? Press for evidence rather than accepting "beginner" or "intermediate" — what have they built, what error would they recognise on sight. **This sizes the schedule, not the gates.** Each rung's real starting point is measured by a placement quiz when that rung comes up (step 7); self-assessment is unreliable in both directions and is never the basis for skipping or padding a gate.
3. **Budget:** minutes per day, and is there a deadline or event driving this?
4. **Access:** what exemplars, materials, tools, courses, or people can they actually get at? (This constrains everything downstream.)
5. **Only if genuinely unclear:** is the aim performance, understanding, or production? These need different drills.

## Step 2 — Decompose into sub-skills

Franklin's sharpest move: he knew his writing had **three separate deficits** — thin vocabulary, weak sentence-level expression, and poor structure — and he built a **separate drill for each**. He did not "practice writing."

Break the subject into **3–6 mechanical sub-skills that can fail independently, plus the judgment rung from step 4** — the judgment rung is additional, never one of the six. Test: could someone be good at one and bad at another? If not, you haven't decomposed — you've renamed.

- *Basket weaving* → material preparation · coil tension · shape control · finishing/rim · pattern design
- *Kubernetes* → manifest authoring · debugging a broken pod · networking model · resource tuning
- *Sales calls* → discovery questioning · objection handling · narrative framing · close mechanics

## Step 3 — The answer key gate (do not skip)

Every drill Franklin invented had a built-in answer key: the original *Spectator* essay, the tally in the little book, the other man's essay. **No teacher required, because the correction was baked in.**

For each sub-skill, name the answer key explicitly. Valid kinds:

| Kind | Example |
|---|---|
| The original artifact | The essay, the diagram, the reference implementation |
| A physical result | The basket holds water, or it doesn't |
| An executable check | Tests pass, the cluster comes up, the number reconciles |
| An expert's version | Their solution, revealed after yours is committed |
| A resolving prediction | You call it in writing, reality settles it |

**If a sub-skill has no answer key, it is not drillable.** Either convert it into one that is, or cut it and say so. Do not let a sub-skill through on "I'll just reflect on it" — that is the failure mode this whole method exists to prevent.

## Step 4 — Check what the gate just dropped

The gate filters **drills**, not sub-skills. Applied carelessly it selects for whatever is mechanically checkable and silently discards the judgment at the center of the subject — the part that decides *when* and *why* to apply the mechanics. The result is a curriculum that produces someone who executes correctly and cannot say what any of it is for.

So after step 3, ask explicitly: **is there a "knowing what this is for" sub-skill I just dropped because it looked un-drillable?** There almost always is — hearing what a hard-to-write test is telling you, feeling when the clay is wrong, knowing which objection is the real one.

It is drillable. The key is nearly always a **resolving prediction**:

1. Before acting, predict in writing what will happen and why
2. Act
3. Score it: hit / partial / blind miss / false alarm

**Blind misses — "I thought this would be easy" — are the signal.** They are the cues the user cannot yet read, and they name themselves over a cycle. Track hit rate in `PREDICTIONS.md`. A rising rate is the evidence; a flat one after a full cycle means the sources aren't reaching their hands and the drills need to change.

This rung is **in addition to** the 3–6 from step 2, and it runs in parallel across all thirteen weeks rather than occupying a slot of its own.

## Step 5 — Order the ladder, easiest rung first

Franklin argued against the Latin-first convention: start with French, then Italian, then Spanish, and Latin comes nearly free. *"If you begin with the lowest you will with more ease ascend to the top."*

Order the sub-skills so each one makes the next cheaper, starting from whatever is **tractable today with materials in hand** — not from whatever is most prestigious or most fundamental. Prestige-first curricula are the ones people quit.

## Step 6 — Write the orientation block

Before rung 1, and before any mechanics, the campaign answers one question: **what
is this subject, and why does anyone do it this way?**

This is not a gate and has no exit test. It is one session, and it exists because a
curriculum built from step 2 onward is a ladder with no ground floor — it teaches
the mechanics of a thing the learner cannot yet say the point of. A learner who can
write a fixture but cannot say what test-first is *for* will drop the campaign around
week 5 and will be right to.

Write into `GATES.md` an ungated `orientation` block naming what the session must
cover:

1. **What the thing is** — the loop, the process, the form. Concretely, not by
   analogy.
2. **The mechanisms** — what it actually buys, enumerated and *separable*. "It
   improves quality" is not a mechanism. "A test you have not watched fail has never
   been verified to be wired to the behaviour" is.
3. **The honest case against** — where the evidence is weak or mixed, what the
   practice is bad at, what the live disagreements in the field are. A campaign that
   opens with advocacy produces a learner who cannot tell a real objection from a
   lazy one, and it forfeits the user's trust the first time they meet a credible
   critic.
4. **The rungs mapped onto the thing** — why rung 1 is first, and what each later
   rung is for. This converts the schedule from an arbitrary list into a route.

### The exemplar-contamination rule

If the campaign's source track drills a text that argues for the subject — and it
usually does, because that is what makes a good `r01` — then **orientation must not
paraphrase that text's argument, its ordering, or the misreadings it names.**
Reconstructing it later requires recall; reading a summary now converts that into
recognition and quietly destroys the exemplar.

Orient from the common ground of the field instead, and say in the note which text
is being held back and why. Where the whole orientation would be that one text,
either pick a different `r01` or accept that the campaign has no drilled source for
that rung — both are honest; a spoiled exemplar is not.

## Step 7 — Build the acquisition gate for every rung

**This step comes before drill design, because a drill on unacquired material is not a drill.**

For each rung ask: *can they already read the exemplar?* Not "could they write it" — could they look at a reference example of this sub-skill and understand what every part is doing and why? If no, the rung needs acquisition.

For each rung that does, name four things.

### 1. Placement — do not size a gate from a guess

**Never assume a starting point, in either direction.** Assuming zero bores an
experienced user out of a fourteen-week campaign; assuming competence strands a
beginner in drills whose diff is noise. Both failures look like "the method doesn't
work."

Placement is **run per rung by `franklin-drill`, immediately before that rung's
acquisition block** — not here, and not all at once at campaign creation. A guess
made in week 1 about where the user will stand in week 10 is worthless: they will
have spent nine weeks in the subject by then. What this step does is *declare that
placement is required* and leave the box unsized until it runs.

So write into the rung's `GATES.md` block:

```yaml
  placement:
    status: pending        # pending | done
    run_on: null           # YYYY-MM-DD, filled by franklin-drill
    result: null           # zero | partial | solid — filled by franklin-drill
    evidence: ""           # which quiz items were missed, in one line
```

and set `time_box` as a **range** — `"2–6 sessions, set by placement"` — rather than
a fixed number. `franklin-drill` narrows it when placement runs.

**The box includes the placement session.** Placement costs a real twenty minutes, so
a rung boxed at three sessions buys one placement and two acquisition sessions. Size
the ranges knowing that, or every rung silently runs a session over.

The step-1 interview answer still matters: it sizes the *schedule* so the calendar is
roughly right. It does not size the gate.

### 2. The material — at least two modalities, links verified

Name the material, and name it as **specific resources with URLs**, never as a
category. "Read the docs" is not material; a named page is.

Every acquisition block offers **at least canonical text and a video**, because
people do not all learn the same way and a campaign that ships only one modality
silently fails the half of users who need the other:

| Modality | Required? | What it must be |
|---|---|---|
| **Canonical text** | **Always** | The authoritative written reference — official docs, the spec, the primary source. Named pages, not a site root. |
| **Video / talk / screencast** | **Always, where one exists** | A specific video with a **timestamped segment**, not a channel or a playlist. For anything with tacit motion — craft, hardware, tooling — this is the *primary* material, not a supplement. |
| **Worked example or interactive** | Strongly preferred | A tutorial with exercises, a playground, a kata, a repo that runs. The *do it* modality, distinct from read-or-watch. |
| **One deeper dive** | Optional, always flagged | A chapter, paper, or long talk marked **explicitly beyond the gate**, so the curious user has somewhere to go without inflating the time box. |

Where no video exists for a rung, **say so in the block rather than omitting the row
silently** — the absence is information, and it tells the user not to go looking.

**Search; never recall.** The skill's rule for sources applies with full force to
acquisition material: recommendations from memory go stale, and a dead link in week
one destroys confidence in the whole plan. Search for each resource and **verify it
resolves before writing it down.** Note plainly anything paywalled, borrow-only, or
requiring an account.

Links are gathered **per rung, when that rung's block starts**, by `franklin-drill` —
for the same reason placement is: a link verified in week 1 for a week-11 rung may
well be dead by week 11. At campaign creation, name one canonical text and one video
per rung so the plan is legible, and mark the rest `to_verify`.

Reference docs are excellent here even though they are never drilled: acquisition and drilling want opposite media.

### 3. The exit test

Two checks, both external, neither Claude's opinion:

- **Explain it unaided.** Write the explanation from memory, no source open. Vague explanation means it hasn't landed.
- **Pass the source's own exercises.** Most good acquisition material ships them. If it doesn't, substitute a small build-from-scratch task with a runnable or visible result.

### 4. The time box

A number of sessions — **a range until placement narrows it**, and it counts the placement session itself. Acquisition expands to fill whatever it is given; the exit test is what ends it, the box is what stops it quietly becoming the campaign.

### Acquisition is not the source track

They differ in kind and both are needed:

| | Acquisition | Sources (step 9) |
|---|---|---|
| Teaches | **What** it is and how it works | **Why** it matters and when to use it |
| Example | pytest docs, a fixtures tutorial | Beck's *Canon TDD* |
| Form | Read, follow, do the exercises | Drilled — hints, cold, rebuild, diff |
| Repeats? | No. Passed once, done. | Yes, across the cycle |
| Bounded by | Its exit test and time box | The one-in-three ratio |

### Where a whole block is acquisition

Sometimes a rung's material is genuinely new *and* the user has no adjacent skill to lean on. Then the first block is acquisition and contains no drills at all. **Say so plainly rather than inventing a drill to fill the week.** A curriculum honest about "week 1 you are learning pytest, there is nothing to reconstruct yet" is worth more than one that pretends otherwise.

### When acquisition is unnecessary

A rung can turn out not to need its gate — a rusty expert, an adjacent skill that transfers. **That is placement's call to make, not the interview's.** Write the gate as `needed: true` with placement pending; if placement comes back `solid`, `franklin-drill` marks the gate passed on the spot with the evidence recorded, and the block converts to drills. Do not pre-emptively skip a gate on a self-report, and do not manufacture one to look thorough.

## Step 8 — Assign a drill form to each sub-skill

These run **after** that rung's gate is passed. Three canonical forms; pick and adapt per sub-skill, and name the adaptation in the curriculum.

**A. Reconstruction** (his core drill). Compress an exemplar to terse hints → set it aside for days → rebuild from hints alone, without looking → diff against the original.
- *Text:* one hint per sentence's idea, then rewrite the piece.
- *Physical:* hints are the technique steps you observed; the rebuild is the object; the diff is photo-vs-photo.
- *Code/systems:* hints are the architecture in bullets; the rebuild is a from-scratch implementation.

**B. Constraint transform** (his prose→verse→prose). Re-express the material under a constraint that *forces* the missing capability, wait, then transform it back. Franklin used meter and rhyme specifically because they forced him to hunt for synonyms — the exact deficit he'd diagnosed.
- Pick a constraint that makes the weak sub-skill unavoidable. Explain a concept with no jargon; build the thing with one tool removed; weave with an unfamiliar material.

**C. Scramble** (his structure drill). Shuffle your own hints into disorder, come back weeks later, re-sequence them cold, then compare your ordering to the original's.
- Works anywhere sequence matters: argument, process, assembly order, runbook steps.

## Step 9 — Build the source track

Franklin read enormously and drilled on top of it. The drills were never the whole education.

But sources do not get a passive parallel track. **Each one is an exemplar**: prepped to hints, held cold, rebuilt blind, diffed. Reading has no answer key on its own, which is exactly why it cannot be the spine.

For each rung, name **one drilled source**. Add background only where it earns a line.

### Picking the medium

| Medium | Good for acquisition? | Good for drilling? |
|---|---|---|
| Reference docs | **Yes — the best** | **Never.** You look things up; you don't reconstruct a manual |
| Tutorial / worked examples / course | **Yes — fastest route in** | Its *published solutions* are exemplars; the walkthrough is not |
| Essay, chapter, paper (argumentative) | Weak — assumes the mechanics already | **Yes — the default.** Reconstruct the argument, diff claim by claim |
| Recorded talk | Moderate | Yes, from a 10–15 min segment; transcripts make it diffable |
| Demonstration / screencast | **Yes** — tacit motion exists nowhere in text | Yes — reconstruct the procedure, perform it, rewatch and diff |
| Primary artifact (real code, objects, recordings) | No — unmediated and unexplained | **Yes** — standard reconstruction |

That first row resolves an old tension: **reference docs are banned from drilling and ideal for acquisition.** The media differ because the modes differ.

For physical and craft subjects, demonstration video does double duty — it is both the acquisition material and the exemplar.

**A course with published solutions is the sharpest trap here.** Working through it in order is a tutorial, and the user finishes able to follow instructions. Use the walkthrough for acquisition; then take each unit's *intent* as hints, let it go cold, rebuild blind, and diff against the reference — which is the answer key, never the thing followed along with. Say this out loud, and give it a fault-grid row.

### The test for whether a source gets drilled

**Only if you can say what the diff would compare.** "Reconstruct Beck's argument for test-first, diff claim by claim" passes. "Read the docs" does not — that is acquisition or background, not a drill.

### Finding the sources

- **Search; do not recall.** Recommendations from memory go stale, and a dead link destroys confidence in the whole plan. Verify each one is reachable before listing it.
- **Primary over commentary.** The practitioner who invented the thing beats the explainer.
- **One session's worth.** An essay, a chapter, a talk segment — not a whole book.
- **Free and accessible first.** Note plainly when something must be bought or borrowed.

### The trap

Consuming feels like progress and costs nothing. A campaign where every source is current and every drill is behind has failed while feeling successful — and for some subjects that is the *dominant* failure mode, so say so out loud when it is.

**Cap sources at roughly one session in three.** Acquisition is exempt from that ratio — it is bounded by its exit test and time box instead — but it *is* bounded, and the review checks both.

## Step 10 — Find the Junto

Franklin's club had enforced rules: an original essay from each member every quarter, debate *"in the sincere spirit of inquiry after truth, without fondness for dispute or desire of victory,"* and a **cash fine** for expressing positiveness or flatly contradicting someone.

Identify one real venue — a person, a group, a forum, a subreddit, a Discord — where the user will present work and take criticism. Schedule one presentation at week 12. If they truly have no venue, say so plainly and substitute a public post; do not pretend a private journal is a Junto.

## Step 11 — Seed the pipeline

Once rung 1's gate is passed, several exemplars stay in flight at once so a ripe one is always waiting. A campaign seeded with a single exemplar strands the user for four days with nothing to do.

**Name three concrete exemplars for the first drilling block** — specific files, objects, passages, videos, or repos, not categories — recorded as `e01`, `e02`, `e03` with `status: awaiting-material`. Source exemplars are `r01`, `r02`, … so the ratio stays visible.

```
[acquire rung 1] → [exit test] → prep e01 ──┐
                                 prep e02 ──┼─ (4+ days cold) ─> rebuild e01 ─> ...
                                 prep e03 ──┘
```

Write into the generated `README.md`, in the user's own subject terms:

- **The two modes**, and which one each block is in.
- **The first block is acquisition, not drilling.** Nothing to reconstruct yet, and that is correct.
- **Prep is real work** — compressing something to intent-hints requires understanding it first. That is also why prep is impossible before the gate.
- **What "cold" forbids:** re-reading *the exemplar under cold*. Nothing else. Reading around the subject, docs, adjacent material and throwaway practice are all fine and encouraged.
- **The source cap**, and why it exists.

## Step 12 — Write the repo

```
<home>/<subject-slug>/
  campaign.yml       # status, aim, dates — the machine-readable header
  README.md          # aim, ladder, two modes, pipeline, source cap, how to resume
  CURRICULUM.md      # per rung: acquisition gate, exit test, drill form, answer key
  SCHEDULE.md        # weeks, acquisition blocks marked, checkboxes
  GATES.md           # acquisition exit tests and whether each has been passed
  FAULTS.md          # the 13-row grid + running fault log
  PREDICTIONS.md     # the resolving-prediction log, if the campaign has one
  exemplars/<id>/    # original.md (or link + notes), hints.md, meta.yml
  rebuilds/<id>/     # attempt-NN.md, diff-NN.md
  reviews/           # week-NN.md
```

`campaign.yml`:
```yaml
subject: test-driven-development
status: active            # active | queued | complete | abandoned
aim: <the observable aim, one line>
week_1: 2026-09-21
blocked_on: null
planned_start: null
curriculum_is_draft: false
```

`GATES.md` — an ungated orientation block, then one block per rung; **`franklin-drill` reads this before serving any drill**:
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

`meta.yml` per exemplar:
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

A queued campaign also gets a **STATUS banner at the top of its README**.

`git init`, commit as `franklin: start <subject>` (or `franklin: queue <subject>`). One commit per session from here on — `git log` is the record, and `franklin-history` reads it as its source of truth.

**Pick one home for the repo and say which it is** — and if it is not `~/franklin`, say that `$FRANKLIN_HOME` needs to be set for the other skills to find it. Two copies on two machines diverge. If the repo lives on the user's own machine, confirm the tooling the drills will need actually runs there before reporting success.

## Step 13 — Report back, short

**Active campaign:** the ladder in order, **what the first acquisition block is and how it will be tested**, the daily time slot, and when the first rebuild actually happens. Do not hand them three exemplars to obtain if the first block is acquisition — they'll need those in week 3, not tonight.

**Queued campaign:** the ladder, what it is blocked on and until when, and that the curriculum is a draft.

**Either way**, once more than one campaign directory exists, say that `franklin-drill` and `franklin-review` now need the subject named explicitly. Then stop. Do not restate the curriculum — it's in the repo.

## Non-negotiables

- **Acquire before you drill.** Reconstruction sharpens craft on material already understood. Running it earlier teaches nothing and reads to the user as the method being broken.
- **Orient before you acquire.** Mechanics without "what is this and why" produce a learner who executes correctly and cannot say what any of it is for. One ungated session, and it includes the honest case against.
- **Measure the starting point; never assume it.** Not zero, not competent. A placement quiz per rung, scored against a key, immediately before that rung's block.
- **Two modalities minimum, links verified live.** Canonical text and a video with a timestamped segment, searched and checked to resolve when the block starts — never recalled from memory, never a bare site root.
- **Twenty minutes is the real number.** Franklin studied "at night after work, or before it began in the morning, or on Sundays." Design for the seams.
- **One active campaign.** Two is forty minutes a day and loses both.
- **The cold delay is the method**, not overhead. Four days minimum.
- **Never design a drill — or an exit test — whose answer key is Claude's opinion.** External correction or it isn't a check.
- **Never let sources or acquisition become the campaign.** They serve the drills; they don't replace them.