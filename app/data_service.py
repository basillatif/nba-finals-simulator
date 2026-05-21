"""Cached data access for Streamlit pages."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from data.ingestion import fetch_team_stats
from data.preprocessing import enrich_team_features


@st.cache_data(ttl=60 * 60 * 12, show_spinner=False)
def load_team_stats(season: str, season_type: str, force_refresh: bool = False) -> pd.DataFrame:
    """Load, enrich, and cache team-level statistics for the app."""

    return enrich_team_features(fetch_team_stats(season, season_type, force_refresh))
