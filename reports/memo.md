---
title: "Next media batch: test the DMEM peak, not just chase it"
subtitle: "Technical memo, Head of Data Science case study"
author: "Harsh Puri"
date: "October 2026"
---

<p class="thesis">The data cannot tell us which blend is best. They point to one signal, DMEM near 44%, and a model that is confident about it without having earned that confidence. The next plate tests that signal directly, at about E19's cost, with a test set before the run that is allowed to come back inconclusive.</p>

## Recommendation

Five formulations, 11 randomised wells each: two designed DMEM steps around the best blend, two model picks, and a same-plate re-run of the best historical blend (E19).

| Slot | Role | DMEM | RPMI-10 | X-VIVO 15 | AR5 | EUR/L | Model estimate (80% range) | P(above E19) |
|---|---|---|---|---|---|---|---|---|
| 1 | DMEM step down | 40% | 22% | 21% | 17% | 178.19 | 66.3 (48.4 to 84.1) | 0.26 |
| 2 | DMEM step up | 50% | 18% | 18% | 14% | 178.69 | 62.5 (44.6 to 80.4) | 0.12 |
| 3 | Cheaper alternative | 43% | 56% | 1% | 0% | 173.92 | 65.9 (49.2 to 82.6) | 0.27 |
| 4 | Expected improvement | 44% | 21% | 28% | 7% | 178.32 | 69.1 (51.3 to 86.8) | 0.39 |
| Anchor | E19 re-run | 44.6% | 20.1% | 19.6% | 15.7% | 178.43 | 70.1; observed 81.0 | |

*The model shrinks E19's 81.0 to 70.1 because its posterior combines E19's readings with neighbouring blends and the fitted 11.8-point noise. The 80.2 re-run, if it was a separate run, suggests that shrinkage is too strong, which is one more reason the same-plate E19, not the model, sets the bar. Ranges are for one measured recipe mean under the model. P(above E19) uses the joint posterior and ignores shifts between batches.*

<figure class="float"><img src="figures/09_memo_batch_map.png" alt="Batch map"><figcaption>Picks (stars) against the 24 historical blends. Slots 1 and 2 sit on a line through E19: about the same ratios of the other three media (whole percentages), DMEM moved down and up.</figcaption></figure>

**Why these four.** DMEM share is the only blend variable with a clear signal. It stands for what differs between DMEM and RPMI: glucose (4.5 against 2 g/L), calcium (1.8 against 0.4 mM), bicarbonate (so pH under 5% CO2) and osmolality. This design cannot separate them, so each blend's pH and osmolality are recorded. Across rounds 1 and 2, blends at 29 to 33% DMEM scored 48 to 49%, E12 at 44.5% scored 68.1%, and blends at 60 to 77% scored 43 to 56%. Near 50% DMEM, E15 (49%) scored 55 and E05 (54.5%) 42, both at different ratios of the other three media; the 50% step tests the response along E19's dilution path instead. All six round-3 blends sit at 44 to 45% DMEM and score 67 to 81% while their other three components vary widely. The model's DMEM length scale sits at its floor: it believes viability changes sharply with DMEM, yet 40% and 50% at E19's ratios have never been tested. Slots 1 and 2 test that belief on one line through E19, with FBS held at 6.2 to 6.8% (E19 6.5%), so serum does not confound the contrast. Slot 3 asks whether RPMI-10 can replace both serum-free media, which are protein-containing (human albumin, transferrin), not animal-free; slot 4 whether X-VIVO 15 can replace AR5, the medium with no public price.

**Cost.** Model picks cost no more per litre than E19 in at least 6 of 9 FBS and AR5 price scenarios. The designed steps may cost up to 1% more: 50% DMEM is EUR 0.26/L over E19, a gap smaller than the uncertainty in the FBS price itself. Savings against E19 are small (up to 2.53%), so this ceiling screens candidates; it is not a business case.

**What I changed after review.** An earlier model pick, 44/26/19/11, was 0.981 correlated with E19 and predicted at 70.2 against E19's 70.1: a well the model priced at nothing. Reviewers flagged it; I replaced it and the exploration pick with the two DMEM steps.

## Problem, objective and constraints

The decision is which 3 to 5 formulations go on the next plate, when each PBMC round takes days, single results are noisy and only 24 historical blends exist. The goal is a next experiment that teaches the lab something whatever the result, not the best prediction.

**Objective.** Maximise mean PBMC viability at 72 hours (the next plate adds viable-cell recovery against a t = 0 count), subject to a cost per litre of prepared medium no higher than E19's under the same price scenario for model picks; the two designed steps may be up to 1% over at base prices. I chose a constraint over a weighted score because a lab manager can check a constraint by hand.

