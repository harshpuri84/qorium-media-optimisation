# Fix plan after the GPT-6 Astra review (2026-10-02)

**Historical plan.** The following triage records the 2 October snapshot. Later implementation and batch changes are recorded in [DECISIONS.md](DECISIONS.md); use [PLAN.md](PLAN.md) for current delivery status. Old slot numbers and unresolved items below are not the current recommendation.

Source: [review_gpt6_astra_2026-10-02.md](review_gpt6_astra_2026-10-02.md). The review was read-only and ran in Codex on GPT-6-Astra (medium) through Herdr.

I spot-checked findings 1, 9 and 11 against the code and README, and all three hold. Findings 2 to 8 and 10 come from reading the code and look correct, but I have not re-run them myself.

## Triage

| # | Reviewer severity | My severity | Verdict | Note |
|---|---|---|---|---|
| 1 | Blocker | Major | Agree | `believer()` sets `alpha=1e-6`, so the SEM-noise rerun loses every historical noise term after its first pick. The main pooled GP keeps its noise term in `WhiteKernel`, so the 4 headline recipes are largely unaffected. The SEM-noise sensitivity row is not. `normalize_y` also re-scales the data after each pretend result is added. |
| 2 | Major | Major | Agree | EI uses the noisy best of 81%. "P(beats E19)" compares against a fixed 70.1%. The comparison must use the joint posterior difference. |
| 3 | Major | Major | Agree | The explore score is integrated variance reduction over a 1,500-point sample. Rename it, test it with other seeds, and stop saying the simulation proves "one exploration slot". |
| 4 | Major | Major | Agree | Forward-round coverage is 0% in round 3 and 16.7% in round 1. Lead with this result, not a footnote. |
| 5 | Major | Major | Agree | Results on all 24 points stay primary. Drop E02 and E14 one at a time as a sensitivity check. Describe them as unexplained low results, not "failed runs". |
| 6 | Major | Minor | Partly agree | Add one higher-noise truth (SD 11.83). Label the simulation illustrative. Skip a full batch-shift model. |
| 7 | Major | Major | Agree | Add a guard so a selection with no eligible candidate stops with an error. Stress-test the 2.5%, 5% and 6/9 thresholds in one table. |
| 8 | Major | Minor | Agree | Label the economics provisional. Slot 2 saves only €4.51/L. Say so plainly. |
| 9 | Blocker | Blocker | Agree | 4 picks + E19 + DMEM-10 = 6 formulations, but the brief caps a batch at 5. Keep E19 and drop DMEM-10. Normalise E19 to 100% (44.7 + 20.1 + 19.6 + 15.7 = 100.1). |
| 10 | Major | Major | Agree | Slot 3 changes three fractions, not one. Describe it as a mixture contrast, not a DMEM effect. Test length-scale floors of 0.05 and 0.2. Cut "AR5 is not needed" and "one result settles it". |
| 11 | Blocker | Blocker | Agree | Memo, walkthrough and six-scenario answers do not exist yet. README lines 3 and 58 are stale. The folder sits inside the vault git repo and needs its own repo. |

## Ordered steps

| Step | Work | Files | Est. min | Verify |
|---|---|---|---|---|
| 1 | Fix the believer refit: freeze the y-scaling, keep historical noise, and give each pretend result explicit noise. Add a guard for a selection with no eligible candidate. | `compare_models.py`, `select_batch.py` | 45 | Posterior variance never rises after a pretend result is added. The SEM-noise rerun matches a hand-computed conditional for one point. |
| 2 | Compute P(beats E19) from the joint posterior: var(x) + var(E19) − 2 cov(x, E19). Label EI's incumbent. | `select_batch.py`, `batch_selection.md` | 20 | The probabilities move, and the new values are reported. |
| 3 | Capacity: 4 picks + E19 = 5 formulations. Drop the DMEM-10 control. Normalise E19. | `select_batch.py`, `batch_selection.md`, `DECISIONS.md` | 15 | The CSV holds 4 rows. The memo states 5 formulations in the batch. |
| 4 | Evidence pass: put all-data results first, drop E02 and E14 one at a time, test length-scale floors of 0.05/0.1/0.2, run 3 explore seeds, add the 11.83-SD simulation truth. | `compare_models.py`, `select_batch.py`, `model_comparison.md` | 60 | One sensitivity table shows which picks survive. |
| 5 | Threshold stress table: discount 0/2.5/5%, gap 3/5/8%, scenarios 5/6/7 of 9. | `select_batch.py` | 20 | The table shows how far each slot shifts. |
| 6 | Rewrite claims: remove "failed run", "settles it", "AR5 not needed" and "simulation proves". Mark the economics provisional. | `model_comparison.md`, `batch_selection.md`, README | 25 | No line makes a claim beyond what the evidence shows. |
| 7 | Package: write the memo (≤4 pages, including the six scenarios), the walkthrough script, a one-command runner, and a separate git repo. Report hours actually spent. | new `reports/memo.md`, `run_all.sh`, README | 90 | A clean `.venv` rerun reproduces the CSV. The memo fits on 4 pages. |

Total is about 4.5 hours. Steps 1 to 3 change the recommendation, so they come first. Steps 4 to 6 change how much we claim. Step 7 is the deliverable.

## Interview questions to prepare

From the review, Section C:

1. Why trust a GP with 0% round-3 coverage?
2. What does "51% better than E19" mean?
3. Did the simulation validate these four recipes?
4. Why exclude near-duplicates when a replicate might be worth more?
5. What does PBMC viability tell Qorium?
