"""Command-line interface for Submission Cards."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict

from .collectr import CollectrValidationError, summarize_export


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="submission-cards")
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate = subparsers.add_parser("validate", help="validate a Collectr CSV")
    validate.add_argument("path", help="path to the Collectr export")
    return parser


def main() -> int:
    args = build_parser().parse_args()
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
