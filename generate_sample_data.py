#!/usr/bin/env python3
"""
Generate sample tourism data for testing and demonstration.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_tourism_data(num_days=730, output_file="data/raw/tourism_data.csv"):
    """
    Generate synthetic tourism booking data.

    Args:
        num_days: Number of days of data to generate (default: 730 = 2 years)
        output_file: Path to save the CSV file
    """
    print(f"Generating {num_days} days of tourism data...")

    # Set random seed for reproducibility
    np.random.seed(42)

    # Generate dates
    start_date = datetime(2023, 1, 1)
    dates = [start_date + timedelta(days=i) for i in range(num_days)]

    # Initialize lists
    bookings_list = []
    temperatures = []
    is_holidays = []
    prices = []

    for i, date in enumerate(dates):
        # Seasonal pattern (higher in summer)
        day_of_year = date.timetuple().tm_yday
        seasonal_factor = 50 * np.sin(2 * np.pi * day_of_year / 365 - np.pi/2)

        # Weekly pattern (higher on weekends)
        day_of_week = date.weekday()
        weekend_boost = 20 if day_of_week >= 5 else 0

        # Holiday pattern (randomly assign ~10% as holidays)
        is_holiday = 1 if np.random.random() < 0.10 else 0
        holiday_boost = 30 if is_holiday else 0

        # Temperature (seasonal variation)
        temp = int(15 + 15 * np.sin(2 * np.pi * day_of_year / 365 - np.pi/2) + np.random.normal(0, 3))
        temp = max(0, min(40, temp))  # Clamp between 0 and 40

        # Price (varies with season and demand)
        base_price = 80
        seasonal_price = int(20 * np.sin(2 * np.pi * day_of_year / 365 - np.pi/2))
        price = base_price + seasonal_price + np.random.randint(-5, 6)
        price = max(50, min(150, price))  # Clamp between 50 and 150

        # Bookings (influenced by all factors + noise)
        base_bookings = 100
        trend = i * 0.05  # Slight upward trend
        noise = np.random.normal(0, 15)

        bookings = int(base_bookings + seasonal_factor + weekend_boost + holiday_boost + trend + noise)
        bookings = max(20, bookings)  # Minimum 20 bookings

        # Append to lists
        bookings_list.append(bookings)
        temperatures.append(temp)
        is_holidays.append(is_holiday)
        prices.append(price)

    # Create DataFrame
    df = pd.DataFrame({
        'date': dates,
        'bookings': bookings_list,
        'temperature': temperatures,
        'is_holiday': is_holidays,
        'price': prices
    })

    # Save to CSV
    df.to_csv(output_file, index=False)

    print(f"✅ Data saved to {output_file}")
    print(f"\nData Summary:")
    print(f"  Rows: {len(df)}")
    print(f"  Date Range: {df['date'].min()} to {df['date'].max()}")
    print(f"  Avg Bookings: {df['bookings'].mean():.1f}")
    print(f"  Avg Temperature: {df['temperature'].mean():.1f}°C")
    print(f"  Avg Price: {df['price'].mean():.1f}€")
    print(f"  Holiday Days: {df['is_holiday'].sum()} ({(df['is_holiday'].sum()/len(df)*100):.1f}%)")
    print(f"\nFirst few rows:")
    print(df.head())


if __name__ == "__main__":
    generate_tourism_data()
