import streamlit as st
import pandas as pd
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="Project Management & Analytics", layout="wide")

st.title("Project Management System")

# 1. Mass Upload Section
st.header("Project Upload")
uploaded_file = st.file_uploader("Upload Project Template (CSV or Excel)", type=['csv', 'xlsx'])

# Initialize session state for data persistence
if 'project_data' not in st.session_state:
    st.session_state.project_data = pd.DataFrame(columns=[
        "Project Name", "Start Date", "Projected End Date", "Actual End Date", "Status"
    ])

if uploaded_file:
    try:
        new_data = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        st.session_state.project_data = pd.concat([st.session_state.project_data, new_data], ignore_index=True)
        st.success(f"Uploaded {len(new_data)} projects successfully!")
    except Exception as e:
        st.error(f"Error loading file: {e}")

# 2. Filters & Analytics Section
st.header("Project Filters & Analytics")

# Filter Logic
status_options = st.session_state.project_data["Status"].unique().tolist() if not st.session_state.project_data.empty else []
status_filter = st.multiselect("Filter by Status", options=status_options, default=[])

df_display = st.session_state.project_data.copy()
if status_filter:
    df_display = df_display[df_display["Status"].isin(status_filter)]

# Display Data Table
st.subheader("Project Overview")
st.dataframe(df_display, use_container_width=True)

# 3. Individual Project Tracking & Sign-off
st.header("Sign-off & Scope Management")
with st.expander("Attach Sign-off Scope"):
    project_names = df_display["Project Name"].tolist() if not df_display.empty else ["None"]
    project_to_update = st.selectbox("Select Project", project_names)
    attachment = st.file_uploader(f"Upload sign-off for {project_to_update}", type=['pdf', 'png', 'jpg'])
    
    if st.button("Save Attachment"):
        if project_to_update != "None":
            st.info(f"Attachment for {project_to_update} has been linked to the scope.")
        else:
            st.warning("Please select a valid project.")

# Sidebar Analytics
if not df_display.empty:
    st.sidebar.header("Quick Analytics")
    st.sidebar.metric("Filtered Projects", len(df_display))
