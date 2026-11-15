"""
Pre-renders lightweight web-optimized cloud assets for deployed environments (Streamlit Community Cloud, Render, etc.).
Extracts:
1. High-fidelity JPEG composites for Sentinel-2 (NIR-Red-Blue and SWIR-NIR-Red) across all 3 phases (~250KB each).
2. Compressed NPZ arrays for all single-band rasters (~150KB each).
3. Full metadata JSON preserving original image dimensions, coordinates, CRSs, and file sizes.
Total asset package is ~6-8 MB, well within GitHub's file limits.
"""

import os
import json
import rasterio
from rasterio.enums import Resampling
import numpy as np
from PIL import Image
from pathlib import Path
from Dashboard.config import RASTER_PATHS, DASHBOARD_DIR

OUT_DIR = DASHBOARD_DIR / "data" / "cloud_assets"
OUT_DIR.mkdir(parents=True, exist_ok=True)

def generate_s2_composites():
    print("Generating Sentinel-2 Cloud Composites...")
    s2_metadata = {}
    
    for phase, path in RASTER_PATHS["S2"].items():
        if not os.path.exists(path):
            print(f"Skipping {phase}, file not found: {path}")
            continue
            
        print(f"Processing Sentinel-2 {phase}...")
        with rasterio.open(path) as src:
            bounds = [src.bounds.bottom, src.bounds.left, src.bounds.top, src.bounds.right]
            scale = max(src.width, src.height) / 750
            out_shape = (int(src.height / scale), int(src.width / scale))
            
            # Read bands (1: Blue, 2: Red, 3: NIR, 4: SWIR)
            b_blue = src.read(1, out_shape=out_shape, resampling=Resampling.bilinear).astype(np.float32)
            b_red = src.read(2, out_shape=out_shape, resampling=Resampling.bilinear).astype(np.float32)
            b_nir = src.read(3, out_shape=out_shape, resampling=Resampling.bilinear).astype(np.float32)
            b_swir = src.read(4, out_shape=out_shape, resampling=Resampling.bilinear).astype(np.float32)
            
            meta_entry = {
                "filename": os.path.basename(path),
                "width": src.width,
                "height": src.height,
                "count": src.count,
                "crs": str(src.crs),
                "bounds": bounds,
                "file_size_mb": round(os.path.getsize(path) / (1024 * 1024), 2)
            }
            s2_metadata[phase] = meta_entry
            
            def norm_band(arr):
                valid = arr[np.isfinite(arr) & (arr > 0)]
                if len(valid) == 0:
                    return np.zeros_like(arr, dtype=np.uint8)
                p2, p98 = np.percentile(valid, (2, 98))
                if p98 <= p2:
                    p98 = p2 + 1e-4
                s = np.clip((arr - p2) / (p98 - p2), 0.0, 1.0)
                s = np.nan_to_num(s, nan=0.0)
                return (s * 255).astype(np.uint8)
            
            # 1. NIR-Red-Blue composite
            rgb_nir = np.dstack([norm_band(b_nir), norm_band(b_red), norm_band(b_blue)])
            img_nir = Image.fromarray(rgb_nir)
            out_nir = OUT_DIR / f"S2_{phase}_NIR.jpg"
            img_nir.save(out_nir, quality=85)
            print(f"  -> Saved {out_nir.name} ({round(os.path.getsize(out_nir)/1024, 1)} KB)")
            
            # 2. SWIR-NIR-Red composite
            rgb_swir = np.dstack([norm_band(b_swir), norm_band(b_nir), norm_band(b_red)])
            img_swir = Image.fromarray(rgb_swir)
            out_swir = OUT_DIR / f"S2_{phase}_SWIR.jpg"
            img_swir.save(out_swir, quality=85)
            print(f"  -> Saved {out_swir.name} ({round(os.path.getsize(out_swir)/1024, 1)} KB)")

    return s2_metadata

def generate_index_rasters():
    print("\nGenerating Single-Band Index NPZ Rasters...")
    index_metadata = {}
    
    for cat, sub in RASTER_PATHS.items():
        if cat == "S2":
            continue
        for k, path in sub.items():
            if not os.path.exists(path):
                continue
                
            with rasterio.open(path) as src:
                bounds = [src.bounds.bottom, src.bounds.left, src.bounds.top, src.bounds.right]
                scale = max(src.width, src.height) / 700
                out_shape = (int(src.height / scale), int(src.width / scale))
                
                is_class = "Classification" in str(path) or "Priority" in str(path)
                resample = Resampling.nearest if is_class else Resampling.bilinear
                
                data = src.read(1, out_shape=out_shape, resampling=resample).astype(np.float32)
                nodata = src.nodata
                if nodata is not None:
                    data[data == nodata] = np.nan
                data[data <= -9990.0] = np.nan
                
                # Save compressed npz with float16
                npz_name = f"{cat}_{k}.npz"
                npz_path = OUT_DIR / npz_name
                np.savez_compressed(
                    npz_path,
                    data=data.astype(np.float16),
                    bounds=bounds
                )
                
                meta_entry = {
                    "filename": os.path.basename(path),
                    "width": src.width,
                    "height": src.height,
                    "count": src.count,
                    "crs": str(src.crs),
                    "bounds": bounds,
                    "file_size_mb": round(os.path.getsize(path) / (1024 * 1024), 2),
                    "npz_file": npz_name
                }
                index_metadata[f"{cat}_{k}"] = meta_entry
                print(f"  -> Saved {npz_name} ({round(os.path.getsize(npz_path)/1024, 1)} KB)")

    return index_metadata

def main():
    s2_meta = generate_s2_composites()
    idx_meta = generate_index_rasters()
    
    all_meta = {
        "S2": s2_meta,
        "indices": idx_meta
    }
    
    meta_path = OUT_DIR / "metadata.json"
    with open(meta_path, "w") as f:
        json.dump(all_meta, f, indent=2)
    print(f"\nMetadata saved to {meta_path.name}")
    print("Cloud asset pre-rendering complete!")

if __name__ == "__main__":
    main()
