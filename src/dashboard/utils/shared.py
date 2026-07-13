"""
Shared Utilities for Nifty 100 Dashboard
Handles SQLite database loading, caching, and custom sidebar navigation.
Implements strictly modern Light Theme (White Mode) with Times New Roman typography.
"""

import os
import sqlite3
import pandas as pd
import streamlit as st

# Strictly modern White Mode CSS Theme with Times New Roman typography
THEME_CSS = """
<style>
/* Hide default streamlit page list in sidebar */
[data-testid="sidebar-nav"] {
    display: none !important;
}

/* Base Light Theme styling */
.stApp {
    background-color: #ffffff;
    color: #1f2328;
    font-family: 'Times New Roman', Georgia, Times, serif !important;
}

/* Times New Roman on all elements */
h1, h2, h3, h4, h5, h6, p, span, div, label, input, button, select, table, th, td {
    font-family: 'Times New Roman', Georgia, Times, serif !important;
}

/* Sidebar styling - modern clean light-grey */
[data-testid="stSidebar"] {
    background-color: #f6f8fa !important;
    border-right: 1px solid #d0d7de !important;
}

/* Metric tile styling - modern clean white card with border & shadow */
div[data-testid="metric-container"] {
    background-color: #ffffff !important;
    border: 1px solid #d0d7de !important;
    padding: 18px !important;
    border-radius: 6px !important;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05) !important;
    color: #1f2328 !important;
}

/* Text inside metric */
div[data-testid="metric-container"] label {
    color: #57606a !important;
    font-size: 14px !important;
    font-weight: 600 !important;
}

div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
    color: #0969da !important;
    font-size: 26px !important;
    font-weight: bold !important;
}

/* Input boxes & selectbox styling */
.stTextInput>div>div>input, .stSelectbox>div>div>div {
    background-color: #ffffff !important;
    color: #1f2328 !important;
    border: 1px solid #d0d7de !important;
    border-radius: 6px !important;
}

/* Buttons and primary color - modern GitHub green */
.stButton>button {
    background-color: #1a7f37 !important;
    color: white !important;
    border-radius: 6px !important;
    border: 1px solid rgba(27, 31, 36, 0.15) !important;
    font-weight: 600 !important;
    padding: 6px 16px !important;
    transition: background-color 0.2s ease !important;
}
.stButton>button:hover {
    background-color: #1b8c3f !important;
}

/* Custom horizontal line */
hr {
    border-top: 1px solid #d0d7de !important;
    margin: 20px 0 !important;
}

/* Table container styling */
.stDataFrame {
    border: 1px solid #d0d7de !important;
    border-radius: 6px !important;
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
        "<h2 style='color: #0969da; margin-bottom: 5px; font-family: \"Times New Roman\", serif;'>Nifty 100</h2>"
        "<p style='color: #57606a; font-size: 13px; font-family: \"Times New Roman\", serif;'>Financial Intelligence Platform</p>"
        "</div>"
        "<hr style='border-top: 1px solid #d0d7de; margin: 10px 0;'>",
        unsafe_allow_html=True
    )
    
    # Custom links styled for white mode
    st.sidebar.page_link("src/dashboard/app.py", label="🏠 Home / Overview")
    st.sidebar.page_link("src/dashboard/pages/company.py", label="🏢 Company Profile")
    st.sidebar.page_link("src/dashboard/pages/screener.py", label="🔍 Financial Screener")
    st.sidebar.page_link("src/dashboard/pages/peers.py", label="👥 Peer Comparison")
    st.sidebar.page_link("src/dashboard/pages/trends.py", label="📈 Trend Analysis")
    st.sidebar.page_link("src/dashboard/pages/sectors.py", label="📊 Sector Analysis")
    st.sidebar.page_link("src/dashboard/pages/capital.py", label="🗺️ Capital Allocation Map")
    st.sidebar.page_link("src/dashboard/pages/documents.py", label="📄 Annual Reports")
    
    st.sidebar.markdown(
        "<div style='position: fixed; bottom: 10px; left: 10px; font-size: 11px; color: #57606a; font-family: \"Times New Roman\", serif;'>"
        "v1.0.0 | Google DeepMind Pair"
        "</div>",
        unsafe_allow_html=True
    )
