# Nifty 100 Financial Intelligence Platform

A production-grade fundamental analytics platform that transforms raw financial statement data (P&L, Balance Sheet, Cash Flow) and supplementary datasets into structured relational data for 92 Nifty 100 companies.

---

## 📁 Project Structure

```text
NIFTY100/
├── data/                             # Data warehouse directory
│   ├── raw/                         # Raw input files (read-only Excel files)
│   ├── supporting datasets/          # Supplementary Excel files (sectors, pricing, etc.)
│   └── nifty100.db                  # Target SQLite database (10 tables)
│
├── src/                             # Application source code
│   ├── etl/                         # Ingestion loader & 16 DQ rules validator
│   │   ├── loader.py                # Excel loading & field normalizers
│   │   └── validator.py             # Data quality checks (DQ-01 to DQ-16)
│   ├── db/                          # Database persistence layer
│   │   ├── loader.py                # Ingestion database loader
│   │   └── schema.sql               # SQLite schema definition script
│   ├── analytics/                   # Ratio & CAGR engines (future sprint)
│   └── dashboard/                   # Web interface dashboard (future sprint)
│
├── tests/                           # Unit test suites
│   ├── etl/                         # Normalizer and Excel load tests
│   └── dq/                          # Data Quality rules validation tests
│
├── output/                          # Ingestion & ETL outputs
│   ├── validation_failures.csv      # Logged violations from raw data
│   └── load_audit.csv               # Ingestion stats and success rates
│
├── reports/                         # PDF & Excel output reports (future sprint)
├── logs/                            # Application run logs
├── requirements.txt                 # Pinned dependencies
├── .env.template                    # Environment variables template
└── .env                             # Environment configuration (ignored in Git)
```

---

## ⚙️ Environment Setup

### 1. Prerequisites
- **Python**: version 3.10 to 3.12.x

### 2. Virtual Environment Setup
Create and activate a Python virtual environment:
```powershell
# Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
Install all required packages from `requirements.txt`:
```powershell
pip install -r requirements.txt
```

### 4. Configuration
Copy `.env.template` to `.env` and adjust paths or settings as needed:
```powershell
cp .env.template .env
```

---

## 🚀 Running Ingestion (ETL)

### 1. Run Data Quality Validator
To run the 16 validation rules against the raw files and generate the data quality log:
```powershell
python -m src.etl.validator
```
*Output generated: `output/validation_failures.csv`*

### 2. Load Ingestion into SQLite
To initialize the SQLite database from schema and load all tables (applying rejections, deduplications, and cleaning rules):
```powershell
python -m src.db.loader
```
*Database generated: `data/nifty100.db`*  
*Audit log generated: `output/load_audit.csv`*

---

## 🧪 Testing

To run the complete test suite (normalizer and data quality validation tests):
```powershell
python -m pytest -v
```
Currently: **76/76 unit tests passing** (100% success rate).
