#!/usr/bin/env python3
import sys
import json
import os
from pathlib import Path

# Require Python 3.6+
if sys.version_info < (3, 6):
    print("Error: Python 3.6 or higher is required", file=sys.stderr)
    print(f"Current version: {sys.version}", file=sys.stderr)
    sys.exit(1)

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from config_manager import load_config
from display_formatter import format_compact, format_verbose
from git_utils import get_git_branch
import colors

def extract_data(json_data, config):
    """Extract relevant fields from Claude Code JSON input."""
    data = {}

    # Model ID (more specific than display_name)
    if "model" in json_data:
        if "id" in json_data["model"]:
            data["model"] = json_data["model"]["id"]
        elif "display_name" in json_data["model"]:
            # Fallback to display_name if id not available
            data["model"] = json_data["model"]["display_name"]

    # Version
    if "version" in json_data:
        data["version"] = json_data["version"]

    # Context window
    if "context_window" in json_data:
        cw = json_data["context_window"]
        if "remaining_percentage" in cw:
            data["context_remaining"] = int(cw["remaining_percentage"])

        # Total tokens
        total_tokens = 0
        if "total_input_tokens" in cw:
            total_tokens += cw["total_input_tokens"]
        if "total_output_tokens" in cw:
            total_tokens += cw["total_output_tokens"]

        if total_tokens > 0:
            data["tokens"] = total_tokens

    # Workspace
    if "workspace" in json_data and "current_dir" in json_data["workspace"]:
        cwd = json_data["workspace"]["current_dir"]
        data["current_dir"] = os.path.basename(cwd) or cwd

        # Get git branch
        git_branch = get_git_branch(cwd)
        if git_branch:
            data["git_branch"] = git_branch

    # Cost
    if "cost" in json_data:
        cost_data = json_data["cost"]
        if "total_cost_usd" in cost_data:
            data["cost"] = cost_data["total_cost_usd"]

        if "total_duration_ms" in cost_data:
            duration_ms = cost_data["total_duration_ms"]
            data["duration"] = duration_ms

            # Calculate cost per hour
            if data.get("cost") and duration_ms > 0:
                duration_hours = duration_ms / (1000 * 60 * 60)
                data["cost_per_hour"] = data["cost"] / duration_hours if duration_hours > 0 else 0

            # Calculate tokens per minute
            if data.get("tokens") and duration_ms > 0:
                duration_minutes = duration_ms / (1000 * 60)
                data["tokens_per_minute"] = int(data["tokens"] / duration_minutes) if duration_minutes > 0 else 0

        # Lines changed
        lines_added = cost_data.get("total_lines_added", 0)
        lines_removed = cost_data.get("total_lines_removed", 0)
        if lines_added > 0 or lines_removed > 0:
            data["lines_changed"] = lines_added + lines_removed

    # Output style
    if "output_style" in json_data and "name" in json_data["output_style"]:
        data["output_style"] = json_data["output_style"]["name"]

    return data

def main():
    """Main entry point for statusline script."""
    try:
        # Read JSON from stdin
        input_data = sys.stdin.read()
        json_data = json.loads(input_data)

        # Load user config
        config = load_config()

        # Override color setting if NO_COLOR is set OR if disabled in config
        if not colors.is_color_enabled() or not config.get("enable_colors", True):
            # Temporarily disable colors in the colors module
            import os
            os.environ["NO_COLOR"] = "1"

        # Extract data from JSON
        data = extract_data(json_data, config)

        # Format output based on display mode
        display_mode = config.get("display_mode", "compact")

        if display_mode in ["large", "verbose"]:  # Support both names for compatibility
            output = format_verbose(data, config)
        else:
            output = format_compact(data, config)

        # Output to stdout
        print(output)

    except json.JSONDecodeError:
        print("Error: Invalid JSON input", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
