"""Select the next four blends: one slot per role, chosen in sequence with pending-point conditioning.

Slots: 1 exploit (highest posterior mean), 2 cheaper alternative, 3 explore (largest integrated
posterior-variance reduction over recipes that could still be the best), 4 expected improvement over
the incumbent posterior mean once slots 1 to 3 are pending. Eligibility: base cost rule, the cost rule
in at least MIN_SCENARIOS_OK of 9 price scenarios, 1% dispensing steps, and a minimum volume gap from
every historical recipe, from the single-media controls (an operational exclusion, see DECISIONS.md)
and from each other. The plate holds five formulations: these four plus a re-run of E19.
"""
import csv
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import norm

from compare_models import GP, LOW_IDS, ei
from design_space import COMPONENTS, REFERENCE_ID, base_prices, blend_cost, ceiling, load_data, \
    scenario_prices, simplex_grid

ROOT = Path(__file__).resolve().parents[1]
SEED = 20261002
Z80 = norm.ppf(0.9)
SINGLE_MEDIA = np.eye(4)
REPLICATES = 4
DEFAULTS = dict(cheap_discount=0.025, min_gap_pct=5.0, min_scenarios_ok=6, exclude_single_media=True)
CHUNK = 2000
ROLES = [
    ('Exploit', 'highest posterior mean viability'),
    ('Cheaper alternative', 'highest posterior mean at least {cheap_discount:.1%} below the cost ceiling'),
    ('Explore', 'largest integrated posterior-variance reduction over recipes that could still be the best'),
    ('Expected improvement', 'highest expected improvement over the incumbent posterior mean, slots 1 to 3 pending'),
]


def gap_pct(A, B):
    """Share of total volume that must move to turn one recipe into the other."""
    return 50 * np.abs(A[:, None, :] - B[None, :, :]).sum(-1)


def variance_reduction(model, cand, mask):
    """Explore score: total posterior-variance reduction over the plausible-optimum region (eligible recipes
    whose mean + 2 sd reaches the incumbent posterior mean) from measuring one recipe in that region."""
    mu, sd = model.latent(cand)
    region = np.flatnonzero(mask & (mu + 2 * sd >= model.best_mean()))
    if not len(region):
        region = np.flatnonzero(mask)
    noise = model.noise_new * model.ys ** 2
    score = np.full(len(cand), -np.inf)
    for i in range(0, len(region), CHUNK):
        a = region[i:i + CHUNK]
        C = model.latent_cov(cand[a], cand[region])
        score[a] = (C ** 2).sum(1) / (sd[a] ** 2 + noise)
    return score


def eligible(X, cand, prices, opts):
    cost = blend_cost(cand, prices)
    cap = ceiling(prices)
    tested = np.vstack([X, SINGLE_MEDIA]) if opts['exclude_single_media'] else X
    robust = sum(blend_cost(cand, p) <= ceiling(p) + 1e-9 for p in scenario_prices().values()) >= opts['min_scenarios_ok']
    ok = (cost <= cap + 1e-9) & robust & (gap_pct(cand, tested).min(1) >= opts['min_gap_pct'])
    return ok, ok & (cost <= cap * (1 - opts['cheap_discount']))


def select(model, X, cand, prices, anchor=None, **overrides):
    """anchor: recipe re-run on the same plate; conditioned on as pending before any slot is chosen."""
    opts = {**DEFAULTS, **overrides}
    ok, cheap = eligible(X, cand, prices, opts)
    masks = [ok, cheap, ok, ok]
    cur, picks = model, []
    if anchor is not None:
        cur = cur.fantasize(np.atleast_2d(anchor))
    for (role, _), mask in zip(ROLES, masks):
        if picks:
            mask = mask & (gap_pct(cand, cand[picks]).min(1) >= opts['min_gap_pct'])
        if not mask.any():
            raise ValueError(f'No eligible candidate for slot "{role}" with settings {opts}')
        mu, sd = cur.latent(cand)
        if role == 'Explore':
            s = variance_reduction(cur, cand, mask)
        elif role == 'Expected improvement':
            s = np.where(mask, ei(mu, sd, cur.best_mean()), -np.inf)
        else:
            s = np.where(mask, mu, -np.inf)
        k = int(np.argmax(s))
        picks.append(k)
        cur = cur.fantasize(cand[[k]])
    return picks


def p_beats(model, P, ref):
    """P(true viability of each pick > true viability of the reference), from the joint latent posterior."""
    A = np.vstack([P, ref])
    mu, _ = model.latent(A)
    C = model.latent_cov(A)
    d_mu = mu[:-1] - mu[-1]
    d_var = np.diag(C)[:-1] + C[-1, -1] - 2 * C[:-1, -1]
    return 1 - norm.cdf(-d_mu / np.sqrt(np.maximum(d_var, 1e-12)))


