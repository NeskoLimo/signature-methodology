import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="LogicForge: Signature Methodology", layout="wide")

st.title("🚀 LogicForge: Strategic Value Framework")
st.markdown("---")

# --- SIDEBAR: FILTERS & CONTROLS ---
st.sidebar.header("Data Controls")
uploaded_file = st.sidebar.file_uploader("Upload Project Template", type=["csv", "xlsx"])

# --- DATA PROCESSING ---
if uploaded_file:
    # Handle CSV or Excel
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    
    st.success(f"Successfully loaded {len(df)} projects.")

    # Sidebar Filters
    if "Status" in df.columns:
        status_list = df["Status"].unique().tolist()
        selected_status = st.sidebar.multiselect("Filter by Status", status_list, default=status_list)
        df = df[df["Status"].isin(selected_status)]

    # --- ANALYTICS DASHBOARD ---
    st.header("📊 Project Portfolio Analytics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Projects", len(df))
    with col2:
        if "Actual End Date" in df.columns:
            completed = df["Actual End Date"].notnull().sum()
            st.metric("Completed Sign-offs", completed)
    with col3:
        st.metric("Active Pipeline", len(df) - (completed if "Actual End Date" in df.columns else 0))

    st.subheader("Project Inventory")
    st.dataframe(df, use_container_width=True)

else:
    st.info("💡 Please upload your Project Template via the sidebar to begin analytics.")
    # Example template for the user to see what's needed
    st.write("Your template should include: `Project Name`, `Status`, `Start Date`, `Projected End Date`, `Actual End Date`, `Baseline`, `Target`.")

# --- GOVERNANCE: SIGN-OFF CAPABILITY ---
st.markdown("---")
st.header("📂 Governance & Scope Sign-off")
with st.expander("Attach New Scope Sign-off"):
    proj_name = st.text_input("Project Name for Sign-off")
    scope_doc = st.file_uploader("Upload Signed Scope (PDF)", type=["pdf"])
    if st.button("Link Sign-off to Project"):
        st.success(f"Scope for {proj_name} has been archived.")
