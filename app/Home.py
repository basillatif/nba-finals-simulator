"""Home page for the NBA Finals Predictor app."""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]
APP_DIR = Path(__file__).resolve().parent

if str(APP_DIR) in sys.path:
    sys.path.remove(str(APP_DIR))
sys.path = [path for path in sys.path if path != str(PROJECT_ROOT)]
sys.path.insert(0, str(PROJECT_ROOT))

if "app" in sys.modules and not hasattr(sys.modules["app"], "__path__"):
    del sys.modules["app"]

from app.data_service import TeamStatsDataset, load_team_stats_dataset
from app.playoff_context import EAST_CHAMPION, FINALS_MATCHUP, WEST_CHAMPION, team_index
from config.settings import settings
from models.baseline import heuristic_game_probability
from models.explainability import build_matchup_narrative
from simulation.monte_carlo import simulate_finals_series
from utils.charts import outcome_histogram, probability_bar, radar_chart


st.set_page_config(
    page_title=settings.app_name,
    page_icon=":basketball:",
    layout="wide",
    initial_sidebar_state="expanded",
)


def apply_theme() -> None:
    """Apply polished Finals-focused styling."""

    st.markdown(
        """
        <style>
        .stApp {
            background: #f7f8fb;
            color: #172033;
        }
        section[data-testid="stSidebar"] {
            background: #ffffff;
            border-right: 1px solid #e2e8f0;
        }
        div[data-testid="metric-container"] {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 14px;
        }
        .hero-shell {
            background: linear-gradient(135deg, #111827 0%, #25324a 54%, #b91c1c 100%);
            border-radius: 8px;
            color: #ffffff;
            padding: 30px 34px;
            margin-bottom: 18px;
            box-shadow: 0 18px 42px rgba(15, 23, 42, 0.16);
        }
        .hero-title {
            font-size: 3.15rem;
            line-height: 1.05;
            font-weight: 800;
            letter-spacing: 0;
            margin-bottom: 0.4rem;
        }
        .hero-copy {
            color: #dbe4f0;
            max-width: 820px;
            font-size: 1.08rem;
            line-height: 1.55;
        }
        .hero-kicker {
            color: #fbbf24;
            font-size: 0.82rem;
            font-weight: 800;
            letter-spacing: 0.08em;
            margin-bottom: 0.8rem;
            text-transform: uppercase;
        }
        .verdict {
            color: #ffffff;
            font-size: 1.25rem;
            font-weight: 700;
            margin-top: 1.2rem;
        }
        .panel {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 18px 20px;
            min-height: 128px;
        }
        .panel-label {
            color: #64748b;
            font-size: 0.78rem;
            font-weight: 800;
            letter-spacing: 0.06em;
            margin-bottom: 0.4rem;
            text-transform: uppercase;
        }
        .panel-value {
            color: #172033;
            font-size: 1.32rem;
            font-weight: 800;
            line-height: 1.12;
        }
        .panel-note {
            color: #64748b;
            font-size: 0.9rem;
            line-height: 1.35;
            margin-top: 0.55rem;
        }
        .section-copy {
            color: #475569;
            max-width: 900px;
        }
        div[data-testid="stDataFrame"] {
            border: 1px solid #e2e8f0;
            border-radius: 8px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def format_gap(value: float, suffix: str = "") -> str:
    """Format a signed matchup gap for display."""

    sign = "+" if value > 0 else ""
    return f"{sign}{value:.1f}{suffix}"


def short_team_name(team_name: str) -> str:
    """Return a punchy team label for compact UI surfaces."""

    known_names = {
        "New York Knicks": "Knicks",
        "San Antonio Spurs": "Spurs",
    }
    return known_names.get(team_name, team_name.split()[-1])


def data_source_label(dataset: TeamStatsDataset) -> str:
    """Return a readable source label for the app chrome."""

    labels = {
        "live_nba_api": "Live NBA API",
        "cached_nba_api": "Cached NBA API",
        "sample_fallback": "Sample fallback",
    }
    return labels.get(dataset.source, dataset.source.replace("_", " ").title())


def format_last_updated(dataset: TeamStatsDataset) -> str:
    """Return a concise timestamp for cached or refreshed data."""

    if dataset.last_updated is None:
        return "Not available"
    return dataset.last_updated.astimezone().strftime("%b %d, %Y %I:%M %p %Z")


def build_edge_rows(team_a, team_b) -> list[dict[str, str]]:
    """Build readable head-to-head edge rows for the homepage."""

    edge_specs = [
        ("Offensive firepower", "off_rating", " points per 100", True),
        ("Defensive resistance", "def_rating", " points allowed per 100", False),
        ("Shot quality", "ts_pct", " percentage points", True),
        ("Turnover control", "tm_tov_pct", " percentage points", False),
        ("Rebounding", "reb_pct", " percentage points", True),
        ("Close-game profile", "clutch_net_rating", " points per 100", True),
        ("Recent form", "recent_net_rating", " points per 100", True),
    ]

    rows: list[dict[str, str]] = []
    for label, column, suffix, higher_is_better in edge_specs:
        value_a = float(team_a[column])
        value_b = float(team_b[column])
        if column == "ts_pct":
            value_a *= 100
            value_b *= 100

        a_leads = value_a >= value_b if higher_is_better else value_a <= value_b
        leader = team_a["team_name"] if a_leads else team_b["team_name"]
        leader_value = value_a if a_leads else value_b
        trailing_value = value_b if a_leads else value_a
        raw_gap = leader_value - trailing_value
        gap = raw_gap if higher_is_better else abs(raw_gap)
        rows.append(
            {
                "Matchup lever": label,
                "Edge": leader,
                "Gap": format_gap(gap, suffix),
            }
        )
    return rows


apply_theme()

st.sidebar.title(settings.app_name)
season = st.sidebar.text_input("Season", value=settings.season)
season_type_options = ["Regular Season", "Playoffs"]
season_type = st.sidebar.selectbox(
    "Season type",
    season_type_options,
    index=season_type_options.index(settings.season_type),
)
force_refresh = st.sidebar.toggle("Refresh nba_api cache", value=False)

with st.spinner("Loading team metrics..."):
    dataset = load_team_stats_dataset(
        season=season,
        season_type=season_type,
        force_refresh=force_refresh,
    )
    teams = dataset.teams

st.sidebar.caption(f"Data source: {data_source_label(dataset)}")
st.sidebar.caption(f"Last updated: {format_last_updated(dataset)}")

if dataset.error:
    st.sidebar.warning("Live refresh failed; using the latest cached NBA API snapshot.")

if not dataset.is_real_data:
    st.error(
        "Real NBA data is unavailable, so predictions are disabled. "
        "Refresh the NBA API cache or add a tracked NBA API snapshot before launch."
    )
    if dataset.error:
        st.caption(f"Refresh error: {dataset.error}")
    st.stop()

team_a = teams.loc[teams["team_name"] == WEST_CHAMPION].iloc[0]
team_b = teams.loc[teams["team_name"] == EAST_CHAMPION].iloc[0]

with st.spinner("Simulating the Finals..."):
    neutral_probability_a = heuristic_game_probability(team_a, team_b)
    result = simulate_finals_series(
        team_a_name=WEST_CHAMPION,
        team_b_name=EAST_CHAMPION,
        neutral_win_probability_a=neutral_probability_a,
        simulations=settings.default_simulations,
        home_court_edge=settings.home_court_edge,
    )

champion_probability = max(
    result.team_a_championship_probability,
    result.team_b_championship_probability,
)
projected_champion = (
    WEST_CHAMPION
    if result.team_a_championship_probability >= result.team_b_championship_probability
    else EAST_CHAMPION
)
top_outcome = result.outcomes.sort_values("probability", ascending=False).iloc[0]
top_outcome_label = f'{short_team_name(top_outcome["winner"])} in {int(top_outcome["games"])}'
matchup_narrative = build_matchup_narrative(team_a, team_b, projected_champion)

st.markdown(
    f"""
    <div class="hero-shell">
        <div class="hero-kicker">2026 Finals forecast</div>
        <div class="hero-title">{WEST_CHAMPION} vs {EAST_CHAMPION}</div>
        <div class="hero-copy">
            A best-of-seven simulator that turns team strengths into a title forecast,
            series scripts, and the matchup levers most likely to decide June.
        </div>
        <div class="verdict">
            First read: {projected_champion} win the title {champion_probability:.1%} of the time.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

summary_cols = st.columns(3)
summary_cols[0].markdown(
    f"""
    <div class="panel">
        <div class="panel-label">Projected champion</div>
        <div class="panel-value">{projected_champion}</div>
        <div class="panel-note">{champion_probability:.1%} championship probability across {settings.default_simulations:,} series.</div>
    </div>
    """,
    unsafe_allow_html=True,
)
summary_cols[1].markdown(
    f"""
    <div class="panel">
        <div class="panel-label">Most likely ending</div>
        <div class="panel-value">{top_outcome_label}</div>
        <div class="panel-note">{top_outcome["probability"]:.1%} of simulations ended this way.</div>
    </div>
    """,
    unsafe_allow_html=True,
)
summary_cols[2].markdown(
    f"""
    <div class="panel">
        <div class="panel-label">Expected fight</div>
        <div class="panel-value">{result.expected_series_length:.2f} games</div>
        <div class="panel-note">Neutral Game 1 win probability: {neutral_probability_a:.1%} for {WEST_CHAMPION}.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.info(matchup_narrative)

st.subheader("Title Probability")
st.plotly_chart(
    probability_bar(WEST_CHAMPION, EAST_CHAMPION, result.team_a_championship_probability),
    use_container_width=True,
)

st.subheader("Series Scripts")
st.plotly_chart(outcome_histogram(result.outcomes), use_container_width=True)

st.subheader("What Actually Swings The Matchup")
st.markdown(
    '<div class="section-copy">These are direct team-vs-team advantages, not blended averages. Each row points to a basketball pressure point the series can turn on.</div>',
    unsafe_allow_html=True,
)
st.dataframe(
    build_edge_rows(team_a, team_b),
    use_container_width=True,
    hide_index=True,
)

st.divider()
st.header("Team Comparison")

team_names = teams["team_name"].sort_values().tolist()
left, right = st.columns(2)
comparison_team_a_name = left.selectbox(
    "Team A",
    team_names,
    index=team_index(team_names, FINALS_MATCHUP[0]),
)
comparison_team_b_name = right.selectbox(
    "Team B",
    team_names,
    index=team_index(team_names, FINALS_MATCHUP[1], 1),
)

comparison_team_a = teams.loc[teams["team_name"] == comparison_team_a_name].iloc[0]
comparison_team_b = teams.loc[teams["team_name"] == comparison_team_b_name].iloc[0]

controls = st.columns(3)
injury_a = controls[0].slider(
    f"{comparison_team_a_name} injury adjustment",
    -10.0,
    10.0,
    0.0,
    0.5,
)
injury_b = controls[1].slider(
    f"{comparison_team_b_name} injury adjustment",
    -10.0,
    10.0,
    0.0,
    0.5,
)
shooting_variance = controls[2].slider("Shooting variance", 0.6, 1.8, 1.0, 0.1)

comparison_probability_a = heuristic_game_probability(
    comparison_team_a,
    comparison_team_b,
    injury_adjustment_a=injury_a,
    injury_adjustment_b=injury_b,
    shooting_variance=shooting_variance,
)
comparison_favorite = (
    comparison_team_a_name if comparison_probability_a >= 0.5 else comparison_team_b_name
)

metric_cols = st.columns(3)
metric_cols[0].metric(
    f"{comparison_team_a_name} win probability",
    f"{comparison_probability_a:.1%}",
)
metric_cols[1].metric(
    f"{comparison_team_b_name} win probability",
    f"{1 - comparison_probability_a:.1%}",
)
metric_cols[2].metric("Projected favorite", comparison_favorite)

st.plotly_chart(
    probability_bar(
        comparison_team_a_name,
        comparison_team_b_name,
        comparison_probability_a,
    ),
    use_container_width=True,
)
st.info(build_matchup_narrative(comparison_team_a, comparison_team_b, comparison_favorite))

st.subheader("Radar Comparison")
st.plotly_chart(
    radar_chart(comparison_team_a, comparison_team_b),
    use_container_width=True,
)

st.subheader("Raw Matchup Table")
st.dataframe(
    teams[teams["team_name"].isin([comparison_team_a_name, comparison_team_b_name])].T,
    use_container_width=True,
)
