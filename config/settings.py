"""Application settings for the NBA Finals Predictor."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:  # pragma: no cover - deployment can run without .env support
    load_dotenv = None

if load_dotenv is not None:
    load_dotenv()


@dataclass(frozen=True)
class AppSettings:
    """Runtime configuration loaded from environment variables."""

    app_name: str = "NBA Finals Predictor"
    season: str = "2025-26"
    season_type: str = "Playoffs"
    timeout_seconds: int = int(os.getenv("NBA_API_TIMEOUT_SECONDS", "30"))
    cache_dir: Path = Path(os.getenv("NBA_CACHE_DIR", "data/raw"))
    processed_dir: Path = Path("data/processed")
    model_dir: Path = Path("models/artifacts")
    log_level: str = os.getenv("NBA_LOG_LEVEL", "INFO")
    default_simulations: int = 10_000
    home_court_edge: float = 0.035


settings = AppSettings()
