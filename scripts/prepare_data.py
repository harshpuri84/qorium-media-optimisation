"""Create traceable PBMC analysis tables without altering the source workbook."""
import csv
import hashlib
import json
import math
from pathlib import Path
import statistics

from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'data/raw/narayanan_2025/PBMC_Experiments.xlsx'
PROCESSED = ROOT / 'data/processed'
COMPONENTS = ['dmem', 'rpmi_10', 'xvivo', 'ar5']
SOURCE_COLUMNS = ['DMEM', 'RPMI-10', 'XVIVO', 'AR5']
ROUNDING_TOLERANCE_PCT_POINTS = 0.11
ARTICLE = 'https://www.nature.com/articles/s41467-025-61113-5'


def write_csv(path, rows, fields=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = fields or list(rows[0])
    with path.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def verify_source():
    manifest = json.loads((ROOT / 'data/raw/source_manifest.json').read_text())
    record = next(r for r in manifest['files'] if r['path'] == str(SOURCE.relative_to(ROOT)))
    if hashlib.sha256(SOURCE.read_bytes()).hexdigest() != record['sha256']:
        raise ValueError('PBMC source fingerprint changed. Resolve provenance before processing.')


def get_costs():
    path = ROOT / 'data/inputs/component_costs.csv'
    if not path.exists():
        labels = ['DMEM with FBS and Penicillin-Streptomycin per article methods',
                  'RPMI-10 with supplements per article methods',
                  'XVIVO 15 prepared per manufacturer instructions',
                  'AR5 prepared per manufacturer instructions']
        rows = [dict(component_id=c, prepared_medium_label=label, price_per_litre='',
                     currency='', price_basis='', price_source='', as_of_date='', notes='')
                for c, label in zip(COMPONENTS, labels)]
        write_csv(path, rows)
    with path.open(newline='') as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 4 or {r['component_id'] for r in rows} != set(COMPONENTS):
        raise ValueError('Expected exactly one price-input row per component.')
    prices = {}
    currencies = set()
    complete = True
    for row in rows:
        value = row['price_per_litre'].strip()
        if value:
            price = float(value)
            if not math.isfinite(price) or price < 0:
                raise ValueError('Prices must be finite and nonnegative.')
            prices[row['component_id']] = price
        else:
            complete = False
        currency = row['currency'].strip().upper()
        if currency:
            if len(currency) != 3 or not currency.isalpha():
                raise ValueError('Use a three-letter currency code.')
            currencies.add(currency)
        if not currency or not row['price_source'].strip() or row['price_basis'] not in {'observed', 'estimate', 'hypothetical'}:
            complete = False
    if len(currencies) > 1:
        raise ValueError('Convert all component prices into one documented currency first.')
    return prices if complete else None, next(iter(currencies)) if complete else ''


def main():
    verify_source()
    workbook = load_workbook(SOURCE, data_only=True)
    # Export all sheets positionally. Empty/duplicate headers and blank cells
    # stay intact, including the two-row cytokine header.
    for sheet in workbook:
        target = ROOT / 'data/interim' / f'pbmc_{sheet.title}.csv'
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('w', newline='', encoding='utf-8') as handle:
            csv.writer(handle).writerows(sheet.values)

    sheet = workbook['MediaBlendingStudies']
    rows = list(sheet.values)
    headers = list(rows[0])
    required = ['Expt #', 'Round', *SOURCE_COLUMNS, *[f'Via{i}' for i in range(1, 6)], 'Average Viability [%]']
    if any(headers.count(h) != 1 for h in required):
        raise ValueError('Unexpected media-blend schema.')
    formulations, measurements, analysis, issues = [], [], [], []

    def issue(severity, source_sheet, source_row, description, action):
        issues.append(dict(severity=severity, source_file=SOURCE.name,
                           source_sheet=source_sheet, source_row=source_row,
                           issue=description, action=action))

    prices, currency = get_costs()
    for row_number, values in enumerate(rows[1:], 2):
        data = dict(zip(headers, values))
        expt, round_number = int(data['Expt #']), int(data['Round'])
        fid = f'PBMC-E{expt:02d}'
        raw = [float(data[c]) for c in SOURCE_COLUMNS]
        if any(not math.isfinite(x) or not 0 <= x <= 100 for x in raw):
            raise ValueError(f'Invalid mixture values in {fid}.')
        total = sum(raw)
        if abs(total - 100) > ROUNDING_TOLERANCE_PCT_POINTS:
            raise ValueError(f'Mixture total {total} outside rounding tolerance for {fid}.')
        fractions = dict(zip([c + '_fraction' for c in COMPONENTS], [x / total for x in raw]))
        locator = dict(source_file=SOURCE.name, source_sheet=sheet.title, source_row=row_number)
        formulation = dict(formulation_id=fid, experiment_number=expt, round=round_number, **locator,
                           **dict(zip([c + '_pct_raw' for c in COMPONENTS], raw)),
                           mixture_sum_pct_raw=total, normalisation_applied=abs(total - 100) > 1e-8,
                           normalisation_factor=100 / total, **fractions,
                           supplied_viability_mean_pct=float(data['Average Viability [%]']))
        if formulation['normalisation_applied']:
            issue('info', sheet.title, row_number, f'Published mixture totals {total:g}%.',
                  'Retain raw percentages and proportionally normalise analysis fractions.')
        readings = []
        for reading_number in range(1, 6):
            label = f'Via{reading_number}'
            value = data[label]
            if value is None:
                continue
            value = float(value)
            if not math.isfinite(value) or not 0 <= value <= 100:
                raise ValueError(f'Invalid viability reading in {fid}.')
            readings.append(value)
            measurements.append(dict(measurement_id=f'{fid}-{label}', formulation_id=fid,
                                     source_reading_label=label, viability_pct=value,
                                     assay='AOPI viable-cell assay', timepoint_hours=72, **locator))
        if len(readings) < 2:
            raise ValueError(f'Insufficient reported readings in {fid}.')
        if len(readings) < 5:
            issue('info', sheet.title, row_number, f'{5-len(readings)} of five reading slots are blank.',
                  'Preserve blanks as missing; summarise available readings only.')
        mean = statistics.mean(readings)
        variance = statistics.variance(readings)
        difference = mean - formulation['supplied_viability_mean_pct']
        if abs(difference) > 1e-5:
            raise ValueError(f'Published mean does not reconcile for {fid}: {difference}')
        recipe_key = ','.join(f'{fractions[c+"_fraction"]:.10f}' for c in COMPONENTS)
        group = 'blend-' + hashlib.sha256(recipe_key.encode()).hexdigest()[:12]
        analysis.append(dict(formulation_id=fid, experiment_number=expt, round=round_number,
                             formulation_group=group, **fractions,
                             mixture_sum_pct_raw=total,
                             normalisation_applied=formulation['normalisation_applied'],
                             assay='AOPI viable-cell assay', timepoint_hours=72,
                             n_readings=len(readings), viability_mean_pct=mean,
                             viability_sd_pct_points=math.sqrt(variance),
                             viability_sem_pct_points=math.sqrt(variance / len(readings)),
                             mean_noise_variance_proxy=variance / len(readings),
                             supplied_mean_difference_pct_points=difference,
                             noise_interpretation='Reported-reading spread; donor/pool identities unknown; SEM assumes independence',
                             blend_cost_per_litre=sum(fractions[c+'_fraction'] * prices[c] for c in COMPONENTS) if prices else '',
                             cost_currency=currency,
                             cost_status='calculated_from_supplied_inputs' if prices else 'unavailable_price_inputs'))
        formulations.append(formulation)

    ids = [f['formulation_id'] for f in formulations]
    if len(set(ids)) != len(ids) or len(ids) != 24 or {a['round'] for a in analysis} != {0, 1, 2, 3}:
        raise ValueError('Unexpected experiment IDs, count or rounds.')
    if any(not math.isclose(sum(a[c+'_fraction'] for c in COMPONENTS), 1, abs_tol=1e-12) for a in analysis):
        raise ValueError('Normalised mixtures do not sum to one.')
    if len({m['measurement_id'] for m in measurements}) != len(measurements):
        raise ValueError('Duplicate measurement IDs.')
    if sum(a['n_readings'] for a in analysis) != len(measurements):
        raise ValueError('Reading counts do not reconcile.')

    for row_number, row in enumerate(list(workbook['Control_OptimalMediaComparison'].values)[1:], 2):
        mix = row[1:5]
        if any(x is None for x in mix):
            reason = f'{row[0]} has a missing mixture fraction.'
        elif abs(sum(mix) - 100) > ROUNDING_TOLERANCE_PCT_POINTS:
            reason = f'{row[0]} published fractions total {sum(mix):g}%.'
        else:
            reason = f'{row[0]} belongs to a separate comparison study; not in initial training.'
        issue('warning', 'Control_OptimalMediaComparison', row_number, reason,
              'Exclude from initial training; retain original sheet and resolve context/composition before reuse.')
    issue('warning', sheet.title, '', 'Donor, well and pool identities are not supplied.',
          'Keep reading labels; treat SEM and noise variance as provisional proxies.')
    if prices is None:
        issue('warning', '', '', 'Complete prepared-media price inputs and provenance are unavailable.',
              'Leave costs blank; populate data/inputs/component_costs.csv or define a labelled scenario.')
    issue('info', 'CytokineComposition', '', 'Separate cytokine phase uses different features and outcomes.',
          'Retain source export; exclude from media-blend model.')

    write_csv(PROCESSED / 'pbmc_formulations.csv', formulations)
    write_csv(PROCESSED / 'pbmc_measurements.csv', measurements)
    write_csv(PROCESSED / 'pbmc_analysis.csv', analysis)
    write_csv(PROCESSED / 'data_quality_issues.csv', issues)

    round_summary = []
    for r in sorted({a['round'] for a in analysis}):
        values = [a['viability_mean_pct'] for a in analysis if a['round'] == r]
        round_summary.append(dict(round=r, n_experiments=len(values),
                                  mean_viability_pct=statistics.mean(values),
                                  min_viability_pct=min(values), max_viability_pct=max(values)))
    write_csv(PROCESSED / 'pbmc_round_summary.csv', round_summary)
    best = max(analysis, key=lambda a: a['viability_mean_pct'])
    audit = [
        '# PBMC data audit', '',
        'This report is regenerated by `scripts/prepare_data.py` from the retained public workbook.', '',
        f'- Historical experiments: {len(analysis)}.',
        f'- Unique normalised recipe groups: {len(set(a["formulation_group"] for a in analysis))}.',
        f'- Nonmissing reported readings: {len(measurements)}.',
        f'- Missing reading slots: {len(analysis)*5-len(measurements)}.',
        f'- Readings per experiment: {min(a["n_readings"] for a in analysis)} to {max(a["n_readings"] for a in analysis)}.',
        f'- Source mixture total range: {min(a["mixture_sum_pct_raw"] for a in analysis):g}% to {max(a["mixture_sum_pct_raw"] for a in analysis):g}%.',
        f'- Mixtures proportionally normalised: {sum(a["normalisation_applied"] for a in analysis)}.',
        f'- Largest absolute discrepancy from published means: {max(abs(a["supplied_mean_difference_pct_points"]) for a in analysis):.3g} percentage points.',
        f'- Highest observed mean: {best["formulation_id"]}, {best["viability_mean_pct"]:.2f}% viability in round {best["round"]}. This is an observed result, not a new recommendation.',
        f'- Blend costs: {"calculated from completed price inputs" if prices else "unavailable; price inputs are blank or incomplete"}.', '',
        '| Round | Experiments | Mean viability % | Minimum % | Maximum % |',
        '| --- | --- | --- | --- | --- |',
        *[f'| {a["round"]} | {a["n_experiments"]} | {a["mean_viability_pct"]:.2f} | {a["min_viability_pct"]:.2f} | {a["max_viability_pct"]:.2f} |' for a in round_summary], '',
        'Round means describe adaptively selected historical experiments. They do not establish causal improvement or prospective performance.', '',
        '## Checks completed', '',
        'Source SHA256 verified; required columns unique; experiment and measurement IDs unique; concentration and viability values finite and bounded; mixtures within declared rounding tolerance; normalised fractions sum to one; reading counts reconcile; recomputed means reconcile with supplied means.', '',
        '## Limitations', '',
        'Reported readings lack donor/pool identities. SEM and variance of the mean use an unverified independence assumption. The separate comparison sheet is excluded and contains a 200% AR5 recipe and a missing XVIVO fraction. No source values have been repaired. Prices are provisional estimates from `data/inputs/price_sources.csv`; the cost rule and scenarios are applied in later scripts. No paired fidelity assays exist in this subset.', '',
        f'Source context: [Narayanan et al. 2025]({ARTICLE}); [data](https://doi.org/10.6084/m9.figshare.27715134).', ''
    ]
    (ROOT / 'docs/data_audit.md').write_text('\n'.join(audit))
    print(f'Prepared {len(analysis)} formulations and {len(measurements)} readings. All data checks passed.')


if __name__ == '__main__':
    main()
