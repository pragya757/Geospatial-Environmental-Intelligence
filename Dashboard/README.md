# SIMILIPAL FOREST INTELLIGENCE DASHBOARD
### Multi-Temporal Forest Fire Detection, Vegetation Change Assessment and Ecological Vulnerability Analysis Using Satellite Imagery – A Case Study of Similipal Forest, Odisha, India.

---

## Executive Overview

This web-based geospatial dashboard functions as an interactive forest fire intelligence and ecological monitoring platform for the **Similipal Biosphere Reserve, Odisha, India**. It presents research results derived from multi-temporal Sentinel-2 MSI surface reflectance imagery, MODIS/Landsat thermal products, and multi-criteria decision modeling.

The application allows researchers, forestry officials, evaluators, and conservationists to interactively explore:
1. **Multi-Spectral Satellite Imagery** across three observation phases (Pre-Fire, During-Fire, Post-Fire).
2. **Vegetation & Moisture Dynamics** through NDVI, EVI, MSAVI, and NDMI.
3. **Thermal Radiation Anomalies** via Land Surface Temperature (LST in Relative Thermal Units).
4. **Wildfire Burn Impact Severity Zonation** based on the Burning Ratio Index (BRI).
5. **Coupled Fire Impact Modeling** demonstrating that fire severity dominates observed canopy loss.
6. **Multi-Criteria Ecological Vulnerability Scoring (EVS)** and weight sensitivity scenarios.
7. **Restoration Priority Zonation** with exact geodesic area allocations.

---

## Project Architecture

```
Similipal_Project/
│
├── fire_analysis.ipynb                        # Main academic research notebook (Unchanged)
├── project_image_inventory.csv                # Complete satellite raster file inventory (Unchanged)
│
├── Fire_Project/                              # Primary satellite rasters & research outputs (Unchanged)
│   ├── S2_PreFire.tif                         # Sentinel-2 4-band multi-spectral pre-fire scene
│   ├── S2_DuringFire.tif                      # Sentinel-2 4-band active fire scene
│   ├── S2_PostFire.tif                        # Sentinel-2 4-band post-fire response scene
│   ├── NDVI_*.tif, EVI_*.tif, NDMI_*.tif      # Derived vegetation index rasters
│   ├── BRI_*.tif                              # Burning Ratio Index rasters
│   ├── LST_*.tif                              # Relative Land Surface Temperature products
│   ├── similipal_boundary.geojson             # Official Similipal reserve vector boundary
│   │
│   ├── Burn_Severity_Analysis/                # BRI impact classification & statistics
│   │   ├── BRI_Impact_Classification.tif
│   │   ├── BRI_Impact_Area_Statistics.csv
│   │   └── dBRI_During.tif, dBRI_Post.tif
│   │
│   └── Ecological_Vulnerability_Analysis/     # Multi-criteria vulnerability modeling
│       ├── Ecological_Vulnerability_Score.tif
│       ├── Restoration_Priority_Classification.tif
│       ├── Vegetation_Degradation_Score.tif
│       ├── Moisture_Degradation_Score.tif
│       ├── Relative_Thermal_Stress_Score.tif
│       └── Weight_Sensitivity_Analysis.csv
│
└── Dashboard/                                 # Interactive Web Dashboard Application
    ├── app.py                                 # Main Streamlit application entry point
    ├── requirements.txt                       # Python dependencies
    ├── README.md                              # This documentation
    ├── config.py                              # Global configuration, verified stats & path registry
    │
    ├── components/                            # Reusable UI & geospatial components
    │   ├── header.py                          # Hero branding banner & research badges
    │   ├── sidebar.py                         # Sidebar navigation & study area parameters
    │   ├── metrics_cards.py                   # Styled metric cards & priority pills
    │   ├── maps.py                            # Folium Leaflet interactive maps (OpenStreetMap basemap)
    │   └── charts.py                          # Interactive Plotly charts
    │
    ├── modules/                               # 10 Dedicated Dashboard Sections
    │   ├── overview.py                        # 1. Executive overview & research highlights
    │   ├── satellite_viewer.py                # 2. Sentinel-2 false/true color composite viewer
    │   ├── vegetation.py                      # 3. NDVI, EVI, MSAVI, NDMI in-depth analysis
    │   ├── thermal.py                         # 4. Relative LST & thermal stress analysis
    │   ├── burn_impact.py                     # 5. BRI burn impact classification & severity
    │   ├── vulnerability.py                   # 6. EVS multi-criteria synthesis & sensitivity
    │   ├── change_detection.py                # 7. Multi-temporal change & coupled regression
    │   ├── restoration.py                     # 8. Decision support & priority zonation
    │   ├── reports.py                         # 9. CSV export, report download & GIS inventory
    │   └── about.py                           # 10. Academic context, citations & limitations
    │
    ├── utils/                                 # High-performance processing utilities
    │   ├── raster_loader.py                   # Memory-safe decimation, bounds & RGBA generation
    │   ├── stats_calculator.py                # Notebook verified stats & dynamic aggregator
    │   └── msavi_exporter.py                  # Reproducible MSAVI calculation directly from S2 bands
    │
    ├── data/
    │   └── msavi/                             # Exported reproducible MSAVI GeoTIFFs
    └── assets/
        └── style.css                          # Dark forest-green & charcoal theme stylesheet
```

