# NBA Finals Predictor

An interactive Streamlit analytics app for predicting the 2026 NBA Finals matchup between the San Antonio Spurs and New York Knicks.

## Architecture

- `app/`: Streamlit app and multipage UI.
- `data/`: nba_api ingestion, sample fallback data, and preprocessing.
- `models/`: baseline logistic-regression boundary, heuristic predictor, and explainability.
- `simulation/`: best-of-7 Monte Carlo engine.
- `utils/`: logging and chart helpers.
- `tests/`: focused regression tests.

The first implementation keeps live data ingestion, feature engineering, prediction, and simulation decoupled. That makes the app usable now with sample fallback data while leaving a clean path to train and persist a real supervised model.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
streamlit run app/app.py
```

## Current Features

- Team-level advanced-stat ingestion through `nba_api`.
- Cached sample fallback when the NBA Stats API is unavailable.
- Preprocessing hooks for missing values, scaling, recent form, and playoff weighting.
- Interpretable game-win probability baseline.
- Best-of-7 Finals Monte Carlo simulator with home-court advantage.
- Fixed Spurs-Knicks Finals simulator.
- Streamlit pages for home, team comparison, simulation exploration, and model insights.
- Plotly probability bars, outcome charts, and matchup radar charts.

## Tradeoffs

This initial version uses a calibrated heuristic for live predictions because a production supervised model needs a labeled historical playoff-game dataset with consistent feature snapshots before each game. The project already includes a logistic-regression pipeline boundary so the heuristic can be replaced without changing the UI or simulator.

## Deployment

The app is compatible with Streamlit Community Cloud. Set environment variables from `.env.example`, then use:

```bash
streamlit run app/app.py
```

For Docker:

```bash
docker build -t nba-finals-predictor .
docker run -p 8501:8501 nba-finals-predictor
```

## Future Improvements

- Player-level RAPM and lineup-adjusted team strength.
- Injury availability and minutes-impact modeling.
- Betting odds integration for calibration checks.
- Live playoff predictions with daily refresh jobs.
- Reinforcement learning for lineup optimization.
- LLM-generated matchup analysis grounded in model explanations.
