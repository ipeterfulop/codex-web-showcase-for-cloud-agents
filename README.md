# Sales normalizer

Internal Python utility for preparing messy sales CSV exports for downstream review and cleanup. The project provides a small command-line entry point, a canonical output schema, sample fixtures, and tests around the current transformation behavior.

## Quickstart

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
python -m src.prepare_sales_data \
  --input data/raw/sales_messy_sample.csv \
  --output data/output/sales_cleaned_preview.csv
```

## Current behavior

- Reads a single sales CSV export and writes a prepared CSV.
- Normalizes obvious header variations into the project schema.
- Trims surrounding whitespace from string fields.
- Emits a consistent output column order.
- Adds the `source_file` column for traceability.

## Canonical output schema

The prepared output is written with these columns:

- `order_id`
- `order_date`
- `customer_name`
- `amount`
- `currency`
- `status`
- `source_file`

## Project structure

```text
.
├── AGENTS.md                      # Setup, validation, and repo rules for future contributors/agents
├── data/
│   ├── expected/                  # Small expected-output samples for basic cases
│   └── raw/                       # Sample raw CSV exports
├── src/
│   ├── prepare_sales_data.py      # CLI and preparation pipeline
│   └── schema.py                  # Canonical schema helpers
├── tests/
│   ├── fixtures/                  # Test input files
│   └── test_prepare_sales_data.py # Baseline and pending-behavior tests
└── .github/workflows/test.yml     # CI for the test suite
```

## Validation

Run the full test suite:

```bash
pytest -q
```

Run the sample pipeline manually:

```bash
python -m src.prepare_sales_data \
  --input data/raw/sales_messy_sample.csv \
  --output data/output/sales_cleaned_preview.csv
```

## TODO

- Add robust deduplication for repeated `order_id` values.
- Normalize mixed date formats to a single output format.
- Parse messy amount strings and separate numeric amount from currency consistently.
- Standardize status values across exports.
- Define and document how malformed rows should be dropped or reported.
- Generate a lightweight data-quality summary alongside cleaned outputs.
