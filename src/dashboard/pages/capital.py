"""
Capital Allocation Map Page for Nifty 100 Dashboard
URL Path: /capital
"""

import streamlit as st
import plotly.express as px
import pandas as pd

from utils.shared import render_navigation, load_query

# Set Page Config
st.set_page_config(
    page_title="Capital Allocation Map - Nifty 100",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Render Custom Sidebar
render_navigation()

st.title("🗺️ Capital Allocation Pattern Map")
st.markdown("Treemap visualization categorizing Nifty 100 companies by their CFO, CFI, and CFF cash flow patterns.")

# 1. Load latest year (2024-03) cash flows
latest_year = "2024-03"

query_cf = f"""
    SELECT 
        c.id as Ticker,
        c.company_name as [Company Name],
        COALESCE(s.broad_sector, c.sector) as Sector,
        cf.operating_activity as CFO,
        cf.investing_activity as CFI,
        cf.financing_activity as CFF,
        m.market_cap_cr as [Market Cap (Cr)]
    FROM companies c
    JOIN cashflow cf ON c.id = cf.company_id AND cf.year = '{latest_year}'
    LEFT JOIN sectors s ON c.id = s.company_id
    LEFT JOIN market_cap m ON c.id = m.company_id AND m.year = '{latest_year}'
"""

df_cf = load_query(query_cf)

# 2. Categorize companies into 8 allocation patterns
def get_cf_pattern(row):
    cfo = "+" if row['CFO'] >= 0 else "-"
    cfi = "+" if row['CFI'] >= 0 else "-"
    cff = "+" if row['CFF'] >= 0 else "-"
    return f"[{cfo}, {cfi}, {cff}]"

# Description mapping for the 8 pattern labels
pattern_descriptions = {
    "[+, -, -]": "Standard Operations: Reinvesting CFO, repaying debt/paying dividends (Healthy)",
    "[+, -, +]": "Growth Expansion: CFO + financing used for investing (Aggressive Growth)",
    "[+, +, -]": "Cash Harvester: Divesting assets, paying down debt",
    "[+, +, +]": "High Liquidity Accumulation: Inflows from all activities",
    "[-, -, +]": "Startup Stage: Funding operations & investing through debt/equity",
    "[-, -, -]": "Cash Burn: Outflows in all activities (High Risk)",
    "[-, +, +]": "Survival Mode: Selling assets & raising cash to fund operations",
    "[-, +, -]": "Liquidation/Restructuring: CFO/CFF negative, asset sales positive"
}

df_cf['Pattern'] = df_cf.apply(get_cf_pattern, axis=1)
df_cf['Pattern Description'] = df_cf['Pattern'].map(pattern_descriptions)

# Drop any NaNs in crucial columns
df_cf_clean = df_cf.dropna(subset=['Market Cap (Cr)'])

if not df_cf_clean.empty:
    st.subheader("Nifty 100 Cash Allocation Map (FY24)")
    st.markdown("Size: Market Cap (Cr) | Color: Capital Allocation Pattern Category")
    
    # 3. Plot Treemap with premium custom colors representing financial health
    custom_colors = {
        "[+, -, -]": "#1a7f37",  # Soft Green (Healthy)
        "[+, -, +]": "#0969da",  # Soft Blue (Growth)
        "[+, +, -]": "#6e7781",  # Soft Grey (Harvester)
        "[+, +, +]": "#8250df",  # Soft Purple (Liquidity)
        "[-, -, +]": "#d97706",  # Soft Amber (Startup)
        "[-, -, -]": "#cf222e",  # Soft Red (Cash Burn)
        "[-, +, +]": "#bc4c00",  # Soft Orange (Survival)
        "[-, +, -]": "#8c1d1d"   # Dark Red (Liquidation)
    }
    
    fig_tree = px.treemap(
        df_cf_clean,
        path=['Pattern Description', 'Sector', 'Ticker'],
        values='Market Cap (Cr)',
        color='Pattern',
        hover_data=['Company Name', 'CFO', 'CFI', 'CFF'],
        color_discrete_map=custom_colors
    )
    fig_tree.update_layout(
        margin=dict(t=30, b=30, l=10, r=10),
        paper_bgcolor='rgba(0,0,0,0)',
        font_family='Times New Roman'
    )
    st.plotly_chart(fig_tree, use_container_width=True)
    
    st.markdown("<hr style='border-top: 1px solid rgba(128, 128, 128, 0.15); margin: 20px 0;'>", unsafe_allow_html=True)
    
    # 4. Filter List by Pattern Category
    st.subheader("Search Companies by Pattern Category")
    selected_pattern = st.selectbox("Select Capital Pattern Category:", list(pattern_descriptions.keys()))
    
    df_filtered = df_cf[df_cf['Pattern'] == selected_pattern].copy()
    
    st.write(f"**Pattern Description**: {pattern_descriptions[selected_pattern]}")
    st.write(f"**Companies in this category**: {len(df_filtered)}")
    
    df_filtered_display = df_filtered[['Ticker', 'Company Name', 'Sector', 'CFO', 'CFI', 'CFF']].copy()
    for col in ['CFO', 'CFI', 'CFF']:
        df_filtered_display[col] = df_filtered_display[col].map(lambda x: f"₹{x:,.2f} Cr" if pd.notna(x) else "N/A")
        
    st.dataframe(df_filtered_display, use_container_width=True, hide_index=True)
else:
    st.info("No cash flow data available for treemap generation.")
