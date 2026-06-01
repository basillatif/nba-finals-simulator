"""NBA Finals Predictor Streamlit application."""

from __future__ import annotations

import streamlit as st

from app.data_service import load_team_stats
from app.playoff_context import EAST_CHAMPION, WEST_CHAMPION
from config.settings import settings


st.set_page_config(
    page_title=settings.app_name,
    page_icon=":basketball:",
    layout="wide",
    initial_sidebar_state="expanded",
)


def apply_theme() -> None:
    """Apply clean light styling."""

    st.markdown(
        """
        <style>
        .stApp {
            background: #f8fafc;
            color: #172033;
        }
        section[data-testid="stSidebar"] {
            background: #ffffff;
            border-right: 1px solid #e2e8f0;
        }
        div[data-testid="metric-container"] {
            background: #ffffff;
            border: 1px solid #e2e8f0;
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
            color: #475569;
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
    f'<div class="hero-copy">An interactive analytics workbench for the 2026 NBA Finals between the {WEST_CHAMPION} and {EAST_CHAMPION}.</div>',
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
