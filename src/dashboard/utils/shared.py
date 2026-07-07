"""
Shared Utilities for Nifty 100 Dashboard
Handles SQLite database loading, caching, and custom sidebar navigation.
"""

import os
import sqlite3
import pandas as pd
import streamlit as st

# Custom styling to give a premium, state-of-the-art look
THEME_CSS = """
<style>
/* Hide default streamlit page list in sidebar */
[data-testid="sidebar-nav"] {
    display: none !important;
}

/* Custom background and text colors */
.stApp {
    background-color: #0e1117;
    color: #e0e6ed;
    font-family: 'Inter', sans-serif;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background-color: #161b22;
    border-right: 1px solid #30363d;
}

/* Metric tile styling */
div[data-testid="metric-container"] {
    background-color: #21262d;
    border: 1px solid #30363d;
    padding: 15px;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Buttons and primary color */
.stButton>button {
    background-color: #238636;
    color: white;
    border-radius: 6px;
    border: none;
    transition: background-color 0.2s ease;
}
.stButton>button:hover {
    background-color: #2ea043;
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
        "<h2 style='color: #58a6ff; margin-bottom: 5px;'>Nifty 100</h2>"
        "<p style='color: #8b949e; font-size: 13px;'>Financial Intelligence Platform</p>"
        "</div>"
        "<hr style='border-top: 1px solid #30363d; margin: 10px 0;'>",
        unsafe_allow_html=True
    )
    
    # Custom links
    st.sidebar.page_link("src/dashboard/app.py", label="🏠 Home / Overview")
    st.sidebar.page_link("src/dashboard/pages/company.py", label="🏢 Company Profile")
    st.sidebar.page_link("src/dashboard/pages/screener.py", label="🔍 Financial Screener")
    st.sidebar.page_link("src/dashboard/pages/peers.py", label="👥 Peer Comparison")
    st.sidebar.page_link("src/dashboard/pages/trends.py", label="📈 Trend Analysis")
    st.sidebar.page_link("src/dashboard/pages/sectors.py", label="📊 Sector Analysis")
    st.sidebar.page_link("src/dashboard/pages/capital.py", label="🗺️ Capital Allocation Map")
    st.sidebar.page_link("src/dashboard/pages/documents.py", label="📄 Annual Reports")
    
    st.sidebar.markdown(
        "<div style='position: fixed; bottom: 10px; left: 10px; font-size: 11px; color: #8b949e;'>"
        "v1.0.0 | Google DeepMind Pair"
        "</div>",
        unsafe_allow_html=True
    )
