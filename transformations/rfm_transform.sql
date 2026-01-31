INSERT INTO fct_customer_rfm (customer_id, recency, frequency, monetary, rfm_calculated_date)
SELECT
    customer_id,
    (CURRENT_DATE - MAX(transaction_date)) AS recency,
    COUNT(transaction_id) AS frequency,
    SUM(amount) AS monetary,
    CURRENT_DATE
FROM raw_transactions
GROUP BY customer_id
ON CONFLICT (customer_id)
DO UPDATE SET
    recency = EXCLUDED.recency,
    frequency = EXCLUDED.frequency,
    monetary = EXCLUDED.monetary,
    rfm_calculated_date = CURRENT_DATE;
