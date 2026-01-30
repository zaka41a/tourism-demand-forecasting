# Contributing to Tourism Demand Forecasting

First off, thank you for considering contributing to Tourism Demand Forecasting! 🎉

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)

## 📜 Code of Conduct

This project and everyone participating in it is governed by respect and professionalism. Please be kind and constructive in your communications.

## 🤝 How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates.

**When reporting bugs, include:**
- Clear, descriptive title
- Detailed description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)
- Error messages and stack traces

**Example:**
```
Title: Model training fails with large datasets

Description:
When training with datasets > 100K rows, the process crashes with
a MemoryError.

Steps to reproduce:
1. Load data with 150K rows
2. Run: python train.py --optimize
3. Observe crash after ~5 minutes

Environment:
- OS: Ubuntu 22.04
- Python: 3.12.0
- RAM: 8GB
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues.

**Include:**
- Clear description of the enhancement
- Rationale (why is this useful?)
- Possible implementation approach
- Examples of how it would work

### Pull Requests

We actively welcome your pull requests!

## 🛠️ Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/tourism-demand-forecasting.git
cd tourism-demand-forecasting
```

### 2. Create Virtual Environment

```bash
python3.12 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Install main dependencies
pip install -r requirements.txt

# Install development dependencies
pip install flake8 black pylint pytest-cov
```

### 4. Setup Project

```bash
python setup_dirs.py
```

### 5. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

## 🔄 Pull Request Process

### 1. Make Your Changes

- Write clean, readable code
- Follow the coding standards below
- Add tests for new features
- Update documentation as needed

### 2. Test Your Changes

```bash
# Run tests
pytest tests/ -v

# Check coverage
pytest tests/ --cov=src --cov-report=term

# Lint your code
flake8 src/ --max-line-length=100
black --check src/ tests/ --line-length=100
```

### 3. Commit Your Changes

Use clear, descriptive commit messages:

```bash
# Good commit messages:
git commit -m "Add LSTM model implementation for time series forecasting"
git commit -m "Fix memory leak in data preprocessing pipeline"
git commit -m "Update README with Docker installation instructions"

# Bad commit messages:
git commit -m "fix bug"
git commit -m "changes"
git commit -m "update"
```

**Commit Message Format:**
```
<type>: <subject>

<body (optional)>

<footer (optional)>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### 4. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:
- Clear title describing the change
- Detailed description of what was changed and why
- Link to related issues
- Screenshots (if UI changes)

### 5. PR Review Process

- Maintainers will review your PR
- Address any requested changes
- Once approved, your PR will be merged

## 📝 Coding Standards

### Python Style

We follow PEP 8 with some modifications:

```python
# Maximum line length: 100 characters
# Use 4 spaces for indentation
# Use descriptive variable names

# Good:
def calculate_demand_forecast(temperature, price, is_holiday):
    """Calculate tourism demand forecast based on input parameters."""
    pass

# Bad:
def calc(t, p, h):
    pass
```

### Docstrings

Use Google-style docstrings:

```python
def train_model(df, optimize=False):
    """
    Train a machine learning model for demand forecasting.

    Args:
        df (pd.DataFrame): Training data with features and target
        optimize (bool): Whether to run hyperparameter optimization

    Returns:
        tuple: (model, X_test, y_test, X_train, y_train)

    Raises:
        ValueError: If dataframe is empty or missing required columns
    """
    pass
```

### Type Hints

Use type hints where beneficial:

```python
from typing import Tuple, Optional
import pandas as pd

def load_data(path: str) -> pd.DataFrame:
    """Load data from CSV file."""
    pass

def train_model(df: pd.DataFrame, optimize: bool = False) -> Tuple[object, ...]:
    """Train model and return results."""
    pass
```

### Error Handling

Always handle errors appropriately:

```python
# Good:
try:
    df = load_data(path)
except FileNotFoundError:
    logger.error(f"File not found: {path}")
    raise
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise

# Bad:
try:
    df = load_data(path)
except:
    pass
```

## 🧪 Testing Guidelines

### Writing Tests

- Place tests in `tests/` directory
- Name test files as `test_<module>.py`
- Name test functions as `test_<functionality>`
- Use descriptive test names

```python
# Good test names:
def test_load_data_handles_missing_file():
    """Test that load_data raises FileNotFoundError for missing files."""
    pass

def test_model_training_returns_expected_types():
    """Test that train_model returns correct data types."""
    pass

# Bad test names:
def test_data():
    pass

def test1():
    pass
```

### Test Coverage

- Aim for 80%+ code coverage
- Test edge cases and error conditions
- Test both success and failure scenarios

```python
def test_evaluate_model_with_valid_input():
    """Test evaluation with valid input data."""
    # Test normal case

def test_evaluate_model_with_empty_input():
    """Test evaluation handles empty input gracefully."""
    # Test edge case

def test_evaluate_model_raises_on_invalid_type():
    """Test evaluation raises TypeError for invalid input."""
    # Test error condition
```

## 📚 Documentation

### Code Comments

- Use comments to explain **why**, not **what**
- Keep comments up to date with code changes
- Avoid obvious comments

```python
# Good:
# Use log transformation to handle skewed distribution
transformed_data = np.log1p(data)

# Bad:
# Transform data
transformed_data = np.log1p(data)
```

### README Updates

If your changes affect usage:
- Update README.md
- Update QUICKSTART.md if needed
- Add examples where appropriate

## 🎯 Areas We Need Help

### High Priority
- [ ] LSTM/GRU model implementations
- [ ] Real-time data ingestion pipeline
- [ ] API endpoint development
- [ ] Performance optimizations

### Medium Priority
- [ ] Additional visualization types
- [ ] More comprehensive tests
- [ ] Documentation improvements
- [ ] Example notebooks

### Low Priority
- [ ] Code refactoring
- [ ] Minor bug fixes
- [ ] Styling improvements

## 🏆 Recognition

Contributors will be:
- Added to the Contributors section in README
- Mentioned in release notes
- Acknowledged in CHANGELOG

## ❓ Questions?

- Open an issue with the `question` label
- Email: zaksab98@gmail.com

## 📖 Resources

- [Python Style Guide (PEP 8)](https://www.python.org/dev/peps/pep-0008/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Pytest Documentation](https://docs.pytest.org/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)

---

Thank you for contributing! 🚀
