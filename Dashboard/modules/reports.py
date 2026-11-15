"""
Module 9: Reports & Data Export for Similipal Forest Intelligence.
Provides academic download packages, CSV area statistics, project summary reports, and GeoTIFF references.
"""

import streamlit as st
import pandas as pd
import io
import os
from pathlib import Path

from Dashboard.config import (
    STUDY_AREA,
    NOTEBOOK_STATS,
    RASTER_PATHS,
    CSV_PATHS
)
from Dashboard.utils.stats_calculator import (
    get_indices_comparison_df,
    get_restoration_priority_df,
    get_burn_severity_df
)

def df_to_md(df: pd.DataFrame) -> str:
    """Robust conversion of a DataFrame to a Markdown table with fallback."""
    if df is None or df.empty:
        return ""
    try:
        return df.to_markdown(index=False)
    except Exception:
        # Reliable pure-python markdown formatter
        headers = [str(c) for c in df.columns]
        lines = ["| " + " | ".join(headers) + " |"]
        lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
        for _, row in df.iterrows():
            vals = []
            for v in row:
                if isinstance(v, float):
                    vals.append(f"{v:,.4f}" if abs(v) < 10 else f"{v:,.2f}")
                else:
                    vals.append(str(v))
            lines.append("| " + " | ".join(vals) + " |")
        return "\n".join(lines)

def generate_markdown_report() -> str:
    """Generates a comprehensive academic research summary report in Markdown format."""
    indices_df = get_indices_comparison_df()
    priority_df = get_restoration_priority_df()
    bri_reserve_df = get_burn_severity_df(scope="reserve_boundary")
    bri_scene_df = get_burn_severity_df(scope="full_scene")
    sens_df = pd.read_csv(CSV_PATHS["Weight_Sensitivity"]) if CSV_PATHS["Weight_Sensitivity"].exists() else pd.DataFrame()

    report = f"""# SIMILIPAL FOREST INTELLIGENCE RESEARCH REPORT
## Multi-Temporal Forest Fire Detection, Vegetation Change Assessment and Ecological Vulnerability Analysis

### 1. STUDY AREA SPECIFICATION
- **Target Reserve**: {STUDY_AREA['name']}
- **Geographic Location**: {STUDY_AREA['location']}
- **Coordinates (Center)**: {STUDY_AREA['coordinates']['lat']}°N, {STUDY_AREA['coordinates']['lon']}°E
- **Spatial Bounds**: Lat [{STUDY_AREA['bounds']['min_lat']}, {STUDY_AREA['bounds']['max_lat']}], Lon [{STUDY_AREA['bounds']['min_lon']}, {STUDY_AREA['bounds']['max_lon']}]
- **Total Classified Area (Reserve Boundary)**: 3,485.37 km² (348,536.9 Geodesic Hectares)
- **Observation Phases**: Pre-Fire (Baseline), During-Fire (Impact), Post-Fire (Response)
- **Satellite Platforms**: European Space Agency Sentinel-2 MSI (B2, B4, B8, B11) & MODIS/Landsat Thermal

---

### 2. MULTI-TEMPORAL VEGETATION & MOISTURE DYNAMICS
{df_to_md(indices_df)}

#### Statistical Observations:
1. **NDVI (Chlorophyll Greenness)**: Mean NDVI declined from 0.3515 (Pre-Fire) to 0.3230 (During-Fire), representing an area-wide relative drop of -6.07% (std: 16.56%). Post-fire observation rose to 0.3682 (+0.0167).
2. **EVI (Canopy Structure)**: Mean EVI dropped from 0.3695 to 0.3281 during fire (-11.2%), increasing to 0.3900 post-fire.
3. **MSAVI (Soil-Adjusted)**: Pre-fire mean: 0.24573545, During-fire mean: 0.23015447 (Mean Δ = -0.01558), Post-fire mean: 0.27652243 (Mean Δ = +0.03079).
   - During-fire shift: 55.80% of valid pixels classified as Decreased, 21.10% No significant change, 23.10% Increased.
   - Post-fire shift: 21.37% of valid pixels classified as Decreased, 12.65% No significant change, 65.97% Increased.
4. **NDMI (Moisture Content)**: Acute foliar moisture drop of 80.9% (0.0899 to 0.0172), with 66.74% of valid pixels showing moisture decrease during fire.
5. **Relative LST (Thermal)**: Surface relative thermal radiance increased by a mean of +2,420.59 relative units during active fires.

---

### 3. POST-FIRE RESTORATION PRIORITY ZONATION
Geodesic area calculation on WGS84 ellipsoid (`pyproj.Geod`):

{df_to_md(priority_df)}

- **High + Very High Priority Zones**: 781.51 km² (22.42% of Similipal Reserve)
- **Very High Priority Core**: 338.20 km² (9.71%) requiring strategic intervention.

---

### 4. BURN IMPACT CLASSIFICATION (BRI)
*Methodological note: BRI is formulated as (B8 - B11)/(B8 + B11), mathematically identical to NDMI, utilized as a burn disparity metric.*

#### A. Within Similipal Reserve Boundary (3,485.37 km²):
{df_to_md(bri_reserve_df)}

#### B. Full Regional Satellite Scene (5,615.53 km² - Original Tile Quartiles from Notebook Cell 124):
{df_to_md(bri_scene_df)}

---

### 5. COUPLED FIRE IMPACT MODELING
- **Regression Equation**: ΔNDVI = -0.0032 + (0.6898) × ΔBRI + (0.0000) × ΔLST
- **R² Score**: 0.3206 (32.1% of canopy loss explained by fire severity and surface temperature)
- **Correlation with Observed (r)**: 0.582 (p < 0.0001)
- **Dominant Driver**: Fire Severity (BRI, r = 0.702) dominates over thermal forcing (r = -0.052).

---

### 6. WEIGHT SENSITIVITY ANALYSIS
{df_to_md(sens_df) if not sens_df.empty else "Sensitivity analysis table available in project files."}

---
*Report compiled from verified project rasters and notebook outputs.*
"""
    return report

