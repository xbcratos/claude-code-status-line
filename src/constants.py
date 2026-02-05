"""
Constants and configuration values for the Claude Code Statusline Tool.

This module centralizes all hardcoded values to improve maintainability
and make the codebase more configurable.
"""

from typing import Dict, List

# ============================================================================
# Field Names
# ============================================================================

FIELD_MODEL = "model"
FIELD_VERSION = "version"
FIELD_CONTEXT_REMAINING = "context_remaining"
FIELD_TOKENS = "tokens"
FIELD_CURRENT_DIR = "current_dir"
FIELD_GIT_BRANCH = "git_branch"
FIELD_COST = "cost"
FIELD_DURATION = "duration"
FIELD_LINES_CHANGED = "lines_changed"
FIELD_OUTPUT_STYLE = "output_style"

# Calculated/Rate Fields
FIELD_COST_PER_HOUR = "cost_per_hour"
FIELD_TOKENS_PER_MINUTE = "tokens_per_minute"

# Icon Keys (used for icon and color lookups in config)
ICON_KEY_DIRECTORY = "directory"
ICON_KEY_GIT_BRANCH = "git_branch"
ICON_KEY_MODEL = "model"
ICON_KEY_VERSION = "version"
ICON_KEY_STYLE = "style"
ICON_KEY_CONTEXT = "context"
ICON_KEY_DURATION = "duration"
ICON_KEY_COST = "cost"
ICON_KEY_TOKENS = "tokens"
ICON_KEY_LINES_CHANGED = "lines_changed"

# Configuration Keys
CONFIG_KEY_DISPLAY_MODE = "display_mode"
CONFIG_KEY_VISIBLE_FIELDS = "visible_fields"
CONFIG_KEY_FIELD_ORDER = "field_order"
CONFIG_KEY_ICONS = "icons"
CONFIG_KEY_COLORS = "colors"
CONFIG_KEY_SHOW_PROGRESS_BARS = "show_progress_bars"
CONFIG_KEY_PROGRESS_BAR_WIDTH = "progress_bar_width"
CONFIG_KEY_ENABLE_COLORS = "enable_colors"

# All valid field names in order
VALID_FIELD_NAMES: List[str] = [
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
]

# ============================================================================
# Display Modes
# ============================================================================

DISPLAY_MODE_COMPACT = "compact"
DISPLAY_MODE_VERBOSE = "verbose"

VALID_DISPLAY_MODES: List[str] = [
    DISPLAY_MODE_COMPACT,
    DISPLAY_MODE_VERBOSE,
]

# ============================================================================
# Line Grouping
# ============================================================================

LINE_IDENTITY = 1  # Directory, branch, model, version, style
LINE_STATUS = 2    # Context, duration
LINE_METRICS = 3   # Cost, tokens, lines changed

# Map fields to their display line
FIELD_LINE_ASSIGNMENT: Dict[str, int] = {
    FIELD_CURRENT_DIR: LINE_IDENTITY,
    FIELD_GIT_BRANCH: LINE_IDENTITY,
    FIELD_MODEL: LINE_IDENTITY,
    FIELD_VERSION: LINE_IDENTITY,
    FIELD_OUTPUT_STYLE: LINE_IDENTITY,
    FIELD_CONTEXT_REMAINING: LINE_STATUS,
    FIELD_DURATION: LINE_STATUS,
    FIELD_COST: LINE_METRICS,
    FIELD_TOKENS: LINE_METRICS,
    FIELD_LINES_CHANGED: LINE_METRICS,
}

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

# Default colors for fields
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
    "progress_bar_filled": COLOR_GREEN,
    "progress_bar_empty": COLOR_WHITE,
    "separator": COLOR_WHITE,
}

# ============================================================================
# Icons
# ============================================================================

DEFAULT_ICONS: Dict[str, str] = {
    "directory": "📁",
    "git_branch": "🌿",
    "model": "🤖",
    "version": "📟",
    "context": "🧠",
    "cost": "💰",
    "tokens": "📊",
    "duration": "⌛",
    "style": "🎨",
}

# ============================================================================
# Labels (for verbose mode)
# ============================================================================

FIELD_LABELS: Dict[str, str] = {
    FIELD_CURRENT_DIR: "Directory:",
    FIELD_GIT_BRANCH: "Git branch:",
    FIELD_MODEL: "Model:",
    FIELD_VERSION: "Version:",
    FIELD_OUTPUT_STYLE: "Style:",
    FIELD_CONTEXT_REMAINING: "Context remaining:",
    FIELD_DURATION: "Duration:",
    FIELD_COST: "Cost:",
    FIELD_TOKENS: "Tokens:",
    FIELD_LINES_CHANGED: "Lines changed:",
}

# ============================================================================
# Icon Keys (map field names to icon keys)
# ============================================================================

FIELD_ICON_KEYS: Dict[str, str] = {
    FIELD_CURRENT_DIR: "directory",
    FIELD_GIT_BRANCH: "git_branch",
    FIELD_MODEL: "model",
    FIELD_VERSION: "version",
    FIELD_CONTEXT_REMAINING: "context",
    FIELD_COST: "cost",
    FIELD_TOKENS: "tokens",
    FIELD_DURATION: "duration",
    FIELD_OUTPUT_STYLE: "style",
}

# ============================================================================
# Progress Bar Settings
# ============================================================================

MIN_PROGRESS_BAR_WIDTH = 5
MAX_PROGRESS_BAR_WIDTH = 50
DEFAULT_PROGRESS_BAR_WIDTH = 10

# ============================================================================
# Default Configuration Values
# ============================================================================

DEFAULT_DISPLAY_MODE = DISPLAY_MODE_COMPACT

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
}

DEFAULT_FIELD_ORDER: List[str] = [
    FIELD_CURRENT_DIR,
    FIELD_GIT_BRANCH,
    FIELD_MODEL,
    FIELD_VERSION,
    FIELD_CONTEXT_REMAINING,
    FIELD_TOKENS,
    FIELD_COST,
    FIELD_DURATION,
    FIELD_LINES_CHANGED,
    FIELD_OUTPUT_STYLE,
]

DEFAULT_SHOW_PROGRESS_BARS = True
DEFAULT_ENABLE_COLORS = True

# ============================================================================
# Time Formatting
# ============================================================================

MILLISECONDS_PER_SECOND = 1000
SECONDS_PER_MINUTE = 60
MINUTES_PER_HOUR = 60
MILLISECONDS_PER_MINUTE = MILLISECONDS_PER_SECOND * SECONDS_PER_MINUTE
MILLISECONDS_PER_HOUR = MILLISECONDS_PER_MINUTE * MINUTES_PER_HOUR

# ============================================================================
# Git Settings
# ============================================================================

GIT_COMMAND_TIMEOUT_SECONDS = 0.5
GIT_HEAD_REF_PREFIX = "ref: refs/heads/"
GIT_DETACHED_HEAD_HASH_LENGTH = 7
