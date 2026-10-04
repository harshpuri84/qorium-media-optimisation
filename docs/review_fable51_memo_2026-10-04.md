# Fable 5.1 review of the final memo (2026-10-04)

Cursor agent, claude-fable-5-1-thinking-high, plan (read-only) mode, via Herdr. Reviewed commit e06ab52.

1. Coverage

• Problem framing: covered (memo.md:34).
• Assumptions and constraints: covered (table,
  memo.md:38-47).
• Objective definition: covered (memo.md:36), but see
  contradiction in section 4.
• Exploratory findings: covered (memo.md:53-58).
• Modelling approach and algorithm rationale: covered
  (memo.md:62-66).
• Uncertainty handling: covered (memo.md:70-83).
• Recommended next experiments: covered.
• Risks, limitations, validation plan: thin. Three bullets
  at memo.md:118-120; dataset limits (no donor IDs, pooled
  readings, FBS lot) appear only in passing.
• Exploration/exploitation justification: covered but the
  wording is attackable (section 3).
• Six strategy scenarios: covered, one line each; the
  categorical row is the thinnest.

2. Accuracy

Every recommendation-table value, cost, interval, probability,
LOO/forward metric, simulation figure, rerun count (19),
median shifts (16%, 6%), well counts (11, 57, 36 idle) and
screen statistics (±7, 89%, 11%) reconcile with the CSVs.
Mismatches:

• memo.md:42 "At least 5% of volume from any tested recipe":
  slot 1 is 4.7% from E19 (next_experiments.csv,
  nearest_gap_pct). The rule holds for model picks only; say
  so.
• memo.md:8 "at no more than E19's cost": slot 2 is EUR
  178.69 against 178.43 (memo.md:17, 28). Thesis contradicts
  the table.
• memo.md:44 "Viability at 72 h, plus viable cells per mL |
  Only public endpoint": viable cells per mL is not in the
  public data; it is a new readout for this plate.
• memo.md:81 "by 72% only in the fit without DMEM": true for
  the maximum, but slot 4 also moves 34% under per-recipe
  noise (batch_stability.csv, gp_sem_noise). Say "72% without
  DMEM, 34% under per-recipe noise, under 10% otherwise".


3. Five sentences a skeptical CSO or ML lead will challenge

1. memo.md:22 "compare picks with 70.1, not 81" sits beside
   memo.md:56, where E19 reproduced at 80.2 (n=6). The lab
   has measured E19 at ~80 eleven times; the model says 70.
   A CSO will say the model, not E19, is wrong.

   Replace: "The model shrinks E19's 81.0 to 70.1 because its
11.8-point noise estimate treats the top of six as partly
luck. The independent 80.2 re-run suggests that shrinkage is
too strong, which is one more reason the same-plate E19, not
the model, sets the bar."

2. memo.md:57 "E14 is most likely a technical failure; I
   keep it in the fit because dropping data by outcome
   biases the model." If you believe it is technical,
   keeping it is what biases the fit (slot 4 predicted 69.1
   with E14, 87.0 without).

   Replace: "E14 is most likely a technical failure, but no
record proves it. It stays in the primary fit; without it the
picks move by at most 1% of volume, while slot 4's estimate
rises from 69 to 87, so the plate, not the fit, decides."

3. memo.md:26 lists 29 to 33%, 44.5%, and 60 to 77% DMEM and
   skips E15 (49%, 55.3) and E05 (54.5%, 41.7). A CSO will
   say 50% has been tested and fell.

   Replace: "Near 50% DMEM, E15 (49%) scored 55 and E05
(54.5%) 42, both at different ratios of the other three media.
The 50% step at E19's ratios separates the DMEM effect from
those ratios."

4. memo.md:85 "The batch explores where the model is most
   confident and least tested." In BO terms exploration goes
   where uncertainty is highest; this phrasing invites a
   correction.

   Replace: "Slots 1 and 2 are designed contrasts, not
acquisition picks: they test the model's sharpest assumption,
the DMEM length scale at its floor, where posterior sd (7.3)
is also higher than at the model picks (5.5 to 7.2)."

5. memo.md:64 "The random forest matched its error but gives
   no principled uncertainty." Quantile forests and jackknife
   intervals exist, and the RF's 80% coverage (0.79) equals
   the GP's.

   Replace: "The random forest matched the GP's error and
coverage (0.79), but its tree-spread interval is not a
posterior I can condition on pending picks; the GP's is."

Also verify memo.md:56 "separate comparison": if the control
comparison ran the same day as round 3, it reproduces nothing.
Check the paper's methods before submission.

4. Duplication and contradiction in the new sections

• Constraints table memo.md:41 repeats the Cost paragraph
  memo.md:28 word for word in substance.
• "How sure we are" rows for model form, low results and
  prices (memo.md:73-75) restate the Robustness paragraph
  memo.md:81. Keep one.
• memo.md:36 objective "cost no higher than E19's"
  contradicts memo.md:28, 41 allowing designed steps 1%
  over. Scope the objective's constraint to model picks.
• memo.md:77 "Batch shift | E19 re-run on the same plate; 11
  wells per formulation": replicates measure within-plate
  noise, not batch shift. Move the 11 wells to the
  reading-noise row.
• memo.md:85 "two designed steps that answer a clear
  question whatever the model believes" restates
  memo.md:26-27.
• memo.md:34 "each round takes days" and memo.md:118 "weeks,
  not days" are consistent (PBMC vs Qorium) but read as a
  clash; add "for PBMCs" at line 34.

Verdict: ready after the listed fixes; the four accuracy items
and sentence 1 are the ones to do.
