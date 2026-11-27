"""Run every query in sql/queries.sql against the database and show the results.

Run from the repo root:  python -m src.run_queries
Results are also saved as CSVs in reports/query_results/ so they can be
looked at without opening the database.
"""
import logging
import re
import sqlite3

import pandas as pd

from src import data_loading as dl

log = logging.getLogger(__name__)

QUERY_FILE = dl.ROOT / "sql" / "queries.sql"
RESULTS_DIR = dl.ROOT / "reports" / "query_results"


def split_queries(text: str) -> dict[str, str]:
    """Split the SQL file into {"Q1": "...", "Q5a": "...", "X1": "..."}."""
    parts = re.split(r"^-- (Q\d+[a-z]?|X\d+)\.", text, flags=re.MULTILINE)
    # parts = [preamble, name, body, name, body, ...]
    # the rest of the "-- Q1. title" line ends up at the start of body, so put its "--" back
    return {name: ("--" + body).strip() for name, body in zip(parts[1::2], parts[2::2])}


def is_select(sql: str) -> bool:
    no_comments = re.sub(r"--[^\n]*", "", sql).strip().upper()
    return no_comments.startswith(("SELECT", "WITH"))


def run_all(db_path=dl.DB_PATH) -> dict[str, pd.DataFrame]:
    results = {}
    con = sqlite3.connect(db_path)
    try:
        for name, sql in split_queries(QUERY_FILE.read_text(encoding="utf-8")).items():
            if is_select(sql):
                results[name] = pd.read_sql_query(sql, con)
                log.info("%s: %d rows", name, len(results[name]))
            else:
                con.executescript(sql)      # DDL, e.g. creating the view in Q12
                log.info("%s: ran DDL statements", name)
        con.commit()
    finally:
        con.close()
    return results


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    results = run_all()

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    pd.set_option("display.width", 160)
    pd.set_option("display.max_columns", 20)
    for name, df in results.items():
        df.to_csv(RESULTS_DIR / f"{name}.csv", index=False)
        print(f"\n=== {name} ({len(df)} rows) ===")
        print(df.head(12).to_string(index=False))


if __name__ == "__main__":
    main()
