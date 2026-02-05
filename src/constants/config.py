"""
Configuration-related constants for the Claude Code Statusline Tool.

Contains configuration keys, validation bounds, and default configuration values.
"""

from typing import Dict, List

# Import field names for default configuration
from .fields import (
    FIELD_MODEL,
    FIELD_VERSION,
    FIELD_CONTEXT_REMAINING,
    FIELD_TOKENS,
    FIELD_CURRENT_DIR,
    FIELD_GIT_BRANCH,
    FIELD_COST,
    FIELD_DURATION,
    FIELD_LINES_CHANGED,
    FIELD_OUTPUT_STYLE,
    FIELD_CPU_USAGE,
    FIELD_MEMORY_USAGE,
    FIELD_BATTERY,
    FIELD_PYTHON_VERSION,
    FIELD_PYTHON_VENV,
    FIELD_DATETIME,
)

# ============================================================================
# Configuration Keys
# ============================================================================

CONFIG_KEY_DISPLAY_MODE = "display_mode"
CONFIG_KEY_VISIBLE_FIELDS = "visible_fields"
CONFIG_KEY_FIELD_ORDER = "field_order"
CONFIG_KEY_ICONS = "icons"
CONFIG_KEY_COLORS = "colors"
CONFIG_KEY_SHOW_PROGRESS_BARS = "show_progress_bars"
CONFIG_KEY_PROGRESS_BAR_WIDTH = "progress_bar_width"
CONFIG_KEY_ENABLE_COLORS = "enable_colors"

# ============================================================================
# Progress Bar Settings
# ============================================================================

MIN_PROGRESS_BAR_WIDTH = 5
MAX_PROGRESS_BAR_WIDTH = 50
DEFAULT_PROGRESS_BAR_WIDTH = 10

# ============================================================================
# Default Configuration Values
# ============================================================================

DEFAULT_SHOW_PROGRESS_BARS = True
DEFAULT_ENABLE_COLORS = True

DEFAULT_VISIBLE_FIELDS: Dict[str, bool] = {
    FIELD_MODEL: True,
    FIELD_VERSION: True,
    FIELD_CONTEXT_REMAINING: True,
    FIELD_TOKENS: True,
    FIELD_CURRENT_DIR: True,
    FIELD_GIT_BRANCH: True,
    FIELD_COST: True,
    FIELD_DURATION: False,
    FIELD_LINES_CHANGED: False,
    FIELD_OUTPUT_STYLE: False,
    FIELD_CPU_USAGE: True,
    FIELD_MEMORY_USAGE: True,
    FIELD_BATTERY: True,
    FIELD_PYTHON_VERSION: True,
    FIELD_PYTHON_VENV: True,
    FIELD_DATETIME: True,
}

DEFAULT_FIELD_ORDER: List[str] = [
    FIELD_CURRENT_DIR,
    FIELD_GIT_BRANCH,
    FIELD_MODEL,
    FIELD_VERSION,
    FIELD_OUTPUT_STYLE,
    FIELD_PYTHON_VERSION,
    FIELD_DATETIME,
    FIELD_CONTEXT_REMAINING,
    FIELD_DURATION,
    FIELD_TOKENS,
    FIELD_COST,
    FIELD_LINES_CHANGED,
    FIELD_CPU_USAGE,
    FIELD_MEMORY_USAGE,
    FIELD_BATTERY,
    FIELD_PYTHON_VENV,
]
