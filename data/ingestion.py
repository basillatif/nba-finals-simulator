"""Data ingestion pipeline for NBA team-level statistics."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from config.settings import settings
from data.sample_teams import load_sample_team_stats
from utils.logging import get_logger

logger = get_logger(__name__)


CORE_COLUMNS = {
    "TEAM_ID": "team_id",
    "TEAM_NAME": "team_name",
    "OFF_RATING": "off_rating",
    "DEF_RATING": "def_rating",
    "NET_RATING": "net_rating",
    "PACE": "pace",
    "TS_PCT": "ts_pct",
    "REB_PCT": "reb_pct",
    "TM_TOV_PCT": "tm_tov_pct",
}


def _cache_path(season: str, season_type: str) -> Path:
    safe_type = season_type.lower().replace(" ", "_")
    return settings.cache_dir / f"team_stats_{season}_{safe_type}.csv"


def fetch_team_stats(
    season: str = settings.season,
    season_type: str = settings.season_type,
    force_refresh: bool = False,
) -> pd.DataFrame:
    """Load team-level stats from cache, with explicit live refresh support."""

    settings.cache_dir.mkdir(parents=True, exist_ok=True)
    cache_file = _cache_path(season, season_type)

    if cache_file.exists() and not force_refresh:
        logger.info("Loading cached team stats from %s", cache_file)
        return pd.read_csv(cache_file)

    if not force_refresh:
        logger.info("No cached team stats found at %s; using sample data", cache_file)
        return load_sample_team_stats()

    try:
        from nba_api.stats.endpoints import leaguedashteamstats

        logger.info("Fetching team stats for %s (%s)", season, season_type)
        base = leaguedashteamstats.LeagueDashTeamStats(
            season=season,
            season_type_all_star=season_type,
            measure_type_detailed_defense="Advanced",
            timeout=settings.timeout_seconds,
        ).get_data_frames()[0]

        stats = base.rename(columns=CORE_COLUMNS)[list(CORE_COLUMNS.values())]
        clutch = fetch_clutch_metrics(season=season, season_type=season_type)
        stats = stats.merge(clutch, on=["team_id", "team_name"], how="left")
        stats.to_csv(cache_file, index=False)
        return stats
    except Exception as exc:  # pragma: no cover - protects Streamlit UX from API outages
        logger.warning("nba_api ingestion failed; using sample data. Error: %s", exc)
        return load_sample_team_stats()


def fetch_clutch_metrics(
    season: str = settings.season,
    season_type: str = settings.season_type,
) -> pd.DataFrame:
    """Fetch clutch net rating when available."""

    from nba_api.stats.endpoints import leaguedashteamclutch

    clutch = leaguedashteamclutch.LeagueDashTeamClutch(
        season=season,
        season_type_all_star=season_type,
        measure_type_detailed_defense="Advanced",
        clutch_time="Last 5 Minutes",
        ahead_behind="Ahead or Behind",
        point_diff=5,
        timeout=settings.timeout_seconds,
    ).get_data_frames()[0]

    return clutch.rename(
        columns={
            "TEAM_ID": "team_id",
            "TEAM_NAME": "team_name",
            "NET_RATING": "clutch_net_rating",
        }
    )[["team_id", "team_name", "clutch_net_rating"]]
