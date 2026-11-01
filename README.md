# UPI Fraud Detection Using Python and SQL

## About the Project

I built this project to understand how transaction data can be used to identify possible UPI fraud. I wanted to go beyond basic analysis, so I tried different approaches, including SQL analysis, rule-based fraud detection and machine learning.

I used MySQL to explore transaction patterns and Python to analyse the data, prepare features, train models and evaluate their performance.

The dataset used in this project is synthetic. The results are only for learning and analysis purposes and do not represent actual bank transactions.

## Project Objectives

- Understand the transaction data and check its quality.
- Find patterns in fraud and non-fraud transactions.
- Analyse transaction behaviour using SQL and Python.
- Build a basic rule-based fraud detection approach.
- Train and evaluate machine learning models.
- Compare rule-based and machine learning results on the same test dataset.

## Tools and Technologies

- Python
- Pandas
- NumPy
- Scikit-learn
- MySQL
- SQL
- Matplotlib

Power BI dashboard development is planned as a later stage.

## Dataset Overview

The dataset contains 20,000 transactions.

| Description | Count |
|---|---:|
| Total Transactions | 20,000 |
| Non-Fraud Transactions | 19,237 |
| Fraud Transactions | 763 |
| Fraud Rate | 3.82% |

The dataset includes transaction amount, transaction type, payment app, device information, user details, transaction timing and other risk-related features.

## Project Work

### 1. Data Checking and Preparation

I started by checking the dataset, reviewing its columns, identifying data quality issues and preparing the data for further analysis.

I also checked fraud labels and reviewed features that could cause data leakage before model training.

### 2. SQL Analysis Using MySQL

I created SQL queries to understand how fraud-labelled transactions are distributed across different categories.

The analysis covered:

- Total fraud and non-fraud transactions.
- Overall fraud rate.
- Fraud by transaction type.
- Fraud by KYC status.
- New device and IP location mismatch.
- Failed transaction attempts.
- Night vs day transactions.
- Transaction amount ranges.

#### Some Findings From SQL Analysis

| Analysis | Observation |
|---|---|
| Transaction Type | P2M had the highest fraud rate at 3.99%. |
| KYC Status | Not Verified transactions had a 5.69% fraud rate. |
| New Device + IP Mismatch | This group had the highest rate at 16.67%. |
| Failed Attempts | Four failed attempts had an 8.42% fraud rate. |
| Night vs Day | Night transactions had a 5.27% fraud rate, compared with 3.12% during the day. |
| Transaction Amount | The 5,000–9,999 range had the highest rate at 6.44%. |

These findings helped me understand which transaction features could be useful for further fraud analysis.

### 3. Python Data Analysis

I used Pandas to explore different transaction and user-related features.

The analysis included:

- Fraud by device type.
- Fraud by payment app.
- Fraud by receiver type.
- Fraud by city tier.
- Fraud by KYC status.
- Night vs day transaction patterns.
- User behaviour.
- Transaction amount compared with average user transaction value.
- New device and IP mismatch.
- Failed attempts and transaction amount ranges.

I also compared the main Python findings with the SQL results. The transaction type, KYC status, night vs day, new device and IP mismatch, failed attempts, and transaction amount results matched.

### 4. Rule-Based Fraud Detection

I created a simple rule-based approach using selected risk indicators.

A transaction is flagged if it has a new device, an IP location mismatch, or at least three failed attempts in the previous 24 hours.

I used this approach as a baseline for comparison with the machine learning model.

### 5. Machine Learning Model

I compared Logistic Regression and Random Forest during validation.

Logistic Regression was selected based on its validation PR-AUC.

I tested different classification thresholds and selected 0.7 based on the validation F1-score.

The final model was evaluated on a separate test dataset containing 4,000 transactions.

## Model Results

Both approaches were evaluated on the same 4,000 test transactions.

| Metric | Rule-Based | Logistic Regression |
|---|---:|---:|
| Fraud Cases Detected | 56 | 48 |
| False Alerts | 545 | 381 |
| Fraud Cases Missed | 97 | 105 |
| Precision | 9.32% | 11.19% |
| Recall | 36.60% | 31.37% |
| F1-Score | 14.85% | 16.49% |

### What I Learned From the Results

The rule-based approach detected eight more fraud cases than Logistic Regression, but it also generated more false alerts.

Logistic Regression had better precision and a slightly higher F1-score at the selected threshold. However, it missed more fraud cases.

This comparison helped me understand that detecting more fraud cases and reducing false alerts are two different goals. The choice of approach depends on the balance between them.

## Project Structure

```text
UPI Fraud Detection/
│
├── data/
│   ├── transactions.csv
│   ├── transactions_cleaned.csv
│   ├── users.csv
│   ├── merchants.csv
│   ├── fraud_labels.csv
│   └── data_dictionary.csv
│
├── src/
│   ├── audit_data.py
│   ├── audit_data_leakage.py
│   ├── fraud_pattern_analysis.py
│   ├── evaluate_rules.py
│   ├── train_model.py
│   ├── compare_models.py
│   └── other analysis scripts
│
├── sql/
│   └── fraud_analysis.sql
│
├── reports/
│   ├── fraud_by_transaction_type.csv
│   ├── fraud_by_user_kyc_status.csv
│   ├── fraud_night_vs_day.csv
│   ├── fraud_by_device_ip_flags.csv
│   ├── fraud_by_failed_attempts.csv
│   ├── fraud_by_amount_range.csv
│   ├── model_comparison.csv
│   ├── ml_final_test_metrics.csv
│   ├── model_evaluation_report.md
│   └── sql_analysis_report.md
│
└── README.md
```

## Limitations and Future Improvements

This is a learning project, and there is still room for improvement.

- The dataset is synthetic, not actual UPI transaction data.
- The results may not represent real-world fraud patterns.
- Some transaction groups contain fewer records, so their fraud rates need careful interpretation.
- The current model can be improved by testing additional features and approaches.
- A Power BI dashboard is planned to present the analysis and results in a more interactive way.

## Project Status

- Data checking and preparation: Completed
- Python analysis: Completed
- SQL analysis: Completed
- Rule-based fraud detection: Completed
- Machine learning model training: Completed
- Model evaluation and comparison: Completed
- Documentation: In progress
- Power BI dashboard: Planned

**Note:** This project uses synthetic data and is created for educational and portfolio purposes only.