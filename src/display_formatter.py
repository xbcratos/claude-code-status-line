from typing import Dict, Any, Optional
from colors import colorize

# Constants for line grouping
LINE_IDENTITY = 1  # Directory, branch, model, version, style
LINE_STATUS = 2    # Context, duration
LINE_METRICS = 3   # Cost, tokens, lines changed

# Field to line assignment
FIELD_LINE_ASSIGNMENT = {
    "current_dir": LINE_IDENTITY,
    "git_branch": LINE_IDENTITY,
    "model": LINE_IDENTITY,
    "version": LINE_IDENTITY,
    "output_style": LINE_IDENTITY,
    "context_remaining": LINE_STATUS,
    "duration": LINE_STATUS,
    "cost": LINE_METRICS,
    "tokens": LINE_METRICS,
    "lines_changed": LINE_METRICS,
}


def format_progress_bar(percentage: int, width: int, config: Dict[str, Any]) -> str:
    """Create colored progress bar like [=========-]."""
    if not config.get("show_progress_bars", True):
        return ""

    filled_count = int((percentage / 100) * width)
    empty_count = width - filled_count

    filled_color = config["colors"].get("progress_bar_filled", "green")
    empty_color = config["colors"].get("progress_bar_empty", "white")
    separator_color = config["colors"].get("separator", "white")

    filled = colorize("=" * filled_count, filled_color)
    empty = colorize("-" * empty_count, empty_color)
    bracket_open = colorize("[", separator_color)
    bracket_close = colorize("]", separator_color)

    return f"{bracket_open}{filled}{empty}{bracket_close}"


def format_field(field_name: str, value: str, config: Dict[str, Any]) -> str:
    """Format individual fields with colors and icons."""
    if not value:
        return ""

    icon = config["icons"].get(field_name, "")
    color = config["colors"].get(field_name, "white")

    colored_value = colorize(str(value), color)

    if icon:
        return f"{icon} {colored_value}"
    return colored_value


def format_field_verbose(field_name: str, value: str, label: str, config: Dict[str, Any]) -> str:
    """Format individual fields with colors, icons, and labels for verbose mode."""
    if not value:
        return ""

    icon = config["icons"].get(field_name, "")
    color = config["colors"].get(field_name, "white")

    # Colorize the label and value
    label_colored = colorize(label, config["colors"].get("separator", "white"))
    value_colored = colorize(str(value), color)

    # Combine icon, label, and value
    if icon:
        return f"{icon} {label_colored} {value_colored}"
    return f"{label_colored} {value_colored}"


def format_duration(duration_ms: int) -> str:
    """Convert milliseconds to readable format."""
    if duration_ms < 1000:
        return f"{duration_ms}ms"

    seconds = duration_ms / 1000
    if seconds < 60:
        return f"{seconds:.1f}s"

    minutes = int(seconds / 60)
    hours = int(minutes / 60)

    if hours > 0:
        remaining_minutes = minutes % 60
        return f"{hours}h {remaining_minutes}m"

    return f"{minutes}m"


