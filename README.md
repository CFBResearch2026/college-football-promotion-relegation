# F26 College Football Research — GitHub Checkpoint

**Paused after Batch 99 | 2026-10-22 | Next: Batch 100**

This is a versioned research snapshot, **not** a certified Big Ten championship prediction service. It preserves the experimental engines, 2025 historical scenario inputs, validation outputs, rule-source questions, and reproducibility trail. Do not overwrite the raw source artifacts when developing Batch 100.

## State of research

- 2025 Big Ten conference schedule reconstructed: 81 conference games, 18 schools, 9 games per school (Batch 98).
- Batch 98 candidate: 7/7 official published scenarios matched using reconstructed inputs; eighth possible final-week combination also evaluated.
- Batch 99: 97,272 game-outcome/eligibility combinations checked for **structural invariants only** (no ineligible or duplicate finalists, maximum two); zero violations. This does **not** verify rule-correct selections.
- Batch 99: 9/9 clear-leader exclusion controls passed; eight historical combinations replayed and resolved. The Batch 99 replay was not a new 7/7 official expected-result certification.
- Complete governing 2025 rule document is not authenticated. Equal-percentage ranked-common-opponent treatment, multiple ineligible leading teams, SportSource rating inputs, and commissioner-draw handling remain unresolved.
- General-purpose simulation certification: **ON HOLD / PROVISIONAL**. Media audience causal-premium estimation is also unresolved.

## Repository layout

- `engine/`: multiple **experimental** versions, including the Batch 99 eligibility candidate. Do not assume all are equivalent or production-ready.
- `data/historical/`: 2025 conference schedule, official-scenario reference table, replay inputs and results.
- `validation/`: executed tests, fixtures, random/adversarial outputs and logs.
- `governance/`: rule interpretations, unresolved policy gaps, certification gates.
- `reports/`: Batch 99 narrative and machine-readable summary.
- `FILE_MANIFEST_SHA256.csv`: integrity hashes of copied files.
- `RESUME_BATCH100.md`: exact handoff plan.

## How to resume

Start with `RESUME_BATCH100.md`, then read `reports/F26_Batch99_Report.md`, `reports/F26_Batch99_Summary.json`, `governance/F26_Batch99_Rule_Gap_Register.csv`, and `validation/F26_Batch99_Rule_Path_Audit.csv`. Use the engine in `engine/F26_Batch99_Eligibility_Selection_Engine_CANDIDATE.py` as the **candidate baseline**, not an authoritative rule implementation.

This checkpoint is a curated subset of the **135-file** Batch 99 research directory. Keep the complete `CFB_F26_Batch99.zip` separately as the immutable full-fidelity archive. Files in this checkpoint retain their original Batch 99 names.

## Provenance and caution

The Big Ten 2024 rules are a historical reference, not independently proven to govern the 2025 season unchanged. See `governance/F26_Batch99_2025_Rules_Source_Review.md`. All results should retain original source and evidence labels. Do not present invariant testing as independent adjudication of participant correctness.
