"""Reusable, non-mutating data-quality helpers."""

import logging
import math
from typing import Literal, Sequence

import pandas as pd
from pandas.api.types import is_numeric_dtype

logger = logging.getLogger(__name__)


def missing_value_report(frame: pd.DataFrame) -> pd.DataFrame:
    """Return missing-value counts and percentages for each column."""
    missing_count = frame.isna().sum()
    missing_percent = frame.isna().mean().mul(100).fillna(0.0)
    report = pd.DataFrame(
        {
            "column": frame.columns,
            "missing_count": missing_count.to_numpy(),
            "missing_percent": missing_percent.to_numpy(),
        }
    )
    logger.info("Reported missing values across %d rows", len(frame))
    return report


def standardize_text_columns(
    frame: pd.DataFrame, columns: Sequence[str]
) -> pd.DataFrame:
    """Return a copy with selected text columns trimmed and lower-cased."""
    result = frame.copy(deep=True)
    for column in columns:
        result[column] = (
            result[column]
            .astype("string")
            .str.strip()
            .str.replace(r"\s+", " ", regex=True)
            .str.lower()
        )
    logger.info(
        "Standardized %d text columns across %d rows", len(columns), len(frame)
    )
    return result


def flag_iqr_outliers(
    frame: pd.DataFrame, column: str, multiplier: float = 1.5
) -> pd.Series:
    """Return a Boolean mask for values outside the column's IQR fences.

    Missing values are not flagged. The input column must be numeric and
    contain at least one non-missing value.
    """
    if not math.isfinite(multiplier) or multiplier <= 0:
        raise ValueError("multiplier must be a finite number greater than zero")

    values = frame[column]
    if values.notna().sum() == 0:
        raise ValueError(f"column {column!r} has no non-missing values")
    if not is_numeric_dtype(values):
        raise TypeError(f"column {column!r} must have a numeric dtype")

    first_quartile = values.quantile(0.25)
    third_quartile = values.quantile(0.75)
    spread = third_quartile - first_quartile
    lower_fence = first_quartile - multiplier * spread
    upper_fence = third_quartile + multiplier * spread
    outliers = (values.lt(lower_fence) | values.gt(upper_fence)).fillna(False)
    logger.info(
        "Flagged %d outlier rows from %d rows in column %s",
        int(outliers.sum()),
        len(frame),
        column,
    )
    return outliers


def remove_duplicate_rows(
    frame: pd.DataFrame,
    subset: Sequence[str] | None = None,
    keep: Literal["first", "last", False] = "first",
) -> pd.DataFrame:
    """Return a copy without duplicate rows and log the number removed."""
    result = frame.drop_duplicates(subset=subset, keep=keep)
    logger.info("Removed %d duplicate rows", len(frame) - len(result))
    return result


def drop_rows_with_missing(
    frame: pd.DataFrame, subset: Sequence[str]
) -> pd.DataFrame:
    """Return a copy without rows missing any of the required columns."""
    if not subset:
        raise ValueError("subset must contain at least one column")

    missing_columns = [column for column in subset if column not in frame.columns]
    if missing_columns:
        raise KeyError(f"columns not found: {missing_columns}")

    result = frame.dropna(subset=list(subset))
    logger.info("Removed %d rows missing required values", len(frame) - len(result))
    return result
