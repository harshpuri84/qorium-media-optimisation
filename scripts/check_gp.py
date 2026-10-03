"""Focused checks for the GP posterior and pending-point conditioning. Run: python scripts/check_gp.py"""
import numpy as np

from compare_models import GP
from design_space import load_data, simplex_grid


def main():
    ids, _, X, y, sem = load_data()
    cand = simplex_grid(5)
    rng = np.random.default_rng(0)

    for noise in ['pooled', 'sem']:
        gp = GP(noise, restarts=2).fit(X, y, sem)

        # 1. Explicit latent posterior matches sklearn after removing observation noise.
        mu_sk, sd_sk = gp.m.predict(cand, return_std=True)
        mu, sd = gp.latent(cand)
        assert np.allclose(mu, mu_sk, atol=1e-4), f'{noise}: mean mismatch {np.abs(mu - mu_sk).max()}'
        if noise == 'pooled':
            white = gp.m.kernel_.k2.noise_level * gp.ys ** 2
            assert np.allclose(sd ** 2 + white, sd_sk ** 2, rtol=1e-4), f'{noise}: variance mismatch'
        else:
            assert np.allclose(sd, sd_sk, rtol=1e-4), f'{noise}: variance mismatch'

        # 2. Historical noise and y scaling survive conditioning on pending points.
        Xf = cand[rng.choice(len(cand), 3, replace=False)]
        f = gp.fantasize(Xf)
        assert np.array_equal(f.noise_vec[:len(y)], gp.noise_vec), f'{noise}: historical noise changed'
        assert (f.ym, f.ys) == (gp.ym, gp.ys), f'{noise}: y scaling changed'
        assert np.allclose(f.noise_vec[len(y):], gp.noise_new), f'{noise}: pending-point noise wrong'

        # 3. Pending points leave the mean unchanged and never raise posterior variance.
        mu_f, sd_f = f.latent(cand)
        assert np.allclose(mu_f, mu, atol=1e-6), f'{noise}: fantasy moved the mean'
        assert np.all(sd_f <= sd + 1e-9), f'{noise}: variance increased'

        # 4. Sequential conditioning equals one-shot conditioning on the same pending points.
        g = gp
        for x in Xf:
            g = g.fantasize(x[None])
        assert np.allclose(g.latent(cand)[1], sd_f, atol=1e-8), f'{noise}: sequential != batch conditioning'

        # 5. Joint covariance diagonal agrees with marginal variance.
        assert np.allclose(np.diag(gp.latent_cov(cand[:50])), sd[:50] ** 2, rtol=1e-6), f'{noise}: covariance diag'
        print(f'{noise}: all checks passed')


if __name__ == '__main__':
    main()
