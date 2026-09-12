import unittest

import test_collectr as fixtures
from submission_cards.collectr import CollectrValidationError, summarize_export


class ImportBoundaryTests(unittest.TestCase):
    write_csv = fixtures.CollectrTests.write_csv

    def row(self, quantity="1", category="Pokemon"):
        return f"Main,{category},Synthetic Set,Synthetic Card,001,Rare,Holofoil,Ungraded,Near Mint,0,{quantity},10,0,false,2026-01-01,\n"

    def test_fractional_and_nonfinite_quantities_fail(self):
        for quantity in ("1.5", "-0.5", "NaN", "Infinity", "-Infinity", "", "abc"):
            with self.subTest(quantity=quantity):
                with self.assertRaises(CollectrValidationError):
                    summarize_export(self.write_csv(fixtures.HEADER + self.row(quantity)))

    def test_integral_decimal_quantity_is_exact(self):
        self.assertEqual(summarize_export(self.write_csv(fixtures.HEADER + self.row("2.0"))).total_units, 2)

    def test_accented_category_and_false_positive(self):
        summary = summarize_export(self.write_csv(fixtures.HEADER + self.row(category="Pokémon") + self.row(category="NotPokemon")))
        self.assertEqual(summary.pokemon_records, 1)

    def test_accepts_new_export_date_and_bom(self):
        header = '\ufeff' + fixtures.HEADER.replace('2026-09-11', '2027-01-01')
        self.assertEqual(summarize_export(self.write_csv(header + self.row())).records, 1)

    def test_malformed_rows_fail(self):
        for row in (self.row().rstrip() + ',extra\n', 'Main,Pokemon\n'):
            with self.subTest(row=row):
                with self.assertRaisesRegex(CollectrValidationError, 'Malformed CSV row'):
                    summarize_export(self.write_csv(fixtures.HEADER + row))

    def test_bad_dates_and_duplicate_headers_fail(self):
        for header in (fixtures.HEADER.replace('2026-09-11', '2026-02-30'), fixtures.HEADER.replace('Notes', 'Quantity')):
            with self.subTest(header=header):
                with self.assertRaises(CollectrValidationError):
                    summarize_export(self.write_csv(header + self.row()))

    def test_empty_category_fails(self):
        with self.assertRaisesRegex(CollectrValidationError, 'Empty Category'):
            summarize_export(self.write_csv(fixtures.HEADER + self.row(category='')))
