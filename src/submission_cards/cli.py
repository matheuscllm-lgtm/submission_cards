"""Command-line interface for Submission Cards."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from dataclasses import asdict

from .collectr import CollectrValidationError, summarize_export
from .scenarios import ScenarioValidationError, compare_scenarios


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="submission-cards")
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate = subparsers.add_parser("validate", help="validate a Collectr CSV")
    validate.add_argument("path", help="path to the Collectr export")
    compare = subparsers.add_parser("compare", help="simulate supplied routes at 90/180/365 days")
    compare.add_argument("path", help="normalized scenario JSON for one copy")
    compare.add_argument("--output", required=True, help="private destination for the comparison JSON")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "compare":
        try:
            source = Path(args.path)
            destination = Path(args.output)
            if source.resolve() == destination.resolve():
                raise ScenarioValidationError("Output must not overwrite the input")
            result = compare_scenarios(json.loads(source.read_text(encoding="utf-8-sig")))
            encoded = json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False)
            destination.parent.mkdir(parents=True, exist_ok=True)
            with destination.open("x", encoding="utf-8") as handle:
                handle.write(encoded + "\n")
        except (ScenarioValidationError, OSError, UnicodeError, ValueError, OverflowError) as exc:
            print(json.dumps({"ok": False, "error": type(exc).__name__}))
            return 2
        print(json.dumps({"ok": True, "simulation_only": True}))
        return 0
    if args.command == "validate":
        try:
            summary = summarize_export(args.path)
        except (CollectrValidationError, OSError, UnicodeError) as exc:
            print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
            return 2
        print(json.dumps({"ok": True, **asdict(summary)}, ensure_ascii=False, indent=2))
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