def to_tenths(f):
    """Round fractions to 0.1 mL per 100 mL, largest remainder, so volumes sum to exactly 100.0."""
    t = np.asarray(f) * 1000
    base = np.floor(t)
    base[np.argsort(-(t - base))[:int(round(1000 - base.sum()))]] += 1
    return base / 10


def recipe(f):
    return '/'.join(str(int(round(x * 100))) for x in f)


def write(path, rows):
    with path.open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    ids, _, X, y, sem = load_data()
    cand = simplex_grid(1)
    prices = base_prices()
    model = GP('pooled', restarts=10).fit(X, y, sem)
    picks = select(model, X, cand, prices)
    P = cand[picks]
    ref = X[ids.index(REFERENCE_ID)]

    mu, sd = model.latent(P)
    obs_sd = np.sqrt(sd ** 2 + model.noise_new * model.ys ** 2)
    ref_mu = float(model.latent(ref[None])[0][0])
    pb = p_beats(model, P, ref)
    scen = scenario_prices()
    scen_costs = np.array([blend_cost(P, p) for p in scen.values()])
    scen_ok = np.array([blend_cost(P, p) <= ceiling(p) + 1e-9 for p in scen.values()])
    gaps = gap_pct(P, X)

    # Alternative fits: (model, X used for eligibility) for prediction checks and full reruns.
    def drop(i):
        k = np.array([d != i for d in ids])
        return GP('pooled', restarts=10).fit(X[k], y[k], sem[k]), X[k]
    variants = {
        'gp_sem_noise': (GP('sem', restarts=10).fit(X, y, sem), X),
        'gp_ls_floor_0.05': (GP('pooled', restarts=10, ls_floor=0.05).fit(X, y, sem), X),
        'gp_ls_floor_0.2': (GP('pooled', restarts=10, ls_floor=0.2).fit(X, y, sem), X),
        'gp_ls_upper_3': (GP('pooled', restarts=10, ls_upper=3.0).fit(X, y, sem), X),
        'gp_without_e02': drop(LOW_IDS[0]),
        'gp_without_e14': drop(LOW_IDS[1]),
    }
    var_mu = {k: m.latent(P)[0] for k, (m, _) in variants.items()}

    reruns = {k: cand[select(m, Xv, cand, prices)] for k, (m, Xv) in variants.items()}
    reruns['anchor_pending'] = cand[select(model, X, cand, prices, anchor=ref)]
    for name, p in scen.items():
        if name != 'fbs_x1.0_ar5_x1.0':  # identical to base prices
            reruns[f'price_{name}'] = cand[select(model, X, cand, p)]
    shift = {k: np.diag(gap_pct(P, R)) for k, R in reruns.items()}

    # Threshold stress: change one selection rule at a time.
    stress_settings = {'cheap_discount_0%': dict(cheap_discount=0.0), 'cheap_discount_5%': dict(cheap_discount=0.05),
                       'min_gap_3%': dict(min_gap_pct=3.0), 'min_gap_8%': dict(min_gap_pct=8.0),
                       'min_scenarios_5_of_9': dict(min_scenarios_ok=5), 'min_scenarios_7_of_9': dict(min_scenarios_ok=7),
                       'single_media_allowed': dict(exclude_single_media=False)}
    stress = {k: cand[select(model, X, cand, prices, **v)] for k, v in stress_settings.items()}

    rows = []
    for i, (role, rule) in enumerate(ROLES):
        j = int(np.argmin(gaps[i]))
        rows.append(dict(
            slot=i + 1, role=role, selection_rule=rule.format(**DEFAULTS),
            **{f'{c}_pct': int(round(P[i, n] * 100)) for n, c in enumerate(COMPONENTS)},
            **{f'{c}_ml_per_100ml': v for c, v in zip(COMPONENTS, to_tenths(P[i]))},
            cost_eur_per_litre_base=round(float(blend_cost(P[i], prices)), 2),
            cost_eur_per_litre_min=round(float(scen_costs[:, i].min()), 2),
            cost_eur_per_litre_max=round(float(scen_costs[:, i].max()), 2),
            within_ceiling_scenarios=f'{int(scen_ok[:, i].sum())}/{len(scen)}',
            predicted_viability_pct=round(float(mu[i]), 1),
            latent_sd_pct_points=round(float(sd[i]), 1),
            measured_mean_80pct_low=round(float(mu[i] - Z80 * obs_sd[i]), 1),
            measured_mean_80pct_high=round(float(mu[i] + Z80 * obs_sd[i]), 1),
            prob_true_viability_above_e19=round(float(pb[i]), 2),
            **{f'predicted_{k}': round(float(v[i]), 1) for k, v in var_mu.items()},
            nearest_historical=ids[j], nearest_gap_pct=round(float(gaps[i, j]), 1),
            nearest_observed_viability_pct=round(float(y[j]), 1),
            reruns_unchanged=f'{sum(v[i] == 0 for v in shift.values())}/{len(shift)}',
            median_shift_pct_across_reruns=round(float(np.median([v[i] for v in shift.values()])), 1),
            max_shift_pct_across_reruns=round(float(np.max([v[i] for v in shift.values()])), 1),
        ))
    write(ROOT / 'outputs/next_experiments.csv', rows)

    plate = [dict(position=f'slot {r["slot"]}', role=r['role'],
                  **{f'{c}_ml_per_100ml': r[f'{c}_ml_per_100ml'] for c in COMPONENTS}) for r in rows]
    plate.append(dict(position='anchor', role=f'{REFERENCE_ID} re-run (historical 81.0%)',
                      **{f'{c}_ml_per_100ml': v for c, v in zip(COMPONENTS, to_tenths(ref))}))
    write(ROOT / 'outputs/plate_formulations.csv', plate)

    # Plate map: REPLICATES independent wells per formulation, randomised over interior wells of a 96-well
    # plate (rows B-G, columns 2-11) to avoid edge effects. Replicate count is an assumption, see DECISIONS.md.
    interior = [f'{r}{c}' for r in 'BCDEFG' for c in range(2, 12)]
    wells = np.random.default_rng(SEED).choice(interior, len(plate) * REPLICATES, replace=False)
    layout = [dict(well=w, position=plate[i // REPLICATES]['position'], role=plate[i // REPLICATES]['role'],
                   replicate=i % REPLICATES + 1) for i, w in enumerate(wells)]
    write(ROOT / 'outputs/plate_layout.csv', sorted(layout, key=lambda r: (r['well'][0], int(r['well'][1:]))))

    write(ROOT / 'reports/tables/batch_stability.csv',
          [dict(variant=k, **{f'slot_{i + 1}_shift_pct': round(float(v[i]), 1) for i in range(4)},
                **{f'slot_{i + 1}_recipe': recipe(reruns[k][i]) for i in range(4)}) for k, v in shift.items()])
    write(ROOT / 'reports/tables/batch_threshold_stress.csv',
          [dict(setting=k, **{f'slot_{i + 1}_shift_pct': round(float(gap_pct(P[i:i + 1], R[i:i + 1])[0, 0]), 1) for i in range(4)},
                **{f'slot_{i + 1}_recipe': recipe(R[i]) for i in range(4)}) for k, R in stress.items()])

    fig, ax = plt.subplots(figsize=(6.5, 5))
    sc = ax.scatter(X[:, 0] * 100, X[:, 2] * 100, c=y, cmap='viridis', vmin=0, vmax=85, s=45, edgecolor='white')
    for i, (role, _) in enumerate(ROLES):
        ax.scatter(P[i, 0] * 100, P[i, 2] * 100, marker='*', s=320, color='#C15F3C', edgecolor='black', zorder=3)
        ax.annotate(f'{i + 1} {role}', (P[i, 0] * 100, P[i, 2] * 100), xytext=(8, 6), textcoords='offset points', fontsize=8)
    ax.scatter(ref[0] * 100, ref[2] * 100, s=160, facecolor='none', edgecolor='black', lw=1.5)
    ax.annotate('E19 (anchor re-run)', (ref[0] * 100, ref[2] * 100), xytext=(8, -12), textcoords='offset points', fontsize=8)
    ax.set_xlabel('DMEM %')
    ax.set_ylabel('X-VIVO 15 %')
    ax.set_title('Next batch (stars) against 24 historical blends; projection hides RPMI-10 and AR5', fontsize=9)
    fig.colorbar(sc, label='Observed mean viability %')
    fig.tight_layout()
    fig.savefig(ROOT / 'reports/figures/08_next_batch.png', dpi=160)

    print('kernel:', model.m.kernel_)
    print('noise sd on a recipe mean:', round(float(np.sqrt(model.noise_new) * model.ys), 2))
    print('incumbent posterior mean:', round(model.best_mean(), 1), '| E19 posterior mean:', round(ref_mu, 1),
          '| ceiling', round(ceiling(prices), 2))
    print('min gap between picks %:', round(float(gap_pct(P, P)[~np.eye(4, dtype=bool)].min()), 1))
    for r in rows:
        print(r)
    for k, v in shift.items():
        print(k, [round(float(x), 1) for x in v], [recipe(f) for f in reruns[k]])
    for k, R in stress.items():
        print('stress', k, [recipe(f) for f in R])


if __name__ == '__main__':
    main()
