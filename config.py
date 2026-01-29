"""
Configuration file for Tourism Demand Forecasting project.
"""

import os

# Project directories
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")
MODELS_DIR = os.path.join(PROJECT_ROOT, "models")
LOGS_DIR = os.path.join(PROJECT_ROOT, "logs")

# Create directories if they don't exist
for directory in [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, MODELS_DIR, LOGS_DIR]:
    os.makedirs(directory, exist_ok=True)

# Data files
RAW_DATA_FILE = os.path.join(RAW_DATA_DIR, "tourism_data.csv")
PROCESSED_DATA_FILE = os.path.join(PROCESSED_DATA_DIR, "processed_data.csv")

# Model configuration
MODEL_CONFIG = {
    'n_estimators': 200,
    'max_depth': 15,
    'min_samples_split': 5,
    'min_samples_leaf': 2,
    'random_state': 42,
    'n_jobs': -1
}

# Features configuration
BASE_FEATURES = [
    "temperature",
    "is_holiday",
    "price",
    "month",
    "day_of_week"
]

ADVANCED_FEATURES = [
    "quarter",
    "is_weekend",
    "week_of_year",
    "month_sin",
    "month_cos",
    "day_sin",
    "day_cos",
    "bookings_lag_7",
    "bookings_lag_30",
    "bookings_rolling_7"
]

NUMERICAL_FEATURES = [
    "temperature",
    "price",
    "month",
    "day_of_week",
    "quarter",
    "week_of_year"
]

# Training configuration
TRAIN_TEST_SPLIT_RATIO = 0.2
RANDOM_STATE = 42
CV_FOLDS = 5

# GridSearchCV parameters
GRID_SEARCH_PARAMS = {
    'n_estimators': [100, 200, 300],
    'max_depth': [10, 15, 20, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

# Logging configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = os.path.join(LOGS_DIR, "app.log")

# Dashboard configuration
DASHBOARD_TITLE = "🌍 Tourism Demand Forecast"
DASHBOARD_ICON = "🏨"
DASHBOARD_LAYOUT = "wide"

# Visualization settings
COLOR_SCHEME = {
    'primary': '#667eea',
    'secondary': '#764ba2',
    'success': '#c8e6c9',
    'warning': '#fff9c4',
    'danger': '#ffcdd2'
}

# Model saving
MODEL_SAVE_PATH = os.path.join(MODELS_DIR, "trained_model.pkl")
SCALER_SAVE_PATH = os.path.join(MODELS_DIR, "scaler.pkl")

# Performance thresholds
PERFORMANCE_THRESHOLDS = {
    'mae': 15,  # Maximum acceptable MAE
    'rmse': 20,  # Maximum acceptable RMSE
    'r2': 0.7,  # Minimum acceptable R²
    'mape': 15  # Maximum acceptable MAPE (%)
}
