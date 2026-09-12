# Repository instructions

## Scope

This repository evaluates card-routing decisions across RAW, COMC, PSA and CGC.

## Non-negotiable rules

- Never commit files from `data/private/` or `outputs/private/`.
- Never commit credentials, API keys or authenticated-session data.
- Match card identity by game, set, number, variant, language and condition.
- Match graded comps by grading company and grade.
- Use sold transactions for valuation; label active listings separately.
- Keep card-specific gem rate, sample size, liquidity and data date visible.
- Do not target an arbitrary number of eligible cards.
- Use `REVIEW_DATA` when evidence is insufficient; do not silently impute certainty.
- Treat a Collectr Near Mint label as inventory metadata, not a predicted grade.

## Workflow

- Read `README.md`, `docs/PROJECT_STATE.md` and `docs/METHODOLOGY.md` first.
- Make changes on a branch and submit a PR after the initial repository bootstrap.
- Run `PYTHONPATH=src python -m unittest discover -s tests -v` before publishing.
- Update `docs/PROJECT_STATE.md` whenever a milestone or decision rule changes.
- Do not publish scan results or personal inventory in GitHub.
