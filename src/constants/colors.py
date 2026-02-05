"""
Color-related constants for the Claude Code Statusline Tool.

Contains color definitions, valid colors list, and default color
assignments for fields.
"""

from typing import Dict, List

# Import field names for default colors mapping
from .fields import (
    FIELD_CURRENT_DIR,
    FIELD_GIT_BRANCH,
    FIELD_MODEL,
    FIELD_VERSION,
    FIELD_CONTEXT_REMAINING,
    FIELD_COST,
    FIELD_TOKENS,
    FIELD_DURATION,
    FIELD_OUTPUT_STYLE,
    FIELD_LINES_CHANGED,
    FIELD_CPU_USAGE,
    FIELD_MEMORY_USAGE,
    FIELD_BATTERY,
    FIELD_PYTHON_VERSION,
    FIELD_PYTHON_VENV,
    FIELD_DATETIME,
)

# ============================================================================
# Colors
# ============================================================================

COLOR_CYAN = "cyan"
COLOR_GREEN = "green"
COLOR_BLUE = "blue"
COLOR_MAGENTA = "magenta"
COLOR_YELLOW = "yellow"
COLOR_RED = "red"
COLOR_WHITE = "white"

VALID_COLORS: List[str] = [
    COLOR_CYAN,
    COLOR_GREEN,
    COLOR_BLUE,
    COLOR_MAGENTA,
    COLOR_YELLOW,
    COLOR_RED,
    COLOR_WHITE,
]

# ============================================================================
# Default Colors
# ============================================================================

DEFAULT_COLORS: Dict[str, str] = {
    FIELD_CURRENT_DIR: COLOR_CYAN,
    FIELD_GIT_BRANCH: COLOR_GREEN,
    FIELD_MODEL: COLOR_BLUE,
    FIELD_VERSION: COLOR_MAGENTA,
    FIELD_CONTEXT_REMAINING: COLOR_YELLOW,
    FIELD_COST: COLOR_RED,
    FIELD_TOKENS: COLOR_CYAN,
    FIELD_DURATION: COLOR_MAGENTA,
    FIELD_OUTPUT_STYLE: COLOR_BLUE,
    FIELD_LINES_CHANGED: COLOR_CYAN,
    FIELD_CPU_USAGE: COLOR_BLUE,
    FIELD_MEMORY_USAGE: COLOR_MAGENTA,
    FIELD_BATTERY: COLOR_GREEN,
    FIELD_PYTHON_VERSION: COLOR_YELLOW,
    FIELD_PYTHON_VENV: COLOR_CYAN,
    FIELD_DATETIME: COLOR_WHITE,
    "progress_bar_filled": COLOR_GREEN,
    "progress_bar_empty": COLOR_WHITE,
    "separator": COLOR_WHITE,
}
