
import os
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
    average_precision_score,
)

# 1. Load cleaned dataset
df = pd.read_csv("data/transactions_cleaned.csv")
# Feature engineering
df["amount_vs_user_avg"] = (
    df["amount"] /
    df["user_avg_txn_value"].replace(0, float("nan"))
)
features = [
    "amount",
    "hour_of_day",
    "is_weekend",
    "is_night_transaction",
    "receiver_type",
    "transaction_type",
    "payment_app",
    "device_type",
    "user_city_tier",
    "user_kyc_status",
    "user_avg_monthly_txn",
    "user_avg_txn_value",
    "user_loyalty_score",
    "recurring_payment_flag",
    "amount_vs_user_avg",
        "new_device_flag",
    "ip_location_mismatch",
    "failed_attempts_last_24h",
    "transaction_velocity",
    "amount_deviation_score",
]

X = df[features]
y = df["is_fraud"]

# 2. Define numeric and categorical features


numeric_features = [
    "amount",
    "hour_of_day",
    "is_weekend",
    "is_night_transaction",
    "user_avg_monthly_txn",
    "user_avg_txn_value",
    "user_loyalty_score",
    "recurring_payment_flag",
    "amount_vs_user_avg",
    "new_device_flag",
    "ip_location_mismatch",
    "failed_attempts_last_24h",
    "transaction_velocity",
    "amount_deviation_score",
]

categorical_features = [
    "receiver_type",
    "transaction_type",
    "payment_app",
    "device_type",
    "user_city_tier",
    "user_kyc_status",
]
print("Numeric features:", numeric_features)
print("Categorical features:", categorical_features)
print("All model features:", features)
# 3. Preprocessing
numeric_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
])

categorical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore")),
])

preprocessor = ColumnTransformer([
    ("numeric", numeric_pipeline, numeric_features),
    ("categorical", categorical_pipeline, categorical_features),
])

# 4. Split into train, validation and test sets

X_train_full, X_test, y_train_full, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y,
)

# Save actual transaction IDs from the test set
import os
os.makedirs("reports", exist_ok=True)

test_ids = df.loc[X_test.index, "transaction_id"]

test_ids.to_csv(
    "reports/ml_test_ids.csv",
    index=False
)

print("Saved: reports/ml_test_ids.csv")

X_train, X_val, y_train, y_val = train_test_split(
    X_train_full,
    y_train_full,
    test_size=0.20,
    random_state=42,
    stratify=y_train_full,
)

print("Training rows:", len(X_train))
print("Validation rows:", len(X_val))
print("Test rows:", len(X_test))

# 5. Define Logistic Regression model
lr_model = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", LogisticRegression(
        class_weight="balanced",
        max_iter=1000,
        random_state=42,
    )),
])

# 6. Define Random Forest model
rf_model = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(
        n_estimators=200,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    )),
])

# 7. Train both models using training data only
lr_model.fit(X_train, y_train)
rf_model.fit(X_train, y_train)

# 8. Compare models on the SAME validation dataset
lr_val_prob = lr_model.predict_proba(X_val)[:, 1]
rf_val_prob = rf_model.predict_proba(X_val)[:, 1]

lr_pr_auc = average_precision_score(y_val, lr_val_prob)
rf_pr_auc = average_precision_score(y_val, rf_val_prob)

print("\nMODEL COMPARISON - VALIDATION DATA")
print("Logistic Regression PR-AUC:", round(lr_pr_auc, 4))
print("Random Forest PR-AUC:", round(rf_pr_auc, 4))
print("Validation fraud rate:", round(y_val.mean(), 4))

# Select model using validation PR-AUC
if lr_pr_auc >= rf_pr_auc:
    best_model = lr_model
    best_model_name = "Logistic Regression"
    best_val_prob = lr_val_prob
else:
    best_model = rf_model
    best_model_name = "Random Forest"
    best_val_prob = rf_val_prob

print("\nSelected model:", best_model_name)

#
# 9. Compare thresholds on validation data
threshold_results = []

print("\nTHRESHOLD COMPARISON - VALIDATION DATA")

for threshold in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]:
    val_predictions = (best_val_prob >= threshold).astype(int)

    precision = precision_score(
        y_val, val_predictions, zero_division=0
    )
    recall = recall_score(
        y_val, val_predictions, zero_division=0
    )
    f1 = f1_score(
        y_val, val_predictions, zero_division=0
    )

    tn, fp, fn, tp = confusion_matrix(
        y_val, val_predictions, labels=[0, 1]
    ).ravel()

    threshold_results.append({
        "Model": best_model_name,
        "Threshold": threshold,
        "Precision": precision,
        "Recall": recall,
        "F1_Score": f1,
        "PR_AUC": lr_pr_auc if best_model_name == "Logistic Regression" else rf_pr_auc,
        "True_Positive": tp,
        "False_Positive": fp,
        "False_Negative": fn,
        "True_Negative": tn,
        "Flagged_Transactions": tp + fp,
    })

    print(
        f"Threshold: {threshold:.1f} | "
        f"Precision: {precision:.3f} | "
        f"Recall: {recall:.3f} | "
        f"F1: {f1:.3f} | "
        f"Flagged: {tp + fp} | "
        f"False Positives: {fp}"
    )

