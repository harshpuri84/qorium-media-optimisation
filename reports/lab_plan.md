# Lab plan: from recommendation to a plate a scientist can run

The memo gives the decision. This page gives what the bench needs, what I could not specify from the public data, and what the same loop would look like on Qorium's process. Anything marked **SOP** has to come from the assay owner; I have not invented it.

## 1. The next PBMC plate

| Item | Plan | Source |
|---|---|---|
| Formulations | Two DMEM steps (40%, 50%), a cheaper blend, an AR5-to-X-VIVO blend, and the E19 re-run; volumes in `outputs/plate_formulations.csv` | `select_batch.py` |
| Wells | 11 per formulation, 55 in total, in randomised row blocks: five interior rows carry two wells of every formulation, one row carries one of each plus the controls | `outputs/plate_layout.csv` |
| Edge | Outer ring (36 wells) filled with PBS against evaporation | layout |
| Assay controls | 2 no-cell blanks for background, 2 heat-killed PBMC wells to set the AOPI dead-cell gate | layout |
| Cells | One donor, one thaw, one rest period for all 57 cell-containing wells, so the E19 comparison is not confounded by donor or thaw | design rule |
| Lots | FBS lot, basal media lots and serum-free media lots logged per medium preparation. FBS is the largest source of lot-to-lot variation in these media | `COMPONENT_LOT` in `docs/SCHEMA.md` |
| Seeding density, well volume, rest time after thaw | **SOP**, copied from the source study's methods | not in the public workbook |
| Readout | Viability % **and** total and viable cells per mL from the same AOPI read, plus a t = 0 count from the seeded suspension. Viability alone can stay high while cells are lost |
| Harvest | One harvest procedure for every well, defined in the SOP: what is collected, how it is mixed, and the volume read | `outputs/results_template.csv` |
| Medium checks | pH after equilibration in the incubator, and osmolality, for each blend. DMEM carries more bicarbonate than RPMI, so blends differ in pH under 5% CO2. DMEM share also moves glucose (4.5 against 2 g/L) and calcium (1.8 against 0.4 mM), so this plate cannot say which of them drives a DMEM effect | results template |
| Pooling | The source study pooled cultures before reading. Reading single wells needs enough events per well; the assay owner confirms this, or wells are pooled and the replicate count changes | **SOP** |
| Options if capacity allows | A no-cell blank per blend, to correct for medium autofluorescence (10 wells per formulation instead of 11). A second donor as a block, to show the ranking is not one donor's | option |
| Supply | 11 wells per arm assumes enough cells from one donor and enough of each medium; if not, cut wells evenly across arms and widen the screen accordingly | assumption |

## 2. Plate validity, set before the run

The assay owner sets the numbers; these are the checks I would ask for.

| Check | Fails if |
|---|---|
| Missing wells | More than 2 of 11 wells lost for any formulation |
| Dead-cell control | Gate does not separate the heat-killed wells from live wells |
| Blank background | Event count in blanks above an agreed level |
| Spread within a formulation | Within-formulation SD far above the historical 9.51 points |
| Preparation records | Any deviation in medium preparation or cell handling not logged |

A failed check makes the plate inconclusive: investigate, then repeat the same five formulations. A low E19 anchor alone triggers a review of preparation and assay conditions; it does not prove a historical batch effect.

## 3. Screen and confirm

| Step | Rule |
|---|---|
| Screen | A blend passes if its mean is no more than 5 points below the same-plate E19, at equal or lower cost. With 11 wells per arm the 90% interval on the difference is about plus or minus 7 points (t, 20 degrees of freedom) |
| How often a blend passes | Truly equal to E19: 89%. 5 points worse: 50%. 10 points worse: 11%. 15 points worse: under 1%. All four comparisons share one E19 estimate, so their errors are correlated |
| What a pass means | "Not excluded". A lead needs a mean above E19 by more than the interval |
| Independent repeats | This plate estimates variation within one cell and one medium preparation. Before sizing confirmation, repeat the finalist and E19 on independent preparations to estimate preparation-to-preparation variance |
| Confirm | One finalist, two at most. Paired comparison against concurrent E19, blocked by independent preparations on different days. Accept if the one-sided 95% lower bound on the difference stays above minus 5 points, with acceptable cost and quality |
| Size of the confirmation | Set from the measured preparation-level variance. For scale only: at SD 9.51 between independent units, 20 per arm gives 51% power and about 45 per arm gives 80% |

## 4. What would change for Qorium

The recipes do not transfer. Qorium grows bovine skin fibroblasts in bioreactors with its own medium, and states that no animal products are used beyond the cells. The workflow transfers; the domain constraints, model assumptions and decision rules have to be rebuilt.

| PBMC case study | Qorium version |
|---|---|
| Suspension immune cells, viability at 72 h | Adherent bovine fibroblasts: attachment, growth to confluence and collagen deposition over weeks. Dead cells detach, so viability says little; growth rate and collagen are the endpoints |
| Four commercial media, two with 10% FBS | An approved animal-product-free ingredient list. That excludes FBS and also animal-derived insulin, transferrin, albumin and trypsin. Human dermal fibroblasts grow well serum-free and commercial fibroblast serum-free media exist; for bovine skin fibroblasts that is an expectation to test. The published gap below serum controls is for primary bovine myoblasts (Kolkmann, Post et al. 2020). Attachment substrates and dissociation enzymes must also be animal-free |
| Mixture of four complete media on a simplex | Concentrations of 8 to 15 defined components in a box. The redundant-coordinate issue disappears, the kernel has more dimensions than this data could support, so it needs priors or a screening design first |
| One endpoint | A non-destructive growth readout during culture, and collagen at the end. Collagen needs a definition first: deposited or secreted, per culture or per cell (for example hydroxyproline or Sirius Red), plus material-quality acceptance. Destructive assays need sister wells, which costs capacity |
| Cost per litre against E19 | Medium cost per gram of acceptable collagen or per square metre of sheet, with quality constraints |
| One medium | Two media phases: expansion, then collagen production. Collagen needs ascorbate and 2 to 4 weeks. Phenotype and passage number are recorded, because fibroblasts drift with passage |
| A round takes days | A round takes weeks. Each round must carry more information, which argues for replication and designed contrasts over more formulations |

**What changes in the code:** the candidate generator (box constraints instead of a simplex), the kernel inputs and priors, the cost denominator, the endpoints and their noise models, and the decision rules. The pending-point conditioning, anchor, validity gate and screen-then-confirm logic carry over.

**A first Qorium plate in the same pattern:** two designed steps on the component the team believes matters most, two model picks within an approved animal-free list, the current production medium as the anchor, replicated wells, a growth readout mid-culture and collagen at the end.

## 5. Questions I would ask the CSO

1. Which endpoint decides a medium change: growth rate, collagen per cell, sheet properties, or cost per square metre?
2. What loss in that endpoint is acceptable for what saving, and who signs it off?
3. Which ingredients are already ruled in or out, for regulatory, supply or performance reasons?
4. How large is the gap between plate results and bioreactor results, and is there a scale-down model to calibrate against?
5. How much variation do you see between cell batches and biopsies, and is it recorded?

*Sources.* Narayanan et al. (2025), Nat. Commun. 16, 6055. Kolkmann AM, Post MJ et al. (2020), "Serum-free media for the growth of primary bovine myoblasts", Cytotechnology 72(1), 111-120. Qorium process description, qorium.com, accessed 3 October 2026.
