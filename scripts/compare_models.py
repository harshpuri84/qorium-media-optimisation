"""Compare surrogate models and experiment-selection policies on the PBMC blend data.

1. Leave-one-formulation-out (LOO) accuracy and interval coverage for four surrogates.
2. Forward-round check: train on earlier rounds, predict the next round.
3. Simulated campaigns: random vs GP-based batch policies on two synthetic "true" response surfaces.
"""
import copy
import csv
import warnings
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import norm, spearmanr
from sklearn.ensemble import RandomForestRegressor
from sklearn.exceptions import ConvergenceWarning
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import ConstantKernel, Matern, WhiteKernel
from sklearn.linear_model import BayesianRidge

from design_space import base_prices, feasible, load_data, simplex_grid

warnings.filterwarnings('ignore', category=ConvergenceWarning)
ROOT = Path(__file__).resolve().parents[1]
TABLES, FIGURES = ROOT / 'reports/tables', ROOT / 'reports/figures'
SEED = 20261002
Z80 = norm.ppf(0.9)
LOW_IDS = ['PBMC-E02', 'PBMC-E14']


# ---------- surrogates: fit(X, y, sem) then predict(X) -> (mean, sd of a new observed mean) ----------
class GP:
    """Matern 5/2 with per-component length scales floored at ls_floor (default 0.1).

    sklearn fits the hyperparameters once. Posteriors are then computed explicitly from the fitted
    latent kernel, the training-time y scaling and a per-point noise vector, so conditioning on
    pending (fantasy) points keeps the scaling and every historical noise term fixed.
    """

    def __init__(self, noise='pooled', restarts=3, ls_floor=0.1, ls_upper=10.0):
        self.noise, self.restarts, self.ls_floor, self.ls_upper = noise, restarts, ls_floor, ls_upper

    def fit(self, X, y, sem):
        kernel = ConstantKernel(1.0, (1e-2, 1e2)) * Matern([0.3] * 4, (self.ls_floor, self.ls_upper), nu=2.5)
        alpha = 1e-6
        if self.noise == 'pooled':
            kernel = kernel + WhiteKernel(0.1, (1e-3, 1.0))
        else:  # per-recipe SEM as known noise, in normalised units
            alpha = (sem / y.std()) ** 2 + 1e-6
        self.m = GaussianProcessRegressor(kernel, alpha=alpha, normalize_y=True,
                                          n_restarts_optimizer=self.restarts, random_state=SEED).fit(X, y)
        k = self.m.kernel_
        self.ym, self.ys = float(self.m._y_train_mean), float(self.m._y_train_std)
        if self.noise == 'pooled':
            self.kf = k.k1
            self.noise_new = k.k2.noise_level + 1e-6   # normalised noise variance of one new recipe mean
            noise_vec = np.full(len(y), self.noise_new)
        else:
            self.kf = k
            self.noise_new = float(np.mean(sem ** 2)) / self.ys ** 2 + 1e-6
            noise_vec = np.asarray(alpha, float)
        self._condition(X, (y - self.ym) / self.ys, noise_vec)
        return self

    def _condition(self, X, z, noise_vec):
        self.X, self.z, self.noise_vec = X, z, noise_vec
        self.L = np.linalg.cholesky(self.kf(X) + np.diag(noise_vec))
        self.w = np.linalg.solve(self.L.T, np.linalg.solve(self.L, z))

    def fantasize(self, Xf):
        """Copy conditioned on pending points whose results equal the current posterior mean."""
        new = copy.copy(self)
        zf = self.kf(Xf, self.X) @ self.w
        new._condition(np.vstack([self.X, Xf]), np.append(self.z, zf),
                       np.append(self.noise_vec, np.full(len(Xf), self.noise_new)))
        return new

    def latent_cov(self, A, B=None):
        """Posterior covariance of the underlying response between A and B, original units."""
        B = A if B is None else B
        Va = np.linalg.solve(self.L, self.kf(self.X, A))
        Vb = Va if B is A else np.linalg.solve(self.L, self.kf(self.X, B))
        return (self.kf(A, B) - Va.T @ Vb) * self.ys ** 2

    def latent(self, A):
        """Posterior mean and sd of the underlying response, without observation noise."""
        mu = self.ym + self.ys * (self.kf(A, self.X) @ self.w)
        V = np.linalg.solve(self.L, self.kf(self.X, A))
        var = np.maximum(self.kf.diag(A) - (V ** 2).sum(0), 1e-12) * self.ys ** 2
        return mu, np.sqrt(var)

    def predict(self, A):
        """Predictive mean and sd for a newly measured recipe mean."""
        mu, sd = self.latent(A)
        return mu, np.sqrt(sd ** 2 + self.noise_new * self.ys ** 2)

    def best_mean(self):
        """Incumbent: highest posterior mean at any measured or pending recipe."""
        return float(self.latent(self.X)[0].max())


