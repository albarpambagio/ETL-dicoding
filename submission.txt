# 🛠️ ETL Data Pipeline Project

A modular and scalable ETL pipeline that:
1. **Extracts** product data from [Fashion Studio](https://fashion-studio.dicoding.dev/)
2. **Transforms** raw data into clean, structured format
3. **Loads** results to CSV with proper error handling

---

## 🌟 Key Features

| Component         | Highlights                                  | Tech Used              |
|------------------|---------------------------------------------|------------------------|
| **Extraction**    | Async scraping with SSL verification        | `aiohttp` + `certifi`  |
| **Transformation**| Currency conversion, text normalization     | `pandas`               |
| **Loading**       | Timestamped CSV exports                     | `aiofiles`             |
| **Testing**       | 90%+ coverage                               | `pytest`               |

---

## 🚀 Installation (Choose Your Method)

### ⚡ Method 1: UV (Ultra-Fast - Recommended)
```bash
# 1. Install UV (if needed)
pip install uv

# 2. Setup environment & dependencies
# Mac/Linux
uv venv && source .venv/bin/activate

# Windows
uv venv 
.venv\Scripts\activate

# 3. Install dependencies
uv pip install -r requirements.txt
```

### 🐍 Method 2: Standard Python
```bash
# 1. Create and activate virtual environment
# Mac/Linux
python -m venv venv && source venv/bin/activate

# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1   

# 2. Install dependencies
pip install -r requirements.txt.
```

---

## ▶️ Running the Pipeline

```bash
# With UV (faster execution)
uv run main.py 

# Standard Python
python main.py
```

---

## 🧪 Testing

### Unit Tests
```bash
pytest tests/ -v
```

### Coverage Reports
```bash
# Basic coverage
pytest --cov=utils tests/

# HTML report (opens in browser)
pytest --cov=utils --cov-report=html && open htmlcov/index.html
```

---

## 📂 Project Structure

```
.
├── utils/
│   ├── extract.py       # Async scraper (rate-limited)
│   ├── transform.py     # Data cleaning pipelines
│   └── load.py          # CSV writer with auto-dir creation
├── tests/               # 90%+ coverage
│   ├── test_extract.py  # Mocked HTTP tests
│   └── ...              # Transformation/load tests
└── main.py              # CLI entry point
```

---

## 📊 Sample Output

```csv
product_id,title,price_idr,rating,scraped_at
123,"Premium T-Shirt",250000.0,4.5,2025-05-01 10:00:00
456,"Denim Jeans",750000.0,4.2,2025-05-01 10:01:00
```


