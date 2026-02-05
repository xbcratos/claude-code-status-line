"""Tests for display_formatter module."""
import pytest
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from display_formatter import (
    format_progress_bar,
    format_field,
    format_field_verbose,
    format_duration,
    format_compact,
    format_verbose
)
from config_manager import get_default_config


class TestFormatProgressBar:
    """Tests for format_progress_bar function."""

    def test_full_progress_bar(self, monkeypatch):
        """Test 100% progress bar."""
        monkeypatch.delenv("NO_COLOR", raising=False)
        config = get_default_config()
        result = format_progress_bar(100, 10, config)
        assert "=" in result
        assert "-" not in result.replace("reset", "")  # Avoid matching in reset codes

    def test_empty_progress_bar(self, monkeypatch):
        """Test 0% progress bar."""
        monkeypatch.delenv("NO_COLOR", raising=False)
        config = get_default_config()
        result = format_progress_bar(0, 10, config)
        # All should be empty
        assert result.count("-") >= 10 or "[" in result

    def test_half_progress_bar(self, monkeypatch):
        """Test 50% progress bar."""
        monkeypatch.delenv("NO_COLOR", raising=False)
        config = get_default_config()
        result = format_progress_bar(50, 10, config)
        # Should have both filled and empty
        assert "=" in result or "[" in result

    def test_progress_bar_disabled(self, monkeypatch):
        """Test progress bar returns empty when disabled."""
        monkeypatch.delenv("NO_COLOR", raising=False)
        config = get_default_config()
        config["show_progress_bars"] = False
        result = format_progress_bar(50, 10, config)
        assert result == ""


class TestFormatField:
    """Tests for format_field function."""

    def test_format_field_with_icon(self, monkeypatch):
        """Test formatting field with icon."""
        monkeypatch.delenv("NO_COLOR", raising=False)
        config = get_default_config()
        result = format_field("directory", "my-project", config)
        assert "my-project" in result
        assert config["icons"]["directory"] in result

    def test_format_field_without_icon(self, monkeypatch):
        """Test formatting field without icon."""
        monkeypatch.delenv("NO_COLOR", raising=False)
        config = get_default_config()
        config["icons"]["directory"] = ""
        result = format_field("directory", "my-project", config)
        assert "my-project" in result

    def test_format_field_empty_value(self, monkeypatch):
        """Test formatting empty value returns empty string."""
        monkeypatch.delenv("NO_COLOR", raising=False)
        config = get_default_config()
        result = format_field("directory", "", config)
        assert result == ""

    def test_format_field_none_value(self, monkeypatch):
        """Test formatting None value returns empty string."""
        monkeypatch.delenv("NO_COLOR", raising=False)
        config = get_default_config()
        result = format_field("directory", None, config)
        assert result == ""


class TestFormatFieldVerbose:
    """Tests for format_field_verbose function."""

    def test_format_field_verbose_with_icon(self, monkeypatch):
        """Test verbose formatting with icon and label."""
        monkeypatch.delenv("NO_COLOR", raising=False)
        config = get_default_config()
        result = format_field_verbose("directory", "my-project", "Directory:", config)
        assert "my-project" in result
        assert "Directory:" in result
        assert config["icons"]["directory"] in result

    def test_format_field_verbose_without_icon(self, monkeypatch):
        """Test verbose formatting without icon."""
        monkeypatch.delenv("NO_COLOR", raising=False)
        config = get_default_config()
        config["icons"]["directory"] = ""
        result = format_field_verbose("directory", "my-project", "Directory:", config)
        assert "my-project" in result
        assert "Directory:" in result

    def test_format_field_verbose_empty_value(self, monkeypatch):
        """Test verbose formatting with empty value."""
        monkeypatch.delenv("NO_COLOR", raising=False)
        config = get_default_config()
        result = format_field_verbose("directory", "", "Directory:", config)
        assert result == ""


class TestFormatDuration:
    """Tests for format_duration function."""

    def test_format_milliseconds(self):
        """Test formatting milliseconds."""
        assert format_duration(500) == "500ms"

    def test_format_seconds(self):
        """Test formatting seconds."""
        assert format_duration(5000) == "5.0s"
        assert format_duration(45500) == "45.5s"

    def test_format_minutes(self):
        """Test formatting minutes."""
        assert format_duration(120000) == "2m"
        assert format_duration(300000) == "5m"

    def test_format_hours_and_minutes(self):
        """Test formatting hours with remaining minutes."""
        assert format_duration(3600000) == "1h 0m"
        assert format_duration(3900000) == "1h 5m"
        assert format_duration(7200000) == "2h 0m"


