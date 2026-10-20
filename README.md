# Sports Data Reporting Lab

Offline, standard-library Python demonstration for sports dashboards, MLB odds snapshot comparison, and repeatable reporting. Python 3.10+ required. Synthetic teams and bookmakers; no live API, real sportsbook data, model forecasts, picks or wagers.

## Run

```sh
python -m unittest -v
python report.py --as-of 2026-10-19T18:00:00Z --output reports/demo --synthetic
```

Open `reports/demo/index.html` locally. JSON is generated alongside it. Choose a new output directory for each run; existing directories are not overwritten. The demo timestamp is fixed for reproducibility, not current-market evidence. Inspect the committed `demo-preview/index.html` for a prebuilt synthetic sample.

For authorized customer exports, provide `--input path/to/export.csv`, an explicit timezone-aware `--as-of` timestamp and a fresh output directory. Do not use `--synthetic` for real customer data. The schema is the header of demo.csv. This prototype supports MLB full-game two-way moneyline quotes only; do not mix totals, spreads, props or differing settlement rules. Operator must confirm matching bookmaker settlement and pitcher rules before comparison.

The scanner validates dates and event identities, rejects duplicate quotes and invalid odds, excludes future observations, quotes older than 15 minutes and started events, then selects the highest supplied price per event/selection. It does not fetch quotes or verify whether a price can actually be bet. Inverse decimal odds are margin-inclusive implied probabilities, not model forecasts. An empty eligible set produces NO_ELIGIBLE_QUOTES rather than a recommendation.

## Related freelance services

Contact: [IAMDIGITAL.ENT@GMAIL.COM](mailto:IAMDIGITAL.ENT@GMAIL.COM?subject=Sports%20Data%20Project).

- **I will build a sports analytics dashboard:** one authorized dataset, agreed metrics, clear timestamps and a dashboard/report. This repository demonstrates a snapshot table, not a complete interactive multi-sport product.
- **I will create an MLB odds scanner:** scope approved data feeds, market identifiers, freshness checks and price comparison. The included prototype scans offline snapshots; live adapters, API subscriptions and hosting require separate work.
- **I will automate sports data reporting:** validated input, reproducible report generation and agreed delivery. The command-line report works now; scheduling, email and Telegram delivery are not implemented here.

Paid work requires written scope, acceptance criteria, usage rights and terms. No promised profits, betting success, prediction accuracy or income. No bets are placed and no gambling accounts are connected. Do not send API keys, passwords or personal betting records to public issues.

## Data rights and security

Use client-owned data or a provider license covering the exact intended display and redistribution. API access is not blanket resale permission. No sportsbook scraping, access-control bypass, user-account automation or private data publication. Client keeps provider credentials in their own secret store, never a public repository. Historical tests must preserve observation timestamps and separate future information from available-at-the-time inputs.

## License

Limited evaluation only under LICENSE.txt, not an open-source license. Richard Jones reserves commercial-use and redistribution rights to the extent legally held; GitHub platform and mandatory legal rights remain unaffected. AI-assisted implementation; copyright is not claimed where it does not exist. No warranty or support is included. The custom license is a draft requiring legal review before commercial reliance. A separate agreement is needed for production deployment or paid client use.


## NFL leans and MLB player forecast reporting

`forecast_report.py` displays existing user-supplied NFL leans and MLB player forecasts offline. It does not fit or run prediction models. The original MLB quote-comparison command remains unchanged.

```sh
python forecast_report.py --input forecast_demo.json --as-of 2026-10-20T17:00:00Z --output forecast-preview --synthetic
python -m unittest discover -v
```

The JSON input is an array; `forecast_demo.json` documents the required fields. Each record needs sport (NFL or MLB), event_id, entity_id, market, period, selection, model_version, captured_at (timezone required), and the original status. MLB also requires player_id. Use an explicit exact line when applicable; probability may be absent/null and is never inferred from odds. Include start_utc when known. Extra fields such as original BPP, provenance, odds and uncertainty are retained unchanged in the nested `original` JSON record.

**HELD labels remain intact.** The report always adds DISPLAY_ONLY_NOT_ADMITTED separately, even if a source claims CLEARED. Missing start time, future captures and historical events are flagged, not silently repaired. This is an archive/report adapter, not a pregame admission engine. It performs no API calls and will not overwrite an existing output directory. The input bytes are hashed. Do not publish private customer or licensed forecast data; the supplied example is synthetic only.
