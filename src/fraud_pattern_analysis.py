
import pandas as pd
import os

# Load cleaned dataset
df = pd.read_csv("data/transactions_cleaned.csv")

# Create reports folder if it does not exist
os.makedirs("reports", exist_ok=True)

print("DATASET OVERVIEW")
print("Total transactions:", len(df))
print("Fraud transactions:", int(df["is_fraud"].sum()))
print("Fraud rate:", round(df["is_fraud"].mean() * 100, 2), "%")

# 1. Compare transaction amount
print("\n1. TRANSACTION AMOUNT BY FRAUD STATUS")

amount_analysis = df.groupby("is_fraud")["amount"].agg(
    ["count", "mean", "median", "min", "max"]
).round(2)

print(amount_analysis.to_string())

# 2. Fraud rate by selected categorical features
categorical_features = [
    "user_kyc_status",
    "device_type",
    "payment_app",
    "transaction_type",
    "receiver_type",
    "user_city_tier",
]

for feature in categorical_features:
    print(f"\n2. FRAUD RATE BY {feature.upper()}")

    analysis = df.groupby(feature, dropna=False).agg(
        total_transactions=("is_fraud", "size"),
        fraud_cases=("is_fraud", "sum"),
        fraud_rate=("is_fraud", "mean"),
    )

    analysis["fraud_rate_pct"] = (
        analysis["fraud_rate"] * 100
    ).round(2)

    analysis = analysis.drop(columns=["fraud_rate"])
    analysis = analysis.sort_values(
        "fraud_rate_pct", ascending=False
    )

    print(analysis.to_string())

    # Save each analysis for further review
    filename = f"reports/fraud_by_{feature}.csv"
    analysis.to_csv(filename)

# 3. Compare night versus daytime transactions
print("\n3. FRAUD RATE: NIGHT VS DAY")

night_analysis = df.groupby("is_night_transaction").agg(
    total_transactions=("is_fraud", "size"),
    fraud_cases=("is_fraud", "sum"),
    fraud_rate=("is_fraud", "mean"),
)

night_analysis["fraud_rate_pct"] = (
    night_analysis["fraud_rate"] * 100
).round(2)

print(night_analysis.to_string())

night_analysis.to_csv("reports/fraud_night_vs_day.csv")

# 4. Compare average monthly transaction behavior
print("\n4. USER TRANSACTION BEHAVIOR BY FRAUD STATUS")

behavior_analysis = df.groupby("is_fraud").agg(
    avg_monthly_txn=("user_avg_monthly_txn", "mean"),
    avg_txn_value=("user_avg_txn_value", "mean"),
    avg_loyalty_score=("user_loyalty_score", "mean"),
).round(2)

print(behavior_analysis)

behavior_analysis.to_csv(
    "reports/fraud_user_behavior.csv"
)

print("\nAnalysis complete.")
print("CSV reports saved in the reports folder.")
# 5. Compare transaction amount with user's average
df["amount_vs_user_avg"] = (
    df["amount"] /
    df["user_avg_txn_value"].replace(0, pd.NA)
)

print("\n5. TRANSACTION AMOUNT VS USER AVERAGE")
comparison = df.groupby("is_fraud")["amount_vs_user_avg"].agg(
    ["count", "mean", "median"]
).round(2)

print(comparison.to_string())
comparison.to_csv("reports/fraud_amount_vs_user_avg.csv")
print("Saved: reports/fraud_amount_vs_user_avg.csv")