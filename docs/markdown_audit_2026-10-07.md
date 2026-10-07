# Markdown audit — 7 October 2026

## Verdict and scope

The current supporting Markdown is presentable for case-study review after the corrections below. No change to the selected recipes or numerical outputs was required. The material supports an experimental proposal; assay approval and independent confirmation are still needed before execution or adoption.

The audit covered all **24 Markdown files tracked at baseline commit `2e8f5f5`**, including the README, current reports, schema, plans, decision log and 11 dated review records. Historical reviews were assessed as records of earlier snapshots, rather than current assertions. The memo source was read for alignment and retained. Following the user's scope clarification, the PDF, presentation, notebook and code were left unchanged. This report is the 25th Markdown file.

## Findings and corrections

| Priority | Finding | Correction and evidence |
| --- | --- | --- |
| Medium | The walkthrough and batch report said E10/E14 most likely differed because of preparation, and that concurrent re-runs would test preparation rather than medium | Corrected both reports. Shared-condition re-runs can test whether the recipe gap reproduces; they cannot establish its historical cause. Prioritising the DMEM contrast is a resource-allocation judgement. Both recipes remain in the primary fit |
| Medium | The walkthrough said all five formulations were no more expensive than E19 | Stated the base-price exception for designed steps. Slot 2 is EUR 178.69/L versus E19 at EUR 178.43/L; only model picks have the strict ceiling |
| Medium | The walkthrough said slot 4 would remove the unpriced AR5 cost | Replaced with partial substitution. The chosen recipe still contains 7% AR5 |
| Medium | Screening and confirmation wording blurred diagnostic steps, screened candidates and experimental units | Screen applies to slots 3 and 4. DMEM steps are diagnostic. Independent preparation repeats estimate preparation-level variance before confirmation is sized; this plate measures within-preparation repeatability |
| Medium | The batch report said the less-AR5 direction held in every other sensitivity rerun | Added the 1% model-cost-tolerance exception, whose slot 4 is 44/12/28/16. The main batch remains 44/21/28/7 |
| Medium | High model correlation was described as zero information value; forward bias became an extra uncertainty term | Removed those interpretations. Correlated candidates can add information. A forward miss demonstrates failed forecasting without quantifying a calibrated additional variance |
| Medium | The data dictionary described component costs as a durable editable input | Identified `price_sources.csv` as the source to edit. `build_costs.py` overwrites derived component costs and scenarios; direct component-cost edits are lost during the runner |
| Low | PLAN still said delivery was pending and listed already-resolved inputs; FIX_PLAN read as an active task list | Updated PLAN to the completed case-study snapshot and remaining lab handoff. Labelled FIX_PLAN historical and clarified the chronology in DECISIONS |
| Low | README's reproduction language implied every planning number was a generated result and all figures were byte-stable | Distinguished generated analysis results from conditional screen/confirmation calculations. CSVs and PNGs reproduced exactly; exploratory PDF content matched but creation timestamps changed. Corrected the figure count to 12 |
| Low | Lab-plan wording made unmeasured FBS lot variation and a proposed Qorium design sound established | Removed the claim that FBS was the measured largest variation source. Labelled Qorium component counts, media phases and timing illustrative, to agree with the team |

Additional clarity changes: the schema uses the current 11-well example and final batch roles; the lab plan spells out interpolation weights and labels failure triggers as proposed. The batch report describes a positive contrast as evidence of curvature along the tested path, rather than locating a local optimum. Curvature alone does not establish declines on both sides or identify an isolated ingredient effect.

## Verification

Checks were read-only against the submitted data, except for Markdown corrections. Before the scope was narrowed, an isolated clone completed the full runner using the existing pinned environment. A separate fresh environment installed the pinned analysis and notebook dependencies and passed `pip check`; its second full pipeline run was stopped when the user narrowed the scope. This audit therefore does **not** claim a completed fresh-environment pipeline execution.

- All **30 tracked CSVs** and **12 PNGs** matched the isolated completed rerun byte for byte. The five exploratory PDFs had identical page-content streams and changed only `/CreationDate`; submitted artifacts were preserved.
- Source hashes matched the manifest; the PBMC analysis has **24 formulations**, **103 readings** and **17 missing reading slots**. All 24 recipes remain in the primary dataset.
- The plate has **55 formulation wells**, **2 no-cell blanks**, **2 heat-killed controls**, **36 PBS edge wells** and one unused interior well. There are **57 cell-containing wells**, with 11 wells for each of five formulations.
- There are **19 sensitivity reruns**. Median volume shifts are 0%, 0%, 16% and 6% for slots 1 to 4.
- Independent arithmetic gives pooled reported-reading SD **9.5125** points and an approximately **6.996-point** 90% difference-interval half-width for 11 independent wells per arm, using t with 20 degrees of freedom.
- The normal-approximation screen pass rates are **89.12%, 50%, 10.88% and 0.68%** for true differences 0, −5, −10 and −15 points. These support the rounded figures in the lab plan, conditional on independent wells and the historical SD.
- Known-variance non-inferiority planning calculations give approximately **50.69%** power at 20 independent observations per arm and **80.19%** at 45. These are illustrations, not confirmation sample sizes for this assay.
- Local Markdown links resolved, CSVs had consistent row widths, and the final diff passed whitespace checks. No placeholder or unresolved TODO was found in current delivery Markdown.

