"""Convert catalogue pack prices into prepared-medium cost per litre, plus a price sensitivity grid."""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / 'data/inputs/price_sources.csv'
COSTS = ROOT / 'data/inputs/component_costs.csv'
SCENARIOS = ROOT / 'data/inputs/cost_scenarios.csv'

# Article methods: basal medium + 10% FBS + 1% Penicillin-Streptomycin, by volume.
SUPPLEMENTED = {'basal': 0.89, 'fbs': 0.10, 'pen_strep': 0.01}
FBS_MULTIPLIERS = [0.5, 1.0, 1.5]
AR5_MULTIPLIERS = [1.0, 1.5, 2.02]  # times X-VIVO 15 per litre; 2.02 from the CellGenix GMP TCM reference


def per_litre(row):
    return float(row['pack_price']) / float(row['pack_volume_ml']) * 1000


def prepared_prices(src, fbs_mult=1.0, ar5_mult=1.0):
    fbs = per_litre(src['fbs']) * fbs_mult
    pen = per_litre(src['pen_strep'])
    supplements = SUPPLEMENTED['fbs'] * fbs + SUPPLEMENTED['pen_strep'] * pen
    xvivo = per_litre(src['xvivo15'])
    return {
        'dmem': SUPPLEMENTED['basal'] * per_litre(src['dmem_basal']) + supplements,
        'rpmi_10': SUPPLEMENTED['basal'] * per_litre(src['rpmi_basal']) + supplements,
        'xvivo': xvivo,
        'ar5': xvivo * ar5_mult,
    }


def main():
    with SOURCES.open(newline='') as handle:
        src = {r['item_id']: r for r in csv.DictReader(handle)}
    base = prepared_prices(src)
    meta = {
        'dmem': ('DMEM with 10% FBS and 1% Penicillin-Streptomycin per article methods', 'estimate',
                 'price_sources.csv: dmem_basal, fbs, pen_strep', 'FBS is about 74% of this cost and is a search-snippet price'),
        'rpmi_10': ('RPMI-10 with 10% FBS and 1% Penicillin-Streptomycin per article methods', 'estimate',
                    'price_sources.csv: rpmi_basal, fbs, pen_strep', 'FBS is about 79% of this cost and is a search-snippet price'),
        'xvivo': ('XVIVO 15 prepared per manufacturer instructions', 'observed',
                  'price_sources.csv: xvivo15', 'Complete medium; no supplements added'),
        'ar5': ('AR5 prepared per manufacturer instructions', 'hypothetical',
                'price_sources.csv: ar5 (proxy = X-VIVO 15 per litre)', 'AR5 price not found; swept 1.0x to 2.02x X-VIVO 15'),
    }
    rows = [dict(component_id=c, prepared_medium_label=meta[c][0], price_per_litre=f'{base[c]:.2f}', currency='EUR',
                 price_basis=meta[c][1], price_source=meta[c][2], as_of_date='2026-10-02', notes=meta[c][3])
            for c in ['dmem', 'rpmi_10', 'xvivo', 'ar5']]
    with COSTS.open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    grid = []
    for fm in FBS_MULTIPLIERS:
        for am in AR5_MULTIPLIERS:
            p = prepared_prices(src, fm, am)
            grid.append(dict(scenario=f'fbs_x{fm}_ar5_x{am}', fbs_multiplier=fm, ar5_multiplier=am,
                             **{f'{c}_eur_per_litre': f'{v:.2f}' for c, v in p.items()}))
    with SCENARIOS.open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(grid[0]))
        writer.writeheader()
        writer.writerows(grid)

    for c, v in base.items():
        print(f'{c:8s} EUR {v:7.2f} per litre')


if __name__ == '__main__':
    main()
