"""Cached data access for Streamlit pages."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

import pandas as pd
import streamlit as st

from app.playoff_context import ACTIVE_PLAYOFF_TEAMS
from data.ingestion import fetch_team_stats, fetch_team_stats_with_metadata
from data.preprocessing import enrich_team_features


@dataclass(frozen=True)
class TeamStatsDataset:
    """Active Finals teams plus data-source provenance."""

    teams: pd.DataFrame
    source: str
    is_real_data: bool
    last_updated: datetime | None = None
    error: str | None = None


@st.cache_data(ttl=60 * 60 * 12, show_spinner=False)
def load_team_stats(season: str, season_type: str, force_refresh: bool = False) -> pd.DataFrame:
    """Load, enrich, and cache team-level statistics for the app."""

    teams = enrich_team_features(fetch_team_stats(season, season_type, force_refresh))
    active_teams = teams[teams["team_name"].isin(ACTIVE_PLAYOFF_TEAMS)].copy()
    return active_teams.sort_values("team_name").reset_index(drop=True)


@st.cache_data(ttl=60 * 60 * 12, show_spinner=False)
def load_team_stats_dataset(
    season: str,
    season_type: str,
    force_refresh: bool = False,
) -> TeamStatsDataset:
    """Load active Finals teams with launch-safe data-source metadata."""

    result = fetch_team_stats_with_metadata(season, season_type, force_refresh)
    teams = enrich_team_features(result.stats)
    active_teams = teams[teams["team_name"].isin(ACTIVE_PLAYOFF_TEAMS)].copy()
    return TeamStatsDataset(
        teams=active_teams.sort_values("team_name").reset_index(drop=True),
        source=result.source,
        is_real_data=result.is_real_data,
        last_updated=result.last_updated,
        error=result.error,
    )
