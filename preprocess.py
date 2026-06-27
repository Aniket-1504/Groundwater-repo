import pandas as pd
import numpy as np

# -------------------------------
# 1. Load all 3 datasets
# -------------------------------
df1 = pd.read_csv("NWMP_July2025.csv", encoding="latin1")
df2 = pd.read_csv("NWMP_August2025_MPCB_0.csv", encoding="latin1")
df3 = pd.read_csv("NWMP_September2025_MPCB_0.csv", encoding="latin1")

df = pd.concat([df1, df2, df3], ignore_index=True)

print("Merged dataset shape:", df.shape)

# -------------------------------
# 2. Standardize column names
# -------------------------------
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

print("Columns:", df.columns.tolist())

# -------------------------------
# 3. Handle missing values
# -------------------------------
# Convert numeric-looking columns safely
for col in df.columns:
    try:
        df[col] = pd.to_numeric(df[col])
    except:
        pass

# Fill missing numeric values with median
num_cols = df.select_dtypes(include=["float64", "int64"]).columns
df[num_cols] = df[num_cols].fillna(df[num_cols].median())

# Fill missing categorical values with mode
cat_cols = df.select_dtypes(include=["object"]).columns
for col in cat_cols:
    df[col] = df[col].fillna(df[col].mode()[0])

print("Missing values handled.")

# -------------------------------
# 4. Date column processing
# -------------------------------
# Try common date column names
date_cols = ["date", "sampling_date", "observation_date"]

for col in date_cols:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors="coerce")
        print("Date column processed:", col)

# -------------------------------
# 5. Remove duplicates
# -------------------------------
before = df.shape[0]
df = df.drop_duplicates()
after = df.shape[0]

print("Duplicates removed:", before - after)

# -------------------------------
# 6. Outlier removal (IQR method)
# -------------------------------
# for col in num_cols:
#     Q1 = df[col].quantile(0.25)
#     Q3 = df[col].quantile(0.75)
#     IQR = Q3 - Q1

#     lower = Q1 - 1.5 * IQR
#     upper = Q3 + 1.5 * IQR

#     df = df[(df[col] >= lower) & (df[col] <= upper)]

# print("Outliers removed.")
# -------------------------------
# 6. Outlier handling (clipping)
# -------------------------------
for col in num_cols:
    lower = df[col].quantile(0.01)
    upper = df[col].quantile(0.99)
    df[col] = df[col].clip(lower, upper)

print("Outliers clipped (not removed).")


# -------------------------------
# 7. Save cleaned dataset
# -------------------------------
df.to_csv("groundwater_cleaned.csv", index=False)

print("Cleaned dataset saved as groundwater_cleaned.csv")
