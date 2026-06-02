"""Monte Carlo simulation explorer page."""

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

from app.data_service import load_team_stats_dataset
from app.playoff_context import FINALS_MATCHUP, team_index
from config.settings import settings
from models.baseline import heuristic_game_probability
from simulation.monte_carlo import simulate_finals_series
from utils.charts import outcome_histogram, probability_bar


st.set_page_config(page_title="Simulation Explorer", layout="wide")
st.title("Simulation Explorer")

dataset = load_team_stats_dataset(settings.season, settings.season_type)
teams = dataset.teams
st.caption(f"Data source: {dataset.source.replace('_', ' ').title()}")
if not dataset.is_real_data:
    st.error("Real NBA data is unavailable, so simulations are disabled.")
    st.stop()
team_names = teams["team_name"].sort_values().tolist()

controls_top = st.columns(2)
finals_teams = list(FINALS_MATCHUP)
team_a_name = controls_top[0].selectbox(
    "Home-court Team A",
    finals_teams,
    index=team_index(finals_teams, FINALS_MATCHUP[0]),
)
team_b_name = FINALS_MATCHUP[1] if team_a_name == FINALS_MATCHUP[0] else FINALS_MATCHUP[0]
controls_top[1].text_input("Team B", value=team_b_name, disabled=True)

team_a = teams.loc[teams["team_name"] == team_a_name].iloc[0]
team_b = teams.loc[teams["team_name"] == team_b_name].iloc[0]

controls = st.columns(4)
simulations = controls[0].slider("Simulations", 10_000, 100_000, settings.default_simulations, 5_000)
home_edge = controls[1].slider("Home-court edge", 0.0, 0.08, settings.home_court_edge, 0.005)
injury_a = controls[2].slider(f"{team_a_name} injury adjustment", -10.0, 10.0, 0.0, 0.5)
injury_b = controls[3].slider(f"{team_b_name} injury adjustment", -10.0, 10.0, 0.0, 0.5)

with st.spinner("Running Monte Carlo simulation..."):
    neutral_probability_a = heuristic_game_probability(
        team_a,
        team_b,
        injury_adjustment_a=injury_a,
        injury_adjustment_b=injury_b,
    )
    result = simulate_finals_series(
        team_a_name=team_a_name,
        team_b_name=team_b_name,
        neutral_win_probability_a=neutral_probability_a,
        simulations=simulations,
        home_court_edge=home_edge,
    )

summary_cols = st.columns(3)
summary_cols[0].metric(f"{team_a_name} title probability", f"{result.team_a_championship_probability:.1%}")
summary_cols[1].metric(f"{team_b_name} title probability", f"{result.team_b_championship_probability:.1%}")
summary_cols[2].metric("Expected length", f"{result.expected_series_length:.2f} games")

st.plotly_chart(
    probability_bar(team_a_name, team_b_name, result.team_a_championship_probability),
    use_container_width=True,
)
st.plotly_chart(outcome_histogram(result.outcomes), use_container_width=True)

st.dataframe(result.outcomes.sort_values("probability", ascending=False), use_container_width=True, hide_index=True)
