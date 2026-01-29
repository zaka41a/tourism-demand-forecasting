"""
Advanced visualization functions for Tourism Demand Forecasting.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np


def plot_time_series(df, target_col='bookings', title='Time Series Analysis'):
    """
    Plot time series with trend and seasonality.

    Args:
        df: DataFrame with date and target columns
        target_col: Name of the target column
        title: Plot title
    """
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Original Time Series', 'Rolling Statistics'),
        vertical_spacing=0.1
    )

    # Original time series
    fig.add_trace(
        go.Scatter(x=df['date'], y=df[target_col], name='Original',
                   line=dict(color='#667eea', width=1)),
        row=1, col=1
    )

    # Rolling mean and std
    rolling_mean = df[target_col].rolling(window=30).mean()
    rolling_std = df[target_col].rolling(window=30).std()

    fig.add_trace(
        go.Scatter(x=df['date'], y=rolling_mean, name='30-day MA',
                   line=dict(color='#f56565', width=2)),
        row=2, col=1
    )

    fig.add_trace(
        go.Scatter(x=df['date'], y=rolling_std, name='30-day Std',
                   line=dict(color='#48bb78', width=2)),
        row=2, col=1
    )

    fig.update_layout(height=600, title_text=title, showlegend=True)
    return fig


def plot_feature_importance(model, feature_names, top_n=10):
    """
    Plot feature importance from trained model.

    Args:
        model: Trained model with feature_importances_ attribute
        feature_names: List of feature names
        top_n: Number of top features to display
    """
    importance_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': model.feature_importances_
    }).sort_values('Importance', ascending=False).head(top_n)

    fig = px.bar(
        importance_df,
        x='Importance',
        y='Feature',
        orientation='h',
        title=f'Top {top_n} Most Important Features',
        color='Importance',
        color_continuous_scale='Viridis'
    )

    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    return fig


def plot_residuals(y_true, y_pred):
    """
    Plot residual analysis.

    Args:
        y_true: True values
        y_pred: Predicted values
    """
    residuals = y_true - y_pred

    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            'Residuals vs Predicted',
            'Residuals Distribution',
            'Q-Q Plot',
            'Residuals Over Time'
        )
    )

    # Residuals vs Predicted
    fig.add_trace(
        go.Scatter(x=y_pred, y=residuals, mode='markers',
                   marker=dict(color='#667eea', opacity=0.6),
                   name='Residuals'),
        row=1, col=1
    )
    fig.add_hline(y=0, line_dash="dash", line_color="red", row=1, col=1)

    # Residuals Distribution
    fig.add_trace(
        go.Histogram(x=residuals, nbinsx=30,
                     marker=dict(color='#48bb78'),
                     name='Distribution'),
        row=1, col=2
    )

    # Q-Q Plot
    from scipy import stats
    qq = stats.probplot(residuals, dist="norm")
    fig.add_trace(
        go.Scatter(x=qq[0][0], y=qq[0][1], mode='markers',
                   marker=dict(color='#ed8936'),
                   name='Q-Q'),
        row=2, col=1
    )
    fig.add_trace(
        go.Scatter(x=qq[0][0], y=qq[1][1] + qq[1][0] * qq[0][0],
                   mode='lines', line=dict(color='red', dash='dash'),
                   name='Theoretical'),
        row=2, col=1
    )

    # Residuals over time
    fig.add_trace(
        go.Scatter(y=residuals, mode='lines',
                   line=dict(color='#9f7aea'),
                   name='Time Series'),
        row=2, col=2
    )
    fig.add_hline(y=0, line_dash="dash", line_color="red", row=2, col=2)

    fig.update_layout(height=800, showlegend=True, title_text="Residual Analysis")
    return fig


def plot_correlation_heatmap(df, features):
    """
    Plot correlation heatmap.

    Args:
        df: DataFrame
        features: List of features to include
    """
    corr_matrix = df[features].corr()

    fig = px.imshow(
        corr_matrix,
        text_auto='.2f',
        aspect='auto',
        color_continuous_scale='RdBu_r',
        zmin=-1,
        zmax=1,
        title='Feature Correlation Matrix'
    )

    fig.update_layout(height=600, width=700)
    return fig


def plot_predictions_vs_actual(y_true, y_pred, title='Predictions vs Actual'):
    """
    Plot predicted vs actual values.

    Args:
        y_true: True values
        y_pred: Predicted values
        title: Plot title
    """
    fig = go.Figure()

    # Scatter plot
    fig.add_trace(go.Scatter(
        x=y_true,
        y=y_pred,
        mode='markers',
        marker=dict(color='#667eea', size=8, opacity=0.6),
        name='Predictions'
    ))

    # Perfect prediction line
    min_val = min(y_true.min(), y_pred.min())
    max_val = max(y_true.max(), y_pred.max())
    fig.add_trace(go.Scatter(
        x=[min_val, max_val],
        y=[min_val, max_val],
        mode='lines',
        line=dict(color='red', dash='dash'),
        name='Perfect Prediction'
    ))

    fig.update_layout(
        title=title,
        xaxis_title='Actual Values',
        yaxis_title='Predicted Values',
        height=500,
        width=700
    )

    return fig


def plot_seasonal_patterns(df, target_col='bookings'):
    """
    Plot seasonal patterns by month and day of week.

    Args:
        df: DataFrame with date and target columns
        target_col: Name of target column
    """
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Monthly Pattern', 'Weekly Pattern')
    )

    # Monthly pattern
    monthly_avg = df.groupby('month')[target_col].mean()
    fig.add_trace(
        go.Bar(x=monthly_avg.index, y=monthly_avg.values,
               marker=dict(color='#667eea'),
               name='Monthly'),
        row=1, col=1
    )

    # Weekly pattern
    weekly_avg = df.groupby('day_of_week')[target_col].mean()
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    fig.add_trace(
        go.Bar(x=days, y=weekly_avg.values,
               marker=dict(color='#48bb78'),
               name='Weekly'),
        row=1, col=2
    )

    fig.update_layout(height=400, showlegend=False, title_text="Seasonal Patterns")
    return fig


def create_forecast_plot(dates, actual, predicted, forecast_dates=None, forecast_values=None):
    """
    Create a forecast plot with historical and future predictions.

    Args:
        dates: Historical dates
        actual: Actual values
        predicted: Predicted values for historical period
        forecast_dates: Future dates (optional)
        forecast_values: Future predictions (optional)
    """
    fig = go.Figure()

    # Actual values
    fig.add_trace(go.Scatter(
        x=dates,
        y=actual,
        mode='lines',
        name='Actual',
        line=dict(color='#667eea', width=2)
    ))

    # Historical predictions
    fig.add_trace(go.Scatter(
        x=dates,
        y=predicted,
        mode='lines',
        name='Predicted',
        line=dict(color='#f56565', width=2, dash='dash')
    ))

    # Future forecast
    if forecast_dates is not None and forecast_values is not None:
        fig.add_trace(go.Scatter(
            x=forecast_dates,
            y=forecast_values,
            mode='lines',
            name='Forecast',
            line=dict(color='#48bb78', width=2, dash='dot')
        ))

    fig.update_layout(
        title='Tourism Demand Forecast',
        xaxis_title='Date',
        yaxis_title='Bookings',
        height=500,
        hovermode='x unified'
    )

    return fig


def plot_performance_metrics(metrics_dict):
    """
    Plot model performance metrics.

    Args:
        metrics_dict: Dictionary with metric names and values
    """
    fig = go.Figure()

    metrics_names = list(metrics_dict.keys())
    metrics_values = list(metrics_dict.values())

    fig.add_trace(go.Bar(
        x=metrics_names,
        y=metrics_values,
        marker=dict(
            color=metrics_values,
            colorscale='Viridis',
            showscale=True
        ),
        text=[f'{v:.2f}' for v in metrics_values],
        textposition='outside'
    ))

    fig.update_layout(
        title='Model Performance Metrics',
        xaxis_title='Metric',
        yaxis_title='Value',
        height=400
    )

    return fig
