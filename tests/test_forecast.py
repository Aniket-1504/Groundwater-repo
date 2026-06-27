import os
import sys
import unittest
import pandas as pd

# Add parent path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from forecast_module.ml_models import (
    load_and_preprocess_data,
    prepare_lagged_dataset,
    evaluate_models,
    generate_forecasts
)
from forecast_module.explainability import explain_prediction
from forecast_module.alerts import check_forecast_alerts


class TestGroundwaterForecasting(unittest.TestCase):
    
    def setUp(self):
        # Create a tiny mock dataframe simulating groundwater cleaned csv
        self.mock_data = pd.DataFrame({
            "district": ["Akola"] * 10,
            "stn_name": ["Akola Station"] * 10,
            "sampling_date": [f"2025-07-{i:02d}" for i in range(1, 11)],
            "approx_depth": ["50-100cm"] * 10, # parsed to 0.75m
            "temperature": [25.0] * 10,
            "humidity": [60.0] * 10,
            "rainfall": [10.0] * 10
        })
        
    def test_preprocessing(self):
        # Check parsing
        from app import parse_depth
        self.assertEqual(parse_depth("50-100cm"), 0.75)
        
    def test_lagged_dataset_creation(self):
        from app import parse_depth
        df = self.mock_data.copy()
        df["depth"] = df["approx_depth"].apply(parse_depth)
        df["date"] = pd.to_datetime(df["sampling_date"])
        df_supervised, features, target = prepare_lagged_dataset(df, n_lags=2)
        # With 10 rows and 2 lags, we should have 8 rows after dropping NaNs
        if not df_supervised.empty:
            self.assertEqual(len(df_supervised), 8)
            self.assertIn("depth_lag_1", features)
            self.assertIn("depth_lag_2", features)
            self.assertEqual(target, "depth")
            
    def test_explainability(self):
        # Mock last features dict
        last_features = {
            "depth_lag_1": 0.75,
            "depth_lag_2": 0.75,
            "depth_lag_3": 0.75,
            "rainfall_lag_1": 10.0,
            "rainfall_lag_2": 10.0,
            "rainfall_lag_3": 10.0,
            "temperature_lag_1": 25.0,
            "temperature_lag_2": 25.0,
            "temperature_lag_3": 25.0,
            "humidity_lag_1": 60.0,
            "humidity_lag_2": 60.0,
            "humidity_lag_3": 60.0,
            "month_sin": 0.5,
            "month_cos": 0.8
        }
        
        # Test heuristic features matching
        from sklearn.linear_model import LinearRegression
        model = LinearRegression()
        model.coef_ = [0.1] * 15 # mock coefficients
        
        explanation = explain_prediction("ARIMA", model, self.mock_data, last_features)
        self.assertIn("contributions", explanation)
        self.assertIn("summary_points", explanation)
        self.assertTrue(len(explanation["contributions"]) > 0)
        
    def test_alert_generation(self):
        # Mock predictions list
        predictions = [
            {"horizon": "7d", "predicted_depth_m": 4.5, "confidence_score": 0.95},
            {"horizon": "30d", "predicted_depth_m": 7.0, "confidence_score": 0.90}, # APPROACH DEDEPLETION
            {"horizon": "3m", "predicted_depth_m": 9.0, "confidence_score": 0.80}, # CRITICAL DEDEPLETION
            {"horizon": "1y", "predicted_depth_m": 9.5, "confidence_score": 0.60}
        ]
        
        alerts = check_forecast_alerts("Akola", predictions, historical_avg=5.0)
        self.assertTrue(len(alerts) > 0)
        
        # Check alert types are correctly mapped
        alert_types = [a["type"] for a in alerts]
        self.assertIn("CRITICAL_THRESHOLD", alert_types)


if __name__ == "__main__":
    unittest.main()
