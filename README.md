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
docs/              Schema, data dictionary, decisions log, data audit, plan, review records and a domain primer (domain_primer.html)
scripts/           Data preparation, cost rule, model comparison, batch selection and GP checks
notebooks/         Narrated walkthrough notebook, executed with outputs (renders on GitHub)
reports/           Memo (md, rendered html and pdf, css), walkthrough script, exploratory, model and batch reports
reports/figures/   Figures 01 to 12 (09 to 12 are the memo figures)
reports/tables/    Generated evidence tables
outputs/           Recommended blends, plate formulations, randomised plate layout, recipe manifest and per-well results template
```

Start with [the memo](reports/memo.pdf), or [the notebook](notebooks/walkthrough.ipynb) for the same story with the evidence inline. Then read [the batch recommendation](reports/batch_selection.md), [model evidence](reports/model_comparison.md), [lab plan and open questions](reports/lab_plan.md), and [data schema](docs/SCHEMA.md). Use [the eight-minute walkthrough](reports/walkthrough.md) for the interview. Dated review files and the decision log record earlier snapshots; their old recipe values and findings may be superseded.

## Reproduce everything

Python 3.12 or newer and the pinned dependencies in `requirements.txt`. One command rebuilds the generated analysis tables, figures and recommendation (seed 20261002). It regenerates the tracked outputs in place and finishes by listing any files that differ from the committed version. The previously recorded fresh-clone run took 4 to 5 minutes on an Apple-silicon laptop. An isolated rerun on 7 October reproduced the CSVs and PNGs byte for byte; the five exploratory PDFs differed only in creation-date metadata. Other platforms may differ in the last decimals of optimiser output.

```sh
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
./run_all.sh
```

Render the memo (optional; needs pandoc and Google Chrome, path shown for macOS):

```sh
cd reports && pandoc memo.md -s --css memo.css --embed-resources -o memo.html \
  && "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --no-pdf-header-footer --print-to-pdf=memo.pdf "file://$PWD/memo.html"
```

Rebuild the notebook after `run_all.sh` (needs `pip install -r requirements-notebook.txt`):

```sh
.venv/bin/pip install -r requirements-notebook.txt
.venv/bin/python scripts/build_notebook.py
```

The individual steps, in order:

```sh
PY=.venv/bin/python
$PY scripts/fetch_data.py
$PY scripts/build_costs.py
$PY scripts/prepare_data.py
$PY scripts/explore_data.py
$PY scripts/design_space.py
$PY scripts/check_gp.py
$PY scripts/compare_models.py
$PY scripts/select_batch.py
$PY scripts/memo_figures.py
```

Fetching skips already verified files. The Cosenza reference files are not redistributed and no script reads them; set `FETCH_REFERENCE=1` to download them. A changed or damaged file raises an error instead of overwriting an existing source. Processing recomputes all generated data tables and `docs/data_audit.md`.

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

See [project plan](docs/PLAN.md), [data dictionary](docs/DATA_DICTIONARY.md), [decisions](docs/DECISIONS.md), [data audit](docs/data_audit.md) and [Markdown consistency audit](docs/markdown_audit_2026-10-07.md).

See the [exploratory report](reports/exploratory_analysis.md) for the findings and modelling implications. PNG figures support review; PDF versions support reuse in the technical memo.

## Licences

Code: MIT (`LICENSE`). Data: the PBMC and K. phaffii workbooks in `data/raw/narayanan_2025/` are from Narayanan et al. (2025), Nature Communications 16:6055, figshare doi:10.6084/m9.figshare.27715134, released under the MIT licence; their notice applies to those files. The Cosenza et al. (2022) reference files are not included; `fetch_data.py` downloads them on request from the original repository.

## How this was built

I used AI assistants to draft code and text and as adversarial reviewers. Their review records are in `docs/` with dates, and every change they prompted is logged in `docs/DECISIONS.md`. `run_all.sh` reproduces the data, model, simulation and recommendation results cited in the memo. The screen and confirmation planning figures are conditional statistical calculations described in [the lab plan](reports/lab_plan.md), rather than a separate output of the runner. The judgement calls are mine.
