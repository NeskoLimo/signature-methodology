import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="LogicForge: Signature Methodology", layout="wide")

st.title("🚀 LogicForge: Strategic Value Framework")
st.markdown("---")

# --- DATA LOADING & CALCULATIONS ---
uploaded_file = st.sidebar.file_uploader("Upload Project Template", type=["csv", "xlsx"])

def calculate_metrics(df):
    # Convert dates to datetime objects
    date_cols = ["Start Date", "Projected End Date", "Actual End Date"]
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col])
    
    # Calculate Slippage (Days)
    if "Projected End Date" in df.columns and "Actual End Date" in df.columns:
        df['Slippage (Days)'] = (df['Actual End Date'] - df['Projected End Date']).dt.days
    return df

if uploaded_file:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    df = calculate_metrics(df)
    
    # --- KPI TILES ---
    st.header("📊 Executive Summary")
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.metric("Total Projects", len(df))
    with c2:
        avg_slippage = df['Slippage (Days)'].mean() if 'Slippage (Days)' in df.columns else 0
        st.metric("Avg Slippage", f"{avg_slippage:.1f} Days", delta_color="inverse")
    with c3:
        if "Baseline" in df.columns and "Target" in df.columns:
            total_saved = (df['Baseline'] - df['Target']).sum()
            st.metric("Total Efficiency Gain", f"{total_saved:,} units")
    with c4:
        st.metric("Status", "Cloud Live")

    # --- FILTERS & DATA ---
    st.markdown("---")
    st.subheader("Project Inventory & Schedule Variance")
    
    # Simple color formatting for slippage
    def color_slippage(val):
        if val > 0: return 'color: red'
        if val < 0: return 'color: green'
        return ''

    st.dataframe(df.style.applymap(color_slippage, subset=['Slippage (Days)'] if 'Slippage (Days)' in df.columns else []), use_container_width=True)

else:
    st.info("Awaiting CSV/Excel upload to generate Signature Analytics.")

st.sidebar.markdown("---")
st.sidebar.caption("v2.1 | Signature Methodology")
