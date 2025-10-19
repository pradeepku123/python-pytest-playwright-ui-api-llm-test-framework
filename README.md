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
pytest test_hybrid.py
```

## Structure
- `conftest.py` - Test fixtures for browser and API sessions
- `test_hybrid.py` - Sample hybrid tests
- `pytest.ini` - Pytest configuration