CREATE TABLE IF NOT EXISTS raw_transactions (
    transaction_id VARCHAR PRIMARY KEY,
    customer_id VARCHAR,
    transaction_date DATE,
    amount NUMERIC,
    ingestion_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS fct_customer_rfm (
    customer_id VARCHAR PRIMARY KEY,
    recency INTEGER,
    frequency INTEGER,
    monetary NUMERIC,
    rfm_calculated_date DATE
);

CREATE TABLE IF NOT EXISTS customer_segments (
    customer_id VARCHAR,
    cluster_id INTEGER,
    model_run_date DATE,
    PRIMARY KEY (customer_id, model_run_date)
);
