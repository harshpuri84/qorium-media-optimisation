# GPT-6 Astra review of memo and walkthrough (2026-10-03)

Codex, GPT-6-Astra medium, read-only, run through Herdr. Second review in the same session as review_gpt6_astra_2026-10-02.md.

## 1. Accuracy

Read-only review completed. The PDF is four A4 pages. Recommendation
recipes, costs, intervals and probabilities in reports/memo.md:14–18
match the output CSVs. The EDA figures, validation table, simulation win
counts, kernel values and correlation 0.981 also reconcile; I
independently refitted the main GP.

Corrections and qualifications:

 Location                Issue                    Correct value/source
━━━━━━━━━━━━━━━━━━━━━━  ━━━━━━━━━━━━━━━━━━━━━━━  ━━━━━━━━━━━━━━━━━━━━━━━
 reports/memo.md:42      FBS contributes “74      74.30%–79.79%,
                         to 79%.”                 therefore 74–80%
                                                  rounded; calculated
                                                  from data/inputs/
                                                  price_sources.csv and
                                                  component_costs.csv.
──────────────────────  ───────────────────────  ───────────────────────
 reports/                “Three of the four       All four: AR5
 walkthrough.md:51;      picks move volume out    fractions 11%, 0%,
 omission in             of AR5.”                 0%, 7%, versus anchor
 memo.md:81                                       15.7%; outputs/
                                                  plate_formulations.cs
                                                  v:2–6.
──────────────────────  ───────────────────────  ───────────────────────
 reports/                Slots 1 and 4 “barely    Median shifts 0%/7%,
 walkthrough.md:49       move.”                   maxima 26%/12%; slot
                                                  4 changes in 14/14
                                                  reruns. Source:
                                                  outputs/
                                                  next_experiments.csv:
                                                  2,5.
──────────────────────  ───────────────────────  ───────────────────────
 reports/memo.md:113;    Runtime “about 5         Unverified, not
 README.md:31            minutes.”                demonstrably wrong:
                                                  no timing evidence
                                                  supplied, and I did
                                                  not run the output-
                                                  writing pipeline.
                                                  Qualify by machine or
                                                  supply a timed run.

walkthrough.md:23–27 uses reasonable spoken rounding: 72.65→73,
40.627→41, €172.49–180.98→€172–181. These are not mismatches.

## 2. Coverage against the brief

Covered: decision-first framing, objective, EDA, multiple approaches,
five formulations, exploration/exploitation rationale, all six scenarios
(memo.md:99–104), schema and walkthrough.

Still missing or thin:

• Timebox: memo.md:115 retains [HOURS TO BE CONFIRMED BY HARSH], also
  present in the PDF. Replace with actual total effort, including domain
  learning; acknowledge any overrun.

• GitHub delivery: the project now has its own Git repository and
  commit, but git remote -v is empty. Supply an accessible GitHub
  repository link and verify the submission contents.

• Replication: memo.md:10,77,93 specifies wells, not biological
  independence. State whether wells share cell preparation/donor and
  medium preparation; specify independent preparations/days for
  confirmation.

• Decision criterion: memo.md:111 defines success as “within noise.”
  Non-significance does not establish equivalence. Predefine a
  biologically acceptable viability-loss margin and confirmation
  criterion.

• Uncertainty: add a table footnote at memo.md:18: “Intervals describe a
  new measured recipe mean conditional on this model; probabilities
  compare latent responses with E19 and exclude unmodelled batch
  shifts.” Historical reading independence is unknown.

• Feasibility: memo.md:30 needs an explicit assumption that the lab
  accepts these commercial-media blends and dispensing volumes.

• Multi-fidelity: memo.md:100–101 should require paired calibration
  experiments before relying on cheap assays; expensive assays also need
  coverage that estimates cross-assay relationships.

• Schema: docs/SCHEMA.md:140 says measurements can attach to a RUN, but
  MEASUREMENT only has well_id. Clarify linking matched cultures across
  destructive assays; donor/pool and biological-replicate identifiers
  need explicit treatment.

• Reproduction: run_all.sh:6–8 rebuilds analysis outputs, not the memo
  PDF. Document its rendering command separately.

## 3. Claims a panel could attack

