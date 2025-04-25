# 🛠️ ETL Data Pipeline Project

A modular and scalable ETL (Extract, Transform, Load) pipeline for scraping, cleaning, and loading [Fashion Studio Website created by Dicoding](https://fashion-studio.dicoding.dev/) data into a CSV.

---

## 🚀 Quick Start

### ✅ Prerequisites

Make sure you have the following installed:

- [Python 3.10+](https://www.python.org/downloads/)
- [UV (Ultra Venv)](https://github.com/astral-sh/uv) — install with:
  ```bash
  pip install uv
  ```
- [PostgreSQL](https://www.postgresql.org/download/) — used for data storage

---

### 📦 Installation (with UV)

```bash
# Clone the repository
git clone https://github.com/yourusername/etl-pipeline.git
cd etl-pipeline

# Create and activate a virtual environment with UV
uv venv venv

# Activate the virtual environment
source venv/bin/activate      # On Linux/macOS
.\venv\Scripts\activate       # On Windows

# Install dependencies (including dev dependencies)
uv pip install -e ".[dev]"
```
---
### ▶️ Running the Pipeline

```bash
uv run main.py
```
---

---

### 🧪 Running Tests

To run unit tests:

```bash
python -m pytest tests/
```

To run tests with coverage:

```bash
pytest --cov=utils tests/
```

To generate a coverage report in HTML format:

```bash
pytest --cov=utils --cov-report=html
```

The report will be saved in the `htmlcov/` directory. Open `htmlcov/index.html` in your browser to view it.

---