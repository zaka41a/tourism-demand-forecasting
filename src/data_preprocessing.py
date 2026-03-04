import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_and_clean_data(path):
    """
    Load and clean data with enhanced feature engineering.

    Args:
        path: Path to CSV file

    Returns:
        pd.DataFrame: Cleaned dataframe with engineered features
    """
    try:
        logger.info(f"Loading data from {path}")
        df = pd.read_csv(path, parse_dates=["date"])

        initial_rows = len(df)
        df = df.dropna()
        logger.info(f"Removed {initial_rows - len(df)} rows with missing values")

        # Temporal features
        df["month"] = df["date"].dt.month
        df["day_of_week"] = df["date"].dt.dayofweek
        df["quarter"] = df["date"].dt.quarter
        df["is_weekend"] = (df["day_of_week"] >= 5).astype(int)
        df["week_of_year"] = df["date"].dt.isocalendar().week

        # Seasonal features (cyclical encoding)
        df["month_sin"] = np.sin(2 * np.pi * df["month"] / 12)
        df["month_cos"] = np.cos(2 * np.pi * df["month"] / 12)
        df["day_sin"] = np.sin(2 * np.pi * df["day_of_week"] / 7)
        df["day_cos"] = np.cos(2 * np.pi * df["day_of_week"] / 7)

        # Lag features (only add windows that leave enough usable rows)
        lag_columns = []
        if len(df) > 7:
            df["bookings_lag_7"] = df["bookings"].shift(7)
            df["bookings_rolling_7"] = df["bookings"].rolling(window=7).mean()
            lag_columns.extend(["bookings_lag_7", "bookings_rolling_7"])
        if len(df) > 37:
            df["bookings_lag_30"] = df["bookings"].shift(30)
            lag_columns.append("bookings_lag_30")
        if lag_columns:
            df = df.dropna(subset=lag_columns)

        logger.info(f"Feature engineering completed. Shape: {df.shape}")

        return df

    except FileNotFoundError:
        logger.error(f"File not found: {path}")
        raise
    except Exception as e:
        logger.error(f"Error processing data: {str(e)}")
        raise


def scale_features(X_train, X_test, numerical_features):
    """
    Scale numerical features using StandardScaler.

    Args:
        X_train: Training features
        X_test: Test features
        numerical_features: List of numerical feature names

    Returns:
        tuple: Scaled X_train, X_test, and fitted scaler
    """
    try:
        scaler = StandardScaler()

        X_train_scaled = X_train.copy()
        X_test_scaled = X_test.copy()

        X_train_scaled[numerical_features] = scaler.fit_transform(X_train[numerical_features])
        X_test_scaled[numerical_features] = scaler.transform(X_test[numerical_features])

        logger.info(f"Scaled {len(numerical_features)} numerical features")

        return X_train_scaled, X_test_scaled, scaler

    except Exception as e:
        logger.error(f"Error scaling features: {str(e)}")
        raise
