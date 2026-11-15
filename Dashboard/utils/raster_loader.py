"""
Memory-efficient raster loading, downsampling, and spatial image generation for Streamlit.
Optimized to handle 200MB - 550MB GeoTIFF files without crashing or lag.
"""

import os
import rasterio
from rasterio.enums import Resampling
import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from pathlib import Path
from Dashboard.config import CACHE_DIR, STUDY_AREA

@st.cache_data(show_spinner=False)
def get_raster_metadata(filepath_str: str) -> dict:
    """Extracts essential metadata from a GeoTIFF without reading pixel data."""
    if not filepath_str or not os.path.exists(filepath_str):
        return {"error": "File not found"}
    
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
            "bounds": [bounds.bottom, bounds.left, bounds.top, bounds.right], # min_lat, min_lon, max_lat, max_lon
            "transform": [round(v, 6) for v in src.transform][:6],
            "file_size_mb": round(os.path.getsize(filepath_str) / (1024 * 1024), 2)
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
    Returns: (array, bounds [min_lat, min_lon, max_lat, max_lon])
    """
    if not os.path.exists(filepath_str):
        return np.full((100, 100), np.nan), [21.4, 85.9, 22.1, 86.6]
    
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

@st.cache_data(show_spinner=False)
def load_s2_composite(
    filepath_str: str,
    composite_type: str = "NIR-Red-Blue (Vegetation)",
    max_dim: int = 800
) -> tuple[np.ndarray, list]:
    """
    Generates a normalized 3-channel False Color or True-Like Composite from Sentinel-2 GeoTIFF.
    Bands:
      Band 1: B2 (Blue)
      Band 2: B4 (Red)
      Band 3: B8 (NIR)
      Band 4: B11 (SWIR)
    """
    if not os.path.exists(filepath_str):
        return np.zeros((100, 100, 3), dtype=np.uint8), [21.4, 85.9, 22.1, 86.6]

    with rasterio.open(filepath_str) as src:
        scale = max(src.width, src.height) / max_dim
        out_shape = (int(src.height / scale), int(src.width / scale)) if scale > 1.0 else (src.height, src.width)
        
        # Read bands based on requested composite
        if composite_type == "SWIR-NIR-Red (Burn & Moisture)":
            r_band, g_band, b_band = 4, 3, 2 # B11, B8, B4
        elif composite_type == "True-Color Approximation (Red-GreenProxy-Blue)":
            # Sentinel-2 in this project has B2, B4, B8, B11. We approximate Green from (Red+NIR)/4 or similar
            r_band, g_band, b_band = 2, 3, 1
        else:
            # Default: Standard False Color NIR-Red-Blue (B8, B4, B2) used in notebook Cell 6
            r_band, g_band, b_band = 3, 2, 1

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

def array_to_rgba_image(
    data: np.ndarray, 
    cmap_name: str = "RdYlGn", 
    vmin: float = None, 
    vmax: float = None
) -> Image.Image:
    """Converts a 2D float array with NaNs into an RGBA PIL Image with transparent NaNs."""
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

