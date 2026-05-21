"""Feature engineering and preprocessing for matchup modeling."""

from __future__ import annotations

from typing import Iterable

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


FEATURE_COLUMNS = [
    "off_rating",
    "def_rating",
    "net_rating",
    "pace",
    "ts_pct",
    "reb_pct",
    "tm_tov_pct",
    "clutch_net_rating",
    "recent_net_rating",
    "playoff_weight",
]


def enrich_team_features(team_stats: pd.DataFrame) -> pd.DataFrame:
    """Add maintainable derived features used by the model and simulator."""

    df = team_stats.copy()
    df["clutch_net_rating"] = df["clutch_net_rating"].fillna(df["net_rating"])
    df["recent_net_rating"] = df.get("recent_net_rating", df["net_rating"])
    df["playoff_weight"] = df.get("playoff_weight", 1.0)
    df["efficiency_balance"] = df["off_rating"] - df["def_rating"]
    df["possession_quality"] = df["ts_pct"] * 100 - df["tm_tov_pct"] + df["reb_pct"] / 10
    return df


def build_preprocessor() -> Pipeline:
    """Create a numeric preprocessing pipeline for baseline models."""

    return Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )


def create_matchup_features(
    team_a: pd.Series,
    team_b: pd.Series,
    feature_columns: Iterable[str] = FEATURE_COLUMNS,
) -> pd.DataFrame:
    """Represent a matchup as Team A minus Team B feature differentials."""

    values = {
        f"diff_{column}": float(team_a[column]) - float(team_b[column])
        for column in feature_columns
        if column in team_a.index and column in team_b.index
    }
    return pd.DataFrame([values])


def estimate_recent_form(team_game_logs: pd.DataFrame, window: int = 10) -> pd.DataFrame:
    """Compute rolling recent form from team game logs when historical logs are available."""

    if team_game_logs.empty:
        return pd.DataFrame(columns=["team_id", "recent_net_rating"])

    logs = team_game_logs.sort_values(["team_id", "game_date"]).copy()
    logs["recent_net_rating"] = (
        logs.groupby("team_id")["net_rating"]
        .rolling(window=window, min_periods=3)
        .mean()
        .reset_index(level=0, drop=True)
    )
    latest = logs.groupby("team_id", as_index=False).tail(1)
    return latest[["team_id", "recent_net_rating"]].replace({np.nan: None})
