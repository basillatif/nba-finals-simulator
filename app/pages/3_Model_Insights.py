"""Model insights and explainability page."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
APP_DIR = Path(__file__).resolve().parents[1]

if str(APP_DIR) in sys.path:
    sys.path.remove(str(APP_DIR))
sys.path = [path for path in sys.path if path != str(PROJECT_ROOT)]
sys.path.insert(0, str(PROJECT_ROOT))

if "app" in sys.modules and not hasattr(sys.modules["app"], "__path__"):
    del sys.modules["app"]

from app.data_service import load_team_stats_dataset
from config.settings import settings
from data.preprocessing import FEATURE_COLUMNS


st.set_page_config(page_title="Model Insights", layout="wide")
st.title("Model Insights")

dataset = load_team_stats_dataset(settings.season, settings.season_type)
teams = dataset.teams
st.caption(f"Data source: {dataset.source.replace('_', ' ').title()}")
if not dataset.is_real_data:
    st.error("Real NBA data is unavailable, so model insights are disabled.")
    st.stop()

st.write(
    "The first model slice uses an interpretable logistic-style heuristic over team differentials. "
    "It now tempers noisy recent-form and clutch samples, then adds explicit Finals path context "
    "so New York's sweep and San Antonio's seven-game Thunder test influence the forecast without "
    "overwhelming the core team-quality signal."
)

importance = pd.DataFrame(
    {
        "feature": FEATURE_COLUMNS,
        "weight": [0.0, 0.0, 0.34, 0.0, 3.8, 0.05, -0.08, 0.14, 0.06, 1.6, 1.0],
    }
)
fig = px.bar(
    importance.sort_values("weight"),
    x="weight",
    y="feature",
    orientation="h",
    template="plotly_white",
    title="Heuristic Feature Coefficients",
)
st.plotly_chart(fig, use_container_width=True)

st.info(
    "Finals path context is a manual matchup adjustment: a small haircut for the Knicks' sweep "
    "layoff/rhythm risk and a Spurs bump for surviving a seven-game Western Conference Finals "
    "against Oklahoma City."
)

st.subheader("Team Feature Matrix")
st.dataframe(
    teams[["team_name", *[column for column in FEATURE_COLUMNS if column in teams.columns]]],
    use_container_width=True,
    hide_index=True,
)
