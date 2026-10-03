"""Build and execute notebooks/walkthrough.ipynb, a narrated tour of the results.

The notebook reads the outputs that run_all.sh writes and refits the main GP once, so it duplicates no
selection logic. Run: python scripts/build_notebook.py (needs nbformat, nbclient, ipykernel).
"""
from pathlib import Path

import nbformat as nbf
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'notebooks/walkthrough.ipynb'

md, code = nbf.v4.new_markdown_cell, nbf.v4.new_code_cell
cells = [
    md("""# Next media batch: a narrated walkthrough

This notebook follows the memo (`reports/memo.pdf`) in order and shows the evidence behind each step. It reads the tables and figures that `run_all.sh` writes, and refits the main Gaussian process (GP) once so you can see the model directly. All selection logic lives in `scripts/`.

**Question.** Which 3 to 5 media formulations should the lab run next, balancing viability, cost, uncertainty, noise, feasibility and batch size?

**Answer.** Four new blends of DMEM-10, RPMI-10, X-VIVO 15 and AR5, plus a same-plate re-run of the best historical blend, E19."""),
    code("""from pathlib import Path
import sys
import pandas as pd
from IPython.display import Image, display

ROOT = Path.cwd().parent if Path.cwd().name == 'notebooks' else Path.cwd()
sys.path.insert(0, str(ROOT / 'scripts'))
pd.set_option('display.width', 160, 'display.max_columns', 30)
fig = lambda name, width=720: display(Image(filename=str(ROOT / 'reports/figures' / name), width=width))"""),
    md("""## 1. The data

24 blends from Narayanan et al. (2025), run in four rounds of six, with viability at 72 hours. Fractions are volume shares that sum to 1."""),
    code("""data = pd.read_csv(ROOT / 'data/processed/pbmc_analysis.csv')
cols = ['formulation_id', 'round', 'dmem_fraction', 'rpmi_10_fraction', 'xvivo_fraction', 'ar5_fraction',
        'n_readings', 'viability_mean_pct', 'viability_sd_pct_points', 'blend_cost_per_litre']
data[cols].round(3)"""),
    md("""## 2. What the data says

Round 3 beat every earlier round, but all six round-3 blends sit at about 44% DMEM, so a recipe effect and a batch effect look the same. E10 and E14 are 2.6% of volume apart and 40.6 points apart in viability."""),
    code("""display(data.groupby('round')['viability_mean_pct'].agg(['count', 'mean', 'min', 'max']).round(2))
fig('01_viability_by_experiment.png')
fig('05_nearest_recipe_pairs.png')"""),
    md("""## 3. Cost

Prices are provisional (see `data/inputs/price_sources.csv`). The cost rule: a new blend may cost no more per litre than E19 under the same price scenario. Nine scenarios vary the two least certain prices, FBS and AR5."""),
    code("""display(pd.read_csv(ROOT / 'data/inputs/component_costs.csv')[['component_id', 'price_per_litre', 'currency', 'price_basis']])
pd.read_csv(ROOT / 'reports/tables/cost_rule_feasibility.csv')"""),
    md("""## 4. Model comparison

Leave-one-out on all 24 blends is the primary view. The forward-round test (train on earlier rounds, predict the next) is the honest one, and every model fails it on round 3."""),
    code("""loo = pd.read_csv(ROOT / 'reports/tables/model_loo.csv')
display(loo[loo.training == 'all 24'][['model', 'rmse', 'spearman', 'coverage_80', 'nlpd']])
fwd = pd.read_csv(ROOT / 'reports/tables/model_forward_round.csv')
display(fwd[['model', 'test_round', 'rmse', 'bias', 'spearman', 'coverage_80']])
fig('06_loo_parity.png', 900)"""),
    md("""## 5. The fitted GP

The main model, refitted here. Note the length scales: DMEM sits at its 0.1 floor and RPMI-10 and AR5 at the 10.0 ceiling, so the model treats RPMI-10 and AR5 as interchangeable. The batch tests that assumption."""),
    code("""import numpy as np
from compare_models import GP
from design_space import load_data
ids, rounds, X, y, sem = load_data()
gp = GP('pooled', restarts=10).fit(X, y, sem)
print('kernel:', gp.m.kernel_)
print('noise SD on a recipe mean:', round(float(np.sqrt(gp.noise_new) * gp.ys), 2), 'viability points')"""),
    md("""## 6. Policy simulation

30 paired campaigns against two smooth synthetic truths at two noise levels. Illustrative only: it compares policies, it does not validate the four blends."""),
    code("""pd.read_csv(ROOT / 'reports/tables/policy_simulation_summary.csv')"""),
    code("""fig('07_policy_simulation.png', 900)"""),
    md("""## 7. The recommendation

One slot per role, chosen in sequence. After each pick the GP conditions on a pending result, so the exploring slots look elsewhere."""),
    code("""rec = pd.read_csv(ROOT / 'outputs/next_experiments.csv')
display(rec[['slot', 'role', 'dmem_pct', 'rpmi_10_pct', 'xvivo_pct', 'ar5_pct', 'cost_eur_per_litre_base',
             'within_ceiling_scenarios', 'predicted_viability_pct', 'measured_mean_80pct_low',
             'measured_mean_80pct_high', 'prob_true_viability_above_e19']])
fig('08_next_batch.png', 600)"""),
    md("""## 8. How stable are the picks?

Each row reruns the full selection with one change. Cells are the volume (%) separating the rerun's pick from the main pick."""),
    code("""display(pd.read_csv(ROOT / 'reports/tables/batch_stability.csv').iloc[:, :5])
pd.read_csv(ROOT / 'reports/tables/batch_threshold_stress.csv').iloc[:, :5]"""),
    md("""## 9. The plate

Five formulations, four randomised wells each, interior wells only. The screen passes a blend that is no more than 5 points below the same-plate E19 at equal or lower cost. A pass goes to a confirmation run of about 20 wells per arm over at least two independent preparations."""),
    code("""display(pd.read_csv(ROOT / 'outputs/plate_formulations.csv'))
pd.read_csv(ROOT / 'outputs/plate_layout.csv').head(8)"""),
]

nb = nbf.v4.new_notebook(cells=cells, metadata={'kernelspec': {'name': 'python3', 'display_name': 'Python 3', 'language': 'python'}})
NotebookClient(nb, timeout=600, kernel_name='python3', resources={'metadata': {'path': str(ROOT / 'notebooks')}}).execute()
OUT.parent.mkdir(exist_ok=True)
nbf.write(nb, OUT)
print('wrote', OUT.relative_to(ROOT))
