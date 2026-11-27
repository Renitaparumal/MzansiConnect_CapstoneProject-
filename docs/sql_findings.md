# Phase 5: what the SQL says

All numbers come from `sql/queries.sql`, run against `data/processed/mzansiconnect.db`
(6,000 customers, 34,920 usage rows, 3,493 tickets). The raw output of every query is saved in
`reports/query_results/`. These are descriptive counts and rates, not proof of cause.

## Answers to the twelve business questions

**Q1. Size and churn.** 6,000 customers, 1,261 churned, so **21.0%** churn. About one in five, which matches the brief.

**Q2. Plan and contract.** Contract length is the clearest split so far.

| Plan | Contract | Customers | Churn |
| --- | --- | ---: | ---: |
| Hybrid | No contract | 576 | 31.6% |
| Prepaid | No contract | 3,323 | 24.7% |
| Postpaid | 12 months | 924 | 13.6% |
| Hybrid | 12 months | 336 | 12.2% |
| Postpaid | 24 months | 841 | 10.8% |

Every prepaid customer is on no contract, so for prepaid "plan" and "contract" can't be separated.
No-contract customers churn at roughly 2 to 3 times the rate of contract customers.

**Q3. Provinces.** Eastern Cape (24.0%), North West (23.3%), Limpopo (21.7%).
The 200-customer rule matters here: Northern Cape has only 193 customers and a 21.8% churn rate, which would
have put it third ahead of Limpopo. With under 200 customers a rate that size is not very stable, which is
the reason for the cutoff, but it is worth knowing the top three depends on it.

**Q4. ARPU.** Hybrid R318.37, Postpaid R317.56, Prepaid R116.18. A prepaid customer brings in about a third of
the revenue of the other two plans, and prepaid is also the biggest group (3,323 customers).

**Q5. Heavy ticket raisers.** 52 customers raised more than three tickets and **53.8%** of them churned,
against 20.7% for everyone else. The group is small, so treat the exact figure loosely.
Looking at it the other way, 27.1% of customers with at least one ticket churned (666 of 2,462) versus 16.8% of
those with none (595 of 3,538).

**Q6. Satisfaction.** Churned customers rated their tickets 2.30 on average, retained customers 2.98.
Only 2,429 of the 3,493 tickets have a score (unresolved tickets cannot be rated), so the averages rest on the
rated ones.

**Q7. Data usage, January to June.** 5,546 customers have a usable reading for both months. The biggest
fallers lose more than half their data usage (for example CUST00133: 19.8 GB to 6.6 GB). The full per-customer
list is in `reports/query_results/Q7.csv` and is a natural source for a "usage trend" feature later.

**Q8. Top customers per province.** Five per province, 45 rows, no ties. Top spenders bring in roughly R3,600
to R4,000 over the six months, so the top five in each province are close together.

**Q9. Revenue over time.** Monthly revenue slides every month, from R1.214m in January to R1.185m in June
(down 2.4%), for R7.21m in total over the six months.

**Q10. Ticket categories.** Roaming (30.5% churn, lift 1.45), Billing (30.0%), Other (29.8%), Network coverage
(29.6%). Every category sits between 1.33 and 1.45 times the overall churn rate, so no single category stands
out. The bigger signal seems to be raising a ticket at all (see Q5), not what it was about.
Roaming has only 118 customers, so its place at the top is not solid.

**Q11. Three falling months in a row.** 796 customers show three consecutive month-on-month drops in data
usage, and **49.1%** of them churned, more than double the 21.0% overall rate. This looks like the strongest
single early-warning signal in the SQL work, and a good candidate feature. (Read "three months in a row" as three
consecutive drops; the query comment explains this.)

**Q12. View.** `customer_summary` has one row per customer (profile, usage totals, ticket counts and averages).
The `cancellation_reason` column is left out on purpose because it is only known after the customer leaves.

## Checkpoint questions

**Why can joining customers to both usage and tickets without aggregating inflate revenue?**
A customer with 6 usage rows and 3 tickets turns into 18 rows after the join, and each usage row is repeated 3
times. Summing revenue on that result counts it too many times. Query X1 shows it: the naive join gives
R8,395,802 against the correct R7,205,743, about 16.5% too high. Customers with no tickets are not affected, so
the error depends on who raises tickets, which makes it hard to spot. The fix is to aggregate each child table
(by customer) in a CTE first, then join the one-row-per-customer results.

**What does an index do, and what is its cost?**
An index is a sorted lookup structure on one or more columns. The database can jump straight to matching rows
instead of reading the entire table. For example, looking up one customer's tickets now shows
`SEARCH support_tickets USING INDEX idx_tickets_customer` in `EXPLAIN QUERY PLAN`. The cost is extra disk space,
slower inserts and updates (the index has to be kept in step), and for tiny tables like these the benefit is
small. I only added indexes on columns that are joined or filtered on often.

## Things to remember for later phases

- Q11 and Q7 both point at usage *trend* mattering more than usage level.
- `cancellation_reason` is leakage. It is in the database for reporting but is excluded from the view.
- Missing values are still NULL. Fill them inside the modelling pipeline so the fill values come only from the
  training data.
- The cleaning rules in `src/clean_data.py` were written to get Phase 5 going. If your Phase 4 notebooks make
  different calls (for example on the 371.12 GB value), re-run `clean_data`, `build_database` and `run_queries`
  and update the numbers above.