• Ranking as the escape hatch: memo.md:55–57; walkthrough.md:33–35,63.
  Forward GP Spearman is 0.257, −0.314, 0.257, not evidence of reliable
  prospective ranking (model_forward_round.csv:2–4). Use replacement
  below.

• “Ten parameters … is too many”: memo.md:55. Bayesian ridge
  regularizes; parameter count alone does not explain failure. Replace:
  “The fitted quadratic performed poorly here; these data do not
  establish why.”

• Failed run versus biological cliff: memo.md:37; walkthrough.md:25
  creates a false dichotomy. Replace: “Consistent low readings could
  reflect biology or unrecorded preparation, cell-source or assay
  conditions.”

• Cost “only matters” when prices move: memo.md:40; walkthrough.md:27.
  Base-price constraints already exclude 49.7% of the grid. Replace:
  “Base-price differences are modest, but the ceiling materially
  restricts selection.”

• AR5 quote is “most valuable”: memo.md:42; walkthrough.md:27. No value-
  of-information comparison establishes this. Replace with “an important
  missing input alongside the dominant FBS price.”

• Conditioning “pushes” picks away: memo.md:59; walkthrough.md:41. It
  reduces variance while preserving means; the explicit distance rule
  enforces separation.

• Exploration identifies the best location: walkthrough.md:41. It
  minimizes integrated response variance over a model-defined region,
  not optimizer uncertainty directly.

• E19 at 55 proves a batch effect: memo.md:88,109; walkthrough.md:57.
  One discrepant anchor cannot identify cause. Say “would trigger
  investigation of reproducibility and batch conditions.”

• Unequal simulation constraints necessarily handicap the policy:
  model_comparison.md:91. Restrictions can regularize search
  beneficially. Replace with “Different eligibility rules prevent
  attributing gains solely to acquisition strategy.”

## 4. Communication: three weakest passages

The opening recommendation is clear. The main readability problem is
reassuring language that exceeds the evidence.

A. Model rationale — memo.md:55–57; walkthrough.md:33–35

> “The GP provides a usable uncertainty-based selection rule, but
> neither its predictions nor its rankings are prospectively validated.
> Its forward-round rank correlations are 0.26, −0.31 and 0.26. I
> therefore use it to propose a diverse batch, with a concurrent E19
> anchor and independent confirmation before adoption.”

B. Robustness — memo.md:79; walkthrough.md:49

> “Slot 1 is unchanged in eight of fourteen reruns, but shifts 26% under
> the alternative noise model. Slot 4 shifts a median 7% and at most
> 12%. These are recurring search directions, not uniquely established
> recipes; slots 2 and 3 are more sensitive.”

C. Validation — memo.md:87–93,111; walkthrough.md:57

> “Compare each candidate with concurrent E19 using a prespecified
> acceptable viability-loss margin. Four wells assess within-plate
> repeatability; they do not establish robustness across cell
> preparations or days. Advance promising candidates to independent
> confirmation. A low E19 result triggers investigation rather than
> proving a historical batch effect.”

Also define RMSE, coverage and NLPD beneath memo.md:48–53; distinguish
five model variants from the four displayed rows.

## 5. Status of the original 11 findings

1. Fixed: conditioning preserves scaling and historical noise; focused
   checks exist.

2. Fixed as approximation: posterior-mean EI incumbent and joint E19
   covariance implemented.

3. Mostly fixed: full-region variance reduction implemented; walkthrough
   terminology still overstates it.

4. Partial: failures disclosed, but ranking reassurance, noise-floor
   checks and replicate interpretation remain weak.

5. Mostly fixed: all-data analysis primary; “failed run” wording has
   resurfaced.

6. Partial: deployed policy/high-noise simulation added; unequal
   eligibility and smooth-truth limitations remain.

7. Fixed operationally: thresholds stress-tested, empty masks rejected,
   exclusions acknowledged.

8. Partial: provisional economics transparent; quote-priority claim
   remains unsupported.

9. Mostly fixed: five formulations, normalized anchor and 20 wells;
   biological replication remains unspecified.

10. Partial: sensitivity improved; causal interpretations persist in the
   memo/walkthrough.

11. Mostly fixed: deliverables and isolated repo exist; hours
   placeholder, GitHub publication and PDF reproduction remain.

Verdict: ready after listed fixes.
