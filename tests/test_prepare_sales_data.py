from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from src.prepare_sales_data import prepare_sales_data
from src.schema import canonical_columns


FIXTURES_DIR = Path(__file__).parent / "fixtures"
EXPECTED_DIR = Path(__file__).resolve().parents[1] / "data" / "expected"


def test_prepare_sales_data_writes_canonical_schema_for_simple_input(tmp_path: Path) -> None:
    input_path = FIXTURES_DIR / "basic_sales_input.csv"
    output_path = tmp_path / "basic_sales_output.csv"

    result = prepare_sales_data(input_path, output_path)
    expected = pd.read_csv(EXPECTED_DIR / "basic_sales_expected.csv", dtype=str, keep_default_na=False)

    assert output_path.exists()
    assert list(result.columns) == canonical_columns()
    pd.testing.assert_frame_equal(result, expected)


def test_prepare_sales_data_trims_whitespace_and_sets_source_file(tmp_path: Path) -> None:
    input_path = FIXTURES_DIR / "sales_messy_sample.csv"
    output_path = tmp_path / "messy_output.csv"

    result = prepare_sales_data(input_path, output_path)

    first_customer = result.loc[result["order_id"] == "1008", "customer_name"].iloc[0]
    first_status = result.loc[result["order_id"] == "1003", "status"].iloc[0]

    assert first_customer == "Grace Kim"
    assert first_status == "SHIPPED"
    assert set(result["source_file"]) == {"sales_messy_sample.csv"}


@pytest.mark.xfail(reason="Deduplication by order_id is not implemented yet.", strict=True)
def test_prepare_sales_data_deduplicates_order_ids(tmp_path: Path) -> None:
    input_path = FIXTURES_DIR / "sales_messy_sample.csv"
    output_path = tmp_path / "deduped_output.csv"

    result = prepare_sales_data(input_path, output_path)

    assert result["order_id"].value_counts().max() == 1


@pytest.mark.xfail(reason="Dates, amounts, and statuses are not normalized yet.", strict=True)
def test_prepare_sales_data_normalizes_dates_amounts_and_statuses(tmp_path: Path) -> None:
    input_path = FIXTURES_DIR / "sales_messy_sample.csv"
    output_path = tmp_path / "normalized_output.csv"

    result = prepare_sales_data(input_path, output_path).set_index("order_id")

    assert result.loc["1001", "order_date"] == "2024-01-05"
    assert result.loc["1002", "amount"] == "45.00"
    assert result.loc["1007", "status"] == "cancelled"
