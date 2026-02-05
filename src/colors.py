import os
from typing import Dict, Optional

COLORS: Dict[str, str] = {
    "cyan": "\033[96m",
    "green": "\033[92m",
    "blue": "\033[94m",
    "magenta": "\033[95m",
    "yellow": "\033[93m",
    "red": "\033[91m",
    "white": "\033[97m",
    "reset": "\033[0m"
}

# Module-level override for color state (set by statusline.py)
_color_override: Optional[bool] = None

def is_color_enabled() -> bool:
    """Check if colors should be used (respects NO_COLOR environment variable and override)."""
    # Check override first (set by statusline when config disables colors)
    if _color_override is not None:
        return _color_override
    # Fall back to NO_COLOR environment variable
    return os.environ.get("NO_COLOR") is None

def colorize(text: str, color_name: str) -> str:
    """Wrap text in ANSI color codes."""
    if not is_color_enabled():
        return text

    color_code = COLORS.get(color_name.lower(), "")
    reset_code = COLORS["reset"]

    if color_code:
        return f"{color_code}{text}{reset_code}"
    return text

def reset() -> str:
    """Return ANSI reset code."""
    return COLORS["reset"] if is_color_enabled() else ""
