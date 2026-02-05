"""Tests for colors module."""
import os
import pytest
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from colors import colorize, is_color_enabled, reset, COLORS


class TestColorize:
    """Tests for colorize function."""

    def test_colorize_with_colors_enabled(self, monkeypatch):
        """Test colorize adds ANSI codes when colors are enabled."""
        monkeypatch.delenv("NO_COLOR", raising=False)
        result = colorize("test", "cyan")
        assert result == f"{COLORS['cyan']}test{COLORS['reset']}"

    def test_colorize_with_colors_disabled(self, monkeypatch):
        """Test colorize returns plain text when NO_COLOR is set."""
        monkeypatch.setenv("NO_COLOR", "1")
        result = colorize("test", "cyan")
        assert result == "test"

    def test_colorize_invalid_color(self, monkeypatch):
        """Test colorize handles invalid color names gracefully."""
        monkeypatch.delenv("NO_COLOR", raising=False)
        result = colorize("test", "invalid_color")
        assert result == "test"

    def test_colorize_all_colors(self, monkeypatch):
        """Test all defined colors work correctly."""
        monkeypatch.delenv("NO_COLOR", raising=False)
        for color_name in ["cyan", "green", "blue", "magenta", "yellow", "red", "white"]:
            result = colorize("test", color_name)
            assert COLORS[color_name] in result
            assert COLORS["reset"] in result

    def test_colorize_empty_string(self, monkeypatch):
        """Test colorize handles empty strings."""
        monkeypatch.delenv("NO_COLOR", raising=False)
        result = colorize("", "cyan")
        assert result == f"{COLORS['cyan']}{COLORS['reset']}"


class TestIsColorEnabled:
    """Tests for is_color_enabled function."""

    def test_colors_enabled_by_default(self, monkeypatch):
        """Test colors are enabled when NO_COLOR is not set."""
        monkeypatch.delenv("NO_COLOR", raising=False)
        assert is_color_enabled() is True

    def test_colors_disabled_with_no_color(self, monkeypatch):
        """Test colors are disabled when NO_COLOR is set."""
        monkeypatch.setenv("NO_COLOR", "1")
        assert is_color_enabled() is False

    def test_colors_disabled_with_empty_no_color(self, monkeypatch):
        """Test colors are disabled even with empty NO_COLOR."""
        monkeypatch.setenv("NO_COLOR", "")
        assert is_color_enabled() is False


class TestReset:
    """Tests for reset function."""

    def test_reset_with_colors_enabled(self, monkeypatch):
        """Test reset returns ANSI code when colors are enabled."""
        monkeypatch.delenv("NO_COLOR", raising=False)
        assert reset() == COLORS["reset"]

    def test_reset_with_colors_disabled(self, monkeypatch):
        """Test reset returns empty string when colors are disabled."""
        monkeypatch.setenv("NO_COLOR", "1")
        assert reset() == ""
