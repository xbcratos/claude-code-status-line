"""Tests for statusline module."""
import json
import pytest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock
from io import StringIO

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from statusline import extract_data, main


class TestExtractData:
    """Tests for extract_data function."""

    def test_extract_model_id(self):
        """Test extracts model ID."""
        json_data = {"model": {"id": "claude-sonnet-4"}}
        config = {}
        result = extract_data(json_data, config)
        assert result["model"] == "claude-sonnet-4"

    def test_extract_model_fallback_to_display_name(self):
        """Test falls back to display_name when id not available."""
        json_data = {"model": {"display_name": "Sonnet 4"}}
        config = {}
        result = extract_data(json_data, config)
        assert result["model"] == "Sonnet 4"

    def test_extract_version(self):
        """Test extracts version."""
        json_data = {"version": "v1.0.85"}
        config = {}
        result = extract_data(json_data, config)
        assert result["version"] == "v1.0.85"

    def test_extract_context_remaining(self):
        """Test extracts context remaining percentage."""
        json_data = {
            "context_window": {
                "remaining_percentage": 85
            }
        }
        config = {}
        result = extract_data(json_data, config)
        assert result["context_remaining"] == 85

    def test_extract_total_tokens(self):
        """Test calculates total tokens from input and output."""
        json_data = {
            "context_window": {
                "total_input_tokens": 1000,
                "total_output_tokens": 500
            }
        }
        config = {}
        result = extract_data(json_data, config)
        assert result["tokens"] == 1500

    def test_extract_current_dir(self):
        """Test extracts current directory basename."""
        json_data = {
            "workspace": {
                "current_dir": "/path/to/my-project"
            }
        }
        config = {}
        result = extract_data(json_data, config)
        assert result["current_dir"] == "my-project"

    def test_extract_current_dir_root(self):
        """Test handles root directory."""
        json_data = {
            "workspace": {
                "current_dir": "/"
            }
        }
        config = {}
        result = extract_data(json_data, config)
        assert result["current_dir"] == "/"

    def test_extract_git_branch(self, tmp_path):
        """Test extracts git branch."""
        # Create a mock git repo
        git_dir = tmp_path / ".git"
        git_dir.mkdir()
        head_file = git_dir / "HEAD"
        head_file.write_text("ref: refs/heads/feature-branch\n")

        json_data = {
            "workspace": {
                "current_dir": str(tmp_path)
            }
        }
        config = {}
        result = extract_data(json_data, config)
        assert result["git_branch"] == "feature-branch"

    def test_extract_cost(self):
        """Test extracts cost."""
        json_data = {
            "cost": {
                "total_cost_usd": 2.48
            }
        }
        config = {}
        result = extract_data(json_data, config)
        assert result["cost"] == 2.48

    def test_extract_duration(self):
        """Test extracts duration."""
        json_data = {
            "cost": {
                "total_duration_ms": 120000
            }
        }
        config = {}
        result = extract_data(json_data, config)
        assert result["duration"] == 120000

    def test_calculate_cost_per_hour(self):
        """Test calculates cost per hour."""
        json_data = {
            "cost": {
                "total_cost_usd": 1.0,
                "total_duration_ms": 3600000  # 1 hour
            }
        }
        config = {}
        result = extract_data(json_data, config)
        assert result["cost_per_hour"] == 1.0

    def test_calculate_tokens_per_minute(self):
        """Test calculates tokens per minute."""
        json_data = {
            "context_window": {
                "total_input_tokens": 1000,
                "total_output_tokens": 500
            },
            "cost": {
                "total_duration_ms": 60000  # 1 minute
            }
        }
        config = {}
        result = extract_data(json_data, config)
        assert result["tokens_per_minute"] == 1500

    def test_extract_lines_changed(self):
        """Test calculates total lines changed."""
        json_data = {
            "cost": {
                "total_lines_added": 100,
                "total_lines_removed": 50
            }
        }
        config = {}
        result = extract_data(json_data, config)
        assert result["lines_changed"] == 150

    def test_extract_output_style(self):
        """Test extracts output style name."""
        json_data = {
            "output_style": {
                "name": "markdown"
            }
        }
        config = {}
        result = extract_data(json_data, config)
        assert result["output_style"] == "markdown"

    def test_extract_empty_data(self):
        """Test handles empty JSON gracefully."""
        json_data = {}
        config = {}
        result = extract_data(json_data, config)
        assert isinstance(result, dict)
        assert len(result) == 0


