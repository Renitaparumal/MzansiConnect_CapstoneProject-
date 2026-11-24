src/data_validation.py

from typing import Any, Dict, List
import pandas as pd

from config.phase4_config import VALIDATION_BOUNDS


def validate_completeness(df: pd.DataFrame) -> Dict[str, float]:
    """Return missing-value percentage per column."""
    if df.empty:
        return {}
    return ((df.isna().sum() / len(df)) * 100).round(2).to_dict()


def validate_validity(datasets: Dict[str, pd.DataFrame]) -> Dict[str, int]:
    """Check logical bounds on age, usage, revenue, and satisfaction scores."""
    issues: Dict[str, int] = {}

    customers = datasets.get("customers")
    if customers is not None and "age" in customers.columns:
        invalid_age = customers[
            customers["age"].notna()
            & (
                (customers["age"] < VALIDATION_BOUNDS["age_min"])
                | (customers["age"] > VALIDATION_BOUNDS["age_max"])
            )
        ]
        issues["customers_invalid_age_count"] = int(len(invalid_age))

    usage = datasets.get("usage")
    if usage is not None:
        for col in ("data_gb", "voice_minutes", "sms_count", "revenue_zar"):
            if col in usage.columns:
                neg_count = int((usage[col].notna() & (usage[col] < 0)).sum())
                issues[f"usage_negative_{col}_count"] = neg_count

    tickets = datasets.get("tickets")
    if tickets is not None:
        if "resolution_hours" in tickets.columns:
            neg_res = int(
                (tickets["resolution_hours"].notna() & (tickets["resolution_hours"] < 0)).sum()
            )
            issues["tickets_negative_resolution_hours_count"] = neg_res
        if "satisfaction_score" in tickets.columns:
            bad_csat = int(
                (
                    tickets["satisfaction_score"].notna()
                    & (
                        (tickets["satisfaction_score"] < 1)
                        | (tickets["satisfaction_score"] > 5)
                    )
                ).sum()
            )
            issues["tickets_out_of_range_csat_count"] = bad_csat

    return issues


def validate_uniqueness(datasets: Dict[str, pd.DataFrame]) -> Dict[str, int]:
    """Check uniqueness of primary/event identifiers."""
    issues: Dict[str, int] = {}

    customers = datasets.get("customers")
    if customers is not None and "customer_id" in customers.columns:
        issues["customers_duplicate_customer_id"] = int(
            customers["customer_id"].duplicated().sum()
        )

    tickets = datasets.get("tickets")
    if tickets is not None and "ticket_id" in tickets.columns:
        issues["tickets_duplicate_ticket_id"] = int(
            tickets["ticket_id"].duplicated().sum()
        )

    return issues


def validate_timeliness(datasets: Dict[str, pd.DataFrame]) -> Dict[str, int]:
    """Ensure dates fall on or before the July 31, 2026 prediction boundary."""
    max_dt = pd.Timestamp(VALIDATION_BOUNDS["max_date"])
    issues: Dict[str, int] = {}

    for name, df in datasets.items():
        for col in ("signup_date", "created_date", "month"):
            if col in df.columns and pd.api.types.is_datetime64_any_dtype(df[col]):
                future_count = int((df[col].notna() & (df[col] > max_dt)).sum())
                issues[f"{name}_{col}_after_2026_07_31"] = future_count

    return issues


def validate_referential_integrity(datasets: Dict[str, pd.DataFrame]) -> Dict[str, int]:
    """Verify foreign keys (customer_id) exist in the master customers table."""
    issues: Dict[str, int] = {}
    customers = datasets.get("customers")

    if customers is None or "customer_id" not in customers.columns:
        return {"missing_master_customers_table": 1}

    valid_ids = set(customers["customer_id"].dropna())

    for child_name in ("usage", "tickets"):
        child_df = datasets.get(child_name)
        if child_df is not None and "customer_id" in child_df.columns:
            orphan_mask = child_df["customer_id"].notna() & (
                ~child_df["customer_id"].isin(valid_ids)
            )
            issues[f"{child_name}_orphan_customer_ids"] = int(orphan_mask.sum())

    return issues


def run_validation_suite(datasets: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
    """Execute all Phase 4 validation checks and return a summary report."""
    completeness = {
        name: validate_completeness(df) for name, df in datasets.items()
    }

    return {
        "row_counts": {name: int(len(df)) for name, df in datasets.items()},
        "completeness_missing_pct": completeness,
        "validity": validate_validity(datasets),
        "uniqueness": validate_uniqueness(datasets),
        "timeliness": validate_timeliness(datasets),
        "referential_integrity": validate_referential_integrity(datasets),
    }
