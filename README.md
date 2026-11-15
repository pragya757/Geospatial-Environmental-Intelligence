# Geospatial-Environmental-Intelligence

## Multi-Temporal Forest Fire Detection, Vegetation Change Assessment and Ecological Vulnerability Analysis Using Satellite Imagery – A Case Study of Similipal Forest, Odisha, India

---

## 🌲 Project Overview

This repository contains the complete academic research codebase and interactive geospatial dashboard for environmental intelligence monitoring in the **Similipal Biosphere Reserve, Odisha, India**. 

The system analyzes multi-temporal satellite earth observations across three observation phases:
1. **Pre-Fire Phase**: Baseline healthy forest canopy condition.
2. **During-Fire Phase**: Active wildfire progression, canopy scorch, and moisture desiccation.
3. **Post-Fire Phase**: Immediate aftermath, understory regrowth, and phenological response.

---

## 🛰️ Key Scientific Features

- **Multi-Sensor Earth Observation**: Calibrated European Space Agency **Sentinel-2 MSI** (Bands 2, 4, 8, 11) surface reflectance and **MODIS/Landsat-8** thermal infrared observations.
- **Biophysical Vegetation & Moisture Indices**:
  - **NDVI** (Chlorophyll Greenness): Mean relative drop of -6.07% during fire ($0.3515 \to 0.3230$).
  - **EVI** (Canopy Architecture): Reduced aerosol distortion using the blue band ($0.3695 \to 0.3281$).
  - **MSAVI** (Soil-Adjusted): Dynamic soil adjustment over incinerated exposed soil; 55.80% of valid pixels experienced decrease during fire.
  - **NDMI** (Canopy Moisture Content): Acute foliar moisture drop of 80.9% ($0.0899 \to 0.0172$); 66.74% of the reserve experienced moisture depletion.
- **Coupled Fire Impact Modeling**:
  - Multi-variable linear regression equation:
    $$\Delta\text{NDVI} = -0.0032 + (0.6898) \times \Delta\text{BRI} + (0.0000) \times \Delta\text{LST}$$
  - $R^2 = 0.3206$, Correlation with observed canopy loss $r = 0.582$ ($p < 0.0001$).
  - Statistically validates that **Fire Severity (BRI, $r = 0.702$)** is the primary driver of canopy loss over surface thermal anomalies ($r = -0.052$).
- **Thermal Radiative Analysis**:
  - Relative Land Surface Temperature (LST in Relative Thermal Units) mapping active radiative warming ($\Delta\text{LST}$ mean: +2,420.59 relative units).
- **Burn Severity Classification (BRI)**:
  - 5-class zonation based on Near-Infrared and Short-Wave Infrared disparity.
- **Multi-Criteria Ecological Vulnerability Scoring (EVS)**:
  - Synthesis of Vegetation Degradation (0.40), Moisture Degradation (0.30), and Relative Thermal Stress (0.30) with 5-regime sensitivity testing.
- **Geodesic Restoration Prioritization**:
  - Exact ellipsoidal area calculations on WGS84 (`pyproj.Geod`) over the 3,485.37 km² reserve:
    - **Low Priority**: 1,638.29 km² (47.00%)
    - **Moderate Priority**: 1,065.57 km² (30.57%)
    - **High Priority**: 443.31 km² (12.72%)
    - **Very High Priority**: 338.20 km² (9.71%)

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
