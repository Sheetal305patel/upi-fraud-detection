
import pandas as pd

# Load cleaned dataset
df = pd.read_csv("data/transactions_cleaned.csv")

print("FRAUD LABEL AUDIT")
print("-" * 40)

# 1. Check dataset size
print("Total rows:", len(df))

# 2. Check missing fraud labels
print("Missing fraud labels:", df["is_fraud"].isna().sum())

# 3. Inspect all label values
print("\nUnique label values:")
print(df["is_fraud"].value_counts(dropna=False).to_string())

# 4. Check whether labels are binary
valid_labels = df["is_fraud"].isin([0, 1])
print("\nInvalid label rows:", (~valid_labels).sum())

# 5. Check fraud rate
if df["is_fraud"].notna().all() and valid_labels.all():
    print("Fraud rate:", round(df["is_fraud"].mean() * 100, 2), "%")
else:
    print("Fraud rate not calculated: missing or invalid labels found.")

# 6. Check duplicate transaction IDs
if "transaction_id" in df.columns:
    print(
        "\nDuplicate transaction IDs:",
        df["transaction_id"].duplicated().sum()
    )

print("\nAudit complete.")
