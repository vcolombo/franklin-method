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

This compares them directly: the keys and the enums, in both directions.
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


def reference_blocks() -> list[dict]:
    raw = REFERENCE.read_text(encoding="utf-8")
    return [yaml.safe_load(m.group(1)) for m in YAML_FENCE.finditer(raw)]


def main() -> int:
    problems: list[str] = []

    if not REFERENCE.exists():
        sys.stderr.write(f"missing {REFERENCE.relative_to(REPO)}\n")
        return 1

    chk = load_checker()
    raw_reference = REFERENCE.read_text(encoding="utf-8")
    blocks = reference_blocks()
    if len(blocks) != 3:
        sys.stderr.write(f"expected 3 yaml blocks in reference.md, found {len(blocks)}\n")
        return 1
    campaign, gates, meta = blocks

    # --- campaign.yml -------------------------------------------------------
    documented = set(campaign)
    if documented != chk.CAMPAIGN_KEYS:
        only_doc = sorted(documented - chk.CAMPAIGN_KEYS)
        only_code = sorted(chk.CAMPAIGN_KEYS - documented)
        if only_doc:
            problems.append(f"campaign.yml: documented but unknown to the checker: {only_doc}")
        if only_code:
            problems.append(f"campaign.yml: the checker knows keys the reference omits: {only_code}")
    missing_required = sorted(chk.CAMPAIGN_REQUIRED - documented)
    if missing_required:
        problems.append(f"campaign.yml: required keys absent from the example: {missing_required}")

    # --- GATES.md -----------------------------------------------------------
    if "orientation" not in gates or "rungs" not in gates:
        problems.append("GATES.md: the example needs both an orientation block and rungs")
    else:
        rung = gates["rungs"][0]
        missing = sorted(chk.RUNG_REQUIRED - set(rung))
        if missing:
            problems.append(f"GATES.md: the checker requires rung keys the example omits: {missing}")
        placement = rung.get("placement") or {}
        for key in ("status", "run_on", "result", "evidence"):
            if key not in placement:
                problems.append(f"GATES.md: placement.{key} is enforced but not documented")

    # --- meta.yml -----------------------------------------------------------
    for key in ("id", "kind", "sub_skill", "status", "prepped", "cold_until"):
        if key not in meta:
            problems.append(f"meta.yml: {key} is enforced but not documented")

    # --- the enums ----------------------------------------------------------
    enums = {
        "campaign status": chk.CAMPAIGN_STATUS,
        "placement status": chk.PLACEMENT_STATUS,
        "placement result": chk.PLACEMENT_RESULT,
        "exemplar kind": chk.EXEMPLAR_KINDS,
        "exemplar status": chk.EXEMPLAR_STATUS,
    }
    for label, values in enums.items():
        absent = sorted(v for v in values if v not in raw_reference)
        if absent:
            problems.append(f"{label}: values the checker accepts but the reference never shows: {absent}")

    if problems:
        sys.stderr.write("the prose schema and the checker disagree:\n")
        for p in problems:
            sys.stderr.write(f"  - {p}\n")
        return 1

    print("reference.md and check-campaign.py agree")
    return 0


if __name__ == "__main__":
    sys.exit(main())
