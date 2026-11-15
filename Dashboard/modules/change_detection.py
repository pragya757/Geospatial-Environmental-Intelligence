"""
Module 7: Temporal Change Detection & Coupled Fire Impact Modeling.
Investigates multi-temporal spectral shifts and evaluates the biophysical regression model
coupling NDVI decline with fire severity (BRI) and surface heating (LST).
"""

import streamlit as st
from streamlit_folium import st_folium
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from Dashboard.config import RASTER_PATHS, NOTEBOOK_STATS
from Dashboard.components.maps import create_folium_raster_map
from Dashboard.components.metrics_cards import render_metric_card

def render():
    st.markdown("## Temporal Change Detection & Coupled Impact Modeling")
    st.markdown("""
    Quantify pixel-level multi-temporal trajectories between observation phases.
    This module features single-index difference analysis and the author's **Coupled Fire Impact Model** 
    examining the drivers of observed vegetation loss.
    """)

    st.markdown("""
    <div class="warning-callout">
        <strong>Ecological Nuance & Scientific Interpretation:</strong><br>
        The post-fire observation shows increased vegetation-index values relative to the pre-fire observation across a substantial proportion of valid pixels. 
        This may reflect vegetation regrowth, seasonal variation, rainfall, and phenological changes. 
        Long-term recovery of climax forest canopy and structural woody biomass requires additional multi-year observations and ground verification.
    </div>
    """, unsafe_allow_html=True)

    tab_change_maps, tab_coupled_model = st.tabs([
        "1. Multi-Temporal Change Maps",
        "2. Coupled Fire Impact Model (BRI + LST)"
    ])

    # ==================== SUB-TAB 1: CHANGE MAPS ====================
    with tab_change_maps:
        st.markdown("### Temporal Difference Products")
        
        col_ctrl1, col_ctrl2 = st.columns(2)
        with col_ctrl1:
            index_selected = st.selectbox(
                "Select Index for Change Analysis",
                ["NDVI (Vegetation Greenness)", "MSAVI (Soil-Adjusted)", "NDMI / BRI (Moisture & Burn Disparity)", "LST (Relative Thermal)"]
            )
        with col_ctrl2:
            time_comparison = st.selectbox(
                "Comparison Interval",
                ["During-Fire vs Pre-Fire (Fire Impact)", "Post-Fire vs Pre-Fire (Initial Response)"]
            )

        if "NDVI" in index_selected:
            raster_p = str(RASTER_PATHS["NDVI"]["dNDVI_During"]) if "During-Fire" in time_comparison else str(RASTER_PATHS["NDVI"]["dNDVI_Post"])
            cmap = "RdYlGn"
            vmin, vmax = -0.15, 0.15
            unit_label = "ΔNDVI"
            mean_val = NOTEBOOK_STATS["NDVI"]["dNDVI_During"]["mean"] if "During-Fire" in time_comparison else NOTEBOOK_STATS["NDVI"]["dNDVI_Post"]["mean"]
        elif "MSAVI" in index_selected:
            raster_p = str(RASTER_PATHS["MSAVI"]["dMSAVI_During"]) if "During-Fire" in time_comparison else str(RASTER_PATHS["MSAVI"]["dMSAVI_Post"])
            cmap = "RdYlGn"
            vmin, vmax = -0.15, 0.15
            unit_label = "ΔMSAVI"
            mean_val = NOTEBOOK_STATS["MSAVI"]["dMSAVI_During"]["mean"] if "During-Fire" in time_comparison else NOTEBOOK_STATS["MSAVI"]["dMSAVI_Post"]["mean"]
        elif "LST" in index_selected:
            raster_p = str(RASTER_PATHS["LST"]["dLST_During"]) if "During-Fire" in time_comparison else str(RASTER_PATHS["LST"]["dLST_Post"])
            cmap = "inferno"
            vmin, vmax = 500, 3500
            unit_label = "ΔLST (Relative Units)"
            mean_val = NOTEBOOK_STATS["LST"]["dLST_During"]["mean"] if "During-Fire" in time_comparison else NOTEBOOK_STATS["LST"]["dLST_Post"]["mean"]
        else: # NDMI / BRI
            raster_p = str(RASTER_PATHS["BRI"]["dBRI_During"]) if "During-Fire" in time_comparison else str(RASTER_PATHS["BRI"]["dBRI_Post"])
            cmap = "hot"
            vmin, vmax = 0.0, 0.2
            unit_label = "ΔBRI"
            mean_val = NOTEBOOK_STATS["BRI"]["dBRI_During"]["mean"] if "During-Fire" in time_comparison else NOTEBOOK_STATS["BRI"]["dBRI_Post"]["mean"]

        c_map, c_desc = st.columns([1.8, 1.0])
        with c_map:
            st.markdown(f"#### {index_selected} — {time_comparison}")
            m = create_folium_raster_map(raster_p, title=f"{unit_label} Change", cmap_name=cmap, vmin=vmin, vmax=vmax, opacity=0.9)
            st_folium(m, width=650, height=450, key="change_folium")

        with c_desc:
            st.markdown("#### Statistical Summary")
            render_metric_card(
                title=f"Mean {unit_label}",
                value=f"{mean_val:+.4f}" if abs(mean_val) < 100 else f"{mean_val:+,.1f}",
                subtitle="Study Area Spatial Mean",
                delta="During Fire Drop" if "During" in time_comparison and mean_val < 0 else "Temporal Difference",
                delta_type="normal"
            )

            st.markdown(f"""
            - **Common Spatial Mask**: Rasters are harmonized on a shared valid pixel grid.
            - **Spatial Extent**: 7,798 × 7,793 pixels.
            - **Source File**: `{raster_p.split('/')[-1]}`
            """)

    # ==================== SUB-TAB 2: COUPLED MODEL ====================
    with tab_coupled_model:
        st.markdown("### Coupled Fire Impact Modeling (Notebook Cells 70–90)")
        st.markdown("""
        To examine whether observed vegetation changes were driven by fire severity or thermal anomalies, 
        the research evaluated two analytical approaches:
        - **Way 1 (Direct Observation)**: Pixel-wise $\\Delta\\text{NDVI}$ calculation between during-fire and pre-fire imagery.
        - **Way 2 (Coupled Biophysical Model)**: Multi-variable linear regression modeling $\\Delta\\text{NDVI}$ as a joint function of fire severity ($\\Delta\\text{BRI}$) and surface thermal heating ($\\Delta\\text{LST}$).
        """)

        model_meta = NOTEBOOK_STATS["NDVI"]["Model_Coupled"]

        st.markdown(f"""
        <div class="info-callout" style="font-size: 1.05rem;">
            <strong>Validated Regression Equation:</strong><br>
            $$\\Delta\\text{{NDVI}} = -0.0032 + (0.6898) \\times \\Delta\\text{{BRI}} + (0.0000) \\times \\Delta\\text{{LST}}$$
            <div style="margin-top: 8px; font-size: 0.9rem;">
                <strong>R² Score:</strong> {model_meta['r2']:.4f} &nbsp;|&nbsp; 
                <strong>Correlation with Observed (r):</strong> {model_meta['correlation_observed_modeled']:.3f} ($p < 0.0001$) &nbsp;|&nbsp; 
                <strong>Valid Pixels Modeled:</strong> {model_meta['valid_pixels']:,}
            </div>
        </div>
        """, unsafe_allow_html=True)

        m_col1, m_col2 = st.columns(2)
        with m_col1:
            st.markdown("#### Driver Importance & Correlation Breakdown")
            corr_df = pd.DataFrame([
                {"Driver": "Fire Severity (ΔBRI)", "Correlation (r)": model_meta["corr_ndvi_bri"], "p-value": "< 0.0001", "Significance": "Primary Driver"},
                {"Driver": "Thermal Stress (ΔLST)", "Correlation (r)": model_meta["corr_ndvi_lst"], "p-value": "< 0.0001", "Significance": "Secondary Local Modulator"},
            ])
            st.dataframe(corr_df, use_container_width=True, hide_index=True)

            fig_imp = px.bar(
                corr_df,
                x="Driver",
                y="Correlation (r)",
                color="Driver",
                color_discrete_sequence=["#C0392B", "#2980B9"],
                text="Correlation (r)"
            )
            fig_imp.update_layout(
                paper_bgcolor="#121614",
                plot_bgcolor="#141C18",
                font=dict(color="#E0E6E2"),
                height=260,
                showlegend=False,
                yaxis=dict(gridcolor="#23362B", range=[-0.2, 0.8])
            )
            st.plotly_chart(fig_imp, use_container_width=True)

        with m_col2:
            st.markdown("#### Observed vs Modeled ΔNDVI")
            st.markdown("""
            The spatial correlation ($r = 0.582$) between observed canopy loss and model-predicted loss confirms:
            1. Observed vegetation degradation across Similipal was strongly correlated with **fire severity ($\Delta$BRI)**.
            2. The regression model explains 32.1% of spatial variance across 60.5 million valid pixels.
            """)
            
            obs_vs_mod = pd.DataFrame({
                "Metric": ["Mean Value", "Std Deviation", "Min Value", "Max Value"],
                "Observed ΔNDVI (Way 1)": [-0.02845, 0.04860, -0.51598, 0.51433],
                "Modeled ΔNDVI (Way 2)": [-0.02869, 0.03474, -0.31030, 0.36586]
            })
            st.dataframe(obs_vs_mod, use_container_width=True, hide_index=True)
            st.caption("Raster source: `Modeled_dNDVI.tif` vs `dNDVI_During.tif`")
