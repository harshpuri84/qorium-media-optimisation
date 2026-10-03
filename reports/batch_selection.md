# Next batch: four blends plus one anchor

Regenerate with `python scripts/select_batch.py`. Outputs:

- `outputs/next_experiments.csv`: the four recipes and the evidence for each.
- `outputs/plate_formulations.csv`: dispensing volumes for all five formulations.
- `reports/tables/batch_stability.csv`: sensitivity reruns.
- `reports/tables/batch_threshold_stress.csv`: threshold stress tests.

## Recommendation

The batch has five formulations, the most the brief allows: four new blends plus a re-run of E19.

| Slot | Role | DMEM | RPMI-10 | X-VIVO 15 | AR5 | EUR/L base (scenario range) | Predicted viability (80% range of measured mean) | P(true viability above E19) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Exploit | 44% | 26% | 19% | 11% | 177.69 (130.65 to 245.04) | 70.2 (53.6 to 86.8) | 0.54 |
| 2 | Cheaper alternative | 43% | 56% | 1% | 0% | 173.92 (107.40 to 240.45) | 65.9 (49.2 to 82.6) | 0.27 |
| 3 | Explore | 37% | 33% | 30% | 0% | 176.82 (129.78 to 223.86) | 60.1 (41.1 to 79.2) | 0.12 |
| 4 | Expected improvement | 45% | 21% | 27% | 7% | 178.31 (133.96 to 235.59) | 69.1 (51.5 to 86.7) | 0.38 |
| Anchor | E19 re-run | 44.6 mL | 20.1 mL | 19.6 mL | 15.7 mL | 178.43 | historical 81.0 | n/a |

The anchor volumes are per 100 mL and sum to exactly 100.0 mL. The published E19 recipe sums to 100.1%, so it was normalised before rounding.

How to read the table:

- **Cost.** Every pick meets the base ceiling of EUR 178.43/L and the cost rule in at least 7 of 9 price scenarios. The prices are provisional (see `reports/model_comparison.md`).
- **Predicted viability.** This is the GP's posterior mean. The 80% range is for one measured recipe mean. The forward-round check shows these ranges miss shifts between rounds of up to 29 points. Treat them as conditional on the model, not as forecasts.
- **P(true viability above E19).** This comes from the joint posterior of each pick and E19, so it includes E19's own uncertainty and the correlation between the two. It is a probability under the model. It does not account for a batch effect between rounds. Slot 1 is 0.981 correlated with E19 under the model, so its 0.54 means the model cannot tell the two apart. It is not evidence that slot 1 is better. Treating the two as independent would give 0.51, 0.29, 0.17 and 0.45.

![Next batch](figures/08_next_batch.png)

The figure projects the recipes onto DMEM and X-VIVO 15. Two points that look close here can still differ in RPMI-10 and AR5.

## Why each recipe

1. **Exploit: 44 / 26 / 19 / 11.** This is the highest posterior mean among recipes at least 5% of volume away from every tested recipe. It keeps the round-3 DMEM level and moves volume from AR5 to RPMI-10. Expected viability is level with E19 (P = 0.54), at EUR 0.74/L less. It is the most stable pick: unchanged in 9 of 15 reruns, median shift 0%. The per-recipe noise model moves it 26% of volume. The model treats RPMI-10 and AR5 as interchangeable (both length scales sit at the 10.0 ceiling), so this pick tests that assumption rather than relying on it.

2. **Cheaper alternative: 43 / 56 / 1 / 0.** This is the highest posterior mean among recipes at least 2.5% below the ceiling. It saves EUR 4.51/L at base prices, which is small. Its value is that it contains almost no serum-free media, so if it performs, AR5's unknown price stops mattering. The models disagree on it: 65.9% for the main GP, 51.9% with per-recipe noise. One measurement will narrow that, but will not settle it given noise of about 12 points. This pick depends on prices. At half-price FBS the cheaper pick becomes 44 / 31 / 19 / 6.

3. **Explore: 37 / 33 / 30 / 0.** Of all recipes that could still be the best, this one most reduces posterior variance across that whole region. Every candidate in the region is scored, with no sampling. Moving DMEM from 44% to 37% also changes the other three fractions, so it is a mixture contrast against the round-3 cluster, not a test of DMEM alone. It checks whether good results extend beyond the narrow 43.96% to 44.94% DMEM band of round 3. It is not stable across model variants: 2 of 15 reruns unchanged, and the no-E14 model moves it 40% of volume. That is expected, because exploration chases uncertainty and uncertainty depends on the model. Its expected viability is the lowest of the four, and that is the cost of the information.

4. **Expected improvement: 45 / 21 / 27 / 7.** This has the highest expected improvement over the incumbent posterior mean (70.2%) while slots 1 to 3 are pending. It shifts volume from AR5 to X-VIVO 15 at the round-3 DMEM level. It has the largest upside under alternative fits: 77.6% with per-recipe noise and 86.2% without E14. It moves at most 12% of volume across all 15 reruns.

## Exploration and exploitation

- **Slots 1 and 4 exploit.** They stay near the best region and try to beat E19.
- **Slot 2 trades** a little expected viability for lower cost and for less exposure to AR5's unknown price.
- **Slot 3 explores.**

