-- MzansiConnect business questions
--
-- Run with:  python -m src.run_queries
-- Each block starts with "-- Q<number>." so the Python runner can split the file.
-- Reminder: customers have many usage rows AND many tickets. Whenever a query
-- needs both, each child table is summed up in a CTE first and then joined,
-- otherwise rows multiply and totals come out inflated (see X1 at the bottom).


-- Q1. How many customers are there, and what percentage churned?
-- churned is stored as 1/0, so SUM counts churners and AVG would give the rate.
SELECT
    COUNT(*)                                          AS total_customers,
    SUM(churned)                                      AS churned_customers,
    ROUND(100.0 * SUM(churned) / COUNT(*), 1)         AS churn_pct
FROM customers;


-- Q2. Churn rate by plan type and contract length.
-- CASE turns contract_months into a readable label (0 means no contract).
SELECT
    plan_type,
    CASE WHEN contract_months = 0 THEN 'No contract'
         ELSE contract_months || ' months' END        AS contract,
    COUNT(*)                                          AS customers,
    SUM(churned)                                      AS churned,
    ROUND(100.0 * AVG(churned), 1)                    AS churn_pct
FROM customers
GROUP BY plan_type, contract_months
ORDER BY plan_type, contract_months;


-- Q3. The three provinces with the highest churn rate, ignoring small ones.
-- HAVING filters after grouping, which WHERE can't do. Provinces with fewer
-- than 200 customers are left out because their rates swing too much.
SELECT
    province,
    COUNT(*)                                          AS customers,
    SUM(churned)                                      AS churned,
    ROUND(100.0 * AVG(churned), 1)                    AS churn_pct
FROM customers
GROUP BY province
HAVING COUNT(*) >= 200
ORDER BY AVG(churned) DESC
LIMIT 3;


-- Q4. Average monthly revenue per customer (ARPU) by plan type.
-- Averages each customer's own months first, then averages across customers.
-- That way a customer with 4 months of data counts the same as one with 6.
WITH customer_revenue AS (
    SELECT customer_id, AVG(revenue_zar) AS avg_monthly_revenue
    FROM usage_monthly
    GROUP BY customer_id
)
SELECT
    c.plan_type,
    COUNT(*)                                          AS customers,
    ROUND(AVG(r.avg_monthly_revenue), 2)              AS arpu_zar
FROM customers c
JOIN customer_revenue r ON r.customer_id = c.customer_id
GROUP BY c.plan_type
ORDER BY arpu_zar DESC;


-- Q5a. Churn rate for customers with more than three tickets vs everyone else.
-- Tickets are counted per customer in a CTE; LEFT JOIN keeps customers who
-- never raised a ticket (COALESCE turns their NULL count into 0).
WITH ticket_counts AS (
    SELECT customer_id, COUNT(*) AS n_tickets
    FROM support_tickets
    GROUP BY customer_id
)
SELECT
    CASE WHEN COALESCE(t.n_tickets, 0) > 3 THEN 'More than 3 tickets'
         ELSE '3 tickets or fewer' END                AS ticket_group,
    COUNT(*)                                          AS customers,
    SUM(c.churned)                                    AS churned,
    ROUND(100.0 * AVG(c.churned), 1)                  AS churn_pct
FROM customers c
LEFT JOIN ticket_counts t ON t.customer_id = c.customer_id
GROUP BY ticket_group
ORDER BY ticket_group DESC;


-- Q5b. The customers behind Q5a: everyone with more than three tickets.
SELECT
    c.customer_id,
    t.n_tickets,
    CASE WHEN c.churned = 1 THEN 'Yes' ELSE 'No' END  AS churned
FROM customers c
JOIN (SELECT customer_id, COUNT(*) AS n_tickets
      FROM support_tickets
      GROUP BY customer_id
      HAVING COUNT(*) > 3) t ON t.customer_id = c.customer_id
ORDER BY t.n_tickets DESC, c.customer_id;


-- Q6. Average satisfaction score, churned vs retained.
-- This is an average over tickets, not customers. AVG() skips NULL scores
-- (unresolved or unrated tickets); rated_tickets shows how many it really used.
SELECT
    CASE WHEN c.churned = 1 THEN 'Churned' ELSE 'Retained' END   AS status,
    COUNT(*)                                          AS tickets,
    COUNT(t.satisfaction_score)                       AS rated_tickets,
    ROUND(AVG(t.satisfaction_score), 2)               AS avg_satisfaction
