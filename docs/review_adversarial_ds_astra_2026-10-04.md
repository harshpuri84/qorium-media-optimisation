# Adversarial data-science review of the final memo (GPT-6 Astra, 2026-10-04)

Codex, GPT-6-Astra medium, read-only, via Herdr. Reviewed commit a729478.

## 1. Decision logic

The redesign is defensible; claiming it will settle the DMEM peak is not.
Revising a batch after criticism is good judgment, but the new rationale needs
an explicit estimand and power calculation rather than retrospective
certainty.

memo.md:8 promises “enough replicates to read the result”; :120 defines
success as settling whether the peak is sharp. Yet the model predicts drops
from E19 of only 3.8 points at 40% DMEM and 7.6 at 50%. With SD 9.51 and 11
independent wells per arm:

• Difference SE is 4.06 points.

• Approximate one-sided 5% detection power is 24% and 59%, respectively.

• A prespecified curvature contrast—E19 minus the interpolated response
  between the two steps—has predicted magnitude 5.57 points, SE 3.52, and only
  48% power.

These are optimistic known-variance calculations excluding preparation
effects.

What I would recommend: retain the five formulations as an exploratory local
design, but preregister that curvature contrast and explicitly allow
“inconclusive.” Do not promise to establish sharpness. Approximately 28
independent observations per formulation would give 80% power for that
particular model-implied curvature under the same assumptions—already
exceeding this plate’s capacity. Independent preparation blocks matter more
than presenting 11 technical wells as decisive.

## 2. Statistics and misleading interpretations

• memo.md:22: “noise estimate treats the top of six as partly luck.” The GP
  contains no “top-of-six” selection adjustment. E19 shrinks through
  conditioning on all observations, the fitted mean, covariance and noise. The
  possible 80.2% repeat is useful external evidence, but cannot establish
  excessive shrinkage without resolving independence and protocol
  comparability.

• :26,98: “separates the DMEM effect” / “The sharp DMEM peak is real.” These
  are mixture-path effects: increasing DMEM necessarily dilutes the other
  media. A decline on one side does not establish a peak; even declines on
  both sides establish only a local response along this path. Replace with:
  “Evidence of curvature along the E19-ratio dilution path, requiring
  independent confirmation.”

• :58: “E14 is most likely a technical failure.” Low within-run SD 2.70 cannot
  distinguish reproducible low biology from a shared preparation failure. This
  unsupported causal preference now drives rejection of the diagnostic
  alternative.

• :63: Scheffé fails “because its 10 coefficients face 24 points.” That
  explanation was previously corrected and has returned. Regularization,
  response shape, coverage and confounding all matter; the data do not
  identify the cause.

• :67: log-ratio coordinates are “the standard alternative.” They require
  handling genuine zero components, which these recipes contain. State the
  zero-handling assumptions before promising this next step; ordinary
  orthonormal simplex coordinates are another option.

• :90: ±7 points and 89%/11% pass rates. Arithmetic is correct under
  independent normal well errors with SD 9.51. It is not demonstrated assay
  performance; it excludes preparation-specific errors and assumes historical
  reading spread transfers to unpooled wells.

• :82: UCB “beat random reliably.” These are unadjusted exploratory discovery-
  regret tests. A Bonferroni threshold across 16 comparisons is 0.003125:
  0.016 does not clear it. Use “nominal evidence in two settings.”

## 3. Internal mismatches only

• memo.md:90 requires equal or lower cost to pass, but slot 2 intentionally
  costs €178.69 versus €178.43. It cannot pass the stated screen.

• batch_selection.md:34 says every pick maintains a 5% gap; slot 1’s recorded
  gap is 4.7% (outputs/next_experiments.csv).

• memo.md:24 says the other ratios are the same. Whole-percent rounding makes
  them approximate: 22:21:17 and 18:18:14, versus E19’s 20.1:19.6:15.7.

• batch_selection.md:41 says slot 4 removes AR5’s uncertain cost; slot 4 still
  contains 7% AR5.

• model_comparison.md:87,90 calls the simulated four-role policy the deployed
  recommendation; deployment now uses two designed steps.

• compare_models.py:55–56 defaults new_wells=4; select_batch.py:187 does not
  override it in the reading-count sensitivity, despite 11 wells now planned.

• The 1% designed-cost tolerance is checked only at base prices
  (select_batch.py:175). At half-price FBS/base AR5, slot 1 costs €136.53
  versus €134.93, approximately 1.19% more. Clarify the scope of memo.md:36.

## 4. Questions exposing AI dependence

• What exactly are you testing? “Curvature along one mixture path, not an
  isolated causal DMEM effect.”

• Why does E19 shrink? “The posterior combines its observation with
  neighboring data and fitted noise; it does not explicitly correct for
  winning six trials.”

• What does 11 wells buy? “Within-preparation precision, not eleven
  independent biological replications.”

• Why is P(above E19) not the screening probability? “It compares latent
  responses under the GP; the screen compares noisy measured means with a
  five-point margin.”

• Why keep these recipes after sensitivity failures? “They are interpretable
  hypotheses to test, not robustly identified optima.”

## 5. Ranked fixes

1. Preregister the curvature contrast, uncertainty calculation and
   inconclusive outcome; remove “settles” and “peak is real.”

2. Separate diagnostic interpretation from adoption screening, so the
   deliberately over-budget step remains useful.

3. Qualify the power/pass-rate assumptions and specify independent preparation
   repeats.

4. Remove unsupported causal explanations for E14 and Scheffé; rewrite
   shrinkage accurately.

5. Fix the seven mismatches above, including new_wells=11.

6. Replace “reliably” with exploratory evidence and specify how zero-
   containing mixtures would be modeled.

Verdict: ready after these fixes—the batch is a reasonable exploratory design,
but its promised conclusions remain stronger than its information capacity.

