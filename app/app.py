"""NBA Finals Predictor Streamlit application entrypoint."""

from __future__ import annotations

import runpy
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

runpy.run_module("app.Home", run_name="__main__")
