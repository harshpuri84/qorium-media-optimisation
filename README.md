# Qorium media optimisation case study

This project recommends four new media formulations plus one anchor re-run (five in total) for the next experimental batch, balancing biological performance, media cost, uncertainty and feasibility. The recommendation is in `outputs/next_experiments.csv` and `reports/batch_selection.md`; model evidence is in `reports/model_comparison.md`. The technical memo is `reports/memo.pdf` and the walkthrough script is `reports/walkthrough.md`.

## Starting dataset

Use the **PBMC media blending experiment** from Narayanan et al. (2025), permitted by the assignment. It contains 24 formulations across four rounds and repeated viability readings. Four commercial media proportions form a constrained mixture. This is a public demonstration dataset, not Qorium experimental data. Its endpoint is PBMC viability after 72 hours, not proliferation or collagen productivity.

The 2022 Cosenza repository was also inspected. Its current solver uses generated examples, and its saved text arrays lack self-contained column and transformation metadata. Keep these as reference material; do not assume their semantics or combine their costs with the PBMC data. The K. phaffii workbook is retained as an alternative, not pooled with PBMCs.

## Project layout

```text
data/
  raw/             Original public workbooks, reference files and source manifest
  interim/         Faithful flat exports of workbook sheets
  processed/       Formulations, measurements, analysis table and quality issues
  inputs/          Price sources, prepared-media prices and price scenarios
docs/              Plan, schema, data dictionary, decisions, data audit and external reviews
scripts/           Data preparation, cost rule, model comparison, batch selection and GP checks
notebooks/         Narrated walkthrough notebook, executed with outputs (renders on GitHub)
reports/           Memo (md, pdf), walkthrough script, exploratory, model and batch reports
reports/figures/   Figures 01 to 08
reports/tables/    Generated evidence tables
outputs/           Recommended blends, plate formulations, randomised plate layout, recipe manifest and per-well results template
```

Start with `reports/memo.pdf`, or `notebooks/walkthrough.ipynb` for the same story with the evidence inline. Then `reports/batch_selection.md` for the recommendation detail, `reports/model_comparison.md` for the evidence, and `docs/SCHEMA.md` for the data model.

## Reproduce everything

Python 3.12 or newer and the pinned dependencies in `requirements.txt`. One command rebuilds every table, figure and the recommendation (seed 20261002). A run from a fresh environment took 5 minutes 7 seconds on an Apple-silicon laptop:

```sh
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
./run_all.sh
```

Render the memo (needs pandoc and Google Chrome):

```sh
cd reports && pandoc memo.md -s --css memo.css --embed-resources -o memo.html \
  && "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --no-pdf-header-footer --print-to-pdf=memo.pdf "file://$PWD/memo.html"
```

Rebuild the notebook after `run_all.sh` (needs `pip install -r requirements-notebook.txt`):

```sh
python scripts/build_notebook.py
```

The individual steps, in order:

```sh
python scripts/fetch_data.py
python scripts/build_costs.py
python scripts/prepare_data.py
python scripts/explore_data.py
python scripts/design_space.py
python scripts/check_gp.py
python scripts/compare_models.py
python scripts/select_batch.py
```

Fetching skips already verified files. A changed or damaged file raises an error instead of overwriting an existing source. Processing recomputes all generated data tables and `docs/data_audit.md`.

Start analysis with `data/processed/pbmc_analysis.csv`. There is one row per historical experiment. The `*_fraction` columns are proportional corrections of the rounded published percentages and sum to one. Original percentages remain in `pbmc_formulations.csv` and the interim exports. Measurement detail is in `pbmc_measurements.csv`.

## Cost inputs

Catalogue pack prices and their provenance live in `data/inputs/price_sources.csv`. `python scripts/build_costs.py` converts them to EUR per litre of **prepared** medium (basal + 10% FBS + 1% Penicillin-Streptomycin for DMEM and RPMI-10, per the article) and writes `data/inputs/component_costs.csv` and the sensitivity grid `data/inputs/cost_scenarios.csv`. Rerun `scripts/prepare_data.py` afterwards.

Base prices (2026-10-02): DMEM-10 EUR 180.89, RPMI-10 EUR 168.45, X-VIVO 15 EUR 181.00, AR5 EUR 181.00 per litre. The FBS price is a search snippet and AR5 is a hypothetical proxy (its catalogue item was not found). Treat costs as estimates and report results across the scenario grid.

## Current limitations

- Readings are preserved with source column labels; donor, well and pooling identities are unavailable. SD measures reported-reading spread. SEM and variance of the mean are provisional independence-based calculations, not validated biological uncertainty estimates.
- Source mixture totals range from 99.9% to 100.1%. The small normalisation correction is recorded for each formulation.
- The separate control/optimal comparison sheet contains missing and inconsistent fractions and is excluded from initial training. No source values are silently repaired.
- The cytokine study measures different outcomes and is excluded from the media-blend task.
- Historical round is evaluation metadata, not a candidate recipe feature.
- Exploratory analysis is in `reports/exploratory_analysis.md`, with five figures and descriptive tables. It identifies clustered final-round recipes and discrepancies between nearby recipes.
- Prices are provisional: FBS comes from a search snippet and AR5 is a hypothetical proxy. Results are reported across nine price scenarios.
- The GP is a ranking aid, not a forecaster: every model under-predicted round 3 by 22 to 29 points. The batch includes an E19 re-run as a same-plate anchor.

See [project plan](docs/PLAN.md), [data dictionary](docs/DATA_DICTIONARY.md), [decisions](docs/DECISIONS.md) and [data audit](docs/data_audit.md).

See the [exploratory report](reports/exploratory_analysis.md) for the findings and modelling implications. PNG figures support review; PDF versions support reuse in the technical memo.
