from app.data_service import load_team_stats
from app.playoff_context import ACTIVE_PLAYOFF_TEAMS, EAST_FINAL_MATCHUP, WEST_FINAL_MATCHUP, team_index
from data.sample_teams import load_sample_team_stats


def test_sample_teams_match_2026_conference_finalists() -> None:
    teams = set(load_sample_team_stats()["team_name"])

    assert teams == set(ACTIVE_PLAYOFF_TEAMS)
    assert set(EAST_FINAL_MATCHUP).issubset(teams)
    assert set(WEST_FINAL_MATCHUP).issubset(teams)


def test_team_index_prefers_configured_matchup() -> None:
    team_names = ["Cleveland Cavaliers", "New York Knicks"]

    assert team_index(team_names, "New York Knicks") == 1
    assert team_index(team_names, "Oklahoma City Thunder", fallback=1) == 1


def test_loaded_teams_are_limited_to_active_playoff_teams() -> None:
    teams = set(load_team_stats("2025-26", "Playoffs", force_refresh=False)["team_name"])

    assert teams == set(ACTIVE_PLAYOFF_TEAMS)
