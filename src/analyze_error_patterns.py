
import pandas as pd

df = pd.read_csv("reports/ml_test_error_analysis.csv")

error_types = ["False Positive", "False Negative"]

for error_type in error_types:
    subset = df[df["error_type"] == error_type]

    print(f"\n{'=' * 45}")
    print(f"{error_type.upper()} ANALYSIS")
    print(f"{'=' * 45}")
    print("Transactions:", len(subset))

    if subset.empty:
        continue

    print("\nAverage transaction amount:")
    print(round(subset["amount"].mean(), 2))

    print("\nNew device flag:")
    print(subset["new_device_flag"].value_counts(dropna=False).to_string())

    print("\nIP location mismatch:")
    print(
        subset["ip_location_mismatch"]
        .value_counts(dropna=False)
        .to_string()
    )

    print("\nFailed attempts:")
    print(
        subset["failed_attempts_last_24h"]
        .value_counts(dropna=False)
        .sort_index()
        .to_string()
    )

    print("\nNight vs day:")
    print(
        subset["is_night_transaction"]
        .value_counts(dropna=False)
        .to_string()
    )

# Save error-pattern summary for documentation
summary_rows = []

for error_type in ["False Positive", "False Negative"]:
    subset = df[df["error_type"] == error_type]

    if subset.empty:
        continue

    summary_rows.append({
        "error_type": error_type,
        "transactions": len(subset),
        "avg_amount": round(subset["amount"].mean(), 2),
        "new_device_count": int((subset["new_device_flag"] == 1).sum()),
        "ip_mismatch_count": int((subset["ip_location_mismatch"] == 1).sum()),
        "night_transaction_count": int((subset["is_night_transaction"] == 1).sum()),
        "zero_failed_attempts": int((subset["failed_attempts_last_24h"] == 0).sum())
    })

summary = pd.DataFrame(summary_rows)
summary.to_csv("reports/model_error_pattern_summary.csv", index=False)

print("\nSaved: reports/model_error_pattern_summary.csv")
