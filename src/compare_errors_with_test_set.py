
import pandas as pd

# Load test-set predictions and error labels
df = pd.read_csv("reports/ml_test_error_analysis.csv")

groups = {
    "Entire Test Set": df,
    "False Positives": df[df["error_type"] == "False Positive"],
    "False Negatives": df[df["error_type"] == "False Negative"],
    "True Positives": df[df["error_type"] == "True Positive"],
    "True Negatives": df[df["error_type"] == "True Negative"],
}

rows = []

for group_name, group in groups.items():
    rows.append({
        "group": group_name,
        "transactions": len(group),
        "night_transactions_pct": round(
            group["is_night_transaction"].mean() * 100, 2
        ),
        "new_device_pct": round(
            group["new_device_flag"].mean() * 100, 2
        ),
        "ip_mismatch_pct": round(
            group["ip_location_mismatch"].mean() * 100, 2
        ),
        "avg_amount": round(group["amount"].mean(), 2),
    })

summary = pd.DataFrame(rows)

summary.to_csv(
    "reports/error_patterns_vs_test_set.csv",
    index=False
)

print("\nERROR PATTERNS VS TEST SET")
print("--------------------------")
print(summary.to_string(index=False))
print("\nSaved: reports/error_patterns_vs_test_set.csv")
