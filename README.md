# MzansiConnect — Design Choices (README)

> This section documents the engineering decisions behind `src/data_loading.py` and `src/utils.py` so the marker can see the choices were deliberate, not copied.

---

## Design Choices — `src/data_loading.py` and `src/utils.py`

### Guiding principles

1. **One job per function.** Every helper does exactly one thing and its name says what that is. If a name needed "and", the function was split.
2. **Return, never mutate.** Every function returns a new object; the caller keeps the original for auditing and rollback. This also makes each function trivially unit-testable on a small hand-made DataFrame.
3. **Explicit inputs, no hidden globals.** All data enters as arguments. No function reaches into a global DataFrame, so behaviour is predictable and reproducible.
4. **Flag, don't delete.** Cleaning helpers *report* or *mark* problems (missingness, outliers, duplicates, sentinels) and leave the decision to the cleaning notebook, where it is logged with a justification. This keeps the Phase 4 cleaning log honest and reviewable.
5. **Log, don't print.** Loaders and helpers use the `logging` module so row counts appear in a timestamped, levelled stream that can be redirected to a file. `print` disappears the moment you run headless.

---

### `src/data_loading.py`

| Function | What it does | Why it exists |
|---|---|---|
| `_read_csv` | Reads a file from `data/raw/`, raises a clear error if missing, logs row/column counts. | One choke-point for all reads means one place to enforce "never edit raw files" and one place that logs provenance. |
| `load_customers` / `load_usage` / `load_tickets` / `load_dictionary` | Thin, named wrappers. | Callers read as English (`load_customers()`), and a future schema change touches one function, not every notebook. |

**Path handling:** paths are resolved relative to the module file (`Path(__file__).resolve().parent.parent`), so the loaders work no matter which directory you launch Jupyter or pytest from. Hard-coded relative paths break as soon as the working directory changes.

**Why a `FileNotFoundError` with a helpful message:** a missing raw file is an environment problem, not a data problem. Failing fast with "place the CSVs in data/raw/" saves the grader ten minutes of guessing.

---

### `src/utils.py`

| Function | Single job | Data issue it guards against (from the brief) | Trade-off accepted |
|---|---|---|---|
| `missing_values_report` | Count and rank missingness per column. | "Missing values in several columns, and the *reason* for missingness may matter." | Reports only — no imputation. Imputation is a modelling decision that belongs in Phase 4 with a written justification, not in a helper. |
| `standardise_text` | One text-cleanup pipeline; returns a copy. | Inconsistent spellings/capitalisation: `western cape`, `WC`, `GAUTENG `, `male`/`MALE`/`M` in `customers.csv`. | Optional `title_case` because some columns (e.g. `gender`) are better left lower-case; the caller chooses. Non-strings become `NaN` (via `astype("string")`) rather than raising, so mixed columns don't crash a notebook. |
| `flag_iqr_outliers` | Boolean mask using Tukey's fences. | "Impossible or suspicious values (ages, negative or extreme usage)." | Flags rather than removes, because a very large data-usage value can be a legitimate heavy user — the brief explicitly warns to check surrounding months before deleting. `k=3.0` is available for "extreme" outliers. Raises `TypeError` on non-numeric input so mistakes surface early. NaNs return `False` (not-outlier) to keep the mask usable in filters. |
| `duplicate_report` | Count exact duplicate rows, optionally on a column subset. | "Exact duplicate customer rows." in `customers.csv`. | Counts only. Dropping duplicates is deferred to Phase 4 because you must first confirm they are true duplicates (same `customer_id`) and not coincidental matches. The `subset` argument lets you check duplicates on `customer_id` alone later. |
| `to_numeric_safe` | Coerce to numeric, un-parseable → `NaN`. | Placeholder/mixed values that break arithmetic. | Deliberately does **not** strip sentinels — that is a separate, explicit step (`replace_sentinels`) so the two decisions are logged independently. |
| `replace_sentinels` | Map known placeholders (default `-999`, `999999`) to `NaN`. | "Treat placeholder values such as -999 correctly" in `usage_monthly.csv`. | Defaults are a starting point, not gospel; the cleaning notebook passes the sentinels it actually finds in `value_counts()`. Kept separate from coercion so "we saw a sentinel" and "it was text" are two distinct, auditable facts. |

**Why `missing_values_report` returns `pct_missing` rounded to 2 dp:** percentages are for humans reading a report; keeping full precision would clutter the Phase 4 cleaning log. The raw counts are kept alongside for exactness.

**Why `standardise_text` collapses internal whitespace:** `"Western  Cape"` (double space) and `"Western Cape"` should map to the same category. Without collapsing, `value_counts()` would show them as separate groups and hide the problem.

---

### Testing approach (`tests/test_utils.py`)

- **Small, hand-made DataFrames.** Each test builds the smallest input that exercises the behaviour, so failures point at the function, not at a 6,000-row fixture.
- **One behaviour per test.** Six functions, nine tests — enough to cover the happy path, the empty/degenerate case (`missing_values_report` on an empty frame), the error path (`flag_iqr_outliers` on text), and the "don't mutate the input" guarantee.
- **Edge cases that mirror the real data:** `None` in text, `np.nan` in numerics, `-999` and `999999` sentinels, and a clear IQR outlier (`1000` against `10–50`).
- **Deterministic.** No random data, no I/O — the suite runs in milliseconds and never depends on the CSVs being present.

---

### Checkpoint answers (Phase 2)

**Why is a virtual environment important when sharing a project?**
It pins the exact library versions in `requirements.txt`, so a grader who clones the repo runs the same `pandas`/`scikit-learn` behaviour you did. Without it, a global upgrade can silently change parsing, sorting or model defaults and your results stop reproducing. It also isolates the project from unrelated packages on your machine, so a conflicting dependency elsewhere can't break your pipeline.

**What is the difference between a function that returns a DataFrame and one that modifies it in place? Which is safer?**
A returning function produces a **new** object and leaves the caller's DataFrame untouched; an in-place function (`df.drop(..., inplace=True)`) mutates the caller's object as a side effect. Returning is safer: the original survives for auditing and rollback, the function is trivially unit-testable (assert on the return value), and pipelines compose cleanly (`df = clean(df)`). In-place mutation hides state changes, makes debugging harder, and is a common source of "why did my raw data change?" bugs. **All helpers in `src/utils.py` return and never mutate.**

---

### Repository structure (Phase 2)
