# Project plan and delivery status

Updated 7 October 2026. The case-study deliverables are complete. This page records current status; the dated review files and [original fix plan](FIX_PLAN.md) describe earlier snapshots.

## Decision delivered

Recommend four new media blends and a concurrent E19 re-run: five formulations in total. Two designed DMEM steps test the response along E19's mixture path, and two model picks test a cheaper blend and a partial AR5 substitution. Each formulation has 11 wells, subject to assay-owner confirmation of cell supply and readout feasibility.

The recommendation is in [batch_selection.md](../reports/batch_selection.md), with recipes and model evidence in `outputs/next_experiments.csv`. Model picks meet E19's cost ceiling at base prices and in at least six of nine price scenarios. The designed steps may be up to 1% above E19 at base prices and are read as a diagnostic, separately from candidate screening.

## Milestones

| Stage | Work | Evidence | Status |
| --- | --- | --- | --- |
| 1 Data preparation | Select one public system, retain provenance, validate mixtures and readings | [Data audit](data_audit.md), processed tables and source manifest | Complete |
| 2 Exploratory analysis | Outcome history, reading spread, mixture coverage and nearby recipes | [Exploratory report](../reports/exploratory_analysis.md), figures and evidence tables | Complete |
| 3 Objective and cost | Prepared-media costs, E19-relative ceiling and scenario sensitivity | Price sources, component costs and nine scenarios | Complete with provisional prices |
| 4 Modelling | Compare the mean, mixture regression, forest and GP; test forward rounds and simulated policies | [Model comparison](../reports/model_comparison.md) and focused GP checks | Complete; prospective performance remains weak |
| 5 Batch selection | Two designed contrasts, two model picks, anchor and sensitivity checks | [Batch report](../reports/batch_selection.md), recipe manifest and plate layout | Complete |
| 6 Delivery | Runnable pipeline, technical memo, timed walkthrough, schema and GitHub repository | [README](../README.md), [walkthrough](../reports/walkthrough.md) and [schema](SCHEMA.md) | Complete for the case-study snapshot |

## Objective and validation decisions

Maximise mean PBMC viability at 72 hours within the stated cost and mixture rules. The next plate adds viable-cell recovery against a t = 0 count. Fractions are nonnegative and sum to one; the model picks use whole percentages. E19's normalised recipe is dispensed at 0.1 mL resolution per 100 mL.

All 24 historical recipes remain in the primary model. Excluding E02 or E14 is a sensitivity check, not a correction to the source data. The main GP uses pooled noise; alternative noise assumptions and covariance coordinates are also tested. Round is evaluation metadata, rather than a candidate feature.

Forward-round failures limit the claims: the GP proposes candidates, and concurrent experimental comparisons determine what advances. Neither good leave-one-out coverage nor the illustrative simulations validate the proposed recipes. The simulations use synthetic truths and do not test the final designed batch, replication or confirmation policy.

The control comparison and cytokine study remain outside initial training. K. phaffii is retained as a separate source. There is no paired multi-fidelity dataset in the chosen subset, so multi-fidelity is an extension requiring calibration experiments.

## Experimental handoff still to agree

These are prerequisites to running or adopting a formulation, rather than missing case-study deliverables. See [the lab plan](../reports/lab_plan.md).

- Assay SOP, harvest, seeding, well volume, pooling or single-well readout and cell supply.
- Plate-validity thresholds, the statistical test for the DMEM contrast and handling of missing wells and row blocks.
- Independent cell and medium preparation repeats to estimate preparation-level variation before sizing confirmation.
- Actual supplier quotes and a business acceptance rule based on cost per acceptable output.
- For Qorium: approved animal-free inputs, growth and collagen endpoint definitions, material-quality constraints, culture phases and scale transfer.

The software reproduces a fixed public-data snapshot. Updating it with a new experimental round would require a versioned ingestion and approval process; the supplied manifest and results template are a starting handoff, not that implementation.

## Timebox and review record

The original allocation was 4 to 6 hours. It was a plan, not a measured effort record, and the repository does not establish actual total time spent. The walkthrough is scripted for eight minutes; actual spoken duration needs rehearsal.

Steps 1 to 7 of [FIX_PLAN.md](FIX_PLAN.md) have been implemented or superseded by the final batch design. [DECISIONS.md](DECISIONS.md) preserves the chronology, including rejected suggestions and later withdrawals of earlier interpretations.
