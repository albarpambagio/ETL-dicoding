# 🛠️ ETL Data Pipeline Project

A modular and scalable ETL (Extract, Transform, Load) pipeline for scraping, cleaning, and loading [Fashion Studio Website](https://fashion-studio.dicoding.dev/) data into structured CSV files.

---

## 🚀 Quick Start

### ✅ Prerequisites

| Requirement       | Installation Guide                     |
|-------------------|----------------------------------------|
| Python 3.10+      | [Download Python](https://www.python.org/downloads/) |
| UV (Ultra Venv)   | `pip install uv`                       |

---

## 🛠️ Installation

### Using UV (Recommended)

```bash
# 1. Clone repository
git clone https://github.com/yourusername/etl-pipeline.git
cd etl-pipeline

# 2. Create and activate virtual environment
uv venv venv
source venv/bin/activate      # Linux/macOS
.\venv\Scripts\activate       # Windows

# 3. Install dependencies
uv pip install -e ".[dev]"
```

### Alternative (using pip)

```bash
python -m venv venv
source venv/bin/activate      # Linux/macOS
.\venv\Scripts\activate       # Windows
pip install -e .
```

---

## ▶️ Running the Pipeline

```bash
uv run main.py [--pages 50] [--format csv]
```

**Options**:
- `--pages`: Number of pages to scrape (default: 50)
- `--format`: Output format (csv/json, default: csv)

---

## 🧪 Testing

### Unit Tests
```bash
python -m pytest tests/ -v
```

### Coverage Reports
```bash
# Basic coverage
pytest --cov=src tests/

# HTML report (opens in browser)
pytest --cov=src --cov-report=html && open htmlcov/index.html
```

### Test Types
| Test Type       | Command                      | Location           |
|-----------------|------------------------------|--------------------|
| Extraction      | `pytest tests/test_extract.py` | `tests/test_extract.py` |
| Transformation  | `pytest tests/test_transform.py` | `tests/test_transform.py` |
| Loading         | `pytest tests/test_load.py`  | `tests/test_load.py` |

---

## 🏗️ Project Structure

```
etl-pipeline/
├── utils/
│   ├── extract.py        # Web scraping logic
│   ├── transform.py      # Data cleaning
│   └── load.py           # CSV export
├── tests/
│   ├── test_extract.py
│   ├── test_transform.py
│   └── test_load.py
└── main.py  
    ...             # Pipeline entry point
```

---

## 📊 Sample Output

```csv
Title,Price,Rating,Colors,Size,Gender,Scraped_At
T-shirt 2,1634400.0,3.9,3,M,Women,2025-04-25 16:58:23
Hoodie 3,7950080.0,4.8,3,L,Unisex,2025-04-25 16:58:23
```
---