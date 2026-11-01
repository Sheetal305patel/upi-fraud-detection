
import pandas as pd

df = pd.read_csv("data/transactions_cleaned.csv")

print("DATA LEAKAGE AUDIT")
print("-" * 40)

# Check columns that may be derived from or closely related to the label
possible_leakage_columns = [
    "is_fraud",
    "status",
    "balance_after_transaction",
    "transaction_frequency_score",
    "fraud_label",
]

for col in possible_leakage_columns:
    if col in df.columns:
        print(f"\nColumn: {col}")
        print("Data type:", df[col].dtype)
        print("Unique values:", df[col].nunique())
        print("Missing values:", df[col].isna().sum())

        if col != "is_fraud":
            print("Sample values:")
            print(df[col].head(5).to_list())

print("\nAll dataset columns:")
print(df.columns.to_list())

print("\nAudit complete.")
