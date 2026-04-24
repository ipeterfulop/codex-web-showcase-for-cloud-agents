from __future__ import annotations

import pandas as pd

CANONICAL_COLUMNS = [
    "order_id",
    "order_date",
    "customer_name",
    "amount",
    "currency",
    "status",
    "source_file",
]


def canonical_columns() -> list[str]:
    return list(CANONICAL_COLUMNS)


def ensure_canonical_columns(frame: pd.DataFrame) -> pd.DataFrame:
    for column in CANONICAL_COLUMNS:
        if column not in frame.columns:
            frame[column] = ""
    return frame


def reorder_to_canonical(frame: pd.DataFrame) -> pd.DataFrame:
    ordered = ensure_canonical_columns(frame.copy())
    return ordered[CANONICAL_COLUMNS]
