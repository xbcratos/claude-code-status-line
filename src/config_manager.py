import json
import os
from pathlib import Path

CONFIG_DIR = Path.home() / ".claude-code-statusline"
CONFIG_FILE = CONFIG_DIR / "config.json"

def get_default_config():
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
            "progress_bar_filled": "green",
            "progress_bar_empty": "white",
            "separator": "white"
        },
        "show_progress_bars": True,
        "progress_bar_width": 10,
        "enable_colors": True
    }

def ensure_config_exists():
    """Create default config if missing."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    if not CONFIG_FILE.exists():
        save_config(get_default_config())

def load_config():
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

        return config
    except (json.JSONDecodeError, IOError):
        return get_default_config()

def save_config(config):
    """Save config to file."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)
