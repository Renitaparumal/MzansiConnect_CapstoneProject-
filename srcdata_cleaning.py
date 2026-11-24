src/data_cleaning.py

from typing import Dict, List, Tuple
import numpy as np
import pandas as pd

from config.phase4_config import BINARY_MAP, PLACEHOLDER_VALUES, PLAN_TYPE_MAP, PROVINCE_MAP


class CleaningTracker:
    """Collects human-readable audit entries during data cleaning."""

    def __init__(self) -> None:
        self.logs: List[str] = []

    def record(self, message: str) -> None:
        self.logs.append(message)


def replace_placeholders(df: pd.DataFrame, tracker: CleaningTracker, dataset_name: str) -> pd.DataFrame:
    """Replace sentinel/placeholder values such as -999 with NaN."""
    df = df.copy()
    replaced_count = 0

    for col in df.columns:
        mask = df[col].isin(PLACEHOLDER_VALUES)
        count = int(mask.sum())
        if count > 0:
            df.loc[mask, col] = np.nan
            replaced_count += count

    tracker.record(f"[{dataset_name}] Replaced {replaced_count} placeholder entries with NaN.")
    return df


def remove_exact_duplicates(
    df: pd.DataFrame,
    tracker: CleaningTracker,
    dataset_name: str,
    subset_cols: List[str] | None = None,
) -> pd.DataFrame:
    """Remove exact duplicate rows (or duplicates on a specified key subset)."""
    df = df.copy()
    before_rows = len(df)
    df = df.drop_duplicates(subset=subset_cols, keep="first")
    removed = before_rows - len(df)
    tracker.record(f"[{dataset_name}] Removed {removed} duplicate rows ({len(df)} remaining).")
    return df


def standardize_text_and_categories(
    df: pd.DataFrame, tracker: CleaningTracker, dataset_name: str
) -> pd.DataFrame:
    """Standardize string whitespace, casing, provinces, plan types, and binary indicators."""
    df = df.copy()

    obj_cols = df.select_dtypes(include=["object", "string"]).columns
    for col in obj_cols:
        df[col] = df[col].astype("string").str.strip()

    if "province" in df.columns:
        df["province"] = (
            df["province"]
            .str.lower()
            .map(PROVINCE_MAP)
            .fillna(df["province"].str.title())
        )
        tracker.record(f"[{dataset_name}] Standardized 'province' categories.")

    if "plan_type" in df.columns:
        df["plan_type"] = (
            df["plan_type"]
            .str.lower()
            .map(PLAN_TYPE_MAP)
            .fillna(df["plan_type"].str.title())
        )
        tracker.record(f"[{dataset_name}] Standardized 'plan_type' categories.")

    for binary_col in ("churned", "dropped_call_complaint", "resolved"):
        if binary_col in df.columns:
            mapped = df[binary_col].str.lower().map(BINARY_MAP)
            df[binary_col] = mapped.where(mapped.notna(), df[binary_col])
            tracker.record(f"[{dataset_name}] Normalized binary column '{binary_col}'.")

    return df


def parse_dates_and_numerics(
    df: pd.DataFrame, tracker: CleaningTracker, dataset_name: str
) -> pd.DataFrame:
    """Convert date strings to datetime and numeric columns to numeric types safely."""
    df = df.copy()

    for date_col in ("signup_date", "created_date", "month"):
        if date_col in df.columns:
            df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
            tracker.record(f"[{dataset_name}] Parsed '{date_col}' as datetime.")

    numeric_candidates = [
        "age",
        "contract_months",
        "data_gb",
        "voice_minutes",
        "revenue_zar",
        "sms_count",
        "resolution_hours",
        "satisfaction_score",
    ]
    for num_col in numeric_candidates:
        if num_col in df.columns:
            df[num_col] = pd.to_numeric(df[num_col], errors="coerce")

    return df


def clean_datasets(
    datasets: Dict[str, pd.DataFrame],
) -> Tuple[Dict[str, pd.DataFrame], List[str]]:
    """Run all Phase 4 cleaning steps across loaded datasets."""
    tracker = CleaningTracker()
    cleaned: Dict[str, pd.DataFrame] = {}

    for name, df in datasets.items():
        step_df = replace_placeholders(df, tracker, name)
        step_df = remove_exact_duplicates(step_df, tracker, name)
        step_df = standardize_text_and_categories(step_df, tracker, name)
        step_df = parse_dates_and_numerics(step_df, tracker, name)

        if name == "customers" and "customer_id" in step_df.columns:
            step_df = step_df.dropna(subset=["customer_id"])
            step_df = remove_exact_duplicates(
                step_df, tracker, name, subset_cols=["customer_id"]
            )

        cleaned[name] = step_df

    return cleaned, tracker.logs
