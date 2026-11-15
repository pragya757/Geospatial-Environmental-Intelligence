"""
Sidebar navigation and global filtering for Similipal Forest Intelligence.
"""

import streamlit as st
from Dashboard.config import STUDY_AREA

MODULES = [
    "1. Overview & Research Summary",
    "2. Satellite Image Comparison",
    "3. Vegetation Index Analysis",
    "4. Thermal Analysis (Relative LST)",
    "5. Burn Impact Analysis (BRI)",
    "6. Ecological Vulnerability Assessment",
    "7. Temporal Change Detection",
    "8. Restoration Priorities & Decision Support",
    "9. Reports & Data Export",
    "10. About the Research"
]

def render_sidebar():
    """Renders the sidebar navigation and study area parameters."""
    with st.sidebar:
        st.markdown("""
        <div style="padding: 10px 0 15px 0;">
            <h2 style="color: #27AE60; margin-bottom: 2px; font-size: 1.35rem; font-weight: 700; letter-spacing: -0.5px;">SIMILIPAL MONITOR</h2>
            <div style="color: #8CA094; font-size: 0.82rem;">Geospatial Environmental Intelligence</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Navigation")
        selected_module = st.radio(
            "Select Analysis Module",
            MODULES,
            index=0,
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.markdown("### Observation Phases")
        st.markdown("""
        - **Pre-Fire Phase**: Baseline healthy forest condition
        - **During-Fire Phase**: Active wildfire progression & canopy loss
        - **Post-Fire Phase**: Immediate aftermath & initial response
        """)
        
        st.markdown("---")
        st.markdown("### Study Area Reference")
        st.markdown(f"""
        - **Target**: {STUDY_AREA['name']}
        - **Region**: {STUDY_AREA['location']}
        - **Coordinates**: 21.75° N, 86.25° E
        - **Classified Area**: 3,485.37 km²
        - **Observation Data**: Sentinel-2 (B2, B4, B8, B11)
        """)

        st.markdown("""
        <div style="background: rgba(241, 196, 15, 0.08); border: 1px solid rgba(241, 196, 15, 0.25); border-radius: 6px; padding: 10px; margin-top: 15px; font-size: 0.78rem; color: #D5C88F; line-height: 1.4;">
            <strong>Historical Satellite Observations</strong><br>
            Analysis is based on calibrated Sentinel-2 surface reflectance and thermal satellite observations. Not a real-time active alerting feed.
        </div>
        """, unsafe_allow_html=True)

        return selected_module
