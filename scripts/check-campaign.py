#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["pyyaml"]
# ///
"""Check a Franklin-method campaign repo against the schema the skills write.

The skills are prose, and prose gates get talked past. This is the same schema
as a script: it reads campaign.yml, GATES.md and exemplars/*/meta.yml and says
where the campaign has drifted from what franklin-drill expects to find.

Usage:
    uv run scripts/check-campaign.py ~/franklin/tdd   # no install needed
    scripts/check-campaign.py ~/franklin/tdd          # needs PyYAML present
    scripts/check-campaign.py --all          # every campaign under the home
    scripts/check-campaign.py --strict ...   # warnings count as failures
    scripts/check-campaign.py --json ...
    scripts/check-campaign.py --no-vcs-check ...   # before git init

The campaign home defaults to ~/franklin, overridden by $FRANKLIN_HOME or --home.

Exit codes: 0 clean, 1 findings, 2 could not run (bad path, missing PyYAML).
"""

from __future__ import annotations

import argparse
import datetime as dt
import difflib
import json
import os
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - environment problem, not a finding
    sys.stderr.write(
        "check-campaign needs PyYAML. Either of these works:\n"
        "\n"
        "    uv run %s <campaign>        # installs nothing; uv reads this file's header\n"
        "    python3 -m pip install --user pyyaml\n"
        "\n"
        "(PyYAML is a library, not a command, so `pipx run` cannot supply it.)\n"
        % sys.argv[0]
    )
    sys.exit(2)

ERROR = "ERROR"
WARN = "WARN"

COLD_DAYS_MIN = 4
STALE_LINKS_DAYS = 45

CAMPAIGN_KEYS = {
    "subject", "status", "aim", "week_1", "blocked_on",
    "planned_start", "curriculum_is_draft",
}
CAMPAIGN_REQUIRED = {"subject", "status", "aim"}
CAMPAIGN_STATUS = {"active", "queued", "complete", "abandoned"}

RUNG_REQUIRED = {"rung", "needed", "placement", "material", "time_box", "exit_test", "passed"}
PLACEMENT_STATUS = {"pending", "done"}
PLACEMENT_RESULT = {"zero", "partial", "solid"}

EXEMPLAR_KINDS = {"artifact", "reading", "video"}
EXEMPLAR_STATUS = {"awaiting-material", "ready-to-prep", "cold", "rebuilt", "diffed"}

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
RANGE_RE = re.compile(r"\d\s*[-–]\s*\d")
YAML_FENCE_RE = re.compile(r"^```ya?ml\s*$(.*?)^```\s*$", re.S | re.M)


class Findings:
    def __init__(self) -> None:
        self.items: list[dict] = []

    def add(self, level: str, code: str, where: str, message: str) -> None:
        self.items.append({"level": level, "code": code, "where": where, "message": message})

    def error(self, code: str, where: str, message: str) -> None:
        self.add(ERROR, code, where, message)

    def warn(self, code: str, where: str, message: str) -> None:
        self.add(WARN, code, where, message)

    @property
    def errors(self) -> int:
        return sum(1 for i in self.items if i["level"] == ERROR)

    @property
    def warnings(self) -> int:
        return sum(1 for i in self.items if i["level"] == WARN)


def as_date(value) -> dt.date | None:
    """Return a date for a YAML date or an ISO string, else None."""
    if isinstance(value, dt.datetime):
        return value.date()
    if isinstance(value, dt.date):
        return value
    if isinstance(value, str) and DATE_RE.match(value.strip()):
        try:
            return dt.date.fromisoformat(value.strip())
        except ValueError:
            return None
    return None


def is_blank(value) -> bool:
    return value is None or (isinstance(value, str) and not value.strip())


