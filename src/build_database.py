"""Create data/processed/mzansiconnect.db from sql/schema.sql and the cleaned CSVs.

Run from the repo root (after src.clean_data):  python -m src.build_database
"""
import logging
import sqlite3

import pandas as pd

from src import data_loading as dl

log = logging.getLogger(__name__)

SCHEMA_FILE = dl.ROOT / "sql" / "schema.sql"


def prepare_tables() -> dict[str, pd.DataFrame]:
    """Load the cleaned CSVs and get them into the shape the schema expects."""
    customers, usage, tickets = dl.load_processed()

    customers["churned"] = (customers["churned"] == "Yes").astype(int)
    customers["age"] = customers["age"].astype("Int64")      # whole numbers, with NULLs

    usage["sms_count"] = usage["sms_count"].astype("Int64")

    tickets["resolved"] = (tickets["resolved"] == "Yes").astype(int)
    tickets["satisfaction_score"] = tickets["satisfaction_score"].astype("Int64")

    return {"customers": customers, "usage_monthly": usage, "support_tickets": tickets}


def build(db_path=dl.DB_PATH) -> None:
    tables = prepare_tables()

    if db_path.exists():
        db_path.unlink()        # start from scratch so reruns give the same file

    con = sqlite3.connect(db_path)
    try:
        con.executescript(SCHEMA_FILE.read_text(encoding="utf-8"))
        con.execute("PRAGMA foreign_keys = ON")      # off by default in SQLite, per connection

        # parents first, otherwise the foreign keys complain
        for name in ["customers", "usage_monthly", "support_tickets"]:
            tables[name].to_sql(name, con, if_exists="append", index=False)
            log.info("loaded %-16s %6d rows", name, len(tables[name]))
        con.commit()

        problems = con.execute("PRAGMA foreign_key_check").fetchall()
        if problems:
            raise RuntimeError(f"{len(problems)} foreign key violations, first: {problems[0]}")
        log.info("foreign key check passed, integrity: %s",
                 con.execute("PRAGMA integrity_check").fetchone()[0])
    finally:
        con.close()
    log.info("database written to %s", db_path)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    build()
