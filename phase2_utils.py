"""
utils.py
--------
Reusable, single-purpose helper functions for the MzansiConnect project.

Design rules:
  - one job per function,
  - inputs are explicit arguments (no hidden globals),
  - functions RETURN new objects; they do not mutate their inputs,
  - every public function has type hints and a docstring.
"""

from __future__ import annotations

import logging
from typing import Iterable

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


# --------------------------------------------------------------------------- #
# 1. Missing-value report
# --------------------------------------------------------------------------- #
def missing_values_report(df: pd.DataFrame) -> pd.DataFrame:
    """
    Summarise missing values per column.

    Parameters
    ----------
    df : pd.DataFrame
        Any DataFrame.

    Returns
    -------
    pd.DataFrame
        Columns: `column`, `n_missing`, `pct_missing`, sorted by pct_missing
        descending. Empty DataFrame (with same columns) if df has no columns.
    """
    n_rows = len(df)
    report = pd.DataFrame(
        {
            "column": df.columns,
            "n_missing": [int(df[c].isna().sum()) for c in df.columns],
        }
    )
    report["pct_missing"] = (
        (report["n_missing"] / n_rows * 100).round(2) if n_rows else 0.0
    )
    return report.sort_values("pct_missing", ascending=False).reset_index(drop=True)


# --------------------------------------------------------------------------- #
# 2. Standardise text columns
# --------------------------------------------------------------------------- #
def standardise_text(
    series: pd.Series,
    *,
    lowercase: bool = True,
    strip: bool = True,
    title_case: bool = False,
) -> pd.Series:
    """
    Return a cleaned copy of a text Series (never mutates the input).

    Parameters
    ----------
    series : pd.Series
        Text-like Series. Non-string values become NaN.
    lowercase : bool, default True
        Lowercase before optional title-casing.
    strip : bool, default True
        Strip leading/trailing whitespace (and collapse internal runs to one space).
    title_case : bool, default False
        Apply title-case at the end (e.g. 'western cape' -> 'Western Cape').

    Returns
    -------
    pd.Series
        Cleaned Series with the same index.
    """
    out = series.astype("string").str.strip() if strip else series.astype("string")
    out = out.str.replace(r"\s+", " ", regex=True) if strip else out
    if lowercase:
        out = out.str.lower()
    if title_case:
        out = out.str.title()
    return out


# --------------------------------------------------------------------------- #
# 3. IQR outlier flagging
# --------------------------------------------------------------------------- #
def flag_iqr_outliers(
    series: pd.Series,
    *,
    k: float = 1.5,
) -> pd.Series:
    """
    Boolean mask flagging IQR outliers (Tukey's fences).

    Parameters
    ----------
    series : pd.Series
        Numeric Series. NaNs are treated as not-outliers (False).
    k : float, default 1.5
        Multiplier for the IQR. Use 3.0 for "extreme" outliers.

    Returns
    -------
    pd.Series
        Boolean Series, True where value is below Q1 - k*IQR or above Q3 + k*IQR.
    """
    if not pd.api.types.is_numeric_dtype(series):
        raise TypeError("flag_iqr_outliers requires a numeric Series")

    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower = q1 - k * iqr
    upper = q3 + k * iqr
    return (series < lower) | (series > upper)


# --------------------------------------------------------------------------- #
# 4. Duplicate report
# --------------------------------------------------------------------------- #
def duplicate_report(
    df: pd.DataFrame,
    subset: Iterable[str] | None = None,
) -> dict[str, int]:
    """
    Count exact duplicate rows.

    Parameters
    ----------
    df : pd.DataFrame
    subset : Iterable[str] | None
        Columns to consider. None = all columns.

    Returns
    -------
    dict
        {'n_duplicates': int, 'n_unique_rows': int, 'n_rows': int}
    """
    dup_mask = df.duplicated(subset=subset, keep="first")
    return {
        "n_rows": len(df),
        "n_duplicates": int(dup_mask.sum()),
        "n_unique_rows": int((~dup_mask).sum()),
    }


# --------------------------------------------------------------------------- #
# 5. Safe numeric coercion
# --------------------------------------------------------------------------- #
def to_numeric_safe(series: pd.Series) -> pd.Series:
    """
    Convert a Series to numeric, turning un-parseable values into NaN.

    Useful for messy columns with placeholders such as '-999' or 'n/a'.

    Parameters
    ----------
    series : pd.Series

    Returns
    -------
    pd.Series
        Float Series (NaN where conversion failed).
    """
    return pd.to_numeric(series, errors="coerce")


# --------------------------------------------------------------------------- #
# 6. Replace placeholder sentinel values
# --------------------------------------------------------------------------- #
def replace_sentinels(
    series: pd.Series,
    sentinels: Iterable[float] = (-999, -999.0, 999999),
) -> pd.Series:
    """
    Replace known placeholder values (e.g. -999) with NaN.

    Parameters
    ----------
    series : pd.Series
        Numeric or object Series.
    sentinels : Iterable[float]
        Values to treat as missing.

    Returns
    -------
    pd.Series
        Copy with sentinels replaced by NaN.
    """
    return series.replace(list(sentinels), np.nan)
