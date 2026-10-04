# Language review of the memo (GPT-6 Astra, 2026-10-04)

Codex, GPT-6-Astra medium, read-only, via Herdr. Reviewed commit 7801a12. Astra judged each suggestion in a ChatGPT language review (docs/review_language_chatgpt_2026-10-04.md) and added its own. Captured from the terminal, so tables keep their terminal layout.

```text
   Review    Checked HEAD 7801a12, the brief and relevant interval/distance
             code. Read-only; no files changed. Recommendations below are
             replacements or deletions, not additions.

   ChatGPT suggestion               1. Title, line 2
   Verdict and recommended wording  ACCEPT: “Recommended next batch for cost-
                                    aware media optimisation”
   Reason                           Shorter, measured and relevant to the brief;
                                    removes the conversational contrast.
  ──────────────────────────────────────────────────────────────────────────────
   ChatGPT suggestion               2. “Without having earned that confidence,”
                                    line 8
   Verdict and recommended wording  ACCEPT WITH EDIT: “whose confidence exceeds
                                    its predictive performance”
   Reason                           ChatGPT’s replacement is longer and
                                    introduces “narrow optimum.” This shorter
                                    phrase preserves the criticism. Superseded
                                    by the opening below.
  ──────────────────────────────────────────────────────────────────────────────
   ChatGPT suggestion               3. “A test set before the run…,” line 8
   Verdict and recommended wording  ACCEPT WITH EDIT: “a prespecified contrast
                                    that may be inconclusive”
   Reason                           Shorter and clearer than both versions;
                                    avoids “explicitly recognised.” Superseded
                                    by the opening below.
  ──────────────────────────────────────────────────────────────────────────────
   ChatGPT suggestion               4. “A well the model priced at nothing,”
                                    line 30
   Verdict and recommended wording  ACCEPT WITH EDIT: Delete the entire review-
                                    history paragraph.
   Reason                           ChatGPT’s replacement is longer and adds
                                    “little additional information,” which is a
                                    different claim. Deletion also implements
                                    broader point 4.
  ──────────────────────────────────────────────────────────────────────────────
   ChatGPT suggestion               5. “Teaches the lab something,” line 34
   Verdict and recommended wording  ACCEPT WITH EDIT: Replace the final sentence
                                    with “I aim to test the DMEM response and
                                    identify candidates for confirmation.”
   Reason                           ChatGPT’s wording is longer and more
                                    abstract. This is shorter than the complete
                                    original sentence and uses first person.
  ──────────────────────────────────────────────────────────────────────────────
   ChatGPT suggestion               6. “Honest uncertainty,” line 61
   Verdict and recommended wording  ACCEPT WITH EDIT: “Across all 24
                                    formulations, the mean baseline has the
                                    lowest negative log predictive density
                                    (NLPD): 4.44 versus the GP’s 5.93.”
   Reason                           Replace the whole second sentence. The
                                    suggested fragment alone is longer; this
                                    version defines NLPD within a shorter
                                    complete sentence.
  ──────────────────────────────────────────────────────────────────────────────
   ChatGPT suggestion               7. “The forward test is the honest one,”
                                    line 61
   Verdict and recommended wording  ACCEPT WITH EDIT: “The forward test predicts
                                    the next round”
   Reason                           ChatGPT’s replacement is substantially
                                    longer. This retains the reason for using
                                    the test without implying other tests are
                                    dishonest.
  ──────────────────────────────────────────────────────────────────────────────
   ChatGPT suggestion               8. “The plate decides,” line 61
   Verdict and recommended wording  ACCEPT WITH EDIT: “I use GP recommendations
                                    to guide experimental comparisons.”
   Reason                           Shorter. ChatGPT’s version is longer;
                                    experiments inform a decision rather than
                                    making it themselves.
  ──────────────────────────────────────────────────────────────────────────────
   ChatGPT suggestion               9. “Makes all four readable,” line 81
   Verdict and recommended wording  ACCEPT WITH EDIT: Replace the whole sentence
                                    with “I compare all four candidates with
                                    concurrent E19.”
   Reason                           Shorter than the original sentence. ChatGPT
                                    quoted only a fragment; its proposed
                                    complete sentence is otherwise reasonable.
  ──────────────────────────────────────────────────────────────────────────────
   ChatGPT suggestion               10. “Buy the missing quote,” line 110
   Verdict and recommended wording  ACCEPT WITH EDIT: “prioritise the quote most
                                    likely to change the selection”
   Reason                           Same length as the original clause;
                                    ChatGPT’s version is longer. Quotes are
                                    obtained, not necessarily purchased.
  ──────────────────────────────────────────────────────────────────────────────
   ChatGPT suggestion               New opening, line 8
   Verdict and recommended wording  ACCEPT WITH EDIT: “I propose testing the
                                    possible optimum near 44% DMEM. The model’s
                                    forward predictions are unreliable. The next
                                    plate combines two designed contrasts, two
                                    model-selected formulations and an E19
                                    control, at approximately E19’s cost. The
                                    prespecified test may be inconclusive.”
   Reason                           ChatGPT’s opening is longer than the
                                    existing opening and duplicates line 12 and
                                    confirmation details. This replacement is
                                    shorter and retains the diagnostic purpose.

   Broader suggestion                  1. Consistent terminology
   Verdict and bounded implementation  ACCEPT WITH EDIT: Use formulation for a
                                       composition, candidate for a proposed
                                       formulation, slot for its table position
                                       and E19 control for the concurrent
                                       reference. Replace “Anchor” with
                                       “Control” in line 20.
   Reason                              Replacing every “blend,” “recipe” and
                                       “pick” mechanically makes prose and slot
                                       references cumbersome. Preserve
                                       distinctions rather than enforcing one
                                       noun.
  ──────────────────────────────────────────────────────────────────────────────
   Broader suggestion                  2. Units and volume distance
   Verdict and bounded implementation  ACCEPT WITH EDIT: Replace line 41’s value
                                       cell with “Model candidates: ≥5% volume
                                       reallocated versus tested formulations
                                       and each other; designed steps: 4.7% and
                                       5.3% versus E19; distance = ½Σ|
                                       Δpercentage|.” Use “percentage points” in
                                       shortened surrounding sentences.
   Reason                              The formula matches select_batch.py:59–
                                       61. Do not add a separate mathematical
                                       paragraph. Bare “% apart” is ambiguous;
                                       indiscriminate unit expansion costs
                                       space.
  ──────────────────────────────────────────────────────────────────────────────
   Broader suggestion                  3. Interval names and coverage
   Verdict and bounded implementation  ACCEPT WITH EDIT: Line 14: “Mean (80%
                                       predictive interval)”. Line 63: replace
                                       “matched the GP’s error and coverage
                                       (0.79)” with “had similar error; both
                                       intervals covered 79% of held-out means”.
   Reason                              Latent variance plus observation variance
                                       confirms predictive intervals
                                       (compare_models.py:119–122;
                                       select_batch.py:168–169). Replace the
                                       complete forest sentence and trim its
                                       ending to stay shorter. “Posterior
                                       predictive” is accurate but unnecessarily
                                       long in this column.
  ──────────────────────────────────────────────────────────────────────────────
   Broader suggestion                  4. Remove review history
   Verdict and bounded implementation  ACCEPT: Delete line 30.
   Reason                              The brief asks for rationale, not the
                                       revision narrative. Already counted
                                       above.
  ──────────────────────────────────────────────────────────────────────────────
   Broader suggestion                  5. Explain compressed phrases
   Verdict and bounded implementation  ACCEPT WITH EDIT: Line 63: replace “and
                                       pending picks can be conditioned on
                                       exactly, which makes batch selection
                                       simple” with “and I condition on pending
                                       outcomes at their predicted means”. Line
                                       116: replace “a box of defined components
                                       per phase” with “bounded component
                                       concentrations per phase”.
   Reason                              Both are shorter. ChatGPT’s “bounded
                                       concentration ranges…” is longer; the
                                       pending-outcome explanation must replace
                                       existing wording, not follow it.

   Careful sentence         Serum, line 26
   Verdict and replacement  ACCEPT WITH EDIT: Replace “with FBS held at 6.2 to
                            6.8% (E19 6.5%), so serum does not confound the
                            contrast” with “with FBS at 6.2–6.8% versus E19’s
                            6.5%; its contribution remains unresolved”.
   Reason                   Shorter. ChatGPT correctly rejects “does not
                            confound,” but “limiting its contribution” still
                            implies a demonstrated biological effect size.
  ──────────────────────────────────────────────────────────────────────────────
   Careful sentence         Success, line 119
   Verdict and replacement  ACCEPT WITH EDIT: “This batch is informative if the
                            curvature contrast and candidate screens guide the
                            next experiment, including when no candidate
                            advances.”
   Reason                   Shorter than the current sentence. ChatGPT’s
                            “interpretable contrast” could still exclude a
                            useful inconclusive result.

   Additional issue    Current text                  Proposed replacement
  ━━━━━━━━━━━━━━━━━━  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   memo.md:22          “sets the bar”                “sets the reference”
  ──────────────────  ────────────────────────────  ────────────────────────────
   :24                 “Picks (stars) against the    “Candidates (stars)
                       24 historical blends”         alongside 24 historical
                                                     formulations”
  ──────────────────  ────────────────────────────  ────────────────────────────
   :26                 “it believes viability        “it predicts sharp
                       changes sharply”              viability changes”
  ──────────────────  ────────────────────────────  ────────────────────────────
   :36                 “because a lab manager can    “because the cost limit is
                       check a constraint by         explicit and checkable”
                       hand”
  ──────────────────  ────────────────────────────  ────────────────────────────
   :52                 “So what”                     “Implication”
  ──────────────────  ────────────────────────────  ────────────────────────────
   :55                 “the anchor measures what     “E19 checks current
                       is left”                      reproducibility”
  ──────────────────  ────────────────────────────  ────────────────────────────
   :67                 “How sure we are”             “Uncertainty”
  ──────────────────  ────────────────────────────  ────────────────────────────
   :81                 “It exploits with two         “I select two model
                       model picks”                  candidates”
  ──────────────────  ────────────────────────────  ────────────────────────────
   :91                 “independent repeats come     “independent repeats
                       first and size the            determine the confirmation
                       confirmation”                 sample size”
  ──────────────────  ────────────────────────────  ────────────────────────────
   :109                “keeps the cheap-to-          “supports calibration
                       expensive link estimable”     between assays”

   Net length estimate                Recommendation
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Approximately 140 words shorter    Count the opening once, delete line 30
                                      once, and use selective terminology
                                      changes. All recommended edits can
                                      replace equal-length or longer passages;
                                      no additional section is needed.
```
