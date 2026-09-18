orientation:
  covered: null
  must_cover: []

rungs:
- rung: anchoring
  needed: true
  placement:
    status: pending
    run_on: null
    result: null
    evidence: ""
  material:
    text:
      - url: https://example.org/negotiation/anchoring
        note: the anchoring chapter
    verified_on: 2026-09-10
  time_box: "4 sessions"
  exit_test:
    explain: "what an anchor does to a counterparty's reservation price"
    exercise: ""
  passed: 2026-09-16
  notes: "user said their background here is essentially none, so we went ahead"

- rung: concession-pattern
  needed: true
  placement:
    status: done
    run_on: 2026-09-17
    result: solid
    evidence: ""
  material:
    text:
      - url: https://example.org
        note: the whole site
    video:
      - url: https://example.org/watch/concessions
        note: no segment given
    verified_on: null
  time_box: "2-6 sessions, set by placement"
  exit_test:
    explain: "why a shrinking concession pattern signals a floor"
    exercise: "run a scripted round and score the pattern against the transcript"
  passed: null
  notes: ""
