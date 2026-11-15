"""
Interactive geospatial map visualizers using Folium, Streamlit-Folium, and Plotly.
Provides interactive zooming, layer toggling, boundary overlay, and color scale legends.
Uses standard OpenStreetMap tiles with attribution to ensure no API key watermarks appear.
"""

import os
import json
import io
import base64
import folium
from folium import plugins
from streamlit_folium import st_folium
import streamlit as st
import numpy as np
import plotly.graph_objects as go
from PIL import Image

from Dashboard.config import STUDY_AREA, COLOR_PALETTES
from Dashboard.utils.raster_loader import (
    load_downsampled_raster,
    load_s2_composite,
    array_to_rgba_image
)

# Standard OpenStreetMap tile URL and official attribution
OSM_TILE_URL = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
OSM_ATTRIBUTION = '&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank">OpenStreetMap</a> contributors'

def get_study_boundary_geojson():
    """Loads and caches the Similipal study boundary GeoJSON."""
    geojson_path = str(STUDY_AREA["boundary_geojson"])
    if os.path.exists(geojson_path):
        with open(geojson_path) as f:
            return json.load(f)
    return None

def create_folium_raster_map(
    raster_path: str,
    title: str = "Raster Overlay",
    cmap_name: str = "RdYlGn",
    vmin: float = None,
    vmax: float = None,
    opacity: float = 0.85,
    overlay_boundary: bool = True
) -> folium.Map:
    """
    Creates an interactive Folium map with a transparent raster overlay
    using standard OpenStreetMap tiles (no API key required).
    """
    center_lat = STUDY_AREA["coordinates"]["lat"]
    center_lon = STUDY_AREA["coordinates"]["lon"]
    
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=9,
        tiles=OSM_TILE_URL,
        attr=OSM_ATTRIBUTION,
        control_scale=True
    )

    # Load downsampled raster for quick rendering
    data, bounds = load_downsampled_raster(raster_path, max_dim=700)
    
    # Convert array to RGBA PNG image only if valid data exists
    if data is not None and np.isfinite(data).any():
        rgba_img = array_to_rgba_image(data, cmap_name=cmap_name, vmin=vmin, vmax=vmax)
        buffered = io.BytesIO()
        rgba_img.save(buffered, format="PNG")
        img_b64 = base64.b64encode(buffered.getvalue()).decode()
        img_url = f"data:image/png;base64,{img_b64}"

        # Bounding box for Folium: [[south, west], [north, east]]
        folium_bounds = [[bounds[0], bounds[1]], [bounds[2], bounds[3]]]

        # Add image overlay
        folium.raster_layers.ImageOverlay(
            image=img_url,
            bounds=folium_bounds,
            opacity=opacity,
            name=title,
            interactive=True,
            cross_origin=False
        ).add_to(m)

    # Add Study Area Boundary if requested
    if overlay_boundary:
        boundary_data = get_study_boundary_geojson()
        if boundary_data:
            folium.GeoJson(
                boundary_data,
                name="Similipal Boundary",
                style_function=lambda x: {
                    "color": "#D35400",
                    "weight": 2.5,
                    "fillColor": "transparent",
                    "dashArray": "5, 5"
                }
            ).add_to(m)

    folium.LayerControl(position="topright").add_to(m)
    return m

def create_folium_rgb_map(
    s2_path: str,
    composite_name: str = "NIR-Red-Blue (Vegetation)",
    opacity: float = 0.9,
    overlay_boundary: bool = True
) -> folium.Map:
    """
    Creates an interactive Folium map with a Sentinel-2 False/True Color Composite overlay
    using standard OpenStreetMap tiles (no API key required).
    """
    center_lat = STUDY_AREA["coordinates"]["lat"]
    center_lon = STUDY_AREA["coordinates"]["lon"]

    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=9,
        tiles=OSM_TILE_URL,
        attr=OSM_ATTRIBUTION,
        control_scale=True
    )

    rgb, bounds = load_s2_composite(s2_path, composite_type=composite_name, max_dim=750)
    if rgb is not None and rgb.shape[0] > 10 and rgb.shape[1] > 10:
        img = Image.fromarray(rgb)
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_b64 = base64.b64encode(buffered.getvalue()).decode()
        img_url = f"data:image/png;base64,{img_b64}"

        folium_bounds = [[bounds[0], bounds[1]], [bounds[2], bounds[3]]]

        folium.raster_layers.ImageOverlay(
            image=img_url,
            bounds=folium_bounds,
            opacity=opacity,
            name=f"Sentinel-2: {composite_name}",
            interactive=True
        ).add_to(m)

    if overlay_boundary:
        boundary_data = get_study_boundary_geojson()
        if boundary_data:
            folium.GeoJson(
                boundary_data,
                name="Similipal Boundary",
                style_function=lambda x: {
                    "color": "#27AE60",
                    "weight": 2.5,
                    "fillColor": "transparent"
                }
            ).add_to(m)

    folium.LayerControl(position="topright").add_to(m)
    return m

def render_plotly_spatial_heatmap(
    data: np.ndarray,
    bounds: list,
    title: str = "Spatial Distribution",
    colorscale: str = "Viridis",
    zmin: float = None,
    zmax: float = None,
    height: int = 500
):
    """Renders a fast interactive Plotly Heatmap with coordinate axes and hovering."""
    min_lat, min_lon, max_lat, max_lon = bounds
    ny, nx = data.shape
    lons = np.linspace(min_lon, max_lon, nx)
    lats = np.linspace(max_lat, min_lat, ny)

    valid = data[np.isfinite(data)]
    if zmin is None and len(valid) > 0:
        zmin = float(np.percentile(valid, 2))
    if zmax is None and len(valid) > 0:
        zmax = float(np.percentile(valid, 98))

    fig = go.Figure(data=go.Heatmap(
        z=data,
        x=lons,
        y=lats,
        colorscale=colorscale,
        zmin=zmin,
        zmax=zmax,
        colorbar=dict(title=dict(text="", font=dict(color="#FFFFFF")), tickfont=dict(color="#FFFFFF")),
        hovertemplate="Lon: %{x:.4f}°E<br>Lat: %{y:.4f}°N<br>Value: %{z:.4f}<extra></extra>"
    ))

    fig.update_layout(
        title=dict(text=title, font=dict(color="#FFFFFF", size=13)),
        paper_bgcolor="#121614",
        plot_bgcolor="#121614",
        height=height,
        margin=dict(l=35, r=35, t=35, b=35),
        xaxis=dict(title="Longitude (°E)", color="#8CA094", gridcolor="#23362B", zeroline=False),
        yaxis=dict(title="Latitude (°N)", color="#8CA094", gridcolor="#23362B", zeroline=False, scaleanchor="x", scaleratio=1),
    )
    return fig
