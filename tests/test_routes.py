import os
import sys
import unittest

# Add parent path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app


class TestRoutes(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.client = app.app.test_client()
        # Mock logged-in user session
        with self.client.session_transaction() as sess:
            sess["user_id"] = 1

    def test_forecast_api(self):
        # Query forecast for Akola
        response = self.client.get("/forecast?district=Akola")
        print("Status code:", response.status_code)
        json_data = response.get_json()
        print("Response JSON keys:", json_data.keys() if json_data else None)
        self.assertEqual(response.status_code, 200)
        self.assertIn("historical", json_data)
        self.assertIn("forecast", json_data)
        
    def test_alerts_api(self):
        response = self.client.get("/alerts?district=Akola")
        print("Alerts Status:", response.status_code)
        json_data = response.get_json()
        print("Alerts count:", json_data.get("alerts_count") if json_data else None)
        self.assertEqual(response.status_code, 200)
        
    def test_feature_importance_api(self):
        response = self.client.get("/feature-importance?district=Akola")
        print("Features Status:", response.status_code)
        json_data = response.get_json()
        print("Features explanation keys:", json_data.get("explanation", {}).keys() if json_data else None)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