class TestMain:
    """Tests for main function."""

    def test_main_with_valid_input(self, monkeypatch, tmp_path):
        """Test main function with valid input."""
        monkeypatch.delenv("NO_COLOR", raising=False)

        # Mock stdin with valid JSON
        test_input = json.dumps({
            "model": {"id": "claude-sonnet-4"},
            "version": "v1.0.0",
            "workspace": {"current_dir": str(tmp_path)}
        })

        # Mock config location
        test_config_dir = tmp_path / "config"
        test_config_file = test_config_dir / "config.json"
        monkeypatch.setattr("config_manager.CONFIG_DIR", test_config_dir)
        monkeypatch.setattr("config_manager.CONFIG_FILE", test_config_file)

        with patch('sys.stdin', StringIO(test_input)):
            with patch('sys.stdout', new=StringIO()) as mock_stdout:
                main()
                output = mock_stdout.getvalue()
                assert len(output) > 0

    def test_main_with_invalid_json(self, monkeypatch, capsys):
        """Test main function handles invalid JSON."""
        with patch('sys.stdin', StringIO("invalid json")):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1

    def test_main_with_colors_disabled_in_config(self, monkeypatch, tmp_path):
        """Test main function respects enable_colors config."""
        monkeypatch.delenv("NO_COLOR", raising=False)

        test_input = json.dumps({
            "model": {"id": "claude-sonnet-4"}
        })

        # Create config with colors disabled
        test_config_dir = tmp_path / "config"
        test_config_dir.mkdir()
        test_config_file = test_config_dir / "config.json"

        from config_manager import get_default_config
        config = get_default_config()
        config["enable_colors"] = False

        with open(test_config_file, 'w') as f:
            json.dump(config, f)

        monkeypatch.setattr("config_manager.CONFIG_DIR", test_config_dir)
        monkeypatch.setattr("config_manager.CONFIG_FILE", test_config_file)

        with patch('sys.stdin', StringIO(test_input)):
            with patch('sys.stdout', new=StringIO()) as mock_stdout:
                main()
                output = mock_stdout.getvalue()
                # Output should not contain ANSI codes
                assert "\033[" not in output

    def test_main_with_no_color_env(self, monkeypatch, tmp_path):
        """Test main function respects NO_COLOR environment variable."""
        monkeypatch.setenv("NO_COLOR", "1")

        test_input = json.dumps({
            "model": {"id": "claude-sonnet-4"}
        })

        test_config_dir = tmp_path / "config"
        test_config_file = test_config_dir / "config.json"
        monkeypatch.setattr("config_manager.CONFIG_DIR", test_config_dir)
        monkeypatch.setattr("config_manager.CONFIG_FILE", test_config_file)

        with patch('sys.stdin', StringIO(test_input)):
            with patch('sys.stdout', new=StringIO()) as mock_stdout:
                main()
                output = mock_stdout.getvalue()
                # Output should not contain ANSI codes
                assert "\033[" not in output

    def test_main_compact_mode(self, monkeypatch, tmp_path):
        """Test main function uses compact mode by default."""
        monkeypatch.delenv("NO_COLOR", raising=False)

        test_input = json.dumps({
            "model": {"id": "claude-sonnet-4"},
            "version": "v1.0.0"
        })

        test_config_dir = tmp_path / "config"
        test_config_file = test_config_dir / "config.json"
        monkeypatch.setattr("config_manager.CONFIG_DIR", test_config_dir)
        monkeypatch.setattr("config_manager.CONFIG_FILE", test_config_file)

        with patch('sys.stdin', StringIO(test_input)):
            with patch('sys.stdout', new=StringIO()) as mock_stdout:
                main()
                output = mock_stdout.getvalue()
                # Compact mode shouldn't have labels like "Model:"
                assert "Model:" not in output

    def test_main_verbose_mode(self, monkeypatch, tmp_path):
        """Test main function uses verbose mode when configured."""
        monkeypatch.delenv("NO_COLOR", raising=False)

        test_input = json.dumps({
            "model": {"id": "claude-sonnet-4"},
            "version": "v1.0.0"
        })

        # Create config with verbose mode
        test_config_dir = tmp_path / "config"
        test_config_dir.mkdir()
        test_config_file = test_config_dir / "config.json"

        from config_manager import get_default_config
        config = get_default_config()
        config["display_mode"] = "verbose"

        with open(test_config_file, 'w') as f:
            json.dump(config, f)

        monkeypatch.setattr("config_manager.CONFIG_DIR", test_config_dir)
        monkeypatch.setattr("config_manager.CONFIG_FILE", test_config_file)

        with patch('sys.stdin', StringIO(test_input)):
            with patch('sys.stdout', new=StringIO()) as mock_stdout:
                main()
                output = mock_stdout.getvalue()
                # Verbose mode should have labels
                assert "Model:" in output
