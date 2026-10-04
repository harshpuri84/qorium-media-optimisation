# Language review of the memo (ChatGPT, 2026-10-04)

Provided by the user. Reviewed commit 7801a12.

**The memo shows strong judgement, but the language needs a tightening pass before submission.** For this case study, the right voice is direct, precise, and measured. Your recommendation is clear; some wording is too conversational, while other passages compress too much technical detail.

The strongest parts are your explicit treatment of uncertainty, the same-plate control, and the distinction between screening and confirmation. Keep those. I would change the following wording:

| Current wording | Suggested wording |
|---|---|
| "test the DMEM peak, not just chase it" | "Recommended next batch for cost-aware media optimisation" |
| "a model that is confident about it without having earned that confidence" | "The model suggests a narrow optimum, but its predictive performance does not justify that level of confidence." |
| "with a test set before the run that is allowed to come back inconclusive" | "using a prespecified statistical contrast, with inconclusive results explicitly recognised" |
| "a well the model priced at nothing" | "a candidate with little predicted improvement or additional information relative to E19" |
| "The goal is a next experiment that teaches the lab something whatever the result" | "The next batch should reduce uncertainty about the response to DMEM concentration while identifying candidates for confirmation." |
| "no model beats the mean on honest uncertainty" | "No model improves on the mean baseline in negative log predictive density (NLPD)." |
| "The forward test is the honest one" | "The forward test more closely reflects the intended use: predicting a subsequent experimental round." |
| "So the GP proposes candidates and the plate decides." | "I therefore use the GP to propose candidates; experimental results determine which candidates advance." |
| "The anchor makes all four readable" | "The concurrent E19 control provides a common reference for evaluating all four candidates." |
| "buy the missing quote that moves the decision most" | "Prioritise obtaining the supplier quote that has the greatest effect on candidate selection." |

Replace the opening with:

> I recommend five formulations for the next batch: two DMEM contrasts around E19, two model-selected candidates, and a concurrent E19 control, with 11 randomised wells per formulation. Historical data suggest a possible local optimum near 44% DMEM, but the model substantially underpredicts the latest experimental round. The batch therefore tests that response directly and screens alternatives at approximately E19's cost. Candidates that pass screening would require confirmation across independent preparations.

Broader changes:
- Use consistent terminology. Prefer formulation over alternating between blend, recipe, and pick. Introduce E19 as the "concurrent control" and use that term consistently.
- Specify units. Use "percentage points" for viability differences and noise. Define what "5% of volume apart" means mathematically.
- Name intervals precisely. Replace "80% range" with the actual interval type, such as "80% posterior predictive interval". State what the reported coverage of 0.79 measures.
- Remove the review history. "What I changed after review" interrupts the recommendation.
- Reduce compressed technical phrases. "Pending picks can be conditioned on exactly" needs an explanation of what is assumed about their unobserved outcomes. "A box of defined components per phase" -> "bounded concentration ranges for defined components in each phase".

Two sentences need particular care:
1. "So serum does not confound the contrast." Too strong, FBS varies 6.2% to 6.8%. Prefer: "FBS remains approximately constant, limiting its contribution to the contrast."
2. "This batch succeeds if ... leaves at least one blend for confirmation." A useful experiment could exclude every candidate. Prefer: "The batch is informative if it yields an interpretable DMEM contrast and determines whether either model-selected candidate warrants confirmation."

The memo is already four pages, the brief's upper limit. Make changes through replacement and deletion.
