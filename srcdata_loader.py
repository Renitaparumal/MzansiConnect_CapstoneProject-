src/data_loader.py


from pathlib import Path
from typing import Dict
import pandas as pd


def load_csv_file(file_path: Path) -> pd.DataFrame:
    """Load a CSV file with normalized lowercase snake_case column names."""
    if not file_path.exists():
        raise FileNotFoundError(f"Expected input file not found: {file_path}")

    df = pd.read_csv(file_path, low_memory=False)
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    return df


def load_raw_datasets(file_paths: Dict[str, Path]) -> Dict[str, pd.DataFrame]:
    """Load core MzansiConnect datasets into a dictionary of DataFrames."""
    datasets: Dict[str, pd.DataFrame] = {}
    for name in ("customers", "usage", "tickets"):
        if name in file_paths and file_paths[name].exists():
            datasets[name] = load_csv_file(file_paths[name])
    return datasets
