"""Checks on the SQLite database and the queries in sql/queries.sql.

Most tests compare a SQL answer with the same number worked out in pandas
from the cleaned CSVs, so a mistake in either one shows up.
"""
import shutil
import sqlite3
import tempfile
from pathlib import Path

import pandas as pd

from src import data_loading as dl
from src import run_queries

_cache = {}


def results() -> dict:
    """Run all queries once against a throwaway copy of the database."""
    if "results" not in _cache:
        tmp = Path(tempfile.mkdtemp()) / "test.db"
        shutil.copy(dl.DB_PATH, tmp)
        _cache["results"] = run_queries.run_all(tmp)
        _cache["db"] = tmp
    return _cache["results"]


def connect() -> sqlite3.Connection:
    results()
    return sqlite3.connect(_cache["db"])


def cleaned():
    return dl.load_processed()


def test_row_counts_match_cleaned_csvs():
    customers, usage, tickets = cleaned()
    con = connect()
    for table, df in [("customers", customers), ("usage_monthly", usage), ("support_tickets", tickets)]:
        n = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        assert n == len(df), table


def test_no_foreign_key_violations_and_unique_keys():
    con = connect()
    assert con.execute("PRAGMA foreign_key_check").fetchall() == []
    n, n_unique = con.execute("SELECT COUNT(*), COUNT(DISTINCT customer_id) FROM customers").fetchone()
    assert n == n_unique


def test_foreign_keys_actually_reject_orphans():
    con = connect()
    con.execute("PRAGMA foreign_keys = ON")
    try:
        con.execute("INSERT INTO support_tickets VALUES ('T-X', 'NOBODY', '2026-01-01', 'Billing', 1.0, 1, 3)")
        raised = False
    except sqlite3.IntegrityError:
        raised = True
    assert raised


def test_q1_matches_pandas():
    customers, _, _ = cleaned()
    row = results()["Q1"].iloc[0]
    assert row["total_customers"] == len(customers)
    assert row["churned_customers"] == (customers["churned"] == "Yes").sum()
    assert row["churn_pct"] == round(100 * (customers["churned"] == "Yes").mean(), 1)


def test_q3_leaves_out_small_provinces():
    customers, _, _ = cleaned()
    sizes = customers["province"].value_counts()
    small = set(sizes[sizes < 200].index)
    assert small                                   # Northern Cape is under 200
    assert not small & set(results()["Q3"]["province"])
    assert len(results()["Q3"]) == 3


def test_q4_arpu_matches_pandas():
    customers, usage, _ = cleaned()
    per_customer = usage.groupby("customer_id")["revenue_zar"].mean()
    expected = customers.set_index("customer_id").join(per_customer).groupby("plan_type")["revenue_zar"].mean()
    got = results()["Q4"].set_index("plan_type")["arpu_zar"]
    for plan, value in expected.items():
        assert abs(got[plan] - value) < 0.01


def test_q5_ticket_groups_add_up_and_match_pandas():
    customers, _, tickets = cleaned()
    q5 = results()["Q5a"].set_index("ticket_group")
    assert q5["customers"].sum() == len(customers)
    counts = tickets.groupby("customer_id").size()
    heavy = counts[counts > 3].index
    assert q5.loc["More than 3 tickets", "customers"] == len(heavy)
    assert len(results()["Q5b"]) == len(heavy)


def test_q6_ignores_null_scores():
    customers, _, tickets = cleaned()
    merged = tickets.merge(customers[["customer_id", "churned"]], on="customer_id")
    expected = merged.groupby("churned")["satisfaction_score"].mean()
    got = results()["Q6"].set_index("status")["avg_satisfaction"]
    assert abs(got["Churned"] - expected["Yes"]) < 0.01
    assert abs(got["Retained"] - expected["No"]) < 0.01


def test_q8_gives_five_per_province():
    q8 = results()["Q8"]
    assert q8.groupby("province").size().max() <= 5
    assert q8["province"].nunique() == 9


def test_q9_running_total_ends_at_total_revenue():
    _, usage, _ = cleaned()
    q9 = results()["Q9"]
    assert abs(q9["running_total_zar"].iloc[-1] - usage["revenue_zar"].sum()) < 0.5
    assert q9["running_total_zar"].is_monotonic_increasing


def test_q11_matches_a_pandas_version_of_the_same_rule():
    _, usage, _ = cleaned()
    usage = usage.dropna(subset=["data_gb"]).copy()
    usage["month_no"] = usage["month"].str[:4].astype(int) * 12 + usage["month"].str[5:].astype(int)
    flagged = set()
    for cust, g in usage.sort_values("month_no").groupby("customer_id"):
        vals = dict(zip(g["month_no"], g["data_gb"]))
        for m in vals:
            if all(k in vals for k in (m - 1, m - 2, m - 3)):
                if vals[m] < vals[m - 1] < vals[m - 2] < vals[m - 3]:
                    flagged.add(cust)
    assert set(results()["Q11"]["customer_id"]) == flagged


def test_view_has_one_row_per_customer_and_no_inflated_revenue():
    customers, usage, tickets = cleaned()
    con = connect()
    view = pd.read_sql_query("SELECT * FROM customer_summary", con)
    assert len(view) == len(customers)
    assert abs(view["total_revenue_zar"].sum() - usage["revenue_zar"].sum()) < 0.5
    assert view["ticket_count"].sum() == len(tickets)
    assert "cancellation_reason" not in view.columns       # leakage kept out on purpose


def test_joining_both_child_tables_at_once_inflates_revenue():
    x1 = results()["X1"].iloc[0]
    assert x1["naive_total_revenue"] > x1["correct_total_revenue"]


def test_index_exists_and_is_used():
    con = connect()
    names = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type = 'index'")}
    assert {"idx_tickets_customer", "idx_usage_month"} <= names
    plan = con.execute(
        "EXPLAIN QUERY PLAN SELECT * FROM support_tickets WHERE customer_id = 'CUST00009'").fetchall()
    assert any("idx_tickets_customer" in str(step) for step in plan)


def test_all_queries_were_found():
    expected = {"Q1", "Q2", "Q3", "Q4", "Q5a", "Q5b", "Q6", "Q7", "Q8", "Q9", "Q10", "Q11", "Q12", "Q12b", "X1"}
    text = run_queries.QUERY_FILE.read_text(encoding="utf-8")
    assert set(run_queries.split_queries(text)) == expected
