"""Offline display of supplied NFL leans and MLB player forecasts; no scoring."""
import argparse
import copy
import hashlib
import html
import json
import math
from pathlib import Path
from report import timestamp

REQUIRED = ("sport", "event_id", "entity_id", "market", "period", "selection",
            "model_version", "captured_at", "status")


def analyze(records, as_of):
    now = timestamp(as_of)
    if not isinstance(records, list):
        raise ValueError("Expected a JSON array")
    output, seen = [], set()
    for record in records:
        if not isinstance(record, dict) or any(
                not isinstance(record.get(k), str) or not record[k].strip()
                for k in REQUIRED):
            raise ValueError("Missing exact identity, model, timestamp or source status")
        if record["sport"] not in ("NFL", "MLB"):
            raise ValueError("Only supplied NFL leans and MLB player forecasts supported")
        if record["sport"] == "MLB" and not record.get("player_id"):
            raise ValueError("MLB player forecasts require player_id")
        captured = timestamp(record["captured_at"])
        p = record.get("probability")
        if p is not None and (type(p) not in (int, float) or not math.isfinite(p) or not 0 <= p <= 1):
            raise ValueError("Probability must be null or finite within [0,1]")
        # Exact target includes line, direction, model version and capture version.
        key = tuple(record[k] for k in REQUIRED if k != "status") + (
            json.dumps(record.get("line"), sort_keys=True), record.get("book"))
        if key in seen:
            raise ValueError("Duplicate forecast version; reconcile upstream")
        seen.add(key)
        issues = ["SOURCE_ADMISSION_NOT_INDEPENDENTLY_VERIFIED",
                  "SAVED_FORECAST_NOT_CURRENT_RECOMMENDATION"]
        if captured > now:
            issues.append("FUTURE_CAPTURE")
        if record.get("start_utc"):
            if timestamp(record["start_utc"]) <= now:
                issues.append("STARTED_OR_HISTORICAL")
        else:
            issues.append("START_TIME_UNKNOWN")
        if record["status"].upper().startswith("HELD"):
            issues.append("SOURCE_HELD_PRESERVED")
        output.append({"original": copy.deepcopy(record),
                       "report_status": "DISPLAY_ONLY_NOT_ADMITTED",
                       "issues": issues})
    return {"as_of": as_of, "rows": output, "count": len(output),
            "status": "SUPPLIED_FORECAST_REPORT_ONLY",
            "new_predictions": 0, "admitted_picks": 0, "network_calls": 0}


def render(result, synthetic=False):
    esc = lambda value: html.escape(str(value), quote=True)
    rows = []
    for item in result["rows"]:
        r = item["original"]
        values = [r["sport"], r["event_id"], r["entity_id"], r["market"],
                  r["period"], r["selection"], r.get("line", "UNKNOWN"),
                  r.get("probability", "UNKNOWN"), r["model_version"],
                  r["captured_at"], r["status"], "; ".join(item["issues"])]
        rows.append("<tr>" + "".join("<td>" + esc(v) + "</td>" for v in values) + "</tr>")
    headers = ["Sport", "Event", "Entity", "Market", "Period", "Selection", "Line",
               "Supplied probability", "Model", "Capture", "Original status", "Report checks"]
    return ('<!doctype html><html lang="en"><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>Supplied forecast report</title><style>body{font:16px system-ui;margin:24px}'
            'td,th{padding:8px;border:1px solid #ccc;text-align:left}table{border-collapse:collapse}'
            '.scroll{overflow-x:auto}</style><h1>NFL / MLB supplied forecast report</h1><p>'
            + ("SYNTHETIC DEMO" if synthetic else "USER-SUPPLIED SAVED DATA")
            + ' — display only, not admitted picks. HELD labels remain unchanged. '
            'No forecasts, fair probabilities, joint probabilities or live prices are generated.</p>'
            '<div class="scroll"><table><thead><tr>'
            + "".join("<th>"+h+"</th>" for h in headers)
            + '</tr></thead><tbody>' + "".join(rows) + '</tbody></table></div></html>')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--as-of", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--synthetic", action="store_true")
    args = parser.parse_args()
    if args.input.stat().st_size > 2_000_000:
        raise ValueError("Input exceeds 2 MB")
    raw = args.input.read_bytes()
    result = analyze(json.loads(raw), args.as_of)
    result["source_sha256"] = hashlib.sha256(raw).hexdigest()
    result["synthetic"] = args.synthetic
    args.output.mkdir(parents=True, exist_ok=False)
    (args.output/"report.json").write_text(json.dumps(result, indent=2, allow_nan=False), encoding="utf8")
    (args.output/"index.html").write_text(render(result, args.synthetic), encoding="utf8")
    print(json.dumps({"rows": result["count"], "admitted_picks": 0, "source_sha256": result["source_sha256"]}))


if __name__ == "__main__":
    main()
