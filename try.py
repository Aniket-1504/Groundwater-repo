import pandas as pd
df = pd.read_csv("groundwater_cleaned.csv")
print(df.columns)
print(df[['approx_depth']].head(20))  # Check if this column exists and has values
df = df[features + ['approx_depth']]
df = df.apply(pd.to_numeric, errors="coerce")
df = df.dropna()

print("Dataset shape:", df.shape)  # Must be > 0