FROM customers c
JOIN support_tickets t ON t.customer_id = c.customer_id
GROUP BY c.churned
ORDER BY c.churned DESC;


-- Q7. Change in data usage between January and June, per customer.
-- Conditional aggregation pulls the two months onto one row. A customer who
-- is missing either month (or had a bad reading set to NULL) gets NULL, not 0.
WITH jan_jun AS (
    SELECT
        customer_id,
        MAX(CASE WHEN month = '2026-01' THEN data_gb END) AS jan_gb,
        MAX(CASE WHEN month = '2026-06' THEN data_gb END) AS jun_gb
    FROM usage_monthly
    GROUP BY customer_id
)
SELECT
    customer_id,
    jan_gb,
    jun_gb,
    ROUND(jun_gb - jan_gb, 2)                         AS change_gb,
    CASE WHEN jan_gb > 0
         THEN ROUND(100.0 * (jun_gb - jan_gb) / jan_gb, 1) END  AS change_pct
FROM jan_jun
WHERE jan_gb IS NOT NULL AND jun_gb IS NOT NULL
ORDER BY change_gb;


-- Q8. Top five customers by total revenue within each province.
-- RANK() restarts for every province (PARTITION BY). If two customers tie on
-- revenue they share a rank, so a province could in theory show more than five.
WITH customer_revenue AS (
    SELECT c.customer_id, c.province, SUM(u.revenue_zar) AS total_revenue
    FROM customers c
    JOIN usage_monthly u ON u.customer_id = c.customer_id
    GROUP BY c.customer_id, c.province
),
ranked AS (
    SELECT
        province,
        customer_id,
        total_revenue,
        RANK() OVER (PARTITION BY province ORDER BY total_revenue DESC) AS revenue_rank
    FROM customer_revenue
)
SELECT province, revenue_rank, customer_id, ROUND(total_revenue, 2) AS total_revenue_zar
FROM ranked
WHERE revenue_rank <= 5
ORDER BY province, revenue_rank;


-- Q9. Monthly revenue with a running total across the six months.
-- Total per month first, then a window SUM that adds up everything up to
-- and including the current month.
WITH monthly AS (
    SELECT month, SUM(revenue_zar) AS revenue
    FROM usage_monthly
    GROUP BY month
)
SELECT
    month,
    ROUND(revenue, 2)                                 AS revenue_zar,
    ROUND(SUM(revenue) OVER (ORDER BY month), 2)      AS running_total_zar
FROM monthly
ORDER BY month;


-- Q10. Which ticket categories go with churn the most?
-- One row per category. Customers are counted once per category even if they
-- raised several tickets of that type. "lift" compares the category's churn
-- rate to the overall rate (1.0 = same as everyone).
-- Careful: this shows association, not cause. Some tickets may be raised
-- because a customer is already unhappy and on the way out.
SELECT
    t.category,
    COUNT(DISTINCT t.customer_id)                                          AS customers,
    COUNT(DISTINCT CASE WHEN c.churned = 1 THEN t.customer_id END)         AS churned,
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN c.churned = 1 THEN t.customer_id END)
          / COUNT(DISTINCT t.customer_id), 1)                              AS churn_pct,
    ROUND((1.0 * COUNT(DISTINCT CASE WHEN c.churned = 1 THEN t.customer_id END)
          / COUNT(DISTINCT t.customer_id))
          / (SELECT AVG(churned) FROM customers), 2)                       AS lift
FROM support_tickets t
JOIN customers c ON c.customer_id = t.customer_id
GROUP BY t.category
ORDER BY churn_pct DESC;


