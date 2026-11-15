"""
Header and hero banner component for Similipal Forest Intelligence.
"""

import streamlit as st

def render_header():
    """Renders the top application branding banner and research badges."""
    st.markdown("""
    <div class="hero-banner">
        <h1 class="hero-title">SIMILIPAL FOREST INTELLIGENCE</h1>
        <div class="hero-subtitle">
            Satellite-Based Forest Fire Analysis & Ecological Vulnerability Monitoring System
        </div>
        <div class="badge-strip">
            <span class="badge-item">Similipal Biosphere Reserve, Odisha, India</span>
            <span class="badge-item info">Sentinel-2 (10-20m) & MODIS/Landsat LST</span>
            <span class="badge-item warning">Multi-Temporal: Pre-Fire | During-Fire | Post-Fire</span>
            <span class="badge-item">Academic Honours Research</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
