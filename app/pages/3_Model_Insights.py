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

from app.data_service import load_team_stats
from config.settings import settings
from data.preprocessing import FEATURE_COLUMNS


st.set_page_config(page_title="Model Insights", layout="wide")
st.title("Model Insights")

teams = load_team_stats(settings.season, settings.season_type)

st.write(
    "The first model slice uses an interpretable logistic-style heuristic over team differentials. "
    "A trained logistic regression pipeline is included as the baseline estimator boundary; the next iteration can add labeled playoff game outcomes and persist model artifacts."
)

importance = pd.DataFrame(
    {
        "feature": FEATURE_COLUMNS,
        "weight": [0.34, -0.18, 0.34, 0.03, 0.22, 0.05, -0.08, 0.14, 0.10, 0.08],
    }
)
fig = px.bar(
    importance.sort_values("weight"),
    x="weight",
    y="feature",
    orientation="h",
    template="plotly_white",
    title="Baseline Feature Direction",
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Team Feature Matrix")
st.dataframe(
    teams[["team_name", *[column for column in FEATURE_COLUMNS if column in teams.columns]]],
    use_container_width=True,
    hide_index=True,
)
