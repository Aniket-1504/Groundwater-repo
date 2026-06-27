import joblib

# Load trained pH model
model = joblib.load("ph_prediction_model.pkl")

print("Model loaded successfully!")
print(model)
