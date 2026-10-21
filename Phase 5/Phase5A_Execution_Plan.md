# Phase 5A: Historical database certification

Date: 2026-10-17
Scope: Stage I 137-school pilot, followed by Stage II 899-program national model.

## Verified from official rulebook v1.0
- Ten ordered FBS competitive conferences, seven of size 14 and three of size 13.
- Twelve regular-season games per school, at least ten conference games, at most two adjacent-tier nonconference games.
- Top two from tiers 2-10 promoted; bottom two from tiers 1-9 relegated.
- Conference winning percentage is primary standings metric; postseason does not reverse movement.

## Initial quantitative checks
- 137 x 12 = 1,644 team-game appearances = 822 unique games if all games are played within the pilot.
- Seven 14-school tiers and three 13-school tiers total 137.
- Nine adjacent boundaries x two promotions = 18 promotions and 18 relegations each normal season.
- The 899-school total is a working count, not a verified annual classification total.

## Execution gates
1. Obtain authoritative 137-school pilot roster and season-by-season classification crosswalk.
2. Check unique program IDs, aliases, membership, tier assignments, and year-specific eligibility.
3. Normalize raw game records; preserve source rows, source URL, time type, and season type.
4. Match mirrored team-side records; flag duplicate games, score disagreements, missing opponent, and ambiguous neutral site.
5. Reconcile team-season records and conference W-L to the canonical game ledger.
6. Quantify coverage by year/classification; report open exceptions rather than treating missing as zero.
7. Certify Stage I before Stage II expansion.

## Status
Protocol audit executed; row-level certification blocked by source-export access. No game records are represented as certified.