-- Q11. Customers whose data usage fell three months in a row.
-- "Three months in a row" is read as three consecutive month-on-month drops
-- (four readings, each lower than the one before). LAG looks back at earlier
-- months for the same customer. month_no turns '2026-03' into a counter so we
-- can check the four readings really are consecutive months; without that
-- check a gap (missing month) would be silently skipped over.
WITH usage_idx AS (
    SELECT
        customer_id,
        month,
        data_gb,
        CAST(substr(month, 1, 4) AS INTEGER) * 12 + CAST(substr(month, 6, 2) AS INTEGER) AS month_no
    FROM usage_monthly
    WHERE data_gb IS NOT NULL
),
lagged AS (
    SELECT
        customer_id,
        month,
        month_no,
        data_gb,
        LAG(data_gb,  1) OVER w AS gb_1_back,
        LAG(data_gb,  2) OVER w AS gb_2_back,
        LAG(data_gb,  3) OVER w AS gb_3_back,
        LAG(month_no, 3) OVER w AS month_no_3_back
    FROM usage_idx
    WINDOW w AS (PARTITION BY customer_id ORDER BY month_no)
),
declining AS (
    SELECT customer_id, month AS run_ends_in
    FROM lagged
    WHERE month_no_3_back = month_no - 3
      AND data_gb < gb_1_back
      AND gb_1_back < gb_2_back
      AND gb_2_back < gb_3_back
)
SELECT
    d.customer_id,
    MIN(d.run_ends_in)                                AS first_run_ends_in,
    COUNT(*)                                          AS number_of_runs,
    CASE WHEN c.churned = 1 THEN 'Yes' ELSE 'No' END  AS churned
FROM declining d
JOIN customers c ON c.customer_id = d.customer_id
GROUP BY d.customer_id
ORDER BY d.customer_id;


-- Q12. A view with one row per customer: profile, usage totals, ticket counts.
-- Usage and tickets are each aggregated in their own CTE before joining, so
-- there is exactly one row per customer. LEFT JOIN on tickets keeps customers
-- who never contacted support (their ticket_count is 0, not NULL).
-- cancellation_reason is deliberately left out of the view: it's leakage, and
-- anyone building a model off this view shouldn't get it by accident.
DROP VIEW IF EXISTS customer_summary;
CREATE VIEW customer_summary AS
WITH usage_totals AS (
    SELECT
        customer_id,
        COUNT(*)                        AS months_with_usage,
        SUM(revenue_zar)                AS total_revenue_zar,
        AVG(revenue_zar)                AS avg_monthly_revenue_zar,
        AVG(data_gb)                    AS avg_data_gb,
        AVG(voice_minutes)              AS avg_voice_minutes,
        AVG(sms_count)                  AS avg_sms_count,
        SUM(dropped_call_complaint)     AS dropped_call_complaints
    FROM usage_monthly
    GROUP BY customer_id
),
ticket_totals AS (
    SELECT
        customer_id,
        COUNT(*)                        AS ticket_count,
        SUM(1 - resolved)               AS unresolved_tickets,
        AVG(resolution_hours)           AS avg_resolution_hours,
        AVG(satisfaction_score)         AS avg_satisfaction
    FROM support_tickets
    GROUP BY customer_id
)
SELECT
    c.customer_id,
    c.signup_date,
    c.age,
    c.gender,
    c.province,
    c.city_type,
    c.plan_type,
    c.contract_months,
    c.device_type,
    c.payment_method,
    c.income_band,
    c.referral_source,
    c.churned,
    u.months_with_usage,
    u.total_revenue_zar,
    u.avg_monthly_revenue_zar,
    u.avg_data_gb,
    u.avg_voice_minutes,
    u.avg_sms_count,
    u.dropped_call_complaints,
    COALESCE(t.ticket_count, 0)         AS ticket_count,
    COALESCE(t.unresolved_tickets, 0)   AS unresolved_tickets,
    t.avg_resolution_hours,
    t.avg_satisfaction
FROM customers c
LEFT JOIN usage_totals  u ON u.customer_id = c.customer_id
LEFT JOIN ticket_totals t ON t.customer_id = c.customer_id;


-- Q12b. Using the view: the ten highest-revenue customers.
SELECT customer_id, province, plan_type, ticket_count,
       ROUND(total_revenue_zar, 2) AS total_revenue_zar, churned
FROM customer_summary
ORDER BY total_revenue_zar DESC
LIMIT 10;


-- X1. Why you aggregate before joining (checkpoint question).
-- "naive" joins customers to usage AND tickets in one go. Every usage row gets
-- repeated once per ticket that customer has, so revenue is overcounted.
-- "correct" sums usage on its own.
SELECT
    (SELECT ROUND(SUM(u.revenue_zar), 2)
     FROM customers c
     JOIN usage_monthly u ON u.customer_id = c.customer_id
     LEFT JOIN support_tickets t ON t.customer_id = c.customer_id)   AS naive_total_revenue,
    (SELECT ROUND(SUM(revenue_zar), 2) FROM usage_monthly)           AS correct_total_revenue;
