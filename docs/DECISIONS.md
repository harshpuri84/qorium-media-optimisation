# Data and modelling decisions

## 2026 10 02 Starting dataset

Selected the `MediaBlendingStudies` sheet in the PBMC workbook accompanying Narayanan et al. (2025). It offers 24 experiments, a low-dimensional constrained mixture and repeated readings. This choice makes noise, feasibility and experiment selection assessable within the timebox. It sacrifices direct alignment with the 2022 muscle-cell ingredient study. It does not establish transfer to Qorium cells or production endpoints.

Sources: [article](https://www.nature.com/articles/s41467-025-61113-5), [dataset](https://springernature.figshare.com/articles/dataset/Experimental_Data_Collected/27715134), [2022 reference repository](https://github.com/ZacharyCosenza/GradStuff_Cosenza).

The current 2022 repository README describes test data, its solver generates synthetic inputs, and the saved text files have no headers. Those arrays remain unverified reference material. A future switch requires a documented component order, assay mapping, outcome transformation and cost interpretation.

## Mixture handling

Interpret the four media values as volume percentages, supported by the article's sum-to-100% constraint. Accept source totals within 0.11 percentage points of 100 as rounding discrepancies. Retain the original values and normalise to sum one for analysis. Larger discrepancies stop preparation of the training table. The tolerance is a processing assumption, not an assay tolerance.

The raw sheet labels the first component `DMEM`, while the comparison sheet uses `DMEM-10`. The methods describe DMEM and RPMI basal media supplemented with 10% FBS and 1% Penicillin-Streptomycin. Use the blending-sheet label in data; prepared-media price inputs must include the relevant supplementation. Do not infer exact supplier specifications beyond what is documented.

## Outcome and repeated readings

The primary endpoint is viability percentage after 72 hours. Recompute experiment means from the available `Via1` through `Via5` values and reconcile with the supplied average. Missing reading slots are missing, not zero. Calculate sample SD and SEM, with an explicit provisional independence assumption for SEM. Source donor and pool identities are not provided. The paper's described pooling and replicate counts do not fully resolve the workbook's two-to-five readings per experiment.

No low/high fidelity pairing is available in this subset. Do not label the repeated readings as separate fidelity levels. Viability alone does not establish preservation of immune-cell composition; the article studies that in a separate cytokine phase.

## Controls and separate biological systems

Export the separate comparison sheet unchanged and exclude it from initial model fitting. Its AR5 row totals 200%, the XVIVO row has a missing fraction, and the reported optimal blend totals 100.1%. Flag these source facts rather than correcting likely typographical errors. The comparison labels and experimental context also differ from the main training sheet.

Retain the cytokine sheet and K. phaffii workbook as separate sources. Do not combine distinct endpoints, protein products or cell systems into one training table without a justified transfer model.

## Cost and unknown inputs

Use costs per litre of prepared medium. Price fields start empty. Do not substitute zero or the 2022 paper's relative cost weights. Unknown prices yield unknown blend costs. User-supplied estimates must have a common currency, provenance and an explicit observed/estimate/hypothetical classification. Final optimisation needs prices plus a stated ceiling or reference.

## 2026 10 02 Exploratory analysis

Completed five descriptive figures, component-association sensitivity tables and all pairwise recipe distances. Analysis retains all 24 formulations, including E02 and E14 with mean viability below 10%. Their reported readings support the low means; the source provides no grounds for silently excluding them.

Final-round recipes cluster at 43.96% to 44.94% DMEM, while other component shares still vary. The highest observed formulation is E19 at 81% mean viability, but reading variation and unknown independence prevent a firm ranking of the leading recipes. No significance tests or biological confidence intervals are claimed.

E10/E14 require only 2.60% of total volume to be reallocated between components, but their observed means differ by 40.63 percentage points. Preserve this pair for model diagnostics and sensitivity analysis. A model should not infer a sharp response solely to fit this discrepancy without considering observation noise or unrecorded batch factors.

Next modelling should compare conservative pooled and recipe-specific noise assumptions, inspect forward-round performance, and evaluate recommendation stability. Raw component correlations are descriptive because the fractions sum to one and recipe selection was adaptive. The data do not establish an independent DMEM effect or a global optimum. Cost scenarios and a reference ceiling remain the next project milestone.

## 2026 10 02 Cost estimates

Sourced EUR list prices for the basal media, FBS, Penicillin-Streptomycin and X-VIVO 15 (`data/inputs/price_sources.csv`). Prepared DMEM and RPMI include 10% FBS and 1% Penicillin-Streptomycin by volume. AR5 (CellGenix 20807) has no findable price, so its base case equals X-VIVO 15 per litre, labelled hypothetical.

At base prices the four media cost EUR 168.45 to 181.00 per litre, and the 24 historical blends span only EUR 172.49 to 180.98 per litre. Cost and viability are uncorrelated (r = 0.05). Cost only separates recipes when FBS or AR5 prices move: across FBS 0.5x to 1.5x and AR5 1.0x to 2.02x, the E19 blend ranges EUR 134.9 to 250.9 per litre. Recommendations must therefore be checked across `cost_scenarios.csv`, and a real AR5 quote is the most valuable missing input.

## 2026 10 02 Cost rule, dispensing and model choice

Cost rule: a candidate must cost no more per litre than PBMC-E19 under the same price scenario. Dispensing: whole-percent fractions summing to 100%. Both are assumptions for the memo, not lab-confirmed limits.

Model choice: GP (Matern 5/2, length-scale floor 0.1, pooled noise) with batch EI by kriging believer. Without E02/E14 it has the best leave-one-out RMSE (7.56 pts vs 13.15 for the mean); the Scheffe quadratic ranks no better than chance. In simulation, batch BO reaches lower regret than random and exploit-only sampling on both a GP and a Scheffe synthetic truth. All models under-predict round 3 by 22 to 29 points, so E19 is re-run as an anchor control outside the four slots. Detail: `reports/model_comparison.md`.

## 2026 10 02 Batch selection

Four slots chosen in sequence with kriging believer: exploit, cheaper alternative (at least 2.5% under the ceiling), explore (largest variance reduction over recipes that could still be best), expected improvement. Every pick meets the base cost rule and the rule in at least 6 of 9 price scenarios, and differs by at least 5% of volume from historical recipes, the four single-media controls and each other. Single media are treated as already tested because the comparison sheet measured them; an earlier variance-only explore rule picked 5/95/0/0, almost pure RPMI-10, which that sheet already shows at about 49.5%. E19 and DMEM-10 alone run as plate controls outside the four slots. Detail: `reports/batch_selection.md`.

## 2026 10 02 Changes after external review

A read-only GPT-6 Astra review (`docs/review_gpt6_astra_2026-10-02.md`) led to these changes (`docs/FIX_PLAN.md` steps 1 to 6):

- **Pending-point conditioning.** The GP now computes posteriors explicitly from the fitted kernel, with fixed y scaling and a per-point noise vector. Pending picks keep every historical noise term. `scripts/check_gp.py` verifies agreement with sklearn, an unchanged mean and a non-increasing variance. The fix changed slot 3 (37/31/31/1 to 37/28/30/5) and slot 4 (45/21/34/0 to 45/21/27/7).
- **Incumbent and comparison.** EI improves on the incumbent posterior mean, not the noisy observed maximum of 81%. P(above E19) uses the joint posterior of each pick and E19.
- **Capacity.** The batch is four picks plus an E19 re-run: five formulations, the brief's maximum. The DMEM-10 control was dropped. E19 volumes are normalised to 100.0 mL per 100 mL.
- **Evidence.** All-data results are primary. E02 and E14 are described as unexplained low outcomes and are withheld one at a time only as a sensitivity check. The simulation adds a high-noise case (11.83) and the deployed four-role policy, and is labelled illustrative.
- **Thresholds.** The 2.5% cheaper margin, 5% minimum gap, 6-of-9 scenario rule and single-media exclusion are judgement calls, now stress-tested in `reports/tables/batch_threshold_stress.csv`. An empty eligible set now raises an error instead of returning an arbitrary recipe.

## 2026 10 02 Changes after Fable 5.1 review

`docs/review_fable51_2026-10-02.md` judged the fixes sound and the work ready for the memo after wording fixes. Applied:

- The explore score now covers the whole plausible-optimum region in chunks, with no 1,500-point sample, and the region threshold uses the incumbent posterior mean. Slot 3 moved from 37/28/30/5 to 37/33/30/0. The explore-seed reruns were removed because the score no longer samples.
- Added a length-scale ceiling of 3.0 as a sensitivity variant. RPMI-10 and AR5 sit at the 10.0 ceiling in the main fit; the picks move by at most 2% under the cap.
- The mean-only leave-one-out Spearman is now blank in the CSV, matching the report.
- Wording: exploit-only is "no better than random, worse on the Scheffe truth". The simulation states that the four-role policy faces stricter eligibility than the other policies.

Earlier log entries that cite the without-E02/E14 RMSE as the reason for choosing the model, or mention a DMEM-10 control, are superseded.

## 2026 10 03 Changes after the submission and workflow review

`docs/submission_workflow_review_2026-10-03.md` (Astra) found the analysis sound but the bridge from plate to decision thin. Applied:

- **Confirmation.** The "about 20 wells per arm" figure is withdrawn. Using SD 9.51, 20 per arm gives 51% power for a 5-point non-inferiority margin, and about 45 gives 80%. Confirmation is now a paired, blocked comparison against concurrent E19 across independent preparations, sized from the pilot's preparation-level variance. Acceptance is a one-sided 95% lower bound above -5 points, plus cost and quality.
- **Validity gate.** The memo now runs plate validity, then screen, then confirmation, and includes an inconclusive outcome. Reading wells individually instead of pooling is flagged as a protocol change to agree.
- **Transfer.** E19 is 6.47% FBS by volume and the picks are 7.0%, 9.9%, 7.0% and 6.6%. Qorium states its process uses no animal products beyond the cells (qorium.com, accessed 3 October 2026), so a Qorium campaign would start from an animal-product-free ingredient list.
- **Business criterion.** The cost ceiling is a screening gate. Base savings against E19 are 0.41%, 2.53%, 0.90% and 0.07%. Adoption needs an agreed minimum saving, judged on media cost per acceptable output.
- **Anchor as pending.** Selecting with E19 conditioned as pending moves slot 4 by 1% (45/21/28/6). The picks are kept and the rerun is recorded in `batch_stability.csv`.
- **Simulation wording.** Gains are credited to the implemented package, not to role mixing alone. The score measures discovery, not confirmation.
- **Schema.** Adds COMPONENT_LOT, CELL_PREP, MEDIUM_PREP and SAMPLE with pooling membership, plus QC status, exclusion reason, raw-file reference and protocol version.
- **Scope.** The pipeline reproduces the case-study snapshot. A weekly loop would need a versioned recipe manifest and a results template.
