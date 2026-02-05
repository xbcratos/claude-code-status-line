"""Tests for config_manager module."""
import json
import pytest
import sys
from pathlib import Path
from unittest.mock import patch, mock_open

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from config_manager import (
    get_default_config,
    ensure_config_exists,
    load_config,
    save_config,
    CONFIG_FILE
)


class TestGetDefaultConfig:
    """Tests for get_default_config function."""

    def test_returns_dict(self):
        """Test returns a dictionary."""
        config = get_default_config()
        assert isinstance(config, dict)

    def test_has_required_keys(self):
        """Test default config has all required keys."""
        config = get_default_config()
        required_keys = [
            "display_mode",
            "visible_fields",
            "field_order",
            "icons",
            "colors",
            "show_progress_bars",
            "progress_bar_width",
            "enable_colors"
        ]
        for key in required_keys:
            assert key in config

    def test_visible_fields_structure(self):
        """Test visible_fields has correct structure."""
        config = get_default_config()
        visible = config["visible_fields"]
        assert isinstance(visible, dict)
        expected_fields = [
            "model", "version", "context_remaining", "tokens",
            "current_dir", "git_branch", "cost", "duration",
            "lines_changed", "output_style"
        ]
        for field in expected_fields:
            assert field in visible
            assert isinstance(visible[field], bool)

    def test_colors_structure(self):
        """Test colors config has correct structure."""
        config = get_default_config()
        colors = config["colors"]
        assert isinstance(colors, dict)
        # Check some key colors exist
        assert "directory" in colors
        assert "git_branch" in colors
        assert "progress_bar_filled" in colors


class TestEnsureConfigExists:
    """Tests for ensure_config_exists function."""

    def test_creates_directory(self, tmp_path, monkeypatch):
        """Test creates config directory if missing."""
        test_config_dir = tmp_path / "test_config"
        test_config_file = test_config_dir / "config.json"

        monkeypatch.setattr("config_manager.CONFIG_DIR", test_config_dir)
        monkeypatch.setattr("config_manager.CONFIG_FILE", test_config_file)

        ensure_config_exists()

        assert test_config_dir.exists()
        assert test_config_file.exists()

    def test_creates_default_config(self, tmp_path, monkeypatch):
        """Test creates default config file."""
        test_config_dir = tmp_path / "test_config"
        test_config_file = test_config_dir / "config.json"

        monkeypatch.setattr("config_manager.CONFIG_DIR", test_config_dir)
        monkeypatch.setattr("config_manager.CONFIG_FILE", test_config_file)

        ensure_config_exists()

        with open(test_config_file) as f:
            config = json.load(f)

        assert config == get_default_config()

    def test_does_not_overwrite_existing(self, tmp_path, monkeypatch):
        """Test doesn't overwrite existing config."""
        test_config_dir = tmp_path / "test_config"
        test_config_dir.mkdir()
        test_config_file = test_config_dir / "config.json"

        # Create custom config
        custom_config = {"custom": "value"}
        with open(test_config_file, 'w') as f:
            json.dump(custom_config, f)

        monkeypatch.setattr("config_manager.CONFIG_DIR", test_config_dir)
        monkeypatch.setattr("config_manager.CONFIG_FILE", test_config_file)

        ensure_config_exists()

        with open(test_config_file) as f:
            config = json.load(f)

        assert config == custom_config


class TestLoadConfig:
    """Tests for load_config function."""

    def test_loads_valid_config(self, tmp_path, monkeypatch):
        """Test loads valid config file."""
        test_config_dir = tmp_path / "test_config"
        test_config_dir.mkdir()
        test_config_file = test_config_dir / "config.json"

        config_data = get_default_config()
        config_data["display_mode"] = "verbose"

        with open(test_config_file, 'w') as f:
            json.dump(config_data, f)

        monkeypatch.setattr("config_manager.CONFIG_DIR", test_config_dir)
        monkeypatch.setattr("config_manager.CONFIG_FILE", test_config_file)

        loaded = load_config()
        assert loaded["display_mode"] == "verbose"

    def test_merges_with_defaults(self, tmp_path, monkeypatch):
        """Test merges partial config with defaults."""
        test_config_dir = tmp_path / "test_config"
        test_config_dir.mkdir()
        test_config_file = test_config_dir / "config.json"

        # Only set display_mode, missing other keys
        partial_config = {"display_mode": "verbose"}

        with open(test_config_file, 'w') as f:
            json.dump(partial_config, f)

        monkeypatch.setattr("config_manager.CONFIG_DIR", test_config_dir)
        monkeypatch.setattr("config_manager.CONFIG_FILE", test_config_file)

        loaded = load_config()

        # Should have custom value
        assert loaded["display_mode"] == "verbose"
        # Should have default values
        assert "visible_fields" in loaded
        assert "icons" in loaded

    def test_handles_invalid_json(self, tmp_path, monkeypatch):
        """Test handles invalid JSON gracefully."""
        test_config_dir = tmp_path / "test_config"
        test_config_dir.mkdir()
        test_config_file = test_config_dir / "config.json"

        # Write invalid JSON
        with open(test_config_file, 'w') as f:
            f.write("invalid json{{{")

        monkeypatch.setattr("config_manager.CONFIG_DIR", test_config_dir)
        monkeypatch.setattr("config_manager.CONFIG_FILE", test_config_file)

        loaded = load_config()

        # Should return default config
        assert loaded == get_default_config()

    def test_handles_missing_file(self, tmp_path, monkeypatch):
        """Test creates config if file doesn't exist."""
        test_config_dir = tmp_path / "test_config"
        test_config_file = test_config_dir / "config.json"

        monkeypatch.setattr("config_manager.CONFIG_DIR", test_config_dir)
        monkeypatch.setattr("config_manager.CONFIG_FILE", test_config_file)

        loaded = load_config()

        # Should create and return default
        assert loaded == get_default_config()
        assert test_config_file.exists()


class TestSaveConfig:
    """Tests for save_config function."""

    def test_saves_config(self, tmp_path, monkeypatch):
        """Test saves config to file."""
        test_config_dir = tmp_path / "test_config"
        test_config_file = test_config_dir / "config.json"

        monkeypatch.setattr("config_manager.CONFIG_DIR", test_config_dir)
        monkeypatch.setattr("config_manager.CONFIG_FILE", test_config_file)

        config = get_default_config()
        config["display_mode"] = "verbose"

        save_config(config)

        with open(test_config_file) as f:
            loaded = json.load(f)

        assert loaded["display_mode"] == "verbose"

    def test_creates_directory_if_missing(self, tmp_path, monkeypatch):
        """Test creates config directory when saving."""
        test_config_dir = tmp_path / "test_config"
        test_config_file = test_config_dir / "config.json"

        monkeypatch.setattr("config_manager.CONFIG_DIR", test_config_dir)
        monkeypatch.setattr("config_manager.CONFIG_FILE", test_config_file)

        assert not test_config_dir.exists()

        save_config(get_default_config())

        assert test_config_dir.exists()
        assert test_config_file.exists()
