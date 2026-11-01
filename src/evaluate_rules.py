
import os
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score
)

# Create reports folder if it does not exist
os.makedirs("reports", exist_ok=True)

# Load cleaned dataset
df = pd.read_csv("data/transactions_cleaned.csv")

# Ensure transaction IDs are treated consistently
df["transaction_id"] = df["transaction_id"].astype(str).str.strip()

# Create the same stratified test split used by the ML project
train_val, test_df = train_test_split(
    df,
    test_size=0.20,
    stratify=df["is_fraud"],
    random_state=42
)

# Make a separate copy of the test data
test_df = test_df.copy()

# Save test transaction IDs
test_df["transaction_id"].to_csv(
    "reports/rule_based_test_ids.csv",
    index=False
)

print("Rule-Based test IDs saved.")
print("Test transactions:", len(test_df))
print("First 5 test IDs:")
print(test_df["transaction_id"].head().tolist())

# Apply rule-based fraud detection to test data
test_df["rule_flag"] = (
    (test_df["new_device_flag"] == 1)
    | (test_df["ip_location_mismatch"] == 1)
    | (test_df["failed_attempts_last_24h"] >= 3)
).astype(int)

# Actual and predicted labels
y_true = test_df["is_fraud"]
y_pred = test_df["rule_flag"]

# Calculate confusion matrix
tn, fp, fn, tp = confusion_matrix(
    y_true,
    y_pred,
    labels=[0, 1]
).ravel()

# Calculate metrics
precision = precision_score(
    y_true, y_pred, zero_division=0
)
recall = recall_score(
    y_true, y_pred, zero_division=0
)
f1 = f1_score(
    y_true, y_pred, zero_division=0
)

# Display results
print("\nRULE-BASED MODEL — TEST SET")
print("---------------------------")
print("Test transactions:", len(test_df))
print("Actual fraud cases:", int(y_true.sum()))
print("True positives:", tp)
print("False positives:", fp)
print("False negatives:", fn)
print("True negatives:", tn)
print(f"Precision: {precision:.4f}")
print(f"Recall:    {recall:.4f}")
print(f"F1-score:  {f1:.4f}")

# Save metrics
metrics = pd.DataFrame([{
    "model": "Rule-Based",
    "test_transactions": len(test_df),
    "true_positives": tp,
    "false_positives": fp,
    "false_negatives": fn,
    "true_negatives": tn,
    "precision": precision,
    "recall": recall,
    "f1_score": f1
}])

metrics.to_csv(
    "reports/rule_based_test_metrics.csv",
    index=False
)

print("\nSaved: reports/rule_based_test_metrics.csv")
print("Saved: reports/rule_based_test_ids.csv")
