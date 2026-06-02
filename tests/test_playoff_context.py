from app.data_service import load_team_stats, load_team_stats_dataset
from app.playoff_context import (
    ACTIVE_PLAYOFF_TEAMS,
    EAST_CHAMPION,
    FINALS_MATCHUP,
    WEST_CHAMPION,
    team_index,
)
from data.sample_teams import load_sample_team_stats


def test_sample_teams_match_2026_finals_field() -> None:
    teams = set(load_sample_team_stats()["team_name"])

    assert teams == set(ACTIVE_PLAYOFF_TEAMS)
    assert EAST_CHAMPION in teams
    assert WEST_CHAMPION in teams
    assert set(FINALS_MATCHUP).issubset(teams)
    assert FINALS_MATCHUP == ("San Antonio Spurs", "New York Knicks")


def test_team_index_prefers_configured_matchup() -> None:
    team_names = ["New York Knicks", "San Antonio Spurs"]

    assert team_index(team_names, "New York Knicks") == 0
    assert team_index(team_names, "San Antonio Spurs", fallback=1) == 1


def test_loaded_teams_are_limited_to_active_playoff_teams() -> None:
    teams = set(load_team_stats("2025-26", "Playoffs", force_refresh=False)["team_name"])

    assert teams == set(ACTIVE_PLAYOFF_TEAMS)


def test_loaded_team_dataset_reports_real_data_source() -> None:
    dataset = load_team_stats_dataset("2025-26", "Playoffs", force_refresh=False)

    assert dataset.is_real_data
    assert dataset.source == "cached_nba_api"
    assert dataset.last_updated is not None
    assert set(dataset.teams["team_name"]) == set(ACTIVE_PLAYOFF_TEAMS)
