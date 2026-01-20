import pandas as pd

def load_and_clean_data(path):
    df = pd.read_csv(path, parse_dates=["date"])
    df = df.dropna()
    df["month"] = df["date"].dt.month
    df["day_of_week"] = df["date"].dt.dayofweek
    return df
