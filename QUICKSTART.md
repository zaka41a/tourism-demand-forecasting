# 🚀 Quick Start Guide - Tourism Demand Forecasting

Get up and running in 5 minutes!

## ⚡ Installation

```bash
# Clone repository
git clone https://github.com/yourusername/tourism-demand-forecasting.git
cd tourism-demand-forecasting

# Create virtual environment
python3.12 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 📊 Launch Dashboard

The fastest way to explore the project:

```bash
streamlit run dashboard/app.py
```

This will open the interactive dashboard in your browser at `http://localhost:8501`

## 🎓 Train Your First Model

### Option 1: Quick Training (Default)
```bash
python train.py
```

### Option 2: Optimized Training (Better but slower)
```bash
python train.py --optimize
```

### Option 3: Custom Data
```bash
python train.py --data path/to/your/data.csv
```

## 📝 Using Jupyter Notebooks

```bash
# Start Jupyter
jupyter notebook

# Open notebooks in order:
# 1. notebooks/01_data_exploration.ipynb
# 2. notebooks/02_feature_engineering.ipynb
# 3. notebooks/03_model_training.ipynb
```

## 🧪 Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

## 📦 Project Structure Overview

```
├── src/                    # Core ML code
├── dashboard/              # Streamlit app
├── notebooks/              # Jupyter notebooks
├── tests/                  # Unit tests
├── data/                   # Data files
├── models/                 # Saved models
├── config.py              # Configuration
└── train.py               # Training script
```

## 🎯 Quick API Usage

```python
# Load and train
from src import load_and_clean_data, train_model, evaluate_model

df = load_and_clean_data("data/raw/tourism_data.csv")
model, X_test, y_test, X_train, y_train = train_model(df)
metrics = evaluate_model(model, X_test, y_test)

print(f"R² Score: {metrics['r2']:.4f}")
```

## 🔧 Configuration

Edit `config.py` to customize:
- Model parameters
- Feature selection
- File paths
- Performance thresholds

## 📚 Next Steps

1. ✅ Launch the dashboard to explore visualizations
2. ✅ Train a model with your own data
3. ✅ Check `README.md` for detailed documentation
4. ✅ Explore notebooks for in-depth analysis
5. ✅ Run tests to verify your setup

## ❓ Troubleshooting

### Dashboard won't start?
```bash
pip install --upgrade streamlit
```

### Import errors?
```bash
pip install -r requirements.txt --force-reinstall
```

### Data not found?
Place your CSV file in `data/raw/` with columns:
- date, bookings, temperature, is_holiday, price

## 🆘 Need Help?

- 📖 Check `README.md` for full documentation
- 🐛 Open an issue on GitHub
- 📧 Contact: your.email@example.com

**Happy Forecasting! 🌍📈**
