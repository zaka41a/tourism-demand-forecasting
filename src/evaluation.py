from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def evaluate_model(model, X_test, y_test):
    """
    Evaluate model performance with multiple metrics.

    Args:
        model: Trained model
        X_test: Test features
        y_test: Test target values

    Returns:
        dict: Dictionary containing all evaluation metrics
    """
    try:
        predictions = model.predict(X_test)

        # Calculate metrics
        mae = mean_absolute_error(y_test, predictions)
        rmse = np.sqrt(mean_squared_error(y_test, predictions))
        r2 = r2_score(y_test, predictions)

        # MAPE (Mean Absolute Percentage Error)
        mape = np.mean(np.abs((y_test - predictions) / y_test)) * 100

        metrics = {
            'mae': mae,
            'rmse': rmse,
            'r2': r2,
            'mape': mape
        }

        logger.info(f"Model Evaluation - MAE: {mae:.2f}, RMSE: {rmse:.2f}, R²: {r2:.4f}, MAPE: {mape:.2f}%")

        return metrics

    except Exception as e:
        logger.error(f"Error evaluating model: {str(e)}")
        raise
