"""
Stats Generator Module
Provides modular API fetching, data calculation, and SVG rendering for GitHub profile stats.
"""

from .config import GITHUB_API, USERNAME, TOKEN, START_DATE, TOP_LANG_COUNT, LANG_COLORS
from .api import fetch_contributions_and_user, fetch_all_repo_language_sizes
from .utils import compute_streaks, parse_iso_date
from .renderers import (
    render_header_banner,
    render_profile_overview,
    render_top_langs,
    render_streaks,
    render_activity_radar,
    render_productive_time,
    display_svg
)

__all__ = [
    "GITHUB_API",
    "USERNAME",
    "TOKEN",
    "START_DATE",
    "TOP_LANG_COUNT",
    "LANG_COLORS",
    "fetch_contributions_and_user",
    "fetch_all_repo_language_sizes",
    "compute_streaks",
    "parse_iso_date",
    "render_header_banner",
    "render_profile_overview",
    "render_top_langs",
    "render_streaks",
    "render_activity_radar",
    "render_productive_time",
    "display_svg"
]
