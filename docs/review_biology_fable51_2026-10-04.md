# Biology and science review of the final memo (Claude Fable 5.1, 2026-10-04)

Cursor agent, claude-fable-5-1-thinking-high, plan (read-only) mode, via Herdr, as a cell biologist. Reviewed commit a729478.

1. Is the biology right?

• memo.md:26 "DMEM is the only component with a clear
  signal." DMEM fraction is not a biological variable; it is
  a proxy for what differs between DMEM and RPMI: glucose
  (4.5 vs 2 g/L), calcium (1.8 vs 0.4 mM), bicarbonate (3.7
  vs 2.0 g/L, so DMEM runs alkaline under 5% CO2), osmolality
  (~335 vs ~290 mOsm) and amino acid profile. Corrected:
  "DMEM share is the only blend variable with a clear signal;
  it stands for glucose, calcium, buffering and osmolality,
  which this design cannot separate. Measured pH and
  osmolality of each blend are recorded as covariates for the
  next round." The lab plan notes the bicarbonate point
  (lab_plan.md:17); the memo never connects it to its own
  headline.
• memo.md:36 "Maximise mean PBMC viability at 72 hours."
  PBMCs are a mixed, mostly non-dividing population.
  Monocytes adhere to plastic within hours and leave the
  suspension; AOPI on sampled suspension reports viability
  of what remains, not of what was seeded. Corrected:
  "viability and viable-cell recovery of the suspension
  fraction at 72 h, against a t=0 count."
• memo.md:27, 101 "serum-free media" used as if a step toward
  animal-free. X-VIVO 15 contains human albumin, transferrin
  and recombinant insulin; it is serum-free, not chemically
  defined, and from a bovine-cell programme's standpoint
  still contains animal-derived protein. Corrected: "two
  serum-free but protein-containing media".
• memo.md:57 "E14 is most likely a technical failure." E10
  (round 1) and E14 (round 2) almost certainly used
  different donors and thaws. A uniformly low plate from a
  poor donor or thaw is biology of the preparation, not a
  pipetting error. Corrected: "most likely a preparation or
  donor effect, not a recipe effect".
• memo.md:116 "Fibroblasts are among the easier cells to
  grow serum-free." True for human dermal fibroblasts in
  defined media with FGF2 and insulin. For primary bovine
  skin fibroblasts the published record is thin, and
  adherent serum-free culture needs an attachment substrate
  (recombinant vitronectin or fibronectin, or synthetic
  coating) and a non-animal dissociation enzyme. The memo
  lists neither; lab_plan.md:53 lists trypsin only.
• memo.md:116 "The open question is collagen output per
  cell." Collagen deposition needs ascorbate-2-phosphate and
  typically TGF-β1, runs over 2 to 4 weeks, and yields
  underhydroxylated, non-deposited procollagen without
  ascorbate. Collagen per cell also ignores the phenotype
  that matters: myofibroblast conversion and senescence with
  passage, both medium-dependent. Corrected: "deposited
  collagen per culture under ascorbate, with phenotype and
  passage recorded".

2. Is the experiment biologically sound?

Mostly. The PBS ring, randomised row blocks, one donor and
thaw, heat-killed gate control, pH and osmolality checks and
lot logging are all right. A bench scientist would change:

• Add a t=0 read of seeding count and viability. Without it
  "viable cells per mL" at 72 h cannot be expressed as
  recovery.
• Define harvest. Suspension sample only, or EDTA/scrape to
  include adherent monocytes. Match the source protocol or
  the historical comparison breaks.
• Blank per blend, not two generic blanks. Debris and
  autofluorescence differ by medium; the one spare interior
  well plus repurposing gives this.
• Pre-equilibrate blends in the incubator and record pH
  after equilibration, not at mixing; the 40/50 DMEM
  contrast is partly a pH contrast.
• FBS fraction is well controlled across slots 1, 2, 4 and
  E19 (6.2 to 6.8%), which is good; slot 3 at 9.9% is the
  only serum shift. Say so, since it means the titration is
  not confounded by serum.
• Consider two donors, 5 and 6 wells each, instead of one
  donor at 11. Within-plate power drops a little; a result
  that holds in two donors is worth more than one donor at
  ±7 points, given every earlier round likely used a
  different donor.

3. Does the Qorium transfer hold?

Partly. Right: viability is near-meaningless for adherent
cells, endpoints are growth and collagen, rounds take weeks,
the problem is a box of defined components, the cost
denominator is per output. Missing or wrong:

• Two media, not one. A cultivated-leather process has an
  expansion phase and a matrix-production phase with
  different media and objectives (doublings per day versus
  collagen deposited per area). The memo and lab_plan.md:61
  optimise one medium.
• Attachment and dissociation reagents are part of the
  animal-free ingredient list and of cost; absent.
• Phenotype and passage as covariates and constraints
  (myofibroblast markers, senescence, population doublings);
  the schema marks passage "future".
• Collagen definition is deferred to the lab plan; the memo
  should name ascorbate dependence and the 2 to 4 week assay
  once.
• Bovine dermal fibroblasts serum-free is asserted, not
  evidenced; state it as an expectation to test.

4. Three CSO questions the memo cannot answer

1. "Is your DMEM peak glucose, calcium, pH or osmolality?"
   Honest answer: the data cannot separate them. This plate
   measures pH and osmolality for every blend; the next
   round adds a bicarbonate-matched or glucose-matched RPMI
   contrast.
2. "Viability of which cells?" Honest answer: of the
   suspension fraction read by AOPI; subset composition is
   unknown and the source paper handled it in a separate
   cytokine study. The Qorium analogue is phenotype drift,
   which needs a marker panel, not a viability number.
3. "What evidence is there that this loop works on a
   three-week adherent collagen assay at four rounds a
   year?" Honest answer: none yet. The PBMC case
   demonstrates the mechanics. At four rounds a year the
   first year is one designed screening round plus
   confirmation, and the value lies in the anchor, validity
   gate and replication discipline, not in the GP.

Verdict: biologically careful but not yet biologically
literate; fix the DMEM-as-proxy framing, add the t=0 read and
harvest definition, and name the two-phase media and
attachment reagents in the transfer section, then it holds.
