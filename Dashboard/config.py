"""
Configuration and constants for Similipal Forest Intelligence Dashboard.
Maintains research integrity by referencing verified project paths and academic research outputs.
"""

import os
from pathlib import Path

# Paths
DASHBOARD_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = DASHBOARD_DIR.parent
FIRE_PROJECT_DIR = PROJECT_ROOT / "Fire_Project"
BURN_SEV_DIR = FIRE_PROJECT_DIR / "Burn_Severity_Analysis"
ECO_VULN_DIR = FIRE_PROJECT_DIR / "Ecological_Vulnerability_Analysis"
MSAVI_DIR = DASHBOARD_DIR / "data" / "msavi"
CACHE_DIR = DASHBOARD_DIR / "cache"

# Ensure directories exist
MSAVI_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# Study Area Metadata
STUDY_AREA = {
    "name": "Similipal Biosphere Reserve & Tiger Reserve",
    "location": "Mayurbhanj District, Odisha, India",
    "coordinates": {"lat": 21.75, "lon": 86.25},
    "bounds": {
        "min_lat": 21.3999,
        "max_lat": 22.1004,
        "min_lon": 85.8999,
        "max_lon": 86.6000
    },
    "boundary_geojson": FIRE_PROJECT_DIR / "similipal_boundary.geojson",
    "phases": ["Pre-Fire", "During-Fire", "Post-Fire"],
    "event_context": "2021 Major Forest Fire Event (Dry Season, February–May)",
    "sensors": "Sentinel-2 MSI (10-20m) & MODIS / Landsat-8 Thermal (LST)",
}

# Verified Raster Mappings
RASTER_PATHS = {
    # Original Sentinel-2 Imagery (4 Bands: B2-Blue, B4-Red, B8-NIR, B11-SWIR)
    "S2": {
        "Pre-Fire": FIRE_PROJECT_DIR / "S2_PreFire.tif",
        "During-Fire": FIRE_PROJECT_DIR / "S2_DuringFire.tif",
        "Post-Fire": FIRE_PROJECT_DIR / "S2_PostFire.tif",
    },
    # Normalized Difference Vegetation Index
    "NDVI": {
        "Pre-Fire": FIRE_PROJECT_DIR / "NDVI_PreFire.tif",
        "During-Fire": FIRE_PROJECT_DIR / "NDVI_DuringFire.tif",
        "Post-Fire": FIRE_PROJECT_DIR / "NDVI_PostFire.tif",
        "dNDVI_During": PROJECT_ROOT / "dNDVI_During.tif",
        "dNDVI_Post": PROJECT_ROOT / "dNDVI_Post.tif",
        "Modeled_dNDVI": FIRE_PROJECT_DIR / "Modeled_dNDVI.tif",
        "Percent_dNDVI": FIRE_PROJECT_DIR / "Percent_dNDVI_During.tif",
    },
    # Enhanced Vegetation Index
    "EVI": {
        "Pre-Fire": FIRE_PROJECT_DIR / "EVI_PreFire.tif",
        "During-Fire": FIRE_PROJECT_DIR / "EVI_DuringFire.tif",
        "Post-Fire": FIRE_PROJECT_DIR / "EVI_PostFire.tif",
    },
    # Normalized Difference Moisture Index
    "NDMI": {
        "Pre-Fire": FIRE_PROJECT_DIR / "NDMI_PreFire.tif",
        "During-Fire": FIRE_PROJECT_DIR / "NDMI_DuringFire.tif",
        "Post-Fire": FIRE_PROJECT_DIR / "NDMI_PostFire.tif",
    },
    # Burning Ratio Index
    "BRI": {
        "Pre-Fire": FIRE_PROJECT_DIR / "BRI_Pre-Fire.tif",
        "During-Fire": FIRE_PROJECT_DIR / "BRI_During-Fire.tif",
        "Post-Fire": FIRE_PROJECT_DIR / "BRI_Post-Fire.tif",
        "dBRI_During": BURN_SEV_DIR / "dBRI_During.tif",
        "dBRI_Post": BURN_SEV_DIR / "dBRI_Post.tif",
        "Impact_Classification": BURN_SEV_DIR / "BRI_Impact_Classification.tif",
    },
    # Relative Land Surface Temperature
    "LST": {
        "Pre-Fire": FIRE_PROJECT_DIR / "LST_PreFire_Relative.tif",
        "During-Fire": FIRE_PROJECT_DIR / "LST_DuringFire_Relative.tif",
        "Post-Fire": FIRE_PROJECT_DIR / "LST_PostFire_Relative.tif",
        "dLST_During": PROJECT_ROOT / "dLST_During.tif",
        "dLST_Post": PROJECT_ROOT / "dLST_Post.tif",
    },
    # Ecological Vulnerability Assessment
    "EVS": {
        "EVS_Score": ECO_VULN_DIR / "Ecological_Vulnerability_Score.tif",
        "Restoration_Priority": ECO_VULN_DIR / "Restoration_Priority_Classification.tif",
        "Veg_Degradation": ECO_VULN_DIR / "Vegetation_Degradation_Score.tif",
        "Moisture_Degradation": ECO_VULN_DIR / "Moisture_Degradation_Score.tif",
        "Thermal_Stress": ECO_VULN_DIR / "Relative_Thermal_Stress_Score.tif",
    },
    # MSAVI (Exported directly from S2 bands with notebook exactness)
    "MSAVI": {
        "Pre-Fire": MSAVI_DIR / "MSAVI_PreFire.tif",
        "During-Fire": MSAVI_DIR / "MSAVI_DuringFire.tif",
        "Post-Fire": MSAVI_DIR / "MSAVI_PostFire.tif",
        "dMSAVI_During": MSAVI_DIR / "dMSAVI_During.tif",
        "dMSAVI_Post": MSAVI_DIR / "dMSAVI_Post.tif",
    }
}

