# 🛠️ ETL Data Pipeline Project

A modular and scalable ETL pipeline that:
1. **Extracts** product data from [Fashion Studio](https://fashion-studio.dicoding.dev/)
2. **Transforms** raw data into clean, structured format
3. **Loads** results to CSV with proper error handling

---

## 📦 Core Components

### 🔍 `extract.py` (Web Scraper)
- **Asynchronous scraping** using `aiohttp` for high performance
- **Rate limiting** with semaphores and random delays to avoid bans
- **Automatic retries** with exponential backoff (HTTP 429 handling)
- **Pagination support** with batch processing (50 pages max)
- **Data extraction** using BeautifulSoup (titles, prices, ratings, etc.)

### ♻️ `transform.py` (Data Cleaning)
- **Null handling**: Drops empty/duplicate records
- **Price conversion**: USD → IDR with configurable exchange rate
- **Text normalization**: 
  - Extracts numeric ratings (4.5 from "Rating: 4.5")
  - Parses color counts (3 from "3 Colors")
- **Field standardization**: 
  - Size formats (M, L, XL)
  - Gender categories (Men/Women/Unisex)

### 💾 `load.py` (Data Export)
- **Async CSV writer** using `aiofiles` + pandas
- **Automatic filename generation** with timestamps
- **Directory creation** if not exists
- **Empty data handling** with warning messages

### 🧪 `tests/` (Quality Assurance)
| Test Type       | Coverage                          | Key Features Verified              |
|-----------------|-----------------------------------|------------------------------------|
| `test_extract.py` | HTTP requests & HTML parsing      | Rate limiting, retry logic, data extraction |
| `test_transform.py` | Data cleaning pipelines           | Price conversion, null handling, text parsing |
| `test_load.py`    | File system operations            | CSV formatting, async file writes |

---

## 🚀 Quick Start

### ✅ Prerequisites

| Requirement       | Installation Guide                     |
|-------------------|----------------------------------------|
| Python 3.13      | [Download Python](https://www.python.org/downloads/) |
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
uv run main.py 
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

### Test Types
| Test Type       | Command                      | Location           |
|-----------------|------------------------------|--------------------|
| Extraction      | `pytest tests/test_extract.py` | `tests/test_extract.py` |
| Transformation  | `pytest tests/test_transform.py` | `tests/test_transform.py` |
| Loading         | `pytest tests/test_load.py`  | `tests/test_load.py` |

---

## 🏗️ Basic Project Structure

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