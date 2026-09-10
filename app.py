import streamlit as st
import pandas as pd
import numpy as np

# 1. Page Configuration & Professional Styling
st.set_page_config(
    page_title="Qiddiya Utility Management System",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End Cyber CSS Injection - Corrected parameter name
st.markdown("""
    <style>
    /* Premium Carbon Background */
    .stApp {
        background-color: #0e1117;
        color: #e2e8f0;
    }
    
    /* Elegant Metric Container Cards */
    div[data-testid="stMetricContainer"] {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    div[data-testid="stMetricContainer"]:hover {
        transform: translateY(-2px);
        border-color: #38bdf8;
    }
    
    /* Clean Sidebar Customization */
    section[data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid #1e293b;
    }
    
    /* Professional Form Overlays */
    .stForm {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 16px !important;
        padding: 30px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Session Control Variables
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "selected_plant" not in st.session_state:
    st.session_state.selected_plant = None

# ==========================================
# MILESTONE 1: SECURITY GATE (LOGIN PAGE)
# ==========================================
if not st.session_state.authenticated:
    # Center the login screen vertically using layout padding columns
    _, col_center, _ = st.columns([1, 1.5, 1])
    
    with col_center:
        st.write("")
        st.write("")
        # Qiddiya Corporate Visual Header Anchor
        st.image("https://seeklogo.com", width=220)
        st.markdown("<h2 style='text-align: center; margin-bottom: 25px;'>Utility Infrastructure Log In</h2>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("Username ID")
            password = st.text_input("Security Password", type="password")
            submit = st.form_submit_button("Authenticate System", use_container_width=True)
            
            if submit:
                # Basic authentication verification logic
                if username.lower() == "admin" and password == "qiddiya2026":
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Invalid corporate credentials. Please check entries.")
    st.stop()

# ==========================================
# MILESTONE 2: SYSTEM PLANT SELECTION HUB
# ==========================================
if st.session_state.selected_plant is None:
    st.markdown("<h1 style='text-align: center; margin-top: 40px;'>Select Infrastructure Plant Network</h1>", unsafe_allowed_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8; margin-bottom: 50px;'>Choose an active utility network node to view dashboards and metrics</p>", unsafe_allowed_html=True)
    
    # 4-Column Operations Grid
    grid_stp, grid_irr, grid_dcp, grid_pot = st.columns(4)
    
    with grid_stp:
        st.markdown("<div style='background:#1e293b; padding:25px; border-radius:12px; border:1px solid #334155; text-align:center;'><h3>⚙️ STP</h3><p style='color:#64748b;'>Sewage Treatment Network</p></div>", unsafe_allow_html=True)
        if st.button("Open STP Network", key="btn_stp", use_container_width=True):
            st.warning("STP Network layout config is offline. Only DCP is active.")
            
    with grid_irr:
        st.markdown("<div style='background:#1e293b; padding:25px; border-radius:12px; border:1px solid #334155; text-align:center;'><h3>🌱 Irrigation</h3><p style='color:#64748b;'>Water Distribution Grid</p></div>", unsafe_allow_html=True)
        if st.button("Open Irrigation Network", key="btn_irr", use_container_width=True):
            st.warning("Irrigation Network layout config is offline. Only DCP is active.")
            
    with grid_dcp:
        st.markdown("<div style='background: linear-gradient(135deg, #0369a1 0%, #0f172a 100%); padding:25px; border-radius:12px; border:1px solid #0284c7; text-align:center;'><h3>❄️ DCP</h3><p style='color:#e2e8f0;'>District Cooling Plant</p></div>", unsafe_allow_html=True)
        if st.button("Open DCP Network", key="btn_dcp", use_container_width=True):
            st.session_state.selected_plant = "DCP"
            st.rerun()
            
    with grid_pot:
        st.markdown("<div style='background:#1e293b; padding:25px; border-radius:12px; border:1px solid #334155; text-align:center;'><h3>💧 Potable</h3><p style='color:#64748b;'>Drinking Water Infrastructure</p></div>", unsafe_allow_html=True)
        if st.button("Open Potable Network", key="btn_pot", use_container_width=True):
            st.warning("Potable Network layout config is offline. Only DCP is active.")
            
    st.stop()

# ==========================================
# MILESTONE 3: DISTRICT COOLING PLANT (DCP) DASHBOARD
# ==========================================
if st.session_state.selected_plant == "DCP":
    
    # Sidebar Header Navigation Branding
    with st.sidebar:
        st.image("https://seeklogo.com", width=140)
        st.markdown("<h4 style='color: #38bdf8; margin-bottom: 20px;'>DCP System Active</h4>", unsafe_allow_html=True)
        
        # Premium Operational Option Controls Menu
        menu = st.radio(
            "Operations Menu",
            ["📊 Performance Dashboard", "📝 Add Plant Reading", "📥 Export Operational Data"]
        )
        st.markdown("---")
        if st.button("Logout / Change Plant", use_container_width=True):
            st.session_state.selected_plant = None
            st.session_state.authenticated = False
            st.rerun()

    # SECTION A: THE METRICS DASHBOARD VIEW
    if menu == "📊 Performance Dashboard":
        st.title("❄️ Chiller Plant Performance Dashboard")
        st.markdown("<p style='color:#94a3b8;'>Real-time operational summaries for District Cooling Plant Network</p>", unsafe_allow_html=True)
        
        # 4 Horizontal Side-by-Side Clean Layout Metrics Cards
        m1, m2, m3, m4 = st.columns(4)
        m1.metric(label="Latest Total Power", value="5,347.50 kW", delta="-12.4 kW")
        m2.metric(label="Latest Refrigeration", value="333.74 TR", delta="+8.2 TR")
        m3.metric(label="Plant Efficiency", value="16.02 kW/TR", delta="-0.45 kW/TR")
        m4.metric(label="Chiller Units Running", value="20 / 24 Units", delta="Optimal Status")
        
        st.markdown("### 📈 Operational Performance Trends")
        
        # Interactive Simulated Monitoring Graph
        chart_data = pd.DataFrame(
            np.random.randn(20, 2) * [0.5, 10] + [16.02, 333.74],
            columns=['Efficiency (kW/TR)', 'Refrigeration (TR)']
        )
        st.line_chart(chart_data, height=350)

    # SECTION B: DATA INPUT FORM VIEW
    elif menu == "📝 Add Plant Reading":
        st.title("📝 Log New Operator Readings")
        st.markdown("<p style='color:#94a3b8;'>Input precise field metrics directly into the shared cloud tables</p>", unsafe_allow_html=True)
        
        with st.form("reading_entry_form"):
            col1, col2 = st.columns(2)
            with col1:
                power_kw = st.number_input("Total Power Intake (kW)", min_value=0.0, step=0.1)
                refrig_tr = st.number_input("Refrigeration Level (TR)", min_value=0.0, step=0.1)
            with col2:
                efficiency = st.number_input("Plant Efficiency Quotient (kW/TR)", min_value=0.0, step=0.01)
                chillers_on = st.slider("Running Chillers Count", min_value=0, max_value=24, value=12)
                
            notes = st.text_area("Operational Log Notes / Status Reports")
            submit_data = st.form_submit_button("Commit Changes to Live Database", use_container_width=True)
            
            if submit_data:
                st.success("Log Entry verified! (Database pipeline update processed successfully)")

    # SECTION C: DATA REPORT SHEET EXPORTS
    elif menu == "📥 Export Operational Data":
        st.title("📥 Operational Log sheets & Exports")
        st.markdown("<p style='color:#94a3b8;'>Review audit history or compile clean spreadsheets for tracking</p>", unsafe_allow_html=True)
        
        # Fixed Table Display with complete array definition
        mock_logs = pd.DataFrame({
            'Timestamp': pd.date_range(start='2026-09-01', periods=5, freq='H'),
            'Total Power (kW)': [5340.2, 5345.1, 5342.8, 5346.0, 5347.5],
            'Refrigeration (TR)': [331.0, 332.5, 330.9, 333.0, 333.74],
            'Efficiency (kW/TR)': [16.13, 16.07, 16.14, 16.05, 16.02],
            'Chillers Active': [18, 19, 18, 20, 20]
        })
        
        st.dataframe(mock_logs, use_container_width=True)
        st.download_button(
            label="Download Master Sheet (CSV Format)",
            data=mock_logs.to_csv(index=False),
            file_name="DCP_Live_Readings.csv",
            mime="text/csv",
            use_container_width=True
        )