# CSV Data Files
CSV_PATHS = {
    "BRI_Impact_Stats": BURN_SEV_DIR / "BRI_Impact_Area_Statistics.csv",
    "Weight_Sensitivity": ECO_VULN_DIR / "Weight_Sensitivity_Analysis.csv",
    "Project_Inventory": PROJECT_ROOT / "project_image_inventory.csv",
}

# Verified Research Statistics (directly verified from fire_analysis.ipynb outputs)
NOTEBOOK_STATS = {
    "NDVI": {
        "Pre-Fire": {"mean": 0.35148147, "valid_pixels": 60708764},
        "During-Fire": {"mean": 0.32303570, "valid_pixels": 60708768},
        "Post-Fire": {"mean": 0.36817336, "valid_pixels": 60708760},
        "dNDVI_During": {"mean": -0.02844610, "min": -0.51598, "max": 0.51433, "std": 0.04860},
        "dNDVI_Post": {"mean": 0.01669264, "min": -0.56198, "max": 0.63283, "std": 0.06530},
        "Percent_Change_During": {"mean": -6.06623, "std": 16.5596},
        "Model_Coupled": {
            "equation": "ΔNDVI = -0.0032 + (0.6898) × ΔBRI + (0.0000) × ΔLST",
            "r2": 0.3206,
            "correlation_observed_modeled": 0.582,
            "corr_ndvi_bri": 0.702,
            "corr_ndvi_lst": -0.052,
            "valid_pixels": 60517336
        }
    },
    "EVI": {
        "Pre-Fire": {"mean": 0.36945504, "min": -0.36790, "max": 2.75289, "valid_pixels": 60708764},
        "During-Fire": {"mean": 0.32814910, "min": -0.34720, "max": 1.96423, "valid_pixels": 60708768},
        "Post-Fire": {"mean": 0.38995978, "min": -0.37873, "max": 2.97418, "valid_pixels": 60708760},
        "dEVI_During": {"mean": -0.041310},
        "dEVI_Post": {"mean": 0.020502},
        "Correlation_with_NDVI": {
            "Pre-Fire": 0.9522,
            "During-Fire": 0.9798,
            "Post-Fire": 0.9839
        }
    },
    "MSAVI": {
        "Pre-Fire": {"mean": 0.24573545, "min": -0.24127853, "max": 0.70237560, "valid_pixels": 60733371},
        "During-Fire": {"mean": 0.23015447, "min": -0.24082673, "max": 0.61883690, "valid_pixels": 60733371},
        "Post-Fire": {"mean": 0.27652243, "min": -0.21876067, "max": 0.64335907, "valid_pixels": 60733371},
        "dMSAVI_During": {
            "mean": -0.01558,
            "decrease_pct": 55.80, "decrease_count": 33888306,
            "stable_pct": 21.10, "stable_count": 12817360,
            "increase_pct": 23.10, "increase_count": 14027705,
        },
        "dMSAVI_Post": {
            "mean": 0.03079,
            "decrease_pct": 21.37, "decrease_count": 12981456,
            "stable_pct": 12.65, "stable_count": 7684480,
            "increase_pct": 65.97, "increase_count": 40067435,
        }
    },
    "NDMI": {
        "Pre-Fire": {"mean": 0.08991230, "min": -0.42627, "max": 0.49655, "valid_pixels": 60733371},
        "During-Fire": {"mean": 0.01720200, "min": -0.39268, "max": 0.46286, "valid_pixels": 60733371},
        "Post-Fire": {"mean": 0.04087727, "min": -0.41108, "max": 0.41133, "valid_pixels": 60733371},
        "dNDMI_During": {
            "mean": -0.0727103,
            "decrease_pct": 66.74, "stable_pct": 32.38, "increase_pct": 0.88
        },
        "dNDMI_Post": {
            "mean": -0.0490350,
            "decrease_pct": 47.59, "stable_pct": 43.34, "increase_pct": 9.07
        }
    },
    "BRI": {
        "Pre-Fire": {"mean": 0.08989},
        "During-Fire": {"mean": 0.01722},
        "Post-Fire": {"mean": 0.04089},
        "dBRI_During": {"mean": 0.07267},
        "dBRI_Post": {"mean": 0.04901},
        "relative_thresholds": {
            "Low": 0.03651,
            "Moderate": 0.07505,
            "High": 0.12294
        },
        # Full Sentinel-2 Scene Tile Statistics (Cell 124 in Notebook, 5,615.53 km² total)
        "classes_full_scene": [
            {"Severity Class": "No Positive Change", "Pixel Count": 16896061, "Area (Hectares)": 156147.56, "Area (km2)": 1561.48, "Percentage (%)": 27.81},
            {"Severity Class": "Low Impact", "Pixel Count": 10964869, "Area (Hectares)": 101344.02, "Area (km2)": 1013.44, "Percentage (%)": 18.05},
            {"Severity Class": "Moderate Impact", "Pixel Count": 10964865, "Area (Hectares)": 101350.92, "Area (km2)": 1013.51, "Percentage (%)": 18.05},
            {"Severity Class": "High Impact", "Pixel Count": 10964866, "Area (Hectares)": 101352.34, "Area (km2)": 1013.52, "Percentage (%)": 18.05},
            {"Severity Class": "Very High Impact", "Pixel Count": 10964866, "Area (Hectares)": 101358.06, "Area (km2)": 1013.58, "Percentage (%)": 18.05},
        ],
        "total_full_scene_km2": 5615.53,
        # Verified Similipal Reserve Area Statistics (Within 3,485.369 km² EVS Boundary)
        "classes_reserve_boundary": [
            {"Severity Class": "No Positive Change", "Pixel Count": 9324234, "Area (Hectares)": 86147.0, "Area (km2)": 861.470, "Percentage (%)": 24.72},
            {"Severity Class": "Low Impact", "Pixel Count": 6559736, "Area (Hectares)": 60621.3, "Area (km2)": 606.213, "Percentage (%)": 17.39},
            {"Severity Class": "Moderate Impact", "Pixel Count": 6742542, "Area (Hectares)": 62316.8, "Area (km2)": 623.168, "Percentage (%)": 17.88},
            {"Severity Class": "High Impact", "Pixel Count": 7172923, "Area (Hectares)": 66293.3, "Area (km2)": 662.933, "Percentage (%)": 19.02},
            {"Severity Class": "Very High Impact", "Pixel Count": 7915237, "Area (Hectares)": 73158.5, "Area (km2)": 731.585, "Percentage (%)": 20.99},
        ],
        "total_reserve_boundary_km2": 3485.369
    },
    "LST": {
        "dLST_During": {"mean": 2420.59, "min": 91.5, "max": 4880.0, "std": 500.42},
        "dLST_Post": {"mean": 1699.47, "min": -1766.5, "std": 965.92},
        "unit_label": "Relative Thermal Units",
        "unit_note": "Digital Numbers / Relative Thermal Units (scaled thermal band, uncalibrated to Celsius)"
    },
    "Restoration_Priority": {
        "classes": {
            "Low": {"class_id": 1, "area_ha": 163829.329, "area_km2": 1638.293, "pct": 47.00, "color": "#27AE60"},
            "Moderate": {"class_id": 2, "area_ha": 106556.659, "area_km2": 1065.567, "pct": 30.57, "color": "#F39C12"},
            "High": {"class_id": 3, "area_ha": 44331.346, "area_km2": 443.313, "pct": 12.72, "color": "#E67E22"},
            "Very High": {"class_id": 4, "area_ha": 33819.585, "area_km2": 338.196, "pct": 9.71, "color": "#C0392B"},
        },
        "total_area_km2": 3485.369,
        "total_area_ha": 348536.919,
        "model_weights": {"vegetation": 0.40, "moisture": 0.30, "thermal": 0.30},
        "mean_vulnerability_score": 0.32731345,
        "common_valid_pixels": 37714672
    }
}

# Legend & Palette configurations
COLOR_PALETTES = {
    "NDVI": "RdYlGn",
    "EVI": "YlGn",
    "MSAVI": "YlGn",
    "NDMI": "BrBG",
    "BRI": "YlOrRd",
    "LST": "inferno",
    "EVS": "RdYlGn_r",
    "Change": "RdYlGn",
    "Priority_Hex": {
        1: "#27AE60",  # Low
        2: "#F39C12",  # Moderate
        3: "#E67E22",  # High
        4: "#C0392B",  # Very High
    },
    "Severity_Hex": {
        0: "#27AE60",  # No Positive Change
        1: "#F39C12",  # Low Impact
        2: "#E67E22",  # Moderate Impact
        3: "#C0392B",  # High Impact
        4: "#78281F",  # Very High Impact
    }
}
