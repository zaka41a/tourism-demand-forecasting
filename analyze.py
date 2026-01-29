#!/usr/bin/env python3
"""
Automated Exploratory Data Analysis (EDA) script.

Usage:
    python analyze.py
    python analyze.py --data path/to/data.csv
    python analyze.py --save-html
"""

import argparse
import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

from src.data_preprocessing import load_and_clean_data
from config import RAW_DATA_FILE


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")


def basic_info(df):
    """Print basic dataset information."""
    print_section("📊 BASIC DATASET INFORMATION")

    print(f"Dataset Shape: {df.shape[0]} rows × {df.shape[1]} columns")
    print(f"Memory Usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    print(f"Date Range: {df['date'].min()} to {df['date'].max()}")
    print(f"Duration: {(df['date'].max() - df['date'].min()).days} days")

    print("\n📋 Column Information:")
    print(df.dtypes.to_string())

    print("\n❓ Missing Values:")
    missing = df.isnull().sum()
    if missing.sum() == 0:
        print("  ✅ No missing values found!")
    else:
        print(missing[missing > 0].to_string())


def statistical_summary(df):
    """Print statistical summary."""
    print_section("📈 STATISTICAL SUMMARY")

    numeric_cols = df.select_dtypes(include=[np.number]).columns
    print(df[numeric_cols].describe().to_string())

    print("\n📊 Skewness:")
    skewness = df[numeric_cols].skew()
    for col, skew in skewness.items():
        interpretation = "symmetric" if abs(skew) < 0.5 else ("left-skewed" if skew < 0 else "right-skewed")
        print(f"  {col:20s}: {skew:7.2f} ({interpretation})")


def correlation_analysis(df):
    """Analyze correlations."""
    print_section("🔗 CORRELATION ANALYSIS")

    numeric_cols = ['bookings', 'temperature', 'price', 'is_holiday', 'month', 'day_of_week']
    available_cols = [col for col in numeric_cols if col in df.columns]

    corr_with_target = df[available_cols].corr()['bookings'].sort_values(ascending=False)

    print("Correlation with Bookings:")
    for col, corr in corr_with_target.items():
        if col != 'bookings':
            strength = "Strong" if abs(corr) > 0.5 else ("Moderate" if abs(corr) > 0.3 else "Weak")
            direction = "positive" if corr > 0 else "negative"
            print(f"  {col:20s}: {corr:7.4f} ({strength} {direction})")


def temporal_analysis(df):
    """Analyze temporal patterns."""
    print_section("📅 TEMPORAL PATTERNS")

    # Monthly analysis
    print("Monthly Statistics:")
    monthly_stats = df.groupby('month')['bookings'].agg(['mean', 'std', 'min', 'max'])
    print(monthly_stats.to_string())

    print("\n📆 Day of Week Statistics:")
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dow_stats = df.groupby('day_of_week')['bookings'].agg(['mean', 'std'])
    dow_stats.index = [days[i] for i in dow_stats.index]
    print(dow_stats.to_string())

    # Weekend vs Weekday
    if 'is_weekend' in df.columns:
        print("\n🏖️  Weekend vs Weekday:")
        weekend_avg = df[df['is_weekend'] == 1]['bookings'].mean()
        weekday_avg = df[df['is_weekend'] == 0]['bookings'].mean()
        diff_pct = ((weekend_avg - weekday_avg) / weekday_avg) * 100
        print(f"  Weekend Average:  {weekend_avg:.2f}")
        print(f"  Weekday Average:  {weekday_avg:.2f}")
        print(f"  Difference:       {diff_pct:+.1f}%")


def holiday_analysis(df):
    """Analyze holiday impact."""
    print_section("🎉 HOLIDAY IMPACT ANALYSIS")

    holiday_avg = df[df['is_holiday'] == 1]['bookings'].mean()
    normal_avg = df[df['is_holiday'] == 0]['bookings'].mean()
    diff_pct = ((holiday_avg - normal_avg) / normal_avg) * 100

    print(f"Average Bookings on Holidays:     {holiday_avg:.2f}")
    print(f"Average Bookings on Normal Days:  {normal_avg:.2f}")
    print(f"Holiday Premium:                  {diff_pct:+.1f}%")

    holiday_count = df['is_holiday'].sum()
    holiday_pct = (holiday_count / len(df)) * 100
    print(f"\nHoliday Days:                     {holiday_count} ({holiday_pct:.1f}%)")


def price_analysis(df):
    """Analyze pricing patterns."""
    print_section("💰 PRICE ANALYSIS")

    print(f"Average Price:   {df['price'].mean():.2f}€")
    print(f"Price Range:     {df['price'].min():.2f}€ - {df['price'].max():.2f}€")
    print(f"Price Std Dev:   {df['price'].std():.2f}€")

    # Price quartiles and demand
    df['price_quartile'] = pd.qcut(df['price'], q=4, labels=['Low', 'Medium-Low', 'Medium-High', 'High'])
    price_demand = df.groupby('price_quartile')['bookings'].mean()

    print("\n📊 Demand by Price Quartile:")
    print(price_demand.to_string())


def seasonality_analysis(df):
    """Analyze seasonality."""
    print_section("🌍 SEASONALITY ANALYSIS")

    if 'quarter' in df.columns:
        print("Quarterly Statistics:")
        quarterly = df.groupby('quarter')['bookings'].agg(['mean', 'std', 'count'])
        quarterly.index = [f'Q{i}' for i in quarterly.index]
        print(quarterly.to_string())

        print("\n📈 Best and Worst Quarters:")
        best_q = quarterly['mean'].idxmax()
        worst_q = quarterly['mean'].idxmin()
        print(f"  Best Quarter:  {best_q} (avg: {quarterly.loc[best_q, 'mean']:.2f})")
        print(f"  Worst Quarter: {worst_q} (avg: {quarterly.loc[worst_q, 'mean']:.2f})")


def outlier_detection(df):
    """Detect outliers."""
    print_section("🔍 OUTLIER DETECTION")

    numeric_cols = ['bookings', 'temperature', 'price']

    for col in numeric_cols:
        if col in df.columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
            outlier_pct = (len(outliers) / len(df)) * 100

            print(f"{col:15s}: {len(outliers):4d} outliers ({outlier_pct:.2f}%)")
            if len(outliers) > 0:
                print(f"  {'':15s}  Range: [{lower_bound:.2f}, {upper_bound:.2f}]")


def generate_insights(df):
    """Generate business insights."""
    print_section("💡 KEY BUSINESS INSIGHTS")

    insights = []

    # Insight 1: Best booking days
    best_dow = df.groupby('day_of_week')['bookings'].mean().idxmax()
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    insights.append(f"📅 Best booking day: {days[best_dow]}")

    # Insight 2: Best month
    best_month = df.groupby('month')['bookings'].mean().idxmax()
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    insights.append(f"📆 Peak season: {months[best_month-1]}")

    # Insight 3: Temperature correlation
    temp_corr = df['temperature'].corr(df['bookings'])
    if temp_corr > 0.3:
        insights.append(f"🌡️  Strong positive correlation with temperature ({temp_corr:.2f})")

    # Insight 4: Price sensitivity
    price_corr = df['price'].corr(df['bookings'])
    if price_corr < -0.2:
        insights.append(f"💰 Price sensitive market (correlation: {price_corr:.2f})")

    # Insight 5: Holiday impact
    if df['is_holiday'].sum() > 0:
        holiday_boost = ((df[df['is_holiday']==1]['bookings'].mean() /
                         df[df['is_holiday']==0]['bookings'].mean() - 1) * 100)
        if holiday_boost > 10:
            insights.append(f"🎉 Holidays boost demand by {holiday_boost:.1f}%")

    for i, insight in enumerate(insights, 1):
        print(f"{i}. {insight}")


def main():
    """Main analysis function."""
    parser = argparse.ArgumentParser(
        description="Automated Exploratory Data Analysis"
    )
    parser.add_argument(
        "--data",
        type=str,
        default=RAW_DATA_FILE,
        help="Path to data CSV file"
    )
    parser.add_argument(
        "--save-report",
        action="store_true",
        help="Save analysis report to file"
    )

    args = parser.parse_args()

    # Header
    print("\n" + "="*70)
    print("  🌍 TOURISM DEMAND FORECASTING - DATA ANALYSIS")
    print("="*70)
    print(f"\n  Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Data Source: {args.data}")

    # Check if file exists
    if not Path(args.data).exists():
        print(f"\n❌ Error: Data file not found: {args.data}")
        sys.exit(1)

    try:
        # Load data
        print("\n  Loading data...")
        df = load_and_clean_data(args.data)
        print(f"  ✅ Data loaded successfully!")

        # Run analyses
        basic_info(df)
        statistical_summary(df)
        correlation_analysis(df)
        temporal_analysis(df)
        holiday_analysis(df)
        price_analysis(df)
        seasonality_analysis(df)
        outlier_detection(df)
        generate_insights(df)

        print("\n" + "="*70)
        print("  ✅ ANALYSIS COMPLETED SUCCESSFULLY")
        print("="*70 + "\n")

        # Save report if requested
        if args.save_report:
            report_file = f"analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            print(f"💾 Report saved to: {report_file}")

    except Exception as e:
        print(f"\n❌ Analysis failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
