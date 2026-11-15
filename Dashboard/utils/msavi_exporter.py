"""
MSAVI Exporter and Processor.
Reproducibly computes and exports MSAVI GeoTIFFs and change products
directly from Sentinel-2 surface reflectance bands following fire_analysis.ipynb (Cell 141 & 144).
"""

import os
import rasterio
import numpy as np
from pathlib import Path
from Dashboard.config import RASTER_PATHS, MSAVI_DIR

def export_msavi_if_needed():
    """
    Checks if MSAVI GeoTIFFs exist in Dashboard/data/msavi.
    If not, calculates them reproducibly using Sentinel-2 bands 2 (Red) and 3 (NIR).
    """
    msavi_pre = MSAVI_DIR / "MSAVI_PreFire.tif"
    msavi_during = MSAVI_DIR / "MSAVI_DuringFire.tif"
    msavi_post = MSAVI_DIR / "MSAVI_PostFire.tif"
    dmsavi_during = MSAVI_DIR / "dMSAVI_During.tif"
    dmsavi_post = MSAVI_DIR / "dMSAVI_Post.tif"

    all_exist = all(p.exists() for p in [msavi_pre, msavi_during, msavi_post, dmsavi_during, dmsavi_post])
    if all_exist:
        return {
            "Pre-Fire": msavi_pre,
            "During-Fire": msavi_during,
            "Post-Fire": msavi_post,
            "dMSAVI_During": dmsavi_during,
            "dMSAVI_Post": dmsavi_post,
        }

    print("[MSAVI Exporter] Computing MSAVI GeoTIFFs from Sentinel-2 rasters...")
    s2_inputs = {
        "Pre-Fire": RASTER_PATHS["S2"]["Pre-Fire"],
        "During-Fire": RASTER_PATHS["S2"]["During-Fire"],
        "Post-Fire": RASTER_PATHS["S2"]["Post-Fire"],
    }

    msavi_arrays = {}
    ref_profile = None

    for phase, path in s2_inputs.items():
        if not path.exists():
            raise FileNotFoundError(f"Missing Sentinel-2 image for {phase}: {path}")

        with rasterio.open(path) as src:
            red = src.read(2).astype(np.float32) / 10000.0
            nir = src.read(3).astype(np.float32) / 10000.0

            valid_mask = (
                (src.read_masks(2) > 0) &
                (src.read_masks(3) > 0) &
                np.isfinite(red) &
                np.isfinite(nir)
            )

            discriminant = (2.0 * nir + 1.0) ** 2 - 8.0 * (nir - red)
            valid_mask &= (discriminant >= 0) & ((nir + red) > 0)

            msavi = np.full(nir.shape, np.nan, dtype=np.float32)
            msavi[valid_mask] = (
                2.0 * nir[valid_mask] + 1.0 - np.sqrt(discriminant[valid_mask])
            ) / 2.0

            msavi_arrays[phase] = msavi
            if ref_profile is None:
                ref_profile = src.profile.copy()

    # Save MSAVI Phase Rasters
    profile = ref_profile.copy()
    profile.update(count=1, dtype="float32", nodata=-9999.0, compress="lzw")

    for phase, target_file in [
        ("Pre-Fire", msavi_pre),
        ("During-Fire", msavi_during),
        ("Post-Fire", msavi_post),
    ]:
        data = msavi_arrays[phase]
        out_data = np.where(np.isfinite(data), data, -9999.0).astype(np.float32)
        with rasterio.open(target_file, "w", **profile) as dst:
            dst.write(out_data, 1)
        print(f"[MSAVI Exporter] Exported {target_file.name}")

    # Calculate change maps (Thresholding per notebook)
    dur_change = msavi_arrays["During-Fire"] - msavi_arrays["Pre-Fire"]
    post_change = msavi_arrays["Post-Fire"] - msavi_arrays["Pre-Fire"]

    for change_arr, target_file in [(dur_change, dmsavi_during), (post_change, dmsavi_post)]:
        out_data = np.where(np.isfinite(change_arr), change_arr, -9999.0).astype(np.float32)
        with rasterio.open(target_file, "w", **profile) as dst:
            dst.write(out_data, 1)
        print(f"[MSAVI Exporter] Exported {target_file.name}")

    return {
        "Pre-Fire": msavi_pre,
        "During-Fire": msavi_during,
        "Post-Fire": msavi_post,
        "dMSAVI_During": dmsavi_during,
        "dMSAVI_Post": dmsavi_post,
    }

if __name__ == "__main__":
    export_msavi_if_needed()

