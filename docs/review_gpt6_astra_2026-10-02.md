• Read-only review completed; no files changed. I checked the requested
code and artifacts and recomputed CSV summaries, but did not run
pipelines that overwrite outputs. The submission is not ready: the
batch-noise bug, capacity ambiguity and missing deliverables need fixing
first.

## Section A — Findings

Paths below are relative to the case-study folder.

 #                      1
 Severity               blocker
 File:line or artifact  scripts/select_batch.py:38–42; scripts/
                        compare_models.py:158
 Issue                  Kriging believer changes the fitted model
                        incorrectly.
 Evidence               SEM-model refits replace every historical noise
                        variance with alpha=1e-6. Both implementations
                        recompute target normalization after fantasies,
                        changing kernel/noise scales in original units
                        despite “fixed hyperparameters.”
 Proposed fix           Freeze initial target scaling; preserve
                        historical noise and assign explicit fantasy
                        noise. Verify analytical conditioning. GPR
                        documentation (https://scikit-learn.org/stable/
                        modules/generated/
                        sklearn.gaussian_process.GaussianProcessRegresso
                        r.html) confirms alpha represents observation
                        variance.
────────────────────────────────────────────────────────────────────────
 #                      2
 Severity               major
 File:line or artifact  compare_models.py:172–175; select_batch.py:141
 Issue                  Acquisition and reported comparison use
                        inconsistent incumbents.
 Evidence               EI targets the noisy maximum 81%; reported
                        probabilities target E19’s fixed posterior
                        estimate 70.1%. The reported 0.51/0.22/0.14/0.37
                        are not probabilities of beating uncertain E19
                        itself.
 Proposed fix           Use a clearly labelled posterior-mean incumbent
                        approximation or noisy EI. For superiority use
                        joint posterior difference variance: vx + v19 −
                        2cov(x,19).
────────────────────────────────────────────────────────────────────────
 #                      3
 Severity               major
 File:line or artifact  select_batch.py:51–65; reports/
                        batch_selection.md
 Issue                  Exploration is overstated.
 Evidence               Score is integrated latent variance reduction
                        over 1,500 sampled eligible candidates, not
                        information gain about the optimizer. It
                        searches only that sample. The final four-role
                        policy is absent from the simulation.
 Proposed fix           Rename the criterion precisely; test sampling
                        stability; compare the actual four-role policy
                        before claiming the simulation establishes “one
                        exploration slot” as optimal.
────────────────────────────────────────────────────────────────────────
 #                      4
 Severity               major
 File:line or artifact  reports/tables/model_forward_round.csv;
                        compare_models.py:24,39–63,86–88
 Issue                  Uncertainty fails prospectively; the report
                        underplays this.
 Evidence               Pooled GP: round-1 coverage 16.7%, NLPD 246.061;
                        round-3 coverage 0%, bias 26.764 points. Forest
                        tree spread is not an observed-outcome
                        predictive interval. Learned 11.83-point noise
                        also absorbs model misspecification.
 Proposed fix           Surface these failures; inspect fold kernels/
                        residuals; add a conservative noise-floor
                        sensitivity. Label intervals conditional and
                        forest spread heuristic; retain optimizer
                        warnings.
────────────────────────────────────────────────────────────────────────
 #                      5
 Severity               major
 File:line or artifact  reports/model_comparison.md;
                        compare_models.py:233–234
 Issue                  Outcome-conditioned deletion supports an
                        overstated model-choice argument.
 Evidence               Removing E02/E14 changes both training and
                        evaluation populations: GP RMSE 16.77 → 7.56. On
                        all data RF RMSE is 16.32, while mean-only NLPD
                        4.435 beats GP 5.934. Calling E14 a “failed run”
                        is unsupported.
 Proposed fix           Keep all-data results primary; withhold E02 and
                        E14 separately as sensitivity checks; describe
                        them as unexplained low outcomes. Avoid
                        declaring a clear GP winner.
────────────────────────────────────────────────────────────────────────
 #                      6
 Severity               major
 File:line or artifact  compare_models.py:201–218; reports/
                        model_comparison.md
 Issue                  Simulation favors smooth-surrogate policies and
                        understates noise.
 Evidence               Both truths are fitted means from the same 24
                        observations. Noise SD 4.97 is below fitted
                        residual SD 11.83; no batch shifts or failure
                        mechanism. Median regrets 2.89 versus 7.82
                        reproduce, but establish only conditional
                        performance.
 Proposed fix           Add one failure/batch-shift truth and higher-
                        noise case with paired seeds; include the
                        deployed policy and report paired differences.
                        Otherwise explicitly downgrade to an
                        illustrative simulation.
────────────────────────────────────────────────────────────────────────
 #                      7
 Severity               major
 File:line or artifact  select_batch.py:23–29,68–88; design_space.py:49
 Issue                  Several consequential constraints are arbitrary;
                        empty eligibility silently fails.
 Evidence               E19 ceiling €178.43/L, 2.5% discount, 5% gap and
                        6/9 scenarios lack decision justification.
                        argmax over all −inf returns an invalid
                        candidate. Single-media exclusion contradicts
                        unresolved comparison-sheet provenance.
 Proposed fix           Parameterize and stress-test thresholds; reject
                        empty masks; distinguish operational exclusions
                        from validated observations. Scenario counts are
                        not probabilities.
