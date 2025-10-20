# Python Hybrid Test Framework

## Setup

### Create Virtual Environment
```bash
python3 -m venv venv
```

### Activate Environment
```bash
# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
playwright install chromium
```

## Console Steps

### Complete Setup and Run
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
playwright install chromium

# Run tests
pytest test_hybrid.py
```

## Run Tests
```bash
pytest
```

## Allure Reports

### Generate and View Reports
```bash
# Run tests with allure results
pytest --alluredir=reports/allure-results

# Generate HTML report
allure generate reports/allure-results -o reports/allure-report --clean

# Serve report (opens browser automatically)
allure serve reports/allure-results
```

## Structure
- `conftest.py` - Global test fixtures
- `framework/` - Test framework components
- `tests/` - Test cases organized by type
- `config/` - Configuration files
- `reports/` - Test reports and results
- `pytest.ini` - Pytest configuration