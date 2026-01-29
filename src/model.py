from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import Ridge
import joblib
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_feature_columns(df):
    """Get available feature columns based on dataframe."""
    base_features = ["temperature", "is_holiday", "price", "month", "day_of_week"]
    optional_features = ["quarter", "is_weekend", "week_of_year",
                        "month_sin", "month_cos", "day_sin", "day_cos",
                        "bookings_lag_7", "bookings_lag_30", "bookings_rolling_7"]

    features = base_features.copy()
    for feat in optional_features:
        if feat in df.columns:
            features.append(feat)

    logger.info(f"Using {len(features)} features: {features}")
    return features


def train_model(df, optimize=False):
    """
    Train a model with optional hyperparameter optimization.

    Args:
        df: DataFrame with features and target
        optimize: If True, perform GridSearchCV for hyperparameter tuning

    Returns:
        tuple: (model, X_test, y_test, X_train, y_train)
    """
    try:
        features = get_feature_columns(df)
        X = df[features]
        y = df["bookings"]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, shuffle=True
        )

        logger.info(f"Training set: {X_train.shape}, Test set: {X_test.shape}")

        if optimize:
            logger.info("Starting hyperparameter optimization with GridSearchCV...")
            model = optimize_model(X_train, y_train)
        else:
            model = RandomForestRegressor(
                n_estimators=200,
                max_depth=15,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42,
                n_jobs=-1
            )
            model.fit(X_train, y_train)

        # Cross-validation score
        cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='r2')
        logger.info(f"Cross-validation R² scores: {cv_scores}")
        logger.info(f"Mean CV R²: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")

        return model, X_test, y_test, X_train, y_train

    except Exception as e:
        logger.error(f"Error training model: {str(e)}")
        raise


def optimize_model(X_train, y_train):
    """
    Optimize model hyperparameters using GridSearchCV.

    Args:
        X_train: Training features
        y_train: Training target

    Returns:
        Optimized model
    """
    try:
        param_grid = {
            'n_estimators': [100, 200, 300],
            'max_depth': [10, 15, 20, None],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4]
        }

        rf = RandomForestRegressor(random_state=42, n_jobs=-1)

        grid_search = GridSearchCV(
            estimator=rf,
            param_grid=param_grid,
            cv=5,
            scoring='r2',
            n_jobs=-1,
            verbose=1
        )

        logger.info("Running GridSearchCV (this may take a few minutes)...")
        grid_search.fit(X_train, y_train)

        logger.info(f"Best parameters: {grid_search.best_params_}")
        logger.info(f"Best CV R² score: {grid_search.best_score_:.4f}")

        return grid_search.best_estimator_

    except Exception as e:
        logger.error(f"Error in hyperparameter optimization: {str(e)}")
        raise


def save_model(model, scaler=None, filepath='models/trained_model.pkl'):
    """
    Save trained model and scaler to disk.

    Args:
        model: Trained model
        scaler: Fitted scaler (optional)
        filepath: Path to save the model
    """
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        model_data = {
            'model': model,
            'scaler': scaler
        }

        joblib.dump(model_data, filepath)
        logger.info(f"Model saved to {filepath}")

    except Exception as e:
        logger.error(f"Error saving model: {str(e)}")
        raise


def load_model(filepath='models/trained_model.pkl'):
    """
    Load trained model and scaler from disk.

    Args:
        filepath: Path to the saved model

    Returns:
        tuple: (model, scaler)
    """
    try:
        model_data = joblib.load(filepath)
        logger.info(f"Model loaded from {filepath}")
        return model_data['model'], model_data.get('scaler')

    except FileNotFoundError:
        logger.error(f"Model file not found: {filepath}")
        raise
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        raise