# Select threshold with highest validation F1-score
threshold_df = pd.DataFrame(threshold_results)
best_threshold_row = threshold_df.loc[
    threshold_df["F1_Score"].idxmax()
]
selected_threshold = float(best_threshold_row["Threshold"])

print("\nSelected threshold (validation F1):", selected_threshold)
print("Validation precision:", round(best_threshold_row["Precision"], 3))
print("Validation recall:", round(best_threshold_row["Recall"], 3))
print("Validation F1-score:", round(best_threshold_row["F1_Score"], 3))


# 10. Save validation threshold metrics for Power BI
os.makedirs("reports", exist_ok=True)

pd.DataFrame(threshold_results).to_csv(
    "model_threshold_metrics.csv", index=False
)

# 11. Final evaluation on the untouched test dataset
test_probabilities = best_model.predict_proba(X_test)[:, 1]
test_predictions = (
    test_probabilities >= selected_threshold
).astype(int)
test_pr_auc = average_precision_score(y_test, test_probabilities)

print("\nFINAL TEST RESULTS")
print("Selected model:", best_model_name)
print("PR-AUC:", round(test_pr_auc, 4))
print("Test fraud rate:", round(y_test.mean(), 4))
print("\nClassification Report:")
print(classification_report(
    y_test,
    test_predictions,
    zero_division=0,
))

# 12. Save confusion matrix from test data at selected threshold
cm = confusion_matrix(y_test, test_predictions)

confusion_df = pd.DataFrame(
    cm,
    index=["Actual Non-Fraud", "Actual Fraud"],
    columns=["Predicted Non-Fraud", "Predicted Fraud"],
)

confusion_df.to_csv(
    f"reports/confusion_matrix_threshold_{selected_threshold:.1f}.csv"
)
print(f"\nConfusion Matrix at threshold {selected_threshold:.1f}:")
print(confusion_df)
# 13. Save Logistic Regression coefficients for interpretation
if best_model_name == "Logistic Regression":
    fitted_preprocessor = best_model.named_steps["preprocessor"]
    classifier = best_model.named_steps["classifier"]

    feature_names = fitted_preprocessor.get_feature_names_out()
    coefficients = classifier.coef_[0]

    importance = pd.DataFrame({
        "feature": feature_names,
        "coefficient": coefficients,
    })

    print("\nTOP 10 POSITIVE COEFFICIENTS")
    print(
        importance.sort_values("coefficient", ascending=False)
        .head(10).to_string(index=False)
    )

    print("\nTOP 10 NEGATIVE COEFFICIENTS")
    print(
        importance.sort_values("coefficient")
        .head(10).to_string(index=False)
    )
else:
    print(
        "\nLogistic Regression coefficients are not shown "
        "because Random Forest was selected."
    )



print("\nDataset shape:", df.shape)
print("Fraud counts:")
print(df["is_fraud"].value_counts())
print("Fraud rate:", round(df["is_fraud"].mean() * 100, 2), "%")

print("\nSaved: model_threshold_metrics.csv")
print("Saved: reports/confusion_matrix_threshold_0.5.csv")
import joblib

joblib.dump(best_model, "reports/fraud_detection_model.pkl")

print("Saved: reports/fraud_detection_model.pkl")


# Save final test metrics using the actual test predictions
import os

os.makedirs("reports", exist_ok=True)

tn, fp, fn, tp = confusion_matrix(
    y_test,
    test_predictions,
    labels=[0, 1]
).ravel()

precision = precision_score(
    y_test, test_predictions, zero_division=0
)
recall = recall_score(
    y_test, test_predictions, zero_division=0
)
f1 = f1_score(
    y_test, test_predictions, zero_division=0
)

test_metrics = pd.DataFrame([{
    "model": best_model_name,
    "dataset": "Test",
    "threshold": selected_threshold,
    "test_transactions": len(y_test),
    "true_positives": int(tp),
    "false_positives": int(fp),
    "false_negatives": int(fn),
    "true_negatives": int(tn),
    "precision": precision,
    "recall": recall,
    "f1_score": f1
}])

test_metrics.to_csv(
    "reports/ml_final_test_metrics.csv",
    index=False
)

print("\nFinal test metrics:")
print(test_metrics.to_string(index=False))
print("\nSaved: reports/ml_final_test_metrics.csv")
