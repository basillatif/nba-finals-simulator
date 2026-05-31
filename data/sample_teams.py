"""Small built-in dataset so the app works before live ingestion is run."""

from __future__ import annotations

import pandas as pd


SAMPLE_TEAM_STATS = [
    {
        "team_id": 1610612752,
        "team_name": "New York Knicks",
        "off_rating": 117.8,
        "def_rating": 112.4,
        "net_rating": 5.4,
        "pace": 96.4,
        "ts_pct": 0.589,
        "reb_pct": 51.4,
        "tm_tov_pct": 11.6,
        "clutch_net_rating": 9.8,
        "recent_net_rating": 7.4,
        "playoff_weight": 1.06,
    },
    {
        "team_id": 1610612759,
        "team_name": "San Antonio Spurs",
        "off_rating": 118.9,
        "def_rating": 112.0,
        "net_rating": 6.9,
        "pace": 99.6,
        "ts_pct": 0.596,
        "reb_pct": 51.1,
        "tm_tov_pct": 12.0,
        "clutch_net_rating": 8.8,
        "recent_net_rating": 8.2,
        "playoff_weight": 1.06,
    },
]


def load_sample_team_stats() -> pd.DataFrame:
    """Return representative team-level stats for local development."""

    return pd.DataFrame(SAMPLE_TEAM_STATS)
