# Lab plan: from recommendation to a plate a scientist can run

The memo gives the decision. This page gives what the bench needs, what I could not specify from the public data, and what the same loop would look like on Qorium's process. Anything marked **SOP** has to come from the assay owner; I have not invented it.

## 1. The next PBMC plate

| Item | Plan | Source |
|---|---|---|
| Formulations | 4 new blends plus the E19 re-run, volumes in `outputs/plate_formulations.csv` | `select_batch.py` |
| Wells | 4 per formulation, 20 in total, one in each of four column blocks so every formulation spans the plate | `outputs/plate_layout.csv` |
| Edge | Outer ring (36 wells) filled with PBS against evaporation | layout |
| Assay controls | 2 no-cell blanks for background, 2 heat-killed PBMC wells to set the AOPI dead-cell gate | layout |
| Cells | One donor, one thaw, one rest period for all 24 cell-containing wells, so the E19 comparison is not confounded by donor or thaw | design rule |
| Seeding density, well volume, rest time after thaw | **SOP**, copied from the source study's methods | not in the public workbook |
| Readout | Viability % **and** total and viable cells per mL from the same AOPI read. Viability alone can stay high while cells are lost | `outputs/results_template.csv` |
| Medium checks | pH and osmolality of each blend before dispensing. DMEM carries more bicarbonate than RPMI, so blends differ in pH under 5% CO2 | results template |
| Pooling | The source study pooled cultures before reading. Reading single wells needs enough events per well; the assay owner confirms this or the wells are pooled and the replicate claim changes | **SOP** |

## 2. Plate validity, set before the run

The assay owner sets the numbers; these are the checks I would ask for.

| Check | Fails if |
|---|---|
| Missing wells | More than 1 of 4 wells lost for any formulation |
| Dead-cell control | Gate does not separate the heat-killed wells from live wells |
| Blank background | Event count in blanks above an agreed level |
| Spread within a formulation | Within-formulation SD far above the historical 9.51 points |
| Preparation records | Any deviation in medium preparation or cell handling not logged |

A failed check makes the plate inconclusive: investigate, then repeat the same five formulations. A low E19 anchor alone triggers a review of preparation and assay conditions; it does not prove a historical batch effect.

## 3. Screen and confirm

| Step | Rule |
|---|---|
| Screen | A blend passes if its mean is no more than 5 points below the same-plate E19, at equal or lower cost. With 4 wells per arm, the 90% interval on the difference is about plus or minus 13 points (t with 6 degrees of freedom), so the screen filters; it does not decide |
| How often a blend passes the screen | Truly equal to E19: 77%. 5 points worse: 50%. 10 points worse: 23%. 15 points worse: 7%. All four comparisons share one E19 estimate, so their errors are correlated |
| Confirm | One finalist, two at most. Paired comparison against concurrent E19, blocked by independent cell and medium preparations on different days. Accept if the one-sided 95% lower bound on the difference stays above minus 5 points, with acceptable cost and quality |
| Size of the confirmation | Set from the preparation-level variance this plate and its repeats measure. For scale only: at SD 9.51 between independent units, 20 per arm gives 51% power and about 45 per arm gives 80% |

## 4. What would change for Qorium

The recipes do not transfer. Qorium grows bovine skin fibroblasts in bioreactors with its own medium, and states that no animal products are used beyond the cells. The method transfers, with these changes:

| PBMC case study | Qorium version |
|---|---|
| Suspension immune cells, viability at 72 h | Adherent bovine fibroblasts: attachment, spreading, growth to confluence and collagen deposition over days to weeks |
| Four commercial media, two with 10% FBS | An approved animal-product-free ingredient list. That excludes FBS and also animal-derived insulin, transferrin, albumin and trypsin. Serum-free work in this field reports growth below serum controls (Kolkmann, Post et al. 2020, Cytotechnology, on primary bovine myoblasts), so growth rate is the first constraint to check |
| Mixture of complete media | Concentrations of defined components (growth factors, attachment factors, lipids, recombinant proteins), usually a box-constrained design rather than a simplex |
| One endpoint | A cheap screen paired with an expensive confirmatory assay: for example a metabolic or DNA-content readout for growth, and hydroxyproline or Sirius Red for collagen |
| Cost per litre | Cost per unit of acceptable output: medium cost per gram of collagen or per square metre of sheet, with material-quality constraints |

**A first Qorium plate in the same pattern:** four blends of approved animal-free ingredients, one bovine fibroblast line, the current production medium as the anchor, four wells per arm, a growth readout at mid-culture and collagen at the end. The model and selection code stay the same; the candidate generator, cost model and endpoints change.

## 5. Questions I would ask the CSO

1. Which endpoint decides a medium change: growth rate, collagen yield per cell, sheet properties, or cost per square metre?
2. What loss in that endpoint is acceptable for what saving, and who signs it off?
3. Which ingredients are already ruled in or out, for regulatory, supply or performance reasons?
4. How large is the gap between plate results and bioreactor results, and is there a scale-down model to calibrate against?
5. How much variation do you see between cell batches and biopsies, and is it recorded?

*Sources.* Narayanan et al. (2025), Nat. Commun. 16, 6055. Kolkmann AM, Post MJ et al. (2020), "Serum-free media for the growth of primary bovine myoblasts", Cytotechnology 72(1), 111-120. Messmer et al. (2022), serum-free differentiation of bovine satellite cells, Nature Food. Qorium process description, qorium.com, accessed 3 October 2026.
