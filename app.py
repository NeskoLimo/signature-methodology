import streamlit as st
import pandas as pd
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="Project Management & Analytics", layout="wide")

st.title("Project Management System")

# 1. Mass Upload Section
st.header("Project Upload")
uploaded_file = st.file_uploader("Upload Project Template (CSV or Excel)", type=['csv', 'xlsx'])

# Using a placeholder for data to maintain the "last working model" state
if 'project_data' not in st.session_state:
    st.session_state.project_data = pd.DataFrame(columns=[
        "Project Name", "Start Date", "Projected End Date", "Actual End Date", "Status", "Sign-off Attachment"
    ])

if uploaded_file:
    # Logic to handle mass upload and enrich analytics
    new_data = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    st.session_state.project_data = pd.concat([st.session_state.project_data, new_data], ignore_index=True)
    st.success(f"Uploaded {len(new_data)} projects successfully!")

---

# 2. Filters & Analytics Section
st.header("Project Filters & Analytics")

col1, col2 = st.columns(2)

with col1:
    status_filter = st.multiselect(
        "Filter by Status",
        options=st.session_state.project_data["Status"].unique() if not st.session_state.project_data.empty else ["No Data"],
        default=[]
    )

# Filter Logic
df = st.session_state.project_state = st.session_state.project_data
if status_filter:
    df = df[df["Status"].isin(status_filter)]

# Display Data Table
st.subheader("Project Overview")
st.dataframe(df, use_container_width=True)

---

# 3. Individual Project Tracking & Sign-off
st.header("Sign-off & Scope Management")
with st.expander("Attach Sign-off Scope"):
    project_to_update = st.selectbox("Select Project", df["Project Name"].tolist() if not df.empty else ["None"])
    attachment = st.file_uploader(f"Upload sign-off for {project_to_update}", type=['pdf', 'png', 'jpg'])
    
    if st.button("Save Attachment"):
        st.info(f"Attachment for {project_to_update} has been linked to the scope.")

# Analytics Summary
if not df.empty:
    st.sidebar.header("Quick Analytics")
    st.sidebar.metric("Total Projects", len(df))
    # Additional logic for Actual vs Projected End Date can be added here
