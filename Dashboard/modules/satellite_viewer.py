"""
Module 2: Satellite Image Comparison & Spectral Composite Viewer.
Inspects Sentinel-2 multi-spectral observations across Pre-Fire, During-Fire, and Post-Fire phases.
"""

import streamlit as st
from streamlit_folium import st_folium
import numpy as np

from Dashboard.config import RASTER_PATHS, STUDY_AREA
from Dashboard.utils.raster_loader import (
    load_s2_composite,
    get_raster_metadata
)
from Dashboard.components.maps import create_folium_rgb_map

def render():
    st.markdown("## Sentinel-2 Satellite Image Comparison")
    st.markdown("""
    Inspect multi-spectral Sentinel-2 Surface Reflectance (SR) observations across the three study phases.
    The source imagery contains four spectral bands:
    **Band 1 (B2 - Blue)**, **Band 2 (B4 - Red)**, **Band 3 (B8 - NIR)**, and **Band 4 (B11 - SWIR)**.
    """)

    # Controls
    ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([1.2, 1.2, 1.0])
    with ctrl_col1:
        composite_choice = st.selectbox(
            "Spectral Composite",
            [
                "NIR-Red-Blue (Vegetation Vitality)",
                "SWIR-NIR-Red (Burn & Moisture Contrast)"
            ],
            help="NIR-Red-Blue (B8-B4-B2) highlights active chlorophyll in red/pink tones. SWIR-NIR-Red (B11-B8-B4) highlights burn scars and exposed soil in orange/charcoal tones."
        )
    with ctrl_col2:
        view_mode = st.radio(
            "Display Mode",
            ["Single Phase Interactive Map", "Side-by-Side Phase Comparison"],
            horizontal=True
        )
    with ctrl_col3:
        overlay_boundary = st.checkbox("Overlay Similipal Boundary", value=True)

    st.markdown("---")

    if view_mode == "Single Phase Interactive Map":
        phase = st.select_slider(
            "Select Observation Phase",
            options=["Pre-Fire", "During-Fire", "Post-Fire"],
            value="During-Fire"
        )
        
        raster_path = str(RASTER_PATHS["S2"][phase])
        meta = get_raster_metadata(raster_path)

        col_map, col_meta = st.columns([2.2, 1.0])
        with col_map:
            st.markdown(f"### {phase} Sentinel-2 Scene")
            st.caption(f"Composite: {composite_choice} | Dimensions: {meta.get('width', 7793)} × {meta.get('height', 7798)} (OpenStreetMap basemap)")
            
            internal_comp_name = "SWIR-NIR-Red (Burn & Moisture)" if "SWIR" in composite_choice else "NIR-Red-Blue (Vegetation)"
            folium_map = create_folium_rgb_map(
                raster_path,
                composite_name=internal_comp_name,
                opacity=0.92,
                overlay_boundary=overlay_boundary
            )
            st_folium(folium_map, width=750, height=520)

        with col_meta:
            clean_phase = phase.replace("-", "")
            st.markdown("### Raster Metadata")
            st.markdown(f"""
            - **File Name**: `{meta.get('filename', f'S2_{clean_phase}.tif')}`
            - **Dimensions**: {meta.get('width', 7793):,} × {meta.get('height', 7798):,} px
            - **Total Pixels**: ~60.77 Million
            - **Spectral Bands**: {meta.get('count', 4)}
            - **Coordinate Reference**: `{meta.get('crs', 'EPSG:4326')}`
            - **File Size**: {meta.get('file_size_mb', 543.8)} MB
            """)

            st.markdown("#### Band Mapping Guide")
            if "SWIR" in composite_choice:
                st.markdown("""
                - **Red Channel**: Band 4 (SWIR - B11, 1610 nm)
                - **Green Channel**: Band 3 (NIR - B8, 842 nm)
                - **Blue Channel**: Band 2 (Red - B4, 665 nm)
                *Burned patches appear as dark brick-red/brown, unburned dense vegetation appears bright green.*
                """)
            else:
                st.markdown("""
                - **Red Channel**: Band 3 (NIR - B8, 842 nm)
                - **Green Channel**: Band 2 (Red - B4, 665 nm)
                - **Blue Channel**: Band 1 (Blue - B2, 490 nm)
                *Dense healthy canopy reflects strongly in NIR (bright red/orange); degraded or burned zones show dull grey/cyan tones.*
                """)

    else:
        # Side-by-Side comparison
        st.markdown("### Multi-Temporal Side-by-Side View")
        comp_col1, comp_col2 = st.columns(2)
        with comp_col1:
            phase1 = st.selectbox("Left Scene", ["Pre-Fire", "During-Fire", "Post-Fire"], index=0)
        with comp_col2:
            phase2 = st.selectbox("Right Scene", ["Pre-Fire", "During-Fire", "Post-Fire"], index=1)

        c1, c2 = st.columns(2)
        internal_comp_name = "SWIR-NIR-Red (Burn & Moisture)" if "SWIR" in composite_choice else "NIR-Red-Blue (Vegetation)"

        with c1:
            st.markdown(f"#### 1. {phase1} Image")
            path1 = str(RASTER_PATHS["S2"][phase1])
            m1 = create_folium_rgb_map(path1, composite_name=internal_comp_name, opacity=0.92, overlay_boundary=overlay_boundary)
            st_folium(m1, width=480, height=450, key=f"map_{phase1}")

        with c2:
            st.markdown(f"#### 2. {phase2} Image")
            path2 = str(RASTER_PATHS["S2"][phase2])
            m2 = create_folium_rgb_map(path2, composite_name=internal_comp_name, opacity=0.92, overlay_boundary=overlay_boundary)
            st_folium(m2, width=480, height=450, key=f"map_{phase2}")
