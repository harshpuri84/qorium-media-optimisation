# Walkthrough script (8 minutes)

A screen share of the memo and repo. Each block lists what is on screen, then what to say. Times are cumulative. Speak to the decision, not the code.

## 0:00 to 0:45. The answer first

**Screen.** `reports/memo.pdf`, page 1.

"One line first. The data can't tell us which blend is best. They point to one signal, DMEM around 44%, and a model that is far more confident about that peak than it has earned. So I recommend a plate that tests the peak directly. Two blends step DMEM down to 40% and up to 50%, keeping E19's other ratios. Two blends come from the model: one cheaper, and one that swaps AR5 for X-VIVO 15. And E19 itself, the best historical blend, runs again on the same plate as the anchor. Eleven wells each, no more expensive than E19.

"I'm not a cell biologist. I used AI assistants for the code and drafts and as adversarial reviewers. My job was to frame the question, decide between options, and reject what didn't hold up. I'll show you where I did that."

## 0:45 to 2:00. What the data told me

**Screen.** Memo, "What the data says", then `reports/figures/01_viability_by_experiment.png`.

"Twenty-four blends of four commercial media, PBMC viability at 72 hours. Three things matter.

"First, round 3 beat everything at 73%, but all six round-3 blends sit at 44% DMEM. So a good recipe and a good lab day look the same. Partly answered, though: the same paper re-ran E19's recipe separately and got 80%.

"Second, DMEM is the only signal. Around 30% it scores 48, at 44% it scores 68 to 81, and from 60 to 77% it scores 43 to 56. The other three media vary widely inside round 3 and barely move the result.

"Third, E14. It is almost identical to E10 and scored 7.5% against 48. Its own readings agree, so I think it's a technical failure. I keep it in the fit, because dropping data by its outcome biases the model."

## 2:00 to 3:30. How far to trust the model

**Screen.** Memo, the forward-test figure.

"I compared a Gaussian process, a random forest, a classic mixture model and the plain average. On honest uncertainty, none beat the average. The GP's ranking looks decent at 0.61, but that is only it separating round 3 from the rest. Inside the earlier rounds it is 0.11.

"The real test: train on earlier rounds, predict the next. It missed round 3 by 27 points. So the model proposes and the plate decides.

"And the model's own settings tell me where it is overconfident. Its DMEM setting is at the limit I allowed, which means it believes in a sharp peak. Nobody has tested 40 or 50% at E19's ratios. That is exactly what slots 1 and 2 do."

## 3:30 to 5:00. Why this batch, and what I rejected

**Screen.** Memo batch map, then `reports/batch_selection.md`, "Batches considered".

"An earlier version used four model picks. Reviewers showed one of them was, to the model, the same as E19: correlation 0.98, predicted 70.2 against 70.1. A wasted well. I replaced it, and the exploration pick, with the two DMEM steps.

"Another reviewer proposed re-running E10 and E14 to explain their gap. I rejected that. E14 looks like a lab failure, so re-running it tells us about that day, not about the medium.

"The two model picks: slot 3 is the best blend at least 2.5% cheaper. It nearly drops the serum-free media, but it raises FBS, so it's no help for an animal-free process. Slot 4 moves volume from AR5 to X-VIVO 15. AR5 has no public price, so if that works, the least certain cost leaves the problem."

## 5:00 to 6:15. What could make me wrong

**Screen.** Memo, "How sure we are", with the pass-probability figure.

"I re-ran the selection 19 ways: different noise models, kernel limits, coordinates, without the odd results, and 8 price scenarios. The DMEM steps are fixed by design. Slot 4 holds except in two fits. Slot 3 moves with prices, which is expected for a cost pick.

"I also simulated 30 paired campaigns. At this noise level no selection policy beat random picks reliably, and the blend you'd pick from single noisy readings ended 5 to 8 points below the best. So the plate spends its idle wells on replicates. Eleven wells per arm shrink the uncertainty on each comparison from plus or minus 13 points to plus or minus 7."

## 6:15 to 8:00. From plate to decision, and Qorium

**Screen.** Memo, "From plate to decision", then `reports/lab_plan.md` section 4.

"Three steps. First, is the plate valid? The assay owner checks blanks, dead-cell controls and spread against rules set in advance. If it fails, we repeat it; we don't interpret it.

"Then the screen. A blend passes if it is within 5 points of the same-plate E19 at equal or lower cost. A pass means 'not excluded', not 'better'.

"Then confirmation, on independent cell and medium preparations, sized from what this plate teaches us about variation.

"For Qorium, the recipes don't transfer: your cells are adherent fibroblasts and the process is animal-free. What transfers is the loop: designed contrasts where the model is overconfident, an anchor every round, replicates, a validity gate, and cost per unit of collagen as the business test. My questions for you are which endpoint decides a medium change, and what loss is acceptable for what saving."

## Likely questions

| Question | Short answer |
|---|---|
| Why trust a GP that missed round 3 by 27 points? | I don't, as a forecast. I use it to propose candidates and to show me where it is overconfident. The DMEM steps test that overconfidence directly |
| Why designed points instead of the model's picks? | The simulation found no reliable advantage for any policy at this noise level, and the model's sharpest assumption is untested. A designed contrast answers a clear question whatever the model believes |
| What does P(above E19) = 0.39 mean? | Under the model, a 39% chance slot 4's true viability beats E19's. It ignores batch effects, which is why E19 is on the plate |
| Why 11 wells? | The plate had 36 idle interior wells. Eleven per arm cut the interval on each comparison from about 13 to about 7 points without adding formulations |
| Why is 50% DMEM allowed above the cost ceiling? | It is EUR 0.26/L over, smaller than the uncertainty in the FBS price. I allowed designed points 1% over; model picks must stay under |
| Why exclude the reviewer's E10 and E14 re-runs? | E14's readings agree closely with each other, which points to a failed run. Re-running it would test the lab on that day, not the medium |
| If you had one more plate, run this or fix the noise first? | Run this. The anchor and 11 wells per arm are the noise measurement |
| How would you build the team around this loop? | Start with a modeller-engineer and a lab-data owner embedded with R&D. The first deliverable is the schema and a frozen dataset per round. The assay owner holds the veto on plate validity |
| Why believe a Bayesian method helps at all? | It hasn't yet beaten the mean, and the memo says so. Its value today is structure: an explicit uncertainty rule, an anchor and pass criteria set in advance. It earns trust when forward rounds beat the mean |

## Questions from a cell biologist

| Question | Short answer |
|---|---|
| Which donor and which thaw? | The historical data do not record them. This plate uses one donor and one thaw for every well; donor effects belong in the confirmation run |
| Why viability and not cell count? | It is the only endpoint in the public data. This plate also records total and viable cells per mL from the same read |
| How do you know 81% is real and not debris? | I don't. The plate adds heat-killed controls to set the dead-cell gate, and blanks for background |
| Does a PBMC blend tell you anything about bovine fibroblasts? | Only the method. Fibroblasts are adherent and among the easier cells to grow serum-free. Your 2020 work showed the gap for bovine myoblasts; for fibroblasts I'd expect the open question to be collagen output per cell, not growth |
| What would your first Qorium plate look like? | Two designed steps on the component your team thinks matters most, two model picks within an approved animal-free list, your production medium as anchor, replicated wells, a growth readout during culture and collagen at the end |
| What changes in your code for Qorium? | The candidate generator, the kernel inputs and priors, the cost denominator and the endpoints. The anchor, pending-point conditioning, validity gate and screen-then-confirm logic carry over |
