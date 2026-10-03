# Walkthrough script (8 minutes)

The walkthrough is a screen share of the repo. Each block lists what is on screen, then what to say. Times are cumulative. Speak to the decision, not the code.

## 0:00 to 0:45. The answer first

**Screen.** `reports/memo.pdf`, page 1, the recommendation table.

"I recommend five formulations for the next batch: four new blends of the four commercial media, plus a re-run of our best historical blend, E19, on the same plate. Four wells each, 20 wells in total. Every new blend costs no more per litre than E19. Each slot has a different job. One exploits, one is cheaper, one explores, and one goes after the biggest expected gain. This plate is a screen; anything that passes goes to a larger confirmation run. I'll spend the next seven minutes on why these four, and on how far you should trust the numbers."

## 0:45 to 1:45. The problem and the data

**Screen.** Memo, "The problem" section. Then `reports/figures/01_viability_by_experiment.png`.

"The brief is an experiment-recommendation problem, not a prediction contest. I used the public PBMC media-blending data from Narayanan 2025: 24 blends of four media, four rounds of six, viability at 72 hours. I picked it over the Cosenza muscle-cell repo because its tables are labelled and the four-part mixture keeps cost and feasibility easy to check. PBMC viability is not Qorium's endpoint, and these media carry FBS. E19 is six and a half percent serum, and every pick raises that. Qorium uses no animal products beyond the cells, so a real campaign would start from an animal-free ingredient list. The method transfers. The recipes and numbers don't."

"The objective is to maximise viability without paying more per litre than E19. I chose a constraint over a desirability score because a lab manager can check a constraint by hand. That ceiling is a screening gate, not a business case. Savings against E19 are under 3%, so adoption needs an agreed minimum saving measured on cost per acceptable output."

## 1:45 to 3:00. Three things the data told me

**Screen.** `reports/figures/03_mixture_compositions.png`, then `05_nearest_recipe_pairs.png`.

"First, round 3 beat every earlier round, 73% against 40 to 51%. But all six round-3 blends sit at 44% DMEM, so a good recipe and a good lab day look identical in this data."

"Second, E10 and E14 are 2.6% of volume apart and 41 points apart in viability. E14's readings agree with each other. That could be biology, or something unrecorded about the preparation, the cells or the assay. I kept it in, and I report results with and without it."

"Third, cost barely separates the historical blends, EUR 172 to 181 per litre, but the cost ceiling still rules out half the candidate recipes. FBS is three quarters of the supplemented-media cost and I could only find a snippet price for it, and I couldn't find an AR5 price at all. So I ran nine price scenarios. Real FBS and AR5 quotes are the most important missing inputs."

## 3:00 to 4:30. Model choice, and the result that keeps me honest

**Screen.** `reports/figures/06_loo_parity.png`, then the forward-round table in `reports/model_comparison.md`.

"I compared a GP, a random forest, the classical Scheffe mixture model and a plain average. On all 24 points no model clearly beats the average. In leave-one-out the GP ranks blends better than chance, with a rank correlation of 0.61. Scheffe does not. I chose the GP because it gives a usable uncertainty-based selection rule."

"Then the honest test. Train on earlier rounds, predict the next. Every model missed round 3 by 22 to 29 points, and the GP's forward rank correlations were 0.26, minus 0.31 and 0.26. So neither its predictions nor its rankings are validated prospectively. I use it to propose a diverse batch. The decision rests on the same-plate comparison with E19 and on confirmation before anything is adopted."

## 4:30 to 6:00. How the four picks were chosen

**Screen.** `reports/figures/08_next_batch.png`, then `reports/figures/07_policy_simulation.png`.

"I pick one slot at a time. After each pick, the model treats that blend as pending. That shrinks uncertainty around it, so the exploring slots look elsewhere, and a 5% volume gap keeps the picks apart. Slot 1 is the highest prediction. Slot 2 is the best blend at least 2.5% cheaper, and it has almost no serum-free medium. Slot 3 is the blend whose result would most shrink the model's uncertainty across the recipes that could still be the best. It moves DMEM down to 37% to test whether the round-3 band is really special. Slot 4 has the biggest expected gain once the other three are pending. It swaps AR5 for X-VIVO 15."

