# Geospatial-Environmental-Intelligence

## Multi-Temporal Forest Fire Detection, Vegetation Change Assessment and Ecological Vulnerability Analysis Using Satellite Imagery – A Case Study of Similipal Forest, Odisha, India

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://geospatial-environmental-intelligence-kp2wpv6bf7ofpmjrofkrs6.streamlit.app/)

---

## 🌲 Project Overview

This repository contains the complete academic research codebase and interactive geospatial dashboard for environmental intelligence monitoring in the **Similipal Biosphere Reserve, Odisha, India**. 

The system analyzes multi-temporal satellite earth observations across three defined observation phases:
1. **Pre-Fire Phase**: Baseline healthy forest canopy condition.
2. **During-Fire Phase**: Active wildfire progression, canopy scorch, and moisture desiccation.
3. **Post-Fire Phase**: Immediate aftermath, seasonal understory flush, and phenological response.

### 🎯 Core Research Objectives
1. **Multi-Temporal Forest Fire Detection & Vegetation Change Assessment**: Quantitative monitoring of chlorophyll greenness (NDVI), canopy architecture (EVI), and foliar water thickness (NDMI) across 3,485.37 km² of Similipal reserve.
2. **Spatial Ecological Vulnerability & Restoration Priority Assessment**: Synthesis of normalized vegetation degradation, moisture loss, and relative thermal stress into a model-derived Ecological Vulnerability Score (EVS) with geodesic restoration priority zonation.
3. **Soil-Adjusted Vegetation Condition Assessment Using MSAVI**: Decoupling exposed mineral soil background effects caused by understory fire consumption using the self-adaptive Modified Soil-Adjusted Vegetation Index (MSAVI).

---

## 🛰️ Key Scientific Features

- **Multi-Sensor Earth Observation**:
  - Calibrated **Sentinel-2 MSI** surface reflectance (File Band 1: B2-Blue, File Band 2: B4-Red, File Band 3: B8-NIR, File Band 4: B11-SWIR; scaled by 10,000).
  - Thermal infrared observations clipped to the reserve boundary.
- **Biophysical Vegetation & Moisture Indices**:
  - **NDVI** (Chlorophyll Greenness): Mean relative drop of -6.07% during fire ($0.3515 \to 0.3230$).
  - **EVI** (Canopy Architecture): Aerosol-corrected using the blue band ($0.3695 \to 0.3281$).
  - **MSAVI** (Soil-Adjusted): Dynamic self-adjusting soil compensation; 55.80% of valid pixels classified as Decreased during fire ($0.2457 \to 0.2302$).
  - **NDMI** (Canopy Moisture Content): Acute foliar moisture drop of 80.9% ($0.0899 \to 0.0172$); 66.74% of valid pixels exhibited moisture depletion.
- **Spectral Equivalence of BRI & NDMI**:
  - Both calculate $\frac{B8 - B11}{B8 + B11}$. NDMI tracks foliar canopy moisture, while BRI serves as a relative spectral burn disparity metric.
  - The composite EVS does **not** double-count them, integrating EVI, NDMI, and LST.
- **Relative Land Surface Temperature (LST)**:
  - Recorded in uncalibrated **Relative Thermal Units** (DN), mapping spatial thermal variation and relative anomalies ($\Delta\text{LST}$ mean: +2,420.59 relative units).
- **Coupled Fire Impact Modeling**:
  - Regression equation: $\Delta\text{NDVI} = -0.0032 + (0.6898) \times \Delta\text{BRI} + (0.0000) \times \Delta\text{LST}$ ($R^2 = 0.3206, r = 0.582, p < 0.0001$).
  - Validates that Fire Severity (BRI, $r = 0.702$) is the primary driver of canopy loss over surface thermal anomalies ($r = -0.052$).
- **Relative Burn Impact Classification**:
  - 5-class zonation based on empirical quantile thresholds (25th, 50th, 75th percentiles of positive $\Delta\text{BRI}$).
- **Model-Derived Ecological Vulnerability Scoring (EVS)**:
  - Weighted synthesis of Vegetation Degradation (0.40, from EVI), Moisture Degradation (0.30, from NDMI), and Relative Thermal Stress (0.30, from LST).
- **Geodesic Restoration Prioritization**:
  - Ellipsoidal area calculations on WGS84 (`pyproj.Geod`) over the 3,485.37 km² reserve:
    - **Low Priority**: 1,638.293 km² (47.00%)
    - **Moderate Priority**: 1,065.567 km² (30.57%)
    - **High Priority**: 443.313 km² (12.72%)
    - **Very High Priority**: 338.196 km² (9.71%)
    - **Total Classified Area**: 3,485.369 km²

---

## 💻 Interactive Streamlit Dashboard

The repository includes a web-based dashboard with 10 analytical modules:
1. **Overview & Research Summary**: Executive metrics, phase comparison cards, interactive Leaflet map.
2. **Satellite Image Comparison**: Sentinel-2 false-color composites (NIR-Red-Blue and SWIR-NIR-Red).
3. **Vegetation Index Analysis**: Dedicated comparative tabs for NDVI, EVI, MSAVI, and NDMI.
4. **Thermal Analysis**: Relative LST anomaly maps and thermal stress interpretation.
5. **Burn Impact Analysis**: BRI severity classification and area statistics.
6. **Ecological Vulnerability (EVS)**: Composite vulnerability maps and sensitivity modeling.
7. **Temporal Change Detection**: Pixel-level difference maps and the coupled regression model.
8. **Restoration Priorities**: Strategic decision support matrix for forest conservation managers.
9. **Reports & Data Export**: CSV statistical downloads, GIS raster inventory, and downloadable research report.
10. **About the Research**: Academic context, study area geography, methodology, and citations.

---

## 🚀 Installation & Execution

### 1. Clone the Repository
```bash
git clone https://github.com/pragya757/Geospatial-Environmental-Intelligence.git
cd Geospatial-Environmental-Intelligence
```

### 2. Install Dependencies
```bash
pip install -r Dashboard/requirements.txt
```

### 3. Launch the Application
```bash
streamlit run Dashboard/app.py
```
Open **`http://localhost:8501`** in your browser.

---

## 📁 Repository Structure

```
├── fire_analysis.ipynb                        # Main Jupyter research analysis notebook
├── project_image_inventory.csv                # Complete satellite raster file inventory
├── similipal_boundary.geojson                 # Official Similipal reserve vector boundary
├── .gitignore                                 # Ignores large GeoTIFF files (>100MB)
├── README.md                                  # Repository documentation
│
├── Dashboard/                                 # Streamlit Web Application
│   ├── app.py                                 # Main application entry point
│   ├── requirements.txt                       # Python dependencies
│   ├── config.py                              # Central configuration & statistics
│   ├── assets/                                # Dark forest-green stylesheet
│   ├── components/                            # UI, Map, and Chart components
│   ├── modules/                               # 10 Dedicated analytical dashboard modules
│   └── utils/                                 # Raster loader, stats calculator, MSAVI exporter
```

---

## 🎓 Academic Attribution

- **Researcher**: Pragya Paramita Sahoo (B.Tech Computer Science & Engineering)
- **Institution**: Department of Computing Technologies, College of Engineering and Technology, SRM Institute of Science and Technology, Kattankulathur, Tamil Nadu, India
- **Supervisor**: Dr. A. Pandiaraj, Assistant Professor
- **Course**: 21CSP302L - Project Work
