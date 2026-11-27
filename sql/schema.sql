-- MzansiConnect database schema (SQLite)
--
-- Three tables, linked by customer_id:
--   customers (1) ----< usage_monthly (many)
--   customers (1) ----< support_tickets (many)
--
-- Dates are stored as ISO text (YYYY-MM-DD) because SQLite has no date type.
-- Yes/No flags are stored as 1/0 so they can be summed and averaged directly.

PRAGMA foreign_keys = ON;

DROP VIEW  IF EXISTS customer_summary;
DROP TABLE IF EXISTS support_tickets;
DROP TABLE IF EXISTS usage_monthly;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id         TEXT    PRIMARY KEY,
    signup_date         TEXT,                          -- NULL if the raw date was impossible
    age                 INTEGER CHECK (age BETWEEN 16 AND 100),
    gender              TEXT    CHECK (gender IN ('Female', 'Male')),
    province            TEXT    NOT NULL,
    city_type           TEXT    NOT NULL CHECK (city_type IN ('Urban', 'Peri-urban', 'Rural')),
    plan_type           TEXT    NOT NULL CHECK (plan_type IN ('Prepaid', 'Postpaid', 'Hybrid')),
    contract_months     INTEGER NOT NULL CHECK (contract_months IN (0, 12, 24)),   -- 0 = no contract
    device_type         TEXT,
    payment_method      TEXT    NOT NULL,
    income_band         TEXT,
    referral_source     TEXT    NOT NULL,
    -- LEAKAGE WARNING: only filled in after a customer has already left.
    -- Fine for reporting, never use it as a model feature.
    cancellation_reason TEXT,
    churned             INTEGER NOT NULL CHECK (churned IN (0, 1))                 -- target column
);

CREATE TABLE usage_monthly (
    customer_id             TEXT    NOT NULL,
    month                   TEXT    NOT NULL CHECK (month GLOB '2026-0[1-6]'),  -- Jan-Jun 2026
    data_gb                 REAL    CHECK (data_gb >= 0),
    voice_minutes           REAL    CHECK (voice_minutes >= 0),
    sms_count               INTEGER CHECK (sms_count >= 0),
    revenue_zar             REAL    NOT NULL CHECK (revenue_zar >= 0),
    dropped_call_complaint  INTEGER NOT NULL CHECK (dropped_call_complaint IN (0, 1)),
    -- one row per customer per month, so the pair is the key
    PRIMARY KEY (customer_id, month),
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
);

CREATE TABLE support_tickets (
    ticket_id           TEXT    PRIMARY KEY,
    customer_id         TEXT    NOT NULL,
    created_date        TEXT    NOT NULL,
    category            TEXT    NOT NULL,
    resolution_hours    REAL    CHECK (resolution_hours > 0),   -- NULL while unresolved
    resolved            INTEGER NOT NULL CHECK (resolved IN (0, 1)),
    satisfaction_score  INTEGER CHECK (satisfaction_score BETWEEN 1 AND 5),
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
);

-- Indexes
--
-- SQLite does not index foreign keys on its own. Almost every query here goes
-- from customers to their tickets, so without this index each customer would
-- trigger a scan of the whole tickets table.
CREATE INDEX idx_tickets_customer ON support_tickets (customer_id);

-- Several queries filter or group by month (Jan vs Jun comparison, running
-- revenue). The primary key starts with customer_id, so it can't help with
-- lookups by month alone, hence a second index.
-- No separate index on usage_monthly(customer_id): the primary key already
-- covers it, and a duplicate would only slow down inserts.
CREATE INDEX idx_usage_month ON usage_monthly (month);
