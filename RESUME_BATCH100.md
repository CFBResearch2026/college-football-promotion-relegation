# Batch 100 — Resume instructions

**Project paused after Batch 99 (2026-10-22).** Do not skip directly to simulation certification.

## Research objectives

1. Build an **independent** expected-result oracle for ineligible teams occupying or tied for first/second/third in the conference standings. Avoid deriving oracle expectations from the candidate engine itself.
2. Extend adversarial tests to compare exact **selected participants**, not merely structural invariants; record reproducible schedules, eligibility masks, decision traces and adjudication confidence.
3. Run both ranked-common-opponent interpretations on constructed equal-percentage standings, identify divergent outcomes and seek authoritative Big Ten clarification. Do not silently choose one.
4. Add explicit unresolved outputs for missing SportSource ratings and commissioner-administered draws. Never guess a winner.
5. Authenticate the actual **2025** Big Ten championship tiebreaker rules; record source URL, revision date, and exact clauses.
6. Re-run the **seven official 2025 scenarios** and the eighth outcome combination on any modified engine with complete reconstructed game inputs; compare against published official expectations and preserve full traces.
7. Deliver Batch 100 package with source code, fixtures, CSV outcomes, source register, change log, test log, unresolved issues and ZIP integrity verification.

## Required gates before general-purpose certification

- Governing rule provenance verified for 2025.
- All implemented rule branches have independent expected-result fixtures.
- No unexplained differential finalist sets.
- Eligibility special cases independently adjudicated.
- Missing ratings/draws return unresolved rather than invented finalists.
- Historical seven-scenario regression matched after the final code change.

## Separate research threads

The larger promotion/relegation project also has Phase 4 historical game/time sourcing and Phase 5 822-game schedule/media valuation work. This checkpoint focuses on the **F26 Big Ten championship-tiebreaker** research; do not treat it as a full backup of those other phases.
