"""
Module 10: About the Project, Academic Research Context, Methodology & Citations.
"""

import streamlit as st
from Dashboard.config import STUDY_AREA

def render():
    st.markdown("## About the Similipal Forest Intelligence Research")
    
    st.markdown("""
    ### Academic Research Overview
    **Project Title**:  
    *Multi-Temporal Forest Fire Detection, Vegetation Change Assessment and Ecological Vulnerability Analysis Using Satellite Imagery – A Case Study of Similipal Forest, Odisha, India.*

    - **Researcher**: Pragya Paramita Sahoo
    - **Academic Degree**: Bachelor of Technology in Computer Science & Engineering
    - **Institution**: Department of Computing Technologies, College of Engineering and Technology, SRM Institute of Science and Technology, Kattankulathur, Tamil Nadu, India
    - **Project Guidance**: Dr. A. Pandiaraj, Assistant Professor
    - **Course Code**: 21CSP302L - Project Work
    """)

    st.markdown("---")

    # Study Area Geography Card
    st.markdown("### Geographic & Ecological Importance of Similipal")
    st.markdown("""
    The **Similipal Biosphere Reserve**, situated in the Mayurbhanj district of northern Odisha, India, spans over 5,569 km² 
    (with the tiger reserve comprising approximately 2,750 km²). 
    It was officially designated under the **UNESCO World Network of Biosphere Reserves in 2009**.
    
    - **Forest Types**: Tropical moist deciduous, dry deciduous, and semi-evergreen forests dominated by Sal (*Shorea robusta*), Asan (*Terminalia tomentosa*), and Dhaura (*Anogeissus latifolia*).
    - **Wildlife Significance**: Critical sanctuary for Royal Bengal Tigers (including rare melanistic tigers), Asian Elephants (*Elephas maximus*), and over 230 bird species.
    - **Fire Vulnerability**: Susceptible to dry-season surface and crown fires between February and May, influenced by high leaf litter accumulation, desiccating winds, and anthropogenic activities.
    """)

    st.markdown("---")

    # Workflow Architecture
    st.markdown("### Research Processing Workflow")
    st.markdown("""
    1. **Pre-Processing & Quality Assurance**:
       - Multi-temporal Sentinel-2 MSI Surface Reflectance (Level-2A).
       - Quality Assessment (QA60) band and spectral threshold rule-based cloud/shadow masking.
       - Atmospheric Dark Object Subtraction (DOS).
       - Spatial subsetting and clipping to the official Similipal reserve boundary (`similipal_boundary.geojson`).
    2. **Multi-Spectral Biophysical Index Derivation**:
       - **NDVI** (B8, B4) — Chlorophyll absorption and photosynthetic canopy vitality.
       - **EVI** (B8, B4, B2) — Canopy architecture and aerosol-corrected vegetation structure.
       - **MSAVI** (B8, B4) — Dynamic soil-adjusted vegetation index over exposed soil.
       - **NDMI** (B8, B11) — Canopy spongy mesophyll equivalent water thickness.
       - **BRI** (B8, B11) — Burning Ratio Index for spectral disparity and burn zonation.
    3. **Thermal Infrared & Surface Heating Dynamics**:
       - Relative Land Surface Temperature (LST) extraction and alignment.
       - Calculation of relative thermal anomalies ($\Delta\text{LST}$) during and following fire events.
    4. **Coupled Fire Impact Modeling**:
       - Multi-variable linear regression validating that fire severity ($\Delta\text{BRI}$) dominates observed canopy loss ($R^2 = 0.3206, r = 0.582, p < 0.001$).
    5. **Multi-Criteria Ecological Vulnerability Score (EVS)**:
       - Min-max normalization and weighted synthesis of Vegetation Degradation (0.40), Moisture Degradation (0.30), and Thermal Stress (0.30).
       - Rigorous sensitivity testing across 5 alternative weighting regimes.
    6. **Geodesic Restoration Prioritization**:
       - Row-by-row ellipsoidal area calculation on WGS84 spheroid (`pyproj.Geod`), eliminating planar coordinate distortion.
       - Partitioning of Similipal into 4 strategic operational management tiers.
    """)

    st.markdown("---")

    # Limitations & Integrity Notice
    st.markdown("### Research Limitations & Scope")
    st.markdown("""
    - **Satellite Observation Scope**: This application is an interactive historical geospatial analysis system based on three defined observation epochs. It does not ingest live telemetry or issue real-time active fire alerts.
    - **Thermal Product Calibration**: Thermal products are preserved in relative radiance units (DN) rather than calibrated degrees Celsius, reflecting rigorous sensor preprocessing standards.
    - **Phenological Regreening**: Post-fire increases in spectral vegetation indices represent herbaceous flush, seasonal phenology, and rainfall response; long-term structural recovery of woody biomass requires multi-year observation.
    - **Decision Support Scope**: Restoration priority polygons serve as strategic prioritization guidance for departmental planning and require local ground-truthing before executing costly field works.
    """)

    st.markdown("---")

    # Academic References
    st.markdown("### Key References & Literature")
    st.markdown("""
    1. **Rouse, J. W., et al. (1974)**. *Monitoring vegetation systems in the Great Plains with ERTS*. Third Earth Resources Technology Satellite-1 Symposium, NASA SP-351, 309–317.
    2. **Huete, A., et al. (2002)**. *Overview of the radiometric and biophysical performance of the MODIS vegetation indices*. Remote Sensing of Environment, 83(1-2), 195–213.
    3. **Qi, J., et al. (1994)**. *A modified soil adjusted vegetation index*. Remote Sensing of Environment, 48(2), 119–126.
    4. **Gao, B. C. (1996)**. *NDWI—A normalized difference water index for remote sensing of vegetation liquid water from space*. Remote Sensing of Environment, 58(3), 257–266.
    5. **Key, C. H., & Benson, N. C. (2006)**. *Landscape assessment: Ground measure of severity, the Composite Burn Index; and Remote sensing of severity, the Normalized Burn Ratio*. FIREMON: Landscape Assessment, USDA Forest Service RMRS-GTR-164-CD.
    6. **Drusch, M., et al. (2012)**. *Sentinel-2: ESA's optical high-resolution mission for GMES operational services*. Remote Sensing of Environment, 120, 25–36.
    """)
