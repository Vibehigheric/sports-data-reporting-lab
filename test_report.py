import csv
from pathlib import Path
import unittest
from report import analyze, render


class Tests(unittest.TestCase):
    def setUp(self):
        with Path(__file__).with_name('demo.csv').open() as f:
            self.rows = list(csv.DictReader(f))
        self.now = '2026-10-19T18:00:00Z'

    def test_best_and_stale(self):
        result = analyze(self.rows, self.now)
        self.assertEqual(result['excluded_rows'], 1)
        self.assertEqual(result['best_observed_prices'][0]['decimal_odds'], 1.95)

    def test_duplicate(self):
        with self.assertRaises(ValueError):
            analyze(self.rows + [self.rows[0]], self.now)

    def test_bad_odds(self):
        for value in ('nan', 'inf', '1', '-2'):
            self.rows[0]['decimal_odds'] = value
            with self.assertRaises(ValueError):
                analyze(self.rows, self.now)

    def test_future_and_started(self):
        self.assertEqual(analyze(self.rows, '2026-10-19T15:00:00Z')['eligible_rows'], 0)
        self.assertEqual(analyze(self.rows, '2026-10-20T00:00:00Z')['eligible_rows'], 0)

    def test_escape(self):
        self.rows[0]['book'] = '<script>alert(1)</script>'
        page = render(analyze([self.rows[0]], self.now), True)
        self.assertNotIn('<script>', page)
        self.assertIn('SYNTHETIC DEMO', page)

    def test_naive_time(self):
        with self.assertRaises(ValueError):
            analyze(self.rows, '2026-10-19T18:00:00')


if __name__ == '__main__':
    unittest.main()
