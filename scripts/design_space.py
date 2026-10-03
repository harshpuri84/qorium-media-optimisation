"""Cost rule and feasible candidate space for the four-media blend.

Cost rule: a candidate is feasible when its prepared-media cost per litre is no higher than
the reference blend PBMC-E19 (best observed mean viability) under the same price scenario.
Dispensing rule: every fraction is a multiple of STEP_PCT percent and fractions sum to 100%.
"""
import csv
from itertools import combinations
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
COMPONENTS = ['dmem', 'rpmi_10', 'xvivo', 'ar5']
LABELS = ['DMEM', 'RPMI-10', 'XVIVO', 'AR5']
REFERENCE_ID = 'PBMC-E19'
STEP_PCT = 1


def read_csv(path):
    with path.open(newline='') as handle:
        return list(csv.DictReader(handle))


def load_data():
    rows = read_csv(ROOT / 'data/processed/pbmc_analysis.csv')
    X = np.array([[float(r[f'{c}_fraction']) for c in COMPONENTS] for r in rows])
    y = np.array([float(r['viability_mean_pct']) for r in rows])
    sem = np.array([float(r['viability_sem_pct_points']) for r in rows])
    ids = [r['formulation_id'] for r in rows]
    rounds = np.array([int(r['round']) for r in rows])
    return ids, rounds, X, y, sem


def base_prices():
    rows = {r['component_id']: float(r['price_per_litre']) for r in read_csv(ROOT / 'data/inputs/component_costs.csv')}
    return np.array([rows[c] for c in COMPONENTS])


def scenario_prices():
    return {r['scenario']: np.array([float(r[f'{c}_eur_per_litre']) for c in COMPONENTS])
            for r in read_csv(ROOT / 'data/inputs/cost_scenarios.csv')}


def blend_cost(X, prices):
    return np.asarray(X) @ prices


def ceiling(prices):
    ids, _, X, _, _ = load_data()
    return float(blend_cost(X[ids.index(REFERENCE_ID)], prices))


def simplex_grid(step_pct=STEP_PCT):
    """All four-part compositions in step_pct increments (stars and bars)."""
    n = 100 // step_pct
    pts = []
    for bars in combinations(range(n + 3), 3):
        parts = np.diff((-1,) + bars + (n + 3,)) - 1
        pts.append(parts)
    return np.array(pts, dtype=float) / n


def feasible(X, prices):
    return blend_cost(X, prices) <= ceiling(prices) + 1e-9


def main():
    ids, _, X, y, _ = load_data()
    grid = simplex_grid()
    out = []
    for name, p in {'base': base_prices(), **scenario_prices()}.items():
        out.append(dict(scenario=name, ceiling_eur_per_litre=f'{ceiling(p):.2f}',
                        grid_points=len(grid), feasible_grid_share=f'{feasible(grid, p).mean():.3f}',
                        historical_feasible=int(feasible(X, p).sum()),
                        min_rpmi_share_on_feasible_grid=f'{grid[feasible(grid, p), 1].min():.2f}'))
    path = ROOT / 'reports/tables/cost_rule_feasibility.csv'
    with path.open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(out[0]))
        writer.writeheader()
        writer.writerows(out)
    for r in out:
        print(r)


if __name__ == '__main__':
    main()
