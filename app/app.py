"""NBA Finals Predictor Streamlit application."""

from __future__ import annotations

import streamlit as st

from app.data_service import load_team_stats
from config.settings import settings


st.set_page_config(
    page_title=settings.app_name,
    page_icon=":basketball:",
    layout="wide",
    initial_sidebar_state="expanded",
)


def apply_theme() -> None:
    """Apply NBA-inspired dark styling."""

    st.markdown(
        """
        <style>
        .stApp {
            background: radial-gradient(circle at top left, #18243a 0, #080b12 36%, #05070d 100%);
            color: #f7f7fb;
        }
        section[data-testid="stSidebar"] {
            background: #090d16;
            border-right: 1px solid rgba(255, 255, 255, 0.08);
        }
        div[data-testid="metric-container"] {
            background: rgba(255, 255, 255, 0.055);
            border: 1px solid rgba(255, 255, 255, 0.10);
            border-radius: 8px;
            padding: 14px;
        }
        .hero-title {
            font-size: 3rem;
            line-height: 1.05;
            font-weight: 800;
            letter-spacing: 0;
            margin-bottom: 0.25rem;
        }
        .hero-copy {
            color: #c9d3e5;
            max-width: 850px;
            font-size: 1.05rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


apply_theme()

st.sidebar.title(settings.app_name)
season = st.sidebar.text_input("Season", value=settings.season)
season_type_options = ["Regular Season", "Playoffs"]
season_type = st.sidebar.selectbox(
    "Season type",
    season_type_options,
    index=season_type_options.index(settings.season_type),
)
force_refresh = st.sidebar.toggle("Refresh nba_api cache", value=False)

with st.spinner("Loading team metrics..."):
    teams = load_team_stats(season=season, season_type=season_type, force_refresh=force_refresh)

st.markdown('<div class="hero-title">NBA Finals Predictor</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-copy">An interactive analytics workbench for comparing Finals matchups, estimating game-level win probability, and stress-testing outcomes with Monte Carlo simulation.</div>',
    unsafe_allow_html=True,
)

st.divider()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Teams loaded", len(teams))
col2.metric("Avg net rating", f"{teams['net_rating'].mean():.1f}")
col3.metric("Avg pace", f"{teams['pace'].mean():.1f}")
col4.metric("Avg true shooting", f"{teams['ts_pct'].mean():.1%}")

st.subheader("Project Architecture")
st.write(
    "The app separates ingestion, preprocessing, modeling, simulation, charting, and Streamlit pages. "
    "That keeps the current heuristic baseline easy to replace with a trained logistic regression, XGBoost, or LightGBM model once a labeled playoff-game dataset is added."
)

st.dataframe(
    teams.sort_values("net_rating", ascending=False),
    use_container_width=True,
    hide_index=True,
)
