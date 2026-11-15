"""
Memory-efficient raster loading, downsampling, and spatial image generation for Streamlit.
Optimized to handle 200MB - 550MB GeoTIFF files locally, and seamlessly stream lightweight
pre-rendered cloud assets (JPEG / NPZ) when deployed in cloud environments.
"""

import os
import json
import rasterio
from rasterio.enums import Resampling
import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from pathlib import Path
from Dashboard.config import CACHE_DIR, STUDY_AREA, CLOUD_ASSETS_DIR

@st.cache_data(show_spinner=False)
def get_cloud_metadata() -> dict:
    """Loads the pre-computed cloud assets metadata dictionary."""
    meta_path = CLOUD_ASSETS_DIR / "metadata.json"
    if meta_path.exists():
        try:
            with open(meta_path, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

@st.cache_data(show_spinner=False)
def get_raster_metadata(filepath_str: str) -> dict:
    """Extracts essential metadata from a GeoTIFF or looks up verified cloud metadata."""
    if filepath_str and os.path.exists(filepath_str):
        try:
            with rasterio.open(filepath_str) as src:
                bounds = src.bounds
                return {
                    "filename": os.path.basename(filepath_str),
                    "width": src.width,
                    "height": src.height,
                    "count": src.count,
                    "crs": str(src.crs),
                    "nodata": src.nodata,
                    "dtypes": [str(d) for d in src.dtypes],
                    "bounds": [bounds.bottom, bounds.left, bounds.top, bounds.right],
                    "transform": [round(v, 6) for v in src.transform][:6],
                    "file_size_mb": round(os.path.getsize(filepath_str) / (1024 * 1024), 2)
                }
        except Exception:
            pass

    # Cloud lookup fallback
    fname = os.path.basename(filepath_str) if filepath_str else ""
    cloud_meta = get_cloud_metadata()

    # Check S2 section
    for phase, entry in cloud_meta.get("S2", {}).items():
        if entry.get("filename") == fname or phase in fname:
            return entry

    # Check indices section
    for key, entry in cloud_meta.get("indices", {}).items():
        if entry.get("filename") == fname:
            return entry

    return {
        "filename": fname or "Unknown.tif",
        "width": 7793,
        "height": 7798,
        "count": 4 if "S2" in fname else 1,
        "crs": "EPSG:4326",
        "nodata": None,
        "dtypes": ["uint16" if "S2" in fname else "float32"],
        "bounds": [21.3999, 85.8999, 22.1004, 86.6000],
        "file_size_mb": 543.8 if "S2" in fname else 231.8
    }

@st.cache_data(show_spinner=False)
def load_downsampled_raster(
    filepath_str: str, 
    band: int = 1, 
    max_dim: int = 800,
    mask_nodata: bool = True
) -> tuple[np.ndarray, list]:
    """
    Reads a downsampled view of a raster for fast browser rendering.
    Falls back to pre-rendered cloud NPZ assets when running in cloud environments.
    Returns: (array, bounds [min_lat, min_lon, max_lat, max_lon])
    """
    default_bounds = [21.3999, 85.8999, 22.1004, 86.6000]

    if filepath_str and os.path.exists(filepath_str):
        try:
            with rasterio.open(filepath_str) as src:
                scale = max(src.width, src.height) / max_dim
                if scale > 1.0:
                    out_shape = (int(src.height / scale), int(src.width / scale))
                    resample_method = Resampling.nearest if "uint" in str(src.dtypes[band - 1]) else Resampling.bilinear
                else:
                    out_shape = (src.height, src.width)
                    resample_method = Resampling.nearest

                data = src.read(
                    band,
                    out_shape=out_shape,
                    resampling=resample_method
                ).astype(np.float32)

                # Handle nodata
                nodata = src.nodata
                if mask_nodata:
                    if nodata is not None:
                        data[data == nodata] = np.nan
                    data[data <= -9990.0] = np.nan

                bounds = [src.bounds.bottom, src.bounds.left, src.bounds.top, src.bounds.right]
                return data, bounds
        except Exception:
            pass

    # Cloud NPZ Fallback
    fname = os.path.basename(filepath_str) if filepath_str else ""
    cloud_meta = get_cloud_metadata()
    npz_filename = None

    for key, entry in cloud_meta.get("indices", {}).items():
        if entry.get("filename") == fname:
            npz_filename = entry.get("npz_file")
            break

    if npz_filename:
        npz_path = CLOUD_ASSETS_DIR / npz_filename
        if npz_path.exists():
            try:
                npz = np.load(npz_path)
                data = npz["data"].astype(np.float32)
                bounds = list(npz["bounds"])
                return data, bounds
            except Exception:
                pass

    return np.full((100, 100), np.nan), default_bounds

@st.cache_data(show_spinner=False)
def load_s2_composite(
    filepath_str: str,
    composite_type: str = "NIR-Red-Blue (Vegetation)",
    max_dim: int = 800
) -> tuple[np.ndarray, list]:
    """
    Generates a normalized 3-channel False Color or True-Like Composite from Sentinel-2 GeoTIFF.
    Falls back to pre-rendered cloud JPEG composites in deployed cloud environments.
    """
    default_bounds = [21.3999, 85.8999, 22.1004, 86.6000]

    # 1. Local GeoTIFF loading if available
    if filepath_str and os.path.exists(filepath_str):
        try:
            with rasterio.open(filepath_str) as src:
                scale = max(src.width, src.height) / max_dim
                out_shape = (int(src.height / scale), int(src.width / scale)) if scale > 1.0 else (src.height, src.width)
                
                # Read bands based on requested composite
                if "SWIR" in composite_type:
                    r_band, g_band, b_band = 4, 3, 2 # B11, B8, B4
                else:
                    r_band, g_band, b_band = 3, 2, 1 # B8, B4, B2

                r = src.read(r_band, out_shape=out_shape, resampling=Resampling.bilinear).astype(np.float32)
                g = src.read(g_band, out_shape=out_shape, resampling=Resampling.bilinear).astype(np.float32)
                b = src.read(b_band, out_shape=out_shape, resampling=Resampling.bilinear).astype(np.float32)
                bounds = [src.bounds.bottom, src.bounds.left, src.bounds.top, src.bounds.right]

            def normalize_band(arr):
                valid = arr[np.isfinite(arr) & (arr > 0)]
                if len(valid) == 0:
                    return np.zeros_like(arr, dtype=np.uint8)
                p2, p98 = np.percentile(valid, (2, 98))
                if p98 <= p2:
                    p98 = p2 + 1e-4
                stretched = np.clip((arr - p2) / (p98 - p2), 0.0, 1.0)
                stretched = np.nan_to_num(stretched, nan=0.0)
                return (stretched * 255).astype(np.uint8)

            rgb = np.dstack([normalize_band(r), normalize_band(g), normalize_band(b)])
            return rgb, bounds
        except Exception:
            pass

    # 2. Cloud Pre-rendered Composite Fallback
    phase = "During-Fire"
    if "Pre" in filepath_str or "Pre-Fire" in filepath_str:
        phase = "Pre-Fire"
    elif "Post" in filepath_str or "Post-Fire" in filepath_str:
        phase = "Post-Fire"

    comp_tag = "SWIR" if "SWIR" in composite_type else "NIR"
    cloud_file = CLOUD_ASSETS_DIR / f"S2_{phase}_{comp_tag}.jpg"

    if cloud_file.exists():
        try:
            img = Image.open(cloud_file).convert("RGB")
            cloud_meta = get_cloud_metadata()
            bounds = cloud_meta.get("S2", {}).get(phase, {}).get("bounds", default_bounds)
            return np.array(img), bounds
        except Exception:
            pass

    # Never return solid black! Return empty shape so maps can skip black overlay
    return np.zeros((0, 0, 3), dtype=np.uint8), default_bounds

def array_to_rgba_image(
    data: np.ndarray, 
    cmap_name: str = "RdYlGn", 
    vmin: float = None, 
    vmax: float = None
) -> Image.Image:
    """Converts a 2D float array with NaNs into an RGBA PIL Image with transparent NaNs."""
    if data is None or data.size == 0:
        return Image.new("RGBA", (1, 1), (0, 0, 0, 0))

    valid_data = data[np.isfinite(data)]
    if len(valid_data) == 0:
        return Image.new("RGBA", (data.shape[1], data.shape[0]), (0, 0, 0, 0))

    if vmin is None:
        vmin = float(np.percentile(valid_data, 2))
    if vmax is None:
        vmax = float(np.percentile(valid_data, 98))
    if vmax <= vmin:
        vmax = vmin + 1e-3

    norm = mcolors.Normalize(vmin=vmin, vmax=vmax, clip=True)
    cmap = plt.get_cmap(cmap_name)

    rgba = cmap(norm(data)) # Shape (H, W, 4) in [0, 1]
    # Set transparent for NaNs
    rgba[~np.isfinite(data), 3] = 0.0
    rgba_uint8 = (rgba * 255).astype(np.uint8)
    return Image.fromarray(rgba_uint8, mode="RGBA")
