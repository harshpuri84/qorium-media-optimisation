"""Two compact figures sized for the memo: the batch map and paired wins over random. Run after run_all.sh."""
import csv
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from design_space import REFERENCE_ID, load_data

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / 'reports/figures'
INK, MUTED, LINE, ACCENT = '#262521', '#6B6960', '#D5D3CC', '#C15F3C'
plt.rcParams.update({'font.family': 'sans-serif', 'font.sans-serif': ['Helvetica Neue', 'Arial'], 'font.size': 7,
                     'axes.edgecolor': LINE, 'axes.labelcolor': INK, 'xtick.color': MUTED, 'ytick.color': MUTED,
                     'axes.spines.top': False, 'axes.spines.right': False})


def read(path):
    with path.open(newline='') as handle:
        return list(csv.DictReader(handle))


def batch_map():
    ids, _, X, y, _ = load_data()
    picks = read(ROOT / 'outputs/next_experiments.csv')
    fig, ax = plt.subplots(figsize=(3.4, 2.7))
    sc = ax.scatter(X[:, 0] * 100, X[:, 2] * 100, c=y, cmap='viridis', vmin=0, vmax=85, s=18, edgecolor='white', lw=0.5)
    labels = {'Exploit': '1 Exploit', 'Cheaper alternative': '2 Cheaper', 'Explore': '3 Explore',
              'Expected improvement': '4 Exp. improvement'}
    offsets = {'Exploit': (-7, -10), 'Cheaper alternative': (6, 4), 'Explore': (-4, 7), 'Expected improvement': (6, 4)}
    for p in picks:
        x, z = float(p['dmem_pct']), float(p['xvivo_pct'])
        ax.scatter(x, z, marker='*', s=120, color=ACCENT, edgecolor=INK, lw=0.5, zorder=3)
        ax.annotate(labels[p['role']], (x, z), xytext=offsets[p['role']], textcoords='offset points', fontsize=6.5,
                    color=INK, ha='right' if p['role'] in ('Explore', 'Exploit') else 'left')
    ref = X[ids.index(REFERENCE_ID)]
    ax.scatter(ref[0] * 100, ref[2] * 100, s=60, facecolor='none', edgecolor=INK, lw=0.9, zorder=2)
    ax.annotate('E19 anchor (ring)', (ref[0] * 100, ref[2] * 100), xytext=(8, -2), textcoords='offset points', fontsize=6.5, color=MUTED)
    ax.set_xlabel('DMEM %')
    ax.set_ylabel('X-VIVO 15 %')
    cb = fig.colorbar(sc, ax=ax, fraction=0.05, pad=0.02)
    cb.set_label('Observed viability %', fontsize=6.5)
    cb.ax.tick_params(labelsize=6)
    cb.outline.set_edgecolor(LINE)
    fig.tight_layout(pad=0.3)
    fig.savefig(FIG / '09_memo_batch_map.png', dpi=220)


def finalist_regret():
    """Median true shortfall of the finalist the lab would pick (highest noisy observed mean), per policy and setting."""
    rows = read(ROOT / 'reports/tables/policy_simulation_summary.csv')
    policies = ['Random (feasible)', 'GP greedy (exploit only)', 'GP-UCB, kappa 2 (batch)', 'GP-EI (batch)',
                'Four-role policy (deployed)']
    names = ['Random', 'Exploit only', 'UCB', 'EI', 'Four-role (ours)']
    settings = [('GP fit to all 24', 'low', 'GP truth, noise 5', 'o', True),
                ('Scheffe fit to all 24', 'low', 'Scheffe truth, noise 5', '^', True),
                ('GP fit to all 24', 'high', 'GP truth, noise 12', 'o', False),
                ('Scheffe fit to all 24', 'high', 'Scheffe truth, noise 12', '^', False)]
    fig, ax = plt.subplots(figsize=(3.4, 2.5))
    for j, (truth, noise, label, marker, filled) in enumerate(settings):
        for i, pol in enumerate(policies):
            r = next((r for r in rows if r['truth'] == truth and r['noise'].startswith(noise) and r['policy'] == pol), None)
            if r is None:
                raise ValueError(f'No simulation summary row for {truth}, {noise}, {pol}')
            c = ACCENT if pol.startswith('Four-role') else INK
            ax.scatter(float(r['median_finalist_regret']), i + (j - 1.5) * 0.12, marker=marker, s=16, zorder=3,
                       facecolor=c if filled else 'white', edgecolor=c, lw=0.9, label=label if i == 0 else None)
    ax.set_yticks(range(len(names)), names)
    ax.set_xlim(0, 11)
    ax.set_ylim(-0.5, 4.5)
    ax.set_xlabel('Final pick: points below the best blend available (median)')
    leg = ax.legend(fontsize=5.6, frameon=False, loc='upper center', bbox_to_anchor=(0.42, -0.24), ncol=2,
                    handletextpad=0.2, columnspacing=1.0)
    for h in leg.legend_handles:
        h.set_edgecolor(MUTED)
        if h.get_facecolor()[0][0] < 0.99:
            h.set_facecolor(MUTED)
    fig.tight_layout(pad=0.3)
    fig.savefig(FIG / '10_memo_finalist_regret.png', dpi=220)


if __name__ == '__main__':
    batch_map()
    finalist_regret()
    print('wrote 09_memo_batch_map.png, 10_memo_finalist_regret.png')
