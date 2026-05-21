"""Small built-in dataset so the app works before live ingestion is run."""

from __future__ import annotations

import pandas as pd


SAMPLE_TEAM_STATS = [
    {
        "team_id": 1610612738,
        "team_name": "Boston Celtics",
        "off_rating": 122.2,
        "def_rating": 110.6,
        "net_rating": 11.6,
        "pace": 97.2,
        "ts_pct": 0.609,
        "reb_pct": 51.8,
        "tm_tov_pct": 11.3,
        "clutch_net_rating": 15.4,
        "recent_net_rating": 12.3,
        "playoff_weight": 1.08,
    },
    {
        "team_id": 1610612743,
        "team_name": "Denver Nuggets",
        "off_rating": 118.5,
        "def_rating": 113.0,
        "net_rating": 5.5,
        "pace": 96.2,
        "ts_pct": 0.589,
        "reb_pct": 50.9,
        "tm_tov_pct": 11.8,
        "clutch_net_rating": 8.2,
        "recent_net_rating": 7.1,
        "playoff_weight": 1.06,
    },
    {
        "team_id": 1610612760,
        "team_name": "Oklahoma City Thunder",
        "off_rating": 118.3,
        "def_rating": 111.1,
        "net_rating": 7.2,
        "pace": 99.8,
        "ts_pct": 0.608,
        "reb_pct": 48.5,
        "tm_tov_pct": 11.2,
        "clutch_net_rating": 10.7,
        "recent_net_rating": 8.9,
        "playoff_weight": 1.04,
    },
    {
        "team_id": 1610612750,
        "team_name": "Minnesota Timberwolves",
        "off_rating": 115.6,
        "def_rating": 108.4,
        "net_rating": 7.2,
        "pace": 97.1,
        "ts_pct": 0.594,
        "reb_pct": 51.2,
        "tm_tov_pct": 13.0,
        "clutch_net_rating": 6.9,
        "recent_net_rating": 7.8,
        "playoff_weight": 1.02,
    },
    {
        "team_id": 1610612749,
        "team_name": "Milwaukee Bucks",
        "off_rating": 117.6,
        "def_rating": 115.0,
        "net_rating": 2.6,
        "pace": 100.2,
        "ts_pct": 0.601,
        "reb_pct": 50.2,
        "tm_tov_pct": 11.9,
        "clutch_net_rating": 4.5,
        "recent_net_rating": 3.1,
        "playoff_weight": 1.00,
    },
    {
        "team_id": 1610612742,
        "team_name": "Dallas Mavericks",
        "off_rating": 117.0,
        "def_rating": 114.9,
        "net_rating": 2.1,
        "pace": 99.4,
        "ts_pct": 0.592,
        "reb_pct": 49.1,
        "tm_tov_pct": 11.4,
        "clutch_net_rating": 9.3,
        "recent_net_rating": 5.8,
        "playoff_weight": 1.03,
    },
]


def load_sample_team_stats() -> pd.DataFrame:
    """Return representative team-level stats for local development."""

    return pd.DataFrame(SAMPLE_TEAM_STATS)
