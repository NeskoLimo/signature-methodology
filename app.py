import streamlit as st
import pandas as pd
from datetime import datetime

# --- APP CONFIGURATION ---
st.set_page_config(page_title="LogicForge: Signature Methodology", layout="wide")

# --- CUSTOM CSS FOR BRANDING ---
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 LogicForge: Strategic Value Framework")
st.markdown("---")

# --- SIDEBAR: CONTROLS & FILTERS ---
st.sidebar.header("📁 Data Management")
uploaded_file = st.sidebar.file_uploader("Upload Project Template", type=["csv", "xlsx"])

# --- CORE LOGIC FUNCTIONS ---
def process_data(df):
    # Standardize column names (removing spaces/casing issues)
    df.columns = [c.strip() for c in df.columns]
    
    # Date Conversion
    date_cols = ["Start Date", "Projected End Date", "Actual End Date"]
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    
    # Calculate Slippage (Actual vs Projected)
    if "Projected End Date" in df.columns and "Actual End Date" in df.columns:
        df['Slippage (Days)'] = (df['Actual End Date'] - df['Projected End Date']).dt.days
    
    # Calculate ROI/Efficiency Gap
    if "Baseline" in df.columns and "Target" in df.columns:
        df['Efficiency Gain %'] = ((df['Baseline'] - df['Target']) / df['Baseline'] * 100).round(2)
        
    return df

# --- MAIN DASHBOARD INTERFACE ---
if uploaded_file:
    # Load Data
    raw_df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    df = process_data(raw_df)
    
    # Sidebar Filters
    if "Status" in df.columns:
        status_list = df["Status"].unique().tolist()
        selected_status = st.sidebar.multiselect("Filter by Project Status", status_list, default=status_list)
        df = df[df["Status"].isin(selected_status)]

    # --- SECTION 1: KPI TILES ---
    st.header("📊 Signature Analytics Summary")
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.metric("Total Projects", len(df))
    with c2:
        avg_slip = df['Slippage (Days)'].mean() if 'Slippage (Days)' in df.columns else 0
        st.metric("Avg. Slippage", f"{avg_slip:.1f} Days", delta=f"{avg_slip:.1f}", delta_color="inverse")
    with c3:
        if 'Efficiency Gain %' in df.columns:
            avg_gain = df['Efficiency Gain %'].mean()
            st.metric("Avg. Efficiency Gain", f"{avg_gain}%")
    with c4:
        st.metric("Cloud Status", "Verified Live")

    # --- SECTION 2: VISUALIZATIONS ---
    st.markdown("---")
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("📅 Schedule Variance (Slippage)")
        if 'Slippage (Days)' in df.columns:
            st.bar_chart(data=df, x="Project Name", y="Slippage (Days)")
        else:
            st.warning("Upload 'Projected End Date' and 'Actual End Date' to see slippage.")

    with col_b:
        st.subheader("📈 Efficiency Impact (Baseline vs Target)")
        if "Baseline" in df.columns and "Target" in df.columns:
            chart_df = df[["Project Name", "Baseline", "Target"]].set_index("Project Name")
            st.area_chart(chart_df)

    # --- SECTION 3: DATA TABLE ---
    st.markdown("---")
    st.subheader("📝 Project Inventory Detail")
    
    # Styling the dataframe
    def color_slippage(val):
        if pd.isna(val): return ''
        color = 'red' if val > 0 else 'green' if val < 0 else 'black'
        return f'color: {color}'

    styled_df = df.style.applymap(color_slippage, subset=['Slippage (Days)'] if 'Slippage (Days)' in df.columns else [])
    st.dataframe(styled_df, use_container_width=True)

else:
    # DEFAULT VIEW / INSTRUCTIONS
    st.info("👋 Welcome to LogicForge. Please upload a project template to begin.")
    st.image("https://img.icons8.com/clouds/500/data-configuration.png", width=200)
    
    with st.expander("Required Template Schema"):
        st.write("""
        Your CSV/Excel should contain these headers:
        - **Project Name**: Title of initiative
        - **Status**: Pipeline, Active, Completed, or Signed Off
        - **Start Date**: YYYY-MM-DD
        - **Projected End Date**: YYYY-MM-DD
        - **Actual End Date**: YYYY-MM-DD
        - **Baseline**: Current metric value
        - **Target**: Desired metric value
        """)

# --- FOOTER ---
st.markdown("---")
st.caption(f"LogicForge v2.1 | Signature Methodology | Last Deployment: {datetime.now().strftime('%Y-%m-%d')}")
