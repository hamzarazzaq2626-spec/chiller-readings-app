import streamlit as st
import pandas as pd
import numpy as np
import time

# 1. Page Configuration & Elite Display Configurations
st.set_page_config(
    page_title="Qiddiya Grid Flow // Infrastructure OS",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End Cyber Glassmorphism CSS Injection
st.markdown("""
    <style>
    /* Cyber Terminal Canvas Background */
    .stApp {
        background-color: #050811;
        background-image: 
            radial-gradient(at 0% 0%, rgba(3, 105, 161, 0.15) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(13, 148, 136, 0.1) 0px, transparent 50%);
        color: #f1f5f9;
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* Aerospace Frosted Glass Panel Theme */
    div[data-testid="stMetricContainer"], .stForm, div.stAlert {
        background: rgba(15, 23, 42, 0.65) !important;
        backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(56, 189, 248, 0.2) !important;
        border-radius: 16px !important;
        padding: 24px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) *;
    }
    
    /* Interactive Panel Glow Sweeps */
    div[data-testid="stMetricContainer"]:hover {
        border-color: rgba(56, 189, 248, 0.8) !important;
        box-shadow: 0 0 25px rgba(56, 189, 248, 0.25) !important;
        transform: translateY(-3px);
    }
    
    /* Telemetry Header Formatting */
    div[data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 800 !important;
        color: #06b6d4 !important;
        text-shadow: 0 0 10px rgba(6, 182, 212, 0.4);
    }
    div[data-testid="stMetricLabel"] {
        font-size: 0.85rem !important;
        color: #94a3b8 !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
    
    /* Neon Cyber Buttons Override */
    .stButton>button {
        background: linear-gradient(135deg, #0284c7 0%, #0d9488 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        letter-spacing: 1px !important;
        transition: all 0.2s ease !important;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 15px rgba(13, 148, 136, 0.6) !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize System Security Session Variables
if "authenticated" not in st.session_state: st.session_state.authenticated = False
if "selected_plant" not in st.session_state: st.session_state.selected_plant = None

# ==========================================
# PHASE 1: SYS//AUTH GATEWAY
# ==========================================
if not st.session_state.authenticated:
    _, col_center, _ = st.columns([1, 1.2, 1])
    with col_center:
        st.write(""); st.write(""); st.write("")
        st.markdown("<h1 style='text-align: center; color: #06b6d4; font-weight: 800; letter-spacing: 4px; text-shadow: 0 0 15px rgba(6,182,212,0.5);'>QIDDIYA CITY</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #64748b; font-size: 13px; letter-spacing: 2px; margin-bottom: 35px;'>UTILITY INFRASTRUCTURE HUB</p>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            st.markdown("<p style='color: #38bdf8; font-size: 11px; letter-spacing: 1px; margin-bottom: 5px;'>OPERATOR ACCESS ID</p>", unsafe_allow_html=True)
            username = st.text_input("Operator Email", value="operator@qiddiya.sa", label_visibility="collapsed")
            
            st.markdown("<p style='color: #38bdf8; font-size: 11px; letter-spacing: 1px; margin-top: 15px; margin-bottom: 5px;'>ACCESS CONTROL CODE</p>", unsafe_allow_html=True)
            password = st.text_input("Access Code", type="password", label_visibility="collapsed")
            
            st.write("")
            if st.form_submit_button("INITIALIZE SESSION", use_container_width=True):
                if username == "operator@qiddiya.sa" and password == "qiddiya2026":
                    st.session_state.authenticated = True
                    st.toast("⚡ Session Initialized Successfully", icon="🔋")
                    time.sleep(0.5)
                    st.rerun()
                else: 
                    st.error("🔒 ACCESS DENIED: Invalid Security Credentials")
    st.stop()

# ==========================================
# PHASE 2: INFRASTRUCTURE SWITCHBOARD ROOT
# ==========================================
if st.session_state.selected_plant is None:
    st.markdown("<h1 style='text-align: center; font-weight: 700; letter-spacing: 2px; color: #f8fafc; margin-top: 30px;'>INFRASTRUCTURE CONTROL HUB</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b; letter-spacing: 1px; margin-bottom: 45px;'>SELECT A UTILITY NODE TO ACCESS ITS MONITORING DECK</p>", unsafe_allow_html=True)
    
    grid_stp, grid_irr, grid_dcp, grid_pot = st.columns(4)
    with grid_stp:
        st.markdown("<div style='background:rgba(15,23,42,0.4); padding:25px; border-radius:14px; border:1px dashed rgba(148,163,184,0.2); text-align:center;'><h3>⚙️ STP</h3><p style='color:#64748b; font-size:12px; letter-spacing:1px;'>SEWAGE TREATMENT<br><br><span style='color:#ef4444;'>● LOCKED / OFFLINE</span></p></div>", unsafe_allow_html=True)
        if st.button("Query STP Node", use_container_width=True): st.warning("STP Routing Channel Inactive.")
    with grid_irr:
        st.markdown("<div style='background:rgba(15,23,42,0.4); padding:25px; border-radius:14px; border:1px dashed rgba(148,163,184,0.2); text-align:center;'><h3>🌱 IRRIGATION</h3><p style='color:#64748b; font-size:12px; letter-spacing:1px;'>WATER DISTRIBUTION<br><br><span style='color:#ef4444;'>● LOCKED / OFFLINE</span></p></div>", unsafe_allow_html=True)
        if st.button("Query IRR Node", use_container_width=True): st.warning("Irrigation Routing Channel Inactive.")
    with grid_dcp:
        st.markdown("<div style='background: linear-gradient(135deg, rgba(2,132,199,0.2) 0%, rgba(15,23,42,0.6) 100%); padding:25px; border-radius:14px; border:2px solid #06b6d4; text-align:center; box-shadow: 0 0 20px rgba(6,182,212,0.15);'><h3>❄️ DCP</h3><p style='color:#e2e8f0; font-size:12px; letter-spacing:1px;'>DISTRICT COOLING<br><br><span style='color:#10b981; font-weight:bold; text-shadow: 0 0 8px rgba(16,185,129,0.4);'>● NODE ACTIVE</span></p></div>", unsafe_allow_html=True)
        if st.button("ENTER MONITORING DECK", use_container_width=True):
            st.session_state.selected_plant = "DCP"
            st.rerun()
    with grid_pot:
        st.markdown("<div style='background:rgba(15,23,42,0.4); padding:25px; border-radius:14px; border:1px dashed rgba(148,163,184,0.2); text-align:center;'><h3>💧 POTABLE</h3><p style='color:#64748b; font-size:12px; letter-spacing:1px;'>DRINKING WATER<br><br><span style='color:#ef4444;'>● LOCKED / OFFLINE</span></p></div>", unsafe_allow_html=True)
        if st.button("Query POT Node", use_container_width=True): st.warning("Potable Routing Channel Inactive.")
    st.stop()

# ==========================================
# PHASE 3: ACTIVE CONTROL SYSTEM INTERFACE
# ==========================================
if st.session_state.selected_plant == "DCP":
    with st.sidebar:
        st.markdown("<h2 style='color: #06b6d4; margin-bottom: 0px; text-shadow: 0 0 10px rgba(6,182,212,0.3);'>QIDDIYA</h2><p style='color: #14b8a6; font-size: 11px; letter-spacing: 1px; font-weight: bold;'>⚡ DCP INTERFACE ACTIVE</p>", unsafe_allow_html=True)
        st.write("---")
        menu = st.radio("OPERATIONS RADAR", ["📊 Telemetry Deck", "📝 Deploy Log Entry", "📥 Database Archives"])
        st.write("---")
        if st.button("TERMINATE SESSION", use_container_width=True):
            st.session_state.selected_plant = None; st.session_state.authenticated = False; st.rerun()

    if menu == "📊 Telemetry Deck":
        st.title("❄️ District Cooling Performance Deck")
        st.markdown("<p style='color:#94a3b8; letter-spacing: 0.5px;'>Live algorithmic processing grids for Tier-1 Chiller assets</p>", unsafe_allow_html=True)
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric(label="System Power Consumption", value="5,347.50 kW", delta="-12.4 kW")
        m2.metric(label="Net Refrigeration Output", value="333.74 TR", delta="+8.2 TR")
        m3.metric(label="Active Plant Efficiency", value="16.02 kW/TR", delta="-0.45 kW/TR")
        m4.metric(label="Chiller Arrays Online", value="20 / 24 Units", delta="State: Optimal")
        
        st.write(""); st.write("")
        st.markdown("### 📈 Time-Series Telemetry Trends")
        
        chart_timestamps = pd.date_range(start='2026-09-11 00:00', periods=24, freq='h')
        chart_data = pd.DataFrame({
            'Efficiency Load (kW/TR)': [16.02 + np.sin(i/3)*0.15 for i in range(24)],
            'Refrigeration Yield (TR)': [333.74 + np.cos(i/2)*4.2 for i in range(24)]
        }, index=chart_timestamps)
        
        st.area_chart(chart_data, height=360, use_container_width=True)

    elif menu == "📝 Deploy Log Entry":
        st.title("📝 Dispatch Operator Field Readings")
        st.markdown("<p style='color:#94a3b8;'>Commit verified engineering telemetry metrics directly to active node pipelines</p>", unsafe_allow_html=True)
        
        with st.form("reading_entry_form"):
            col1, col2 = st.columns(2)
            with col1:
                power_kw = st.number_input("Total Power Intake (kW Metric)", min_value=0.0, step=0.1, value=5300.0)
                refrig_tr = st.number_input("Refrigeration Level (TR Metric)", min_value=0.0, step=0.1, value=330.0)
            with col2:
                efficiency = st.number_input("Plant Efficiency Quotient (kW/TR Coefficient)", min_value=0.0, step=0.01, value=16.0)
