"""
Integration tests for the Claude Code Statusline Tool.

Tests complete end-to-end functionality including:
- Full statusline output with icons in compact and verbose modes
- Installation helper functionality
- Complete workflow from JSON input to formatted output
"""

import json
import os
import sys
import tempfile
from pathlib import Path
from io import StringIO

import pytest

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from config_manager import get_default_config
from display_formatter import format_compact, format_verbose
import statusline


class TestFullStatuslineOutput:
    """Test complete statusline output with all fields and icons."""

    def test_full_compact_mode_with_icons(self, monkeypatch):
        """Test complete compact mode output with all fields and icons."""
        monkeypatch.delenv("NO_COLOR", raising=False)

        config = get_default_config()
        # Enable all fields
        for field in config["visible_fields"]:
            config["visible_fields"][field] = True

        # Complete dataset
        data = {
            "model": "claude-sonnet-4-5-20250929",
            "version": "v1.0.85",
            "current_dir": "my-project",
            "git_branch": "main",
            "output_style": "markdown",
            "context_remaining": 85,
            "duration": 1800000,  # 30 minutes
            "tokens": 75000,
            "tokens_per_minute": 2500,
            "cost": 12.50,
            "cost_per_hour": 25.00,
            "lines_changed": 150
        }

        result = format_compact(data, config)

        # Verify structure: should have 3 lines
        lines = result.split("\n")
        assert len(lines) == 3, f"Expected 3 lines, got {len(lines)}"

        # Line 1: Identity (directory, branch, model, version, style)
        line1 = lines[0]
        assert "📁" in line1, "Missing directory icon"
        assert "my-project" in line1
        assert "🌿" in line1, "Missing git branch icon"
        assert "main" in line1
        assert "🤖" in line1, "Missing model icon"
        assert "claude-sonnet-4-5-20250929" in line1
        assert "📟" in line1, "Missing version icon"
        assert "v1.0.85" in line1
        assert "🎨" in line1, "Missing style icon"
        assert "markdown" in line1

        # Line 2: Status (context, duration)
        line2 = lines[1]
        assert "🧠" in line2, "Missing context icon"
        assert "85%" in line2
        assert "[" in line2 and "]" in line2, "Missing progress bar"
        assert "⌛" in line2, "Missing duration icon"
        assert "30m" in line2

        # Line 3: Metrics (cost, tokens, lines_changed)
        line3 = lines[2]
        assert "💰" in line3, "Missing cost icon"
        assert "$12.50" in line3
        assert "$25.00/h" in line3
        assert "📊" in line3, "Missing tokens icon"
        assert "75000 tok" in line3
        assert "2500 tpm" in line3
        assert "150 lines" in line3

    def test_full_verbose_mode_with_icons_and_labels(self, monkeypatch):
        """Test complete verbose mode output with all fields, icons, and labels."""
        monkeypatch.delenv("NO_COLOR", raising=False)

        config = get_default_config()
        config["display_mode"] = "verbose"
        # Enable all fields
        for field in config["visible_fields"]:
            config["visible_fields"][field] = True

        # Complete dataset
        data = {
            "model": "claude-sonnet-4-5-20250929",
            "version": "v1.0.85",
            "current_dir": "my-project",
            "git_branch": "feature/new-api",
            "output_style": "markdown",
            "context_remaining": 75,
            "duration": 3600000,  # 60 minutes
            "tokens": 100000,
            "tokens_per_minute": 1666,
            "cost": 18.75,
            "cost_per_hour": 18.75,
            "lines_changed": 250
        }

        result = format_verbose(data, config)

        # Verify structure: should have 3 lines
        lines = result.split("\n")
        assert len(lines) == 3, f"Expected 3 lines, got {len(lines)}"

        # Line 1: Identity with labels
        line1 = lines[0]
        assert "📁" in line1 and "Directory:" in line1 and "my-project" in line1
        assert "🌿" in line1 and "Git branch:" in line1 and "feature/new-api" in line1
        assert "🤖" in line1 and "Model:" in line1 and "claude-sonnet-4-5-20250929" in line1
        assert "📟" in line1 and "Version:" in line1 and "v1.0.85" in line1
        assert "🎨" in line1 and "Style:" in line1 and "markdown" in line1

        # Line 2: Status with labels
        line2 = lines[1]
        assert "🧠" in line2 and "Context remaining:" in line2 and "75%" in line2
        assert "[" in line2 and "]" in line2, "Missing progress bar"
        assert "⌛" in line2 and "Duration:" in line2 and "1h 0m" in line2

        # Line 3: Metrics with labels
        line3 = lines[2]
        assert "💰" in line3 and "Cost:" in line3 and "$18.75" in line3
        assert "📊" in line3 and "Tokens:" in line3 and "100000 tok" in line3
        assert "Lines changed:" in line3 and "250 lines" in line3

    def test_compact_mode_without_optional_fields(self, monkeypatch):
        """Test compact mode with only required fields (no git, no duration)."""
        monkeypatch.delenv("NO_COLOR", raising=False)

        config = get_default_config()
        # Minimal field set
        config["visible_fields"]["git_branch"] = False
        config["visible_fields"]["duration"] = False
        config["visible_fields"]["lines_changed"] = False
        config["visible_fields"]["output_style"] = False

        data = {
            "model": "claude-opus-4",
            "version": "v1.0.0",
            "current_dir": "test-project",
            "context_remaining": 95,
            "tokens": 5000,
            "cost": 1.25
        }

        result = format_compact(data, config)
        lines = result.split("\n")

        # Should still have 3 lines (some may be empty if no fields visible)
        assert "📁" in result and "test-project" in result
        assert "🤖" in result and "claude-opus-4" in result
        assert "📟" in result and "v1.0.0" in result
        assert "🧠" in result and "95%" in result
        assert "📊" in result and "5000 tok" in result
        assert "💰" in result and "$1.25" in result

        # Should NOT have git, duration, lines, or style
        assert "🌿" not in result, "Git branch should not be present"
        assert "⌛" not in result, "Duration should not be present"
        assert "🎨" not in result, "Style should not be present"

    def test_progress_bar_visual_accuracy(self, monkeypatch):
        """Test that progress bar visual representation is accurate."""
        monkeypatch.delenv("NO_COLOR", raising=False)

        config = get_default_config()
        config["progress_bar_width"] = 10
        config["visible_fields"] = {"context_remaining": True}

        # Test different percentages
        test_cases = [
            (0, 0),    # 0% = 0 filled
            (50, 5),   # 50% = 5 filled
            (100, 10), # 100% = 10 filled
        ]

        for percentage, expected_filled in test_cases:
            data = {"context_remaining": percentage}
            result = format_compact(data, config)

            # Count filled characters (=) in progress bar
            # Extract just the progress bar part
            bar_start = result.find("[")
            bar_end = result.find("]")
            if bar_start != -1 and bar_end != -1:
                # Count visible = characters (ignoring ANSI codes)
                bar_content = result[bar_start+1:bar_end]
                # Remove ANSI codes to count actual characters
                import re
                clean_bar = re.sub(r'\x1b\[[0-9;]*m', '', bar_content)
                filled_count = clean_bar.count("=")
                assert filled_count == expected_filled, \
                    f"Expected {expected_filled} filled chars for {percentage}%, got {filled_count}"