def names_slug(text: str, slug: str) -> bool:
    """True when prose refers to a slug, hyphenated or spelled out.

    Whole-word only. A bare substring test lets an unknown sub-skill named
    `read` pass because the prose happens to say `readiness`, which silently
    suppresses the finding this exists to make.
    """
    needle = re.sub(r"[\s_-]+", " ", str(slug).lower().strip())
    if not needle:
        return False
    haystack = re.sub(r"[\s_-]+", " ", text.lower())
    return re.search(rf"(?<!\w){re.escape(needle)}(?!\w)", haystack) is not None


def load_yaml_document(path: Path, f: Findings, code: str) -> dict | None:
    """Parse a file that is either plain YAML or Markdown with ```yaml blocks."""
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        f.error(code, path.name, f"cannot read: {exc}")
        return None

    blocks = [m.group(1) for m in YAML_FENCE_RE.finditer(raw)]
    sources = blocks if blocks else [raw]

    merged: dict = {}
    parsed_any = False
    reported = False
    for source in sources:
        try:
            doc = yaml.safe_load(source)
        except yaml.YAMLError as exc:
            f.error(code, path.name, f"YAML will not parse: {str(exc).splitlines()[0]}")
            reported = True
            continue
        if doc is None:
            continue
        if not isinstance(doc, dict):
            continue
        parsed_any = True
        for key, value in doc.items():
            if key in merged and isinstance(merged[key], list) and isinstance(value, list):
                merged[key].extend(value)
            else:
                merged[key] = value

    if not parsed_any:
        # The parse error above already said why; "no mapping found" is that same
        # fault restated.
        if not reported:
            f.error(code, path.name, "no YAML mapping found (expected the blocks franklin writes)")
        return None
    return merged


# --------------------------------------------------------------------------
# campaign.yml
# --------------------------------------------------------------------------

def check_campaign_yml(root: Path, f: Findings) -> dict:
    path = root / "campaign.yml"
    if not path.exists():
        f.error("C001", "campaign.yml", "missing — franklin-drill cannot tell whether this campaign is live")
        return {}

    try:
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        f.error("C002", "campaign.yml", f"will not parse: {str(exc).splitlines()[0]}")
        return {}

    if not isinstance(doc, dict):
        f.error("C002", "campaign.yml", "is not a YAML mapping")
        return {}

    for key in sorted(CAMPAIGN_REQUIRED - set(doc)):
        f.error("C003", "campaign.yml", f"missing required key '{key}'")

    status = doc.get("status")
    if status not in CAMPAIGN_STATUS:
        f.error("C004", "campaign.yml",
                f"status {status!r} is not one of {sorted(CAMPAIGN_STATUS)}")

    for key in ("week_1", "planned_start"):
        value = doc.get(key)
        if value is not None and as_date(value) is None:
            f.error("C005", "campaign.yml", f"{key} {value!r} is not YYYY-MM-DD")

    if status == "queued" and is_blank(doc.get("blocked_on")):
        f.warn("C006", "campaign.yml",
               "status is queued but blocked_on is empty — say which campaign it waits on")

    # Extra keys are how a campaign carries its own metadata — a title, a
    # cadence, the ladder repeated for convenience. Policing them buries the
    # real findings under a dozen warnings, so only flag what looks like a
    # misspelling of a key the skills actually read.
    #
    # YAML does not require keys to be strings, and a file with `13: weeks` in
    # it is a campaign to report on, not a traceback: sorting a mixed-type set
    # raises, and get_close_matches only takes strings.
    extra = set(doc) - CAMPAIGN_KEYS
    for key in sorted(repr(k) for k in extra if not isinstance(k, str)):
        f.error("C008", "campaign.yml",
                f"key {key} is not a string — the skills read this file by name")
    for key in sorted(k for k in extra if isinstance(k, str)):
        near = difflib.get_close_matches(key, sorted(CAMPAIGN_KEYS), n=1, cutoff=0.8)
        if near:
            f.warn("C007", "campaign.yml",
                   f"key '{key}' looks like a misspelling of '{near[0]}', which is the one the skills read")

    return doc


