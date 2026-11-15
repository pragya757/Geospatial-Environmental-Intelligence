"""
Module 3: Vegetation Index Analysis (NDVI, EVI, MSAVI, NDMI).
In-depth multi-temporal evaluation of forest canopy greenness, canopy architecture,
soil-adjusted vegetation index, and canopy moisture content.
"""

import streamlit as st
from streamlit_folium import st_folium
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from Dashboard.config import RASTER_PATHS, NOTEBOOK_STATS, COLOR_PALETTES
from Dashboard.components.maps import create_folium_raster_map
from Dashboard.components.metrics_cards import render_metric_card
from Dashboard.components.charts import create_change_distribution_bar

def render():
    st.markdown("## Vegetation & Moisture Index Analysis")
    st.markdown("""
    Evaluate multi-temporal forest canopy dynamics across four complementary biophysical indicators.
    These indices capture distinct physiological and structural dimensions of the Similipal forest canopy.
    """)

    st.markdown("""
    <div class="info-callout">
        <strong>Biophysical Distinction Between Indices:</strong><br>
        <strong>NDVI</strong> reflects chlorophyll absorption and general photosynthetic canopy greenness.<br>
        <strong>EVI</strong> incorporates the Blue band to reduce atmospheric aerosol scattering and decouple canopy background saturation.<br>
        <strong>MSAVI</strong> incorporates a dynamic soil adjustment factor, particularly suited to post-burn environments where understory was scorched and bare soil exposed.<br>
        <strong>NDMI</strong> tracks internal foliar equivalent water thickness using Short-Wave Infrared (SWIR) reflectance.
    </div>
    """, unsafe_allow_html=True)

    tab_ndvi, tab_evi, tab_msavi, tab_ndmi = st.tabs([
        "A. NDVI (Chlorophyll Greenness)",
        "B. EVI (Canopy Structure)",
        "C. MSAVI (Soil-Adjusted Index)",
        "D. NDMI (Canopy Moisture Content)"
    ])

    # ==================== TAB A: NDVI ====================
    with tab_ndvi:
        st.markdown("### Normalized Difference Vegetation Index (NDVI)")
        st.latex(r"NDVI = \frac{NIR - Red}{NIR + Red} = \frac{B8 - B4}{B8 + B4}")

        phase_col1, phase_col2, phase_col3 = st.columns(3)
        ndvi_stats = NOTEBOOK_STATS["NDVI"]
        with phase_col1:
            render_metric_card("Pre-Fire Mean NDVI", f"{ndvi_stats['Pre-Fire']['mean']:.4f}", "60.71M Valid Pixels", "Baseline State", "neutral")
        with phase_col2:
            render_metric_card("During-Fire Mean NDVI", f"{ndvi_stats['During-Fire']['mean']:.4f}", "Active Fire Canopy Loss", f"Δ = {ndvi_stats['dNDVI_During']['mean']:.4f}", "normal")
        with phase_col3:
            render_metric_card("Post-Fire Mean NDVI", f"{ndvi_stats['Post-Fire']['mean']:.4f}", "Post-Fire Greening", f"Δ = +{ndvi_stats['dNDVI_Post']['mean']:.4f}", "normal")

        ndvi_phase = st.radio("Select NDVI Map Phase", ["Pre-Fire", "During-Fire", "Post-Fire", "Change (During - Pre)"], horizontal=True, key="ndvi_phase_radio")
        
        col_map, col_info = st.columns([1.8, 1.0])
        with col_map:
            if ndvi_phase == "Change (During - Pre)":
                raster_p = str(RASTER_PATHS["NDVI"]["dNDVI_During"])
                cmap = "RdYlGn"
                vmin, vmax = -0.15, 0.15
                title = "ΔNDVI (During - Pre Fire)"
            else:
                raster_p = str(RASTER_PATHS["NDVI"][ndvi_phase])
                cmap = "RdYlGn"
                vmin, vmax = 0.0, 0.7
                title = f"{ndvi_phase} NDVI"

            m = create_folium_raster_map(raster_p, title=title, cmap_name=cmap, vmin=vmin, vmax=vmax)
            st_folium(m, width=650, height=450, key="ndvi_folium")

        with col_info:
            st.markdown("#### NDVI Research Insights")
            st.markdown(f"""
            - **Pre-Fire Baseline**: Robust closed-canopy deciduous and semi-evergreen forest with average NDVI around **0.3515**.
            - **Fire Impact**: Widespread canopy scorching dropped mean NDVI to **0.3230**, with maximum localized degradation reaching **-0.5160**.
            - **Relative Decline**: Area-wide relative NDVI declined by a mean of **-6.07%** (std: 16.56%).
            - **Statistical Coupling**: Correlated with burn severity BRI ($r = 0.702$), confirming degradation was primarily fire-driven.
            """)
            st.caption(f"Source file: `{raster_p.split('/')[-1]}`")

    # ==================== TAB B: EVI ====================
    with tab_evi:
        st.markdown("### Enhanced Vegetation Index (EVI)")
        st.latex(r"EVI = 2.5 \times \frac{NIR - Red}{NIR + 6 \times Red - 7.5 \times Blue + 1} = 2.5 \times \frac{B8 - B4}{B8 + 6 \times B4 - 7.5 \times B2 + 1}")

        evi_stats = NOTEBOOK_STATS["EVI"]
        e_col1, e_col2, e_col3 = st.columns(3)
        with e_col1:
            render_metric_card("Pre-Fire Mean EVI", f"{evi_stats['Pre-Fire']['mean']:.4f}", "60.71M Valid Pixels", "Baseline Canopy", "neutral")
        with e_col2:
            render_metric_card("During-Fire Mean EVI", f"{evi_stats['During-Fire']['mean']:.4f}", "Canopy Thinning", f"Δ = {evi_stats['dEVI_During']['mean']:.4f}", "normal")
        with e_col3:
            render_metric_card("Post-Fire Mean EVI", f"{evi_stats['Post-Fire']['mean']:.4f}", "Regrowth & Phenology", f"Δ = +{evi_stats['dEVI_Post']['mean']:.4f}", "normal")

        evi_phase = st.radio("Select EVI Map Phase", ["Pre-Fire", "During-Fire", "Post-Fire"], horizontal=True, key="evi_phase_radio")
        
        em_col, ed_col = st.columns([1.8, 1.0])
        with em_col:
            raster_p = str(RASTER_PATHS["EVI"][evi_phase])
            m = create_folium_raster_map(raster_p, title=f"{evi_phase} EVI", cmap_name="YlGn", vmin=0.0, vmax=0.7)
            st_folium(m, width=650, height=450, key="evi_folium")

        with ed_col:
            st.markdown("#### EVI vs NDVI Correlation")
            st.markdown(f"""
            - **Pre-Fire Correlation**: $r = {evi_stats['Correlation_with_NDVI']['Pre-Fire']:.4f}$
            - **During-Fire Correlation**: $r = {evi_stats['Correlation_with_NDVI']['During-Fire']:.4f}$
            - **Post-Fire Correlation**: $r = {evi_stats['Correlation_with_NDVI']['Post-Fire']:.4f}$
            
            **Why EVI matters here:**  
            Wildfire smoke and aerosol plumes distort red-band absorption. EVI leverages **Band 1 (Blue)** to stabilize atmospheric aerosol scattering and remains unsaturated over dense sal (*Shorea robusta*) forest stands.
            """)
            st.caption(f"Source file: `{raster_p.split('/')[-1]}`")

    # ==================== TAB C: MSAVI ====================
    with tab_msavi:
        st.markdown("### Modified Soil-Adjusted Vegetation Index (MSAVI)")
        st.latex(r"MSAVI = \frac{2 \times NIR + 1 - \sqrt{(2 \times NIR + 1)^2 - 8 \times (NIR - Red)}}{2}")
        st.caption("Derived directly from Sentinel-2 surface reflectance bands without empirical soil-line parameters (Cells 141 & 144).")

        msavi_stats = NOTEBOOK_STATS["MSAVI"]
        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1:
            render_metric_card("Pre-Fire Mean MSAVI", f"{msavi_stats['Pre-Fire']['mean']:.8f}", "60.73M Valid Pixels", "Baseline State", "neutral")
        with m_col2:
            render_metric_card("During-Fire Mean MSAVI", f"{msavi_stats['During-Fire']['mean']:.8f}", "Soil Exposure Increase", f"Mean Δ = {msavi_stats['dMSAVI_During']['mean']:.5f}", "normal")
        with m_col3:
            render_metric_card("Post-Fire Mean MSAVI", f"{msavi_stats['Post-Fire']['mean']:.8f}", "Post-Fire Vegetation", f"Mean Δ = +{msavi_stats['dMSAVI_Post']['mean']:.5f}", "normal")

        ms_col, ch_col = st.columns([1.5, 1.3])
        with ms_col:
            msavi_view = st.selectbox(
                "Select MSAVI Product",
                ["During-Fire vs Pre-Fire (Impact)", "Post-Fire vs Pre-Fire (Response)", "During-Fire MSAVI", "Pre-Fire MSAVI", "Post-Fire MSAVI"]
            )
            if "vs Pre-Fire (Impact)" in msavi_view:
                raster_p = str(RASTER_PATHS["MSAVI"]["dMSAVI_During"])
                cmap = "RdYlGn"
                vmin, vmax = -0.15, 0.15
            elif "vs Pre-Fire (Response)" in msavi_view:
                raster_p = str(RASTER_PATHS["MSAVI"]["dMSAVI_Post"])
                cmap = "RdYlGn"
                vmin, vmax = -0.15, 0.15
            elif "During-Fire" in msavi_view:
                raster_p = str(RASTER_PATHS["MSAVI"]["During-Fire"])
                cmap = "YlGn"
                vmin, vmax = 0.0, 0.6
            elif "Post-Fire" in msavi_view:
                raster_p = str(RASTER_PATHS["MSAVI"]["Post-Fire"])
                cmap = "YlGn"
                vmin, vmax = 0.0, 0.6
            else:
                raster_p = str(RASTER_PATHS["MSAVI"]["Pre-Fire"])
                cmap = "YlGn"
                vmin, vmax = 0.0, 0.6

            m = create_folium_raster_map(raster_p, title=msavi_view, cmap_name=cmap, vmin=vmin, vmax=vmax)
            st_folium(m, width=580, height=430, key="msavi_folium")

        with ch_col:
            st.markdown("#### MSAVI Pixel Classification Breakdown")
            st.markdown("""
            Classification of valid pixels based on the research threshold of **±0.01 MSAVI change units** (Notebook Cell 144):
            """)
            
            dur_chart = create_change_distribution_bar(
                decrease_pct=msavi_stats["dMSAVI_During"]["decrease_pct"],
                stable_pct=msavi_stats["dMSAVI_During"]["stable_pct"],
                increase_pct=msavi_stats["dMSAVI_During"]["increase_pct"],
                title="During-Fire vs Pre-Fire MSAVI Shift (% of Pixels)"
            )
            st.plotly_chart(dur_chart, use_container_width=True)

            post_chart = create_change_distribution_bar(
                decrease_pct=msavi_stats["dMSAVI_Post"]["decrease_pct"],
                stable_pct=msavi_stats["dMSAVI_Post"]["stable_pct"],
                increase_pct=msavi_stats["dMSAVI_Post"]["increase_pct"],
                title="Post-Fire vs Pre-Fire MSAVI Shift (% of Pixels)"
            )
            st.plotly_chart(post_chart, use_container_width=True)

            st.markdown("""
            *Clarification: **55.80%** represents the proportion of valid pixels classified as decreased during fire (33,888,306 pixels), while **23.10%** increased and **21.10%** remained stable.*
            """)

    # ==================== TAB D: NDMI ====================
    with tab_ndmi:
        st.markdown("### Normalized Difference Moisture Index (NDMI)")
        st.latex(r"NDMI = \frac{NIR - SWIR}{NIR + SWIR} = \frac{B8 - B11}{B8 + B11}")

        ndmi_stats = NOTEBOOK_STATS["NDMI"]
        n_col1, n_col2, n_col3 = st.columns(3)
        with n_col1:
            render_metric_card("Pre-Fire Mean NDMI", f"{ndmi_stats['Pre-Fire']['mean']:.4f}", "Hydrated Foliage", "Baseline Moisture", "neutral")
        with n_col2:
            render_metric_card("During-Fire Mean NDMI", f"{ndmi_stats['During-Fire']['mean']:.4f}", "Acute Desiccation", f"Δ = {ndmi_stats['dNDMI_During']['mean']:.4f}", "normal")
        with n_col3:
            render_metric_card("Post-Fire Mean NDMI", f"{ndmi_stats['Post-Fire']['mean']:.4f}", "Partial Moisture Recovery", f"Δ = {ndmi_stats['dNDMI_Post']['mean']:.4f}", "normal")

        nm_col, nd_col = st.columns([1.8, 1.0])
        with nm_col:
            ndmi_phase = st.radio("Select NDMI Map Phase", ["Pre-Fire", "During-Fire", "Post-Fire"], horizontal=True, key="ndmi_phase_radio")
            raster_p = str(RASTER_PATHS["NDMI"][ndmi_phase])
            m = create_folium_raster_map(raster_p, title=f"{ndmi_phase} NDMI", cmap_name="BrBG", vmin=-0.2, vmax=0.4)
            st_folium(m, width=650, height=450, key="ndmi_folium")

        with nd_col:
            st.markdown("#### Moisture Depletion Dynamics")
            st.markdown(f"""
            - **Desiccation Extent**: **66.74% of valid pixels** experienced moisture-related decrease during fire.
            - **Stable Canopy**: **32.38%** preserved moisture, predominantly in moist valley bottoms and evergreen stream corridors.
            - **Post-Fire Deficit**: **47.59%** of the reserve remained in a relative moisture-deficit state post-fire.
            
            *SWIR Band 11 absorption directly correlates with liquid water thickness in leaves, serving as a critical indicator of fuel dryness.*
            """)
            st.caption(f"Source file: `{raster_p.split('/')[-1]}`")
