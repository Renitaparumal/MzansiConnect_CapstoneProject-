"""Tests for reusable data-quality helpers."""

import logging

import pandas as pd
import pytest
from pandas.testing import assert_frame_equal, assert_series_equal

from src.utils import (
    drop_rows_with_missing,
    flag_iqr_outliers,
    missing_value_report,
    remove_duplicate_rows,
    standardize_text_columns,
)


def test_missing_value_report_counts_and_percentages() -> None:
    frame = pd.DataFrame({"age": [20, None, 40], "plan": ["prepaid", None, None]})

    report = missing_value_report(frame)

    assert report.to_dict("records") == [
        {
            "column": "age",
            "missing_count": 1,
            "missing_percent": pytest.approx(100 / 3),
        },
        {
            "column": "plan",
            "missing_count": 2,
            "missing_percent": pytest.approx(200 / 3),
        },
    ]


def test_missing_value_report_empty_frame_has_zero_percentages() -> None:
    report = missing_value_report(pd.DataFrame(columns=["age"]))

    assert report.loc[0, "missing_count"] == 0
    assert report.loc[0, "missing_percent"] == 0


def test_standardize_text_columns_normalizes_without_mutating_input() -> None:
    original = pd.DataFrame({"plan": ["  PREPAID  ", "Post   paid", None]})

    result = standardize_text_columns(original, ["plan"])

    assert result["plan"].tolist()[:2] == ["prepaid", "post paid"]
    assert pd.isna(result.loc[2, "plan"])
    assert_frame_equal(
        original, pd.DataFrame({"plan": ["  PREPAID  ", "Post   paid", None]})
    )


def test_flag_iqr_outliers_marks_extreme_value_but_not_missing() -> None:
    frame = pd.DataFrame({"spend": [1.0, 2.0, 2.0, 3.0, 100.0, None]})

    result = flag_iqr_outliers(frame, "spend")

    assert_series_equal(
        result,
        pd.Series([False, False, False, False, True, False], name="spend"),
    )


def test_flag_iqr_outliers_rejects_non_numeric_column() -> None:
    with pytest.raises(TypeError, match="numeric dtype"):
        flag_iqr_outliers(pd.DataFrame({"plan": ["prepaid"]}), "plan")


def test_flag_iqr_outliers_requires_observed_values() -> None:
    with pytest.raises(ValueError, match="non-missing"):
        flag_iqr_outliers(pd.DataFrame({"spend": [None, None]}), "spend")


def test_remove_duplicate_rows_returns_copy_and_logs_removed_rows(
    caplog: pytest.LogCaptureFixture,
) -> None:
    frame = pd.DataFrame({"customer_id": [1, 1, 2], "plan": ["a", "a", "b"]})

    caplog.set_level(logging.INFO)
    result = remove_duplicate_rows(frame)

    assert len(result) == 2
    assert len(frame) == 3
    assert "Removed 1 duplicate rows" in caplog.text


def test_drop_rows_with_missing_required_values() -> None:
    frame = pd.DataFrame({"customer_id": [1, 2, 3], "age": [25, None, 40]})

    result = drop_rows_with_missing(frame, ["customer_id", "age"])

    assert result["customer_id"].tolist() == [1, 3]
    assert len(frame) == 3


def test_drop_rows_with_missing_requires_known_columns() -> None:
    with pytest.raises(KeyError, match="columns not found"):
        drop_rows_with_missing(pd.DataFrame({"age": [20]}), ["missing"])
