"""Tests for raw CSV loaders."""

import logging
from pathlib import Path
from typing import Callable

import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from src.data_loading import (
    load_customers,
    load_support_tickets,
    load_usage_monthly,
)


@pytest.mark.parametrize(
    ("filename", "loader"),
    [
        ("customers.csv", load_customers),
        ("usage_monthly.csv", load_usage_monthly),
        ("support_tickets.csv", load_support_tickets),
    ],
)
def test_loaders_read_csv_and_log_row_count(
    tmp_path: Path,
    caplog: pytest.LogCaptureFixture,
    filename: str,
    loader: Callable[[Path], pd.DataFrame],
) -> None:
    expected = pd.DataFrame({"customer_id": [1, 2]})
    expected.to_csv(tmp_path / filename, index=False)

    with caplog.at_level(logging.INFO):
        result = loader(tmp_path)

    assert_frame_equal(result, expected)
    assert f"Read 2 rows from {tmp_path / filename}" in caplog.text


def test_loader_surfaces_missing_file_error(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        load_customers(tmp_path)
