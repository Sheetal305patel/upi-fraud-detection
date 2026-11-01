
USE upi_fraud_detection;

-- 1. Total transactions
SELECT COUNT(*) AS total_transactions
FROM transactions;

-- 2. Fraud and non-fraud transaction counts
SELECT
    is_fraud,
    COUNT(*) AS transaction_count
FROM transactions
GROUP BY is_fraud
ORDER BY is_fraud;

-- 3. Overall fraud rate
SELECT
    COUNT(*) AS total_transactions,
    SUM(is_fraud) AS fraud_cases,
    ROUND(100.0 * SUM(is_fraud) / COUNT(*), 2) AS fraud_rate_pct
FROM transactions;

-- 4. Fraud rate by transaction type
SELECT
    transaction_type,
    COUNT(*) AS total_transactions,
    SUM(is_fraud) AS fraud_cases,
    ROUND(100.0 * SUM(is_fraud) / COUNT(*), 2) AS fraud_rate_pct
FROM transactions
GROUP BY transaction_type
ORDER BY fraud_rate_pct DESC;

-- 5. Fraud rate by KYC status
SELECT
    user_kyc_status,
    COUNT(*) AS total_transactions,
    SUM(is_fraud) AS fraud_cases,
    ROUND(100.0 * SUM(is_fraud) / COUNT(*), 2) AS fraud_rate_pct
FROM transactions
GROUP BY user_kyc_status
ORDER BY fraud_rate_pct DESC;

-- 6. Fraud rate by new device and IP mismatch
SELECT
    new_device_flag,
    ip_location_mismatch,
    COUNT(*) AS total_transactions,
    SUM(is_fraud) AS fraud_cases,
    ROUND(100.0 * SUM(is_fraud) / COUNT(*), 2) AS fraud_rate_pct
FROM transactions
GROUP BY new_device_flag, ip_location_mismatch
ORDER BY fraud_rate_pct DESC;

-- 7. Fraud rate by failed attempts
SELECT
    failed_attempts_last_24h,
    COUNT(*) AS total_transactions,
    SUM(is_fraud) AS fraud_cases,
    ROUND(100.0 * SUM(is_fraud) / COUNT(*), 2) AS fraud_rate_pct
FROM transactions
GROUP BY failed_attempts_last_24h
ORDER BY failed_attempts_last_24h;

-- 8. Fraud rate by night vs day
SELECT
    is_night_transaction,
    COUNT(*) AS total_transactions,
    SUM(is_fraud) AS fraud_cases,
    ROUND(100.0 * SUM(is_fraud) / COUNT(*), 2) AS fraud_rate_pct
FROM transactions
GROUP BY is_night_transaction;


-- 9. Fraud rate by transaction amount range
SELECT
    CASE
        WHEN amount < 500 THEN 'Below 500'
        WHEN amount < 2000 THEN '500-1999'
        WHEN amount < 5000 THEN '2000-4999'
        WHEN amount < 10000 THEN '5000-9999'
        ELSE '10000+'
    END AS amount_range,
    COUNT(*) AS total_transactions,
    SUM(is_fraud) AS fraud_cases,
    ROUND(100.0 * SUM(is_fraud) / COUNT(*), 2) AS fraud_rate_pct
FROM transactions
GROUP BY amount_range
ORDER BY MIN(amount);