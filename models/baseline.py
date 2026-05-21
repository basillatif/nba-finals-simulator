"""Baseline matchup model with a logistic-regression default."""

from __future__ import annotations

import math

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from data.preprocessing import FEATURE_COLUMNS, build_preprocessor, create_matchup_features


def build_logistic_regression_model() -> Pipeline:
    """Return the baseline model pipeline.

    The estimator is intentionally simple for the first production slice. The module boundary
    lets us replace it with XGBoost or LightGBM without rewriting Streamlit or simulation code.
    """

    return Pipeline(
        steps=[
            ("preprocessor", build_preprocessor()),
            ("classifier", LogisticRegression(max_iter=1_000, random_state=42)),
        ]
    )


def heuristic_game_probability(
    team_a: pd.Series,
    team_b: pd.Series,
    home_court_edge: float = 0.0,
    injury_adjustment_a: float = 0.0,
    injury_adjustment_b: float = 0.0,
    shooting_variance: float = 1.0,
) -> float:
    """Estimate Team A win probability from interpretable team stat differentials.

    This is a calibrated heuristic until a labeled playoff-game training set is added.
    """

    matchup = create_matchup_features(team_a, team_b, FEATURE_COLUMNS).iloc[0]
    score = (
        0.34 * matchup.get("diff_net_rating", 0.0)
        + 0.14 * matchup.get("diff_clutch_net_rating", 0.0)
        + 0.10 * matchup.get("diff_recent_net_rating", 0.0)
        + 3.8 * matchup.get("diff_ts_pct", 0.0)
        + 0.05 * matchup.get("diff_reb_pct", 0.0)
        - 0.08 * matchup.get("diff_tm_tov_pct", 0.0)
        + 1.6 * matchup.get("diff_playoff_weight", 0.0)
    )
    score += (injury_adjustment_a - injury_adjustment_b) * 0.55
    score += home_court_edge * 100
    score /= max(shooting_variance, 0.4)

    probability = 1.0 / (1.0 + math.exp(-score / 6.5))
    return min(max(probability, 0.03), 0.97)
