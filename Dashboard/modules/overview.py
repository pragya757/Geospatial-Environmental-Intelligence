"""
Module 1: Overview & Research Summary for Similipal Forest Intelligence.
"""

import streamlit as st
import pandas as pd
from streamlit_folium import st_folium

from Dashboard.config import STUDY_AREA, RASTER_PATHS, NOTEBOOK_STATS
from Dashboard.components.metrics_cards import render_metric_card, render_priority_card
from Dashboard.components.charts import (
    create_phase_comparison_bar,
    create_area_donut_chart
)
from Dashboard.components.maps import create_folium_raster_map
from Dashboard.utils.stats_calculator import (
    get_indices_comparison_df,
    get_restoration_priority_df,
    get_burn_severity_df
)

def render():
    st.markdown("## Executive Research Overview")
    st.markdown("""
    **Multi-Temporal Forest Fire Detection, Vegetation Change Assessment and Ecological Vulnerability Analysis Using Satellite Imagery**  
    *A Case Study of Similipal Forest, Odisha, India.*
    """)

    st.markdown("""
    <div class="info-callout">
        <strong>Research Overview & Core Objectives:</strong><br>
        This geospatial research dashboard presents satellite-based earth observations over the Similipal Biosphere Reserve, Odisha, India. 
        The project is structured around three primary scientific research objectives:
        <ol style="margin-top: 6px; margin-bottom: 6px; padding-left: 20px;">
            <li><strong>Multi-Temporal Forest Fire Detection & Vegetation Change Assessment:</strong> Quantifying canopy greenness, structure, and moisture shifts across Pre-Fire, During-Fire, and Post-Fire phases using Sentinel-2 MSI (NDVI, EVI, NDMI).</li>
            <li><strong>Spatial Ecological Vulnerability & Post-Fire Restoration Priority Assessment:</strong> Synthesizing normalized vegetation loss, foliar moisture deficit, and relative thermal stress into a model-derived Ecological Vulnerability Score (EVS) to establish geodesic restoration priority zones.</li>
            <li><strong>Soil-Adjusted Vegetation Condition Assessment Using MSAVI:</strong> Decoupling exposed scorched soil background interference using the self-adaptive Modified Soil-Adjusted Vegetation Index (MSAVI).</li>
        </ol>
        <em>Note:</em> This platform is an interactive satellite-based multi-temporal analysis system based on available observations, not an automated real-time wildfire alert dispatch system.
    </div>
    """, unsafe_allow_html=True)

    # Key Statistics Metrics Strip
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_metric_card(
            title="Classified Study Area",
            value="3,485.4 km²",
            subtitle="348,537 Geodesic Hectares",
            delta="Similipal Reserve Boundary",
            delta_type="neutral"
        )
    with col2:
        render_metric_card(
            title="Mean NDVI Change (During)",
            value="-0.0284",
            subtitle="Canopy Chlorophyll Drop",
            delta="-6.07% Mean Relative Drop",
            delta_type="normal"
        )
    with col3:
        render_metric_card(
            title="Moisture Depletion (NDMI)",
            value="66.74%",
            subtitle="Valid Pixels with Decline",
            delta="Foliar Desiccation",
            delta_type="normal"
        )
    with col4:
        render_metric_card(
            title="High / Very High Priority",
            value="781.5 km²",
            subtitle="22.4% of Classified Reserve",
            delta="Urgent Strategic Restoration",
            delta_type="inverse"
        )

    st.markdown("---")

    # Observation Phase Cards
    st.markdown("### The Three Satellite Observation Phases")
    p_col1, p_col2, p_col3 = st.columns(3)
    with p_col1:
        st.markdown("""
        <div style="background-color: #141C18; border: 1px solid #23362B; border-top: 4px solid #27AE60; border-radius: 8px; padding: 18px;">
            <h4 style="color: #27AE60; margin-top: 0; font-size: 1.05rem;">1. Pre-Fire Phase</h4>
            <p style="font-size: 0.88rem; color: #CFDFD6; margin-bottom: 8px;">
                Represents undisturbed baseline forest canopy conditions prior to the onset of dry-season fire ignitions.
            </p>
            <ul style="font-size: 0.82rem; color: #9EB0A5; margin-bottom: 0; padding-left: 18px; line-height: 1.5;">
                <li>Mean NDVI: <strong>0.3515</strong> (Chlorophyll absorption)</li>
                <li>Mean EVI: <strong>0.3695</strong> (Canopy structure)</li>
                <li>Mean NDMI: <strong>0.0899</strong> (Moisture baseline)</li>
                <li>Mean MSAVI: <strong>0.2457</strong> (Soil-adjusted baseline)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with p_col2:
        st.markdown("""
        <div style="background-color: #141C18; border: 1px solid #23362B; border-top: 4px solid #C0392B; border-radius: 8px; padding: 18px;">
            <h4 style="color: #C0392B; margin-top: 0; font-size: 1.05rem;">2. During-Fire Phase</h4>
            <p style="font-size: 0.88rem; color: #CFDFD6; margin-bottom: 8px;">
                Captures peak wildfire impact with widespread canopy scorching, leaf moisture desiccation, and thermal anomalies.
            </p>
            <ul style="font-size: 0.82rem; color: #9EB0A5; margin-bottom: 0; padding-left: 18px; line-height: 1.5;">
                <li>Mean NDVI: <strong>0.3230</strong> (Mean Δ = -0.0284)</li>
                <li>Mean EVI: <strong>0.3281</strong> (Mean Δ = -0.0413)</li>
                <li>Mean NDMI: <strong>0.0172</strong> (Mean Δ = -0.0727)</li>
                <li>MSAVI Decline: <strong>55.80%</strong> of valid pixels</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with p_col3:
        st.markdown("""
        <div style="background-color: #141C18; border: 1px solid #23362B; border-top: 4px solid #F39C12; border-radius: 8px; padding: 18px;">
            <h4 style="color: #F39C12; margin-top: 0; font-size: 1.05rem;">3. Post-Fire Phase</h4>
            <p style="font-size: 0.88rem; color: #CFDFD6; margin-bottom: 8px;">
                Evaluates short-term landscape response, pioneer understory flush, and spatial persistence of burn patches.
            </p>
            <ul style="font-size: 0.82rem; color: #9EB0A5; margin-bottom: 0; padding-left: 18px; line-height: 1.5;">
                <li>Mean NDVI: <strong>0.3682</strong> (Mean Δ = +0.0167)</li>
                <li>Mean EVI: <strong>0.3900</strong> (Mean Δ = +0.0205)</li>
                <li>Mean NDMI: <strong>0.0409</strong> (47.59% moisture deficit)</li>
                <li>MSAVI Increase: <strong>65.97%</strong> of valid pixels</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Spatial Map & Priority Breakdown Side-by-Side
    st.markdown("### Restoration Priority Overview & Spatial Distribution")
    map_col, chart_col = st.columns([1.3, 1.0])

    with map_col:
        st.markdown("**Interactive Restoration Priority Map**")
        st.caption("Derived from multi-criteria Ecological Vulnerability Scoring on standard OpenStreetMap basemap.")
        priority_raster = str(RASTER_PATHS["EVS"]["Restoration_Priority"])
        m = create_folium_raster_map(
            priority_raster,
            title="Restoration Priority",
            cmap_name="RdYlGn_r",
            vmin=1.0,
            vmax=4.0,
            opacity=0.88
        )
        st_folium(m, width=650, height=440)

    with chart_col:
        st.markdown("**Classified Area Distribution**")
        priority_df = get_restoration_priority_df()
        donut_fig = create_area_donut_chart(
            priority_df,
            names_col="Priority Class",
            values_col="Area (km²)",
            colors_dict={
                "Low": "#27AE60",
                "Moderate": "#F39C12",
                "High": "#E67E22",
                "Very High": "#C0392B"
            },
            title="Post-Fire Restoration Priority (km²)"
        )
        st.plotly_chart(donut_fig, use_container_width=True)

    # Detailed Priority Cards
    st.markdown("#### Priority Class Details")
    p_cards = st.columns(4)
    priority_classes = NOTEBOOK_STATS["Restoration_Priority"]["classes"]
    
    with p_cards[0]:
        render_priority_card(
            title="Low Priority",
            area_km2=priority_classes["Low"]["area_km2"],
            area_ha=priority_classes["Low"]["area_ha"],
            percentage=priority_classes["Low"]["pct"],
            color="#27AE60",
            description="Minimal burn impact or rapid canopy retention; self-regenerating resilient forest."
        )
    with p_cards[1]:
        render_priority_card(
            title="Moderate Priority",
            area_km2=priority_classes["Moderate"]["area_km2"],
            area_ha=priority_classes["Moderate"]["area_ha"],
            percentage=priority_classes["Moderate"]["pct"],
            color="#F39C12",
            description="Partial canopy scorch or moisture reduction; requires assisted natural regeneration."
        )
    with p_cards[2]:
        render_priority_card(
            title="High Priority",
            area_km2=priority_classes["High"]["area_km2"],
            area_ha=priority_classes["High"]["area_ha"],
            percentage=priority_classes["High"]["pct"],
            color="#E67E22",
            description="Substantial vegetation & moisture degradation; secondary fire risk and erosion."
        )
    with p_cards[3]:
        render_priority_card(
            title="Very High Priority",
            area_km2=priority_classes["Very High"]["area_km2"],
            area_ha=priority_classes["Very High"]["area_ha"],
            percentage=priority_classes["Very High"]["pct"],
            color="#C0392B",
            description="Severe canopy loss coupled with acute thermal stress; immediate intervention needed."
        )

    st.markdown("---")

    # Cross-Index Comparison Bar Chart
    st.markdown("### Cross-Index Phase Comparison")
    indices_df = get_indices_comparison_df()
    bar_fig = create_phase_comparison_bar(indices_df)
    st.plotly_chart(bar_fig, use_container_width=True)

    # Key Research Findings Callout with Cautious Academic Interpretation
    st.markdown("### Core Research Findings & Scientific Interpretation")
    st.markdown("""
    1. **Primary Fire Driver Confirmed**: Statistical regression demonstrates that **Fire Severity (BRI)** is the dominant driver of observed NDVI degradation ($r = 0.702$, $p < 0.001$), accounting for 32.1% of spatial variance in a coupled model.
    2. **Moisture Desiccation Preceded Severe Damage**: NDMI decreased by **80.9%** during the fire phase, with **66.74% of valid pixels** exhibiting acute moisture depletion, confirming that water stress amplified fire susceptibility.
    3. **Post-Fire Greenness Trajectory**: The post-fire observation shows increased vegetation-index values relative to the pre-fire observation across a substantial proportion of valid pixels (65.97% in MSAVI). This may reflect rapid understory vegetation flush, seasonal variation, rainfall onset, and phenological flushes. Long-term structural recovery of woody biomass requires multi-year monitoring.
    4. **Actionable Spatial Prioritization**: 338.20 km² (9.71%) of Similipal Forest is categorized as **Very High Restoration Priority**, concentrated in central and western core valleys where combined degradation was highest.
    """)
