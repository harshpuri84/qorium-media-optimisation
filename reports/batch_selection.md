# Next batch: two DMEM steps, two model picks, one anchor

Regenerate with `python scripts/select_batch.py`. Outputs:

- `outputs/next_experiments.csv`: the four new recipes and the evidence for each.
- `outputs/plate_formulations.csv`, `outputs/plate_layout.csv`: dispensing volumes and the 96-well map.
- `outputs/recipe_manifest.csv`, `outputs/results_template.csv`: approvable run list and per-well results sheet.
- `reports/tables/batch_stability.csv`, `reports/tables/batch_threshold_stress.csv`: sensitivity reruns.
- `reports/tables/batch_alternatives.csv`: the batches considered and rejected.

## Recommendation

| Slot | Role | DMEM | RPMI-10 | X-VIVO 15 | AR5 | EUR/L base (scenario range) | Model estimate (80% range) | P(above E19) | Corr. with E19 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | DMEM step down (designed) | 40% | 22% | 21% | 17% | 178.19 (136.53 to 251.24) | 66.3 (48.4 to 84.1) | 0.26 | 0.576 |
| 2 | DMEM step up (designed) | 50% | 18% | 18% | 14% | 178.69 (132.99 to 250.23) | 62.5 (44.6 to 80.4) | 0.12 | 0.515 |
| 3 | Cheaper alternative (model) | 43% | 56% | 1% | 0% | 173.92 (107.40 to 240.45) | 65.9 (49.2 to 82.6) | 0.27 | 0.201 |
| 4 | Expected improvement (model) | 44% | 21% | 28% | 7% | 178.32 (134.64 to 234.92) | 69.1 (51.3 to 86.8) | 0.39 | 0.852 |
| Anchor | E19 re-run | 44.6 mL | 20.1 mL | 19.6 mL | 15.7 mL | 178.43 | 70.1 (observed 81.0) | | 1 |

Each formulation gets 11 wells: 55 formulation wells, 2 no-cell blanks and 2 heat-killed controls in the 60 interior wells, and a PBS ring on the edge.

- **Model estimate.** Posterior mean of the pooled-noise GP. The model shrinks E19's observed 81.0 to 70.1, so compare picks with 70.1. The forward test missed round 3 by up to 29 points, so these are conditional on the model.
- **P(above E19).** From the joint posterior of each pick and E19. It ignores shifts between batches.
- **Cost.** Model picks cost no more than E19 (EUR 178.43/L) at base prices and in at least 6 of 9 price scenarios (slot 3: 7, slot 4: 8). The designed steps may cost up to 1% more; slot 2 is EUR 0.26/L over at base prices and meets the ceiling in 6 of 9 scenarios, slot 1 in 3 of 9.

## How the batch was built

1. **Designed DMEM steps.** E19's RPMI-10 : X-VIVO 15 : AR5 ratios are held fixed and DMEM moves to 40% and 50%, rounded to whole percentages. DMEM is the only component with a clear signal, and the GP's DMEM length scale sits at its floor of 0.1, so the model claims a sharp peak near 44% that nobody has tested on either side.
2. **Pending first.** The E19 anchor and both designed steps are conditioned on as pending results before the model chooses, so the model picks look away from them.
3. **Cheaper alternative.** Highest posterior mean at least 2.5% below E19's cost.
4. **Expected improvement.** Highest expected improvement over the incumbent posterior mean (70.2), with every earlier slot pending.

Every pick keeps at least 5% of volume from every tested recipe, the single media and every other pick.

## Why each recipe

1. **DMEM 40%: 40 / 22 / 21 / 17.** Tests the lower side of the claimed peak. The model predicts 66.3, a 3.8-point drop from E19's 70.1. If viability holds, the peak is broader than the model thinks. FBS share 6.2%, slightly below E19's 6.5%.
2. **DMEM 50%: 50 / 18 / 18 / 14.** Tests the upper side. The model predicts 62.5. A strict E19 ceiling would exclude it by EUR 0.26/L, a gap smaller than the uncertainty in the FBS price, which is why the designed steps carry a 1% tolerance.
3. **Cheaper: 43 / 56 / 1 / 0.** Asks whether RPMI-10 can replace both serum-free media. Saves EUR 4.51/L (2.53%). The models disagree on it (51.9 with per-recipe noise against 65.9). It raises FBS to 9.9%, so it is not a step toward an animal-free medium. It depends on prices: at half-price FBS the cheaper pick becomes 44 / 26 / 19 / 11.
4. **Expected improvement: 44 / 21 / 28 / 7.** Keeps the round-3 DMEM level and moves volume from AR5 to X-VIVO 15. AR5 is the medium with no public price, so a pass here would remove the least certain cost from the problem. Correlation with E19 is 0.852, so it is the pick most likely to read close to the anchor.

