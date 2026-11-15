"""
Custom styled metric cards and badges for Similipal Forest Intelligence.
"""

import streamlit as st

def render_metric_card(
    title: str,
    value: str,
    subtitle: str = "",
    delta: str = None,
    delta_type: str = "normal" # "normal" (pos=green), "inverse" (pos=red), "neutral"
):
    """Renders a styled metric card."""
    delta_html = ""
    if delta:
        if delta_type == "inverse":
            color_class = "delta-neg" if not delta.startswith("-") else "delta-pos"
        elif delta_type == "neutral":
            color_class = "metric-sub"
        else:
            color_class = "delta-pos" if not delta.startswith("-") else "delta-neg"
        delta_html = f'<div class="{color_class}" style="font-size: 0.85rem; margin-top: 4px;">{delta}</div>'

    html = f"""
    <div class="metric-card">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
        <div class="metric-sub">{subtitle}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_priority_card(
    title: str,
    area_km2: float,
    area_ha: float,
    percentage: float,
    color: str,
    description: str = ""
):
    """Renders an ecological restoration priority card."""
    html = f"""
    <div style="background-color: #141C18; border: 1px solid #23362B; border-top: 4px solid {color}; border-radius: 8px; padding: 16px; margin-bottom: 12px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <span style="font-weight: 700; font-size: 1.1rem; color: #FFFFFF;">{title}</span>
            <span style="background: {color}22; color: {color}; border: 1px solid {color}55; padding: 2px 8px; border-radius: 12px; font-weight: 700; font-size: 0.8rem;">
                {percentage:.1f}%
            </span>
        </div>
        <div style="font-size: 1.6rem; font-weight: 800; color: #FFFFFF; margin-bottom: 4px;">
            {area_km2:,.1f} <span style="font-size: 0.9rem; font-weight: 500; color: #9EB0A5;">km²</span>
        </div>
        <div style="font-size: 0.85rem; color: #8CA094; margin-bottom: 6px;">
            {area_ha:,.1f} Hectares
        </div>
        <div style="font-size: 0.8rem; color: #CFDFD6; border-top: 1px solid #23362B; padding-top: 8px;">
            {description}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

