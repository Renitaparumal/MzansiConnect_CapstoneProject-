"""Load raw MzansiConnect CSV tables."""

import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)
DEFAULT_RAW_DATA_DIR = Path("data/raw")


def _load_csv(filename: str, data_dir: Path) -> pd.DataFrame:
    """Read one CSV from the raw-data directory and log its row count."""
    path = data_dir / filename
    frame = pd.read_csv(path)
    logger.info("Read %d rows from %s", len(frame), path)
    return frame


def load_customers(data_dir: Path = DEFAULT_RAW_DATA_DIR) -> pd.DataFrame:
    """Load the customer table from ``customers.csv``."""
    return _load_csv("customers.csv", data_dir)


def load_usage_monthly(data_dir: Path = DEFAULT_RAW_DATA_DIR) -> pd.DataFrame:
    """Load monthly subscriber activity from ``usage_monthly.csv``."""
    return _load_csv("usage_monthly.csv", data_dir)


def load_support_tickets(data_dir: Path = DEFAULT_RAW_DATA_DIR) -> pd.DataFrame:
    """Load support interactions from ``support_tickets.csv``."""
    return _load_csv("support_tickets.csv", data_dir)
