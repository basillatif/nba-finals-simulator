"""Current playoff context used for Streamlit defaults."""

from __future__ import annotations


EAST_CHAMPION = "New York Knicks"
WEST_CHAMPION = "San Antonio Spurs"
FINALS_MATCHUP = (WEST_CHAMPION, EAST_CHAMPION)
ACTIVE_PLAYOFF_TEAMS = (EAST_CHAMPION, WEST_CHAMPION)


def team_index(team_names: list[str], preferred_team: str, fallback: int = 0) -> int:
    """Return the index of a preferred team when it is present."""

    if preferred_team in team_names:
        return team_names.index(preferred_team)
    return min(fallback, len(team_names) - 1)
