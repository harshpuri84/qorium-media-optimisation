# Project plan

## Decision to deliver

Recommend exactly four new, feasible media blends with proportions, cost or labelled cost scenario, predicted viability, uncertainty and a reason for each selection. Prepare runnable code, a maximum four-page memo and a five-to-ten-minute walkthrough. Keep the full take-home within the assignment's four-to-six-hour budget.

## Milestones

| Stage | Work | Completion criterion | Status |
| --- | --- | --- | --- |
| 1 Data preparation | Inspect both public sources, select one system, preserve provenance, flatten readings, validate mixtures | Reproducible tables, schema and issue log | Complete |
| 2 Exploratory analysis | Plot viability by round, reading spread and mixture coverage; examine duplicates and nearby recipe discrepancies | Supported findings and documented limitations | Complete |
| 3 Objective and cost | Obtain prepared-media prices or define explicit hypothetical scenarios; choose ceiling/reference and pipetting resolution | Executable cost and feasibility rules | Complete |
| 4 Modelling | Compare feasible random sampling with a conservative noisy GP; optionally use ridge regression as a sanity check | Grouped or round-aware evaluation with uncertainty diagnostics | Complete |
| 5 Batch selection | Generate valid mixture candidates and select four diverse experiments | Exact recipes with individual and batch rationale | Complete |
| 6 Delivery | Rerun from clean environment, write memo, prepare walkthrough and repository documentation | End-to-end reproducible submission | Pending |

## Time allocation

Allow about 45 minutes for data preparation, 45 minutes for exploration and objective definition, 90 minutes for modelling, 60 minutes for selection and sensitivity checks, and 60 minutes for packaging. Use the remaining hour only for material data or reproducibility issues. Record actual time separately; this allocation is a plan, not measured elapsed time.

## Proposed optimisation problem

Maximise expected PBMC viability at 72 hours subject to a prepared-media cost ceiling and mixture constraints. Set the ceiling after selecting a reference blend or an explicit price scenario. Media fractions must be nonnegative and sum to one. The initial numerical search domain is the full mixture simplex, but new blends still require lab compatibility and preparation review. Observed historical min/max values describe coverage, not biological limits.

Use the four mixture fractions as recipe features. Avoid donor, timepoint, assay and batch assumptions that the source does not support. A mixture has three independent degrees of freedom; account for that dependence in modelling. Do not treat the four fractions as independent box-bounded variables.

## Model and validation decisions

- Use a feasible random design baseline and a GP-based selection policy on the same candidate space and cost constraints.
- Keep all readings of one formulation together. Model experiment means with a conservative observation-noise treatment; compare a pooled-noise assumption against reading-specific noise as a sensitivity check. The stored SEM is not sufficient proof of independent biological replication.
- Use leave-formulation-out diagnostics and forward-round evaluation where feasible. Fit preprocessing within training folds. Do not use round number to predict a new formulation.
- Historical data were selected adaptively and are sparse. A retrospective candidate replay over measured formulations can compare policies, but does not establish performance on unmeasured recipes.
- Preserve the control comparison as a separate dataset until its composition inconsistencies are resolved. Do not use the reported optimal blend as a prospective discovery claim.
- With no paired fidelity assays in this chosen subset, discuss multi-fidelity extension rather than fabricate a multi-fidelity analysis.

## Batch design

Target four unique new recipes: a leading candidate, a credible cheaper alternative, an informative uncertain candidate and a diverse promising candidate. These roles guide interpretation; selection should score the batch and prevent near duplicates. Translate fractions to attainable preparation volumes and recheck feasibility after rounding.

Confirm whether reference controls and replicate wells are additional to the four formulation slots. State the assumption explicitly in the submission. Randomise positions or block by experimental conditions and measure every selected blend with the same primary assay.

## Final deliverables

- End-to-end analysis notebook or script with recorded random seed and dependencies.
- `outputs/next_experiments.csv` containing exactly four recipes and their evidence.
- Three-to-four-page memo: framing and assumptions; exploratory findings and method; recommendation table; limitations and validation plan.
- Five-to-ten-minute walkthrough focused on the decision and tradeoffs.
- Repository documentation and a compact schema connecting formulations, measurements and component prices.

## Inputs still needed

Prepared-media prices or an explicitly hypothetical cost scenario; a reference cost ceiling; allowed dispensing resolution; capacity accounting for controls and replicates. These inputs are needed for final recommendations, but not for initial exploratory analysis.

## Review fixes (2026-10-02)

Steps 1 to 6 of `docs/FIX_PLAN.md` are done. Step 7 (memo, walkthrough, runner, standalone repo) is next, after a second external review.
