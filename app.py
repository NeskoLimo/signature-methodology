import streamlit as st
import pandas as pd

# Set Page Config for a professional look
st.set_page_config(page_title="LogicForge | Strategic Value Mapper", layout="wide")

# Custom Styling
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_name=True)

st.title("🚀 LogicForge")
st.subheader("Signature Methodology: From Current State to Quantified Value")
st.info("This tool enforces a Strategic Logic Gate to ensure requirements are tied to measurable outcomes.")

# --- PHASE 1: CURRENT STATE ---
st.header("1. Current State (The Pain)")
col1, col2 = st.columns([2, 1])

with col1:
    current_state_desc = st.text_area("Describe the current pain point or inefficiency:", 
                                   placeholder="e.g., Manual reconciliation of invoices takes 40 hours per week.")
with col2:
    baseline_metric = st.number_input("Baseline Metric (Value)", min_value=0.0, help="The current measurable state (e.g., 40.0)")
    unit = st.text_input("Unit of Measure", value="Hours/Week")

# --- PHASE 2: THE GAP ---
st.header("2. Gap Analysis")
gap_types = st.multiselect("Identify the primary obstacles:", 
                         ["Process Redundancy", "Technical Debt", "Data Silos", "Manual Intervention", "Skill Gap"])

# --- PHASE 3: THE TARGET (THE GAIN) ---
st.header("3. Future State (The Value)")
col3, col4 = st.columns([1, 2])

with col3:
    target_metric = st.number_input("Target Metric (Expected Value)", min_value=0.0)
with col4:
    success_criteria = st.text_input("Definition of Success", placeholder="e.g., Reduce manual effort by 50%")

# --- ANALYTICAL ENGINE ---
st.divider()
if st.button("Validate Strategic Alignment"):
    if not current_state_desc or baseline_metric == 0:
        st.error("❌ Error: You must define a Current State and a Baseline Metric to proceed.")
    elif target_metric >= baseline_metric:
        st.warning("⚠️ Scope Risk: The target metric shows no improvement over the baseline. Value delivery is unverified.")
    else:
        # Calculate Improvement
        improvement = baseline_metric - target_metric
        roi_percent = (improvement / baseline_metric) * 100
        
        st.success(f"✅ Strategic Alignment Verified: This project targets a {roi_percent:.1f}% improvement.")
        
        # Dashboard Visuals
        m1, m2, m3 = st.columns(3)
        m1.metric("Baseline", f"{baseline_metric} {unit}")
        m2.metric("Target", f"{target_metric} {unit}")
        m3.metric("Improvement", f"{roi_percent:.1f}%", delta=f"-{improvement} {unit}", delta_color="normal")

        # Visualization
        chart_data = pd.DataFrame({
            "State": ["Current", "Future"],
            "Value": [baseline_metric, target_metric]
        })
        st.bar_chart(data=chart_data, x="State", y="Value")
        
        # Export logic (Simulated for Portfolio)
        st.download_button("Generate Sign-off Summary (Markdown)", 
                         data=f"# LogicForge Sign-off\n\n**Pain:** {current_state_desc}\n**Improvement:** {roi_percent:.1f}%",
                         file_name="project_scope_summary.md")
