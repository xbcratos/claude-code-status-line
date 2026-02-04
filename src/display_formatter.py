import os
from colors import colorize

def format_progress_bar(percentage, width, config):
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

def format_field(field_name, value, config):
    """Format individual fields with colors and icons."""
    if not value:
        return ""

    icon = config["icons"].get(field_name, "")
    color = config["colors"].get(field_name, "white")

    colored_value = colorize(str(value), color)

    if icon:
        return f"{icon} {colored_value}"
    return colored_value

def format_field_verbose(field_name, value, label, config):
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

def format_duration(duration_ms):
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

def format_compact(data, config):
    """Generate compact format statusline."""
    visible = config["visible_fields"]
    field_order = config.get("field_order", [])
    separator = colorize("  ", config["colors"].get("separator", "white"))

    # Group fields into lines based on semantic meaning
    line1_fields = []  # Identity: dir, branch, model, version, style
    line2_fields = []  # Status: context with progress bar
    line3_fields = []  # Metrics: cost, tokens, duration, lines

    # Define which line each field belongs to
    line_assignment = {
        "current_dir": 1,
        "git_branch": 1,
        "model": 1,
        "version": 1,
        "output_style": 1,
        "context_remaining": 2,
        "cost": 3,
        "tokens": 3,
        "duration": 3,
        "lines_changed": 3,
    }

    # Process fields in the user's configured order
    for field_name in field_order:
        if not visible.get(field_name) or not data.get(field_name):
            continue

        line_num = line_assignment.get(field_name, 3)

        # Format the field based on its type
        if field_name == "current_dir":
            formatted = format_field("directory", data["current_dir"], config)
        elif field_name == "git_branch":
            formatted = format_field("git_branch", data["git_branch"], config)
        elif field_name == "model":
            formatted = format_field("model", data["model"], config)
        elif field_name == "version":
            formatted = format_field("version", data["version"], config)
        elif field_name == "output_style":
            formatted = format_field("style", data["output_style"], config)
        elif field_name == "context_remaining":
            percentage = data["context_remaining"]
            progress_bar = format_progress_bar(percentage, config["progress_bar_width"], config)
            context_text = f"Context Remaining: {percentage}%"
            context_colored = colorize(context_text, config["colors"].get("context", "yellow"))
            formatted = f"{config['icons'].get('context', '🧠')} {context_colored} {progress_bar}"
        elif field_name == "cost":
            cost_str = f"${data['cost']:.2f}"
            if data.get("cost_per_hour") is not None:
                cost_str += f" (${data['cost_per_hour']:.2f}/h)"
            formatted = format_field("cost", cost_str, config)
        elif field_name == "tokens":
            tokens_str = f"{data['tokens']} tok"
            if data.get("tokens_per_minute") is not None:
                tokens_str += f" ({data['tokens_per_minute']} tpm)"
            formatted = format_field("tokens", tokens_str, config)
        elif field_name == "duration":
            duration_str = format_duration(data["duration"])
            formatted = format_field("duration", duration_str, config)
        elif field_name == "lines_changed":
            lines_str = f"{data['lines_changed']} lines"
            formatted = colorize(lines_str, config["colors"].get("tokens", "cyan"))
        else:
            continue

        # Add to appropriate line
        if line_num == 1:
            line1_fields.append(formatted)
        elif line_num == 2:
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

def format_verbose(data, config):
    """Generate verbose format statusline with labeled fields."""
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
    }

    # Group fields into lines based on semantic meaning
    line1_fields = []  # Identity: dir, branch, model, version, style
    line2_fields = []  # Status: context, duration
    line3_fields = []  # Metrics: cost, tokens, lines

    # Define which line each field belongs to (large mode shows duration on line 2)
    line_assignment = {
        "current_dir": 1,
        "git_branch": 1,
        "model": 1,
        "version": 1,
        "output_style": 1,
        "context_remaining": 2,
        "duration": 2,
        "cost": 3,
        "tokens": 3,
        "lines_changed": 3,
    }

    # Process fields in the user's configured order
    for field_name in field_order:
        if not visible.get(field_name) or not data.get(field_name):
            continue

        line_num = line_assignment.get(field_name, 3)

        # Format the field based on its type (verbose mode with labels)
        label = labels.get(field_name, "")

        if field_name == "current_dir":
            formatted = format_field_verbose("directory", data["current_dir"], label, config)
        elif field_name == "git_branch":
            formatted = format_field_verbose("git_branch", data["git_branch"], label, config)
        elif field_name == "model":
            formatted = format_field_verbose("model", data["model"], label, config)
        elif field_name == "version":
            formatted = format_field_verbose("version", data["version"], label, config)
        elif field_name == "output_style":
            formatted = format_field_verbose("style", data["output_style"], label, config)
        elif field_name == "context_remaining":
            percentage = data["context_remaining"]
            progress_bar = format_progress_bar(percentage, config["progress_bar_width"], config)
            base_formatted = format_field_verbose("context", f"{percentage}%", label, config)
            formatted = f"{base_formatted} {progress_bar}"
        elif field_name == "duration":
            duration_str = format_duration(data["duration"])
            formatted = format_field_verbose("duration", duration_str, label, config)
        elif field_name == "cost":
            cost_str = f"${data['cost']:.2f}"
            if data.get("cost_per_hour") is not None:
                cost_str += f" (${data['cost_per_hour']:.2f}/h)"
            formatted = format_field_verbose("cost", cost_str, label, config)
        elif field_name == "tokens":
            tokens_str = f"{data['tokens']} tok"
            if data.get("tokens_per_minute") is not None:
                tokens_str += f" ({data['tokens_per_minute']} tpm)"
            formatted = format_field_verbose("tokens", tokens_str, label, config)
        elif field_name == "lines_changed":
            lines_str = f"{data['lines_changed']} lines"
            formatted = format_field_verbose("tokens", lines_str, label, config)
        else:
            continue

        # Add to appropriate line
        if line_num == 1:
            line1_fields.append(formatted)
        elif line_num == 2:
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
