# Sprint 2 Retrospective - Financial Ratio Engine

**Sprint Theme**: Data Enrichment, Financial KPI Calculations, and Growth CAGR Analysis
**Duration**: Days 8–14
**Scope**: Ingestion data enrichment, formula mathematical calculation, edge case validation, and SQLite persistence.

---

## 1. Deliverables Checklist & Status

| Deliverable ID | Deliverable Description | Target Location / Output | Status |
|---|---|---|---|
| **D-05** | `financial_ratios` table populated for all 92 companies × all years | SQLite database table: `financial_ratios` | **COMPLETED** (1,155 rows loaded) |
| **D-06** | `capital_allocation.csv` file mapping sign-based patterns | `output/capital_allocation.csv` | **COMPLETED** (1,155 rows mapped) |
| **D-13** | ROCE bank analysis and relative performance scoring | `output/sector_roce_notes.csv` | **COMPLETED** (234 records scored) |
| **D-14** | Edge case logging for warning flags and anomalies | `output/ratio_edge_cases.log` | **COMPLETED** |
| **D-14** | Expanded unit test suite covering all ratio formulas and boundaries | `tests/kpi/` | **COMPLETED** (21 KPI unit tests green) |
| **D-14** | Sprint retrospective report | `sprint2_retro.md` | **COMPLETED** (This document) |

---

## 2. Key Challenges & Resolved Anomalies

During the implementation of the KPI formulas, several key structural and financial statement discrepancies were discovered and resolved:

### Challenge A: Structural Leverage in Financial Companies
*   **Problem**: Financial institutions (Banks/NBFCs) leverage customer deposits as core business capital. This results in structurally high Debt-to-Equity ratios (often >5×), which would trigger false warnings in a standard screener.
*   **Solution**: Leveraged the `sectors.broad_sector` classification to bypass D/E threshold flags for any company in the `Financials` sector.

### Challenge B: Bank/NBFC Return on Capital (ROCE)
*   **Problem**: Since financial companies have massive deposits/borrowings on their balance sheets, the traditional capital employed denominator is inflated, causing structurally low ROCE percentages (1-3%) that skew absolute rank.
*   **Solution**: Implemented a **Sector-Relative ROCE Analysis**. The engine now computes annual medians and standard deviations specifically for the financial sector, classifying bank ROCE as `Outperforming` or `Underperforming` relative to peers, and flagging true outliers (>1.5 std from median or negative) in `sector_roce_notes.csv`.

### Challenge C: CAGR Negative Base Values (Turnaround Companies)
*   **Problem**: For companies transitioning from a net loss to a net profit (e.g., Tata Motors, Adani Power), the start value in a 3yr or 5yr window is negative. Standard CAGR formula `((end/start)**(1/n) - 1)` is mathematically undefined in real numbers.
*   **Solution**: The CAGR engine detects negative base values, sets CAGR to `None`, and writes a `[CAGR Turnaround]` flag in the logs to represent a turnaround event.

---

## 3. Database Statistics

*   **Ratios Populated**: **1,155 rows** computed and written to `financial_ratios`.
*   **CAGR Analysis Populated**: **92 rows** computed and updated in `analysis` (representing 3yr, 5yr, and 10yr CAGR for Sales, PAT, and EPS).
*   **Sectors Scored**: All 19 companies classified in `Financials` broad sector scored for relative performance across all available years.

---

## 4. Recommendations for Sprint 3 (Screener Engine)

1.  **Financial Sector Filters**: The stock screener in Sprint 3 MUST ignore D/E or OPM filters for the Financials sector. It should rely on ROE, ROA, or NIM (Net Interest Margin) proxies.
2.  **Turnaround Flags in Growth Screens**: Growth filters should handle `None` CAGR values with a `turnaround_flag=True` status as a highly positive signal rather than rejecting the company outright.
