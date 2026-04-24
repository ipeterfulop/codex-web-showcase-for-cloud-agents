from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from .schema import ensure_canonical_columns, reorder_to_canonical

HEADER_ALIASES = {
    "order_id": "order_id",
    "orderid": "order_id",
    "order_date": "order_date",
    "orderdate": "order_date",
    "customer_name": "customer_name",
    "customer": "customer_name",
    "customername": "customer_name",
    "amount": "amount",
    "amount_paid": "amount",
    "amountpaid": "amount",
    "currency": "currency",
    "status": "status",
}


def normalize_header(header: str) -> str:
    normalized = header.strip().lower()
    for token in (" ", "-", "/", "."):
        normalized = normalized.replace(token, "_")
    while "__" in normalized:
        normalized = normalized.replace("__", "_")
    return HEADER_ALIASES.get(normalized.strip("_"), normalized.strip("_"))


def strip_string_values(frame: pd.DataFrame) -> pd.DataFrame:
    cleaned = frame.copy()
    for column in cleaned.columns:
        cleaned[column] = cleaned[column].map(lambda value: value.strip() if isinstance(value, str) else value)
    return cleaned


def prepare_sales_data(input_path: str | Path, output_path: str | Path) -> pd.DataFrame:
    input_path = Path(input_path)
    output_path = Path(output_path)

    frame = pd.read_csv(input_path, dtype=str, keep_default_na=False)
    frame = frame.rename(columns={column: normalize_header(column) for column in frame.columns})
    frame = strip_string_values(frame)
    frame = ensure_canonical_columns(frame)
    frame["source_file"] = input_path.name
    frame = reorder_to_canonical(frame)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(output_path, index=False)
    return frame


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Prepare messy sales CSV data for later cleanup work.")
    parser.add_argument("--input", required=True, help="Path to the raw CSV export.")
    parser.add_argument("--output", required=True, help="Path to write the prepared CSV.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    prepare_sales_data(args.input, args.output)


if __name__ == "__main__":
    main()
