# F26 Batch 99 — Rule-path and adversarial eligibility audit

## Newly executed evidence
{
  "enumerated_eligibility_cases": 97272,
  "invariant_violations": 0,
  "clear_leader_controls": 9,
  "clear_leader_controls_passed": 9,
  "historical_outcomes_replayed": 8,
  "historical_resolved": 8,
  "source_2025_verified": false
}

The enumeration checks only basic invariants (distinct, eligible, at most two finalists), NOT rule correctness. Passing those checks is not certification. Complete round-robin schedules with n=3–5 are exhaustive across game outcomes and nonempty eligibility masks; n=6 samples 1,024 deterministic outcome patterns with all 63 nonempty masks.

## Open policy questions
- The 2024 Big Ten official PDF is primary source for its year. 2025 policy identity is still not authenticated.
- Equal-percent ranked common opponents may require group treatment; do not silently choose.
- Commissioner draw and missing SportSource ratings cannot be reconstructed.
- Multi-ineligible top standings displacement must be adjudicated with independent expected fixtures.

## Follow-up
Batch100: derive rule-based oracle for ineligible No.1/No.2 configurations, fuzz state transitions, test grouped opponent sensitivity, and seek official 2025 policy.
