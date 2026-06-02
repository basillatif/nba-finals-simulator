"""Streamlit Community Cloud entrypoint."""

from __future__ import annotations

import runpy


runpy.run_module("app.Home", run_name="__main__")
