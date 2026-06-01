"""Plotly chart builders for the Streamlit app."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def probability_bar(team_a: str, team_b: str, prob_a: float) -> go.Figure:
    """Build a championship probability bar chart."""

    fig = go.Figure(
        data=[
            go.Bar(
                x=[team_a, team_b],
                y=[prob_a, 1 - prob_a],
                marker_color=["#ff6b35", "#4cc9f0"],
                text=[f"{prob_a:.1%}", f"{1 - prob_a:.1%}"],
                textposition="outside",
            )
        ]
    )
    fig.update_layout(
        yaxis_tickformat=".0%",
        yaxis_range=[0, 1],
        height=360,
        margin=dict(l=20, r=20, t=30, b=20),
        template="plotly_white",
    )
    return fig


def outcome_histogram(outcomes: pd.DataFrame) -> go.Figure:
    """Build a series outcome probability chart."""

    frame = outcomes.copy()
    frame["label"] = frame["winner"] + " " + frame["scoreline"]
    fig = px.bar(
        frame,
        x="label",
        y="probability",
        color="winner",
        text=frame["probability"].map(lambda value: f"{value:.1%}"),
        template="plotly_white",
    )
    fig.update_layout(
        xaxis_title="Series outcome",
        yaxis_title="Probability",
        yaxis_tickformat=".0%",
        height=420,
        margin=dict(l=20, r=20, t=30, b=80),
    )
    return fig


def radar_chart(team_a: pd.Series, team_b: pd.Series) -> go.Figure:
    """Compare two teams across normalized radar dimensions."""

    metrics = ["off_rating", "def_rating", "net_rating", "pace", "ts_pct", "reb_pct", "tm_tov_pct"]
    labels = ["Offense", "Defense", "Net", "Pace", "True Shooting", "Rebounding", "Turnovers"]

    values_a = []
    values_b = []
    for metric in metrics:
        a_value = float(team_a[metric])
        b_value = float(team_b[metric])
        if metric in {"def_rating", "tm_tov_pct"}:
            a_value *= -1
            b_value *= -1
        low = min(a_value, b_value)
        high = max(a_value, b_value)
        spread = high - low or 1.0
        values_a.append(50 + 50 * ((a_value - low) / spread))
        values_b.append(50 + 50 * ((b_value - low) / spread))

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=values_a, theta=labels, fill="toself", name=team_a["team_name"]))
    fig.add_trace(go.Scatterpolar(r=values_b, theta=labels, fill="toself", name=team_b["team_name"]))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        template="plotly_white",
        height=440,
        margin=dict(l=40, r=40, t=40, b=40),
    )
    return fig
