"""Compact figures sized for the memo. Run after run_all.sh.

09 batch map, 10 forward-round test, 11 plate map, 12 screen pass probability.
"""
import csv
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch
from scipy.stats import norm

from design_space import REFERENCE_ID, load_data

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / 'reports/figures'
INK, MUTED, LINE, ACCENT, SOFT = '#262521', '#6B6960', '#D5D3CC', '#C15F3C', '#F4F2EC'
ROLE_COLOURS = {'slot 1': '#C15F3C', 'slot 2': '#E29A7A', 'slot 3': '#5B7FA6', 'slot 4': '#3F7D58', 'anchor': '#262521'}
POOLED_SD = 9.51
plt.rcParams.update({'font.family': 'sans-serif', 'font.sans-serif': ['Helvetica Neue', 'Arial', 'DejaVu Sans'],
                     'font.size': 7, 'axes.edgecolor': LINE, 'axes.labelcolor': INK, 'xtick.color': MUTED,
                     'ytick.color': MUTED, 'axes.spines.top': False, 'axes.spines.right': False})


def read(path):
    with path.open(newline='') as handle:
        return list(csv.DictReader(handle))


def batch_map():
    ids, _, X, y, _ = load_data()
    picks = read(ROOT / 'outputs/next_experiments.csv')
    fig, ax = plt.subplots(figsize=(3.4, 2.7))
    sc = ax.scatter(X[:, 0] * 100, X[:, 2] * 100, c=y, cmap='viridis', vmin=0, vmax=85, s=18, edgecolor='white', lw=0.5)
    ref = X[ids.index(REFERENCE_ID)]
    titr = [p for p in picks if p['role'].startswith('DMEM titration')]
    xs = np.array([float(p['dmem_pct']) for p in titr] + [ref[0] * 100])
    zs = np.array([float(p['xvivo_pct']) for p in titr] + [ref[2] * 100])
    order = np.argsort(xs)
    ax.plot(xs[order], zs[order], color=ACCENT, lw=0.8, ls='--', zorder=2)
    short = {'DMEM titration, 40%': '1 DMEM 40%', 'DMEM titration, 50%': '2 DMEM 50%', 'Cheaper alternative': '3 Cheaper',
             'Expected improvement': '4 Exp. improvement'}
    offsets = {'DMEM titration, 40%': (-6, 5), 'DMEM titration, 50%': (6, 4), 'Cheaper alternative': (6, 4),
               'Expected improvement': (6, 4)}
    for p in picks:
        x, z = float(p['dmem_pct']), float(p['xvivo_pct'])
        ax.scatter(x, z, marker='*', s=110, color=ROLE_COLOURS[f'slot {p["slot"]}'], edgecolor=INK, lw=0.5, zorder=3)
        ax.annotate(short[p['role']], (x, z), xytext=offsets[p['role']], textcoords='offset points', fontsize=6.3,
                    color=INK, ha='right' if p['role'] == 'DMEM titration, 40%' else 'left')
    ax.scatter(ref[0] * 100, ref[2] * 100, s=55, facecolor='none', edgecolor=INK, lw=0.9, zorder=4)
    ax.annotate('E19 control', (ref[0] * 100, ref[2] * 100), xytext=(0, -13), textcoords='offset points', fontsize=6.3, color=MUTED, ha='center')
    ax.set_xlabel('DMEM %')
    ax.set_ylabel('X-VIVO 15 %')
    cb = fig.colorbar(sc, ax=ax, fraction=0.05, pad=0.02)
    cb.set_label('Observed viability %', fontsize=6.5)
    cb.ax.tick_params(labelsize=6)
    cb.outline.set_edgecolor(LINE)
    fig.tight_layout(pad=0.3)
    fig.savefig(FIG / '09_memo_batch_map.png', dpi=220)


def forward_test():
    gp = [r for r in read(ROOT / 'reports/tables/model_forward_round.csv') if r['model'] == 'GP, pooled noise']
    fig, ax = plt.subplots(figsize=(3.4, 1.9))
    for i, r in enumerate(gp):
        pred, obs = float(r['mean_pred']), float(r['mean_obs'])
        ax.plot([pred, obs], [i, i], color=LINE, lw=2.2, zorder=1, solid_capstyle='round')
        ax.scatter(pred, i, color='white', edgecolor=INK, s=30, zorder=3, lw=1)
        ax.scatter(obs, i, color=ACCENT if abs(obs - pred) > 15 else INK, s=30, zorder=3)
        ax.annotate(f'{obs - pred:+.1f}', ((pred + obs) / 2, i), xytext=(0, 5), textcoords='offset points',
                    ha='center', fontsize=6.3, color=MUTED)
    ax.set_yticks(range(len(gp)), [f'Train 0-{int(r["test_round"]) - 1}\npredict {r["test_round"]}' for r in gp])
    ax.set_xlim(30, 80)
    ax.set_ylim(-0.6, len(gp) - 0.3)
    ax.invert_yaxis()
    ax.set_xlabel('Next-round mean viability %  (open: predicted, filled: observed)')
    fig.tight_layout(pad=0.3)
    fig.savefig(FIG / '10_memo_forward_test.png', dpi=220)


