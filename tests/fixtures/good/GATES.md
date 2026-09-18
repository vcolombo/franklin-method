# Gates

Orientation, then one block per rung. `franklin-drill` reads this before serving
any drill.

```yaml
orientation:
  covered: 2026-09-14
  must_cover:
    - "what submerged coiling is — the loop from prepared reed to closed wall"
    - "the mechanisms it buys: tension control, splice placement, rim lock"
    - "the honest case against: slower than stitched work, and no advantage above the waterline"
    - "how the five rungs map onto a finished basket"
  held_back: "r02 — the Nakamura essay argues for wet-work; reconstructing it needs recall"

rungs:
- rung: coil-tension
  needed: true
  placement:
    status: done
    run_on: 2026-09-15
    result: partial
    evidence: "missed splice overlap direction and why tension drifts at the turn"
  material:
    text:
      - url: https://example.org/weaving/coiling-basics
        note: the coiling chapter, tension section
    video:
      - url: https://example.org/watch/coil-tension
        segment: 04:10-11:30
        note: hands-on tension at the turn
    interactive:
      - url: https://example.org/weaving/exercises/coiling
    deeper:
      - url: https://example.org/papers/reed-mechanics
    verified_on: 2026-09-15
  time_box: "3 sessions"
  exit_test:
    explain: "why tension drifts at the turn, and what corrects it, unaided"
    exercise: "coil a 10cm base that holds its shape when squeezed"
  passed: 2026-09-20
  notes: ""

- rung: splice-placement
  needed: true
  placement:
    status: pending
    run_on: null
    result: null
    evidence: ""
  material:
    text:
      - url: https://example.org/weaving/splices
        note: splice types and where each belongs
    video:
      - none_found: "searched; every result is stitched work, which splices differently"
    verified_on: null
  time_box: "2-6 sessions, set by placement"
  exit_test:
    explain: "where a splice may and may not fall on a load-bearing coil"
    exercise: "splice mid-wall and load the basket to failure; the splice must not be the failure"
  passed: null
  notes: ""
```
