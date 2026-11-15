"""
Module 5: Burn Impact Analysis & Burning Ratio Index (BRI) Classification.
Examines relative fire burn impact severity classes, area statistics,
and explains the methodological relationship between regional tile quartiles and the reserve boundary.
"""

import streamlit as st
from streamlit_folium import st_folium
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from Dashboard.config import RASTER_PATHS, NOTEBOOK_STATS, COLOR_PALETTES
from Dashboard.components.maps import create_folium_raster_map
from Dashboard.components.metrics_cards import render_metric_card
from Dashboard.utils.stats_calculator import get_burn_severity_df

def render():
    st.markdown("## Burn Impact Analysis (Burning Ratio Index - BRI)")
    st.markdown("""
    Spatial assessment of wildfire burn impact zonation across Similipal Forest.
    The research utilizes the **Burning Ratio Index (BRI)** computed from Sentinel-2 Near-Infrared (Band 8) and Short-Wave Infrared (Band 11).
    """)

    # Scientific Transparency Callout: BRI vs NDMI
    st.markdown("""
    <div class="info-callout">
        <strong>Spectral Formulation & Mathematical Relationship:</strong><br>
        In the research notebook (Cells 31–34), BRI is formulated as:
        $$\\text{BRI} = \\frac{\\text{NIR} - \\text{SWIR}}{\\text{NIR} + \\text{SWIR}} = \\frac{\\text{B8} - \\text{B11}}{\\text{B8} + \\text{B11}}$$
        This is mathematically the same band ratio as the <strong>Normalized Difference Moisture Index (NDMI)</strong> (Gao, 1996). 
        To maintain research integrity, BRI and NDMI are not presented as two independent spectral measurements. 
        In this research, this ratio is specifically utilized as a <strong>burn-ratio disparity metric</strong> to capture 
        the spectral shift between pre-fire and post-fire canopy states ($\\Delta\\text{BRI} = \\text{BRI}_{\\text{pre}} - \\text{BRI}_{\\text{post}}$) 
        and partition the landscape into relative impact classes.
    </div>
    """, unsafe_allow_html=True)

    # Key metrics
    bri_stats = NOTEBOOK_STATS["BRI"]
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        render_metric_card("Pre-Fire Mean BRI", f"{bri_stats['Pre-Fire']['mean']:.4f}", "Intact Canopy", "Baseline State", "neutral")
    with m2:
        render_metric_card("During-Fire Mean BRI", f"{bri_stats['During-Fire']['mean']:.4f}", "Mean Value Drop", "-80.8% Drop", "normal")
    with m3:
        render_metric_card("During Mean ΔBRI", f"{bri_stats['dBRI_During']['mean']:.4f}", "Burn Disparity", "Strong Fire Signal", "normal")
    with m4:
        render_metric_card("Post Mean ΔBRI", f"{bri_stats['dBRI_Post']['mean']:.4f}", "Residual Disparity", "Scorched Signal", "normal")

    st.markdown("---")

    # Methodological Audit: Full Scene Quartiles vs Reserve Boundary
    st.markdown("""
    <div class="warning-callout">
        <strong>Methodological Investigation of Area Statistics:</strong><br>
        The research notebook evaluated burn impact under two distinct spatial coverages:
        <ol style="margin-bottom: 0; padding-left: 20px;">
            <li><strong>Full Regional Satellite Scene (5,615.53 km²):</strong> In Notebook Cell 124, <code>BRI_Impact_Area_Statistics.csv</code> was generated over the full unclipped Sentinel-2 tile extent (60,755,527 pixels). The positive change pixels (43,859,466 pixels) were split into <strong>four equal quartiles (25%, 50%, 75% percentiles)</strong>, mathematically producing exactly <strong>10,964,866 pixels (~1,013.5 km² each)</strong> for Low, Moderate, High, and Very High classes.</li>
            <li><strong>Within Similipal Reserve Boundary (3,485.37 km²):</strong> When clipped to the official reserve boundary (37,714,672 valid pixels, matching the EVS mask), the distribution reflects actual conservation zonation: <strong>Very High Impact: 731.59 km² (20.99%)</strong>, <strong>High Impact: 662.93 km² (19.02%)</strong>, <strong>Moderate: 623.17 km² (17.88%)</strong>, <strong>Low: 606.21 km² (17.39%)</strong>, and <strong>No Positive Change: 861.47 km² (24.72%)</strong>.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

    # Scope Selector for Tables & Charts
    scope_choice = st.radio(
        "Select Spatial Analysis Scope",
        [
            "Similipal Reserve Boundary (3,485.37 km² - Conservation Focus)",
            "Full Regional Satellite Scene (5,615.53 km² - Original Tile Quartiles)"
        ],
        horizontal=True
    )
    selected_scope = "full_scene" if "Full Regional" in scope_choice else "reserve_boundary"

    # Map & Area Table Side-by-Side
    col_map, col_table = st.columns([1.5, 1.2])

    with col_map:
        st.markdown("### Burn Impact Classification Map")
        st.caption("Classified using notebook relative quantile thresholds (Cell 124) on OpenStreetMap basemap.")
        
        map_product = st.selectbox(
            "Select Product to View",
            [
                "Burn Impact Classification (5 Classes)",
                "ΔBRI During-Fire (Continuous Difference)",
                "ΔBRI Post-Fire (Continuous Difference)",
                "During-Fire BRI",
                "Pre-Fire BRI"
            ]
        )

        if "Classification" in map_product:
            raster_p = str(RASTER_PATHS["BRI"]["Impact_Classification"])
            cmap = "YlOrRd"
            vmin, vmax = 0, 4
            title = "Burn Impact Severity Classes"
        elif "ΔBRI During-Fire" in map_product:
            raster_p = str(RASTER_PATHS["BRI"]["dBRI_During"])
            cmap = "hot"
            vmin, vmax = 0.0, 0.2
            title = "ΔBRI During Fire"
        elif "ΔBRI Post-Fire" in map_product:
            raster_p = str(RASTER_PATHS["BRI"]["dBRI_Post"])
            cmap = "hot"
            vmin, vmax = 0.0, 0.2
            title = "ΔBRI Post Fire"
        elif "During-Fire BRI" in map_product:
            raster_p = str(RASTER_PATHS["BRI"]["During-Fire"])
            cmap = "YlGn"
            vmin, vmax = -0.2, 0.4
            title = "During-Fire BRI"
        else:
            raster_p = str(RASTER_PATHS["BRI"]["Pre-Fire"])
            cmap = "YlGn"
            vmin, vmax = -0.2, 0.4
            title = "Pre-Fire BRI"

        m = create_folium_raster_map(raster_p, title=title, cmap_name=cmap, vmin=vmin, vmax=vmax, opacity=0.9)
        st_folium(m, width=580, height=450, key="bri_folium")

    with col_table:
        st.markdown("### Area Statistics by Severity Class")
        scope_title = "Within Similipal Reserve" if selected_scope == "reserve_boundary" else "Full Scene Tile (Cell 124 CSV)"
        st.caption(f"Geodesic WGS84 area calculation ({scope_title}):")
        
        bri_df = get_burn_severity_df(scope=selected_scope)
        
        st.dataframe(
            bri_df[["Severity Class", "Area (km2)", "Area (Hectares)", "Percentage (%)"]].style.format({
                "Area (km2)": "{:,.2f}",
                "Area (Hectares)": "{:,.1f}",
                "Percentage (%)": "{:.2f}%"
            }),
            use_container_width=True,
            hide_index=True
        )

        st.markdown("#### Relative Impact Thresholds")
        st.markdown("""
        Quantile thresholds derived in notebook Cell 124:
        - **No Positive Change**: $\\Delta\\text{BRI} \\le 0$
        - **Low Impact**: $0 < \\Delta\\text{BRI} \\le 0.0365$
        - **Moderate Impact**: $0.0365 < \\Delta\\text{BRI} \\le 0.0751$
        - **High Impact**: $0.0751 < \\Delta\\text{BRI} \\le 0.1229$
        - **Very High Impact**: $\\Delta\\text{BRI} > 0.1229$
        """)

    st.markdown("---")

    # Bar chart of Burn Impact Areas
    st.markdown("### Area Comparison Across Burn Severity Classes (km²)")
    fig = px.bar(
        bri_df,
        x="Severity Class",
        y="Area (km2)",
        color="Severity Class",
        color_discrete_map={
            "No Positive Change": "#27AE60",
            "Low Impact": "#F39C12",
            "Moderate Impact": "#E67E22",
            "High Impact": "#C0392B",
            "Very High Impact": "#78281F"
        },
        text="Area (km2)"
    )
    fig.update_traces(texttemplate='%{text:,.1f} km²', textposition='outside')
    fig.update_layout(
        paper_bgcolor="#121614",
        plot_bgcolor="#141C18",
        font=dict(color="#E0E6E2"),
        height=380,
        showlegend=False,
        yaxis=dict(gridcolor="#23362B", title="Area (km²)"),
        xaxis=dict(gridcolor="#23362B", title="Severity Class")
    )
    st.plotly_chart(fig, use_container_width=True)