def scheffe(X):
    """Scheffe quadratic mixture terms: x_i and x_i * x_j, no intercept."""
    cross = [X[:, i] * X[:, j] for i in range(4) for j in range(i + 1, 4)]
    return np.column_stack([X] + cross)


class Scheffe:
    def fit(self, X, y, sem):
        self.m = BayesianRidge(fit_intercept=False).fit(scheffe(X), y)
        return self

    def predict(self, X):
        return self.m.predict(scheffe(X), return_std=True)


class Forest:
    def fit(self, X, y, sem):
        self.m = RandomForestRegressor(500, min_samples_leaf=2, random_state=SEED).fit(X, y)
        return self

    def predict(self, X):
        per_tree = np.stack([t.predict(X) for t in self.m.estimators_])
        return per_tree.mean(0), per_tree.std(0) + 1e-9


class MeanOnly:
    def fit(self, X, y, sem):
        self.mu, self.sd = y.mean(), y.std(ddof=1)
        return self

    def predict(self, X):
        return np.full(len(X), self.mu), np.full(len(X), self.sd)


MODELS = {
    'GP, pooled noise': lambda: GP('pooled'),
    'GP, per-recipe SEM noise': lambda: GP('sem'),
    'Scheffe quadratic (Bayesian ridge)': Scheffe,
    'Random forest': Forest,
    'Mean only (baseline)': MeanOnly,
}


def scores(y, mu, sd, ranks=True):
    err = y - mu
    return dict(n=len(y), rmse=float(np.sqrt(np.mean(err ** 2))), mae=float(np.mean(np.abs(err))),
                bias=float(np.mean(err)),
                spearman=float(spearmanr(y, mu).statistic) if ranks and len(y) > 2 and np.std(mu) > 0 else float('nan'),
                coverage_80=float(np.mean(np.abs(err) <= Z80 * sd)),
                nlpd=float(np.mean(-norm.logpdf(y, mu, sd))))


def loo(ids, X, y, sem, train_mask):
    rows, preds = [], {}
    for name, make in MODELS.items():
        mu, sd = np.full(len(y), np.nan), np.full(len(y), np.nan)
        for i in range(len(y)):
            tr = train_mask.copy()
            tr[i] = False
            mu[i], sd[i] = (v[0] for v in make().fit(X[tr], y[tr], sem[tr]).predict(X[i:i + 1]))
        ev = train_mask
        preds[name] = (mu, sd)
        rows.append(dict(model=name, **{k: round(v, 3) if isinstance(v, float) else v
                                        for k, v in scores(y[ev], mu[ev], sd[ev], ranks=name != 'Mean only (baseline)').items()}))
    return rows, preds


def forward(rounds, X, y, sem):
    rows = []
    for name, make in MODELS.items():
        for r in range(3):
            tr, te = rounds <= r, rounds == r + 1
            mu, sd = make().fit(X[tr], y[tr], sem[tr]).predict(X[te])
            rows.append(dict(model=name, train_rounds=f'0-{r}', test_round=r + 1,
                             **{k: round(v, 3) if isinstance(v, float) else v for k, v in scores(y[te], mu, sd).items()},
                             mean_pred=round(float(mu.mean()), 2), mean_obs=round(float(y[te].mean()), 2)))
    return rows


