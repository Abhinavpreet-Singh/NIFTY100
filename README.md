# Nifty 100 Financial Intelligence Platform

A fundamental financial analytics platform that processes raw financial statement data (Balance Sheet, P&L, Cash Flow) for 92 Nifty 100 companies, runs advanced data quality (DQ) validation, and serves insights via a FastAPI backend and an interactive Streamlit dashboard.

---

## Project Structure

```text
NIFTY100/
├── config/              # Screener presets and app configurations
├── data/                # Data warehouse (Excel source datasets & SQLite DB)
├── src/                 # Application source code
│   ├── db/              # Database persistence layer & schema
│   ├── etl/             # Data ingestion and 16 Data Quality (DQ) rules
│   ├── analytics/       # Valuation multipliers, cash flows, & PDF generator
│   ├── api/             # FastAPI REST endpoints (16 endpoints)
│   └── dashboard/       # Streamlit web dashboard pages
├── tests/               # Test suite covering ETL, KPIs, API, and validation
├── output/              # Generated audit logs and test reports
└── reports/             # Compiled PDF Tearsheets, Sectors, and Portfolio Summaries
```

---

## Installation & Setup

### 1. Prerequisites
- **Python**: Version 3.10 to 3.12.x

### 2. Environment Activation
```powershell
# Create virtual environment
python -m venv venv

# Activate on Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Activate on macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

---

## Run Commands

### 1. Run Database Ingestion (ETL)
Rebuild the database, apply cleaning constraints, and generate ingestion audits:
```powershell
python -m src.db.loader
```
*Outputs: SQLite Database (`data/nifty100.db`) and Ingestion Audit (`output/load_audit.csv`)*

### 2. Generate PDF Reports
Compile Tearsheets, Sector Indexes, and Portfolio summaries in PDF format:
```powershell
python -m src.analytics.pdf_generator
```
*Outputs compiled reports under: `reports/`*

### 3. Start FastAPI REST Server
Launch the backend server locally:
```powershell
python -m uvicorn src.api.main:app --port 8000 --reload
```
*API endpoints available at: http://localhost:8000 (Docs at /docs)*

### 4. Start Streamlit Dashboard
Launch the web interface locally:
```powershell
python -m streamlit run src/dashboard/app.py
```
*Dashboard opens at: http://localhost:8501*

---

## Testing

To execute all 114 unit and integration tests (ingestion, ratios, FastAPI, and clustering):
```powershell
python -m pytest -v
```
*Test coverage: 114/114 tests passing.*
