"""Offline moneyline snapshot report. No forecasting, network or betting actions."""
import argparse
import csv
from datetime import datetime, timezone
import html
import json
import math
from pathlib import Path

FIELDS = ['event_id', 'sport', 'home', 'away', 'start_utc', 'book', 'selection', 'decimal_odds', 'observed_utc']


def timestamp(value):
    parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if parsed.utcoffset() is None:
        raise ValueError('Timestamps require an explicit timezone')
    return parsed.astimezone(timezone.utc)


def analyze(rows, as_of, max_age=900):
    now = timestamp(as_of)
    if max_age <= 0:
        raise ValueError('max_age must be positive')
    seen, events, quotes = set(), {}, []
    excluded = 0
    for row in rows:
        if set(row) != set(FIELDS) or any(not isinstance(v, str) or not v.strip() or len(v) > 200 for v in row.values()):
            raise ValueError('Missing, extra or invalid field')
        price = float(row['decimal_odds'])
        if not math.isfinite(price) or price <= 1:
            raise ValueError('Decimal odds must be finite and greater than 1')
        start, observed = timestamp(row['start_utc']), timestamp(row['observed_utc'])
        if row['sport'] != 'MLB' or row['home'] == row['away'] or row['selection'] not in (row['home'], row['away']):
            raise ValueError('Expected MLB two-team moneyline selection')
        key = (row['event_id'], row['book'], row['selection'])
        if key in seen:
            raise ValueError('Duplicate quote; provide one snapshot per book/selection')
        seen.add(key)
        identity = (row['home'], row['away'], start)
        if row['event_id'] in events and events[row['event_id']] != identity:
            raise ValueError('Conflicting event metadata')
        events[row['event_id']] = identity
        age = (now - observed).total_seconds()
        if age < 0 or age > max_age or start <= now:
            excluded += 1
            continue
        quotes.append({**row, 'decimal_odds': price, 'implied_probability': 1 / price})
    best = {}
    for quote in quotes:
        key = (quote['event_id'], quote['selection'])
        if key not in best or quote['decimal_odds'] > best[key]['decimal_odds']:
            best[key] = quote
    return {'as_of': as_of, 'market': 'two-way full-game moneyline only',
            'input_rows': len(rows), 'eligible_rows': len(quotes), 'excluded_rows': excluded,
            'best_observed_prices': list(best.values()),
            'status': 'SNAPSHOT_COMPARISON_ONLY' if quotes else 'NO_ELIGIBLE_QUOTES',
            'warning': 'Implied probability includes bookmaker margin. No fair probabilities, picks, EV or arbitrage claims. Confirm matching settlement rules separately.'}


def render(result, synthetic):
    esc = lambda x: html.escape(str(x), quote=True)
    cells = ''.join('<tr>' + ''.join('<td>' + esc(q[k]) + '</td>' for k in
        ('event_id', 'selection', 'book', 'decimal_odds')) + '</tr>' for q in result['best_observed_prices'])
    return '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sports snapshot report</title><style>body{font:16px system-ui;margin:0;color:#18241c;background:#fff}main{max-width:1050px;margin:auto;padding:24px}h1{font-size:28px}header{border-bottom:3px solid #198754}strong{color:#a14217}.scroll{overflow-x:auto}table{border-collapse:collapse;width:100%;min-width:540px}td,th{text-align:left;padding:12px;border-bottom:1px solid #ccd4ce}p{line-height:1.5}footer{margin-top:32px;border-top:1px solid #ccd4ce;padding-top:16px}</style><main><header><h1>MLB moneyline snapshot</h1><strong>''' + ('SYNTHETIC DEMO - NOT LIVE DATA' if synthetic else 'USER-SUPPLIED SNAPSHOT - NOT LIVE VERIFIED') + '''</strong></header><p>As of ''' + esc(result['as_of']) + '</p><p>Eligible quotes: ' + str(result['eligible_rows']) + ' | Excluded: ' + str(result['excluded_rows']) + '</p><div class="scroll"><table><thead><tr><th>Event</th><th>Selection</th><th>Book</th><th>Decimal odds</th></tr></thead><tbody>' + (cells or '<tr><td colspan="4">No eligible quotes</td></tr>') + '</tbody></table></div><p>' + esc(result['warning']) + '</p><footer>Independent data-reporting demonstration. No wagers or accounts connected.</footer></main></html>'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=Path, default=Path(__file__).with_name('demo.csv'))
    parser.add_argument('--as-of', required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--synthetic', action='store_true')
    args = parser.parse_args()
    if args.input.stat().st_size > 2_000_000:
        raise ValueError('Input exceeds 2 MB')
    with args.input.open(encoding='utf-8', newline='') as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != FIELDS:
            raise ValueError('CSV headers must match documented schema exactly')
        rows = list(reader)
    result = analyze(rows, args.as_of)
    result['synthetic'] = args.synthetic
    args.output.mkdir(parents=True, exist_ok=False)
    (args.output / 'report.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    (args.output / 'index.html').write_text(render(result, args.synthetic), encoding='utf-8')
    print(json.dumps({'status': result['status'], 'eligible': result['eligible_rows'], 'excluded': result['excluded_rows']}))


if __name__ == '__main__':
    main()
