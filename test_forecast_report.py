import copy
import unittest
from forecast_report import analyze, render


def fixture():
    return dict(sport="NFL", event_id="synthetic-event", entity_id="synthetic-team",
                market="moneyline", period="REGULATION", selection="HOME",
                model_version="SYNTHETIC_V1", captured_at="2026-10-20T16:00:00Z",
                status="HELD_LINEUP", probability=0.55, line=None)


class ForecastTests(unittest.TestCase):
    def test_preserves_input_and_held(self):
        row = fixture()
        before = copy.deepcopy(row)
        result = analyze([row], "2026-10-20T17:00:00Z")
        self.assertEqual(result["rows"][0]["original"], before)
        self.assertEqual(row, before)
        self.assertIn("HELD_LINEUP", render(result))
        self.assertEqual(result["admitted_picks"], 0)

    def test_mlb_and_unknown_probability(self):
        row = dict(fixture(), sport="MLB", player_id="synthetic-player",
                   entity_id="synthetic-player", market="batter_home_runs",
                   period="FULL_GAME_INCLUDING_EXTRAS", probability=None)
        self.assertIsNone(analyze([row], "2026-10-20T17:00:00Z")["rows"][0]["original"]["probability"])
        del row["player_id"]
        with self.assertRaises(ValueError):
            analyze([row], "2026-10-20T17:00:00Z")

    def test_bad_and_duplicate(self):
        for p in (True, float("nan"), float("inf"), -0.1, 1.1):
            with self.assertRaises(ValueError):
                analyze([dict(fixture(), probability=p)], "2026-10-20T17:00:00Z")
        with self.assertRaises(ValueError):
            analyze([fixture(), fixture()], "2026-10-20T17:00:00Z")

    def test_future_and_source_status_not_admission(self):
        row = dict(fixture(), status="CLEARED")
        result = analyze([row], "2026-10-19T17:00:00Z")
        self.assertIn("FUTURE_CAPTURE", result["rows"][0]["issues"])
        self.assertEqual(result["rows"][0]["original"]["status"], "CLEARED")
        self.assertEqual(result["rows"][0]["report_status"], "DISPLAY_ONLY_NOT_ADMITTED")

    def test_escape_and_timezone(self):
        row = dict(fixture(), selection="<script>alert(1)</script>")
        self.assertNotIn("<script>", render(analyze([row], "2026-10-20T17:00:00Z")))
        with self.assertRaises(ValueError):
            analyze([dict(row, captured_at="2026-10-20T16:00:00")], "2026-10-20T17:00:00Z")
