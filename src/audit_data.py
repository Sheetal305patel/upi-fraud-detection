
from pathlib import Path
import pandas as pd

project_folder = Path(__file__).resolve().parents[1]
file_path = project_folder / "data" / "transactions.csv"

df = pd.read_csv(file_path)

print("Total transactions:", len(df))
print("Total columns:", len(df.columns))
print("Missing values:", df.isnull().sum().sum())
print("Duplicate transaction IDs:", df["transaction_id"].duplicated().sum())

print("\nFraud label counts:")
print(df["is_fraud"].value_counts().sort_index())

print("\nMissing values by column:")
print(df.isnull().sum()[df.isnull().sum() > 0])