## Remaining questions

These limit operational use and are already disclosed in the lab plan; they do not require more model families or production infrastructure for the case study.

1. Agree assay SOP, single-well versus pooled readout, cell supply, harvest and validity thresholds with the assay owner.
2. Agree the DMEM contrast's statistical test, significance threshold, missing-well treatment and row-block adjustment before the run. The approximate 48% power is an optimistic planning calculation, not measured assay performance.
3. Obtain independent preparation repeats before confirmation sizing. Historical reading spread does not establish preparation-level variance or biological independence.
4. Obtain comparable supplier quotes and agree adoption economics per acceptable output. FBS is snippet-priced and AR5 is a hypothetical proxy.
5. Verify the independence and protocol comparability of the reported 80.2% E19 comparison before treating it as independent reproduction.
6. The original 4-to-6-hour timebox cannot be verified from an actual effort log. The eight-minute walkthrough is a script; spoken timing needs rehearsal.

Qorium's [public process description](https://www.qorium.com/) supports the animal-product exclusion beyond cultured cells; it does not disclose its proprietary media recipes, phase timings or assay protocol. The lab-plan adaptation is consequently illustrative.

## File-by-file disposition

| Markdown file | Disposition |
| --- | --- |
| [README.md](../README.md) | Corrected navigation, figure count and reproduction claims |
| [reports/batch_selection.md](../reports/batch_selection.md) | Corrected rationale, sensitivity exception, uncertainty and screening scope |
| [reports/exploratory_analysis.md](../reports/exploratory_analysis.md) | Checked against processed data and descriptive tables; retained |
| [reports/lab_plan.md](../reports/lab_plan.md) | Clarified diagnostic, statistics, proposed criteria and illustrative transfer |
| [reports/memo.md](../reports/memo.md) | Read as the reference for supporting prose; retained to preserve the accepted rendered memo |
| [reports/model_comparison.md](../reports/model_comparison.md) | Corrected predictive-density interpretation and extra-uncertainty claim |
| [reports/walkthrough.md](../reports/walkthrough.md) | Corrected cost, AR5, E10/E14 and confirmation wording |
| [docs/DATA_DICTIONARY.md](DATA_DICTIONARY.md) | Corrected price-input lifecycle and provenance wording |
| [docs/data_audit.md](data_audit.md) | Counts, means, exclusions and normalisation checked; retained as generated evidence |
| [docs/SCHEMA.md](SCHEMA.md) | Current well count and roles aligned; conceptual/future status retained |
| [docs/PLAN.md](PLAN.md) | Replaced stale delivery status with current scope and handoff |
| [docs/FIX_PLAN.md](FIX_PLAN.md) | Labelled the original plan historical; original triage retained |
| [docs/DECISIONS.md](DECISIONS.md) | Chronology clarified; new corrections appended without rewriting history |
| [docs/review_gpt6_astra_2026-10-02.md](review_gpt6_astra_2026-10-02.md) | Historical initial review; old blocker and recipe values retained |
| [docs/review_fable51_2026-10-02.md](review_fable51_2026-10-02.md) | Historical post-fix review; earlier slot values retained |
| [docs/review_gpt6_astra_memo_2026-10-03.md](review_gpt6_astra_memo_2026-10-03.md) | Historical memo review; later resolution checked in decision log |
| [docs/submission_workflow_review_2026-10-03.md](submission_workflow_review_2026-10-03.md) | Historical workflow review; current replication and schema compared |
| [docs/review_adversarial_astra_2026-10-03.md](review_adversarial_astra_2026-10-03.md) | Historical review; its final verdict is an incomplete capture, retained as such |
| [docs/review_adversarial_fable51_2026-10-03.md](review_adversarial_fable51_2026-10-03.md) | Historical raw transcript; obsolete causal preferences are superseded by later entries |
| [docs/review_fable51_memo_2026-10-04.md](review_fable51_memo_2026-10-04.md) | Historical memo review; recommendation values and later corrections checked |
| [docs/review_biology_fable51_2026-10-04.md](review_biology_fable51_2026-10-04.md) | Historical biology review; accepted changes and retained options distinguished |
| [docs/review_adversarial_ds_astra_2026-10-04.md](review_adversarial_ds_astra_2026-10-04.md) | Historical statistical review; remaining test and preparation assumptions retained |
| [docs/review_language_chatgpt_2026-10-04.md](review_language_chatgpt_2026-10-04.md) | Historical editorial suggestions; retained without presenting them as current requirements |
| [docs/review_language_astra_2026-10-04.md](review_language_astra_2026-10-04.md) | Historical editorial adjudication; retained as captured |

Historical records include reviewer opinions subsequently withdrawn, old slot numbering and superseded statistics. They are supporting review history, not the document to use for the current recommendation. The batch report, model report and lab plan are the current supporting documents.
