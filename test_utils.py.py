"""
Unit tests for src/utils.py.

Run from the repository root with:

    pytest -q

These tests use tiny, hand-made DataFrames so they are fast and deterministic.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src.utils import (
    duplicate_report,
    flag_iqr_outliers,
    missing_values_report,
    replace_sentinels,
    standardise_text,
    to_numeric_safe,
)


# --------------------------------------------------------------------------- #
# 1. missing_values_report
# --------------------------------------------------------------------------- #
def test_missing_values_report_counts_and_sorts():
    df = pd.DataFrame(
        {
            "a": [1, 2, np.nan, np.nan],
            "b": [1, 2, 3, 4],
        }
    )
    rep = missing_values_report(df)

    # 'a' has 2/4 = 50% missing, 'b' has 0%.
    assert list(rep["column"]) == ["a", "b"]
    assert rep.loc[0, "n_missing"] == 2
    assert rep.loc[0, "pct_missing"] == 50.0
    assert rep.loc[1, "n_missing"] == 0


def test_missing_values_report_empty_df():
    rep = missing_values_report(pd.DataFrame())
    assert rep.empty
    assert list(rep.columns) == ["column", "n_missing", "pct_missing"]


# --------------------------------------------------------------------------- #
# 2. standardise_text
# --------------------------------------------------------------------------- #
def test_standardise_text_lower_strip_title():
    s = pd.Series(["  Western  Cape ", "GAUTENG", None, "kwazulu-natal"])
    out = standardise_text(s, lowercase=True, strip=True, title_case=True)

    assert out.iloc[0] == "Western Cape"
    assert out.iloc[1] == "Gauteng"
    assert pd.isna(out.iloc[2])
    assert out.iloc[3] == "Kwazulu-Natal"


def test_standardise_text_does_not_mutate_input():
    s = pd.Series(["  Male "])
    _ = standardise_text(s)
    assert s.iloc[0] == "  Male "  # original untouched


# --------------------------------------------------------------------------- #
# 3. flag_iqr_outliers
# --------------------------------------------------------------------------- #
def test_flag_iqr_outliers_basic():
    # Q1=20, Q3=40, IQR=20 -> fences 20-30=-10 and 40+30=70.
    s = pd.Series([10, 20, 30, 40, 50, 1000])
    mask = flag_iqr_outliers(s, k=1.5)

    assert mask.iloc[-1] is True or mask.iloc[-1] == True  # 1000 is an outlier
    assert not mask.iloc[:5].any()  # the rest are inside the fences


def test_flag_iqr_outliers_rejects_non_numeric():
    with pytest.raises(TypeError):
        flag_iqr_outliers(pd.Series(["a", "b"]))


def test_flag_iqr_outliers_treats_nan_as_false():
    s = pd.Series([1.0, 2.0, np.nan, 3.0])
    mask = flag_iqr_outliers(s)
    assert mask.iloc[2] == False


# --------------------------------------------------------------------------- #
# 4. duplicate_report
# --------------------------------------------------------------------------- #
def test_duplicate_report_counts():
    df = pd.DataFrame(
        {
            "id": [1, 2, 3, 1],
            "val": ["a", "b", "c", "a"],
        }
    )
    rep = duplicate_report(df)
    assert rep["n_rows"] == 4
    assert rep["n_duplicates"] == 1
    assert rep["n_unique_rows"] == 3


def test_duplicate_report_subset():
    df = pd.DataFrame(
        {
            "id": [1, 2, 3, 4],
            "val": ["a", "a", "b", "c"],
        }
    )
    rep = duplicate_report(df, subset=["val"])
    assert rep["n_duplicates"] == 1  # second 'a'


# --------------------------------------------------------------------------- #
# 5. to_numeric_safe
# --------------------------------------------------------------------------- #
def test_to_numeric_safe_coerces_and_nans():
    s = pd.Series(["1", "2.5", "abc", None, "-999"])
    out = to_numeric_safe(s)

    assert out.iloc[0] == 1.0
    assert out.iloc[1] == 2.5
    assert pd.isna(out.iloc[2])
    assert pd.isna(out.iloc[3])
    assert out.iloc[4] == -999.0


# --------------------------------------------------------------------------- #
# 6. replace_sentinels
# --------------------------------------------------------------------------- #
def test_replace_sentinels_default():
    s = pd.Series([10, -999, 20, 999999])
    out = replace_sentinels(s)

    assert out.iloc[0] == 10
    assert pd.isna(out.iloc[1])
    assert out.iloc[2] == 20
    assert pd.isna(out.iloc[3])


def test_replace_sentinels_custom():
    s = pd.Series([1, 0, 2])
    out = replace_sentinels(s, sentinels=(0,))
    assert pd.isna(out.iloc[1])
    assert out.iloc[0] == 1 and out.iloc[2] == 2