class TestEndToEndWorkflow:
    """Test complete workflow from JSON input to formatted output."""

    def test_statusline_main_compact_mode(self, monkeypatch, capsys):
        """Test main() function with realistic JSON input in compact mode."""
        monkeypatch.delenv("NO_COLOR", raising=False)

        # Create realistic JSON input
        json_input = {
            "model": {"id": "claude-sonnet-4-5-20250929"},
            "version": "v1.0.85",
            "context_window": {
                "remaining_percentage": 80,
                "total_input_tokens": 50000,
                "total_output_tokens": 25000
            },
            "workspace": {"current_dir": "/Users/test/my-project"},
            "cost": {
                "total_cost_usd": 10.50,
                "total_duration_ms": 1200000  # 20 minutes
            },
            "edit_tracker": {
                "total_lines_added": 100,
                "total_lines_removed": 50
            },
            "output": {"style": "markdown"}
        }

        # Simulate stdin input
        json_str = json.dumps(json_input)
        monkeypatch.setattr('sys.stdin', StringIO(json_str))

        # Load config and ensure version field is visible for test
        from config_manager import load_config, save_config
        config = load_config()
        original_version_visible = config["visible_fields"].get("version", True)
        original_tokens_visible = config["visible_fields"].get("tokens", True)
        original_cost_visible = config["visible_fields"].get("cost", True)
        config["visible_fields"]["version"] = True
        config["visible_fields"]["tokens"] = True
        config["visible_fields"]["cost"] = True
        save_config(config)

        try:
            # Run main function
            statusline.main()

            # Capture output
            captured = capsys.readouterr()
            output = captured.out

            # Verify output contains expected elements
            assert "my-project" in output
            assert "claude-sonnet-4-5-20250929" in output
            assert "v1.0.85" in output
            assert "80%" in output
            assert "75000 tok" in output  # 50000 + 25000
            assert "$10.50" in output
            # Note: lines_changed and output_style are not visible by default
        finally:
            # Restore original visibility settings
            config["visible_fields"]["version"] = original_version_visible
            config["visible_fields"]["tokens"] = original_tokens_visible
            config["visible_fields"]["cost"] = original_cost_visible
            save_config(config)

    def test_statusline_main_verbose_mode(self, monkeypatch, capsys):
        """Test main() function with verbose mode."""
        monkeypatch.delenv("NO_COLOR", raising=False)

        json_input = {
            "model": {"id": "claude-opus-4"},
            "version": "v1.0.0",
            "workspace": {"current_dir": "/Users/test/project"}
        }

        json_str = json.dumps(json_input)
        monkeypatch.setattr('sys.stdin', StringIO(json_str))

        # Load config and set to verbose, ensure version field is visible
        from config_manager import load_config, save_config, CONFIG_FILE
        config = load_config()
        original_display_mode = config["display_mode"]
        original_version_visible = config["visible_fields"].get("version", True)
        config["display_mode"] = "verbose"
        config["visible_fields"]["version"] = True
        save_config(config)

        try:
            statusline.main()
            captured = capsys.readouterr()
            output = captured.out

            # Verify labels are present in verbose mode
            assert "Model:" in output
            assert "Version:" in output
            assert "Directory:" in output
        finally:
            # Restore original settings
            config["display_mode"] = original_display_mode
            config["visible_fields"]["version"] = original_version_visible
            save_config(config)


