# Adversarial review: biology and leadership (Claude Fable 5.1, 2026-10-03)

Cursor agent, claude-fable-5-1-thinking-high, plan (read-only) mode, via Herdr, playing the CSO's role. Reviewed commit c37a45f.

1. Strongest attack on the recommendation

The batch spends two of four slots on
recipes the model itself cannot
distinguish from E19. Probe numbers from
the fitted pooled GP:

┌────────────────┬───────────┬───────────┐
│ Recipe         │ Posterior │ Corr.     │
│                │ mean      │ with E19  │
├────────────────┼───────────┼───────────┤
│ E19 (observed  │ 70.1      │ 1.00      │
│ 81.0)          │           │           │
├────────────────┼───────────┼───────────┤
│ Slot 1         │ 70.2      │ 0.981     │
├────────────────┼───────────┼───────────┤
│ Slot 4         │ 69.1      │ 0.882     │
└────────────────┴───────────┴───────────┘

Slot 1 is E19's posterior mean to one
decimal. The screen (memo.md:92) resolves
±13 points. So slots 1 and 4 buy
information the model prices at zero and
the assay cannot read.

Meanwhile the data's only signal is DMEM%.
Across rounds 1 and 2 it is already a
dose-response: 29% DMEM 48.0 (E07), 33%
48.6 (E08), 44.5% 68.1 (E12), 49% 55.3
(E15), 60% 46.9 (E09), 77% 43 to 56 (E16
to E18). Round 3's six blends vary RPMI 0
to 33%, X-VIVO 0 to 20%, AR5 15 to 55% and
score 67 to 81; SD of those six means is
5.2 against an expected SEM of 4.75. At
44% DMEM, the other three components are
noise.

The batch a panel would prefer: E19
anchor, slot 2 (cheapest 44% blend), slot
4 (AR5 to X-VIVO test), and two DMEM
titration points at E19's non-DMEM ratios.
The model predicts 40% DMEM at 66.2 and
50% at 62.4 (sd 7 to 8), a sharp peak
nothing has tested. Note 50% DMEM costs
EUR 178.67 against a ceiling of 178.43:
the cost rule excludes the obvious
experiment on a 0.13% difference derived
from a snippet FBS price. That is the
knife-edge nature of the ceiling, and Post
will see it.

2. Inconsistent, cherry-picked, or
over-claimed

• The replication exists and is unused.
  memo.md:40 "a recipe effect and a
  batch effect look the same";
  model_comparison.md:73 "the data
  cannot separate them". But
  data/interim/pbmc_Control_OptimalMedia
  Comparison.csv holds E19's recipe at
  80.2% (n=6, SD 7.5) beside DMEM-10
  alone 61.5, AR5 57.5, RPMI-10 49.5,
  X-VIVO 32.4. The sheet was excluded
  from training for the 200% AR5 row
  (DECISIONS.md), fine, but the E19 row
  is clean. It is the out-of-round
  reproduction the memo says does not
  exist, and together with E12 it makes
  the batch-effect framing the
  over-claim, not the under-claim.
  Neither appears in memo, walkthrough
  or exploratory_analysis.md.
• Apples to oranges in the headline
  table. memo.md:14-18 sets predictions
  of 60 to 70 against "historical mean
  81.0". E19's posterior mean (70.1) is
  nowhere in the memo. A reader concludes
  every pick loses by 11 to 21 points.

• Noise read as leads. memo.md:92 says a
  blend 10 points worse passes 23% of the
  time and 5 points worse 50%;
  memo.md:94-99 then reads a pass as
  "holds", "is a lead", "can stand in".
  The outcome table manufactures findings
  from a filter with 50% false-pass at
  the margin.
• Idle capacity. memo.md:10 "20 wells in
  total". plate_layout.csv has 60
  interior wells, 24 used, 36 idle. At 11
  wells per arm the 90% interval drops
  from ±13.1 to ±7.0 (t, 20 df) with zero
  extra formulations. The brief caps
  formulations, not wells. If cells or
  medium limit replicates, say so;
  otherwise this is the cheapest
  improvement in the submission.
• Simulation ignored. memo.md:74 finds
  UCB is the only policy that beats
  random; the deployed policy is not
  UCB, "for readability".

3. What Mark Post will challenge

• Endpoint. 72-hour viability of
  non-dividing suspension cells. For
  adherent fibroblasts, dead cells detach
  and are washed off before AOPI, so
  viability is near-uninformative; growth
  rate and collagen per cell are the
  endpoints. lab_plan.md:48-52 names them
  correctly. But lab_plan.md:54 says
  "the model and selection code stay the
  same". They do not: a simplex of four
  complete media becomes a box of 8 to 15
  defined components, the
  redundant-coordinate issue disappears,
  the kernel dimension triples on 24
  points, and the ceiling anchored on E19
  becomes medium cost per gram of
  collagen. And memo.md:120 "a weekly
  loop": collagen deposition under
  ascorbate runs 2 to 3 weeks, so a round
  is a month. Information per round
  matters more than here, which argues
  harder for replication over formulation
  count.