| Constraint or assumption | Value | Source or reason |
|---|---|---|
| Mixture | Fractions sum to 100%, whole percentages | 176,851 candidates |
| Spacing | Model picks at least 5% of volume from tested recipes and each other; designed steps 4.7% and 5.3% from E19 | No near-duplicates |
| Capacity | 5 formulations, 11 wells each | Brief caps at 5; 36 wells were idle |
| Endpoint | Viability at 72 h; this plate adds a t = 0 count and viable cells per mL | Viability is the only public endpoint |
| Prices | FBS from a search snippet; AR5 unpriced, set equal to X-VIVO 15 and varied to 2.02 times | `price_sources.csv` |
| Lab | Blends at 1% resolution; cells for 57 wells from one donor | To confirm |
| E19 re-run | The paper's 80.2% control comparison was a separate run from round 3 | Data give no dates; to confirm from the methods |

## What the data says

I used the public PBMC media-blending data from Narayanan et al. (2025): 24 blends of four commercial media in four rounds of six, 103 viability readings at 72 hours. The tables are complete and labelled, and a four-part mixture keeps cost and feasibility checkable. PBMCs are human immune cells, not bovine fibroblasts, and two of the four media carry 10% FBS: the method transfers to Qorium, the recipes do not.

| Finding | Number | So what |
|---|---|---|
| Round 3 beat every earlier round | 72.65% vs 39.98 to 50.65% | Recipe and lab day are confounded within the main data |
| E19's recipe was re-run in the paper's control comparison | 80.2% (n = 6, SD 7.5) | Assumed a separate run (the data give no dates): round 3 then partly reproduces, and the anchor measures what is left |
| Two near-identical blends disagree | E10 48.15% vs E14 7.52%, 2.60% of volume apart | E10 and E14 ran in different rounds, so a donor or preparation effect is plausible, but the data cannot tell it from real biology. E14 stays in the primary fit; without it the picks move at most 1% of volume while slot 4's estimate rises from 69 to 87, so the plate, not the fit, decides |
| Readings are noisy | pooled within-recipe SD 9.51 points | A 5-point gap is inside the noise of four readings |

<figure class="float"><img src="figures/10_memo_forward_test.png" alt="Forward-round test"><figcaption>Forward test of the GP: trained on earlier rounds, it missed round 3 by 26.8 points.</figcaption></figure>

**Models.** I compared a GP, a random forest, a Scheffe quadratic mixture model and the plain mean. On all 24 blends no model beats the mean on honest uncertainty (NLPD 4.44 for the mean against 5.93 for the GP). The GP's leave-one-out rank correlation of 0.61 comes from separating round 3 from the rest; within rounds 0 to 2 it is 0.11. The Scheffe model ranked no better than chance; the data do not show whether shape, coverage or confounding is to blame. The forward test is the honest one: every model under-predicted round 3 by 22 to 29 points. So the GP proposes candidates and the plate decides.

**Why a GP.** It returns an estimate and its uncertainty together, which batch selection needs to weigh "likely good" against "unknown". It handles small, noisy data through an explicit noise term, and pending picks can be conditioned on exactly, which makes batch selection simple. The random forest matched the GP's error and coverage (0.79), but its tree-spread interval is not a posterior I can condition on pending picks; the Scheffe model ranked no better than chance. BoTorch or Ax would add little on 24 points and four components; scikit-learn with explicit conditioning is easier to check (`check_gp.py`).

**Mixture coordinates.** Four fractions summing to one carry one redundant coordinate. Dropping X-VIVO 15 as a coordinate moves the model picks by 1 to 8% of volume; dropping DMEM moves them by up to 72%, because it hides the signal inside the other three. I keep all four with a floor on the length scales; log-ratio or orthonormal simplex coordinates are alternatives for the next round, once zero components are handled.

## How sure we are

| Source of uncertainty | How I handle it |
|---|---|
| Reading noise | The GP learns 11.83 points SD on a recipe mean, against a root-mean-square reading SEM of 4.97, and I use the larger figure; 11 wells per formulation narrow each comparison |
| Model, data, prices, rules | 19 reruns (noise models, length scales, three-coordinate fits, without E02 or E14, E19 not pending, 8 price scenarios) plus one-at-a-time rule changes |
| Batch shift | E19 re-run on the same plate; independent repeats before confirmation |

<figure class="float"><img src="figures/12_memo_pass_probability.png" alt="Screen pass probability"><figcaption>Chance a blend passes the 5-point screen. Eleven wells per arm sharpen the screen at no cost in formulations.</figcaption></figure>

**Robustness.** Across the 19 reruns the DMEM steps are fixed by design. Slot 3 moved by a median 16% of volume, mainly with prices. Slot 4 moved by a median 6%: 72% without DMEM as a coordinate, 34% under per-recipe noise, 10% or less otherwise.

**Simulation.** I ran 30 paired campaigns of 18 blends against two smooth synthetic truths at two noise levels, with the same rules and measurement errors for every policy. Random picks inside the rules ended 1.6 to 2.1 points from the best blend. Only UCB showed nominal evidence of beating random, at low noise (sign test p = 0.016 and 0.001; 16 exploratory tests, Bonferroni threshold 0.003). At the fitted noise of 11.8 points I detected no advantage for any policy, and the blend picked from single noisy readings sat 4.7 to 7.9 points below the best. That is why this plate spends wells on replicates and two slots on designed contrasts rather than four model picks. The simulation did not test that remedy.