class TestInstallationHelper:
    """Test the installation helper script."""

    def test_install_helper_update_settings(self):
        """Test that install_helper.py can update settings file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            settings_file = Path(tmpdir) / "settings.json"

            # Import the helper
            helper_path = Path(__file__).parent.parent / "install_helper.py"
            sys.path.insert(0, str(helper_path.parent))
            import install_helper

            # Run update_claude_settings
            result = install_helper.update_claude_settings(settings_file)

            assert result == 0, "update_claude_settings should return 0 on success"
            assert settings_file.exists(), "Settings file should be created"

            # Verify content
            with open(settings_file) as f:
                settings = json.load(f)

            assert "statusLine" in settings
            assert settings["statusLine"]["type"] == "command"
            assert settings["statusLine"]["command"] == "~/.claude-code-statusline/statusline.py"

    def test_install_helper_preserves_existing_settings(self):
        """Test that install_helper.py preserves existing settings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            settings_file = Path(tmpdir) / "settings.json"

            # Create existing settings
            existing_settings = {
                "someOtherSetting": "value",
                "nested": {"key": "value"}
            }
            with open(settings_file, 'w') as f:
                json.dump(existing_settings, f)

            # Import and run helper
            helper_path = Path(__file__).parent.parent / "install_helper.py"
            sys.path.insert(0, str(helper_path.parent))
            import install_helper

            result = install_helper.update_claude_settings(settings_file)

            assert result == 0

            # Verify existing settings preserved
            with open(settings_file) as f:
                settings = json.load(f)

            assert settings["someOtherSetting"] == "value"
            assert settings["nested"]["key"] == "value"
            assert "statusLine" in settings

    def test_install_helper_config_creation(self):
        """Test that install_helper.py can create default config."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Import helper
            helper_path = Path(__file__).parent.parent / "install_helper.py"
            sys.path.insert(0, str(helper_path.parent))
            import install_helper

            # Create a temporary src directory with config_manager
            src_dir = Path(tmpdir) / "src"
            src_dir.mkdir()

            # Copy necessary files
            import shutil
            project_src = Path(__file__).parent.parent / "src"
            shutil.copy(project_src / "config_manager.py", src_dir / "config_manager.py")
            # Copy constants directory (it's now a package, not a single file)
            shutil.copytree(project_src / "constants", src_dir / "constants")

            # Run create_default_config
            result = install_helper.create_default_config(str(src_dir))

            # Should succeed and create config file
            config_file = Path.home() / ".claude-code-statusline" / "config.json"
            assert config_file.exists(), "Config file should be created"


class TestIconsAndColorsDisabled:
    """Test output when icons or colors are disabled."""

    def test_compact_without_icons(self, monkeypatch):
        """Test compact mode output when icons are disabled."""
        monkeypatch.delenv("NO_COLOR", raising=False)

        config = get_default_config()
        # Remove all icons
        config["icons"] = {}

        data = {
            "model": "claude-sonnet-4",
            "current_dir": "test-project",
            "context_remaining": 90
        }

        result = format_compact(data, config)

        # Should still have content but no emoji icons
        assert "test-project" in result
        assert "claude-sonnet-4" in result
        assert "90%" in result

        # Count emoji/icon characters - should be minimal
        emoji_count = sum(1 for c in result if ord(c) > 0x1F000)
        assert emoji_count == 0, "Should have no emoji icons"

    def test_output_with_no_color_env(self, monkeypatch):
        """Test that NO_COLOR environment variable disables colors."""
        monkeypatch.setenv("NO_COLOR", "1")

        config = get_default_config()
        data = {
            "model": "claude-sonnet-4",
            "cost": 5.00
        }

        result = format_compact(data, config)

        # Should not contain ANSI color codes
        assert "\x1b[" not in result, "Should not contain ANSI color codes"

        # Should still have content
        assert "claude-sonnet-4" in result
        assert "5.00" in result
