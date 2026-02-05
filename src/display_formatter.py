"""
Display formatting for the Claude Code Statusline Tool.

This module uses the Field class hierarchy to format the statusline output.
Each field knows how to format itself, eliminating code duplication and
improving maintainability.
"""

from typing import Dict, Any, List
from colors import colorize
import constants
from fields import create_field_registry, Field
from models import StatusLineData, Configuration


# Create field registry (singleton pattern)
_field_registry: Dict[str, Field] = create_field_registry()


def get_field(field_name: str) -> Field:
    """
    Get a field instance by name.

    Args:
        field_name: Name of the field

    Returns:
        Field instance

    Raises:
        KeyError: If field not found
    """
    return _field_registry[field_name]


def format_statusline(
    data: Dict[str, Any],
    config: Dict[str, Any],
    verbose: bool = False
) -> str:
    """
    Format the statusline output.

    Args:
        data: Extracted data dictionary
        config: Configuration dictionary
        verbose: Whether to use verbose formatting

    Returns:
        Formatted statusline string
    """
    # Wrap dictionaries in typed models
    status_data = StatusLineData(data)
    configuration = Configuration(config)

    separator = colorize("  ", configuration.get_color("separator"))

    # Group fields by line
    line1_fields: List[str] = []  # Identity
    line2_fields: List[str] = []  # Status
    line3_fields: List[str] = []  # Metrics

    # Process fields in user's configured order
    for field_name in configuration.field_order:
        # Skip if field not visible
        if not configuration.is_field_visible(field_name):
            continue

        # Skip if field not in registry
        if field_name not in _field_registry:
            continue

        # Get field instance and format it
        field = get_field(field_name)
        formatted = field.format(data, config, verbose=verbose)

        if not formatted:
            continue

        # Add to appropriate line based on field's line assignment
        if field.line == constants.LINE_IDENTITY:
            line1_fields.append(formatted)
        elif field.line == constants.LINE_STATUS:
            line2_fields.append(formatted)
        else:  # LINE_METRICS
            line3_fields.append(formatted)

    # Build output lines
    lines = []
    if line1_fields:
        lines.append(separator.join(line1_fields))
    if line2_fields:
        lines.append(separator.join(line2_fields))
    if line3_fields:
        lines.append(separator.join(line3_fields))

    return "\n".join(lines)


def format_compact(data: Dict[str, Any], config: Dict[str, Any]) -> str:
    """
    Generate compact format statusline.

    Args:
        data: Extracted data dictionary
        config: Configuration dictionary

    Returns:
        Formatted statusline in compact mode
    """
    return format_statusline(data, config, verbose=False)


def format_verbose(data: Dict[str, Any], config: Dict[str, Any]) -> str:
    """
    Generate verbose format statusline with labeled fields.

    Args:
        data: Extracted data dictionary
        config: Configuration dictionary

    Returns:
        Formatted statusline in verbose mode
    """
    return format_statusline(data, config, verbose=True)


# ============================================================================
# Legacy Functions (for backward compatibility)
# ============================================================================

def format_progress_bar(percentage: int, width: int, config: Dict[str, Any]) -> str:
    """
    Create colored progress bar (legacy function for tests).

    Args:
        percentage: Progress percentage (0-100)
        width: Width of progress bar
        config: Configuration dictionary

    Returns:
        Formatted progress bar string
    """
    if not config.get("show_progress_bars", True):
        return ""

    filled_count = int((percentage / 100) * width)
    empty_count = width - filled_count

    filled_color = config["colors"].get("progress_bar_filled", constants.COLOR_GREEN)
    empty_color = config["colors"].get("progress_bar_empty", constants.COLOR_WHITE)
    separator_color = config["colors"].get("separator", constants.COLOR_WHITE)

    filled = colorize("=" * filled_count, filled_color)
    empty = colorize("-" * empty_count, empty_color)
    bracket_open = colorize("[", separator_color)
    bracket_close = colorize("]", separator_color)

    return f"{bracket_open}{filled}{empty}{bracket_close}"


def format_field(field_name: str, value: str, config: Dict[str, Any]) -> str:
    """
    Format individual fields with colors and icons (legacy function for tests).

    Args:
        field_name: Name of the field
        value: Field value
        config: Configuration dictionary

    Returns:
        Formatted field string
    """
    if not value:
        return ""

    icon = config["icons"].get(field_name, "")
    color = config["colors"].get(field_name, constants.COLOR_WHITE)

    colored_value = colorize(str(value), color)

    if icon:
        return f"{icon} {colored_value}"
    return colored_value


def format_field_verbose(
    field_name: str,
    value: str,
    label: str,
    config: Dict[str, Any]
) -> str:
    """
    Format individual fields with colors, icons, and labels (legacy function for tests).

    Args:
        field_name: Name of the field
        value: Field value
        label: Label for verbose mode
        config: Configuration dictionary

    Returns:
        Formatted field string
    """
    if not value:
        return ""

    icon = config["icons"].get(field_name, "")
    color = config["colors"].get(field_name, constants.COLOR_WHITE)

    # Colorize the label and value
    label_colored = colorize(label, config["colors"].get("separator", constants.COLOR_WHITE))
    value_colored = colorize(str(value), color)

    # Combine icon, label, and value
    if icon:
        return f"{icon} {label_colored} {value_colored}"
    return f"{label_colored} {value_colored}"


def format_duration(duration_ms: int) -> str:
    """
    Convert milliseconds to readable format (legacy function for tests).

    Args:
        duration_ms: Duration in milliseconds

    Returns:
        Human-readable duration string
    """
    if duration_ms < constants.MILLISECONDS_PER_SECOND:
        return f"{duration_ms}ms"

    seconds = duration_ms / constants.MILLISECONDS_PER_SECOND
    if seconds < constants.SECONDS_PER_MINUTE:
        return f"{seconds:.1f}s"

    minutes = int(seconds / constants.SECONDS_PER_MINUTE)
    hours = int(minutes / constants.MINUTES_PER_HOUR)

    if hours > 0:
        remaining_minutes = minutes % constants.MINUTES_PER_HOUR
        return f"{hours}h {remaining_minutes}m"

    return f"{minutes}m"
