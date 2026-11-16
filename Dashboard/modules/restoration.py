"""
Module 8: Restoration Priorities & Geospatial Decision Support.
Translates ecological vulnerability modeling into spatial management zones
and actionable post-fire conservation interventions for Similipal Forest.
"""

import streamlit as st
from streamlit_folium import st_folium
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from Dashboard.config import RASTER_PATHS, NOTEBOOK_STATS
from Dashboard.components.maps import create_folium_raster_map
from Dashboard.components.metrics_cards import render_metric_card, render_priority_card
from Dashboard.utils.stats_calculator import get_restoration_priority_df

def render():
    st.markdown("## Restoration Priorities & Decision Support System")
    st.markdown("""
    Spatial decision-support framework designating post-fire intervention zones across Similipal Biosphere Reserve.
    Priorities are established by segmenting the multi-criteria **Ecological Vulnerability Score (EVS)** 
    into four operational tiers.
    """)

    st.markdown("""
    <div class="warning-callout">
        <strong>Decision Support & Ground-Truth Disclaimer:</strong><br>
        This decision support system provides a <strong>model-based ecological prioritization</strong> derived from 
        satellite observations. It does <strong>not substitute for in-situ field verification</strong> by forestry officials, 
        silviculturists, or wildlife biologists. Recommendations represent strategic zoning to assist departmental resource allocation, 
        soil moisture conservation planning, and seed-ball distribution schedules.
    </div>
    """, unsafe_allow_html=True)

    priority_df = get_restoration_priority_df()
    classes = NOTEBOOK_STATS["Restoration_Priority"]["classes"]

    # Top Metric Banner
    top_col1, top_col2, top_col3, top_col4 = st.columns(4)
    with top_col1:
        render_metric_card("Classified Reserve Area", "3,485.4 km²", "348,537 Hectares", "Similipal Forest Boundary", "neutral")
    with top_col2:
        render_metric_card("Urgent Action Zones (H+VH)", "781.5 km²", "78,151 Hectares", "22.4% of Classified Area", "inverse")
    with top_col3:
        render_metric_card("Very High Priority Core", "338.2 km²", "33,820 Hectares", "9.71% of Reserve", "inverse")
    with top_col4:
        render_metric_card("Resilient Forest (Low)", "1,638.3 km²", "163,829 Hectares", "47.00% Self-Sustaining", "normal")

    st.markdown("---")

    # Interactive Map and Class Detail
    map_col, text_col = st.columns([1.8, 1.2])

    with map_col:
        st.markdown("### Restoration Priority Zonation Map")
        st.caption("Discrete priority classification (1: Low [Green] → 4: Very High [Red]) on OpenStreetMap basemap.")
        priority_raster = str(RASTER_PATHS["EVS"]["Restoration_Priority"])
        m = create_folium_raster_map(
            priority_raster,
            title="Restoration Priority Classes",
            cmap_name="RdYlGn_r",
            vmin=1.0,
            vmax=4.0,
            opacity=0.9
        )
        st_folium(m, width=650, height=480, key="resto_folium")

    with text_col:
        st.markdown("### Area Allocation Table")
        st.dataframe(
            priority_df[["Priority Class", "Area (km²)", "Area (Hectares)", "Percentage (%)"]].style.format({
                "Area (km²)": "{:,.2f}",
                "Area (Hectares)": "{:,.1f}",
                "Percentage (%)": "{:.2f}%"
            }),
            use_container_width=True,
            hide_index=True
        )

        st.markdown("""
        #### Contributing Factors to 'Very High Priority' (Tier 4):
        Areas identified as **Very High Priority (338.2 km²)** are recommended for further field assessment and restoration planning based on the convergence of three normalized EVS indicators:
        1. **Vegetation Degradation ($w_{\\text{veg}} = 0.40$)**: Marked decline in EVI with extensive canopy thinning and exposed soil.
        2. **Moisture Degradation ($w_{\\text{moist}} = 0.30$)**: Severe foliar and surface moisture desiccation captured by NDMI.
        3. **Relative Thermal Stress ($w_{\\text{thermal}} = 0.30$)**: Elevated relative thermal emission indicating persistent radiative warming.
        
        *Satellite-derived scores indicate relative priority tiers to guide allocation; specific silvicultural actions require on-ground field evaluation.*
        """)

    st.markdown("---")

    # Priority Action Matrix
    st.markdown("### Strategic Forest Restoration Matrix")
    st.markdown("Recommended silvicultural and management strategies tailored to each vulnerability zone:")

    strat_col1, strat_col2 = st.columns(2)
    with strat_col1:
        st.markdown("""
        <div style="background-color: #1A1814; border: 1px solid #78281F; border-radius: 8px; padding: 18px; margin-bottom: 16px;">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
                <span style="background: #C0392B; width: 14px; height: 14px; border-radius: 50%; display: inline-block;"></span>
                <h4 style="color: #C0392B; margin: 0; font-size: 1.05rem;">Tier 1: VERY HIGH PRIORITY (338.2 km²)</h4>
            </div>
            <p style="font-size: 0.88rem; color: #CFDFD6; margin-bottom: 10px;">
                Critical core zones where high burn severity, moisture loss, and thermal stress coincide.
            </p>
            <ul style="font-size: 0.83rem; color: #E0E6E2; padding-left: 18px; line-height: 1.5;">
                <li><strong>Soil and Water Conservation:</strong> Construct contour brush layering, stone bunds, and check-dams in upper catchment drainage gullies to mitigate monsoon topsoil erosion.</li>
                <li><strong>Assisted Active Revegetation:</strong> Priority planting and broadcast seeding of native keystone deciduous species (such as <em>Shorea robusta</em>, <em>Madhuca longifolia</em>, <em>Terminalia tomentosa</em>).</li>
                <li><strong>Post-Burn Vegetation Monitoring:</strong> Monitor establishing understory to track whether native regeneration or aggressive colonizers predominate.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background-color: #141A18; border: 1px solid #E67E22; border-radius: 8px; padding: 18px;">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
                <span style="background: #E67E22; width: 14px; height: 14px; border-radius: 50%; display: inline-block;"></span>
                <h4 style="color: #E67E22; margin: 0; font-size: 1.05rem;">Tier 2: HIGH PRIORITY (443.3 km²)</h4>
            </div>
            <p style="font-size: 0.88rem; color: #CFDFD6; margin-bottom: 10px;">
                Moderately degraded stands exhibiting notable understory loss with partial overstory survival.
            </p>
            <ul style="font-size: 0.83rem; color: #E0E6E2; padding-left: 18px; line-height: 1.5;">
                <li><strong>Assisted Natural Regeneration (ANR):</strong> Protect developing root suckers and coppice regrowth from grazing and human disturbance.</li>
                <li><strong>Firebreak Maintenance:</strong> Clear and maintain peripheral fire lines to protect recovering vegetation from subsequent fire cycles.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with strat_col2:
        st.markdown("""
        <div style="background-color: #181914; border: 1px solid #F39C12; border-radius: 8px; padding: 18px; margin-bottom: 16px;">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
                <span style="background: #F39C12; width: 14px; height: 14px; border-radius: 50%; display: inline-block;"></span>
                <h4 style="color: #F39C12; margin: 0; font-size: 1.05rem;">Tier 3: MODERATE PRIORITY (1,065.6 km²)</h4>
            </div>
            <p style="font-size: 0.88rem; color: #CFDFD6; margin-bottom: 10px;">
                Stands with low-intensity scorch where canopy architecture remains largely intact.
            </p>
            <ul style="font-size: 0.83rem; color: #E0E6E2; padding-left: 18px; line-height: 1.5;">
                <li><strong>Passive Natural Regeneration:</strong> Sufficient resilience for natural recovery under regular monsoon cycles.</li>
                <li><strong>Periodic Satellite Monitoring:</strong> Track seasonal greenness to confirm ongoing canopy closure.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background-color: #121814; border: 1px solid #27AE60; border-radius: 8px; padding: 18px;">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
                <span style="background: #27AE60; width: 14px; height: 14px; border-radius: 50%; display: inline-block;"></span>
                <h4 style="color: #27AE60; margin: 0; font-size: 1.05rem;">Tier 4: LOW PRIORITY / RESILIENT (1,638.3 km²)</h4>
            </div>
            <p style="font-size: 0.88rem; color: #CFDFD6; margin-bottom: 10px;">
                Unburned core reserves, deep evergreen stream corridors, and moist valley bottoms.
            </p>
            <ul style="font-size: 0.83rem; color: #E0E6E2; padding-left: 18px; line-height: 1.5;">
                <li><strong>Conservation of Ecological Refugia:</strong> Maintain protection; these zones serve as critical seed sources and wildlife refuges.</li>
                <li><strong>Fuel Load Surveillance:</strong> Monitor dry-season leaf litter build-up along perimeter boundaries.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
