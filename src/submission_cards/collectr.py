"""Collectr CSV validation and inventory summaries."""

from __future__ import annotations

import csv
import re
import unicodedata
from datetime import date
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
        parsed = Decimal(value.strip())
        if not parsed.is_finite() or parsed != parsed.to_integral_value():
            raise ValueError("Quantity must be a finite integer")
        quantity = int(parsed)
    except (InvalidOperation, ValueError, AttributeError) as exc:
        raise CollectrValidationError(
            f"Invalid Quantity at CSV row {row_number}"
        ) from exc
    if quantity < 0:
        raise CollectrValidationError(
            f"Negative Quantity at CSV row {row_number}"
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
        if len(headers) != len(reader.fieldnames or []):
            raise CollectrValidationError("Duplicate CSV headers")
        missing = REQUIRED_COLUMNS - headers
        if missing:
            raise CollectrValidationError(
                "Missing required columns: " + ", ".join(sorted(missing))
            )
        price_headers = [h for h in headers if h.startswith(MARKET_PRICE_PREFIX)]
        if len(price_headers) != 1:
            raise CollectrValidationError("Expected one Collectr market price column")
        match = re.fullmatch(r"Market Price \(As of (\d{4}-\d{2}-\d{2})\)", price_headers[0])
        try:
            if match is None:
                raise ValueError("Invalid date format")
            date.fromisoformat(match.group(1))
        except ValueError as exc:
            raise CollectrValidationError("Invalid market price date") from exc

        records = total_units = pokemon_records = pokemon_units = 0
        categories: set[str] = set()

        for row_number, row in enumerate(reader, start=2):
            if None in row or any(value is None for value in row.values()):
                raise CollectrValidationError(f"Malformed CSV row {row_number}")
            for field in ("Category", "Product Name"):
                if not row[field].strip():
                    raise CollectrValidationError(f"Empty {field} at CSV row {row_number}")
            records += 1
            quantity = _parse_quantity(row["Quantity"], row_number)
            total_units += quantity
            category = row["Category"].strip()
            categories.add(category)
            normalized = unicodedata.normalize("NFKD", category.casefold())
            normalized = "".join(c for c in normalized if not unicodedata.combining(c))
            if normalized == "pokemon":
                pokemon_records += 1
                pokemon_units += quantity

    return InventorySummary(
        records=records,
        total_units=total_units,
        pokemon_records=pokemon_records,
        pokemon_units=pokemon_units,
        categories=tuple(sorted(categories)),
    )