---

## System Requirements & Launch Instructions

### Requirements
- **Python Version**: Python 3.10+ (Tested in `fire_project` conda environment)
- **RAM**: Minimum 8 GB RAM (16 GB recommended for handling 500 MB GeoTIFF files)

### Launching the Dashboard
Run the Streamlit application from the project root directory:
```bash
cd /Users/pragya/Documents/Similipal_Project
conda activate fire_project
streamlit run Dashboard/app.py
```

The application opens in your web browser at:
`http://localhost:8501`

---

## Scientific Findings & Validated Statistics

### 1. Burn Impact Area Statistics & Methodological Clarification
In Notebook Cell 124, `BRI_Impact_Area_Statistics.csv` was computed over the **full Sentinel-2 scene tile (5,615.53 km²)** where positive change pixels were divided into 4 equal quartiles (25%, 50%, 75% percentiles), resulting in exactly equal slices (~1,013.5 km² each).
When clipped to the official **Similipal Reserve Boundary (3,485.37 km²)** using WGS84 geodesic calculations (`pyproj.Geod`):
- **No Positive Change (Class 0)**: 861.47 km² (24.72%)
- **Low Impact (Class 1)**: 606.21 km² (17.39%)
- **Moderate Impact (Class 2)**: 623.17 km² (17.88%)
- **High Impact (Class 3)**: 662.93 km² (19.02%)
- **Very High Impact (Class 4)**: 731.59 km² (20.99%)
- **Total Classified Area**: 3,485.37 km²

### 2. MSAVI Classification vs. Index Values
- **Pre-Fire Mean**: 0.24573545
- **During-Fire Mean**: 0.23015447 (Mean difference $\Delta = -0.01558$)
- **Post-Fire Mean**: 0.27652243 (Mean difference $\Delta = +0.03079$)
- **Pixel Classification (±0.01 threshold)**:
  - During-fire: **55.80% of valid pixels classified as Decreased**, 21.10% No significant change, 23.10% Increased.
  - Post-fire: **21.37% of valid pixels classified as Decreased**, 12.65% No significant change, **65.97% Increased**.

### 3. Ecological Vulnerability Score (EVS) & Restoration Priority
Geodesic area calculations on the WGS84 ellipsoid:
- **Low Priority**: 1,638.293 km² (47.00%)
- **Moderate Priority**: 1,065.567 km² (30.57%)
- **High Priority**: 443.313 km² (12.72%)
- **Very High Priority**: 338.196 km² (9.71%)
- **Total Classified Area**: 3,485.369 km²

### 4. Thermal Analysis Labeling
All Land Surface Temperature metrics are reported in **Relative Thermal Units** (uncalibrated digital radiance values), as no in-situ radiosonde calibration was applied.
- **During-Fire Relative Heating (Mean Δ)**: +2,420.59 relative units (std: 500.42).
- **Post-Fire Relative Persistence (Mean Δ)**: +1,699.47 relative units.

### 5. BRI vs. NDMI Equivalence
Both indices compute $\frac{\text{B8} - \text{B11}}{\text{B8} + \text{B11}}$. In the research, this ratio is applied as a burning ratio index to track pre-fire to post-fire canopy disparity.

---

## Academic Attribution

- **Researcher**: Pragya Paramita Sahoo (B.Tech Computer Science & Engineering)
- **Institution**: SRM Institute of Science and Technology, Department of Computing Technologies, Kattankulathur, Tamil Nadu, India
- **Supervisor**: Dr. A. Pandiaraj, Assistant Professor
