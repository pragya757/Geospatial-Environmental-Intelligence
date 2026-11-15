"""
Interactive Plotly charts for Similipal Forest Intelligence.
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

CHART_THEME = {
    "paper_bgcolor": "#121614",
    "plot_bgcolor": "#141C18",
    "font": {"color": "#E0E6E2", "family": "-apple-system, sans-serif"},
    "gridcolor": "#23362B"
}

def create_phase_comparison_bar(
    indices_df: pd.DataFrame,
    title: str = "Cross-Phase Vegetation Index Comparison"
):
    """Bar chart comparing Pre-Fire, During-Fire, and Post-Fire mean values across indices."""
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=indices_df["Index"],
        y=indices_df["Pre-Fire Mean"],
        name="Pre-Fire (Baseline)",
        marker_color="#27AE60"
    ))
    fig.add_trace(go.Bar(
        x=indices_df["Index"],
        y=indices_df["During-Fire Mean"],
        name="During-Fire (Impact)",
        marker_color="#C0392B"
    ))
    fig.add_trace(go.Bar(
        x=indices_df["Index"],
        y=indices_df["Post-Fire Mean"],
        name="Post-Fire (Response)",
        marker_color="#F39C12"
    ))

    fig.update_layout(
        title=dict(text=title, font=dict(size=14, color="#FFFFFF")),
        paper_bgcolor=CHART_THEME["paper_bgcolor"],
        plot_bgcolor=CHART_THEME["plot_bgcolor"],
        font=CHART_THEME["font"],
        barmode="group",
        height=380,
        margin=dict(l=40, r=40, t=50, b=40),
        xaxis=dict(gridcolor=CHART_THEME["gridcolor"]),
        yaxis=dict(title="Index Mean Value", gridcolor=CHART_THEME["gridcolor"]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def create_change_distribution_bar(
    decrease_pct: float,
    stable_pct: float,
    increase_pct: float,
    title: str = "Temporal Change Distribution (%)"
):
    """Horizontal bar chart of category shifts (Decrease, Stable, Increase)."""
    categories = ["Decrease (Degradation)", "No Significant Change", "Increase"]
    percentages = [decrease_pct, stable_pct, increase_pct]
    colors = ["#C0392B", "#7F8C8D", "#27AE60"]

    fig = go.Figure(go.Bar(
        x=percentages,
        y=categories,
        orientation="h",
        marker_color=colors,
        text=[f"{p:.2f}%" for p in percentages],
        textposition="auto"
    ))

    fig.update_layout(
        title=dict(text=title, font=dict(size=13, color="#FFFFFF")),
        paper_bgcolor=CHART_THEME["paper_bgcolor"],
        plot_bgcolor=CHART_THEME["plot_bgcolor"],
        font=CHART_THEME["font"],
        height=240,
        margin=dict(l=40, r=40, t=35, b=25),
        xaxis=dict(title="Percentage of Valid Pixels (%)", gridcolor=CHART_THEME["gridcolor"], range=[0, max(percentages) * 1.15]),
        yaxis=dict(gridcolor=CHART_THEME["gridcolor"])
    )
    return fig

def create_area_donut_chart(
    df: pd.DataFrame,
    names_col: str,
    values_col: str,
    colors_dict: dict = None,
    title: str = "Area Distribution"
):
    """Donut chart showing proportional area breakdown."""
    fig = px.pie(
        df,
        names=names_col,
        values=values_col,
        hole=0.45,
        title=title,
        color=names_col,
        color_discrete_map=colors_dict
    )

    fig.update_layout(
        paper_bgcolor=CHART_THEME["paper_bgcolor"],
        plot_bgcolor=CHART_THEME["plot_bgcolor"],
        font=CHART_THEME["font"],
        height=380,
        margin=dict(l=30, r=30, t=50, b=30),
        legend=dict(orientation="h", yanchor="bottom", y=-0.15)
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    return fig

def create_sensitivity_bar_chart(df: pd.DataFrame):
    """Bar chart comparing EVS Sensitivity scenarios for Very High Priority area."""
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df["Scenario"],
        y=df["Very High Priority (%)"],
        marker_color=["#2980B9", "#27AE60", "#34495E", "#E67E22", "#C0392B"],
        text=[f"{v:.2f}%" for v in df["Very High Priority (%)"]],
        textposition="auto"
    ))

    fig.update_layout(
        title=dict(text="Restoration Model Sensitivity: Very High Priority Area (%) across Weight Scenarios", font=dict(size=13, color="#FFFFFF")),
        paper_bgcolor=CHART_THEME["paper_bgcolor"],
        plot_bgcolor=CHART_THEME["plot_bgcolor"],
        font=CHART_THEME["font"],
        height=360,
        margin=dict(l=40, r=40, t=45, b=35),
        xaxis=dict(title="Model Scenario", gridcolor=CHART_THEME["gridcolor"]),
        yaxis=dict(title="Very High Priority (%)", gridcolor=CHART_THEME["gridcolor"])
    )
    return fig