## Batches considered

| Batch | Recipes | Why not chosen |
| --- | --- | --- |
| Earlier four-role GP batch | 44/26/19/11, 43/56/1/0, 37/33/30/0, 45/21/27/7 | Slot 1 was 0.981 correlated with E19 and predicted at 70.2 against 70.1: the model priced it at nothing and the screen could not resolve it. The explore pick depended on the model (it moved up to 40% of volume between fits) |
| Reviewer's diagnostic batch | E10, E14, 44/26/19/11, 43/56/1/0 | Re-running E10 and E14 would test whether their 40.6-point gap reproduces. E14's own readings agree closely (SD 2.70), which points to a technical failure; re-running it mostly teaches about the lab on that day, not about the medium. I rejected it and logged why in `docs/DECISIONS.md` |
| Chosen | 40/22/21/17, 50/18/18/14, 43/56/1/0, 44/21/28/7 | Tests the one signal in the data, keeps a cost test and an AR5 test, and uses idle wells for replicates |

## Robustness

**Model and price reruns.** Each row reruns the selection with one change. A cell is the volume (%) separating the rerun's pick from the main pick. The designed steps never move, so only the model slots are shown.

| Rerun | Slot 3 | Slot 4 |
| --- | --- | --- |
| GP with per-recipe noise | 23 | 34 |
| Noise scaled by reading count | 0 | 0 |
| Length-scale floor 0.05 | 1 | 4 |
| Length-scale floor 0.2 | 1 | 7 |
| Length-scale ceiling 3.0 | 0 | 0 |
| Three coordinates, without DMEM | 16 | 72 |
| Three coordinates, without X-VIVO 15 | 1 | 8 |
| Without E02 | 0 | 8 |
| Without E14 | 1 | 1 |
| E19 not counted as pending | 0 | 1 |
| Model picks allowed 1% over E19's cost | 0 | 9 |
| 8 other price scenarios (median) | 30 | 6 |

**Threshold stress.** One rule changes at a time.

| Setting | Slot 3 | Slot 4 |
| --- | --- | --- |
| Cheaper margin 0% | 30 | 1 |
| Cheaper margin 5% | 44 | 0 |
| Minimum gap 3% or 8% | 0 | 0 |
| Cost rule in 5 or 7 of 9 scenarios | 0 | 0 |
| Single media allowed | 0 | 0 |
| Model picks allowed 2% over E19's cost | 0 | 10 |

What this shows:

- **Slot 4 is stable** except under the per-recipe noise model (34%) and the fit without DMEM as a coordinate (72%). The direction, less AR5 and more X-VIVO 15 at about 44% DMEM, holds in every other rerun.
- **Slot 3 depends on prices and on the 2.5% margin.** At a 5% margin it becomes 0/92/0/8, nearly pure RPMI-10. The margin is a judgement call.
- **Coordinate choice matters.** Four fractions summing to one carry a redundant coordinate. Dropping DMEM hides the one component with signal inside the other three and changes the kernel's smoothness assumptions; dropping X-VIVO 15 changes little. I keep four coordinates with a length-scale floor; log-ratio coordinates are the standard alternative for the next round.

## Exploration and exploitation

The batch explores where the model is most confident and least tested: the claimed sharp DMEM peak. That is a designed contrast, not a model pick, because the simulation detected no advantage for any acquisition policy at the fitted noise level, and the blend picked from single noisy readings ended 4.7 to 7.9 points below the best available. The two model picks cover cost (slot 3) and the most promising change at the current DMEM level (slot 4). Eleven wells per arm address the noise directly.

## What the lab result would tell us

The plate is read only after the assay owner confirms it is valid against criteria set in advance. An invalid plate is repeated with the same five formulations.

| Valid plate shows | Next step |
| --- | --- |
| Viability falls off at 40% or 50% DMEM | The DMEM peak is real; search near 44% and relax the other three components |
| 40% and 50% within the screen of E19 | The peak is broader than the model thinks; widen the DMEM range next round |
| Slot 3 not excluded | Candidate for confirmation; not a step toward animal-free media |
| Slot 4 not excluded | AR5 may be replaceable by X-VIVO 15; confirm before acting on it |
| E19 far below 80 | Review preparation and assay conditions before the next round |

A blend passes the screen if its mean is no more than 5 points below the same-plate E19 at equal or lower cost. With 11 wells per arm, the 90% interval on that difference is about plus or minus 7 points (t, 20 degrees of freedom): a blend equal to E19 passes 89% of the time, one 10 points worse 11%. A pass means "not excluded"; a lead needs a mean above E19 by more than the interval. This plate measures variation within one cell and medium preparation only. Independent repeats come first; they set the size of the confirmation run.
