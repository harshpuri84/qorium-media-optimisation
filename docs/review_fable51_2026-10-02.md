# Fable 5.1 review after fix steps 1-6 (2026-10-02)

Cursor agent, model claude-fable-5-1-thinking-high, plan (read-only) mode, run through Herdr.

Verification run: check_gp.py passes for pooled and SEM. I re-fitted
the GP read-only and reproduced P(above E19) = 0.536 / 0.267 /
0.124 / 0.382, the 11,585 2%-grid count, and every cell in both
report tables against the CSVs.

1. Status of the 11 findings

1. Fixed. GP._condition/fantasize (compare_models.py:67-78) keep
   ym, ys and the historical noise_vec; pending noise is explicit.
   check_gp.py asserts all of it.
2. Fixed. EI incumbent is best_mean() (compare_models.py:99-101);
   p_beats uses vx + v19 − 2cov (select_batch.py:87-94). Values
   moved 0.51→0.54, 0.22→0.27, 0.14→0.12, 0.37→0.38 and are
   reported.
3. Partly fixed. Renamed accurately, 3 seeds tested (max shift
   4%), four-role policy in the simulation, "one slot optimal"
   claim removed. But the explore argmax still runs only over the
   1,500 sample (select_batch.py:50-52), which is 19% of the
   7,975-point region.
4. Partly fixed. Forward failure now leads a section ("The models
   fail it"), forest spread labelled heuristic, intervals labelled
   conditional. No fold-kernel inspection and no noise-floor
   sensitivity.
5. Fixed. All-24 primary, E02/E14 withheld separately,
   "unexplained low outcomes", "no model clearly beats the mean".
6. Fixed as planned. 11.83 noise case, deployed policy, paired
   diffs, labelled illustrative. No batch-shift truth (FIX_PLAN
   consciously skipped it).
7. Fixed. ValueError on empty mask (select_batch.py:72-73);
   batch_threshold_stress.csv; "scenario counts are not
   probabilities"; single-media exclusion labelled operational.
8. Mostly fixed. Economics labelled provisional in both reports
   and README; €4.51/L called small; ceiling called a design
   choice. No performance-adjusted cost.
9. Partly fixed. 4 + E19 = 5, DMEM-10 dropped, anchor sums to
   100.0 mL. Still no replicate/well/plate budget anywhere.
10. Fixed. Mixture contrast wording, floors 0.05/0.2 tested, "AR5
    not needed"/"settles it" gone, PBMC→Qorium transfer stated.
11. Not fixed. Step 7 not started. README:3 "still to be written";
    README:20-23 still say "Reserved"; git root is still the vault
    with only the Dex remote.

2. New or remaining problems

• Two length scales pinned at the upper bound, not surfaced. Fitted
  kernel: Matern([0.1, 10, 0.326, 10]); bound is (ls_floor, 10.0)
  at compare_models.py:46. batch_selection.md:95 flags only the
  DMEM floor. Consequence: the model treats RPMI-10 and AR5 as
  interchangeable. corr(slot 1, E19) = 0.981, so the joint P = 0.54
  is "the model cannot tell them apart", not evidence. Note the
  independent-variance P would be 0.505; the joint fix made slots 1
  and 4 look more confident. Fix: state it; add GP(...,
  ls_upper=3.0) to variants in select_batch.py:138-144.
• Explore search space. select_batch.py:48-52 scores only sub.
  Fix: C = model.latent_cov(cand[region], cand[sub]) in chunks of
  ~2,000 rows, gain = (C**2).sum(1) / (var_region + noise),
  score[region] = gain. Also the threshold at line 46 uses
  mu[mask].max(); use model.best_mean() (equal here, 70.22 vs
  70.23, not in general).
• "Exploit-only is worse than random in all four settings"
  (model_comparison.md:103, batch_selection.md:50) is not what the
  paired statistic says: policy_simulation_summary.csv rows 2 and 7
  show median paired diff 0.0 / 0.03 and 13/30, 9/30 better. On
  the GP truth it is a tie. Rewrite: "no better than random; worse
  on the Scheffe truth".
• Simulation not like-for-like. four_role
  (compare_models.py:211-214) obeys the 5% gap, 6-of-9 and
  single-media rules; UCB/EI/random search the whole base-feasible
  grid (:234-235) and truth_max is over that grid. Four-role is
  handicapped, so its win is conservative, but say so or apply
  eligible() to all GP policies.
• Mean-only Spearman = −1.0 in model_loo.csv
  (compare_models.py:151): LOO means shift with the held-out
  point, so it is not constant. Report says n/a; CSV contradicts.
  Fix: return nan for MeanOnly.
• SEM model predictive sd (compare_models.py:94-97) uses mean SEM²
  for every held-out point; LOO coverage for that row is slightly
  wrong. Minor.
• Pairing: correct. Same init and same standardised noise draws per
  seed across policies and noise levels; Random consumes extra
  draws but never uses them.
• Numbers: all report cells reconcile with the CSVs. Only
  batch_selection.md:72 slot 3 price median prints 20 for a true
  19.5. DECISIONS.md:52,57 still give the without-E02/E14 RMSE as
  the model-choice reason and mention the DMEM-10 control; they
  are log entries, but the memo must not inherit them.

3. Ready for the memo?

Yes, with the two wording fixes above done first (exploit-vs-random
claim, length-scale bound). The GP math is now correct and the
artefacts are internally consistent. Three things the memo must say:

1. The model is effectively two-dimensional. DMEM at its floor,
   RPMI-10 and AR5 at their ceiling. Slots 1, 2 and 4 all spend the
   assumption that AR5 volume can move to RPMI-10 or X-VIVO 15 for
   free. The batch tests that assumption; it does not rest on it
   being true. Slot 2 (43/56/1/0) is where the SEM model disagrees
   most (51.9 vs 65.9) and where the stress table flips it to
   0/92/0/8 at a 5% margin.
2. Ranking aid, not forecast, and the decision rule follows from
   that. No model beats the mean on all-24 NLPD; round 3 was
   missed by 22 to 29 points. Every P(above E19) is under the
   model and excludes batch effects. The read-out is the
   same-plate contrast against the E19 re-run: if E19 lands near
   55, judge picks against 55, not 81.
3. Every threshold is a choice, and the lab contract is still thin.
   Ceiling = E19's cost (not a budget), FBS from a snippet, AR5
   hypothetical, 2.5%/5%/6-of-9 rules. Say wells and biological
   replicates per formulation, that a 12-point noise SD means a
   single plate cannot promote a lead, and that PBMC viability
   stands in for Qorium's expansion and collagen assays.
