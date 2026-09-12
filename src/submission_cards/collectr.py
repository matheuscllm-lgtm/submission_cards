"""Collectr CSV validation and inventory summaries."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path


REQUIRED_COLUMNS = {
    "Portfolio Name",
    "Category",
    "Set",
    "Product Name",
    "Card Number",
    "Variance",
    "Grade",
    "Card Condition",
    "Quantity",
}

MARKET_PRICE_PREFIX = "Market Price (As of "


class CollectrValidationError(ValueError):
    """Raised when a Collectr export is unusable."""


@dataclass(frozen=True)
class InventorySummary:
    records: int
    total_units: int
    pokemon_records: int
    pokemon_units: int
    categories: tuple[str, ...]


def _parse_quantity(value: str, row_number: int) -> int:
    try:
        quantity = int(Decimal(value.strip()))
    except (InvalidOperation, ValueError) as exc:
        raise CollectrValidationError(
            f"Invalid Quantity at CSV row {row_number}: {value!r}"
        ) from exc
    if quantity < 0:
        raise CollectrValidationError(
            f"Negative Quantity at CSV row {row_number}: {quantity}"
        )
    return quantity


def summarize_export(path: str | Path) -> InventorySummary:
    """Validate a Collectr CSV and return a non-financial inventory summary."""

    source = Path(path)
    if not source.is_file():
        raise CollectrValidationError(f"File not found: {source}")

    with source.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        headers = set(reader.fieldnames or [])
        missing = REQUIRED_COLUMNS - headers
        if missing:
            raise CollectrValidationError(
                "Missing required columns: " + ", ".join(sorted(missing))
            )
        if not any(header.startswith(MARKET_PRICE_PREFIX) for header in headers):
            raise CollectrValidationError("Missing Collectr market price column")

        records = total_units = pokemon_records = pokemon_units = 0
        categories: set[str] = set()

        for row_number, row in enumerate(reader, start=2):
            records += 1
            quantity = _parse_quantity(row["Quantity"], row_number)
            total_units += quantity
            category = row["Category"].strip()
            categories.add(category)
            if "pokemon" in category.casefold():
                pokemon_records += 1
                pokemon_units += quantity

    return InventorySummary(
        records=records,
        total_units=total_units,
        pokemon_records=pokemon_records,
        pokemon_units=pokemon_units,
        categories=tuple(sorted(categories)),
    )