def _get_formatted_field_value(field_name, data, config, verbose=False, labels=None):
    """
    Get formatted value for a specific field.

    Args:
        field_name: Name of the field to format
        data: Data dictionary containing field values
        config: Configuration dictionary
        verbose: Whether to use verbose formatting with labels
        labels: Dictionary of labels for verbose mode

    Returns:
        Formatted string for the field, or empty string if field not available
    """
    if not data.get(field_name):
        return ""

    # Special handling for different field types
    if field_name == "current_dir":
        if verbose and labels:
            return format_field_verbose("directory", data["current_dir"], labels.get("current_dir", ""), config)
        return format_field("directory", data["current_dir"], config)

    elif field_name == "git_branch":
        if verbose and labels:
            return format_field_verbose("git_branch", data["git_branch"], labels.get("git_branch", ""), config)
        return format_field("git_branch", data["git_branch"], config)

    elif field_name == "model":
        if verbose and labels:
            return format_field_verbose("model", data["model"], labels.get("model", ""), config)
        return format_field("model", data["model"], config)

    elif field_name == "version":
        if verbose and labels:
            return format_field_verbose("version", data["version"], labels.get("version", ""), config)
        return format_field("version", data["version"], config)

    elif field_name == "output_style":
        if verbose and labels:
            return format_field_verbose("style", data["output_style"], labels.get("output_style", ""), config)
        return format_field("style", data["output_style"], config)

    elif field_name == "context_remaining":
        percentage = data["context_remaining"]
        progress_bar = format_progress_bar(percentage, config["progress_bar_width"], config)

        if verbose and labels:
            base_formatted = format_field_verbose("context", f"{percentage}%", labels.get("context_remaining", ""), config)
            return f"{base_formatted} {progress_bar}"
        else:
            context_text = f"Context Remaining: {percentage}%"
            context_colored = colorize(context_text, config["colors"].get("context", "yellow"))
            return f"{config['icons'].get('context', '🧠')} {context_colored} {progress_bar}"

    elif field_name == "duration":
        duration_str = format_duration(data["duration"])
        if verbose and labels:
            return format_field_verbose("duration", duration_str, labels.get("duration", ""), config)
        return format_field("duration", duration_str, config)

    elif field_name == "cost":
        cost_str = f"${data['cost']:.2f}"
        if data.get("cost_per_hour") is not None:
            cost_str += f" (${data['cost_per_hour']:.2f}/h)"

        if verbose and labels:
            return format_field_verbose("cost", cost_str, labels.get("cost", ""), config)
        return format_field("cost", cost_str, config)

    elif field_name == "tokens":
        tokens_str = f"{data['tokens']} tok"
        if data.get("tokens_per_minute") is not None:
            tokens_str += f" ({data['tokens_per_minute']} tpm)"

        if verbose and labels:
            return format_field_verbose("tokens", tokens_str, labels.get("tokens", ""), config)
        return format_field("tokens", tokens_str, config)

    elif field_name == "lines_changed":
        lines_str = f"{data['lines_changed']} lines"
        if verbose and labels:
            return format_field_verbose("lines_changed", lines_str, labels.get("lines_changed", ""), config)
        return colorize(lines_str, config["colors"].get("lines_changed", "cyan"))

    return ""


def _format_output(data, config, verbose=False):
    """
    Common formatting logic for both compact and verbose modes.

    Args:
        data: Data dictionary to format
        config: Configuration dictionary
        verbose: Whether to use verbose mode with labels

    Returns:
        Formatted string with multiple lines
    """
    visible = config["visible_fields"]
    field_order = config.get("field_order", [])
    separator = colorize("  ", config["colors"].get("separator", "white"))

    # Labels for verbose mode
    labels = {
        "current_dir": "Directory:",
        "git_branch": "Git branch:",
        "model": "Model:",
        "version": "Version:",
        "output_style": "Style:",
        "context_remaining": "Context remaining:",
        "duration": "Duration:",
        "cost": "Cost:",
        "tokens": "Tokens:",
        "lines_changed": "Lines changed:",
    } if verbose else None

    # Group fields into lines
    line1_fields = []  # Identity
    line2_fields = []  # Status
    line3_fields = []  # Metrics

    # Process fields in the user's configured order
    for field_name in field_order:
        if not visible.get(field_name):
            continue

        formatted = _get_formatted_field_value(field_name, data, config, verbose, labels)
        if not formatted:
            continue

        # Assign to appropriate line
        line_num = FIELD_LINE_ASSIGNMENT.get(field_name, LINE_METRICS)
        if line_num == LINE_IDENTITY:
            line1_fields.append(formatted)
        elif line_num == LINE_STATUS:
            line2_fields.append(formatted)
        else:
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
    """Generate compact format statusline."""
    return _format_output(data, config, verbose=False)


def format_verbose(data: Dict[str, Any], config: Dict[str, Any]) -> str:
    """Generate verbose format statusline with labeled fields."""
    return _format_output(data, config, verbose=True)
