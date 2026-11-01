
# UPI Fraud Detection — Model Evaluation Report

## 1. Project Overview

This project analyzes UPI transaction data to identify potentially fraudulent transactions. It uses SQL for fraud-pattern analysis and Python to evaluate a rule-based approach and a Logistic Regression classification model.

The dataset contains 20,000 transactions, including 763 transactions labelled as fraud.

**Important:** The dataset used in this project is synthetic. The findings describe this dataset and should not be interpreted as actual banking fraud statistics.

## 2. Dataset Summary

- Total transactions: 20,000
- Non-fraud transactions: 19,237
- Fraud transactions: 763
- Fraud rate: 3.82%
- Test transactions: 4,000
- Fraud cases in test set: 153

The dataset is imbalanced because fraudulent transactions represent a small proportion of all transactions.

## 3. Models Evaluated

### Rule-Based Detection

A transaction is flagged when at least one of the following conditions is met:

- A new device is detected.
- An IP location mismatch is detected.
- Failed transaction attempts in the previous 24 hours are at least three.

### Logistic Regression

A Logistic Regression classifier was trained using transaction amounts, timing features, user-related attributes, device and location signals, and transaction categories.

The classification threshold was selected using validation data, with F1-score as the selection metric. The selected threshold was 0.7.

## 4. Test Set Results

Both approaches were evaluated on the same 4,000 test transactions.

| Metric | Rule-Based | Logistic Regression |
|---|---:|---:|
| True Positives | 56 | 48 |
| False Positives | 545 | 381 |
| False Negatives | 97 | 105 |
| True Negatives | 3,302 | 3,466 |
| Precision | 9.32% | 11.19% |
| Recall | 36.60% | 31.37% |
| F1-score | 14.85% | 16.49% |

## 5. Key Findings

- The rule-based approach detected 56 of the 153 fraud cases in the test set.
- Logistic Regression detected 48 of the 153 fraud cases.
- The rule-based approach detected eight more fraud cases but generated 164 additional false positives.
- Logistic Regression achieved higher precision and F1-score at the selected threshold.
- Both approaches missed a substantial number of fraudulent transactions.

## 6. Limitations

- The dataset is synthetic and may not reflect real-world banking transaction patterns.
- The rule-based conditions are simple screening rules and may generate false alerts.
- The dataset contains relatively few fraud examples compared with non-fraud transactions.
- Model performance may change with different datasets, feature distributions, or classification thresholds.
- These results do not establish that the model is suitable for production banking systems.

## 7. Future Improvements

- Analyze precision-recall trade-offs across multiple thresholds.
- Investigate false positives and missed fraud cases.
- Test additional classification algorithms and compare them on the same test set.
- Improve feature quality and investigate missing values.
- Add monitoring for changes in transaction patterns.
- Validate performance on independently sourced, appropriately authorized real-world data before any production use.

## 8. Conclusion

This project demonstrates a basic fraud-analysis workflow using SQL, Python, rule-based detection, and Logistic Regression. On the current synthetic test set, Logistic Regression achieved a higher F1-score, while the rule-based approach detected more fraud cases. Further evaluation and improvement are needed before drawing conclusions about practical fraud-detection effectiveness.
