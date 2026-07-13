# Sprints 5 & 6 Retrospective - Intelligence, Reports, API, & Clean UI

**Sprints Theme**: Automated qualitative analysis, ReportLab PDF compilation, scikit-learn statistical clustering, FastAPI REST endpoints, and light-theme UI overhauls.
**Duration**: Days 29–45
**Scope**: 16 FastAPI endpoints, 92 tearsheet PDFs, 11 sector reports, 5 KMeans clusters, Pearson correlation matrix, and light-theme overhaul.

---

## 1. Deliverables Checklist & Status

| Deliverable ID | Deliverable Description | Target Location / Output | Status |
|---|---|---|---|
| **D-14** | `pros_cons_generated.csv` detailing strengths & risks | `output/pros_cons_generated.csv` | **COMPLETED** (92 tickers compiled) |
| **D-14** | `cross_validation.csv` checking parsed vs computed CAGR | `output/cross_validation.csv` | **COMPLETED** |
| **D-11** | `cashflow_intelligence.xlsx` report detailing quality and pattern | `output/cashflow_intelligence.xlsx` | **COMPLETED** (2 tabs) |
| **D-11** | `distress_alerts.csv` flagging accrual & cash burn risks | `output/distress_alerts.csv` | **COMPLETED** |
| **D-12** | `cluster_labels.csv` grouping companies via KMeans | `output/cluster_labels.csv` | **COMPLETED** (5 clusters mapped) |
| **D-12** | `correlation_heatmap.png` plotting KPI correlations | `output/correlation_heatmap.png` | **COMPLETED** |
| **D-12** | `portfolio_stats.csv` & `outlier_report.csv` | `output/` | **COMPLETED** |
| **D-08** | Automated PDF tearsheets (92), sectors (11), portfolio (1) | `reports/` | **COMPLETED** |
| **D-15** | FastAPI REST service (16 endpoints) | `src/api/main.py` | **COMPLETED** |
| **D-15** | Postman API collection | `output/postman_collection.json` | **COMPLETED** |
| **D-16** | HTML test report | `output/pytest_report.html` | **COMPLETED** (All green) |
| **D-16** | Unit tests covering new modules | `tests/` | **COMPLETED** (114/114 passing) |

---

## 2. Key Challenges & Resolved Anomalies

### Challenge A: NaN Values during JSON Serialization
*   **Problem**: Pandas dataframes contain `nan` values (from empty fields). FastAPI's standard json encoder throws a `ValueError` trying to serialize these as they are not compliant with standard JSON specifications.
*   **Solution**: Added a recursive cleaning helper `clean_records` that checks every returned dictionary value. If it encounters a `float` that is `nan` or `inf`, it replaces it with `None` (which correctly encodes as `null` in JSON), ensuring robust API responses.

### Challenge B: Seaborn Package Missing
*   **Problem**: Seaborn was missing in the python virtual environment, preventing correlation heatmap plotting.
*   **Solution**: Plotted the correlation matrix using pure Matplotlib `ax.matshow()`, rotating labels and rendering text annotations manually. This maintains a clean dependency tree.

### Challenge C: Starlette TestClient Version Mismatch
*   **Problem**: In newer Starlette/FastAPI versions, TestClient throws `TypeError: Client.__init__() got an unexpected keyword argument 'app'`.
*   **Solution**: Tested the ASGI app using `httpx.AsyncClient` equipped with an `ASGITransport` wrapper inside pytest. This runs the app in-memory, avoiding local networking bottlenecks and version clashes.
