#!/usr/bin/env python3
"""
Installation helper script for Claude Code Statusline Tool.

This script provides helper functions for the install.sh script:
1. Create default configuration
2. Update Claude Code settings.json

This file is not installed to the user's directory - it's only used during installation.
"""

import json
import os
import sys
from pathlib import Path


def create_default_config(install_dir: str) -> int:
    """
    Create default configuration using config_manager.

    Args:
        install_dir: Path to the installation directory

    Returns:
        0 on success, 1 on failure
    """
    try:
        sys.path.insert(0, install_dir)
        from config_manager import ensure_config_exists
        ensure_config_exists()
        return 0
    except Exception as e:
        print(f"Warning: Could not create default config automatically: {e}", file=sys.stderr)
        print("It will be created on first run", file=sys.stderr)
        return 1


def update_claude_settings(settings_file: Path) -> int:
    """
    Update Claude Code settings.json with statusLine configuration.

    Args:
        settings_file: Path to the Claude Code settings.json file

    Returns:
        0 on success, 1 on failure
    """
    try:
        settings_dir = settings_file.parent

        # Create .claude directory if it doesn't exist
        settings_dir.mkdir(parents=True, exist_ok=True)

        # Load existing settings or create new ones
        if settings_file.exists():
            try:
                with open(settings_file, 'r') as f:
                    settings = json.load(f)
                print(f"✓ Loaded existing settings from {settings_file}")
            except json.JSONDecodeError:
                settings = {}
                print(f"Warning: Could not parse {settings_file}, creating new settings")
        else:
            settings = {}
            print(f"✓ Creating new settings file at {settings_file}")

        # Update statusLine configuration
        settings["statusLine"] = {
            "type": "command",
            "command": "~/.claude-code-statusline/statusline.py"
        }

        # Save settings
        with open(settings_file, 'w') as f:
            json.dump(settings, f, indent=2)

        print(f"✓ Updated statusLine configuration in {settings_file}")
        return 0

    except Exception as e:
        print(f"Error: Failed to update settings file: {e}", file=sys.stderr)
        return 1


def main():
    """
    Main entry point for the installation helper.

    Usage:
        python3 install_helper.py create-config <install_dir>
        python3 install_helper.py update-settings <settings_file>
    """
    if len(sys.argv) < 2:
        print("Usage: install_helper.py <command> [args]", file=sys.stderr)
        print("Commands:", file=sys.stderr)
        print("  create-config <install_dir>", file=sys.stderr)
        print("  update-settings <settings_file>", file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1]

    if command == "create-config":
        if len(sys.argv) < 3:
            print("Error: create-config requires install_dir argument", file=sys.stderr)
            sys.exit(1)
        install_dir = sys.argv[2]
        sys.exit(create_default_config(install_dir))

    elif command == "update-settings":
        if len(sys.argv) < 3:
            print("Error: update-settings requires settings_file argument", file=sys.stderr)
            sys.exit(1)
        settings_file = Path(sys.argv[2])
        sys.exit(update_claude_settings(settings_file))

    else:
        print(f"Error: Unknown command '{command}'", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