def render():
    st.markdown("## Reports, Data Export & Downloads")
    st.markdown("""
    Download verified academic research tables, CSV area statistics, consolidated Markdown research summaries, 
    and inspect direct GeoTIFF file references for external GIS processing (QGIS, ArcGIS, Python).
    """)

    st.markdown("---")

    # CSV Download Section
    st.markdown("### Tabular Data & Statistics Export (CSV)")
    c1, c2, c3, c4 = st.columns(4)

    # 1. Indices Comparison CSV
    indices_df = get_indices_comparison_df()
    csv_indices = indices_df.to_csv(index=False).encode('utf-8')
    with c1:
        st.download_button(
            label="Indices Summary (CSV)",
            data=csv_indices,
            file_name="Similipal_Vegetation_Indices_Summary.csv",
            mime="text/csv",
            use_container_width=True
        )
        st.caption("Cross-phase means for NDVI, EVI, MSAVI, NDMI, BRI.")

    # 2. Restoration Priority Area CSV
    priority_df = get_restoration_priority_df()
    csv_priority = priority_df.to_csv(index=False).encode('utf-8')
    with c2:
        st.download_button(
            label="Restoration Priority (CSV)",
            data=csv_priority,
            file_name="Similipal_Restoration_Priority_Area.csv",
            mime="text/csv",
            use_container_width=True
        )
        st.caption("Verified area in km², hectares, and percentages.")

    # 3. Burn Impact CSV
    bri_reserve_df = get_burn_severity_df(scope="reserve_boundary")
    csv_bri = bri_reserve_df.to_csv(index=False).encode('utf-8')
    with c3:
        st.download_button(
            label="Burn Impact (Reserve CSV)",
            data=csv_bri,
            file_name="Similipal_Burn_Impact_Reserve_Boundary.csv",
            mime="text/csv",
            use_container_width=True
        )
        st.caption("Burn impact area within 3,485.37 km² reserve.")

    # 4. Sensitivity CSV
    sens_csv = CSV_PATHS["Weight_Sensitivity"]
    sens_data = b""
    if sens_csv.exists():
        with open(sens_csv, "rb") as f:
            sens_data = f.read()
    with c4:
        st.download_button(
            label="Sensitivity Analysis (CSV)",
            data=sens_data,
            file_name="Similipal_Weight_Sensitivity_Analysis.csv",
            mime="text/csv",
            use_container_width=True
        )
        st.caption("5 weighting scenarios for model sensitivity.")

    st.markdown("---")

    # Full Research Report Download
    st.markdown("### Consolidated Academic Research Report")
    st.markdown("Download a comprehensive markdown executive summary documenting methodology, validated models, and zonation tables.")
    
    report_text = generate_markdown_report()
    st.download_button(
        label="Download Full Research Summary (.md)",
        data=report_text.encode('utf-8'),
        file_name="Similipal_Forest_Fire_Research_Summary.md",
        mime="text/markdown"
    )

    with st.expander("Preview Research Summary Report"):
        st.markdown(report_text)

    st.markdown("---")

    # GeoTIFF File Reference
    st.markdown("### GIS GeoTIFF Raster Inventory")
    st.markdown("""
    All GeoTIFF outputs are georeferenced in **EPSG:4326** and can be opened in QGIS, ArcGIS, or Python (Rasterio/GDAL):
    """)

    inv_records = [
        {"Product": "Pre-Fire Sentinel-2", "Path": str(RASTER_PATHS["S2"]["Pre-Fire"]), "Type": "4-Band Multi-Spectral", "Size": "520 MB"},
        {"Product": "During-Fire Sentinel-2", "Path": str(RASTER_PATHS["S2"]["During-Fire"]), "Type": "4-Band Multi-Spectral", "Size": "544 MB"},
        {"Product": "Post-Fire Sentinel-2", "Path": str(RASTER_PATHS["S2"]["Post-Fire"]), "Type": "4-Band Multi-Spectral", "Size": "551 MB"},
        {"Product": "Ecological Vulnerability Score", "Path": str(RASTER_PATHS["EVS"]["EVS_Score"]), "Type": "Float32 Composite", "Size": "154 MB"},
        {"Product": "Restoration Priority Classification", "Path": str(RASTER_PATHS["EVS"]["Restoration_Priority"]), "Type": "UInt8 4-Class", "Size": "5 MB"},
        {"Product": "Burn Impact Classification", "Path": str(RASTER_PATHS["BRI"]["Impact_Classification"]), "Type": "UInt8 5-Class", "Size": "58 MB"},
        {"Product": "Pre-Fire MSAVI (Exported)", "Path": str(RASTER_PATHS["MSAVI"]["Pre-Fire"]), "Type": "Float32 Index", "Size": "236 MB"},
        {"Product": "During-Fire MSAVI (Exported)", "Path": str(RASTER_PATHS["MSAVI"]["During-Fire"]), "Type": "Float32 Index", "Size": "236 MB"},
        {"Product": "Post-Fire MSAVI (Exported)", "Path": str(RASTER_PATHS["MSAVI"]["Post-Fire"]), "Type": "Float32 Index", "Size": "238 MB"},
        {"Product": "ΔNDVI During Fire", "Path": str(RASTER_PATHS["NDVI"]["dNDVI_During"]), "Type": "Float32 Difference", "Size": "232 MB"},
        {"Product": "ΔLST During Fire", "Path": str(RASTER_PATHS["LST"]["dLST_During"]), "Type": "Float32 Difference", "Size": "232 MB"},
    ]
    st.dataframe(pd.DataFrame(inv_records), use_container_width=True, hide_index=True)

    st.markdown("""
    <div class="info-callout">
        Source GeoTIFF files reside directly in <code>Fire_Project/</code> and root directories for persistent local GIS access.
    </div>
    """, unsafe_allow_html=True)
