"""
Tourism Demand Forecasting - Source Package

This package contains modules for:
- Data preprocessing and feature engineering
- Model training and optimization
- Model evaluation with multiple metrics
"""

__version__ = "2.0.0"
__author__ = "zaka41a"

from .data_preprocessing import load_and_clean_data, scale_features
from .model import train_model, save_model, load_model, optimize_model
from .evaluation import evaluate_model

__all__ = [
    "load_and_clean_data",
    "scale_features",
    "train_model",
    "save_model",
    "load_model",
    "optimize_model",
    "evaluate_model",
]
