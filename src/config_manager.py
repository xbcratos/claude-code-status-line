import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, List

CONFIG_DIR = Path.home() / ".claude-code-statusline"
CONFIG_FILE = CONFIG_DIR / "config.json"

# Valid values for validation
VALID_COLORS = ["cyan", "green", "blue", "magenta", "yellow", "red", "white"]
VALID_DISPLAY_MODES = ["compact", "verbose", "large"]  # "large" is legacy alias for "verbose"
VALID_FIELD_NAMES = [
    "model", "version", "context_remaining", "tokens",
    "current_dir", "git_branch", "cost", "duration",
    "lines_changed", "output_style"
]
MIN_PROGRESS_BAR_WIDTH = 5
MAX_PROGRESS_BAR_WIDTH = 50

def get_default_config() -> Dict[str, Any]:
    """Return default configuration."""
    return {
        "display_mode": "compact",  # Options: "compact" or "verbose"
        "visible_fields": {
            "model": True,
            "version": True,
            "context_remaining": True,
            "tokens": True,
            "current_dir": True,
            "git_branch": True,
            "cost": True,
            "duration": False,
            "lines_changed": False,
            "output_style": False
        },
        "field_order": [
            "current_dir",
            "git_branch",
            "model",
            "version",
            "context_remaining",
            "tokens",
            "cost",
            "duration",
            "lines_changed",
            "output_style"
        ],
        "icons": {
            "directory": "📁",
            "git_branch": "🌿",
            "model": "🤖",
            "version": "📟",
            "context": "🧠",
            "cost": "💰",
            "tokens": "📊",
            "duration": "⌛",
            "style": "🎨"
        },
        "colors": {
            "directory": "cyan",
            "git_branch": "green",
            "model": "blue",
            "version": "magenta",
            "context": "yellow",
            "cost": "red",
            "tokens": "cyan",
            "duration": "magenta",
            "style": "blue",
            "lines_changed": "cyan",
            "progress_bar_filled": "green",
            "progress_bar_empty": "white",
            "separator": "white"
        },
        "show_progress_bars": True,
        "progress_bar_width": 10,
        "enable_colors": True
    }

def ensure_config_exists() -> None:
    """Create default config if missing."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    if not CONFIG_FILE.exists():
        save_config(get_default_config())

def validate_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and sanitize configuration values.

    Args:
        config: Configuration dictionary to validate

    Returns:
        Validated configuration with invalid values replaced by defaults
    """
    default_config = get_default_config()
    warnings = []

    # Validate display_mode
    if config.get("display_mode") not in VALID_DISPLAY_MODES:
        warnings.append(f"Invalid display_mode '{config.get('display_mode')}', using default 'compact'")
        config["display_mode"] = default_config["display_mode"]

    # Validate progress_bar_width
    if "progress_bar_width" in config:
        width = config["progress_bar_width"]
        if not isinstance(width, int) or width < MIN_PROGRESS_BAR_WIDTH or width > MAX_PROGRESS_BAR_WIDTH:
            warnings.append(
                f"Invalid progress_bar_width {width}, must be between {MIN_PROGRESS_BAR_WIDTH} and {MAX_PROGRESS_BAR_WIDTH}. "
                f"Using default {default_config['progress_bar_width']}"
            )
            config["progress_bar_width"] = default_config["progress_bar_width"]

    # Validate colors
    if "colors" in config:
        for field, color in config["colors"].items():
            if color not in VALID_COLORS:
                warnings.append(f"Invalid color '{color}' for field '{field}', using default")
                config["colors"][field] = default_config["colors"].get(field, "white")

    # Validate field_order
    if "field_order" in config:
        invalid_fields = [f for f in config["field_order"] if f not in VALID_FIELD_NAMES]
        if invalid_fields:
            warnings.append(f"Invalid field names in field_order: {', '.join(invalid_fields)}")
            config["field_order"] = [f for f in config["field_order"] if f in VALID_FIELD_NAMES]
            # Add any missing valid fields
            for field in VALID_FIELD_NAMES:
                if field not in config["field_order"]:
                    config["field_order"].append(field)

    # Print warnings if any
    if warnings:
        print("Configuration validation warnings:", file=sys.stderr)
        for warning in warnings:
            print(f"  - {warning}", file=sys.stderr)

    return config


def load_config() -> Dict[str, Any]:
    """Load config from ~/.claude-code-statusline/config.json."""
    ensure_config_exists()

    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)

        # Merge with defaults to handle missing keys
        default_config = get_default_config()
        for key, value in default_config.items():
            if key not in config:
                config[key] = value
            elif isinstance(value, dict):
                for subkey, subvalue in value.items():
                    if subkey not in config[key]:
                        config[key][subkey] = subvalue

        # Validate the loaded config
        config = validate_config(config)

        return config
    except json.JSONDecodeError as e:
        print(f"Warning: Config file contains invalid JSON: {e}", file=sys.stderr)
        print(f"Using default configuration instead.", file=sys.stderr)
        return get_default_config()
    except IOError as e:
        print(f"Warning: Could not read config file: {e}", file=sys.stderr)
        print(f"Using default configuration instead.", file=sys.stderr)
        return get_default_config()

def save_config(config: Dict[str, Any]) -> None:
    """Save config to file."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)
