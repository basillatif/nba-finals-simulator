"""Streamlit entrypoint for the NBA Finals Predictor app.

Running Streamlit against ``app/app.py`` makes Python treat that file as the
``app`` module, which shadows the package imports used by the project. This
launcher keeps the main page code in place while avoiding that name collision.
"""

from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
APP_DIR = Path(__file__).resolve().parent

if str(APP_DIR) in sys.path:
    sys.path.remove(str(APP_DIR))
sys.path = [path for path in sys.path if path != str(PROJECT_ROOT)]
sys.path.insert(0, str(PROJECT_ROOT))

if "app" in sys.modules and not hasattr(sys.modules["app"], "__path__"):
    del sys.modules["app"]

from app.app import *  # noqa: F401,F403,E402
