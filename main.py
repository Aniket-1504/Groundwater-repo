# =========================================
# Water Quality Analysis & Prediction System
# Final Year Project
# =========================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# 1. Load dataset
print("Loading dataset...")
df = pd.read_csv("groundwater_cleaned.csv")

print("\nFirst 5 rows:")
print(df.head())

# 2. Dataset information
print("\nDataset Info:")
print(df.info())

# 3. Select only numeric columns
numeric_df = df.select_dtypes(include=['int64', 'float64'])

print("\nNumeric columns used for ML:")
print(numeric_df.columns)

# 4. Correlation Heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm")
plt.title("Correlation Matrix of Water Quality Parameters")
plt.show()

# 5. Define target variable
target = 'ph'   # predicting pH level

X = numeric_df.drop(target, axis=1)
y = numeric_df[target]

# 6. Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# 7. Train Random Forest model
print("\nTraining Random Forest Model...")
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 8. Predictions
y_pred = model.predict(X_test)

# 9. Evaluation
print("\nModel Performance:")
print("MAE:", mean_absolute_error(y_test, y_pred))
print("MSE:", mean_squared_error(y_test, y_pred))
print("R2 Score:", r2_score(y_test, y_pred))

# 10. Actual vs Predicted Graph
plt.figure()
plt.scatter(y_test, y_pred)
plt.xlabel("Actual pH Value")
plt.ylabel("Predicted pH Value")
plt.title("Actual vs Predicted pH Values")
# plt.show()
plt.savefig("feature_importance.png")
# plt.show()

plt.savefig("actual_vs_predicted.png")
# plt.show()

print("\nWater Quality Prediction System Executed Successfully")