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


def paired_wins():
    rows = read(ROOT / 'reports/tables/policy_simulation_summary.csv')
    policies = ['GP greedy (exploit only)', 'GP-EI (batch)', 'GP-UCB, kappa 2 (batch)', 'Four-role policy (deployed)']
    names = ['Exploit only', 'EI', 'UCB', 'Four-role (ours)']
    settings = [('GP fit to all 24', 'low (SEM 4.97)', 'GP truth, low noise', 'o'),
                ('GP fit to all 24', 'high (fitted 11.83)', 'GP truth, high noise', 's'),
                ('Scheffe fit to all 24', 'low (SEM 4.97)', 'Scheffe truth, low noise', '^'),
                ('Scheffe fit to all 24', 'high (fitted 11.83)', 'Scheffe truth, high noise', 'D')]
    fig, ax = plt.subplots(figsize=(3.4, 2.1))
    ax.axvspan(0, 15, color='#F4F2EC', zorder=0)
    ax.axvline(15, color=MUTED, lw=0.8, ls='--', zorder=1)
    ax.text(15.4, 3.62, 'coin flip', fontsize=6, color=MUTED, va='center')
    for j, (truth, noise, label, marker) in enumerate(settings):
        for i, pol in enumerate(policies):
            r = next(r for r in rows if r['truth'] == truth and r['noise'] == noise and r['policy'] == pol)
            wins = int(r['seeds_better_than_random'].split('/')[0])
            ax.scatter(wins, i + (j - 1.5) * 0.13, marker=marker, s=16, zorder=3,
                       color=ACCENT if pol.startswith('Four-role') else INK, label=label if i == 0 else None)
    ax.set_yticks(range(len(names)), names)
    ax.set_xlim(0, 30)
    ax.set_ylim(-0.5, 3.85)
    ax.set_xlabel('Seeds (of 30) where the policy beat random, paired')
    leg = ax.legend(fontsize=5.8, frameon=False, loc='lower right', handletextpad=0.2, borderaxespad=0.1)
    for h in leg.legend_handles:
        h.set_color(MUTED)
    fig.tight_layout(pad=0.3)
    fig.savefig(FIG / '10_memo_paired_wins.png', dpi=220)


if __name__ == '__main__':
    batch_map()
    paired_wins()
    print('wrote 09_memo_batch_map.png, 10_memo_paired_wins.png')
