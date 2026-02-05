"""
Field classes for the Claude Code Statusline Tool.

This module provides an object-oriented approach to field formatting,
where each field knows how to format itself based on display mode.
"""

from typing import Dict, Any, Optional
from abc import ABC, abstractmethod

from colors import colorize
import constants


class Field(ABC):
    """
    Base class for all statusline fields.

    Each field knows:
    - Its name
    - How to format itself in compact and verbose modes
    - Which line it belongs to
    - Its icon and color
    """

    def __init__(
        self,
        name: str,
        icon_key: str,
        line: int,
        label: str = "",
        color_key: Optional[str] = None
    ):
        """
        Initialize a field.

        Args:
            name: Field name (from constants)
            icon_key: Key for icon lookup in config
            line: Line number for display grouping
            label: Label for verbose mode
            color_key: Key for color lookup (defaults to icon_key)
        """
        self.name = name
        self.icon_key = icon_key
        self.line = line
        self.label = label
        self.color_key = color_key or icon_key

    @abstractmethod
    def format_value(self, data: Dict[str, Any], config: Dict[str, Any]) -> str:
        """
        Format the field's value from raw data.

        Args:
            data: Extracted data dictionary
            config: Configuration dictionary

        Returns:
            Formatted value string
        """
        pass

    def format_compact(self, data: Dict[str, Any], config: Dict[str, Any]) -> str:
        """Format field in compact mode (icon + value)."""
        value = self.format_value(data, config)
        if not value:
            return ""

        icon = config["icons"].get(self.icon_key, "")
        color = config["colors"].get(self.color_key, constants.COLOR_WHITE)
        colored_value = colorize(value, color)

        if icon:
            return f"{icon} {colored_value}"
        return colored_value

    def format_verbose(self, data: Dict[str, Any], config: Dict[str, Any]) -> str:
        """Format field in verbose mode (icon + label + value)."""
        value = self.format_value(data, config)
        if not value:
            return ""

        icon = config["icons"].get(self.icon_key, "")
        color = config["colors"].get(self.color_key, constants.COLOR_WHITE)
        separator_color = config["colors"].get("separator", constants.COLOR_WHITE)

        label_colored = colorize(self.label, separator_color)
        value_colored = colorize(value, color)

        if icon:
            return f"{icon} {label_colored} {value_colored}"
        return f"{label_colored} {value_colored}"

    def format(
        self,
        data: Dict[str, Any],
        config: Dict[str, Any],
        verbose: bool = False
    ) -> str:
        """
        Format the field based on display mode.

        Args:
            data: Extracted data dictionary
            config: Configuration dictionary
            verbose: Whether to use verbose formatting

        Returns:
            Formatted field string
        """
        if verbose:
            return self.format_verbose(data, config)
        return self.format_compact(data, config)


class SimpleField(Field):
    """
    A simple field that displays a value directly.

    Examples: model, version, directory, git_branch
    """

    def format_value(self, data: Dict[str, Any], config: Dict[str, Any]) -> str:
        """Return the field value as-is from data."""
        return str(data.get(self.name, "")) if data.get(self.name) else ""


class ProgressField(Field):
    """
    A field that displays a percentage with an optional progress bar.

    Example: context_remaining
    """

    def format_value(self, data: Dict[str, Any], config: Dict[str, Any]) -> str:
        """Format percentage value."""
        percentage = data.get(self.name)
        if percentage is None:
            return ""
        return f"{percentage}%"

    def _format_progress_bar(
        self,
        percentage: int,
        width: int,
        config: Dict[str, Any]
    ) -> str:
        """Create a colored progress bar."""
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

    def format_compact(self, data: Dict[str, Any], config: Dict[str, Any]) -> str:
        """Format with progress bar in compact mode."""
        percentage = data.get(self.name)
        if percentage is None:
            return ""

        icon = config["icons"].get(self.icon_key, "")
        color = config["colors"].get(self.color_key, constants.COLOR_YELLOW)

        # Use label from constants, capitalize first letter of second word for display
        label_text = self.label.replace("Context remaining:", "Context Remaining:")
        context_text = f"{label_text} {percentage}%"
        context_colored = colorize(context_text, color)
        progress_bar = self._format_progress_bar(
            percentage,
            config[constants.CONFIG_KEY_PROGRESS_BAR_WIDTH],
            config
        )

        return f"{icon} {context_colored} {progress_bar}"

    def format_verbose(self, data: Dict[str, Any], config: Dict[str, Any]) -> str:
        """Format with progress bar in verbose mode."""
        percentage = data.get(self.name)
        if percentage is None:
            return ""

        # Use parent class verbose formatting for base text
        base_formatted = super().format_verbose(data, config)
        progress_bar = self._format_progress_bar(
            percentage,
            config["progress_bar_width"],
            config
        )

        return f"{base_formatted} {progress_bar}"


