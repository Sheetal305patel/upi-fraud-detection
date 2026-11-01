
import os
import pandas as pd

os.makedirs("reports", exist_ok=True)

# Load Rule-Based test metrics
rule_df = pd.read_csv("reports/rule_based_test_metrics.csv")

# Load Logistic Regression final test metrics
ml_df = pd.read_csv("reports/ml_final_test_metrics.csv")

# Keep the same comparison columns
comparison_columns = [
    "model",
    "test_transactions",
    "true_positives",
    "false_positives",
    "false_negatives",
    "true_negatives",
    "precision",
    "recall",
    "f1_score"
]

rule_df = rule_df[comparison_columns]
ml_df = ml_df[comparison_columns]

# Combine results
comparison = pd.concat(
    [rule_df, ml_df],
    ignore_index=True
)

# Save comparison report
comparison.to_csv(
    "reports/model_comparison.csv",
    index=False
)

# Display results
print("\nMODEL COMPARISON - SAME TEST SET")
print("--------------------------------")
print(comparison.to_string(index=False))

print("\nSaved: reports/model_comparison.csv")
