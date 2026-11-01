# UPI Fraud Detection Using Python and SQL

## About the Project

I built this project to understand how transaction data can be used to identify possible UPI fraud. I wanted to go beyond basic data analysis and try both rule-based fraud detection and a machine learning model.

I used SQL to explore transaction patterns and Python to prepare the data, train the model, and check how well both approaches performed.

The dataset used in this project is synthetic, so the results are for learning and analysis purposes only. They do not represent actual bank transactions.

## What I Worked On

- Explored transaction data and checked for missing values and data quality issues.
- Used SQL to study fraud patterns across transaction types, transaction amounts, timings, and risk signals.
- Created a simple rule-based approach to flag transactions with certain risk indicators.
- Trained a Logistic Regression model using transaction and user-related features.
- Compared both approaches using the same set of 4,000 test transactions.
- Evaluated the results using precision, recall, and F1-score.

## Tools I Used

- Python
- Pandas
- Scikit-learn
- MySQL

Power BI dashboard development is planned as a later step.

## Dataset Overview

The dataset contains 20,000 transactions, including:

- 19,237 transactions labelled as non-fraud
- 763 transactions labelled as fraud
- An overall fraud rate of 3.82%

The dataset includes information such as transaction amount, transaction type, time, device details, user attributes, and risk-related indicators.

## Approaches I Tested

### 1. Rule-Based Detection

I started with a straightforward approach using a few risk indicators. A transaction is flagged if it has a new device, an IP location mismatch, or at least three failed attempts in the previous 24 hours.

This gave me a baseline to compare against the machine learning model.

### 2. Logistic Regression

I then trained a Logistic Regression model using selected transaction, timing, device, and user-related features. I compared Logistic Regression with Random Forest during validation and selected Logistic Regression based on its validation PR-AUC.

I also tested different classification thresholds and selected 0.7 based on the validation F1-score.

## Model Results

Both approaches were evaluated on the same 4,000 test transactions.

| Metric | Rule-Based | Logistic Regression |
|---|---:|---:|
| Fraud cases detected | 56 | 48 |
| False alerts | 545 | 381 |
| Fraud cases missed | 97 | 105 |
| Precision | 9.32% | 11.19% |
| Recall | 36.60% | 31.37% |
| F1-score | 14.85% | 16.49% |

## What I Learned From the Results

The rule-based approach detected eight more fraud cases than Logistic Regression, but it also generated more false alerts.

Logistic Regression had better precision and a slightly higher F1-score at the selected threshold. However, it missed more fraud cases than the rule-based approach.

This comparison helped me understand that detecting more fraud cases and reducing false alerts are different goals. The choice of approach depends on the balance between these two priorities.

## Limitations and Next Steps

This project is still a learning project, and there is room for improvement. Since the dataset is synthetic, these results cannot be treated as evidence of how either approach would perform in a real payment system.

Next, I plan to investigate false alerts and missed fraud cases, explore further model improvements, and build a Power BI dashboard to present the analysis and results more clearly.

## Project Status

SQL analysis, model training, test evaluation, and model comparison are complete. Documentation is in progress, and the Power BI dashboard is planned for a later stage.