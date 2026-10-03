# Submission and real-workflow review — 3 October 2026

The submission is a strong, defensible take-home analysis. It meets the core assignment and demonstrates good judgement about small data, confounded experiments and uncertain prices. I would take its recommendation into an R&D planning meeting. I would not yet treat its plate files and confirmation paragraph as a complete lab execution and adoption plan.

The biggest remaining improvement is the bridge from recommendation to experimental evidence and a business decision. More models would add less value than fixing that bridge.

This review assesses the assignment, current memo/PDF, walkthrough, notebook, schema, source data handling, modelling and selection scripts, and generated outputs. It distinguishes assignment requirements from improvements needed for operational use. Qorium's public website informs the transfer assessment; its internal protocols and economics are not available here. No submission files were changed by this review.

## Fit to the assignment

| Requirement | Assessment |
|---|---|
| Frame an experiment recommendation | Strong: the answer leads, with a specific next decision |
| Define an objective and constraints | Met: viability under an E19-relative cost ceiling; assumptions disclosed |
| Compare at least two approaches | Exceeded: mean, mixture regression, RF and two GP variants; policy comparison as well |
| Recommend exactly 3–5 formulations | Met: four new blends and one anchor, five formulations total |
| Explain exploration/exploitation | Met: roles are concrete, although role labels do not guarantee independent information |
| Address all six changed circumstances | Met in the memo |
| Runnable notebook or script | Script pipeline provided; notebook is an executed evidence walkthrough, not the pipeline itself |
| Technical memo, maximum 3–4 pages | Met: rendered PDF has exactly four pages |
| 5–10 minute walkthrough | Script provided, plausibly within the limit; no timed delivery or recording verified |
| Data schema | Substantial conceptual schema; some important experimental relationships need correction |
| GitHub repo | Origin is `https://github.com/harshpuri84/qorium-media-optimisation.git`; local main tracks origin/main. Recipient access was not independently verified |
| 4–6 hour timebox | Actual effort cannot be established from these artifacts |

The brief explicitly says not to build production infrastructure. Missing ELN integration, deployment, and services are not submission defects. A short description of the operational handoffs is enough.

## What is particularly good

- Raw workbook checksums, source row references, retained original fractions, reconciliation of means, and explicit treatment of missing readings make the analysis auditable.
- The public dataset is an allowed choice. Choosing labelled, interpretable data over undocumented arrays is sensible within the timebox.
- E02 and E14 are retained. Sensitivity checks are presented as sensitivity, rather than used to manufacture a better headline result.
- Forward-round validation exposes the main problem: recipe and round are confounded, and prospective rankings are weak. The memo does not disguise this with the stronger leave-one-out result.
- The E19 rerun is a useful use of scarce capacity. It permits a concurrent comparison instead of treating the historical maximum as ground truth.
- GP pending-point conditioning preserves scaling and historical noise, and focused numerical checks exercise those properties. The joint covariance calculation for comparison with E19 is appropriate under the fitted model.
- Price and rule sensitivity are unusually thorough for a take-home exercise. The memo distinguishes scenario counts from real-world certainty.
- The recommendation is readable and reproducible. The PDF is clean at four pages; tables and figures are legible, with no clipping observed. The fourth acquisition rule starts on page 3, a minor layout distraction.

## Priority findings

### 1. Confirmation sample size is not justified by the stated calculation

**Priority: fix before submission.** Location: `reports/memo.md:101`, repeated in the walkthrough and notebook.

The memo correctly says four wells cannot establish equivalence. It then moves from an approximate interval half-width to “about 20 wells per arm” for confirmation. Precision, power and biological replication are different questions.

Using the memo's SD of 9.51 and independent, equal-variance observations:

- Four observations per arm give a normal-approximation 90% half-width of 11.06 points. If that SD is estimated with six residual degrees of freedom, a t interval is about 13.07 points.
- Twenty per arm give a normal half-width of 4.95 points. But a one-sided 5% non-inferiority test with a five-point margin has only about **51% power** when the true difference is zero.
- Under the same idealised known-variance assumptions, about 45 independent observations per arm would give 80% power. This is a diagnostic calculation, **not a replacement lab sample-size recommendation**.