def plate_map():
    layout = read(ROOT / 'outputs/plate_layout.csv')
    fig, ax = plt.subplots(figsize=(3.4, 2.6))
    rows = 'ABCDEFGH'
    ax.add_patch(FancyBboxPatch((0.25, 0.3), 12.5, 8.4, boxstyle='round,pad=0.05,rounding_size=0.4',
                                facecolor=SOFT, edgecolor=LINE, lw=0.8))
    for w in layout:
        r, c = rows.index(w['well'][0]), int(w['well'][1:])
        x, yv = c, 8 - r
        if w['well_type'] == 'PBS edge':
            ax.add_patch(Circle((x, yv), 0.36, facecolor='white', edgecolor=LINE, lw=0.6))
        elif w['well_type'] == 'control':
            ax.add_patch(Circle((x, yv), 0.36, facecolor='white', edgecolor=INK, lw=0.8, hatch='////'))
        else:
            ax.add_patch(Circle((x, yv), 0.36, facecolor=ROLE_COLOURS[w['position']], edgecolor='white', lw=0.4))
    for i, r in enumerate(rows):
        ax.text(0.45, 8 - i, r, ha='center', va='center', fontsize=5.5, color=MUTED)
    for c in range(1, 13):
        ax.text(c, 8.95, str(c), ha='center', va='center', fontsize=5.5, color=MUTED)
    labels = [('slot 1', 'DMEM 40%'), ('slot 2', 'DMEM 50%'), ('slot 3', 'Cheaper'), ('slot 4', 'Exp. improvement'),
              ('anchor', 'E19 control')]
    spots = [(1, -0.35), (4.4, -0.35), (7.8, -0.35), (1, -1.05), (4.4, -1.05)]
    for (k, lab), (x0, y0) in zip(labels, spots):
        ax.add_patch(Circle((x0, y0), 0.22, facecolor=ROLE_COLOURS[k], edgecolor='white'))
        ax.text(x0 + 0.35, y0, lab, va='center', fontsize=5.5, color=INK)
    ax.add_patch(Circle((7.8, -1.05), 0.22, facecolor='white', edgecolor=LINE, lw=0.6))
    ax.text(8.15, -1.05, 'PBS edge ring', va='center', fontsize=5.5, color=INK)
    ax.add_patch(Circle((1, -1.75), 0.22, facecolor='white', edgecolor=INK, hatch='////', lw=0.6))
    ax.text(1.35, -1.75, 'blanks and heat-killed controls', va='center', fontsize=5.5, color=INK)
    ax.set_xlim(0, 13)
    ax.set_ylim(-2.15, 9.3)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.tight_layout(pad=0.2)
    fig.savefig(FIG / '11_memo_plate_map.png', dpi=220)


def pass_probability():
    diff = np.linspace(-20, 10, 301)
    fig, ax = plt.subplots(figsize=(3.4, 1.95))
    for n, style, lab in [(4, '--', '4 wells per arm'), (11, '-', '11 wells per arm (this plate)')]:
        se = POOLED_SD * np.sqrt(2 / n)
        ax.plot(diff, norm.cdf((5 + diff) / se), ls=style, color=ACCENT if n == 11 else MUTED, lw=1.4, label=lab)
    ax.axvline(-5, color=LINE, lw=0.8)
    ax.text(-5.3, 0.04, '5-point margin', rotation=90, fontsize=5.8, color=MUTED, ha='right', va='bottom')
    ax.axvline(0, color=LINE, lw=0.8, ls=':')
    ax.set_xlabel('True difference from same-plate E19, viability points')
    ax.set_ylabel('P(blend passes screen)')
    ax.set_ylim(0, 1.02)
    ax.legend(fontsize=5.8, frameon=False, loc='upper left')
    fig.tight_layout(pad=0.3)
    fig.savefig(FIG / '12_memo_pass_probability.png', dpi=220)


if __name__ == '__main__':
    batch_map()
    forward_test()
    plate_map()
    pass_probability()
    for old in ['10_memo_finalist_regret.png', '10_memo_paired_wins.png']:
        (FIG / old).unlink(missing_ok=True)
    print('wrote 09_memo_batch_map, 10_memo_forward_test, 11_memo_plate_map, 12_memo_pass_probability')