• Kolkmann 2020, cited to its author.
  lab_plan.md:49 and walkthrough.md:83
  use it for "serum-free growth runs
  below serum controls". That paper is
  primary bovine satellite cells, which
  are hard serum-free. Dermal fibroblasts
  are among the easiest cells to grow
  serum-free; commercial fibroblast SFMs
  exist. Post will ask what the paper
  found and whether it applies to his
  cells. This is the riskiest sentence in
  the submission. Reframe: "your 2020
  work shows the gap for myoblasts;
  fibroblasts should be easier to expand,
  so the open question is collagen
  output per cell under animal-free
  conditions."
• E14. memo.md:41 "could reflect biology
  or unrecorded preparation". To a tissue
  engineer, a 41-point drop with SD 2.7
  between near-identical media is a
  technical failure until proven
  otherwise. Keep E14 in the fit, but
  state the belief. Hedging reads as not
  knowing.
• Cheaper means more serum. memo.md:98:
  slot 2 raises FBS to 9.9%. To someone
  who spent a decade removing serum,
  this exposes the cost model as a toy;
  FBS is also the dominant lot-to-lot
  noise source, so round 3's "good day"
  may be an FBS lot. The schema has
  COMPONENT_LOT; the lab plan never
  names FBS lot as a logged variable.
• Answered adequately: donor and thaw
  (one donor on-plate, donors in
  confirmation), pooled C.BIRD reads
  versus single wells (lab_plan.md:17),
  pH/bicarbonate difference between DMEM
  and RPMI, CSO questions.

4. Where "AI did it, I directed it" is
exposed

• memo.md:60 "performed poorly, and
  these data do not establish why": a
  reviewer-substituted hedge. A Head of
  DS has a hypothesis: 10 coefficients,
  6 of 24 points on one DMEM line, two
  7% points no quadratic can bend to.
• memo.md:82 "which I flag rather than
  resolve": the resolution is textbook
  (drop a coordinate, or log-ratio
  transform). Flagging it signals the
  candidate does not know that.
• memo.md:67 the bespoke "integrated
  posterior-variance reduction over
  recipes that could still be the best"
  acquisition. If he cannot say it in
  one sentence, swap it for a textbook
  one.
• docs/ holds five AI review files;
  DECISIONS.md logs every finding as
  applied and none as rejected.
  memo.md:120 "the judgement calls are
  mine" has no exhibit.

Five concepts he must own, one sentence
each:

1. Round-recipe confounding: all the
   good recipes were run on one day, so
   "good recipe" and "good day" cannot
   be separated without re-running a
   recipe on another day.
2. Shrinkage: with 12 points of noise
   per recipe mean, the GP pulls E19's
   81 toward its neighbours to 70,
   because the top of six noisy results
   is partly luck.
3. Length scale at a bound: at the 10.0
   ceiling the model has found no effect
   of RPMI-10 or AR5 and treats them as
   interchangeable; at the 0.1 floor it
   believes viability changes sharply
   with small DMEM changes.
4. Pending-point conditioning: pretending
   a pick already returned its predicted
   value shrinks uncertainty there so
   the next slot looks elsewhere; it
   changes variance, never the mean.

5. Non-inferiority power: with 4 wells
   each and SD 9.5 the plate detects only
   losses above about 13 points, so
   passing a 5-point margin says little
   (77% pass at zero, 50% at minus 5).

5. Verdict: change before submission,
ranked

1. Add the E19 replicate (80.2, n=6) and
   E12 (68.1, round 1) to "What the data
   says". Verify in the paper's methods
   that the comparison sheet was a
   separate run. Recast the batch-effect
   line as "partly answered; the anchor
   measures the residual".
2. Put E19's posterior mean (70.1) in
   the recommendation table and say
   plainly that slot 1 equals it.
3. Swap slot 1 for a DMEM titration point
   (50% DMEM at E19 ratios, predicted
   62.4), keep slot 4 as the
   AR5-to-X-VIVO test. Loosen the ceiling
   to "within 1% of E19" so the rule
   stops excluding on snippet-price
   noise.
4. Fill the plate: 11 wells per arm,
   interval ±7.0; or state the cell or
   medium constraint that limits to 4.
5. Rewrite memo.md:94-99 so a "lead"
   requires beating E19 by more than the
   interval; a pass means only "not
   excluded".
6. Scope the Kolkmann sentence to
   myoblasts and add a
   fibroblast-specific expectation.
   Replace "weekly loop" with a monthly
   round and its consequence.
7. Fix lab_plan.md:54: list what changes
   (candidate generator, kernel inputs,
   cost denominator, endpoints, cycle
   time) instead of "code stays the
   same".
8. Log one rejected AI suggestion in
   DECISIONS.md and state the E14 belief
   in the memo. Those two lines are the
   evidence for "the judgement calls are
   mine".


yy

