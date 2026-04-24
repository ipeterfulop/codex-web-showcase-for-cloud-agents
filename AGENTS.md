# AGENTS.md

This repository contains an internal Python utility for preparing messy sales CSV exports into a consistent reviewable format. Keep changes focused, keep behavior deterministic, and prefer small reviewable increments over broad rewrites.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Validation

Run the full test suite:

```bash
pytest -q
```

Run the sample cleaner manually:

```bash
python -m src.prepare_sales_data \
  --input data/raw/sales_messy_sample.csv \
  --output data/output/sales_cleaned_preview.csv
```

If you change parsing behavior, rerun both the tests and the sample command so docs, fixtures, and generated outputs stay aligned.

## Project Rules

- Keep tests deterministic and fully offline.
- Do not change unrelated files or reshape the repo without a clear need.
- Treat files in `tests/fixtures/` and `data/raw/` as stable realistic fixtures, not throwaway examples.
- Update `README.md` whenever user-visible behavior, commands, or project scope changes.
- Prefer small, explicit parsing logic over hidden magic.
- Preserve the canonical output schema unless there is a strong reason to change it and the change is reflected in code, tests, and docs.
- If you add output artifacts or reports, keep them reproducible from repo inputs and documented in `README.md`.

## Definition of Done

- The cleaner correctly handles the intended messy cases.
- Tests pass locally with `pytest -q`.
- Any new fixtures remain realistic, readable, and deterministic.
- Generated artifacts or reports are reproducible from checked-in inputs.
- `README.md` reflects any user-visible changes in behavior, commands, or outputs.
