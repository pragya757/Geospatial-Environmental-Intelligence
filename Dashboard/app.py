"""
Similipal Forest Intelligence - Main Streamlit Application Entrypoint.
Multi-Temporal Forest Fire Detection, Vegetation Change Assessment and Ecological Vulnerability Analysis.
"""

import sys
from pathlib import Path

# Add project root and dashboard directory to python path for clean modular imports
DASHBOARD_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = DASHBOARD_DIR.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(DASHBOARD_DIR) not in sys.path:
    sys.path.insert(0, str(DASHBOARD_DIR))

import streamlit as st

# Streamlit Page Configuration
st.set_page_config(
    page_title="Similipal Forest Intelligence",
    page_icon="🌲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Custom CSS Styling
css_file = DASHBOARD_DIR / "assets" / "style.css"
if css_file.exists():
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Components & Modules
from Dashboard.components.header import render_header
from Dashboard.components.sidebar import render_sidebar
from Dashboard.modules import (
    overview,
    satellite_viewer,
    vegetation,
    thermal,
    burn_impact,
    vulnerability,
    change_detection,
    restoration,
    reports,
    about
)

def main():
    # Render Application Header
    render_header()

    # Render Sidebar Navigation
    selected_module = render_sidebar()

    # Module Routing
    if "1. Overview" in selected_module:
        overview.render()
    elif "2. Satellite Image" in selected_module:
        satellite_viewer.render()
    elif "3. Vegetation Index" in selected_module:
        vegetation.render()
    elif "4. Thermal Analysis" in selected_module:
        thermal.render()
    elif "5. Burn Impact" in selected_module:
        burn_impact.render()
    elif "6. Ecological Vulnerability" in selected_module:
        vulnerability.render()
    elif "7. Temporal Change" in selected_module:
        change_detection.render()
    elif "8. Restoration Priorities" in selected_module:
        restoration.render()
    elif "9. Reports" in selected_module:
        reports.render()
    elif "10. About" in selected_module:
        about.render()
    else:
        overview.render()

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6A8275; font-size: 0.82rem; padding: 15px 0 25px 0;">
        <strong>SIMILIPAL FOREST INTELLIGENCE SYSTEM</strong> &nbsp;|&nbsp; 
        Academic Research by <strong>Pragya Paramita Sahoo</strong> (B.Tech CSE, SRM Institute of Science and Technology) &nbsp;|&nbsp;
        Supervisor: <strong>Dr. A. Pandiaraj</strong><br>
        Sentinel-2 Multi-Spectral Analysis (B2, B4, B8, B11) & MODIS Thermal Observations &nbsp;|&nbsp; 
        Similipal Biosphere Reserve, Odisha, India
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