"Why not just pick the top four predictions? In a simulation with 30 paired campaigns, always picking the current best was no better than random, and was worse on one of the two synthetic truths. Our four-role package beat random in 19 to 23 of 30 seeds in every setting. It also has stricter eligibility rules, so I credit the package, not role mixing alone. And the score is the best blend sampled, which is discovery, not picking a confirmed winner."

## 6:00 to 7:15. What could make me wrong

**Screen.** The robustness and threshold tables in `reports/batch_selection.md`.

"I reran the whole selection 15 times, changing the noise model, the kernel limits, the two low results, the prices, and whether the anchor counts as pending. Slot 1 is unchanged in 9 of 15, but moves 26% of volume under a different noise model. Slot 4 moves by a median 7%. So these are recurring directions, not uniquely established recipes. Slot 2 moves with prices. Slot 3 moves with the model, which is expected, because exploration follows uncertainty."

"The biggest caveat: the fitted model is close to two-dimensional. It treats RPMI-10 and AR5 as interchangeable. So slot 1's 54% chance of beating E19 means the model can't tell them apart, not that slot 1 is better. All four picks hold less AR5 than E19, so this batch tests that assumption directly."

## 7:15 to 8:00. What happens after the plate

**Screen.** Memo, "How the result changes the next decision" table.

"If the E19 re-run lands near 80%, the round-3 region holds and we push further from AR5. If it lands near 55%, we investigate reproducibility before the next round, and judge everything against 55, not 81. First the assay owner checks the plate is valid, against criteria set in advance; an invalid plate is repeated. Then the screen: a blend passes if it is no more than 5 points below the same-plate E19, at equal or lower cost. Four wells give about plus or minus 11 points on that difference, so the screen only filters. One finalist goes to a paired confirmation against E19 across independent cell and medium preparations, sized from the variance the pilot measures. Accept if the lower bound on the difference clears minus 5 points. For Qorium, the same loop runs on bovine fibroblast expansion and collagen output, with real supplier quotes and a cheap and an expensive assay paired, which the schema already supports."

## Likely questions

| Question | Short answer |
|---|---|
| Why trust a GP that missed round 3 by 27 points? | I don't trust it to forecast, and its forward rankings were weak too. I use it to propose a diverse batch. The decision rests on the same-plate E19 comparison and on confirmation |
| What does "54% better than E19" mean? | Under the model, slot 1 and E19 are 0.98 correlated, so 0.54 is a coin flip. That is why E19 is on the plate |
| Did the simulation validate these four blends? | No. It compared policies on smooth synthetic truths. It says mixing roles beats pure exploitation |
| Why exclude near-duplicates when a replicate might be worth more? | The E19 anchor is the replicate. Four wells give within-plate repeatability; independent preparations come in the confirmation run |
| Why 20 or 45 wells for confirmation? | I don't fix a number yet. With the historical SD, 20 per arm gives only 51% power for a 5-point margin and about 45 gives 80%. The real size comes from the preparation-level variance this pilot measures |
| Does slot 2 help Qorium? | Not directly. It drops the serum-free media but raises FBS to 9.9%. Qorium's process is animal-product-free, so its candidate list would exclude FBS from the start |
| Why not BoTorch? | 24 points and four components. scikit-learn's GP with explicit conditioning is enough and easier to check, and `check_gp.py` verifies it |
| What changes with 10 to 20 prior experiments? | More space-filling picks and wider intervals. With 6 random points, the GP here was confidently wrong |
| How would this work at Qorium? | Same loop, Qorium's cells and assays. Pair a cheap screen with an expensive confirmatory assay, keep cost as a constraint with real quotes, and re-run an anchor every batch |