# ---------- simulated campaigns ----------
def kriging_believer(gp, cand, q, acq):
    """Pick q points; after each pick, condition on a pending result equal to the posterior mean (hyperparameters fixed)."""
    picks, model = [], gp
    for _ in range(q):
        mu, sd = model.latent(cand)
        a = acq(mu, sd, model.best_mean())
        a[picks] = -np.inf
        k = int(np.argmax(a))
        picks.append(k)
        model = model.fantasize(cand[[k]])
    return picks


def ucb(mu, sd, best, kappa=2.0):
    return mu + kappa * sd


def greedy(mu, sd, best):
    return mu


def ei(mu, sd, best):
    """Expected improvement over the incumbent posterior mean (not the noisy observed maximum)."""
    z = (mu - best) / sd
    return (mu - best) * norm.cdf(z) + sd * norm.pdf(z)


def four_role(gp, cand, X):
    """The deployed policy from select_batch.py (imported here to avoid a circular import)."""
    from select_batch import select
    return select(gp, X, cand, base_prices())


POLICIES = {'Random (feasible)': None, 'GP greedy (exploit only)': greedy,
            'GP-UCB, kappa 2 (batch)': ucb, 'GP-EI (batch)': ei, 'Four-role policy (deployed)': four_role}


def campaign(truth, cand, noise_sd, rng, policy, init_idx, rounds=3, q=4):
    idx = list(init_idx)
    yobs = truth[idx] + rng.normal(0, noise_sd, len(idx))
    best = [truth[idx].max()]
    for _ in range(rounds):
        if POLICIES[policy] is None:
            pool = np.setdiff1d(np.arange(len(cand)), idx)
            new = list(rng.choice(pool, q, replace=False))
        else:
            gp = GP('pooled', restarts=1).fit(cand[idx], yobs, np.zeros(len(idx)))
            if POLICIES[policy] is four_role:
                new = list(four_role(gp, cand, cand[idx]))
            else:
                pool = np.setdiff1d(np.arange(len(cand)), idx)
                new = list(pool[kriging_believer(gp, cand[pool], q, POLICIES[policy])])
        idx += new
        yobs = np.append(yobs, truth[new] + rng.normal(0, noise_sd, q))
        best.append(truth[idx].max())
    return best


def simulate(X, y, sem, seeds=30):
    """Illustrative only: both synthetic truths are smooth fits to the same 24 points."""
    cand = simplex_grid(2)
    cand = cand[feasible(cand, base_prices())]
    gp_all = GP('pooled').fit(X, y, sem)
    noises = {'low (SEM 4.97)': float(np.sqrt(np.mean(sem ** 2))),
              'high (fitted 11.83)': float(np.sqrt(gp_all.noise_new) * gp_all.ys)}
    truths = {
        'GP fit to all 24': np.clip(gp_all.latent(cand)[0], 0, 100),
        'Scheffe fit to all 24': np.clip(Scheffe().fit(X, y, sem).predict(cand)[0], 0, 100),
    }
    rows = []
    for tname, truth in truths.items():
        for nname, noise_sd in noises.items():
            for s in range(seeds):
                init = np.random.default_rng(SEED + s).choice(len(cand), 6, replace=False)
                for pname in POLICIES:
                    best = campaign(truth, cand, noise_sd, np.random.default_rng(SEED + 1000 + s), pname, init)
                    for r, b in enumerate(best):
                        rows.append(dict(truth=tname, noise=nname, policy=pname, seed=s, round=r, experiments=6 + 4 * r,
                                         best_true_viability=round(float(b), 3),
                                         regret=round(float(truth.max() - b), 3), truth_max=round(float(truth.max()), 3)))
    return rows, noises, len(cand)


