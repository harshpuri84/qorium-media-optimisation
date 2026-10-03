"""Reproducible descriptive analysis of PBMC media blends, without fitting models."""
import csv
import hashlib
import json
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data/processed'
FIGURES = ROOT / 'reports/figures'
TABLES = ROOT / 'reports/tables'
COMPONENTS = ['dmem', 'rpmi_10', 'xvivo', 'ar5']
LABELS = ['DMEM', 'RPMI-10', 'XVIVO', 'AR5']
ROUND_COLORS = ['#78909c', '#167d9a', '#d19a34', '#61459b']


def read(name):
    with (DATA / name).open(newline='') as handle:
        return list(csv.DictReader(handle))


def write(name, rows):
    with (TABLES / name).open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def corr(a, b):
    if np.std(a) < 1e-12 or np.std(b) < 1e-12:
        return None
    return float(np.corrcoef(a, b)[0, 1])


def save(fig, name):
    fig.savefig(FIGURES / f'{name}.png', dpi=180, facecolor='white', bbox_inches='tight')
    fig.savefig(FIGURES / f'{name}.pdf', facecolor='white', bbox_inches='tight')
    plt.close(fig)


def main():
    FIGURES.mkdir(parents=True, exist_ok=True)
    TABLES.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10,
                         'axes.spines.top': False, 'axes.spines.right': False,
                         'axes.titleweight': 'bold', 'axes.labelcolor': '#334155',
                         'text.color': '#172b3a', 'axes.edgecolor': '#b8c1ca',
                         'grid.color': '#e5e9ed'})
    records = read('pbmc_analysis.csv')
    measurements = read('pbmc_measurements.csv')
    ids = np.array([r['formulation_id'] for r in records])
    rounds = np.array([int(r['round']) for r in records])
    expts = np.array([int(r['experiment_number']) for r in records])
    x = np.array([[float(r[c + '_fraction']) for c in COMPONENTS] for r in records])
    y = np.array([float(r['viability_mean_pct']) for r in records])
    sd = np.array([float(r['viability_sd_pct_points']) for r in records])
    n = np.array([int(r['n_readings']) for r in records])
    assert len(ids) == len(set(ids)) == 24
    assert np.allclose(x.sum(axis=1), 1) and np.all(x >= 0)
    assert sum(n) == len(measurements) == 103
    by_id = {fid: [float(m['viability_pct']) for m in measurements if m['formulation_id'] == fid] for fid in ids}
    for i, fid in enumerate(ids):
        assert len(by_id[fid]) == n[i]
        assert np.isclose(np.mean(by_id[fid]), y[i])
        assert np.isclose(np.std(by_id[fid], ddof=1), sd[i])

    pairs = []
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            pairs.append({'formulation_a': str(ids[i]), 'formulation_b': str(ids[j]),
                          'round_a': int(rounds[i]), 'round_b': int(rounds[j]),
                          'euclidean_distance_fraction': float(np.linalg.norm(x[i] - x[j])),
                          'volume_reallocated_pct': float(np.abs(x[i] - x[j]).sum() * 50),
                          'mean_a_pct': float(y[i]), 'mean_b_pct': float(y[j]),
                          'absolute_mean_gap_pct_points': float(abs(y[i] - y[j]))})
    pairs.sort(key=lambda p: p['euclidean_distance_fraction'])
    write('recipe_pair_distances.csv', pairs)
    nearest = []
    for i, fid in enumerate(ids):
        distance = np.linalg.norm(x - x[i], axis=1)
        distance[i] = np.inf
        j = int(np.argmin(distance))
        nearest.append({'formulation_id': str(fid), 'nearest_formulation': str(ids[j]),
                        'distance_fraction': float(distance[j]),
                        'volume_reallocated_pct': float(np.abs(x[i] - x[j]).sum() * 50),
                        'absolute_mean_gap_pct_points': float(abs(y[i] - y[j]))})
    write('nearest_neighbours.csv', nearest)

    centered_x, centered_y = x.copy(), y.copy()
    for r in np.unique(rounds):
        mask = rounds == r
        centered_x[mask] -= x[mask].mean(axis=0)
        centered_y[mask] -= y[mask].mean()
    low = y < 10  # Descriptive sensitivity only; all experiments remain in analysis.
    correlations = [{'component': label,
                     'pearson_all_experiments': corr(x[:, j], y),
                     'pearson_after_round_centering': corr(centered_x[:, j], centered_y),
                     'pearson_excluding_means_below_10_pct': corr(x[~low, j], y[~low])}
                    for j, label in enumerate(LABELS)]
    write('component_associations.csv', correlations)
    component_summary = [{'component': label, 'min_volume_pct': float(x[:, j].min()*100),
                          'max_volume_pct': float(x[:, j].max()*100),
                          'round_3_min_pct': float(x[rounds == 3, j].min()*100),
                          'round_3_max_pct': float(x[rounds == 3, j].max()*100)}
                         for j, label in enumerate(LABELS)]
    write('mixture_coverage.csv', component_summary)
    ranked = sorted(records, key=lambda r: float(r['viability_mean_pct']), reverse=True)
    write('observed_formulations_ranked.csv', ranked)

    # Outcome history: show every available reading, plus means and descriptive SD.
    fig, ax = plt.subplots(figsize=(12, 5.5))
    for i, fid in enumerate(ids):
        readings = by_id[fid]
        offsets = np.linspace(-0.12, 0.12, len(readings))
        ax.scatter(expts[i] + offsets, readings, s=18, alpha=.4,
                   color=ROUND_COLORS[rounds[i]], zorder=2)
        ax.errorbar(expts[i], y[i], yerr=sd[i], fmt='o', color=ROUND_COLORS[rounds[i]],
                    markersize=5, capsize=3, linewidth=1.2, zorder=3)
    for boundary in [6.5, 12.5, 18.5]:
        ax.axvline(boundary, color='#cbd5df', linestyle='--', linewidth=1)
    for r in range(4):
        ax.text(3.5 + r*6, 101, f'Round {r}', ha='center', color=ROUND_COLORS[r], weight='bold')
    ax.set(xticks=expts, xlim=(.5, 24.5), ylim=(0, 106), xlabel='Historical experiment number',
           ylabel='Viability at 72 hours (%)', title='Viability rises in the final round, after the mixture search narrows')
    ax.grid(axis='y', alpha=.7)
    fig.text(.08, .01, 'Faint dots: reported readings. Solid dots and bars: mean ± sample SD, not confidence intervals.', fontsize=9)
    fig.tight_layout(rect=(0, .04, 1, 1))
    save(fig, '01_viability_by_experiment')

    fig, (left, right) = plt.subplots(1, 2, figsize=(12, 5), gridspec_kw={'width_ratios': [1.5, 1]})
    for r in range(4):
        mask = rounds == r
        left.scatter(y[mask], sd[mask], s=25 + 12*n[mask], color=ROUND_COLORS[r], alpha=.85, label=f'Round {r}')
    for fid in ['PBMC-E02', 'PBMC-E14', 'PBMC-E19', 'PBMC-E20', 'PBMC-E23']:
        i = int(np.flatnonzero(ids == fid)[0])
        left.annotate(fid.replace('PBMC-', ''), (y[i], sd[i]), xytext=(4, 4), textcoords='offset points', fontsize=9)
    left.set(xlabel='Mean viability (%)', ylabel='Sample SD (percentage points)', title='Reported-reading variability differs across recipes')
    left.legend(frameon=False, fontsize=9)
    left.grid(alpha=.6)
    counts = [(int(k), int((n == k).sum())) for k in sorted(set(n))]
    right.bar([k for k, _ in counts], [v for _, v in counts], color='#167d9a', width=.65)
    for k, v in counts:
        right.text(k, v+.15, str(v), ha='center')
    right.set(xticks=[k for k, _ in counts], xlabel='Reported readings per formulation',
              ylabel='Number of formulations', title='Reading counts are uneven')
    fig.text(.08, .01, 'Marker size increases with reading count. Donor and pool identities are unknown; SD does not isolate assay noise.', fontsize=9)
    fig.tight_layout(rect=(0, .05, 1, 1))
    save(fig, '02_reading_variability')

    fig, (ax, side) = plt.subplots(1, 2, figsize=(11, 10), gridspec_kw={'width_ratios': [4, 1.25]})
    positions = np.arange(24)
    starts = np.zeros(24)
    media_colors = ['#1d667a', '#54a5a7', '#d3a145', '#8a75a7']
    for j, label in enumerate(LABELS):
        ax.barh(positions, x[:, j]*100, left=starts, color=media_colors[j], label=label, height=.75)
        starts += x[:, j]*100
    ax.set(yticks=positions, yticklabels=[f'E{e:02d} · R{r}' for e, r in zip(expts, rounds)],
           xlabel='Volume share of prepared medium (%)', xlim=(0, 100), title='Mixtures tested across the four historical rounds')
    ax.invert_yaxis()
    ax.legend(loc='upper center', bbox_to_anchor=(.5, 1.06), ncol=4, frameon=False)
    side.barh(positions, y, color=[ROUND_COLORS[r] for r in rounds], height=.75)
    for i, value in enumerate(y):
        side.text(value+1, i, f'{value:.1f}', va='center', fontsize=8)
    side.set(yticks=positions, yticklabels=[], xlim=(0, 102), xlabel='Mean viability (%)', title='Outcome')
    side.invert_yaxis()
    for a in [ax, side]:
        for boundary in [5.5, 11.5, 17.5]:
            a.axhline(boundary, color='#b8c1ca', linewidth=.8)
    fig.text(.08, .01, 'Fractions are normalised only to correct published rounding. E = experiment; R = historical round.', fontsize=9)
    fig.tight_layout(rect=(0, .03, 1, 1))
    save(fig, '03_mixture_compositions')

    fig, axes = plt.subplots(2, 3, figsize=(12, 8), layout='constrained')
    norm = Normalize(0, 100)
    for ax, (a, b) in zip(axes.ravel(), [(0,1), (0,2), (0,3), (1,2), (1,3), (2,3)]):
        for r, marker in enumerate(['o', 's', '^', 'D']):
            mask = rounds == r
            ax.scatter(x[mask, a]*100, x[mask, b]*100, c=y[mask], cmap='viridis', norm=norm,
                       marker=marker, s=62, edgecolors='white', linewidth=.5, label=f'Round {r}')
        ax.plot([0,100], [100,0], '--', color='#cbd5df', linewidth=1)
        ax.set(xlim=(-3, 103), ylim=(-3, 103), xlabel=f'{LABELS[a]} volume %', ylabel=f'{LABELS[b]} volume %')
        ax.grid(alpha=.4)
    axes[0,0].legend(frameon=False, fontsize=8, loc='upper right')
    fig.colorbar(ScalarMappable(norm=norm, cmap='viridis'), ax=axes, shrink=.7, label='Mean viability (%)')
    fig.suptitle('Coverage is sparse; final-round recipes concentrate near 44% DMEM', fontsize=14, weight='bold')
    save(fig, '04_pairwise_mixture_coverage')

    fig, axes = plt.subplots(1, 3, figsize=(12, 4.5))
    for ax, pair in zip(axes, pairs[:3]):
        for k, key in enumerate(['formulation_a', 'formulation_b']):
            fid = pair[key]
            i = int(np.flatnonzero(ids == fid)[0])
            readings = by_id[fid]
            ax.scatter(k + np.linspace(-.05, .05, len(readings)), readings, color=ROUND_COLORS[rounds[i]], alpha=.45, s=22)
            ax.errorbar(k, y[i], yerr=sd[i], fmt='o', color=ROUND_COLORS[rounds[i]], capsize=5)
        ax.set(xticks=[0,1], xticklabels=[f'{pair["formulation_a"].replace("PBMC-", "")} (R{pair["round_a"]})',
                                       f'{pair["formulation_b"].replace("PBMC-", "")} (R{pair["round_b"]})'],
               xlim=(-.5,1.5), ylim=(0,100), ylabel='Viability (%)',
               title=f'{pair["volume_reallocated_pct"]:.2f}% volume reallocated\n{pair["absolute_mean_gap_pct_points"]:.1f} pp mean gap')
        ax.grid(axis='y', alpha=.5)
    fig.suptitle('The three closest recipe pairs can have different observed outcomes', fontsize=14, weight='bold')
    fig.text(.08, .01, 'Distances use normalised fractions. Bars show sample SD. Differences may reflect response shape or unrecorded experimental factors.', fontsize=9)
    fig.tight_layout(rect=(0,.06,1,.93))
    save(fig, '05_nearest_recipe_pairs')

    pooled_sd = float(np.sqrt(np.sum((n-1)*sd**2) / np.sum(n-1)))
    stats = {'n_formulations': len(ids), 'n_readings': len(measurements),
             'mean_viability_min_pct': float(y.min()), 'mean_viability_max_pct': float(y.max()),
             'median_reading_sd_pct_points': float(np.median(sd)),
             'min_reading_sd_pct_points': float(sd.min()), 'max_reading_sd_pct_points': float(sd.max()),
             'pooled_within_formulation_sd_pct_points': pooled_sd,
             'n_means_below_10_pct': int(low.sum()), 'n_means_at_least_70_pct': int((y >= 70).sum()),
             'top_observed_ids': [r['formulation_id'] for r in ranked[:3]],
             'component_associations': correlations, 'nearest_three_pairs': pairs[:3],
             'source_analysis_sha256': hashlib.sha256((DATA/'pbmc_analysis.csv').read_bytes()).hexdigest(),
             'source_measurements_sha256': hashlib.sha256((DATA/'pbmc_measurements.csv').read_bytes()).hexdigest(),
             'assay_noise_isolated': False, 'cost_analysis_available': False,
             'numpy_version': np.__version__, 'matplotlib_version': matplotlib.__version__}
    (TABLES/'eda_summary.json').write_text(json.dumps(stats, indent=2) + '\n')
    dramatic = next(p for p in pairs if {p['formulation_a'], p['formulation_b']} == {'PBMC-E10', 'PBMC-E14'})
    dmem_final = x[rounds == 3, 0] * 100
    report = [
        '# Exploratory analysis of PBMC media blends', '',
        'The public dataset supports a small, noise-aware mixture optimisation demonstration. The final historical round contains the highest viability readings, but recipe choice and round are intertwined. Nearby recipes sometimes have markedly different outcomes. Use conservative modelling and a diverse next batch; do not infer individual ingredient effects from these plots.', '',
        '## Dataset and outcome', '',
        f'There are {len(ids)} unique mixtures and {len(measurements)} reported readings across four rounds of six formulations. Means range from {y.min():.2f}% to {y.max():.2f}% viability after 72 hours. Two formulations have means below 10%; all remain in the dataset. There are {int((y>=70).sum())} formulations at or above 70%, all from round 3. The 70% threshold is a descriptive reference, not an agreed optimisation constraint.', '',
        '![Viability by historical experiment](figures/01_viability_by_experiment.png)', '',
        'Round means are 39.98%, 50.65%, 42.29% and 72.65%. These describe adaptively selected recipes, not randomised evidence of a round effect. A random train/test split can give optimistic results because it mixes the tightly clustered final round into both sets.', '',
        '## Variation between readings', '',
        f'The median within-formulation sample SD is {np.median(sd):.2f} percentage points, with a range of {sd.min():.2f} to {sd.max():.2f}. A pooled within-formulation SD is {pooled_sd:.2f} percentage points. This describes reported-reading spread and does not isolate technical assay error. Counts range from two to five readings, and 17 reading slots are missing. E20 has only two readings despite having the second-highest mean.', '',
        '![Reading variability](figures/02_reading_variability.png)', '',
        'E19 has the highest mean (81.0%), followed by E20 (76.5%) and E23 (71.5%). Their sample SDs are 8.09, 14.85 and 17.02 percentage points. These point estimates do not establish a reliable ranking. Donor/pool identities and independence are unknown, so this analysis does not calculate significance tests or biological confidence intervals.', '',
        '## Mixture coverage', '',
        f'The four fractions sum to one, leaving three independent degrees of freedom. Final-round DMEM proportions lie between {dmem_final.min():.2f}% and {dmem_final.max():.2f}%. All final-round outcomes exceed 67%, but earlier mixtures with similar DMEM fractions differ in the other components. The pattern suggests a candidate region to investigate, not a stand-alone optimum for DMEM.', '',
        '![Mixture compositions](figures/03_mixture_compositions.png)', '',
        '![Pairwise mixture coverage](figures/04_pairwise_mixture_coverage.png)', '',
        'Only 24 points cover the mixture space. None is a pure-medium vertex in the training set. Pairwise plots are projections; they can hide differences in the other fractions. Low-outcome formulations E02 and E14 are not removed as outliers: their readings consistently support their low means, and their cause is unknown.', '',
        '## Nearby recipes and response consistency', '',
        f'E10 and E14 differ by reallocation of only {dramatic["volume_reallocated_pct"]:.2f}% of total medium volume, yet their observed mean viability differs by {dramatic["absolute_mean_gap_pct_points"]:.2f} percentage points (48.15% versus 7.52%). The discrepancy is large compared with each recipe\'s reported-reading spread. They belong to different historical rounds; nonlinear biology, preparation effects or unrecorded experimental conditions are possible explanations. The data cannot identify which explanation is correct.', '',
        '![Nearest recipe pairs](figures/05_nearest_recipe_pairs.png)', '',
        f'The closest pair is {pairs[0]["formulation_a"]}/{pairs[0]["formulation_b"]}, with {pairs[0]["volume_reallocated_pct"]:.2f}% volume reallocated and a {pairs[0]["absolute_mean_gap_pct_points"]:.1f} percentage-point mean difference. Do not collapse near-neighbour recipes into exact replicates or let a flexible model explain all discrepancies through very short length scales.', '',
        '## Descriptive component associations', '',
        '| Component | All experiments | After centring within each round | Excluding means below 10% |',
        '| --- | --- | --- | --- |',
        *[f'| {r["component"]} | {r["pearson_all_experiments"]:.2f} | {r["pearson_after_round_centering"]:.2f} | {r["pearson_excluding_means_below_10_pct"]:.2f} |' for r in correlations], '',
        'Entries are Pearson correlations, not independent ingredient effects. Mixture fractions are dependent, experiments were adaptively selected and there are only six recipes per round. Round centring is a descriptive sensitivity calculation, not a fitted causal adjustment. The below-10% exclusion is a sensitivity calculation only; the full dataset remains the modelling input.', '',
        '## Implications for the next modelling step', '',
        '- Use a conservative GP on the constrained mixture domain, with a simple regression sanity check and feasible random sampling baseline. Fit transformations within validation folds.',
        '- Compare pooled observation noise with recipe-specific noise proxies; repeat under larger noise assumptions. The stored variance-of-mean proxy assumes independent readings and may understate biological uncertainty.',
        '- Use leave-formulation-out diagnostics and forward-round evaluation. Report fold-specific errors and uncertainty coverage; the latter will be descriptive with this sample size. Group exact repeated formulations if future data introduce them.',
        '- Inspect predictive behaviour around E10/E14. Compare all-data results against a sensitivity fit withholding each low-outcome recipe in turn; never silently exclude them.',
        '- Evaluate candidate proximity to historical recipes and avoid an entire batch of nearly identical high-ranked blends. Include an informative candidate outside the final-round cluster.',
        '- Apply nonnegative fractions and the sum-to-one constraint during generation, then recheck recipes after dispensing-volume rounding.',
        '- This descriptive analysis ignores cost. Provisional catalogue-based prices and nine price scenarios are applied later, in `scripts/design_space.py` and `scripts/select_batch.py`.', '',
        '## Reproduction', '',
        'Run `python scripts/explore_data.py` after data preparation. Outputs are five PNG/PDF figures and descriptive CSV/JSON tables. The script checks that reading counts, means and SDs reconcile with the prepared dataset. It does not fit a model or recommend new experiments.', ''
    ]
    (ROOT/'reports/exploratory_analysis.md').write_text('\n'.join(report))
    print(json.dumps({k: stats[k] for k in ['n_formulations','n_readings','median_reading_sd_pct_points','pooled_within_formulation_sd_pct_points']}, indent=2))
    print('Wrote five figures, five CSV tables, summary JSON and exploratory report.')


if __name__ == '__main__':
    main()
