"""
Python utilities for the Claude Code Statusline Tool.

Provides functions for detecting Python version.
"""

import sys


def get_python_version() -> str:
    """
    Get current Python version.

    Returns:
        Python version string (e.g., "3.11.5") or empty string
    """
    try:
        version_info = sys.version_info
        return f"{version_info.major}.{version_info.minor}.{version_info.micro}"
    except AttributeError:
        return ""
