"""Logging helpers used across pipelines and app code."""

from __future__ import annotations

import logging
import sys

from config.settings import settings


def get_logger(name: str) -> logging.Logger:
    """Return a configured application logger."""

    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(settings.log_level.upper())
    logger.propagate = False
    return logger
