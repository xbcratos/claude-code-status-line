"""
Python utilities for the Claude Code Statusline Tool.

Provides functions for detecting Python version and virtual environment.
"""

import os
import sys
from pathlib import Path
from typing import Optional


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


def get_python_venv() -> str:
    """
    Get current Python virtual environment name.

    Checks VIRTUAL_ENV environment variable and extracts the venv name.

    Returns:
        Virtual environment name or empty string if not in a venv
    """
    venv_path = os.environ.get('VIRTUAL_ENV')
    if not venv_path:
        return ""

    try:
        # Extract the directory name as the venv name
        venv_name = Path(venv_path).name
        return venv_name
    except (ValueError, OSError):
        return ""