# --------------------------------------------------------------------------
# GATES.md
# --------------------------------------------------------------------------

def check_url(url, where: str, f: Findings) -> None:
    if is_blank(url):
        f.error("G023", where, "resource has no url")
        return
    text = str(url).strip()
    if not text.startswith(("http://", "https://")):
        f.warn("G023", where, f"url {text!r} is not an http(s) link")
        return
    rest = text.split("://", 1)[1].rstrip("/")
    if "/" not in rest:
        f.warn("G023", where, f"url {text!r} is a bare site root — name the page")


def check_material(material, where: str, placement_done: bool, gate_passed, today: dt.date,
                   f: Findings) -> None:
    if not isinstance(material, dict):
        f.error("G020", where, "material block missing or not a mapping")
        return

    text = material.get("text")
    if isinstance(text, dict):
        text = [text]
    if not isinstance(text, list) or not text:
        f.error("G020", where, "material.text is empty — no canonical text for this rung")
    else:
        for i, entry in enumerate(text):
            if isinstance(entry, dict):
                check_url(entry.get("url"), f"{where} material.text[{i}]", f)
            else:
                f.error("G020", f"{where} material.text[{i}]", "entry is not a mapping with a url")

    video = material.get("video")
    if isinstance(video, dict):
        # A single resource written as a mapping rather than a one-item list is
        # unambiguous. Calling it "empty" points at the wrong fix — the finding
        # belongs to whatever the entry is actually missing.
        video = [video]
    if not isinstance(video, list) or not video:
        f.error("G021", where,
                "material.video is empty — two modalities are the minimum; "
                "record none_found with a reason if a search turned nothing up")
    else:
        for i, entry in enumerate(video):
            spot = f"{where} material.video[{i}]"
            if not isinstance(entry, dict):
                f.error("G022", spot, "entry is not a mapping")
                continue
            if "none_found" in entry:
                if is_blank(entry.get("none_found")):
                    f.error("G022", spot, "none_found needs the reason the search came up empty")
                continue
            if is_blank(entry.get("url")):
                # One finding, not two: an entry with no video cannot have a
                # segment of one.
                f.error("G023", spot, "resource has no url")
                continue
            check_url(entry.get("url"), spot, f)
            if is_blank(entry.get("segment")):
                f.error("G022", spot, "video has no timestamped segment — a whole video is not a gate")

    for optional in ("interactive", "deeper"):
        entries = material.get(optional)
        if isinstance(entries, list):
            for i, entry in enumerate(entries):
                if isinstance(entry, dict):
                    check_url(entry.get("url"), f"{where} material.{optional}[{i}]", f)

    verified = material.get("verified_on")
    if verified is None:
        if placement_done and gate_passed is None:
            f.warn("G024", where,
                   "material.verified_on is null but the block has started — links are recalled, not checked")
    else:
        verified_date = as_date(verified)
        if verified_date is None:
            f.error("G024", where, f"material.verified_on {verified!r} is not YYYY-MM-DD")
        elif gate_passed is None and (today - verified_date).days > STALE_LINKS_DAYS:
            # Only while the block is still ahead. Telling someone to re-check
            # links "before the block runs" on a gate they passed in week 2 is
            # noise that never goes away.
            f.warn("G025", where,
                   f"links last verified {(today - verified_date).days} days ago "
                   f"(over {STALE_LINKS_DAYS}) — re-check before the block runs")


