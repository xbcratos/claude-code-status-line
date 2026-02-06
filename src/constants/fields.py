"""
Field-related constants for the Claude Code Statusline Tool.

Contains field names, labels, icons, and line assignments for
all displayable fields in the statusline.
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

# System/Environment Fields
FIELD_CPU_USAGE = "cpu_usage"
FIELD_MEMORY_USAGE = "memory_usage"
FIELD_BATTERY = "battery"
FIELD_PYTHON_VERSION = "python_version"
FIELD_DATETIME = "datetime"

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

# System/Environment Icon Keys
ICON_KEY_CPU = "cpu"
ICON_KEY_MEMORY = "memory"
ICON_KEY_BATTERY = "battery"
ICON_KEY_PYTHON = "python"
ICON_KEY_DATETIME = "datetime"

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
    FIELD_CPU_USAGE,
    FIELD_MEMORY_USAGE,
    FIELD_BATTERY,
    FIELD_PYTHON_VERSION,
    FIELD_DATETIME,
]

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
    FIELD_CPU_USAGE: "CPU:",
    FIELD_MEMORY_USAGE: "Memory:",
    FIELD_BATTERY: "Battery:",
    FIELD_PYTHON_VERSION: "Python:",
    FIELD_DATETIME: "Time:",
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
    FIELD_CPU_USAGE: "cpu",
    FIELD_MEMORY_USAGE: "memory",
    FIELD_BATTERY: "battery",
    FIELD_PYTHON_VERSION: "python",
    FIELD_DATETIME: "datetime",
}
