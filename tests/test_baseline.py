from app.data_service import load_team_stats_dataset
from app.playoff_context import EAST_CHAMPION, WEST_CHAMPION
from models.baseline import heuristic_game_probability


def test_spurs_path_context_keeps_finals_probability_competitive() -> None:
    dataset = load_team_stats_dataset("2025-26", "Playoffs", force_refresh=False)
    teams = dataset.teams
    spurs = teams.loc[teams["team_name"] == WEST_CHAMPION].iloc[0]
    knicks = teams.loc[teams["team_name"] == EAST_CHAMPION].iloc[0]

    probability = heuristic_game_probability(spurs, knicks)

    assert probability > 0.30