────────────────────────────────────────────────────────────────────────
 #                      8
 Severity               major
 File:line or artifact  data/inputs/price_sources.csv; scripts/
                        build_costs.py:11–29
 Issue                  Economics depend on weak proxies.
 Evidence               FBS €672/500 mL is snippet-only; AR5 €181/L is
                        hypothetical; high AR5 uses another product’s
                        ratio. Slot 2 saves only €4.51/L while
                        increasing supplemented-media share to 99%.
 Proposed fix           Label economics provisional; obtain comparable
                        quotes or retain explicit hypothetical ranges.
                        Explain relative-to-E19 versus fixed-budget
                        ceilings and assess performance-adjusted cost.
────────────────────────────────────────────────────────────────────────
 #                      9
 Severity               blocker
 File:line or artifact  reports/batch_selection.md
 Issue                  Four recommendations plus two controls require
                        six formulations.
 Evidence               Brief allows 3–5; extra control capacity is
                        assumed. Printed E19 recipe totals 100.1%. No
                        concrete biological replication/plate budget is
                        supplied.
 Proposed fix           Default to four candidates plus E19—five
                        formulations—and remove the extra DMEM control
                        unless capacity permits. Normalize E19 volumes;
                        specify independent cultures, wells and
                        blocking.
────────────────────────────────────────────────────────────────────────
 #                      10
 Severity               major
 File:line or artifact  reports/batch_selection.md; compare_models.py:40
 Issue                  Biological conclusions exceed the design.
 Evidence               Changing DMEM to 37% also changes three other
                        fractions; one result cannot separate DMEM
                        causality from round effects. Length scale 0.1
                        hits its imposed floor. “AR5 is not needed” and
                        “one result settles it” overclaim.
 Proposed fix           Test floor sensitivity; describe mixture
                        contrasts, not ingredient effects. Require
                        replicated same-batch confirmation; connect PBMC
                        viability explicitly to a future Qorium
                        productivity assay.
────────────────────────────────────────────────────────────────────────
 #                      11
 Severity               blocker
 File:line or artifact  docs/PLAN.md; README.md; repository inventory
 Issue                  Required packaging is unfinished.
 Evidence               No final 3–4-page memo, walkthrough or explicit
                        six-scenario response found. Schema exists. Git
                        root is the parent personal vault; only the Dex
                        upstream remote is shown. README still says
                        modelling is pending.
 Proposed fix           Finish deliverables, isolate the case-study
                        repo, provide one-command reproduction, update
                        stale generated prose and report actual—not
                        planned—time spent.

## Section B — Ordered fix plan

1. Repair posterior conditioning and acquisitions — 40–55 minutes.
   Change compare_models.py, select_batch.py; add focused checks. Verify
   preserved historical variances/scaling, nonincreasing conditional
   variance, joint E19 probabilities and explicit empty-mask failure.

2. Set an executable lab/cost contract — 20–30 minutes.
   Change design_space.py, select_batch.py, docs/DECISIONS.md, price
   inputs. Verify five total formulations, normalized preparation
   volumes, scenario feasibility and sensitivity to discount/gap
   assumptions.

3. Reassess evidence — 35–50 minutes.
   Change compare_models.py, reports/model_comparison.md. Inspect
   disastrous forward folds; test noise/length-scale floors and
   individual exclusions. Add only a small adversarial simulation;
   verify the actual selection policy is evaluated.

4. Regenerate and reconcile — 15–25 minutes.
   Update outputs, tables, reports and stale prose in prepare_data.py/
   explore_data.py. Verify every quoted recipe, cost, interval and
   stability statistic against regenerated artifacts; remove causal and
   robustness overclaims.

5. Package the submission — 45–60 minutes.
   Create memo, timed walkthrough and runner; update README/schema and
   isolate the repo. Explicitly answer all six scenarios: 10–20
   observations, cheap noisy assays, expensive reliable assays, missing
   costs, categorical constraints and parallel batches. Verify clean-
   environment execution, page/time limits and elapsed-work disclosure.

## Section C — Five hardest interview questions

1. Why trust this GP after NLPD 246 and zero round-3 coverage?
   “I trust it only as a conditional ranking aid; conservative
   sensitivity checks and a concurrent anchor govern the decision.”

2. What exactly does ‘51% better than E19’ mean?
   “Currently it compares against a fixed posterior estimate; the
   corrected comparison includes E19 uncertainty and covariance.”

3. Did your simulation validate these four recipes?
   “No; it compared policies under fitted synthetic truths and did not
   evaluate the deployed four-role policy.”

4. Why exclude recipes within 5% when replication could be more
   valuable?
   “That was a diversity heuristic; replication and local confirmation
   must compete explicitly within the capacity budget.”

5. What does PBMC viability tell Qorium about leather production?
   “It demonstrates the optimization workflow; transfer requires Qorium-
   specific cell expansion, matrix production and quality endpoints.”

