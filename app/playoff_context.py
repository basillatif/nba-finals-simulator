"""Current playoff context used for Streamlit defaults."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


EAST_CHAMPION = "New York Knicks"
WEST_CHAMPION = "San Antonio Spurs"
FINALS_MATCHUP = (WEST_CHAMPION, EAST_CHAMPION)
ACTIVE_PLAYOFF_TEAMS = (EAST_CHAMPION, WEST_CHAMPION)


@dataclass(frozen=True)
class FinalsPathContext:
    """Team-specific context from the conference finals path."""

    previous_round_games: int
    previous_round_opponent: str
    finals_path_adjustment: float


FINALS_PATH_CONTEXT = {
    EAST_CHAMPION: FinalsPathContext(
        previous_round_games=4,
        previous_round_opponent="Eastern Conference finalist",
        finals_path_adjustment=-1.2,
    ),
    WEST_CHAMPION: FinalsPathContext(
        previous_round_games=7,
        previous_round_opponent="Oklahoma City Thunder",
        finals_path_adjustment=1.8,
    ),
}
DEFAULT_FINALS_PATH_CONTEXT = FinalsPathContext(0, "", 0.0)


def add_finals_path_context(teams: pd.DataFrame) -> pd.DataFrame:
    """Add Finals path context without overwriting sourced team statistics."""

    enriched = teams.copy()
    enriched["previous_round_games"] = enriched["team_name"].map(
        lambda team_name: FINALS_PATH_CONTEXT.get(
            team_name,
            DEFAULT_FINALS_PATH_CONTEXT,
        ).previous_round_games
    )
    enriched["previous_round_opponent"] = enriched["team_name"].map(
        lambda team_name: FINALS_PATH_CONTEXT.get(
            team_name,
            DEFAULT_FINALS_PATH_CONTEXT,
        ).previous_round_opponent
    )
    enriched["finals_path_adjustment"] = enriched["team_name"].map(
        lambda team_name: FINALS_PATH_CONTEXT.get(
            team_name,
            DEFAULT_FINALS_PATH_CONTEXT,
        ).finals_path_adjustment
    )
    return enriched


def team_index(team_names: list[str], preferred_team: str, fallback: int = 0) -> int:
    """Return the index of a preferred team when it is present."""

    if preferred_team in team_names:
        return team_names.index(preferred_team)
    return min(fallback, len(team_names) - 1)
