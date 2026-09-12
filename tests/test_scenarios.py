import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from submission_cards.scenarios import ScenarioValidationError, compare_scenarios


def sample():
    return {
        "card": {"game": "Synthetic", "set": "Test", "number": "001", "variant": "Test foil", "language": "en", "condition": "NM"},
        "currency": "USD", "as_of": "2026-01-01", "raw_net": 100,
        "raw_receipt_days": 0, "annual_discount_rate": 0, "budget": None,
        "routes": [{"id": "PSA_SYNTHETIC", "assumption_basis": "Synthetic test data; not market evidence",
                    "upfront_costs": {"grading": 20, "shipping": 10},
                    "outcomes": [
                        {"label": "PSA 10", "probability": 0.5, "gross_sale": 300, "sale_fee_rate": 0.1, "cashout_fee_rate": 0.05, "receipt_costs": 5, "receipt_days": 120},
                        {"label": "PSA 9", "probability": 0.5, "gross_sale": 100, "sale_fee_rate": 0.1, "cashout_fee_rate": 0.05, "receipt_costs": 5, "receipt_days": 120},
                    ]}],
    }


class ScenarioTests(unittest.TestCase):
    def row(self, doc=None, scenario=1):
        return compare_scenarios(doc or sample())["scenarios"][scenario]["routes"][0]

    def test_independent_cashflow_arithmetic(self):
        # 300 * .9 * .95 - 5 = 251.5; 100 * .9 * .95 - 5 = 80.5.
        # Average 166 less ONE upfront cost 30 -> 136, incremental 36.
        row = self.row()
        self.assertAlmostEqual(row['expected_net'], 136)
        self.assertAlmostEqual(row['incremental_net'], 36)
        self.assertAlmostEqual(row['incremental_roi'], 1.2)
        self.assertEqual(row['capital_required'], 30)
        self.assertEqual(row['probability_underperform_raw'], .5)
        self.assertEqual(row['probability_cash_loss'], 0)

    def test_horizons_use_actual_receipt_days(self):
        result = compare_scenarios(sample())
        self.assertEqual([s['horizon_days'] for s in result['scenarios']], [90, 180, 365])
        self.assertIn('ROUTE_AFTER_HORIZON', result['scenarios'][0]['routes'][0]['reasons'])
        self.assertEqual(result['scenarios'][1]['routes'][0]['status'], 'SIMULATION_ONLY')

    def test_missing_budget_never_means_unlimited_or_approved(self):
        result = compare_scenarios(sample())
        self.assertIn('BUDGET_UNSET', result['allocation_blockers'])
        self.assertFalse(result['submission_ready'])
        self.assertIsNone(self.row()['within_individual_budget'])

    def test_zero_budget_and_exact_boundary(self):
        doc = sample()
        doc['budget'] = 0
        self.assertIn('OVER_INDIVIDUAL_BUDGET', self.row(doc)['reasons'])
        doc['budget'] = 30
        self.assertTrue(self.row(doc)['within_individual_budget'])
        self.assertFalse(compare_scenarios(doc)['submission_ready'])

    def test_discounting_both_alternatives(self):
        doc = sample()
        doc['annual_discount_rate'] = .1
        doc['raw_receipt_days'] = 365
        for o in doc['routes'][0]['outcomes']:
            o['receipt_days'] = 365
        row = self.row(doc, 2)
        self.assertAlmostEqual(row['incremental_present_value'], 166 / 1.1 - 30 - 100 / 1.1)
        self.assertIn('RAW_AFTER_HORIZON', self.row(doc, 0)['reasons'])

    def test_negative_return_is_excluded(self):
        doc = sample()
        doc['routes'][0]['upfront_costs']['grading'] = 200
        self.assertIn('NONPOSITIVE_INCREMENTAL_PRESENT_VALUE', self.row(doc)['reasons'])

    def test_zero_cost_roi_is_undefined(self):
        doc = sample()
        doc['routes'][0]['upfront_costs'] = {'no_upfront_cost': 0}
        self.assertIsNone(self.row(doc)['incremental_roi'])

    def test_negative_receipt_requires_extra_reserve(self):
        doc = sample()
        doc['routes'][0]['outcomes'][1]['receipt_costs'] = 100
        self.assertAlmostEqual(self.row(doc)['capital_required'], 44.5)

    def test_invalid_distribution(self):
        for bad in (None, -.1, .7, float('nan'), True, '0.5'):
            with self.subTest(bad=bad):
                doc = sample()
                doc['routes'][0]['outcomes'][0]['probability'] = bad
                with self.assertRaises(ScenarioValidationError):
                    compare_scenarios(doc)

    def test_missing_cost_and_identity_fail_closed(self):
        for field in ('gross_sale', 'sale_fee_rate', 'cashout_fee_rate', 'receipt_costs'):
            doc = sample()
            doc['routes'][0]['outcomes'][0][field] = None
            with self.assertRaises(ScenarioValidationError):
                compare_scenarios(doc)
        doc = sample()
        del doc['card']['language']
        with self.assertRaises(ScenarioValidationError):
            compare_scenarios(doc)

    def test_duplicate_routes_rejected(self):
        doc = sample()
        doc['routes'].append(copy.deepcopy(doc['routes'][0]))
        with self.assertRaises(ScenarioValidationError):
            compare_scenarios(doc)

    def test_ranked_by_incremental_present_value(self):
        doc = sample()
        cheaper = copy.deepcopy(doc['routes'][0])
        cheaper['id'] = 'Alternative'
        cheaper['upfront_costs'] = {'total': 15}
        doc['routes'].append(cheaper)
        self.assertEqual(compare_scenarios(doc)['scenarios'][1]['routes'][0]['id'], 'Alternative')

    def test_cli_writes_file_without_disclosing_input_or_overwriting(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, target = Path(tmp) / 'input.json', Path(tmp) / 'result.json'
            source.write_text(json.dumps(sample()))
            cmd = [sys.executable, '-m', 'submission_cards.cli', 'compare', str(source), '--output', str(target)]
            run = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertEqual(json.loads(run.stdout), {'ok': True, 'simulation_only': True})
            saved = target.read_bytes()
            self.assertTrue(json.loads(saved)['simulation_only'])
            self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 2)
            self.assertEqual(target.read_bytes(), saved)
