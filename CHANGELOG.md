# Changelog

What changed between released versions of the plugin, for people who install it with
`/plugin marketplace add vcolombo/franklin-method` and want to know what an update
brings without reading the commit history.

Versions are the ones in `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`,
which always agree — CI fails the build if they don't.

## 0.3.2 — 2026-09-19

**`franklin-review`'s schema check had never run.** The step invoked the checker
through `$CLAUDE_PLUGIN_ROOT` unbraced. Claude Code substitutes only the exact token
`${CLAUDE_PLUGIN_ROOT}` into skill content, and does not put the variable in the Bash
tool's environment, so the command resolved to `/scripts/check-campaign.py` and every
review fell through to the not-installed fallback. If you installed 0.3.0 or 0.3.1,
your reviews were running without the schema check. ([#4](https://github.com/vcolombo/franklin-method/issues/4))

Eight reporting faults in `check-campaign.py`, none of which changed a schema rule —
all of them the checker describing a campaign wrongly:

- `--all` treated `<home>/history/` as a campaign, so a single `franklin-history`
  report made it exit 1 forever. Discovery now requires a `campaign.yml` or
  `GATES.md`. ([#5](https://github.com/vcolombo/franklin-method/issues/5))
- `R001` walked ancestors to `/`, so a campaign under a git-tracked home directory
  looked tracked — and `franklin-history` would have mined that repo's log as the
  campaign's session record. It now expects the campaign or its home, and names the
  distant repo otherwise. `--no-vcs-check` covers a campaign before `git init`.
- `X003`/`X004` fired on exemplars whose rung is `needed: false`, waiting on a gate
  that will never pass.
- A missing or unparseable `GATES.md` made every exemplar report `X001` as well.
- An unparseable YAML fence reported twice for one fault.
- `material.video` written as a lone mapping was reported as empty.
- `G024`/`G025` nagged about re-checking links on gates already passed.
- An unhashable `rung:` or `sub_skill:` raised `TypeError` instead of reporting.

The schemas moved out of `skills/franklin/SKILL.md` into
`skills/franklin/reference.md`, loaded on demand, with a test that fails when the
prose and the checker stop agreeing. ([#6](https://github.com/vcolombo/franklin-method/issues/6),
[#7](https://github.com/vcolombo/franklin-method/issues/7))

Adds this changelog.

0.3.1 was an intermediate version within this change and was never published on its
own.

## 0.3.0 — 2026-09-18

**The campaign home is configurable.** All four skills hardcoded `~/franklin/*/`, so
a campaign kept anywhere else was invisible to them — `franklin-history` worst of
all, since it globs rather than taking a path and would have reported on nothing
while looking like it had run. They now read `$FRANKLIN_HOME`, falling back to
`~/franklin`.

**`franklin-review` runs the schema check as step 0**, before the fault tally. (This
did not actually work until 0.3.2 — see above.)

`check-campaign.py` carries a PEP 723 header, so `uv run` supplies PyYAML with
nothing to install, and its dependency message names commands that work.

Signal-to-noise: a first run against a real campaign returned 38 findings of which
about 8 were real. Extra `campaign.yml` keys are no longer policed unless they look
like misspellings, a `needed: false` rung reports once instead of six times, a video
entry with no url reports once, and the parallel judgment rung is no longer called a
dangling reference.

## 0.2.0 — 2026-09-18

**`scripts/check-campaign.py`** — the campaign schema as a runnable check. It reads
`campaign.yml`, `GATES.md` and every `exemplars/*/meta.yml` and reports where a
campaign has drifted from what `franklin-drill` expects, including a gate marked
passed while its placement is still pending.

**The time box counts the placement session**, stated in all four skills. A box
narrowed to three buys one placement and two acquisition sessions.

CI validates both manifests and the skills with `--strict` and runs the fixture
suite.

## 0.1.0 — 2026-09-18

First release. Four skills — `franklin`, `franklin-drill`, `franklin-review`,
`franklin-history` — plus the plugin and marketplace manifests.

Acquisition is measured rather than assumed: a placement quiz per rung scored against
a key written before the user answers, one orientation session before rung 1 that
includes the honest case against the subject, and acquisition material in at least
two modalities with links verified live.