def check_placement(placement, where: str, rung_passed, f: Findings) -> bool:
    """Returns True when placement has actually run."""
    if not isinstance(placement, dict):
        f.error("G010", where,
                "no placement block — the rung's starting point is unmeasured "
                "(older campaign: franklin-drill should add one and treat it as pending)")
        return False

    status = placement.get("status")
    if status not in PLACEMENT_STATUS:
        f.error("G011", where, f"placement.status {status!r} is not one of {sorted(PLACEMENT_STATUS)}")
        return False

    run_on = placement.get("run_on")
    result = placement.get("result")
    evidence = placement.get("evidence")

    if status == "pending":
        if run_on is not None or result is not None:
            f.error("G015", where,
                    "placement.status is pending but run_on/result are filled in")
        if rung_passed is not None:
            f.error("G016", where,
                    "gate is marked passed while placement is still pending — "
                    "the gate was sized by self-report, which is exactly what the schema refuses")
        return False

    # status == done
    if as_date(run_on) is None:
        f.error("G012", where, f"placement.status is done but run_on {run_on!r} is not a date")
    if result not in PLACEMENT_RESULT:
        f.error("G013", where,
                f"placement.result {result!r} is not one of {sorted(PLACEMENT_RESULT)}")
    elif result in ("partial", "solid") and is_blank(evidence):
        f.error("G014", where,
                f"placement.result is {result} with no evidence — a {result} result that names "
                "no missed items is a self-report wearing a quiz's clothes")
    return True


def check_gates(root: Path, today: dt.date, f: Findings) -> tuple[list[dict], bool]:
    """Returns (rungs, ladder_known). ladder_known is False when GATES.md could
    not be read far enough to know what the rungs are — in which case the
    exemplar cross-checks have nothing to compare against and must stay quiet."""
    path = root / "GATES.md"
    if not path.exists():
        f.error("G001", "GATES.md", "missing — franklin-drill reads this before serving any drill")
        return [], False

    doc = load_yaml_document(path, f, "G002")
    if doc is None:
        return [], False

    orientation = doc.get("orientation")
    if not isinstance(orientation, dict):
        f.error("G003", "GATES.md", "no orientation block — rung 1 has nothing to orient from")
    else:
        must_cover = orientation.get("must_cover")
        if not isinstance(must_cover, list) or not must_cover:
            f.error("G004", "GATES.md orientation", "must_cover is empty")
        covered = orientation.get("covered")
        if covered is not None and as_date(covered) is None:
            f.error("G005", "GATES.md orientation", f"covered {covered!r} is not null or YYYY-MM-DD")

    rungs = doc.get("rungs")
    if not isinstance(rungs, list) or not rungs:
        f.error("G006", "GATES.md", "no rungs")
        return [], False

    seen: set[str] = set()
    for index, rung in enumerate(rungs):
        if not isinstance(rung, dict):
            f.error("G007", f"GATES.md rungs[{index}]", "rung is not a mapping")
            continue

        raw_name = rung.get("rung")
        if raw_name is None:
            name = f"rungs[{index}]"
        elif isinstance(raw_name, str) and raw_name.strip():
            name = raw_name
        else:
            # A list or a number here is unhashable or unprintable downstream, and
            # the file's contract is to report rather than traceback.
            f.error("G007", f"GATES.md rungs[{index}]",
                    f"rung name {raw_name!r} is not a name — the ladder is keyed by it")
            name = f"rungs[{index}]"
        where = f"GATES.md {name}"
        if name in seen:
            f.error("G028", where, "duplicate rung name")
        seen.add(name)

        needed = rung.get("needed")
        if not isinstance(needed, bool):
            f.error("G008", where, f"needed {needed!r} is not a boolean")

        passed = rung.get("passed")
        if passed is not None and as_date(passed) is None:
            f.error("G027", where, f"passed {passed!r} is not null or YYYY-MM-DD")

        # A rung written off as not needed usually has no material, no exit test
        # and no box either. Reporting each of those as its own error buries the
        # one finding that matters under five that follow from it, so say the one
        # thing and stop: the gate was skipped without measuring, which is the
        # call the interview does not get to make.
        if needed is False:
            placement = rung.get("placement")
            result = None
            if isinstance(placement, dict):
                # Collapsing the dependent fields is not a reason to stop reading
                # the placement itself. A quiz recorded with no evidence or an
                # unparseable run_on is its own finding, and swallowing it here
                # would hide exactly the recording this checker exists to catch.
                check_placement(placement, where, passed, f)
                if placement.get("status") == "done":
                    result = placement.get("result")

            if result == "solid":
                f.warn("G029", where,
                       "placement came back solid, so record the gate as needed: true with "
                       "passed: <date> and the evidence — needed: false loses why it was skipped")
            elif result in ("zero", "partial"):
                f.error("G029", where,
                        f"placement came back {result} — the quiz says this rung is needed, "
                        "and needed: false overrides the measurement with an opinion")
            else:
                f.error("G029", where,
                        "needed is false with no completed placement behind it — skipping a gate "
                        "is placement's call to make, not the interview's. Set needed: true with "
                        "placement pending; if the quiz comes back solid the gate passes on the spot")
            continue

        for key in sorted(RUNG_REQUIRED - set(rung)):
            if key != "placement":  # placement gets its own, louder finding
                f.error("G007", where, f"missing required key '{key}'")

        placement_done = check_placement(rung.get("placement"), where, passed, f)

        time_box = rung.get("time_box")
        if is_blank(time_box):
            f.error("G018", where, "time_box is empty")
        elif placement_done and RANGE_RE.search(str(time_box)):
            f.warn("G017", where,
                   f"time_box {time_box!r} is still a range after placement ran — narrow it to a number")

        check_material(rung.get("material"), where, placement_done, as_date(passed), today, f)

        exit_test = rung.get("exit_test")
        if not isinstance(exit_test, dict):
            f.error("G026", where, "exit_test block missing")
        else:
            for key in ("explain", "exercise"):
                if is_blank(exit_test.get(key)):
                    f.error("G026", where, f"exit_test.{key} is empty")

    return [r for r in rungs if isinstance(r, dict)], True


