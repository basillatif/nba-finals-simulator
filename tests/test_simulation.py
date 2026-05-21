from simulation.monte_carlo import simulate_finals_series


def test_simulation_probabilities_sum_to_one() -> None:
    result = simulate_finals_series("Team A", "Team B", 0.55, simulations=1_000, random_seed=7)

    assert 0 <= result.team_a_championship_probability <= 1
    assert result.team_a_championship_probability + result.team_b_championship_probability == 1
    assert result.outcomes["probability"].sum() == 1
    assert 4 <= result.expected_series_length <= 7
