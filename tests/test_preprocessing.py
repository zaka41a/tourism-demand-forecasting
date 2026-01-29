"""
Unit tests for data preprocessing functions.
"""

import unittest
import pandas as pd
import numpy as np
import sys
import os
from datetime import datetime, timedelta

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.data_preprocessing import load_and_clean_data, scale_features


class TestDataPreprocessing(unittest.TestCase):
    """Test cases for data preprocessing module."""

    def setUp(self):
        """Create sample test data."""
        dates = pd.date_range(start="2023-01-01", end="2023-01-31", freq="D")
        self.test_df = pd.DataFrame({
            "date": dates,
            "bookings": np.random.randint(50, 200, len(dates)),
            "temperature": np.random.randint(10, 30, len(dates)),
            "is_holiday": np.random.choice([0, 1], len(dates)),
            "price": np.random.randint(70, 120, len(dates))
        })

        # Save test data
        os.makedirs("data/test", exist_ok=True)
        self.test_file = "data/test/test_data.csv"
        self.test_df.to_csv(self.test_file, index=False)

    def tearDown(self):
        """Clean up test files."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_load_and_clean_data(self):
        """Test data loading and cleaning."""
        df = load_and_clean_data(self.test_file)

        # Check if dataframe is not empty
        self.assertGreater(len(df), 0)

        # Check if required columns exist
        self.assertIn("month", df.columns)
        self.assertIn("day_of_week", df.columns)
        self.assertIn("quarter", df.columns)
        self.assertIn("is_weekend", df.columns)

        # Check data types
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(df["date"]))
        self.assertTrue(pd.api.types.is_integer_dtype(df["month"]))

        # Check value ranges
        self.assertTrue(df["month"].between(1, 12).all())
        self.assertTrue(df["day_of_week"].between(0, 6).all())
        self.assertTrue(df["is_weekend"].isin([0, 1]).all())

    def test_scale_features(self):
        """Test feature scaling."""
        df = load_and_clean_data(self.test_file)

        # Split data
        split_idx = int(len(df) * 0.8)
        X_train = df.iloc[:split_idx]
        X_test = df.iloc[split_idx:]

        numerical_features = ["temperature", "price"]

        X_train_scaled, X_test_scaled, scaler = scale_features(
            X_train, X_test, numerical_features
        )

        # Check if scaling was applied
        self.assertIsNotNone(scaler)

        # Check if scaled features have mean ~0 and std ~1
        for feat in numerical_features:
            train_mean = X_train_scaled[feat].mean()
            train_std = X_train_scaled[feat].std()
            self.assertAlmostEqual(train_mean, 0, delta=0.1)
            self.assertAlmostEqual(train_std, 1, delta=0.1)

    def test_missing_values_handling(self):
        """Test handling of missing values."""
        # Add missing values to test data
        df_with_nan = self.test_df.copy()
        df_with_nan.loc[0, "temperature"] = np.nan
        df_with_nan.loc[1, "price"] = np.nan

        test_file_nan = "data/test/test_data_nan.csv"
        df_with_nan.to_csv(test_file_nan, index=False)

        df_cleaned = load_and_clean_data(test_file_nan)

        # Check if NaN rows were removed
        self.assertFalse(df_cleaned.isnull().any().any())

        # Clean up
        if os.path.exists(test_file_nan):
            os.remove(test_file_nan)


if __name__ == "__main__":
    unittest.main()
