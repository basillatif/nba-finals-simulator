"""Team comparison page."""

from __future__ import annotations

import sys
from pathlib import Path

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
from app.playoff_context import FINALS_MATCHUP, team_index
from config.settings import settings
from models.baseline import heuristic_game_probability
from models.explainability import build_matchup_narrative
from utils.charts import probability_bar, radar_chart


st.set_page_config(page_title="Team Comparison", layout="wide")
st.title("Team Comparison")

teams = load_team_stats(settings.season, settings.season_type)
team_names = teams["team_name"].sort_values().tolist()

left, right = st.columns(2)
team_a_name = left.selectbox("Team A", team_names, index=team_index(team_names, FINALS_MATCHUP[0]))
team_b_name = right.selectbox("Team B", team_names, index=team_index(team_names, FINALS_MATCHUP[1], 1))

team_a = teams.loc[teams["team_name"] == team_a_name].iloc[0]
team_b = teams.loc[teams["team_name"] == team_b_name].iloc[0]

controls = st.columns(3)
injury_a = controls[0].slider(f"{team_a_name} injury adjustment", -10.0, 10.0, 0.0, 0.5)
injury_b = controls[1].slider(f"{team_b_name} injury adjustment", -10.0, 10.0, 0.0, 0.5)
shooting_variance = controls[2].slider("Shooting variance", 0.6, 1.8, 1.0, 0.1)

probability_a = heuristic_game_probability(
    team_a,
    team_b,
    injury_adjustment_a=injury_a,
    injury_adjustment_b=injury_b,
    shooting_variance=shooting_variance,
)
favorite = team_a_name if probability_a >= 0.5 else team_b_name

metric_cols = st.columns(3)
metric_cols[0].metric(f"{team_a_name} win probability", f"{probability_a:.1%}")
metric_cols[1].metric(f"{team_b_name} win probability", f"{1 - probability_a:.1%}")
metric_cols[2].metric("Projected favorite", favorite)

st.plotly_chart(probability_bar(team_a_name, team_b_name, probability_a), use_container_width=True)
st.info(build_matchup_narrative(team_a, team_b, favorite))

st.subheader("Radar Comparison")
st.plotly_chart(radar_chart(team_a, team_b), use_container_width=True)

st.subheader("Raw Matchup Table")
st.dataframe(
    teams[teams["team_name"].isin([team_a_name, team_b_name])].T,
    use_container_width=True,
)
