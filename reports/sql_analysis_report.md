# SQL Analysis of UPI Fraud Detection Data

## 1. Introduction

After cleaning and checking the transaction data, I started analysing it using MySQL. My main aim was to understand how fraudulent transactions are distributed and whether there are any common patterns in them.

For this analysis, I used the `transactions` table from my `upi_fraud_detection` database. It contains 20,000 transactions.

I wrote SQL queries to check fraud rates across different transaction types, KYC status, devices, failed attempts, transaction timings and transaction amounts.

## 2. Dataset Overview

Before starting the detailed analysis, I checked the total number of records and the distribution of fraud and non-fraud transactions.

| Description | Count |
|---|---:|
| Total Transactions | 20,000 |
| Fraud Transactions | 763 |
| Non-Fraud Transactions | 19,237 |

The overall fraud rate in the dataset is **3.82%**.

This means that out of 20,000 transactions, 763 are labelled as fraudulent.

## 3. Fraud Analysis by Transaction Type

I wanted to check whether fraud was more common in any particular type of transaction.

| Transaction Type | Total Transactions | Fraud Cases | Fraud Rate |
|---|---:|---:|---:|
| P2M | 7,014 | 280 | 3.99% |
| Subscription | 1,381 | 55 | 3.98% |
| P2P | 4,881 | 182 | 3.73% |
| Recharge | 2,063 | 77 | 3.73% |
| Bill Payment | 3,033 | 112 | 3.69% |
| EMI | 1,628 | 57 | 3.50% |

**What I found:**

- P2M has the highest fraud rate at 3.99%.
- Subscription transactions are almost at the same level, with 3.98%.
- EMI has the lowest fraud rate at 3.50%.
- P2M also has the highest number of fraud cases.

The difference between transaction types is not very large, but it is useful to understand how fraud is distributed across them.

## 4. Fraud Analysis by KYC Status

Next, I compared transactions from verified and non-verified users.

| KYC Status | Total Transactions | Fraud Cases | Fraud Rate |
|---|---:|---:|---:|
| Not Verified | 2,706 | 154 | 5.69% |
| Verified | 17,294 | 609 | 3.52% |

**What I found:**

The fraud rate for non-verified users is 5.69%, while for verified users it is 3.52%.

This shows that the non-verified group has a higher fraud rate in this dataset. However, the total number of fraud cases is higher among verified users because they have a much larger number of transactions.

I think KYC status can be a useful feature when checking transaction risk.

## 5. New Device and IP Location Mismatch Analysis

I also checked what happens when a transaction is made from a new device or when the IP location does not match the expected location.

| New Device | IP Mismatch | Transactions | Fraud Cases | Fraud Rate |
|---|---|---:|---:|---:|
| Yes | Yes | 42 | 7 | 16.67% |
| Yes | No | 1,254 | 153 | 12.20% |
| No | Yes | 727 | 68 | 9.35% |
| No | No | 17,977 | 535 | 2.98% |

**What I found:**

- Transactions with both a new device and IP mismatch have the highest fraud rate of 16.67%.
- New device transactions without IP mismatch have a fraud rate of 12.20%.
- Transactions with only IP mismatch have a fraud rate of 9.35%.
- When neither condition is present, the fraud rate is 2.98%.

This was one of the more interesting findings for me. It suggests that device and IP-related information can help identify transactions that may need additional checking.

One thing to keep in mind is that the group with both conditions has only 42 transactions, so its fraud rate should be treated carefully.

## 6. Fraud Analysis by Failed Attempts

I checked whether the number of failed attempts in the last 24 hours had any relation to fraud.

| Failed Attempts | Total Transactions | Fraud Cases | Fraud Rate |
|---:|---:|---:|---:|
| 0 | 14,314 | 495 | 3.46% |
| 1 | 2,863 | 111 | 3.88% |
| 2 | 1,421 | 65 | 4.57% |
| 3 | 783 | 44 | 5.62% |
| 4 | 404 | 34 | 8.42% |
| 5 | 215 | 14 | 6.51% |

