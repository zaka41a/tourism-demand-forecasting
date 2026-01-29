# Tourism Demand Forecasting - Makefile
# Simplified commands for common tasks

.PHONY: help install setup train predict dashboard test clean analyze

help:  ## Show this help message
	@echo "Tourism Demand Forecasting - Available Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'
	@echo ""

install:  ## Install dependencies
	pip install -r requirements.txt

setup:  ## Setup project directories
	python setup_dirs.py

train:  ## Train model with default settings
	python train.py

train-optimized:  ## Train model with hyperparameter optimization
	python train.py --optimize

predict:  ## Run prediction in interactive mode
	python predict.py --interactive

dashboard:  ## Launch Streamlit dashboard
	streamlit run dashboard/app.py

analyze:  ## Run exploratory data analysis
	python analyze.py

test:  ## Run all tests
	pytest tests/ -v

test-coverage:  ## Run tests with coverage report
	pytest tests/ --cov=src --cov-report=html --cov-report=term

clean:  ## Clean generated files
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete
	rm -f logs/*.log
	@echo "✅ Cleanup completed"

clean-all: clean  ## Clean everything including models and data
	rm -f models/*.pkl
	rm -f data/processed/*.csv
	@echo "✅ Full cleanup completed"

lint:  ## Run code linting
	@echo "Running flake8..."
	-flake8 src/ --max-line-length=100 --ignore=E501,W503
	@echo "Running pylint..."
	-pylint src/ --max-line-length=100

format:  ## Format code with black
	black src/ tests/ *.py --line-length=100

notebook:  ## Start Jupyter notebook server
	jupyter notebook

freeze:  ## Generate requirements.txt from current environment
	pip freeze > requirements.txt

check:  ## Check if all dependencies are installed
	@echo "Checking dependencies..."
	@python -c "import pandas; print('✓ pandas')"
	@python -c "import numpy; print('✓ numpy')"
	@python -c "import sklearn; print('✓ scikit-learn')"
	@python -c "import streamlit; print('✓ streamlit')"
	@python -c "import plotly; print('✓ plotly')"
	@echo "✅ All core dependencies are installed"

docs:  ## Generate documentation
	@echo "📚 Documentation files:"
	@echo "  - README.md"
	@echo "  - QUICKSTART.md"
	@echo "  - CHANGELOG.md"

quick-start: install setup  ## Quick start setup (install + setup)
	@echo ""
	@echo "✅ Setup complete! Next steps:"
	@echo "  1. Place your data in data/raw/"
	@echo "  2. Run: make train"
	@echo "  3. Run: make dashboard"

all: install setup train dashboard  ## Complete setup and launch
