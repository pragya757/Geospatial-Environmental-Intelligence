"""
Module 4: Thermal Analysis & Land Surface Temperature Dynamics.
Evaluates relative thermal stress, surface heating anomalies, and post-fire thermal retention.
"""

import streamlit as st
from streamlit_folium import st_folium
import plotly.graph_objects as go
import numpy as np

from Dashboard.config import RASTER_PATHS, NOTEBOOK_STATS
from Dashboard.components.maps import create_folium_raster_map
from Dashboard.components.metrics_cards import render_metric_card

def render():
    st.markdown("## Land Surface Temperature (LST) & Relative Thermal Stress")
    st.markdown("""
    Spatial assessment of surface thermal anomalies and radiative heat dissipation across Similipal Forest.
    Thermal infrared observations capture vegetation canopy transpiration breakdown and ground heat absorption.
    """)

    st.markdown("""
    <div class="warning-callout">
        <strong>Data Integrity & Unit Specification Notice:</strong><br>
        The thermal datasets in this research are recorded in <strong>Relative Thermal Units / Digital Numbers (DN)</strong> 
        derived from MODIS / Landsat thermal sensors clipped to the study boundary. In accordance with rigorous scientific standards, 
        these values are <strong>not converted to or presented as calibrated degrees Celsius (°C)</strong>, as no atmospheric radio-sounding 
        profile or in-situ radiometric ground validation was applied during preprocessing. All metrics represent <strong>relative thermal radiation intensity</strong>.
    </div>
    """, unsafe_allow_html=True)

    # Metric Strip
    lst_stats = NOTEBOOK_STATS["LST"]
    c1, c2, c3 = st.columns(3)
    with c1:
        render_metric_card(
            title="During-Fire Relative Heating (Mean Δ)",
            value=f"+{lst_stats['dLST_During']['mean']:,.1f}",
            subtitle="Relative Thermal Units",
            delta="+2,420.6 Mean Increase",
            delta_type="inverse"
        )
    with c2:
        render_metric_card(
            title="Maximum Localized Thermal Rise",
            value=f"+{lst_stats['dLST_During']['max']:,.1f}",
            subtitle="Relative Thermal Units",
            delta="Peak Thermal Anomaly",
            delta_type="inverse"
        )
    with c3:
        render_metric_card(
            title="Post-Fire Thermal Persistence (Mean Δ)",
            value=f"+{lst_stats['dLST_Post']['mean']:,.1f}",
            subtitle="Relative Thermal Units",
            delta="Residual Radiative Heating",
            delta_type="inverse"
        )

    st.markdown("---")

    # Map Selector
    st.markdown("### Interactive Thermal Product Map")
    thermal_selection = st.selectbox(
        "Select Thermal Raster Product",
        [
            "ΔLST During-Fire (Thermal Anomaly Map)",
            "ΔLST Post-Fire (Residual Thermal Map)",
            "Pre-Fire Relative LST (Baseline)",
            "During-Fire Relative LST (Peak Thermal)",
            "Post-Fire Relative LST (Aftermath)"
        ]
    )

    if "During-Fire (Thermal Anomaly" in thermal_selection:
        raster_path = str(RASTER_PATHS["LST"]["dLST_During"])
        cmap = "inferno"
        vmin, vmax = 1000.0, 3500.0
        caption = "Active thermal emission anomaly relative to pre-fire baseline (OpenStreetMap basemap)."
    elif "Post-Fire (Residual" in thermal_selection:
        raster_path = str(RASTER_PATHS["LST"]["dLST_Post"])
        cmap = "inferno"
        vmin, vmax = 500.0, 3000.0
        caption = "Residual radiative heating over scorched soil and blackened surfaces."
    elif "Pre-Fire" in thermal_selection:
        raster_path = str(RASTER_PATHS["LST"]["Pre-Fire"])
        cmap = "hot"
        vmin, vmax = 40000.0, 48000.0
        caption = "Pre-fire relative thermal baseline."
    elif "During-Fire Relative" in thermal_selection:
        raster_path = str(RASTER_PATHS["LST"]["During-Fire"])
        cmap = "hot"
        vmin, vmax = 42000.0, 50000.0
        caption = "Active fire relative thermal distribution."
    else:
        raster_path = str(RASTER_PATHS["LST"]["Post-Fire"])
        cmap = "hot"
        vmin, vmax = 41000.0, 49000.0
        caption = "Post-fire relative thermal distribution."

    col_map, col_details = st.columns([1.8, 1.0])
    with col_map:
        st.markdown(f"#### {thermal_selection}")
        st.caption(caption)
        m = create_folium_raster_map(
            raster_path,
            title=thermal_selection,
            cmap_name=cmap,
            vmin=vmin,
            vmax=vmax,
            opacity=0.9
        )
        st_folium(m, width=650, height=460, key="thermal_folium")

    with col_details:
        st.markdown("#### Thermal Stress Interpretation")
        st.markdown("""
        - **Evaporative Cooling Breakdown**: Canopy combustion abruptly curtailed transpirational cooling, leading to rapid ground surface radiative warming.
        - **Surface Albedo Alteration**: Deposition of dark charcoal and ash reduced surface reflectance, enabling burned ground to absorb greater solar insolation.
        - **Spatial Convergence**: The highest relative thermal anomalies coincide with exposed ridges and valley shoulders where flame fronts concentrated.
        """)
        st.caption(f"Source file: `{raster_path.split('/')[-1]}`")

    st.markdown("---")
    st.markdown("### Distribution of Temperature Change (ΔLST During Fire)")
    st.markdown("""
    The thermal difference distribution shows a positive shift across the reserve during the fire phase, 
    with a standard deviation of 500.42 relative units indicating substantial spatial heterogeneity.
    """)
    
    fig = go.Figure()
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=lst_stats["dLST_During"]["mean"],
        title={'text': "Mean Relative Thermal Rise (During Fire - Relative Units)", 'font': {'color': "#FFFFFF"}},
        gauge={
            'axis': {'range': [0, 4000], 'tickcolor': "#FFFFFF"},
            'bar': {'color': "#C0392B"},
            'steps': [
                {'range': [0, 1500], 'color': "#1B4D3E"},
                {'range': [1500, 2500], 'color': "#F39C12"},
                {'range': [2500, 4000], 'color': "#78281F"}
            ],
            'threshold': {
                'line': {'color': "#FFFFFF", 'width': 3},
                'thickness': 0.75,
                'value': 2420.59
            }
        }
    ))
    fig.update_layout(
        paper_bgcolor="#121614",
        font=dict(color="#E0E6E2"),
        height=280,
        margin=dict(l=40, r=40, t=30, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)
