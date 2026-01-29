"""
Unit tests for model training and evaluation.
"""

import unittest
import pandas as pd
import numpy as np
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.model import train_model, get_feature_columns, save_model, load_model
from src.evaluation import evaluate_model


class TestModel(unittest.TestCase):
    """Test cases for model module."""

    def setUp(self):
        """Create sample test data."""
        dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq="D")
        n = len(dates)
        self.test_df = pd.DataFrame({
            "date": dates,
            "bookings": np.random.randint(50, 200, n),
            "temperature": np.random.randint(10, 30, n),
            "is_holiday": np.random.choice([0, 1], n),
            "price": np.random.randint(70, 120, n),
            "month": pd.DatetimeIndex(dates).month,
            "day_of_week": pd.DatetimeIndex(dates).dayofweek,
            "quarter": pd.DatetimeIndex(dates).quarter,
            "is_weekend": (pd.DatetimeIndex(dates).dayofweek >= 5).astype(int),
            "week_of_year": pd.DatetimeIndex(dates).isocalendar().week.values
        })

    def test_get_feature_columns(self):
        """Test feature column extraction."""
        features = get_feature_columns(self.test_df)

        # Check if base features are included
        self.assertIn("temperature", features)
        self.assertIn("is_holiday", features)
        self.assertIn("price", features)
        self.assertIn("month", features)
        self.assertIn("day_of_week", features)

        # Check if optional features are included when available
        self.assertIn("quarter", features)
        self.assertIn("is_weekend", features)
        self.assertIn("week_of_year", features)

    def test_train_model(self):
        """Test model training."""
        model, X_test, y_test, X_train, y_train = train_model(self.test_df, optimize=False)

        # Check if model was trained
        self.assertIsNotNone(model)

        # Check if train/test split was performed
        self.assertGreater(len(X_train), 0)
        self.assertGreater(len(X_test), 0)
        self.assertGreater(len(y_train), 0)
        self.assertGreater(len(y_test), 0)

        # Check if model can make predictions
        predictions = model.predict(X_test)
        self.assertEqual(len(predictions), len(y_test))

    def test_evaluate_model(self):
        """Test model evaluation."""
        model, X_test, y_test, X_train, y_train = train_model(self.test_df, optimize=False)

        metrics = evaluate_model(model, X_test, y_test)

        # Check if all metrics are present
        self.assertIn("mae", metrics)
        self.assertIn("rmse", metrics)
        self.assertIn("r2", metrics)
        self.assertIn("mape", metrics)

        # Check if metrics are reasonable
        self.assertGreater(metrics["mae"], 0)
        self.assertGreater(metrics["rmse"], 0)
        self.assertLessEqual(metrics["r2"], 1)
        self.assertGreater(metrics["mape"], 0)

    def test_save_and_load_model(self):
        """Test model saving and loading."""
        model, X_test, y_test, X_train, y_train = train_model(self.test_df, optimize=False)

        # Save model
        test_model_path = "models/test_model.pkl"
        save_model(model, scaler=None, filepath=test_model_path)

        # Check if file was created
        self.assertTrue(os.path.exists(test_model_path))

        # Load model
        loaded_model, loaded_scaler = load_model(test_model_path)

        # Check if loaded model can make predictions
        predictions_original = model.predict(X_test)
        predictions_loaded = loaded_model.predict(X_test)

        # Check if predictions are identical
        np.testing.assert_array_almost_equal(predictions_original, predictions_loaded)

        # Clean up
        if os.path.exists(test_model_path):
            os.remove(test_model_path)

    def test_model_performance(self):
        """Test if model performance meets minimum requirements."""
        model, X_test, y_test, X_train, y_train = train_model(self.test_df, optimize=False)

        metrics = evaluate_model(model, X_test, y_test)

        # Check if performance is reasonable (not perfect due to random data)
        self.assertGreater(metrics["r2"], -1)  # R² should be > -1
        self.assertLess(metrics["mae"], 200)  # MAE should be reasonable


if __name__ == "__main__":
    unittest.main()
