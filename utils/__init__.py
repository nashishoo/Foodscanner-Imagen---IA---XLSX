"""
Food Scanner - Utils Package
Contains logging and progress utilities
"""
from .logger import setup_logger
from .progress import ProgressTracker

__all__ = ["setup_logger", "ProgressTracker"]
