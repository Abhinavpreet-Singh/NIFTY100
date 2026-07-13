"""
Shared Utilities for Nifty 100 Dashboard
Handles SQLite database loading, caching, and custom sidebar navigation.
Implements dual dark/light responsive layout using CSS variables, defaulting to Light Mode.
Optimized for full width with compact spacing and Times New Roman typography.
"""

import os
import sqlite3
import pandas as pd
import streamlit as st

# Strictly modern hybrid CSS Theme supporting both Dark and Light modes natively
THEME_CSS = """
<style>
/* Hide default streamlit page list in sidebar */
[data-testid="stSidebarNav"] {
    display: none !important;
}

/* Base styling - Times New Roman override */
.stApp {
    font-family: 'Times New Roman', Georgia, Times, serif !important;
}

h1, h2, h3, h4, h5, h6, p, span, div, label, input, button, select, table, th, td {
    font-family: 'Times New Roman', Georgia, Times, serif !important;
}

/* Compact spacing and Full-Width layout (No wastage) */
.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 1.5rem !important;
    padding-left: 2.5rem !important;
    padding-right: 2.5rem !important;
    max-width: 96% !important; /* Full width optimization */
}

/* Enlarge typography with clean, compact margins */
h1 {
    font-size: 34px !important;
    font-weight: 800 !important;
    margin-bottom: 15px !important;
}
h2 {
    font-size: 24px !important;
    font-weight: 700 !important;
    margin-top: 15px !important;
    margin-bottom: 10px !important;
}
h3 {
    font-size: 19px !important;
    font-weight: 600 !important;
}
p, span, label, td, th {
    font-size: 15px !important;
    line-height: 1.5 !important;
}

/* Metric tile styling - adaptive to both light and dark modes */
div[data-testid="metric-container"] {
    background-color: rgba(128, 128, 128, 0.05) !important;
    border: 1px solid rgba(128, 128, 128, 0.15) !important;
    padding: 12px 18px !important;
    border-radius: 6px !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02) !important;
}

/* Text inside metric */
div[data-testid="metric-container"] label {
    font-size: 14px !important;
    font-weight: 600 !important;
}

div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
    color: #0969da !important;
    font-size: 28px !important;
    font-weight: bold !important;
}

/* Custom sidebar borders and links */
[data-testid="stSidebar"] {
    border-right: 1px solid rgba(128, 128, 128, 0.15) !important;
}

[data-testid="stSidebar"] a p {
    font-size: 16px !important;
    font-weight: 500 !important;
}

/* Input boxes & selectbox styling */
.stTextInput>div>div>input, .stSelectbox>div>div>div {
    border-radius: 6px !important;
    font-size: 15px !important;
}

/* Buttons and primary color - modern green */
.stButton>button {
    background-color: #1a7f37 !important;
    color: white !important;
    border-radius: 6px !important;
    border: 1px solid rgba(27, 31, 36, 0.15) !important;
    font-weight: 600 !important;
    padding: 6px 16px !important;
    font-size: 15px !important;
    transition: background-color 0.2s ease !important;
}
.stButton>button:hover {
    background-color: #1b8c3f !important;
}

/* Custom horizontal line */
hr {
    border-top: 1px solid rgba(128, 128, 128, 0.15) !important;
    margin: 15px 0 !important;
}
</style>
"""

@st.cache_data
def get_db_path() -> str:
    """Gets db path from environment or default"""
    return os.getenv("DB_PATH", "./data/nifty100.db")

@st.cache_data
def load_query(query: str) -> pd.DataFrame:
    """Loads query into dataframe and caches it"""
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def apply_custom_theme():
    """Applies clean premium CSS theme to page"""
    st.markdown(THEME_CSS, unsafe_allow_html=True)

def render_navigation():
    """Renders custom ordered sidebar navigation menu"""
    apply_custom_theme()
    
    st.sidebar.markdown(
        "<div style='text-align: center; padding: 10px 0;'>"
        "<h2 style='color: #0969da; margin-bottom: 5px; font-family: \"Times New Roman\", serif; font-size: 22px !important;'>Nifty 100</h2>"
        "<p style='font-size: 13px !important; font-family: \"Times New Roman\", serif;'>Financial Intelligence Platform</p>"
        "</div>"
        "<hr style='margin: 8px 0;'>",
        unsafe_allow_html=True
    )
    
    # Custom links relative to the script's directory (dashboard/)
    st.sidebar.page_link("app.py", label="🏠 Home / Overview")
    st.sidebar.page_link("pages/company.py", label="🏢 Company Profile")
    st.sidebar.page_link("pages/screener.py", label="🔍 Financial Screener")
    st.sidebar.page_link("pages/peers.py", label="👥 Peer Comparison")
    st.sidebar.page_link("pages/trends.py", label="📈 Trend Analysis")
    st.sidebar.page_link("pages/sectors.py", label="📊 Sector Analysis")
    st.sidebar.page_link("pages/capital.py", label="🗺️ Capital Allocation Map")
    st.sidebar.page_link("pages/documents.py", label="📄 Annual Reports")
