import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="LogicForge: Signature Methodology", layout="wide")

st.title("🚀 LogicForge: Strategic Value Framework")
st.markdown("---")

# --- SIDEBAR FILTERS ---
st.sidebar.header("Project Filters")
status_filter = st.sidebar.multiselect("Select Status", ["Pipeline", "Active", "Completed", "Signed Off"], default="Active")

# --- MASS UPLOAD SECTION ---
st.header("1. Project Mass Upload")
uploaded_file = st.sidebar.file_uploader("Upload Project Template (CSV/Excel)", type=["csv", "xlsx"])

if uploaded_file:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    st.success("File Uploaded Successfully!")
    
    # Filter the dataframe based on sidebar
    if "Status" in df.columns:
        df = df[df["Status"].isin(status_filter)]
    
    st.dataframe(df, use_container_width=True)
else:
    st.info("Awaiting template upload. Showing manual entry mode.")

# --- MANUAL ROI CALCULATOR (YOUR ORIGINAL LOGIC) ---
st.header("2. Value Validation (Signature ROI)")
col1, col2 = st.columns(2)

with col1:
    baseline = st.number_input("Baseline (Current Hours/Cost)", min_value=0.0, value=100.0)
    target = st.number_input("Target (Projected Hours/Cost)", min_value=0.0, value=50.0)
    
with col2:
    start_date = st.date_input("Project Start Date", datetime.now())
    end_date = st.date_input("Projected End Date", datetime.now())

if st.button("Calculate ROI"):
    improvement = ((baseline - target) / baseline) * 100
    st.metric("Efficiency Gain", f"{improvement}%", delta=f"{baseline - target} units saved")
    
    # Simple chart for visualization
    chart_data = pd.DataFrame({"Stage": ["Baseline", "Target"], "Values": [baseline, target]})
    st.bar_chart(chart_data, x="Stage", y="Values")

# --- SIGN-OFF SECTION ---
st.header("3. Governance & Sign-off")
scope_file = st.file_uploader("Attach Sign-off Scope (PDF/Docx)", type=["pdf", "docx"])
if scope_file:
    st.success(f"Sign-off attached: {scope_file.name}")

st.markdown("---")
st.caption("Last Updated: 2026-02-21 | Signature Methodology v2.0")
