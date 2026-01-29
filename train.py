#!/usr/bin/env python3
"""
Main training script for Tourism Demand Forecasting model.

Usage:
    python train.py                    # Train with default settings
    python train.py --optimize         # Train with hyperparameter optimization
    python train.py --data path.csv    # Train with custom data
"""

import argparse
import logging
import sys
from pathlib import Path

from src.data_preprocessing import load_and_clean_data
from src.model import train_model, save_model
from src.evaluation import evaluate_model
from config import RAW_DATA_FILE, MODEL_SAVE_PATH, LOG_FILE, LOG_FORMAT, LOG_LEVEL

# Setup logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def main():
    """Main training function."""
    parser = argparse.ArgumentParser(
        description="Train Tourism Demand Forecasting Model"
    )
    parser.add_argument(
        "--data",
        type=str,
        default=RAW_DATA_FILE,
        help="Path to training data CSV file"
    )
    parser.add_argument(
        "--optimize",
        action="store_true",
        help="Run hyperparameter optimization (slower but better results)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=MODEL_SAVE_PATH,
        help="Path to save the trained model"
    )

    args = parser.parse_args()

    logger.info("="*60)
    logger.info("Tourism Demand Forecasting - Model Training")
    logger.info("="*60)

    # Check if data file exists
    if not Path(args.data).exists():
        logger.error(f"Data file not found: {args.data}")
        logger.info("Please ensure your data file exists at the specified path.")
        sys.exit(1)

    try:
        # 1. Load and preprocess data
        logger.info(f"Loading data from: {args.data}")
        df = load_and_clean_data(args.data)
        logger.info(f"Data loaded successfully: {df.shape}")

        # 2. Train model
        logger.info("Starting model training...")
        if args.optimize:
            logger.info("Hyperparameter optimization enabled (this may take several minutes)")

        model, X_test, y_test, X_train, y_train = train_model(df, optimize=args.optimize)
        logger.info("Model training completed!")

        # 3. Evaluate model
        logger.info("Evaluating model performance...")
        metrics = evaluate_model(model, X_test, y_test)

        logger.info("="*60)
        logger.info("MODEL PERFORMANCE METRICS")
        logger.info("="*60)
        logger.info(f"Mean Absolute Error (MAE):       {metrics['mae']:.2f}")
        logger.info(f"Root Mean Squared Error (RMSE):  {metrics['rmse']:.2f}")
        logger.info(f"R² Score:                        {metrics['r2']:.4f}")
        logger.info(f"Mean Absolute Percentage Error:  {metrics['mape']:.2f}%")
        logger.info("="*60)

        # 4. Save model
        logger.info(f"Saving model to: {args.output}")
        save_model(model, scaler=None, filepath=args.output)

        logger.info("✅ Training completed successfully!")
        logger.info(f"Model saved to: {args.output}")
        logger.info(f"Log file: {LOG_FILE}")

        # Performance check
        if metrics['r2'] < 0.7:
            logger.warning("⚠️  Model R² score is below 0.7. Consider:")
            logger.warning("   - Using --optimize flag for hyperparameter tuning")
            logger.warning("   - Collecting more training data")
            logger.warning("   - Adding more features")

    except Exception as e:
        logger.error(f"❌ Training failed: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