class MetricField(Field):
    """
    A field that displays a metric with optional rate information.

    Examples: tokens (with tpm), cost (with cost per hour)
    """

    def __init__(
        self,
        name: str,
        icon_key: str,
        line: int,
        label: str = "",
        color_key: Optional[str] = None,
        rate_field: Optional[str] = None,
        rate_format: str = ""
    ):
        """
        Initialize a metric field.

        Args:
            name: Field name
            icon_key: Icon key
            line: Line number
            label: Verbose mode label
            color_key: Color key
            rate_field: Name of the rate field in data (e.g., "tokens_per_minute")
            rate_format: Format string for rate (e.g., "({value} tpm)")
        """
        super().__init__(name, icon_key, line, label, color_key)
        self.rate_field = rate_field
        self.rate_format = rate_format

    def format_value(self, data: Dict[str, Any], config: Dict[str, Any]) -> str:
        """Format metric value with optional rate."""
        value = data.get(self.name)
        if value is None:
            return ""

        # Format main value
        if self.name == constants.FIELD_COST:
            formatted = f"${value:.2f}"
        elif self.name == constants.FIELD_TOKENS:
            formatted = f"{value} tok"
        elif self.name == constants.FIELD_LINES_CHANGED:
            formatted = f"{value} lines"
        else:
            formatted = str(value)

        # Add rate if available
        if self.rate_field:
            rate_value = data.get(self.rate_field)
            if rate_value is not None:
                if self.name == constants.FIELD_COST:
                    formatted += f" (${rate_value:.2f}/h)"
                elif self.name == constants.FIELD_TOKENS:
                    formatted += f" ({rate_value} tpm)"

        return formatted


class DurationField(Field):
    """
    A field that formats duration in milliseconds to human-readable format.

    Example: duration
    """

    def format_value(self, data: Dict[str, Any], config: Dict[str, Any]) -> str:
        """Format duration from milliseconds to human-readable format."""
        duration_ms = data.get(self.name)
        if duration_ms is None:
            return ""

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


# ============================================================================
# Field Registry
# ============================================================================

def create_field_registry() -> Dict[str, Field]:
    """
    Create a registry of all available fields.

    Returns:
        Dictionary mapping field names to Field instances
    """
    return {
        constants.FIELD_CURRENT_DIR: SimpleField(
            name=constants.FIELD_CURRENT_DIR,
            icon_key=constants.ICON_KEY_DIRECTORY,
            line=constants.LINE_IDENTITY,
            label=constants.FIELD_LABELS[constants.FIELD_CURRENT_DIR]
        ),
        constants.FIELD_GIT_BRANCH: SimpleField(
            name=constants.FIELD_GIT_BRANCH,
            icon_key=constants.ICON_KEY_GIT_BRANCH,
            line=constants.LINE_IDENTITY,
            label=constants.FIELD_LABELS[constants.FIELD_GIT_BRANCH]
        ),
        constants.FIELD_MODEL: SimpleField(
            name=constants.FIELD_MODEL,
            icon_key=constants.ICON_KEY_MODEL,
            line=constants.LINE_IDENTITY,
            label=constants.FIELD_LABELS[constants.FIELD_MODEL]
        ),
        constants.FIELD_VERSION: SimpleField(
            name=constants.FIELD_VERSION,
            icon_key=constants.ICON_KEY_VERSION,
            line=constants.LINE_IDENTITY,
            label=constants.FIELD_LABELS[constants.FIELD_VERSION]
        ),
        constants.FIELD_OUTPUT_STYLE: SimpleField(
            name=constants.FIELD_OUTPUT_STYLE,
            icon_key=constants.ICON_KEY_STYLE,
            line=constants.LINE_IDENTITY,
            label=constants.FIELD_LABELS[constants.FIELD_OUTPUT_STYLE]
        ),
        constants.FIELD_CONTEXT_REMAINING: ProgressField(
            name=constants.FIELD_CONTEXT_REMAINING,
            icon_key=constants.ICON_KEY_CONTEXT,
            line=constants.LINE_STATUS,
            label=constants.FIELD_LABELS[constants.FIELD_CONTEXT_REMAINING]
        ),
        constants.FIELD_DURATION: DurationField(
            name=constants.FIELD_DURATION,
            icon_key=constants.ICON_KEY_DURATION,
            line=constants.LINE_STATUS,
            label=constants.FIELD_LABELS[constants.FIELD_DURATION]
        ),
        constants.FIELD_COST: MetricField(
            name=constants.FIELD_COST,
            icon_key=constants.ICON_KEY_COST,
            line=constants.LINE_METRICS,
            label=constants.FIELD_LABELS[constants.FIELD_COST],
            rate_field=constants.FIELD_COST_PER_HOUR
        ),
        constants.FIELD_TOKENS: MetricField(
            name=constants.FIELD_TOKENS,
            icon_key=constants.ICON_KEY_TOKENS,
            line=constants.LINE_METRICS,
            label=constants.FIELD_LABELS[constants.FIELD_TOKENS],
            rate_field=constants.FIELD_TOKENS_PER_MINUTE
        ),
        constants.FIELD_LINES_CHANGED: MetricField(
            name=constants.FIELD_LINES_CHANGED,
            icon_key=constants.ICON_KEY_TOKENS,  # Uses tokens icon/color by default
            line=constants.LINE_METRICS,
            label=constants.FIELD_LABELS[constants.FIELD_LINES_CHANGED],
            color_key=constants.ICON_KEY_LINES_CHANGED
        ),
    }