def write(name, rows):
    with (TABLES / name).open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    ids, rounds, X, y, sem = load_data()
    loo_rows, preds = [], None
    for label, dropped in [('all 24', []), ('without E02', LOW_IDS[:1]), ('without E14', LOW_IDS[1:]),
                           ('without E02, E14', LOW_IDS)]:
        rows, p = loo(ids, X, y, sem, np.array([i not in dropped for i in ids]))
        preds = preds or p
        loo_rows += [dict(training=label, **r) for r in rows]
    write('model_loo.csv', loo_rows)
    write('model_forward_round.csv', forward(rounds, X, y, sem))

    fig, axes = plt.subplots(1, 4, figsize=(15, 4), sharex=True, sharey=True)
    for ax, name in zip(axes, [list(MODELS)[i] for i in (0, 2, 3, 4)]):
        mu, sd = preds[name]
        low = np.isin(ids, LOW_IDS)
        ax.errorbar(y, mu, yerr=Z80 * sd, fmt='o', color='#262521', ecolor='#bdbab0', ms=4, alpha=.9)
        ax.plot(y[low], mu[low], 'o', color='#C15F3C', ms=6, label='E02, E14')
        ax.plot([0, 100], [0, 100], ls='--', color='#999', lw=1)
        ax.set_title(name + (' (tree spread, heuristic)' if name == 'Random forest' else ''), fontsize=10)
        ax.set_xlabel('Observed mean viability %')
    axes[0].set_ylabel('LOO prediction % (80% interval)')
    axes[0].legend(loc='upper left', fontsize=8)
    fig.tight_layout()
    fig.savefig(FIGURES / '06_loo_parity.png', dpi=160)

    sim, noises, ncand = simulate(X, y, sem)
    write('policy_simulation.csv', sim)
    final = {}
    for r in sim:
        if r['round'] == 3:
            final[(r['truth'], r['noise'], r['policy'], r['seed'])] = r['regret']
    summary = []
    for tname in ['GP fit to all 24', 'Scheffe fit to all 24']:
        for nname in noises:
            for pname in POLICIES:
                reg = np.array([final[(tname, nname, pname, s)] for s in range(30)])
                rnd = np.array([final[(tname, nname, 'Random (feasible)', s)] for s in range(30)])
                d = reg - rnd
                summary.append(dict(truth=tname, noise=nname, policy=pname,
                                    median_regret_18_runs=round(float(np.median(reg)), 2),
                                    q25=round(float(np.percentile(reg, 25)), 2), q75=round(float(np.percentile(reg, 75)), 2),
                                    median_paired_diff_vs_random=round(float(np.median(d)), 2),
                                    seeds_better_than_random=f'{int((d < 0).sum())}/30'))
    write('policy_simulation_summary.csv', summary)

    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    colors = ['#8a877d', '#5B7FA6', '#C15F3C', '#3F7D58', '#A3739B']
    for row, nname in enumerate(noises):
        for col, tname in enumerate(['GP fit to all 24', 'Scheffe fit to all 24']):
            ax = axes[row, col]
            for c, pname in zip(colors, POLICIES):
                sub = [r for r in sim if r['truth'] == tname and r['noise'] == nname and r['policy'] == pname]
                xs = sorted({r['experiments'] for r in sub})
                vals = [[r['regret'] for r in sub if r['experiments'] == e] for e in xs]
                ax.plot(xs, [np.median(v) for v in vals], marker='o', color=c, label=pname)
                ax.fill_between(xs, [np.percentile(v, 25) for v in vals], [np.percentile(v, 75) for v in vals],
                                color=c, alpha=.1)
            ax.set_title(f'Truth: {tname}; noise {nname}', fontsize=9)
            ax.set_xlabel('Experiments run (6 random, then batches of 4)')
            ax.set_ylabel('Regret (viability pts)')
    axes[0, 0].legend(fontsize=7)
    fig.suptitle('Illustrative policy simulation: smooth synthetic truths, 30 paired seeds', fontsize=10)
    fig.tight_layout()
    fig.savefig(FIGURES / '07_policy_simulation.png', dpi=160)

    print(f'simulation: {ncand} feasible candidates at 2% steps, noise sd {noises}')
    for r in loo_rows:
        print(r)
    for r in summary:
        print(r)


if __name__ == '__main__':
    main()
