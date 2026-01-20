import streamlit as st
import pandas as pd
import joblib

st.title("Tourism Demand Forecast Dashboard")

df = pd.read_csv("../data/raw/tourism_data.csv")

st.line_chart(df["bookings"])
