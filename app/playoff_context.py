"""Current playoff context used for Streamlit defaults."""

from __future__ import annotations


EAST_FINAL_MATCHUP = ("Cleveland Cavaliers", "New York Knicks")
WEST_FINAL_MATCHUP = ("Oklahoma City Thunder", "San Antonio Spurs")


def team_index(team_names: list[str], preferred_team: str, fallback: int = 0) -> int:
    """Return the index of a preferred team when it is present."""

    if preferred_team in team_names:
        return team_names.index(preferred_team)
    return min(fallback, len(team_names) - 1)
