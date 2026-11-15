"""
Statistics and data aggregation utilities for Similipal Forest Intelligence.
Combines exact notebook verified metrics with dynamic on-demand calculation.
"""

import numpy as np
import pandas as pd
import streamlit as st
from Dashboard.config import NOTEBOOK_STATS

def get_verified_stats(index_name: str) -> dict:
    """Returns the author's verified research statistics for an index."""
    return NOTEBOOK_STATS.get(index_name, {})

@st.cache_data(show_spinner=False)
def calculate_array_stats(arr: np.ndarray, index_name: str = "Metric") -> dict:
    """Calculates summary statistics on a valid pixel array."""
    valid = arr[np.isfinite(arr)]
    if len(valid) == 0:
        return {
            "name": index_name,
            "count": 0,
            "mean": 0.0,
            "std": 0.0,
            "min": 0.0,
            "max": 0.0,
            "p25": 0.0,
            "p50": 0.0,
            "p75": 0.0
        }
    return {
        "name": index_name,
        "count": int(len(valid)),
        "mean": float(np.mean(valid)),
        "std": float(np.std(valid)),
        "min": float(np.min(valid)),
        "max": float(np.max(valid)),
        "p25": float(np.percentile(valid, 25)),
        "p50": float(np.median(valid)),
        "p75": float(np.percentile(valid, 75))
    }

def get_indices_comparison_df() -> pd.DataFrame:
    """Returns a consolidated summary DataFrame across all 4 vegetation/moisture indices and 3 phases."""
    data = [
        {
            "Index": "NDVI (Chlorophyll Greenness)",
            "Pre-Fire Mean": NOTEBOOK_STATS["NDVI"]["Pre-Fire"]["mean"],
            "During-Fire Mean": NOTEBOOK_STATS["NDVI"]["During-Fire"]["mean"],
            "Post-Fire Mean": NOTEBOOK_STATS["NDVI"]["Post-Fire"]["mean"],
            "During-Fire Difference (Δ)": NOTEBOOK_STATS["NDVI"]["dNDVI_During"]["mean"],
            "Post-Fire Difference (Δ)": NOTEBOOK_STATS["NDVI"]["dNDVI_Post"]["mean"],
            "Primary Sensitivity": "Chlorophyll absorption, general greenness"
        },
        {
            "Index": "EVI (Canopy Structure)",
            "Pre-Fire Mean": NOTEBOOK_STATS["EVI"]["Pre-Fire"]["mean"],
            "During-Fire Mean": NOTEBOOK_STATS["EVI"]["During-Fire"]["mean"],
            "Post-Fire Mean": NOTEBOOK_STATS["EVI"]["Post-Fire"]["mean"],
            "During-Fire Difference (Δ)": NOTEBOOK_STATS["EVI"]["dEVI_During"]["mean"],
            "Post-Fire Difference (Δ)": NOTEBOOK_STATS["EVI"]["dEVI_Post"]["mean"],
            "Primary Sensitivity": "Canopy architecture, atmospheric haze resistance"
        },
        {
            "Index": "MSAVI (Soil-Adjusted Index)",
            "Pre-Fire Mean": NOTEBOOK_STATS["MSAVI"]["Pre-Fire"]["mean"],
            "During-Fire Mean": NOTEBOOK_STATS["MSAVI"]["During-Fire"]["mean"],
            "Post-Fire Mean": NOTEBOOK_STATS["MSAVI"]["Post-Fire"]["mean"],
            "During-Fire Difference (Δ)": NOTEBOOK_STATS["MSAVI"]["dMSAVI_During"]["mean"],
            "Post-Fire Difference (Δ)": NOTEBOOK_STATS["MSAVI"]["dMSAVI_Post"]["mean"],
            "Primary Sensitivity": "Canopy background adjustment over exposed soil"
        },
        {
            "Index": "NDMI (Moisture Content)",
            "Pre-Fire Mean": NOTEBOOK_STATS["NDMI"]["Pre-Fire"]["mean"],
            "During-Fire Mean": NOTEBOOK_STATS["NDMI"]["During-Fire"]["mean"],
            "Post-Fire Mean": NOTEBOOK_STATS["NDMI"]["Post-Fire"]["mean"],
            "During-Fire Difference (Δ)": NOTEBOOK_STATS["NDMI"]["dNDMI_During"]["mean"],
            "Post-Fire Difference (Δ)": NOTEBOOK_STATS["NDMI"]["dNDMI_Post"]["mean"],
            "Primary Sensitivity": "Liquid equivalent water thickness in canopy foliage"
        },
        {
            "Index": "BRI (Burning Ratio Index)*",
            "Pre-Fire Mean": NOTEBOOK_STATS["BRI"]["Pre-Fire"]["mean"],
            "During-Fire Mean": NOTEBOOK_STATS["BRI"]["During-Fire"]["mean"],
            "Post-Fire Mean": NOTEBOOK_STATS["BRI"]["Post-Fire"]["mean"],
            "During-Fire Difference (Δ)": NOTEBOOK_STATS["BRI"]["dBRI_During"]["mean"],
            "Post-Fire Difference (Δ)": NOTEBOOK_STATS["BRI"]["dBRI_Post"]["mean"],
            "Primary Sensitivity": "Spectral disparity index (NIR-SWIR)/(NIR+SWIR)"
        }
    ]
    return pd.DataFrame(data)

def get_restoration_priority_df() -> pd.DataFrame:
    """Returns the verified geodesic area table for post-fire restoration priority classes."""
    classes = NOTEBOOK_STATS["Restoration_Priority"]["classes"]
    records = []
    for label, info in classes.items():
        records.append({
            "Priority Class": label,
            "Class ID": info["class_id"],
            "Area (Hectares)": info["area_ha"],
            "Area (km²)": info["area_km2"],
            "Percentage (%)": info["pct"],
            "Color": info["color"],
        })
    return pd.DataFrame(records)

def get_burn_severity_df(scope: str = "reserve_boundary") -> pd.DataFrame:
    """
    Returns the burn impact classification area statistics.
    scope: 'reserve_boundary' (within 3,485.37 km² Similipal reserve) or 'full_scene' (5,615.53 km² full tile).
    """
    if scope == "full_scene":
        records = NOTEBOOK_STATS["BRI"]["classes_full_scene"]
    else:
        records = NOTEBOOK_STATS["BRI"]["classes_reserve_boundary"]
    return pd.DataFrame(records)
