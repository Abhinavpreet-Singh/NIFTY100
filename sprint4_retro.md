# Sprint 4 Retrospective - Dashboard & Valuation Module

**Sprint Theme**: Valuation intelligence, interactive dashboards, and multi-page web applications.
**Duration**: Days 22–28
**Scope**: 8-screen Streamlit application, shared query caching, overvaluation/undervaluation flags, P/B vs ROE scatter plotting, and valuation summary Excel reports.

---

## 1. Deliverables Checklist & Status

| Deliverable ID | Deliverable Description | Target Location / Output | Status |
|---|---|---|---|
| **D-11** | Streamlit multi-page web dashboard scaffolding | `src/dashboard/app.py` + `pages/` | **COMPLETED** (8 screens built) |
| **D-08** | `valuation_summary.xlsx` report detailing P/E and EV/EBITDA | `output/valuation_summary.xlsx` | **COMPLETED** (5 sheets) |
| **D-15** | `valuation_flags.csv` detailing cautions and discounts | `output/valuation_flags.csv` | **COMPLETED** (92 tickers flagged) |
| **D-08** | P/B vs ROE scatter plot generated in reports | `reports/pb_roe_scatter.png` | **COMPLETED** |
| **D-08** | QA integration testing verifying all queries on 10 tickers | `reports/dashboard_qa.md` | **COMPLETED** (All passed) |
| **D-16** | Dashboard user guide and execution instructions | `dashboard_guide.md`, `README.md` | **COMPLETED** |
| **D-16** | Unit tests covering valuation overvaluation flag boundaries | `tests/valuation/` | **COMPLETED** (1 test green, 105/105 total passing) |
| **D-16** | Sprint retrospective report | `sprint4_retro.md` | **COMPLETED** (This document) |

---

## 2. Key Challenges & Resolved Anomalies

### Challenge A: Custom Ordering of Multi-page App Sidebar
*   **Problem**: Streamlit multi-page apps automatically list pages in the sidebar alphabetically by filename. Prepended numeric prefixes (e.g. `01_company.py`) solve ordering but corrupt page URL routing paths (e.g., `/01_company` instead of the specified `/company`).
*   **Solution**: Kept clean page filenames (e.g., `company.py`, `screener.py`) to preserve exact URL path mapping and injected CSS to hide the default Streamlit page sidebar list. We then rendered a custom navigation list using `st.page_link` to preserve custom ordering and layout.

### Challenge B: Information Technology Sector Name
*   **Problem**: Integration tests failed to return records for the `'IT Services'` broad sector name.
*   **Solution**: Inspected database mapping and found that the broad sector is named `'Information Technology'` (which has 5 companies), while `'IT Services'` is only the peer group name. Corrected test queries to use `'Information Technology'`.

### Challenge C: Outlier Detection for Low Standard Deviation
*   **Problem**: In small sector groups where standard deviation `σ` is extremely small or zero, bubble chart outlier flagging can division-by-zero or flag normal performers.
*   **Solution**: Checked that standard deviation is strictly positive (`std > 0`) before applying `2σ` outlier detection boundaries.

---

## 3. Dashboard Statistics

*   **Screens Navigable**: 8 screens (`/` home, `/company` profile, `/screener` filter, `/peers` group comp, `/trends` sparklines, `/sectors` bubble chart, `/capital` allocation treemap, `/documents` BSE filing links).
*   **Query Performance**: Implemented `st.cache_data` in shared loader to cache database results, ensuring page loads are sub-second on subsequent navigation.
*   **Unit Tests**: Added tests for valuation calculations. Total active unit tests are **105/105 green and passing**.