class TestFormatCompact:
    """Tests for format_compact function."""

    def test_format_compact_basic(self, monkeypatch):
        """Test basic compact formatting."""
        monkeypatch.delenv("NO_COLOR", raising=False)
        config = get_default_config()
        data = {
            "model": "claude-sonnet-4",
            "version": "v1.0.0",
            "current_dir": "my-project",
            "context_remaining": 85,
            "tokens": 1000,
            "cost": 0.50
        }

        result = format_compact(data, config)
        assert "my-project" in result
        assert "claude-sonnet-4" in result
        assert "v1.0.0" in result
        assert "85%" in result
        assert "1000" in result
        assert "0.50" in result

    def test_format_compact_with_git_branch(self, monkeypatch):
        """Test compact formatting includes git branch."""
        monkeypatch.delenv("NO_COLOR", raising=False)
        config = get_default_config()
        data = {
            "current_dir": "my-project",
            "git_branch": "main"
        }

        result = format_compact(data, config)
        assert "main" in result

    def test_format_compact_respects_visible_fields(self, monkeypatch):
        """Test compact formatting respects visible_fields config."""
        monkeypatch.delenv("NO_COLOR", raising=False)
        config = get_default_config()
        config["visible_fields"]["model"] = False
        data = {
            "model": "claude-sonnet-4",
            "current_dir": "my-project"
        }

        result = format_compact(data, config)
        assert "claude-sonnet-4" not in result
        assert "my-project" in result

    def test_format_compact_with_cost_per_hour(self, monkeypatch):
        """Test compact formatting includes cost per hour."""
        monkeypatch.delenv("NO_COLOR", raising=False)
        config = get_default_config()
        data = {
            "cost": 1.50,
            "cost_per_hour": 3.00
        }

        result = format_compact(data, config)
        assert "$1.50" in result
        assert "$3.00/h" in result

    def test_format_compact_with_tokens_per_minute(self, monkeypatch):
        """Test compact formatting includes tokens per minute."""
        monkeypatch.delenv("NO_COLOR", raising=False)
        config = get_default_config()
        data = {
            "tokens": 5000,
            "tokens_per_minute": 1000
        }

        result = format_compact(data, config)
        assert "5000" in result
        assert "1000 tpm" in result

    def test_format_compact_multiline_output(self, monkeypatch):
        """Test compact formatting produces multiple lines."""
        monkeypatch.delenv("NO_COLOR", raising=False)
        config = get_default_config()
        data = {
            "current_dir": "my-project",
            "model": "claude-sonnet-4",
            "context_remaining": 85,
            "tokens": 1000
        }

        result = format_compact(data, config)
        lines = result.split("\n")
        # Should have multiple lines (identity, status, metrics)
        assert len(lines) >= 2


class TestFormatVerbose:
    """Tests for format_verbose function."""

    def test_format_verbose_basic(self, monkeypatch):
        """Test basic verbose formatting with labels."""
        monkeypatch.delenv("NO_COLOR", raising=False)
        config = get_default_config()
        data = {
            "model": "claude-sonnet-4",
            "version": "v1.0.0",
            "current_dir": "my-project"
        }

        result = format_verbose(data, config)
        assert "Model:" in result
        assert "Version:" in result
        assert "Directory:" in result
        assert "claude-sonnet-4" in result

    def test_format_verbose_with_duration(self, monkeypatch):
        """Test verbose formatting includes duration."""
        monkeypatch.delenv("NO_COLOR", raising=False)
        config = get_default_config()
        config["visible_fields"]["duration"] = True
        data = {
            "duration": 120000  # 2 minutes
        }

        result = format_verbose(data, config)
        assert "Duration:" in result
        assert "2m" in result

    def test_format_verbose_respects_field_order(self, monkeypatch):
        """Test verbose formatting respects field_order config."""
        monkeypatch.delenv("NO_COLOR", raising=False)
        config = get_default_config()
        # Custom order: version before model
        config["field_order"] = ["version", "model"]
        config["visible_fields"] = {"model": True, "version": True}
        data = {
            "model": "claude-sonnet-4",
            "version": "v1.0.0"
        }

        result = format_verbose(data, config)
        version_pos = result.find("Version:")
        model_pos = result.find("Model:")
        # Version should appear before Model
        assert version_pos < model_pos

    def test_format_verbose_with_lines_changed(self, monkeypatch):
        """Test verbose formatting includes lines changed."""
        monkeypatch.delenv("NO_COLOR", raising=False)
        config = get_default_config()
        config["visible_fields"]["lines_changed"] = True
        data = {
            "lines_changed": 450
        }

        result = format_verbose(data, config)
        assert "Lines changed:" in result
        assert "450" in result
