from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from submission_cards.collectr import CollectrValidationError, summarize_export


HEADER = (
    "Portfolio Name,Category,Set,Product Name,Card Number,Rarity,Variance,Grade,"
    "Card Condition,Average Cost Paid,Quantity,Market Price (As of 2026-09-11),"
    "Price Override,Watchlist,Date Added,Notes\n"
)


class CollectrTests(unittest.TestCase):
    def write_csv(self, text: str) -> Path:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "export.csv"
        path.write_text(text, encoding="utf-8")
        return path

    def test_summarizes_and_filters_pokemon(self) -> None:
        rows = (
            "Main,Pokemon,Set A,Card A,001,Rare,Holofoil,Ungraded,Near Mint,0,2,10,0,false,2026-01-01,\n"
            "Main,Dragon Ball,Set B,Card B,002,Rare,Holofoil,Ungraded,Near Mint,0,1,20,0,false,2026-01-01,\n"
        )
        summary = summarize_export(self.write_csv(HEADER + rows))
        self.assertEqual(summary.records, 2)
        self.assertEqual(summary.total_units, 3)
        self.assertEqual(summary.pokemon_records, 1)
        self.assertEqual(summary.pokemon_units, 2)

    def test_rejects_missing_required_columns(self) -> None:
        path = self.write_csv("Category,Quantity\nPokemon,1\n")
        with self.assertRaisesRegex(CollectrValidationError, "Missing required columns"):
            summarize_export(path)

    def test_rejects_negative_quantity(self) -> None:
        row = "Main,Pokemon,Set A,Card A,001,Rare,Holofoil,Ungraded,Near Mint,0,-1,10,0,false,2026-01-01,\n"
        with self.assertRaisesRegex(CollectrValidationError, "Negative Quantity"):
            summarize_export(self.write_csv(HEADER + row))


if __name__ == "__main__":
    unittest.main()
