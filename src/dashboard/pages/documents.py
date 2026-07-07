"""
Annual Reports Page for Nifty 100 Dashboard
URL Path: /documents
"""

import streamlit as st
import pandas as pd

from utils.shared import render_navigation, load_query

# Set Page Config
st.set_page_config(
    page_title="Annual Reports - Nifty 100",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Render Custom Sidebar
render_navigation()

st.title("📄 Annual Reports & Corporate Filings")
st.markdown("Search and access annual reports with clickable BSE PDF filing links.")

# 1. Select Ticker
df_companies = load_query("SELECT id, company_name FROM companies ORDER BY id")
company_options = [f"{row['id']} - {row['company_name']}" for _, row in df_companies.iterrows()]

selected_option = st.selectbox("Select Company:", company_options)
ticker = selected_option.split(" - ")[0]

# 2. Fetch documents for this company
query_docs = f"""
    SELECT year, document_name, document_url, document_type
    FROM documents
    WHERE company_id = '{ticker}'
    ORDER BY year DESC
"""

df_docs = load_query(query_docs)

st.subheader(f"Filings Directory: {selected_option.split(' - ')[1]} ({ticker})")

if not df_docs.empty:
    # Build list of filings
    for _, doc in df_docs.iterrows():
        year = doc['year']
        doc_name = doc['document_name'] if pd.notna(doc['document_name']) else "Annual Report Filing"
        url = doc['document_url']
        doc_type = doc['document_type'] if pd.notna(doc['document_type']) else "PDF"
        
        st.markdown(
            f"<div style='background-color: #21262d; border: 1px solid #30363d; padding: 15px; border-radius: 6px; margin-bottom: 10px;'>"
            f"<h5 style='margin-bottom: 5px; color: #58a6ff;'>📅 FY {year} - {doc_name}</h5>"
            f"<p style='margin-bottom: 10px; font-size: 13px; color: #8b949e;'>Type: {doc_type}</p>"
            f"<a href='{url}' target='_blank' style='display: inline-block; background-color: #238636; color: white; padding: 6px 12px; border-radius: 4px; text-decoration: none; font-size: 13px; font-weight: bold;'>📥 Click to View / Download BSE PDF</a>"
            f"</div>",
            unsafe_allow_html=True
        )
else:
    st.markdown(
        "<div style='padding: 20px; background-color: #f8514922; border: 1px solid #f8514955; border-radius: 6px;'>"
        "<h5 style='color: #f85149; margin-bottom: 5px;'>⚠️ Missing Filings</h5>"
        "<p style='color: #e0e6ed; margin: 0;'>No annual report filings could be found for this company in the database.</p>"
        "</div>",
        unsafe_allow_html=True
    )