In the simulation, with the same eligibility rules for every policy, GP policies beat random at low noise, but at the fitted noise of 11.83 points no policy stands out, and the blend the lab would pick from noisy results ends 5 to 10 points below the best available. The four-role split is therefore a design choice for readability and cost coverage, not a simulation result. The simulation's clearer message is that confirmation, not candidate choice, limits the outcome at this noise level.

Batch-level checks:

| Check | Result |
| --- | --- |
| Smallest gap between two picks | 9.0% of volume |
| Smallest gap to any tested recipe | 5.9% (slot 1 vs E24) |
| AR5 share in the picks | 11%, 0%, 0%, 7% |

## Robustness

**Model and price reruns.** Each row reruns the full selection with one change. A cell is the volume (%) separating the rerun's pick from the main pick.

| Rerun | Slot 1 | Slot 2 | Slot 3 | Slot 4 |
| --- | --- | --- | --- | --- |
| GP with per-recipe noise | 26 | 23 | 31 | 12 |
| Length-scale floor 0.05 | 1 | 1 | 11 | 5 |
| Length-scale floor 0.2 | 7 | 1 | 27 | 7 |
| Length-scale ceiling 3.0 | 0 | 0 | 0 | 2 |
| Without E02 | 7 | 0 | 4 | 9 |
| Without E14 | 7 | 1 | 40 | 7 |
| Anchor treated as pending | 0 | 0 | 0 | 1 |
| 8 other price scenarios (median) | 0 | 25 | 21 | 7 |

**Threshold stress.** One selection rule changes at a time, with the GP and prices fixed.

| Setting | Slot 1 | Slot 2 | Slot 3 | Slot 4 |
| --- | --- | --- | --- | --- |
| Cheaper margin 0% | 0 | 25 | 1 | 2 |
| Cheaper margin 5% | 0 | 44 | 1 | 1 |
| Minimum gap 3% | 2 | 0 | 0 | 0 |
| Minimum gap 8% | 4 | 0 | 1 | 0 |
| Cost rule in 5 of 9 scenarios | 0 | 0 | 0 | 0 |
| Cost rule in 7 of 9 scenarios | 0 | 0 | 1 | 0 |
| Single media allowed | 0 | 0 | 0 | 0 |

What the robustness checks show:

- Slots 1 and 4 hold under most changes. The largest moves come from the per-recipe noise model (26% and 12%).
- Slot 2 depends on prices and on the 2.5% margin. At a 5% margin it becomes 0 / 92 / 0 / 8, which is nearly pure RPMI-10. The 2.5% margin is a judgement call. A reviewer can fairly ask for a different number.
- Slot 3 depends on the model, especially on whether E14 is in the fit. It does not depend on the thresholds.
- Excluding single media is an operational rule. They were measured on a separate comparison sheet whose context does not fully match the main data. Allowing them moves no pick.

## Model facts to state in the memo

- **Length scales:** DMEM 0.1 (at its floor), RPMI-10 10 and AR5 10 (both at the ceiling), X-VIVO 15 0.326. A short length scale means the model expects viability to change quickly along that component. The model is effectively two-dimensional. It sees a sharp DMEM response, driven by the round-3 cluster, and treats RPMI-10 and AR5 as interchangeable. Slots 1, 2 and 4 all move volume out of AR5, so the batch tests that assumption. Capping the ceiling at 3.0 moves the picks by at most 2% of volume.
- **Noise:** 11.83 points SD on a recipe mean, against a typical reading SEM of 4.97. The difference covers run-to-run variation plus anything the model gets wrong.
- **Ranking, not forecasting:** the forward-round check missed round 3 by 22 to 29 points. Compare the picks with the E19 re-run on the same plate, not with E19's historical 81%.

## What the lab result would tell us

The plate is read only after the assay owner confirms it is valid against criteria set in advance (missing wells, spread, anchor viability, preparation records). An invalid or inconclusive plate is repeated with the same five formulations. On a valid plate:

| Outcome | Interpretation |
| --- | --- |
| E19 near its historical 81% and slot 1 passes the screen | The round-3 region holds up on a new plate. Some AR5 volume may move to RPMI-10; confirmation decides |
| E19 well below 81% | Judge the picks against this plate's E19. Review preparation and assay conditions; one low anchor does not prove a historical batch effect |
| Slot 3 close to slots 1 and 4 | Good results are not confined to the 44% DMEM band. Widen the search next round |
| Slot 2 passes the screen | RPMI-10 can stand in for the serum-free media in this system. It raises FBS to 9.9% (E19: 6.5%), so it is not a step toward an animal-free medium |
| Slot 4 passes or beats E19 | Moving volume from AR5 to X-VIVO 15 is a lead |

The screen passes a blend whose mean is no more than 5 points below the same-plate E19, at equal or lower cost. Four wells per formulation from one cell and one medium preparation give about plus or minus 11 points on that difference, so the screen only filters. One finalist, two at most, goes to a paired confirmation against concurrent E19 across independent preparations, sized from the preparation-level variance the pilot measures. For Qorium, PBMC viability and FBS-supplemented media only stand in for the method. A real campaign would use an approved animal-product-free ingredient list and Qorium's own cell expansion, collagen output and quality assays.