# --------------------------------------------------------------------------
# exemplars/*/meta.yml
# --------------------------------------------------------------------------

def read_text_or_empty(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def check_exemplars(root: Path, rungs: list[dict], ladder_known: bool, today: dt.date,
                    f: Findings) -> None:
    exemplars_dir = root / "exemplars"
    if not exemplars_dir.is_dir():
        return

    by_sub_skill = {r.get("rung"): r for r in rungs if isinstance(r.get("rung"), str)}

    # Not every sub-skill is a gated rung. The judgment rung runs in parallel and
    # is scored as resolving predictions rather than passed by an exit test, so it
    # lives in PREDICTIONS.md and CURRICULUM.md and never appears under `rungs`.
    # An exemplar pointing at one is correct, and calling it a dangling reference
    # is the checker not knowing the method.
    parallel_prose = (read_text_or_empty(root / "PREDICTIONS.md")
                      + "\n" + read_text_or_empty(root / "CURRICULUM.md"))

    for entry in sorted(p for p in exemplars_dir.iterdir() if p.is_dir()):
        path = entry / "meta.yml"
        where = f"exemplars/{entry.name}"
        if not path.exists():
            f.error("M001", where, "no meta.yml")
            continue

        try:
            meta = yaml.safe_load(path.read_text(encoding="utf-8"))
        except (OSError, yaml.YAMLError) as exc:
            f.error("M002", where, f"meta.yml will not parse: {str(exc).splitlines()[0]}")
            continue
        if not isinstance(meta, dict):
            f.error("M002", where, "meta.yml is not a YAML mapping")
            continue

        if str(meta.get("id") or "") != entry.name:
            f.error("M003", where, f"id {meta.get('id')!r} does not match the directory name")

        if meta.get("kind") not in EXEMPLAR_KINDS:
            f.error("M004", where, f"kind {meta.get('kind')!r} is not one of {sorted(EXEMPLAR_KINDS)}")

        status = meta.get("status")
        if status not in EXEMPLAR_STATUS:
            f.error("M005", where, f"status {status!r} is not one of {sorted(EXEMPLAR_STATUS)}")

        sub_skill = meta.get("sub_skill")
        if is_blank(sub_skill) or not isinstance(sub_skill, str):
            f.error("M009", where,
                    "no sub_skill naming a rung — nothing ties this exemplar to the ladder")
            sub_skill = None

        prepped = meta.get("prepped")
        cold_until = meta.get("cold_until")
        prepped_date = as_date(prepped)
        cold_date = as_date(cold_until)

        if prepped is not None and prepped_date is None:
            f.error("M010", where, f"prepped {prepped!r} is not null or YYYY-MM-DD")
        if cold_until is not None and cold_date is None:
            f.error("M010", where, f"cold_until {cold_until!r} is not null or YYYY-MM-DD")

        if status == "cold" and cold_date is None:
            f.error("M006", where, "status is cold but cold_until is not set")

        if prepped_date and cold_date:
            gap = (cold_date - prepped_date).days
            if gap < COLD_DAYS_MIN:
                f.error("M007", where,
                        f"cold delay is {gap} days — the minimum is {COLD_DAYS_MIN}; "
                        "rebuilding from fresh memory is transcription")

        if status in ("rebuilt", "diffed"):
            rebuilds = root / "rebuilds" / entry.name
            if not rebuilds.is_dir() or not any(rebuilds.iterdir()):
                f.warn("M008", where, f"status is {status} but rebuilds/{entry.name}/ is empty")

        # ---- cross-checks against the ladder -------------------------------
        if sub_skill is None:
            continue
        if not ladder_known:
            # GATES.md is missing or unreadable. Every exemplar would report as a
            # dangling reference, which is one real fault restated once per file.
            continue
        rung = by_sub_skill.get(sub_skill)
        if rung is None:
            if names_slug(parallel_prose, sub_skill):
                # A parallel sub-skill: scored by prediction, with no gate to be
                # early for. The gate cross-checks below do not apply.
                continue
            f.error("X001", where,
                    f"sub_skill {sub_skill!r} matches no rung in GATES.md, and nothing in "
                    "PREDICTIONS.md or CURRICULUM.md names it either")
            continue

        gate_passed = as_date(rung.get("passed"))

        if prepped_date and rung.get("needed") is True and gate_passed is None:
            f.error("X002", where,
                    f"prepped on {prepped_date} but the '{sub_skill}' gate has not passed — "
                    "prep requires understanding the material first")

        if cold_date and gate_passed is None and rung.get("needed") is True:
            # Same guard X002 carries: where the rung needs no gate, there is no
            # gate for the exemplar to be waiting on.
            if cold_date <= today:
                f.error("X004", where,
                        f"ripe since {cold_date} while the '{sub_skill}' gate is still shut — "
                        "it is going stale where it sits")
            else:
                f.warn("X003", where,
                       f"ripens {cold_date} but the '{sub_skill}' gate has not passed — "
                       "re-date it or accept the staleness on purpose")


# --------------------------------------------------------------------------
# repo shape
# --------------------------------------------------------------------------

def check_layout(root: Path, rungs: list[dict], check_vcs: bool, f: Findings) -> None:
    if check_vcs:
        resolved = root.resolve()
        if not ((resolved / ".git").exists() or (resolved.parent / ".git").exists()):
            # Walking every ancestor was too generous: a campaign under a
            # git-tracked home directory looked tracked, and franklin-history
            # would then mine the dotfiles repo's log as this campaign's record
            # of sessions.
            owner = next((a for a in resolved.parents if (a / ".git").exists()), None)
            if owner is None:
                f.warn("R001", ".",
                       "not under git — franklin-history reads the log as its source of truth")
            else:
                f.warn("R001", ".",
                       f"the nearest git repo is {owner}, which is neither this campaign nor its "
                       "home — franklin-history would read that repo's log as this campaign's "
                       "session record. Run git init here")

    for name in ("README.md", "CURRICULUM.md", "SCHEDULE.md", "FAULTS.md"):
        if not (root / name).exists():
            f.warn("R002", name, "missing from the campaign")

    if any(as_date(r.get("passed")) for r in rungs):
        notes = root / "acquire" / "notes"
        if not notes.is_dir() or not any(notes.glob("*.md")):
            f.warn("X005", "acquire/notes/",
                   "a gate has passed but no acquisition notes are committed")


# --------------------------------------------------------------------------

def check_campaign(root: Path, today: dt.date, check_vcs: bool = True) -> Findings:
    f = Findings()
    check_campaign_yml(root, f)
    rungs, ladder_known = check_gates(root, today, f)
    check_exemplars(root, rungs, ladder_known, today, f)
    check_layout(root, rungs, check_vcs, f)
    return f


def looks_like_a_campaign(path: Path) -> bool:
    return (path / "campaign.yml").exists() or (path / "GATES.md").exists()


def discover(args) -> list[Path]:
    if args.all:
        home = Path(args.home).expanduser()
        if not home.is_dir():
            sys.stderr.write(f"no campaign home at {home}\n")
            sys.exit(2)
        # Not every directory under the home is a campaign. franklin-history
        # writes its reports to <home>/history/, and reporting that folder as a
        # campaign missing every file it was never going to have makes --all
        # exit 1 forever, however clean the real campaigns are. A path named
        # explicitly is still checked in full — there the user asserted it is a
        # campaign, and a missing campaign.yml is the finding.
        return sorted(p for p in home.iterdir()
                      if p.is_dir() and not p.name.startswith(".") and looks_like_a_campaign(p))
    roots = []
    for raw in args.paths:
        path = Path(raw).expanduser()
        if not path.is_dir():
            sys.stderr.write(f"not a directory: {path}\n")
            sys.exit(2)
        roots.append(path)
    return roots


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Check a Franklin-method campaign against the schema.")
    parser.add_argument("paths", nargs="*", help="campaign directories")
    parser.add_argument("--all", action="store_true", help="check every campaign under --home")
    parser.add_argument("--home", default=os.environ.get("FRANKLIN_HOME", "~/franklin"),
                        help="campaign home (default: $FRANKLIN_HOME, else ~/franklin)")
    parser.add_argument("--strict", action="store_true", help="treat warnings as failures")
    parser.add_argument("--json", action="store_true", help="machine-readable report")
    parser.add_argument("--today", help="override today's date, YYYY-MM-DD (for tests)")
    parser.add_argument("--no-vcs-check", action="store_true",
                        help="skip the git check, for a campaign not yet git init'ed")
    args = parser.parse_args(argv)

    if not args.paths and not args.all:
        parser.error("give a campaign directory, or --all")

    today = dt.date.today()
    if args.today:
        parsed = as_date(args.today)
        if parsed is None:
            parser.error("--today must be YYYY-MM-DD")
        today = parsed

    roots = discover(args)
    if not roots:
        sys.stderr.write("no campaigns found\n")
        return 2

    report = []
    failed = False
    for root in roots:
        f = check_campaign(root, today, check_vcs=not args.no_vcs_check)
        report.append({
            "campaign": str(root),
            "errors": f.errors,
            "warnings": f.warnings,
            "findings": f.items,
        })
        if f.errors or (args.strict and f.warnings):
            failed = True

    if args.json:
        print(json.dumps({"today": today.isoformat(), "campaigns": report}, indent=2))
        return 1 if failed else 0

    for entry in report:
        name = Path(entry["campaign"]).name
        if not entry["findings"]:
            print(f"{name}: clean")
            continue
        print(f"{name}:")
        for item in entry["findings"]:
            print(f"  {item['level']:<5} {item['code']}  {item['where']}: {item['message']}")
        print(f"  — {entry['errors']} error(s), {entry['warnings']} warning(s)")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
