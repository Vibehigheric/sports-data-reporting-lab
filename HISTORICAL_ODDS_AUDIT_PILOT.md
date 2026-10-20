# Historical Odds Audit — proposed $200 pilot

**Scope-first service offer. Not an automated historical-odds product, verified backtest, deployed monitor or TXODDS integration.** Existing 23-test research audit and 35-test CSV product receipts do not establish validation of this new service's odds-specific rules.

## Fixed pilot boundary

USD $200 for one customer-authorized CSV/JSON export, one schema, one sport, one agreed market family, up to 10,000 rows and an agreed date window. Review a synthetic schema sample and agree feasibility, coverage, turnaround, acceptance and payment/cancellation terms before booking. Larger exports, repairs and adapters are separate scope. This is a proposed price, not proven demand.

## Deliverables after agreed implementation

- Schema/field dictionary and exact matching contract: provider event ID, participant, book/source, market, side, line, period, overtime and settlement-rule identifiers.
- Missing fields, duplicate exact keys, conflicting records, timezone and cutoff checks; gaps measured only against a customer-supplied expected coverage grid. Missing expectations mean UNKNOWN coverage, not complete history.
- Separate supplied OPENING labels, observed snapshots and evidenced closing records. Earliest available is not necessarily market opening; last available is not verified closing. Unknown rules/timestamps remain unresolved.
- Written HTML findings, machine-readable exceptions, source-file SHA256 and reproducibility instructions. No silent repairs; retain the original and version corrected exports.
- One review revision and a handoff of exclusions. No source record or betting settlement certified.

## Acceptance

Agree synthetic clean and deliberately flawed examples before processing authorized records. Each agreed check must produce the expected result; original input bytes remain unchanged; repeat runs use new output locations. Hashes check integrity, not source authenticity or independent timestamp attestation. A data audit does not prove a backtest is trustworthy or profitable.

## Planned extensions — not deployed

Feed Health Monitor (staleness, missing updates, schema drift), customer-credential connector setup (bounded retries/cache), and results reconciliation (immutable forecasts/corrections/unresolved states). No automatic recurring billing, 24/7 support, latency or uptime SLA. Define each as a separate pilot after demand and licensing review.

## Supplier and platform boundaries

TXODDS is a potential supplier, not an EdgeGod partner. No feed purchased, vendor contacted, sample requested or API called. Provider headline counts do not establish exact book/prop/period/date coverage. Customer must confirm storage, processing, display and derived-output rights; API access does not confer resale rights.

No live feed resale, sportsbook pricing, wagering, signals, guaranteed outcomes or source-truth/security/legal certification. No Gumroad consulting or odds-feed listing. Fiverr copy stays a draft pending platform review and available capacity.

Public examples must be synthetic. Scope inquiries: IAMDIGITAL.ENT@GMAIL.COM, without credentials or sensitive attachments.
