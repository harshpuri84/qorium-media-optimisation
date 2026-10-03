# Data schema

This schema covers two things. The first is what this repo stores today. The second is the Benchling-style model a media-optimisation team would need to run this loop on its own lab data. The repo tables map onto it, and the mapping is shown at the end. Fields marked *future* do not exist in the public workbook and are not invented here.

## Design rules

- Biological replication lives on BATCH (`cell_prep_id`, `medium_prep_id`), not on WELL. Four wells from one cell preparation measure repeatability, not robustness. Confirmation needs independent preparations.

- Keep three kinds of record apart: the recipe (what we intend to mix), the run (what was actually made and when) and the measurement (what the assay read). The same recipe run on two plates is two runs. A model that confuses the two will count re-runs as new information and miss batch effects. The E19 anchor exists for exactly that reason.
- One measurement row per well and readout. Summaries are derived, never stored as if they were raw data.
- Every price carries a currency, a date, a source and a basis (`observed`, `estimate` or `hypothetical`).
- Every recommendation records the model version, the price scenario and the selection rule that produced it.

## Entity model

```mermaid
%%{init: {'theme': 'neutral'}}%%
erDiagram
    COMPONENT ||--o{ FORMULATION_COMPONENT : "used in"
    FORMULATION ||--|{ FORMULATION_COMPONENT : "contains"
    FORMULATION ||--o{ RUN : "prepared as"
    BATCH ||--|{ RUN : "groups"
    RUN ||--|{ WELL : "dispensed into"
    WELL ||--o{ MEASUREMENT : "read by"
    ASSAY ||--o{ MEASUREMENT : "defines"
    COMPONENT ||--o{ PRICE : "priced by"
    PRICE_SCENARIO ||--o{ PRICE : "groups"
    RECOMMENDATION ||--|{ RECOMMENDED_FORMULATION : "lists"
    FORMULATION ||--o{ RECOMMENDED_FORMULATION : "selected as"
    MODEL_VERSION ||--o{ RECOMMENDATION : "produced"
    PRICE_SCENARIO ||--o{ RECOMMENDATION : "costed under"

    COMPONENT {
        string component_id PK
        string label
        string supplier
        string catalogue_number
        string kind "basal, serum-free, supplement"
        string lot_number "future"
    }
    FORMULATION {
        string formulation_id PK
        string origin "historical, recommended, control"
        float sum_check "must equal 1.0"
    }
    FORMULATION_COMPONENT {
        string formulation_id FK
        string component_id FK
        float volume_fraction "0 to 1"
        float published_pct "as in source"
    }
    BATCH {
        string batch_id PK
        int round "historical round 0 to 3"
        date run_date "future"
        string cell_source "donor or pool, future"
        string cell_prep_id "biological replicate, future"
        string medium_prep_id "future"
        string operator "future"
    }
    RUN {
        string run_id PK
        string formulation_id FK
        string batch_id FK
        string role "exploit, cheaper, explore, EI, anchor"
    }
    WELL {
        string well_id PK
        string run_id FK
        string plate_id "future"
        string position "e.g. C7"
        int replicate
        string culture_id "links wells from one culture across destructive assays, future"
    }
    ASSAY {
        string assay_id PK
        string name "AOPI viability"
        int timepoint_hours
        string fidelity "low, high"
        float cost_per_sample "future"
    }
    MEASUREMENT {
        string measurement_id PK
        string well_id FK
        string assay_id FK
        float value
        string unit "% viable"
        string source_label "Via1..Via5"
    }
    PRICE {
        string component_id FK
        string scenario_id FK
        float price_per_litre_prepared
        string currency
        string basis "observed, estimate, hypothetical"
        string source_url
        date as_of
    }
    PRICE_SCENARIO {
        string scenario_id PK
        float fbs_multiplier
        float ar5_multiplier
    }
    MODEL_VERSION {
        string model_id PK
        string kernel "Matern 5/2, fitted length scales"
        string noise_model "pooled or per-recipe SEM"
        string code_commit
        int seed
    }
    RECOMMENDATION {
        string recommendation_id PK
        string model_id FK
        string scenario_id FK
        date created
        float cost_ceiling
    }
    RECOMMENDED_FORMULATION {
        string recommendation_id FK
        string formulation_id FK
        int slot
        string role
        float predicted_mean
        float predicted_sd
        float p_above_anchor
    }
```

## Where this repo's files sit

| Entity | Repo file | Notes |
| --- | --- | --- |
| COMPONENT | `data/inputs/price_sources.csv` (catalogue numbers) | 4 media plus FBS and Penicillin-Streptomycin as supplements |
| FORMULATION, FORMULATION_COMPONENT | `data/processed/pbmc_formulations.csv` | Wide format: one fraction column per component |
| BATCH | `round` column | The only batch information in the source |
| RUN, WELL | absent for history; `outputs/plate_layout.csv` for the next batch | The source gives 2 to 5 readings per recipe with no well or donor identity |
| MEASUREMENT | `data/processed/pbmc_measurements.csv` | One row per reported reading |
| ASSAY | `assay`, `timepoint_hours` columns | One assay, so no fidelity levels |
| PRICE, PRICE_SCENARIO | `data/inputs/component_costs.csv`, `data/inputs/cost_scenarios.csv` | Base prices plus 9 scenarios |
| RECOMMENDATION, RECOMMENDED_FORMULATION | `outputs/next_experiments.csv` | One row per slot, with predictions and stability |
| MODEL_VERSION | `scripts/compare_models.py`, seed 20261002 | Not yet stored as a record |

## What changes for a multi-fidelity setup

Cosenza et al. (2022) paired cheap 3-day assays (AlamarBlue, LIVE stain) with 6-day cell counts. In this schema, that is two ASSAY rows with different `fidelity` and `cost_per_sample` values. Non-destructive readouts attach to the same WELL. A destructive assay needs its own WELL, linked to its sister wells through `culture_id`, so the model can pair measurements from one culture. The model then learns how the cheap readout maps to the expensive one. No new tables are needed. That is the test of a schema: the next experiment design should fit without a migration.
