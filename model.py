import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# -----------------------------
# Load cleaned dataset
# -----------------------------
df = pd.read_csv("groundwater_cleaned.csv")

# -----------------------------
# Encode approx_depth → numeric midpoints
# -----------------------------
def encode_depth_interval(value):
    value = str(value).lower()

    if "less than 30" in value:
        return 15
    if "less than 50" in value:
        return 25
    if "less than 100" in value:
        return 50
    if "greater than 100" in value:
        return 125

    return None

df["depth_cm"] = df["approx_depth"].apply(encode_depth_interval)
df = df.dropna(subset=["depth_cm"])

# -----------------------------
# EXACT features used in prediction + app.py
# -----------------------------
features = [
    "temperature",
    "conductivity",
    "turbidity",
    "total_dissolved_solids",
    "hardness_caco3",
    "chlorides",
    "sulphate"
]

# Targets for chemical parameter prediction
targets = ["ph", "dissolved_o2", "bod", "nitrate_n"]

# -----------------------------
# Prepare data
# -----------------------------
df_model = df[features + targets + ["depth_cm"]].apply(pd.to_numeric, errors="coerce")
df_model = df_model.dropna()

X = df_model[features]

models = {}

print("\n--------------------")
print("Training Chemical Models")
print("--------------------")

# -----------------------------
# Train & save chemical models
# -----------------------------
for target in targets:
    y = df_model[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(random_state=42)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)

    rmse = (mean_squared_error(y_test, preds) ** 0.5)
    r2 = r2_score(y_test, preds)

    print(f"{target} → RMSE = {rmse:.3f}, R2 = {r2:.3f}")

    joblib.dump(model, f"{target}_model.pkl")
    models[target] = model

print("\n--------------------")
print("Training DWLR Depth Model")
print("--------------------")

# -----------------------------
# Train DWLR Model
# -----------------------------
y_depth = df_model["depth_cm"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y_depth, test_size=0.2, random_state=42
)

dwlr_model = RandomForestRegressor(random_state=42)
dwlr_model.fit(X_train, y_train)

depth_preds = dwlr_model.predict(X_test)

rmse = (mean_squared_error(y_test, depth_preds) ** 0.5)
r2 = r2_score(y_test, depth_preds)

print(f"DWLR → RMSE = {rmse:.3f}, R2 = {r2:.3f}")

joblib.dump(dwlr_model, "dwlr_model.pkl")

print("\nAll models trained and saved successfully!")
