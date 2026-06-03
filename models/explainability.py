"""Rule-based narrative explanations for matchup predictions."""

from __future__ import annotations

import pandas as pd


EXPLANATION_FEATURES = [
    ("net_rating", "overall net rating"),
    ("off_rating", "offensive efficiency"),
    ("def_rating", "defensive efficiency"),
    ("ts_pct", "true shooting"),
    ("tm_tov_pct", "turnover control"),
    ("reb_pct", "rebounding"),
    ("clutch_net_rating", "clutch performance"),
    ("recent_net_rating", "recent form"),
    ("finals_path_adjustment", "Finals path context"),
]


def possessive(name: str) -> str:
    """Return a readable possessive team name."""

    return f"{name}'" if name.endswith("s") else f"{name}'s"


def build_matchup_narrative(team_a: pd.Series, team_b: pd.Series, favorite: str) -> str:
    """Generate an interpretable explanation from the largest stat edges."""

    favorite_row = team_a if team_a["team_name"] == favorite else team_b
    underdog_row = team_b if team_a["team_name"] == favorite else team_a

    edges: list[tuple[float, str]] = []
    for column, label in EXPLANATION_FEATURES:
        if column not in favorite_row.index:
            continue
        diff = float(favorite_row[column]) - float(underdog_row[column])
        if column == "def_rating":
            diff *= -1
        if column == "tm_tov_pct":
            diff *= -1
        edges.append((diff, label))

    top_edges = [label for diff, label in sorted(edges, reverse=True) if diff > 0][:3]
    if not top_edges:
        return f"{possessive(favorite)} projection is narrow, with no single statistical category dominating the matchup."

    readable_edges = ", ".join(top_edges[:-1])
    if len(top_edges) > 1:
        readable_edges = f"{readable_edges}, and {top_edges[-1]}"
    else:
        readable_edges = top_edges[0]

    return f"{possessive(favorite)} edge comes from {readable_edges}."
