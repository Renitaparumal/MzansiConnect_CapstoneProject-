run_phase4.py

import json
from pathlib import Path
import pandas as pd

from config.phase4_config import FILE_PATHS, PROCESSED_DATA_DIR, REPORTS_DIR
from src.data_cleaning import clean_datasets
from src.data_loader import load_raw_datasets
from src.data_validation import run_validation_suite


def save_outputs(
    cleaned_datasets: dict[str, pd.DataFrame],
    cleaning_logs: list[str],
    validation_report: dict,
) -> None:
    """Save cleaned CSVs, cleaning log, and validation report."""
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    for name, df in cleaned_datasets.items():
        output_file = PROCESSED_DATA_DIR / f"{name}_clean.csv"
        df.to_csv(output_file, index=False)

    log_path: Path = REPORTS_DIR / "phase4_cleaning_log.txt"
    log_path.write_text("\n".join(cleaning_logs), encoding="utf-8")

    report_path: Path = REPORTS_DIR / "phase4_validation_report.json"
    report_path.write_text(json.dumps(validation_report, indent=2), encoding="utf-8")


def main() -> None:
    raw_datasets = load_raw_datasets(FILE_PATHS)
    cleaned_datasets, cleaning_logs = clean_datasets(raw_datasets)
    validation_report = run_validation_suite(cleaned_datasets)
    save_outputs(cleaned_datasets, cleaning_logs, validation_report)

    print("Phase 4 completed successfully.")
    print("Validation summary:", json.dumps(validation_report, indent=2))


if __name__ == "__main__":
    main()
