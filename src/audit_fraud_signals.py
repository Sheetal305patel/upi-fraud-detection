
import pandas as pd

df = pd.read_csv("data/transactions_cleaned.csv")

print("FRAUD SIGNAL AUDIT")
print("-" * 40)

# 1. Binary and discrete features
categorical_features = [
    "new_device_flag",
    "ip_location_mismatch",
    "failed_attempts_last_24h",
]

for feature in categorical_features:
    print(f"\nFraud rate by {feature}")

    result = df.groupby(feature, dropna=False).agg(
        total_transactions=("is_fraud", "size"),
        fraud_cases=("is_fraud", "sum"),
        fraud_rate=("is_fraud", "mean"),
    )

    result["fraud_rate_pct"] = (
        result["fraud_rate"] * 100
    ).round(2)

    print(result.drop(columns="fraud_rate").to_string())

# 2. Group continuous numerical features into ranges
for feature in ["transaction_velocity", "amount_deviation_score"]:
    print(f"\nFraud rate by {feature} range")

    # Create five ranges for easier comparison
    valid_values = df[feature].dropna()

    if valid_values.nunique() > 1:
        bins = pd.qcut(
            valid_values,
            q=5,
            duplicates="drop",
        )

        temp = df.loc[valid_values.index, ["is_fraud"]].copy()
        temp["range"] = bins

        result = temp.groupby(
            "range", observed=True
        ).agg(
            total_transactions=("is_fraud", "size"),
            fraud_cases=("is_fraud", "sum"),
            fraud_rate=("is_fraud", "mean"),
        )

        result["fraud_rate_pct"] = (
            result["fraud_rate"] * 100
        ).round(2)

        print(result.drop(columns="fraud_rate").to_string())

    print("Missing values:", df[feature].isna().sum())

print("\nAudit complete.")