**Exploration and exploitation.** Slots 1 and 2 are designed contrasts, not acquisition picks: they test the model's sharpest assumption, the DMEM length scale at its floor, where posterior SD (7.3 and 7.4) is also higher than at the model picks (5.5 to 7.2). It exploits with two model picks at the current DMEM level: one for cost, one for the most promising change. The anchor makes all four readable against the best blend on the same plate.

## From plate to decision

**1. Is the plate valid?** All 57 cell-containing wells use one donor, one thaw and logged FBS and medium lots. The assay owner checks missing wells, spread, blanks and the dead-cell gate against criteria set before the run. An invalid plate is repeated, not interpreted. A t = 0 read gives seeding count and viability. Harvest follows the source protocol, and pH is recorded after the blends equilibrate in the incubator. The source study pooled cultures before reading, so reading single wells is a protocol change to agree first.

**2. Read the DMEM steps.** The primary test, set before the run, is E19 minus the interpolated mean of the 40% and 50% steps. The model predicts 5.6 points with a standard error of about 3.5, so power is about 48%; each step alone has 24% and 59%. "Inconclusive" is an allowed result. This is a diagnostic, read regardless of cost.

**3. Screen the candidates.** Slots 3 and 4 pass if their mean is no more than 5 points below the same-plate E19 at equal or lower cost. With 11 wells per arm the 90% interval is about plus or minus 7 points (89% pass if equal, 11% if 10 points worse), assuming independent wells with the historical SD. A pass means "not excluded".

**4. Confirm, then decide.** One finalist, two at most, compared with concurrent E19 across independent cell and medium preparations on different days. This plate estimates variation within one preparation only; independent repeats come first and size the confirmation. Accept if the one-sided 95% lower bound on the difference stays above minus 5 points, with acceptable cost and quality, and with the business case agreed separately as cost per unit of acceptable output.

<figure class="float"><img src="figures/11_memo_plate_map.png" alt="Plate map"><figcaption>11 wells per formulation in randomised row blocks, PBS edge ring, blanks and heat-killed controls.</figcaption></figure>

| Valid plate shows | Next step |
|---|---|
| Curvature detected along the E19 path | Evidence of a local optimum near 44%; confirm, then search there |
| No curvature detected | Inconclusive or broader than the model thinks; widen the DMEM range |
| Slot 3 not excluded | Candidate for confirmation. It raises FBS to 9.9% (E19 6.5%), so it is not a step toward animal-free media |
| Slot 4 not excluded | AR5 may be replaceable by X-VIVO 15; confirm before acting on it |
| E19 far below 80 | Review preparation and assay conditions before the next round |

## How the strategy changes

| If | Then |
|---|---|
| Only 10 to 20 prior experiments | More space-filling picks, simpler kernels with priors, wider intervals. With 6 random points this GP was confidently wrong (round-1 coverage 17%) |
| Cheap assays are noisy | Screen widely with them, after paired calibration runs that measure the same cultures with both assays |
| Expensive assays are reliable | Reserve them for finalists, anchors and a spread of blends that keeps the cheap-to-expensive link estimable |
| Cost data is incomplete | Keep cost as a constraint across a price-scenario grid; buy the missing quote that moves the decision most |
| Components are categorical or constrained | One GP per category or a mixed kernel; limits as hard rules in the candidate generator |
| Experiments run in parallel batches | Choose jointly with pending-point conditioning, enforce spacing, re-run an anchor every batch |

## Qorium, risks and validation

- **Transfer.** Qorium grows adherent bovine skin fibroblasts on an animal-free process, so FBS and animal-derived insulin, transferrin and albumin are out. Human dermal fibroblasts grow well serum-free; for primary bovine skin fibroblasts that is an expectation to test, and the published gap is for bovine myoblasts (Kolkmann, Post et al. 2020). The process has two media, expansion (doublings per day) and matrix production (deposited collagen per area under ascorbate, over 2 to 4 weeks), plus animal-free attachment substrates and dissociation enzymes, with phenotype and passage tracked. What changes: a box of defined components per phase, growth and collagen endpoints, cost per gram of collagen. `reports/lab_plan.md` sketches that first plate.
- **Data limits.** No donor, well or pool identities, pooled readings and unrecorded FBS lots: historical noise and batch effects are estimated, not measured. This plate logs all three.
- **Model.** The forward-test miss is the main warning. If this plate's E19 lands far from 80, add a batch term before the next round.
- **Validation.** This batch succeeds if it reads the curvature contrast (detected, not detected or inconclusive) and leaves at least one blend for confirmation.

**Code, sources and method.** `run_all.sh` reproduces everything from public data (seed 20261002). Data: Narayanan et al. 2025, Nat. Commun. 16:6055. Method: Cosenza et al. 2022, Biotechnol. Bioeng. 119:2447.
