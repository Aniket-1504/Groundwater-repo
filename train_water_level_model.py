import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
import os

# -----------------------------
# 1. Load dataset
# -----------------------------
df = pd.read_csv("groundwater_cleaned.csv")

# -----------------------------
# 2. Map approx_depth to numeric
# -----------------------------
depth_map = {
    "Less than 50cm": 25,
    "50-100cm": 75,
    "Greater than 100cm": 125
}

df['approx_depth_cm'] = df['approx_depth'].map(depth_map)

# Drop rows where approx_depth_cm is missing
df = df.dropna(subset=['approx_depth_cm'])

# -----------------------------
# 3. Define features & target
# -----------------------------
features = [
    "temperature",
    "conductivity",
    "turbidity",
    "total_dissolved_solids",
    "hardness_caco3",
    "chlorides",
    "sulphate",
    "nitrate_n"
]

target = 'approx_depth_cm'

# Keep only necessary columns
df = df[features + [target]].apply(pd.to_numeric, errors='coerce')
df = df.dropna()

print("Dataset shape after processing:", df.shape)

# -----------------------------
# 4. Train-test split
# -----------------------------
X = df[features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -----------------------------
# 5. Train model
# -----------------------------
model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# -----------------------------
# 6. Evaluate
# -----------------------------
preds = model.predict(X_test)
rmse = mean_squared_error(y_test, preds)**0.5
r2 = r2_score(y_test, preds)
print("Water Level RMSE:", rmse)
print("Water Level R2:", r2)

# -----------------------------
# 7. Save model
# -----------------------------
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/water_level_model.pkl")
print("✅ water_level_model.pkl saved successfully")
