"""Monte Carlo simulation for best-of-seven NBA Finals series."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


HOME_PATTERN = ("A", "A", "B", "B", "A", "B", "A")


@dataclass(frozen=True)
class SeriesSimulationResult:
    """Aggregated output from repeated series simulations."""

    team_a_name: str
    team_b_name: str
    team_a_championship_probability: float
    team_b_championship_probability: float
    expected_series_length: float
    outcomes: pd.DataFrame
    simulated_series: pd.DataFrame


def simulate_finals_series(
    team_a_name: str,
    team_b_name: str,
    neutral_win_probability_a: float,
    simulations: int = 10_000,
    home_court_edge: float = 0.035,
    random_seed: int | None = 42,
) -> SeriesSimulationResult:
    """Simulate a 2-2-1-1-1 best-of-seven series."""

    rng = np.random.default_rng(random_seed)
    rows: list[dict[str, object]] = []

    for simulation_id in range(simulations):
        wins_a = 0
        wins_b = 0
        games_played = 0

        for home_team in HOME_PATTERN:
            home_adjustment = home_court_edge if home_team == "A" else -home_court_edge
            game_probability_a = np.clip(neutral_win_probability_a + home_adjustment, 0.02, 0.98)
            if rng.random() < game_probability_a:
                wins_a += 1
            else:
                wins_b += 1

            games_played += 1
            if wins_a == 4 or wins_b == 4:
                break

        winner = team_a_name if wins_a > wins_b else team_b_name
        loser_wins = min(wins_a, wins_b)
        rows.append(
            {
                "simulation_id": simulation_id,
                "winner": winner,
                "games": games_played,
                "team_a_wins": wins_a,
                "team_b_wins": wins_b,
                "outcome": f"{winner} in {games_played}",
                "scoreline": f"4-{loser_wins}",
            }
        )

    simulated = pd.DataFrame(rows)
    team_a_probability = float((simulated["winner"] == team_a_name).mean())
    outcome_counts = (
        simulated.groupby(["winner", "scoreline", "games"], as_index=False)
        .size()
        .rename(columns={"size": "count"})
    )
    outcome_counts["probability"] = outcome_counts["count"] / simulations

    return SeriesSimulationResult(
        team_a_name=team_a_name,
        team_b_name=team_b_name,
        team_a_championship_probability=team_a_probability,
        team_b_championship_probability=1.0 - team_a_probability,
        expected_series_length=float(simulated["games"].mean()),
        outcomes=outcome_counts,
        simulated_series=simulated,
    )