**What I found:**

The fraud rate generally increases as failed attempts increase from zero to four. The highest rate is 8.42% at four failed attempts.

At five attempts, the rate decreases to 6.51%, so the pattern is not continuously increasing.

This indicates that failed attempts could be useful when analysing suspicious transaction behaviour.

## 7. Night vs Day Transaction Analysis

I wanted to see whether transaction timing made any difference to the fraud rate. For this, I compared daytime and nighttime transactions.

| Metric | Night | Day |
|---|---:|---:|
| Total Transactions | 6,492 | 13,508 |
| Fraud Cases | 342 | 421 |
| Fraud Rate | 5.27% | 3.12% |
| Total Transaction Amount | ₹57,36,449.28 | ₹1,18,00,487.79 |
| Fraud Transaction Amount | ₹3,26,002.85 | ₹3,89,785.70 |

**What I found:**

The fraud rate during nighttime is 5.27%, compared to 3.12% during the day.

The nighttime fraud rate is approximately 1.69 times the daytime rate.

However, the total number of fraud cases and fraud transaction amount are higher during the day because there are more daytime transactions.

This made me consider transaction timing as another useful feature for fraud analysis.

## 8. Fraud Analysis by Transaction Amount

I divided transactions into different amount ranges to understand whether fraud rates change with transaction value.

| Amount Range | Total Transactions | Fraud Cases | Fraud Rate |
|---|---:|---:|---:|
| Below ₹500 | 9,354 | 355 | 3.80% |
| ₹500–1,999 | 8,753 | 322 | 3.68% |
| ₹2,000–4,999 | 1,668 | 72 | 4.32% |
| ₹5,000–9,999 | 202 | 13 | 6.44% |
| ₹10,000+ | 23 | 1 | 4.35% |

**What I found:**

- The ₹5,000–9,999 range has the highest fraud rate at 6.44%.
- Transactions below ₹500 have the highest number of fraud cases (355).
- The ₹10,000+ category has only 23 transactions.

I noticed that a higher transaction amount does not always mean a higher fraud risk. It is better to analyse the amount along with other transaction details.

## 9. Overall Findings

After completing these SQL queries, I found a few patterns worth looking at more closely:

1. The overall fraud rate in the dataset is 3.82%.
2. P2M transactions have the highest fraud rate among transaction types.
3. Non-verified users have a higher fraud rate than verified users.
4. New device activity combined with IP mismatch shows a higher fraud rate.
5. Transactions with four failed attempts have the highest fraud rate in the failed-attempt groups.
6. Nighttime transactions have a higher fraud rate than daytime transactions.
7. The ₹5,000–9,999 amount range has the highest fraud rate among the amount groups.

These observations helped me understand which transaction features may be useful for further fraud analysis.

## 10. Conclusion

This SQL analysis helped me understand the transaction data in more detail. I used MySQL queries such as `COUNT()`, `SUM()`, `ROUND()`, `GROUP BY`, `ORDER BY` and `CASE WHEN` to calculate fraud counts and compare fraud rates across different categories.

I also found that looking at only one feature is not enough to understand fraud properly. Device information, IP mismatch, KYC status, failed attempts, transaction timing and transaction amount can all provide useful information when studied together.

I will use these findings as a reference for the next stages of my UPI Fraud Detection project, especially while working with Python and machine learning models.

## 11. Limitations

- This project uses a synthetic dataset, not actual UPI or bank transaction records.
- The findings describe only the data used in this project.
- A higher fraud rate does not prove that a particular feature causes fraud.
- Some categories have fewer transactions, so their fraud rates may be less reliable.
- Fraud transaction amount refers to the value of transactions labelled as fraud, not confirmed financial loss.

---

**Tools Used:** MySQL and SQL

**Project:** UPI Fraud Detection

*Note: This project is created for learning and portfolio purposes using synthetic transaction data.*