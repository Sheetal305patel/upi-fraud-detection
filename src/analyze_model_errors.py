
import os
import pandas as pd
from sklearn.model_selection import train_test_split

os.makedirs("reports", exist_ok=True)

# Load the same dataset
df = pd.read_csv("data/transactions_cleaned.csv")

# Recreate the ML test split
# Create the feature used during model training
df["amount_vs_user_avg"] = (
    df["amount"] / df["user_avg_txn_value"].replace(0, pd.NA)
).fillna(0)

X = df.drop(columns=["is_fraud"])
y = df["is_fraud"]

_, X_test, _, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# Load the saved trained model
import joblib

model = joblib.load("reports/fraud_detection_model.pkl")

# Match the features used during model training
# The model's pipeline should select/transform its expected features.
X_test_model = X_test.copy()

# Predict fraud probabilities and apply the selected threshold
fraud_probability = model.predict_proba(X_test_model)[:, 1]
threshold = 0.7
predicted_fraud = (fraud_probability >= threshold).astype(int)

# Build an error-analysis table
results = df.loc[X_test.index].copy()
results["fraud_probability"] = fraud_probability
results["predicted_fraud"] = predicted_fraud

results["error_type"] = "Correct Prediction"
results.loc[
    (results["is_fraud"] == 0) & (results["predicted_fraud"] == 1),
    "error_type"
] = "False Positive"

results.loc[
    (results["is_fraud"] == 1) & (results["predicted_fraud"] == 0),
    "error_type"
] = "False Negative"

results.loc[
    (results["is_fraud"] == 1) & (results["predicted_fraud"] == 1),
    "error_type"
] = "True Positive"

results.loc[
    (results["is_fraud"] == 0) & (results["predicted_fraud"] == 0),
    "error_type"
] = "True Negative"

# Save all predictions for investigation
output_path = "reports/ml_test_error_analysis.csv"
results.to_csv(output_path, index=False)

# Summarize the results
print("\nMODEL ERROR ANALYSIS")
print("--------------------")
print(results["error_type"].value_counts().to_string())

print("\nSaved:", output_path)
