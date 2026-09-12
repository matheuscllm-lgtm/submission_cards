"""Scenario arithmetic for one copy; not a market-data or submission recommender."""

from __future__ import annotations

import math
from datetime import date

HORIZONS = (90, 180, 365)
IDENTITY_FIELDS = ("game", "set", "number", "variant", "language", "condition")


class ScenarioValidationError(ValueError):
    """Input is incomplete, ambiguous or numerically invalid."""


def number(value, field, *, maximum=None, integer=False):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ScenarioValidationError(f"{field}: explicit numeric value required")
    try:
        value = float(value)
    except OverflowError as exc:
        raise ScenarioValidationError(f"{field}: invalid number") from exc
    if not math.isfinite(value) or value < 0 or (maximum is not None and value > maximum):
        raise ScenarioValidationError(f"{field}: out of range")
    if integer and not value.is_integer():
        raise ScenarioValidationError(f"{field}: integer required")
    return value


def text(value, field):
    if not isinstance(value, str) or not value.strip():
        raise ScenarioValidationError(f"{field}: nonempty text required")
    return value


def present_value(amount, days, annual_rate):
    return amount / ((1 + annual_rate) ** (days / 365))


def compare_scenarios(document):
    """Compare supplied scenarios. Never construct or approve a submission batch.

    Costs at time zero are deducted once. At receipt, sale fee applies to gross,
    cashout applies to the balance after sale fee, then other receipt costs apply.
    Inputs are assumed to describe one exact copy and one currency. Prices and
    probabilities are user-supplied hypotheses, not validated market evidence.
    """
    if not isinstance(document, dict):
        raise ScenarioValidationError("Expected an object")
    card = document.get("card")
    if not isinstance(card, dict):
        raise ScenarioValidationError("card: complete identity required")
    for field in IDENTITY_FIELDS:
        text(card.get(field), f"card.{field}")
    currency = text(document.get("currency"), "currency")
    if len(currency) != 3 or not currency.isascii() or not currency.isalpha() or currency != currency.upper():
        raise ScenarioValidationError("currency: uppercase three-letter code required")
    as_of = text(document.get("as_of"), "as_of")
    try:
        date.fromisoformat(as_of)
    except ValueError as exc:
        raise ScenarioValidationError("as_of: ISO date required") from exc
    raw_net = number(document.get("raw_net"), "raw_net")
    raw_days = number(document.get("raw_receipt_days"), "raw_receipt_days", integer=True)
    discount = number(document.get("annual_discount_rate"), "annual_discount_rate", maximum=1)
    budget = document.get("budget")
    if budget is not None:
        budget = number(budget, "budget")
    routes = document.get("routes")
    if not isinstance(routes, list) or not routes:
        raise ScenarioValidationError("routes: nonempty list required")

    raw_pv = present_value(raw_net, raw_days, discount)
    evaluations = []
    route_ids = set()
    for route in routes:
        if not isinstance(route, dict):
            raise ScenarioValidationError("route: object required")
        route_id = text(route.get("id"), "route.id")
        if route_id in route_ids:
            raise ScenarioValidationError("Duplicate route ID")
        route_ids.add(route_id)
        basis = text(route.get("assumption_basis"), "assumption_basis")
        costs = route.get("upfront_costs")
        if not isinstance(costs, dict) or not costs:
            raise ScenarioValidationError("upfront_costs: named costs required, including explicit zero if applicable")
        upfront = sum(number(v, f"upfront_costs.{k}") for k, v in costs.items())
        outcomes = route.get("outcomes")
        if not isinstance(outcomes, list) or not outcomes:
            raise ScenarioValidationError("outcomes: nonempty list required")
        probabilities, receipts, days_list, pv_receipts = [], [], [], []
        labels = set()
        for outcome in outcomes:
            if not isinstance(outcome, dict):
                raise ScenarioValidationError("outcome: object required")
            label = text(outcome.get("label"), "outcome.label")
            if label in labels:
                raise ScenarioValidationError("Duplicate outcome label")
            labels.add(label)
            p = number(outcome.get("probability"), "probability", maximum=1)
            gross = number(outcome.get("gross_sale"), "gross_sale")
            sale_fee = number(outcome.get("sale_fee_rate"), "sale_fee_rate", maximum=1)
            cashout_fee = number(outcome.get("cashout_fee_rate"), "cashout_fee_rate", maximum=1)
            other = number(outcome.get("receipt_costs"), "receipt_costs")
            days = number(outcome.get("receipt_days"), "receipt_days", integer=True)
            receipt = gross * (1 - sale_fee) * (1 - cashout_fee) - other
            probabilities.append(p)
            receipts.append(receipt)
            days_list.append(days)
            pv_receipts.append(present_value(receipt, days, discount))
        if not math.isclose(sum(probabilities), 1, abs_tol=1e-9, rel_tol=0):
            raise ScenarioValidationError("Outcome probabilities must sum to 1")
        ev = sum(p * receipt for p, receipt in zip(probabilities, receipts)) - upfront
        pv = sum(p * receipt for p, receipt in zip(probabilities, pv_receipts)) - upfront
        # Only outcomes with positive mass constrain receipt horizon and reserve.
        active = [(p, receipt, day) for p, receipt, day in zip(probabilities, receipts, days_list) if p > 0]
        capital = upfront + max(0, -min(receipt for _, receipt, _ in active))
        evaluations.append({
            "id": route_id, "assumption_basis": basis,
            "upfront_cost": upfront, "capital_required": capital,
            "expected_net": ev, "incremental_net": ev - raw_net,
            "expected_present_value": pv, "incremental_present_value": pv - raw_pv,
            "incremental_roi": (ev - raw_net) / capital if capital > 0 else None,
            "expected_receipt_days": sum(p * day for p, _, day in active),
            "latest_receipt_days": max(day for _, _, day in active),
            "probability_underperform_raw": sum(p for p, receipt, _ in active if receipt - upfront < raw_net),
            "probability_cash_loss": sum(p for p, receipt, _ in active if receipt - upfront < 0),
            "within_individual_budget": None if budget is None else capital <= budget,
        })
    scenarios = []
    for horizon in HORIZONS:
        rows = []
        for result in evaluations:
            reasons = []
            if raw_days > horizon:
                reasons.append("RAW_AFTER_HORIZON")
            if result["latest_receipt_days"] > horizon:
                reasons.append("ROUTE_AFTER_HORIZON")
            if result["incremental_present_value"] <= 0:
                reasons.append("NONPOSITIVE_INCREMENTAL_PRESENT_VALUE")
            if result["within_individual_budget"] is False:
                reasons.append("OVER_INDIVIDUAL_BUDGET")
            rows.append({**result, "status": "EXCLUDED" if reasons else "SIMULATION_ONLY", "reasons": reasons})
        rows.sort(key=lambda r: (-r["incremental_present_value"], r["id"]))
        scenarios.append({"horizon_days": horizon, "routes": rows})
    blockers = ["MARKET_EVIDENCE_NOT_VERIFIED", "RISK_POLICY_UNSET", "BATCH_ALLOCATION_NOT_IMPLEMENTED"]
    if budget is None:
        blockers.insert(0, "BUDGET_UNSET")
    return {
        "schema_version": 1, "simulation_only": True,
        "objective": "incremental_net_profit_subject_to_time_and_risk",
        "card": card, "currency": currency, "as_of": as_of,
        "raw_net": raw_net, "raw_present_value": raw_pv,
        "annual_discount_rate": discount, "budget": budget,
        "submission_ready": False, "allocation_blockers": blockers,
        "scenarios": scenarios,
    }