The historical SD is reported-reading spread with unresolved pooling, so it is not established as the well-level SD of the proposed protocol. Twenty wells distributed over two preparations also do not constitute twenty independent biological preparations. Shared blocks can improve paired comparisons, but treatment-by-preparation variability still needs to be estimated.

**Recommended change:** call 20 wells a provisional planning illustration. Define confirmation as a paired, blocked comparison against concurrent E19 across independent preparations/days. Estimate the variance of preparation-level differences in the pilot, then size confirmation for an agreed loss margin and power. A possible acceptance rule is a prespecified one-sided lower confidence bound above minus five points, plus acceptable cost and quality. State whether one finalist or several comparisons will be confirmed. Use “non-inferiority” for the one-sided loss-margin objective; equivalence is a different claim.

### 2. Qorium transfer requires changing the feasible ingredients, not just the endpoint

**Priority: fix before submission.** Locations: `reports/memo.md:116`, the cheaper-slot discussion, and `reports/walkthrough.md`.

The memo already distinguishes PBMC viability from Qorium productivity. It should also identify the serum constraint explicitly. Qorium publicly states that, beyond the cultured cells themselves, its collagen-sheet process uses no animal products. Source: [Qorium, The Process](https://www.qorium.com/), accessed 3 October 2026. That does not disclose every internal R&D condition, but it makes animal-product eligibility a necessary transfer question.

Under this submission's prepared-media assumptions, the E19 blend contains approximately 6.47% FBS overall. The cheaper pick contains **9.9% FBS**, because 99% of it is supplemented DMEM/RPMI. All four new picks increase the FBS fraction relative to E19. Removing AR5 therefore does not demonstrate movement toward an animal-product-free formulation.

**Recommended change:** retain the permitted dataset and recipes. Add a direct statement that these are PBMC demonstrations; a Qorium campaign would define approved animal-product-free inputs before generating candidates, and retrain on the relevant cell/process data. Do not imply that reducing purchased serum-free media is a transferable benefit on its own.

### 3. The business acceptance rule is not yet tied to useful output

**Priority: clarify before submission; agree with the lab before a run.** Locations: the objective, cheaper-slot rationale and screening rule.

The cost ceiling is valid for the assignment. However, a five-point performance loss can pass even when cost savings are negligible. Base savings relative to E19 are approximately 0.41%, 2.53%, 0.90% and 0.07% for slots 1–4. For slot 4, the allowed loss is substantial compared with twelve cents per litre of nominal savings.

Illustration only: at identical total cell counts and medium usage, changing from 81% to 76% viability while reducing cost from EUR 178.43/L to EUR 173.92/L would increase medium cost per viable cell by about 3.9%. Those assumptions are not established by the dataset; the example explains why viability and EUR/L cannot demonstrate production economics.

**Recommended change:** distinguish a permissive screening gate from a business adoption criterion. In the actual workflow, agree a minimum worthwhile saving or performance gain and evaluate media consumption per acceptable output. For Qorium, candidate metrics might be cost per acceptable collagen output or sheet area, with growth and material-quality constraints, subject to the team's actual process. Avoid presenting viability-per-euro as a sufficient manufacturing KPI.

### 4. The first plate lacks an explicit validity and inconclusive-result gate

**Priority: add a compact operational description.** Locations: `reports/memo.md:91–101` and `outputs/plate_layout.csv`.

The E19 anchor and randomisation are good. But the plan jumps from measured means to recipe decisions. There is no defined response to missing wells, excessive dispersion, assay failure, an unexpectedly poor anchor, or evidence of preparation error. “Near 55%” is an example, not a predeclared validity threshold.

The source study used a specialised C.BIRD microplate setup and pooled replicate cultures for readings. A generic 96-well map with four independently read wells changes the measurement protocol unless that change is explicitly agreed. Source: [Narayanan et al., Methods: Culturing PBMCs and Viability Assays](https://pmc.ncbi.nlm.nih.gov/articles/PMC12218302/). This is an assay-handoff issue, not evidence the proposed screen cannot work.

**Recommended change:** identify the culture/assay SOP and whether pooling is used; state that an assay owner establishes plate-validity criteria. Use three outcomes: valid and promising, valid and unpromising, or inconclusive/invalid requiring investigation or repetition. Carry forward the same five formulations; any necessary assay blanks or other QC wells consume physical capacity and should be described separately. A low anchor triggers investigation and does not by itself establish a historical batch effect.

### 5. The schema cannot faithfully represent some of the preparation and pooling relationships

**Priority: repair the conceptual diagram before calling it lab-ready.** Locations: `docs/SCHEMA.md:52–73`, `82–88`.

Separating formulation, run and measurement is the right foundation. Three relationships remain problematic:

- `medium_prep_id` is a single field on BATCH, but a batch containing five recipes ordinarily has multiple actual media preparations. Shared component stocks and each final blend preparation are different records.
- `lot_number` belongs to a lot of a component, not to the component definition. A component may have several lots over time or multiple lots in use.
- Each MEASUREMENT points to one WELL. A pooled assay sample may derive from multiple wells, and multiple technical reads may derive from the same sample. `culture_id` alone does not represent this many-to-one pooling lineage.

**Recommended change:** place final-media preparation on RUN or a linked PREPARATION entity; distinguish component and component lot; add SAMPLE and sample-to-well membership where pooling applies. Include raw-result references, QC status, exclusion reasons, and protocol versions in the conceptual extension. This can remain a lightweight diagram; no database implementation is needed.

### 6. Simulation supports the implemented package, not an isolated benefit of role mixing

**Priority: tighten wording; additional experiments optional.** Locations: `scripts/compare_models.py:221–264`, `reports/memo.md:74`.

The four-role policy uses scenario robustness, minimum distance and single-media exclusions. The other policies mainly use base-cost feasibility and exclusion of already measured points. Different eligibility rules can themselves improve search. The detailed report acknowledges this, but the memo's “simulation supports mixing roles” is stronger than the comparison identifies.

The outcome is also the best **true** latent viability among sampled points. An experimenter does not observe that truth and must choose a finalist from noisy data. This metric demonstrates discovery opportunity, not the ability to identify and confirm the best recipe. No anchor is run in the simulated campaigns, so they do not reproduce the full five-formulation operating policy.

**Recommended change:** say the implemented four-role package performed better in these illustrative settings. If expanding the analysis, use matched eligibility for all policies and score the true performance of a finalist selected from noisy observations. Add round/preparation effects only if time permits. These are limitations to state, not grounds to rebuild the submission.

### 7. The scheduled anchor is absent from pending-point selection

**Priority: worthwhile methodological refinement, not a correctness blocker.** Locations: `scripts/select_batch.py:82–103`, `142–146`, `207–210`.

The selector conditions on the four new picks, then appends E19 to the plate. It never conditions on the anchor that will also be measured. Because slot 1 is highly correlated with E19, the planned anchor can affect marginal information value around that region.

**Recommended change:** test selection with E19 included as a pending observation before assigning new slots, keeping display predictions from the original fitted model. Compare whether the recipes change. This would make the information accounting consistent with the actual plate, though it still cannot represent unmodelled batch shifts.

### 8. The repository reproduces a historical snapshot, not the next-round data loop

**Priority: describe the boundary; no production build required.** Locations: `scripts/prepare_data.py`, `scripts/design_space.py`, and `scripts/select_batch.py`.

Preparation reads a fixed workbook and enforces exactly 24 experiments in rounds 0–3. E19 is hard-coded as the reference. Generated output files are overwritten, and recommendation/model IDs are conceptual rather than stored. Appending results and rerunning the command is therefore not yet a supported weekly workflow.

**Recommended change:** explicitly call this an end-to-end reproduction of the case-study snapshot. Describe a small future handoff: approved recipe manifest → executed preparations and sample IDs → raw results plus QC → frozen analysis dataset → signed-off next batch. A versioned CSV manifest and results template would be sufficient for a supervised pilot; an ELN API, service or dashboard is unnecessary for this assignment.

### 9. Some supporting prose still contradicts the corrected memo

**Priority: quick consistency cleanup.** Location: `reports/batch_selection.md:103–109`.

The detailed batch report still says an E19 rerun near 55% means round 3 “was partly a batch effect,” and that a similar slot 1 result permits substitution “without loss.” Neither follows from this screen. It also refers to a “single plate of single measurements,” despite four wells per formulation. Bring these passages into line with the memo's more cautious interpretation and independent confirmation plan. `docs/data_audit.md` still ends by saying prices and a cost ceiling are required despite the pipeline computing them. Historical review files should stay clearly dated so superseded issues are not mistaken for current defects.

## How it would fit into a real workflow

| Stage | Already supplied | What the real team must add | Decision owner |
|---|---|---|---|
| Agree the campaign | Endpoint, ceiling and five-slot proposal | Actual output metric, acceptable loss, eligible inputs, assay budget | R&D/process lead with data scientist |
| Review data | Provenance, checks, EDA, outlier sensitivity | Preparation, passage/cell-bank, lot, protocol and QC records | Scientist and data scientist |
| Propose batch | Feasible candidates, role-based selection, sensitivity | Inventory, physical compatibility and dispensing review | Data scientist and bench scientist |
| Release work order | Ratios and randomised well positions | Actual mix volumes, preparation/sample IDs, SOP, plate-validity rules | Bench/assay owner |
| Run and acquire | Conceptual measurement schema | Execution deviations, raw files, pooling map, QC | Bench/assay owner |
| Review screen | Concurrent E19 comparison and proposed margin | Validity gate and explicit inconclusive category | R&D lead and data scientist |
| Confirm | Intent to use independent preparations | Blocked design, sample-size basis, prespecified acceptance rule | Assay/process lead with statistical input |
| Update/adopt | Described next-round logic | Versioned data ingestion; independent confirmation and later scale transfer | R&D/process lead |

This is close to the analytical core of a scientist-in-the-loop workflow. It is less close to a complete lab handoff, and much further from evidence for a production recipe change. That is a reasonable stage for this take-home, provided the boundary is explicit.

## What I would change before sending it

1. Correct the confirmation paragraph and distinguish technical wells from independent preparations.
2. Add one explicit sentence about Qorium's animal-product-free feasible space and the FBS dependence of this demonstration.
3. Add a compact validity → screen → confirmation decision flow, including an inconclusive result.
4. Fix the preparation/lot/sample relationships in the schema.
5. Qualify the simulation conclusion and align the detailed batch report with the memo.

Keep the dataset, core GP implementation and overall recommendation unless these clarifications reveal a new decision requirement. Do not add more model families, a second full dataset, or production infrastructure. Replace lower-value technical detail to keep the memo at four pages.

For the interview, the strongest framing is: “This is a supervised next-experiment proposal. The model identifies useful comparisons, the concurrent anchor makes the screen interpretable, and independent confirmation determines whether a promising recipe deserves adoption.” Be prepared to explain why the next scarce slot should test a new blend rather than provide another independent repeat of the promising region.

## Verification record

The current PDF was inspected visually on all four pages. Its page count meets the brief. The notebook contains 11 executed code cells with no stored error outputs. Focused GP checks passed for pooled and recipe-specific noise during the isolated pipeline rerun. Independent calculations verified the confirmation-precision concern, percentage savings and FBS fractions above.

Full pipeline reproduction completed successfully in a temporary copy, including source verification, preparation, exploration, GP checks, model/policy comparisons, batch selection and memo figures. All 23 CSV files compared across outputs, evidence tables, processed data and cost inputs were byte-identical to the submitted files. The existing project Python environment was used; a fresh dependency installation and recipient GitHub access were not part of this check. The submitted artifacts were not overwritten.
