"""
Display-related constants for the Claude Code Statusline Tool.

Contains display modes, line grouping, icons, time formatting,
and git settings.
"""

from typing import Dict

# Import field names for line assignment
from .fields import (
    FIELD_CURRENT_DIR,
    FIELD_GIT_BRANCH,
    FIELD_MODEL,
    FIELD_VERSION,
    FIELD_OUTPUT_STYLE,
    FIELD_CONTEXT_REMAINING,
    FIELD_DURATION,
    FIELD_COST,
    FIELD_TOKENS,
    FIELD_LINES_CHANGED,
    FIELD_CPU_USAGE,
    FIELD_MEMORY_USAGE,
    FIELD_BATTERY,
    FIELD_PYTHON_VERSION,
    FIELD_PYTHON_VENV,
    FIELD_DATETIME,
)

# ============================================================================
# Display Modes
# ============================================================================

DISPLAY_MODE_COMPACT = "compact"
DISPLAY_MODE_VERBOSE = "verbose"

VALID_DISPLAY_MODES = [
    DISPLAY_MODE_COMPACT,
    DISPLAY_MODE_VERBOSE,
]

DEFAULT_DISPLAY_MODE = DISPLAY_MODE_COMPACT

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
    FIELD_PYTHON_VERSION: LINE_IDENTITY,
    FIELD_DATETIME: LINE_IDENTITY,
    FIELD_CONTEXT_REMAINING: LINE_STATUS,
    FIELD_DURATION: LINE_STATUS,
    FIELD_COST: LINE_METRICS,
    FIELD_TOKENS: LINE_METRICS,
    FIELD_LINES_CHANGED: LINE_METRICS,
    FIELD_CPU_USAGE: LINE_METRICS,
    FIELD_MEMORY_USAGE: LINE_METRICS,
    FIELD_BATTERY: LINE_METRICS,
    FIELD_PYTHON_VENV: LINE_METRICS,
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
    "cpu": "💻",
    "memory": "🧮",
    "battery": "🔋",
    "python": "🐍",
    "datetime": "🕐",
}

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
GH_COMMAND_TIMEOUT_SECONDS = 2.0  # Longer timeout for gh API calls
GIT_HEAD_REF_PREFIX = "ref: refs/heads/"
GIT_DETACHED_HEAD_HASH_LENGTH = 7
