"""
data_loading.py
---------------
Functions to load the raw MzansiConnect CSV files into pandas DataFrames.

Each loader:
  - reads from data/raw/ (the untouched originals),
  - returns a fresh DataFrame (never mutates global state),
  - logs how many rows were read.

Usage
-----
    from src.data_loading import load_customers, load_usage, load_tickets, load_dictionary
"""

from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

# --------------------------------------------------------------------------- #
# Logging
# --------------------------------------------------------------------------- #
logger = logging.getLogger(__name__)
if not logger.handlers:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

# --------------------------------------------------------------------------- #
# Paths (relative to the repository root)
# --------------------------------------------------------------------------- #
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"


# --------------------------------------------------------------------------- #
# Internal helper
# --------------------------------------------------------------------------- #
def _read_csv(filename: str) -> pd.DataFrame:
    """Read a CSV from data/raw/ and log the row count."""
    path = RAW_DIR / filename
    if not path.exists():
        raise FileNotFoundError(
            f"Raw file not found: {path}. "
            "Place the provided CSVs in data/raw/."
        )
    df = pd.read_csv(path)
    logger.info("Loaded %s: %d rows, %d columns", filename, len(df), df.shape[1])
    return df


# --------------------------------------------------------------------------- #
# Public loaders
# --------------------------------------------------------------------------- #
def load_customers() -> pd.DataFrame:
    """
    Load customers.csv (one row per customer).

    Returns
    -------
    pd.DataFrame
        Raw customer data. Includes the target column `churned`.
    """
    return _read_csv("customers.csv")


def load_usage() -> pd.DataFrame:
    """
    Load usage_monthly.csv (monthly usage/revenue per customer, Jan–Jun 2026).

    Returns
    -------
    pd.DataFrame
        Raw usage data. A customer may have 0–6 rows.
    """
    return _read_csv("usage_monthly.csv")


def load_tickets() -> pd.DataFrame:
    """
    Load support_tickets.csv (support tickets raised in the same period).

    Returns
    -------
    pd.DataFrame
        Raw ticket data. A customer may have 0–n tickets.
    """
    return _read_csv("support_tickets.csv")


def load_dictionary() -> pd.DataFrame:
    """
    Load data_dictionary.csv (column descriptions, types, examples).

    Returns
    -------
    pd.DataFrame
        The data dictionary. Read this before writing cleaning code.
    """
    return _read_csv("data_dictionary.csv")


if __name__ == "__main__":  # quick manual smoke test
    for loader in (load_customers, load_usage, load_tickets, load_dictionary):
        df = loader()
        print(f"{loader.__name__}: {df.shape}")