#!/usr/bin/env python3
"""
Project validation script - checks if everything is set up correctly.

Usage:
    python validate.py
"""

import sys
import os
from pathlib import Path
import importlib.util


def print_header(text):
    """Print formatted header."""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def print_check(name, status, message=""):
    """Print check result."""
    symbol = "✅" if status else "❌"
    print(f"  {symbol} {name:40s} {message}")
    return status


def check_python_version():
    """Check Python version."""
    print_header("🐍 Python Version Check")
    version = sys.version_info
    status = version.major == 3 and version.minor >= 10
    print_check(
        "Python Version",
        status,
        f"({version.major}.{version.minor}.{version.micro})"
    )
    if not status:
        print("  ⚠️  Python 3.10+ required")
    return status


def check_dependencies():
    """Check required packages."""
    print_header("📦 Dependencies Check")

    packages = {
        'pandas': 'pandas',
        'numpy': 'numpy',
        'sklearn': 'scikit-learn',
        'matplotlib': 'matplotlib',
        'seaborn': 'seaborn',
        'streamlit': 'streamlit',
        'plotly': 'plotly',
        'joblib': 'joblib',
        'pytest': 'pytest'
    }

    all_ok = True
    for module, package in packages.items():
        try:
            __import__(module)
            version = None
            try:
                mod = __import__(module)
                version = getattr(mod, '__version__', 'unknown')
            except:
                pass
            version_str = f"v{version}" if version else ""
            print_check(package, True, version_str)
        except ImportError:
            print_check(package, False, "NOT INSTALLED")
            all_ok = False

    return all_ok


def check_directory_structure():
    """Check project directories."""
    print_header("📁 Directory Structure Check")

    required_dirs = [
        'src',
        'dashboard',
        'tests',
        'data',
        'data/raw',
        'data/processed',
        'models',
        'logs',
        'notebooks'
    ]

    all_ok = True
    for dir_path in required_dirs:
        exists = Path(dir_path).exists()
        print_check(dir_path, exists)
        if not exists:
            all_ok = False

    return all_ok


def check_source_files():
    """Check required source files."""
    print_header("📄 Source Files Check")

    required_files = {
        'Core Modules': [
            'src/__init__.py',
            'src/data_preprocessing.py',
            'src/model.py',
            'src/evaluation.py',
            'src/visualizations.py'
        ],
        'Scripts': [
            'train.py',
            'predict.py',
            'analyze.py',
            'setup_dirs.py',
            'validate.py'
        ],
        'Dashboard': [
            'dashboard/app.py'
        ],
        'Tests': [
            'tests/__init__.py',
            'tests/test_preprocessing.py',
            'tests/test_model.py'
        ],
        'Configuration': [
            'config.py',
            'requirements.txt',
            '.gitignore'
        ],
        'Documentation': [
            'README.md',
            'QUICKSTART.md',
            'CHANGELOG.md',
            'CONTRIBUTING.md',
            'LICENSE'
        ]
    }

    all_ok = True
    for category, files in required_files.items():
        print(f"\n  {category}:")
        for file_path in files:
            exists = Path(file_path).exists()
            status = print_check(f"  {file_path}", exists)
            if not exists:
                all_ok = False

    return all_ok


def check_imports():
    """Check if project modules can be imported."""
    print_header("🔧 Module Import Check")

    modules = [
        'src.data_preprocessing',
        'src.model',
        'src.evaluation',
        'src.visualizations',
        'config'
    ]

    all_ok = True
    for module in modules:
        try:
            spec = importlib.util.find_spec(module)
            if spec is not None:
                print_check(module, True)
            else:
                print_check(module, False, "Cannot be found")
                all_ok = False
        except Exception as e:
            print_check(module, False, str(e))
            all_ok = False

    return all_ok


def check_data():
    """Check for data files."""
    print_header("📊 Data Files Check")

    raw_data = Path('data/raw/tourism_data.csv')
    has_data = raw_data.exists()

    print_check("Sample data file", has_data)

    if not has_data:
        print("\n  ℹ️  To add sample data:")
        print("     1. Place your CSV file in data/raw/")
        print("     2. Ensure it has columns: date, bookings, temperature, is_holiday, price")

    return True  # Not critical


def check_docker():
    """Check Docker configuration."""
    print_header("🐳 Docker Configuration Check")

    docker_files = {
        'Dockerfile': Path('Dockerfile').exists(),
        'docker-compose.yml': Path('docker-compose.yml').exists()
    }

    all_ok = True
    for file, exists in docker_files.items():
        print_check(file, exists)
        if not exists:
            all_ok = False

    return all_ok


def check_ci_cd():
    """Check CI/CD configuration."""
    print_header("🔄 CI/CD Configuration Check")

    ci_file = Path('.github/workflows/ci.yml')
    exists = ci_file.exists()
    print_check("GitHub Actions workflow", exists)

    return exists


def run_quick_test():
    """Run a quick functionality test."""
    print_header("🧪 Quick Functionality Test")

    try:
        # Test imports
        from src.data_preprocessing import load_and_clean_data
        from src.model import train_model
        from src.evaluation import evaluate_model
        print_check("Module imports", True)

        # Test config
        import config
        print_check("Config loading", True)

        return True

    except Exception as e:
        print_check("Functionality test", False, str(e))
        return False


def print_summary(results):
    """Print validation summary."""
    print_header("📋 Validation Summary")

    total = len(results)
    passed = sum(results.values())
    failed = total - passed

    print(f"\n  Total Checks:  {total}")
    print(f"  Passed:        {passed} ✅")
    print(f"  Failed:        {failed} ❌")

    percentage = (passed / total) * 100
    print(f"  Success Rate:  {percentage:.1f}%\n")

    if percentage == 100:
        print("  🎉 Congratulations! Your setup is perfect!\n")
        print("  Next steps:")
        print("    1. Run: python train.py")
        print("    2. Run: streamlit run dashboard/app.py")
    elif percentage >= 80:
        print("  ✅ Your setup is good, but some optional components are missing.\n")
        print("  You can still use the main functionality!")
    else:
        print("  ⚠️  Your setup needs attention. Please fix the failed checks.\n")
        print("  Run: make install  (or pip install -r requirements.txt)")
        print("  Run: python setup_dirs.py")


def main():
    """Main validation function."""
    print("\n" + "=" * 70)
    print("  🌍 TOURISM DEMAND FORECASTING - PROJECT VALIDATION")
    print("  Version 2.0 - Enhanced Edition")
    print("=" * 70)

    results = {}

    # Run all checks
    results['Python Version'] = check_python_version()
    results['Dependencies'] = check_dependencies()
    results['Directory Structure'] = check_directory_structure()
    results['Source Files'] = check_source_files()
    results['Module Imports'] = check_imports()
    results['Data Files'] = check_data()
    results['Docker Config'] = check_docker()
    results['CI/CD Config'] = check_ci_cd()
    results['Functionality Test'] = run_quick_test()

    # Print summary
    print_summary(results)

    # Exit code
    if all(results.values()):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
