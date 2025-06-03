"""
Core package for the AI Data Visualization Assistant.

This package contains the core functionality including the GenBI React Agent
and visualization tools.
"""

# Import key components to make them available at the package level
from .gen_bi_react_agent import GenBIReactAgent
from .viz_tools import VizTools

__all__ = ['GenBIReactAgent']
