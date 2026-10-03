# Analysis data dictionary

The source is `PBMC_Experiments.xlsx`, sheet `MediaBlendingStudies`, from [Figshare](https://doi.org/10.6084/m9.figshare.27715134). Recipe proportions are volume fractions. Viability is stored on the 0 to 100 scale.

## Tables and relationships

`pbmc_formulations.csv` has one row per experiment. `pbmc_measurements.csv` has one row per nonmissing reading and joins through `formulation_id`. `pbmc_analysis.csv` joins formulations to within-experiment summaries and optional prepared-media costs. Never count both summary and measurement rows as distinct experiments.

| Field | Table | Type and unit | Meaning |
| --- | --- | --- | --- |
| formulation_id | All PBMC tables | string | Stable ID `PBMC-E01` through `PBMC-E24` |
| experiment_number | Formulations, analysis | integer | Original `Expt #` |
| round | Formulations, analysis | integer | Original adaptive round 0 through 3; evaluation metadata |
| source_file, source_sheet, source_row | Formulations, measurements | string, string, integer | Traceability to original workbook; row includes header |
| dmem_pct_raw, rpmi_10_pct_raw, xvivo_pct_raw, ar5_pct_raw | Formulations | float, volume % | Published mixture amounts, unchanged |
| mixture_sum_pct_raw | Formulations, analysis | float, volume % | Sum of published mixture amounts |
| dmem_fraction, rpmi_10_fraction, xvivo_fraction, ar5_fraction | Formulations, analysis | float, L/L | Original amount divided by the row's mixture total |
| normalisation_applied | Formulations, analysis | boolean | Whether total differed from 100 beyond numerical tolerance |
| normalisation_factor | Formulations | float | 100 divided by published total |
| supplied_viability_mean_pct | Formulations | float, % | Published average, retained for reconciliation |
| measurement_id | Measurements | string | Unique formulation ID plus source reading label |
| source_reading_label | Measurements | string | Original `Via1` through `Via5`; does not identify a donor |
| viability_pct | Measurements | float, % | One nonmissing reported viability reading |
| assay, timepoint_hours | Measurements, analysis | string, integer | AOPI viable-cell assay description and 72 h from article |
| n_readings | Analysis | integer | Available reported readings, not known independent culture count |
| viability_mean_pct | Analysis | float, % | Arithmetic mean of available readings; modelling target |
| viability_sd_pct_points | Analysis | float, percentage points | Sample SD, denominator n minus 1 |
| viability_sem_pct_points | Analysis | float, percentage points | SD / sqrt(n), provisional independence assumption |
| mean_noise_variance_proxy | Analysis | float, percentage points squared | Sample variance / n; unvalidated model-noise proxy |
| supplied_mean_difference_pct_points | Analysis | float, percentage points | Recomputed mean minus published mean |
| formulation_group | Analysis | string | Equal normalised recipes share a group for leakage-safe splitting |
| noise_interpretation | Analysis | string | Explains unknown pool/donor identities |
| blend_cost_per_litre, cost_currency, cost_status | Analysis | float, string, string | Sum of fraction times prepared-media price, or unavailable |

## Component costs

`data/inputs/component_costs.csv` contains four components. `component_id` matches the fraction columns without `_fraction`. `prepared_medium_label` describes the media to price. `price_per_litre` is numeric and initially blank. `currency` is a common currency code. `price_basis` is `observed`, `estimate` or `hypothetical`. `price_source` is a URL or supplied quote reference. `as_of_date` is an optional ISO date. `notes` records preparation and price assumptions.

The file is an editable input and is not overwritten by preparation. All four price values, currencies, bases and source references must be populated before any blend cost is calculated. Negative or nonfinite prices and mixed currencies stop preparation. Zero remains zero.

## Quality issues and audit

`data_quality_issues.csv` records severity, source locator, issue and action. It includes normalised rounded mixtures, missing reading slots, unknown replicate identities, absent costs and excluded control records. `docs/data_audit.md` reports counts, outcome ranges and checks. Source files are fingerprinted in `data/raw/source_manifest.json` with SHA256 hashes and retrieval timestamps.

## Future lab schema

When adapting this work to lab data, add component catalogue IDs and lots; cell type and passage; donor or biological replicate ID; pool ID; plate and well; assay protocol/version; batch and timestamp; dispensing volumes; raw readout and calibrated endpoint; price currency/date and source. Keep recipe, execution and measurement records separate and join them through stable IDs. These fields are unavailable in the current workbook and are not invented.
