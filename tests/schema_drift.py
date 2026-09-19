#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["pyyaml"]
# ///
"""Fail when the prose schema and the checker stop agreeing.

`skills/franklin/reference.md` tells Claude what to write into a campaign.
`scripts/check-campaign.py` decides whether what got written is valid. Nothing
made those two describe the same thing, so a field added to one and not the
other would produce a campaign that satisfies the skill and fails the checker,
or worse, one the checker waves through because it was never taught the rule.

Keys and enums, compared exactly, in both directions.

Enums are read from the trailing comment on the field they belong to — a
`# a | b | c` beside the key — and parsed into a set. Searching the file for
each value as a substring is not enough: `cold` occurs inside `cold_until`, so
a status could be dropped from the documented enum and still look present.
"""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
REFERENCE = REPO / "skills" / "franklin" / "reference.md"
CHECKER = REPO / "scripts" / "check-campaign.py"
YAML_FENCE = re.compile(r"^```yaml\s*$(.*?)^```\s*$", re.S | re.M)


def load_checker():
    spec = importlib.util.spec_from_file_location("check_campaign", CHECKER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def blocks(raw: str, problems: list[str]) -> list[tuple[str, dict]]:
    """Every parseable yaml fence, as (source text, parsed mapping)."""
    found = []
    for i, m in enumerate(YAML_FENCE.finditer(raw)):
        source = m.group(1)
        try:
            doc = yaml.safe_load(source)
        except yaml.YAMLError as exc:
            problems.append(f"reference.md: yaml block {i} will not parse: "
                            f"{str(exc).splitlines()[0]}")
            continue
        if isinstance(doc, dict):
            found.append((source, doc))
    return found


def block_with(found, key: str, label: str, problems: list[str]):
    """Locate a block by what it contains, not by where it sits in the file."""
    matches = [b for b in found if key in b[1]]
    if not matches:
        problems.append(f"reference.md: no yaml block documents {label} (looked for '{key}')")
        return None, None
    if len(matches) > 1:
        problems.append(f"reference.md: {len(matches)} yaml blocks contain '{key}' — "
                        f"cannot tell which documents {label}")
        return None, None
    return matches[0]


def documented_enum(source: str, key: str, indent_any: bool = False):
    """The `# a | b | c` comment beside `key:`, as a set."""
    prefix = r"^\s*" if indent_any else r"^"
    pattern = re.compile(prefix + re.escape(key) + r":[^#\n]*#\s*(.+)$", re.M)
    m = pattern.search(source)
    if not m:
        return None
    return {v.strip() for v in m.group(1).split("|") if v.strip()}


def compare_enum(label: str, documented, accepted: set, problems: list[str]) -> None:
    if documented is None:
        problems.append(f"{label}: the reference documents no '# a | b | c' comment for it")
        return
    only_doc = sorted(documented - accepted)
    only_code = sorted(accepted - documented)
    if only_doc:
        problems.append(f"{label}: documented but rejected by the checker: {only_doc}")
    if only_code:
        problems.append(f"{label}: accepted by the checker but not documented: {only_code}")


def main() -> int:
    if not REFERENCE.exists():
        sys.stderr.write(f"missing {REFERENCE.relative_to(REPO)}\n")
        return 1

    problems: list[str] = []
    chk = load_checker()
    found = blocks(REFERENCE.read_text(encoding="utf-8"), problems)

    campaign_src, campaign = block_with(found, "subject", "campaign.yml", problems)
    gates_src, gates = block_with(found, "rungs", "GATES.md", problems)
    meta_src, meta = block_with(found, "sub_skill", "meta.yml", problems)

    # --- campaign.yml -------------------------------------------------------
    if campaign is not None:
        documented = set(campaign)
        only_doc = sorted(documented - chk.CAMPAIGN_KEYS)
        only_code = sorted(chk.CAMPAIGN_KEYS - documented)
        if only_doc:
            problems.append(f"campaign.yml: documented but unknown to the checker: {only_doc}")
        if only_code:
            problems.append(f"campaign.yml: the checker knows keys the reference omits: {only_code}")
        missing = sorted(chk.CAMPAIGN_REQUIRED - documented)
        if missing:
            problems.append(f"campaign.yml: required keys absent from the example: {missing}")
        compare_enum("campaign status", documented_enum(campaign_src, "status"),
                     chk.CAMPAIGN_STATUS, problems)

    # --- GATES.md -----------------------------------------------------------
    if gates is not None:
        if "orientation" not in gates:
            problems.append("GATES.md: the example needs an orientation block")
        rungs = gates.get("rungs")
        if not isinstance(rungs, list) or not rungs or not isinstance(rungs[0], dict):
            problems.append("GATES.md: the example needs at least one rung mapping")
        else:
            rung = rungs[0]
            missing = sorted(chk.RUNG_REQUIRED - set(rung))
            if missing:
                problems.append(f"GATES.md: the checker requires rung keys the example omits: {missing}")
            placement = rung.get("placement") or {}
            for key in ("status", "run_on", "result", "evidence"):
                if key not in placement:
                    problems.append(f"GATES.md: placement.{key} is enforced but not documented")
        compare_enum("placement status", documented_enum(gates_src, "status", indent_any=True),
                     chk.PLACEMENT_STATUS, problems)
        compare_enum("placement result", documented_enum(gates_src, "result", indent_any=True),
                     chk.PLACEMENT_RESULT, problems)

    # --- meta.yml -----------------------------------------------------------
    if meta is not None:
        for key in ("id", "kind", "sub_skill", "status", "prepped", "cold_until"):
            if key not in meta:
                problems.append(f"meta.yml: {key} is enforced but not documented")
        compare_enum("exemplar kind", documented_enum(meta_src, "kind"),
                     chk.EXEMPLAR_KINDS, problems)
        compare_enum("exemplar status", documented_enum(meta_src, "status"),
                     chk.EXEMPLAR_STATUS, problems)

    if problems:
        sys.stderr.write("the prose schema and the checker disagree:\n")
        for p in problems:
            sys.stderr.write(f"  - {p}\n")
        return 1

    print("reference.md and check-campaign.py agree")
    return 0


if __name__ == "__main__":
    sys.exit(main())
