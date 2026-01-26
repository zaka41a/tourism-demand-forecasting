<div align="center">
   
# 🌍 Tourism Demand Forecasting

![Status](https://img.shields.io/badge/Status-In_Progress-yellow) ![Python](https://img.shields.io/badge/Python-3.12-blue) ![Libraries](https://img.shields.io/badge/Libraries-Pandas%20|%20NumPy%20|%20Scikit-learn%20|%20Matplotlib%20|%20Streamlit-orange)

</div>

---

## 📌 Project Description

This project aims to **forecast tourism demand** using historical data.  
The goal is to help tourism businesses make informed decisions about **resource allocation, pricing, and operational planning**.  

**In short:**  
- Explore historical booking data 📊  
- Create features from dates, prices, holidays, and weather 🌡️  
- Train Machine Learning & AI models 🤖  
- Predict bookings for better decision-making 🏨  

---

## 🗂️ Project Structure
```
tourism-demand-forecasting/
│
├── data/
│ ├── raw/ # Raw data
│ └── processed/ # Cleaned / processed data
│
├── notebooks/
│ ├── 01_data_exploration.ipynb # Data exploration & visualization
│ ├── 02_feature_engineering.ipynb # Feature engineering
│ └── 03_model_training.ipynb # Model training & evaluation
│
├── scripts/ # Optional: automation scripts
├── app/ # Streamlit interactive dashboard
├── requirements.txt # Required Python packages
└── README.md # Project overview
```

---

## 📊 Data

The dataset includes the following columns:  

| Column        | Type       | Description |
|---------------|-----------|-------------|
| `date`        | datetime  | Booking date |
| `bookings`    | int       | Number of bookings |
| `temperature` | int       | Average temperature |
| `is_holiday`  | int       | Holiday (1 = yes, 0 = no) |
| `price`       | int       | Price per booking |

- No missing values ✅  
- Data combines **historical bookings, weather, and holiday information**  

---

## 🛠️ Tools & Libraries

- **Python 3.12** 🐍  
- **Pandas & NumPy** for data processing 🗃️  
- **Matplotlib & Seaborn** for visualization 📈  
- **Scikit-learn** for machine learning models 🧠  
- **Streamlit** for interactive dashboards 💻  

---

## 🧩 Workflow

1. **Data Exploration** 📊  
   - `df.info()`, `df.describe()`, time series visualization  
2. **Feature Engineering** ⚙️  
   - Extract weekday, month, weekend from `date`  
   - Encode `is_holiday` as categorical variable  
3. **Model Training** 🤖  
   - Target variable: `bookings`  
   - Models: Linear Regression, Random Forest Regressor  
4. **Evaluation & Selection** 📈  
   - Metrics: RMSE, MAE  
   - Choose the best-performing model for predictions  
5. **Dashboard & Visualization** 🖥️  
   - Interactive predictions using Streamlit  

---

## 📈 Results

- The model provides **accurate booking forecasts** ✅  
- Key influencing factors: price, holidays, weekday 💡  
- Practical business value: **resource planning, pricing strategies, marketing optimization**  

---

## ✅ Next Steps

- Expand dataset: more locations, longer periods ⏳  
- Use advanced AI models (e.g., **LSTM for time series**) 📊  
- Deploy Streamlit dashboard for **real-time forecasts** 🚀  

---

## 💻 Installation

```bash
# Create virtual environment
python3.12 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# Install required packages
pip install -r requirements.txt

# Optional: register Jupyter kernel
python -m ipykernel install --user --name tourism-venv --display-name "Python (tourism-venv)"
```

## 📚 References

- Scikit-learn Documentation

- Pandas Documentation

- Streamlit Docs

## 👨‍💻 Author

 **Built by zaka41a ❤️**
