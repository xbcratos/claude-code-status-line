"""
Tests for data models (StatusLineData and Configuration).
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from models import StatusLineData, Configuration
import constants


class TestStatusLineData:
    """Test StatusLineData model."""

    def test_model_property(self):
        """Test model property access."""
        data = StatusLineData({"model": "claude-sonnet-4"})
        assert data.model == "claude-sonnet-4"

    def test_version_property(self):
        """Test version property access."""
        data = StatusLineData({"version": "v1.0.0"})
        assert data.version == "v1.0.0"

    def test_context_remaining_property(self):
        """Test context_remaining property access."""
        data = StatusLineData({"context_remaining": 85})
        assert data.context_remaining == 85

    def test_tokens_property(self):
        """Test tokens property access."""
        data = StatusLineData({"tokens": 5000})
        assert data.tokens == 5000

    def test_current_dir_property(self):
        """Test current_dir property access."""
        data = StatusLineData({"current_dir": "my-project"})
        assert data.current_dir == "my-project"

    def test_git_branch_property(self):
        """Test git_branch property access."""
        data = StatusLineData({"git_branch": "main"})
        assert data.git_branch == "main"

    def test_cost_property(self):
        """Test cost property access."""
        data = StatusLineData({"cost": 12.50})
        assert data.cost == 12.50

    def test_duration_property(self):
        """Test duration property access."""
        data = StatusLineData({"duration": 120000})
        assert data.duration == 120000

    def test_lines_changed_property(self):
        """Test lines_changed property access."""
        data = StatusLineData({"lines_changed": 150})
        assert data.lines_changed == 150

    def test_output_style_property(self):
        """Test output_style property access."""
        data = StatusLineData({"output_style": "markdown"})
        assert data.output_style == "markdown"

    def test_cost_per_hour_property(self):
        """Test cost_per_hour property access."""
        data = StatusLineData({"cost_per_hour": 25.00})
        assert data.cost_per_hour == 25.00

    def test_tokens_per_minute_property(self):
        """Test tokens_per_minute property access."""
        data = StatusLineData({"tokens_per_minute": 2500})
        assert data.tokens_per_minute == 2500

    def test_properties_return_none_when_missing(self):
        """Test that properties return None when field is missing."""
        data = StatusLineData({})
        assert data.model is None
        assert data.version is None
        assert data.context_remaining is None
        assert data.tokens is None
        assert data.current_dir is None
        assert data.git_branch is None
        assert data.cost is None
        assert data.duration is None
        assert data.lines_changed is None
        assert data.output_style is None
        assert data.cost_per_hour is None
        assert data.tokens_per_minute is None

    def test_get_method(self):
        """Test get method with default value."""
        data = StatusLineData({"model": "claude-sonnet-4"})
        assert data.get("model") == "claude-sonnet-4"
        assert data.get("missing_field") is None
        assert data.get("missing_field", "default") == "default"

    def test_to_dict_method(self):
        """Test to_dict returns a copy of data."""
        original = {"model": "claude-sonnet-4", "version": "v1.0.0"}
        data = StatusLineData(original)
        result = data.to_dict()

        assert result == original
        # Verify it's a copy, not the same object
        result["model"] = "changed"
        assert data.model == "claude-sonnet-4"

    def test_repr_method(self):
        """Test __repr__ for debugging."""
        data = StatusLineData({"model": "claude-sonnet-4", "version": "v1.0.0"})
        repr_str = repr(data)

        assert "StatusLineData" in repr_str
        assert "model='claude-sonnet-4'" in repr_str
        assert "version='v1.0.0'" in repr_str


class TestConfiguration:
    """Test Configuration model."""

    def test_display_mode_property(self):
        """Test display_mode property access."""
        config = Configuration({"display_mode": "verbose"})
        assert config.display_mode == "verbose"

    def test_display_mode_default(self):
        """Test display_mode returns default when missing."""
        config = Configuration({})
        assert config.display_mode == constants.DISPLAY_MODE_COMPACT

    def test_is_verbose_true(self):
        """Test is_verbose returns True for verbose mode."""
        config = Configuration({"display_mode": "verbose"})
        assert config.is_verbose is True

    def test_is_verbose_false(self):
        """Test is_verbose returns False for compact mode."""
        config = Configuration({"display_mode": "compact"})
        assert config.is_verbose is False

    def test_enable_colors_property(self):
        """Test enable_colors property access."""
        config = Configuration({"enable_colors": False})
        assert config.enable_colors is False

    def test_enable_colors_default(self):
        """Test enable_colors returns default when missing."""
        config = Configuration({})
        assert config.enable_colors is True

    def test_show_progress_bars_property(self):
        """Test show_progress_bars property access."""
        config = Configuration({"show_progress_bars": False})
        assert config.show_progress_bars is False

    def test_show_progress_bars_default(self):
        """Test show_progress_bars returns default when missing."""
        config = Configuration({})
        assert config.show_progress_bars is True

    def test_progress_bar_width_property(self):
        """Test progress_bar_width property access."""
        config = Configuration({"progress_bar_width": 15})
        assert config.progress_bar_width == 15

    def test_progress_bar_width_default(self):
        """Test progress_bar_width returns default when missing."""
        config = Configuration({})
        assert config.progress_bar_width == constants.DEFAULT_PROGRESS_BAR_WIDTH

    def test_visible_fields_property(self):
        """Test visible_fields property access."""
        fields = {"model": True, "version": False}
        config = Configuration({"visible_fields": fields})
        assert config.visible_fields == fields

    def test_visible_fields_default(self):
        """Test visible_fields returns empty dict when missing."""
        config = Configuration({})
        assert config.visible_fields == {}

    def test_is_field_visible_true(self):
        """Test is_field_visible returns True for visible field."""
        config = Configuration({"visible_fields": {"model": True}})
        assert config.is_field_visible("model") is True

    def test_is_field_visible_false(self):
        """Test is_field_visible returns False for hidden field."""
        config = Configuration({"visible_fields": {"model": False}})
        assert config.is_field_visible("model") is False

    def test_is_field_visible_missing(self):
        """Test is_field_visible returns False for missing field."""
        config = Configuration({"visible_fields": {}})
        assert config.is_field_visible("model") is False

    def test_field_order_property(self):
        """Test field_order property access."""
        order = ["model", "version", "cost"]
        config = Configuration({"field_order": order})
        assert config.field_order == order

    def test_field_order_default(self):
        """Test field_order returns empty list when missing."""
        config = Configuration({})
        assert config.field_order == []

    def test_icons_property(self):
        """Test icons property access."""
        icons = {"directory": "📁", "model": "🤖"}
        config = Configuration({"icons": icons})
        assert config.icons == icons

    def test_icons_default(self):
        """Test icons returns empty dict when missing."""
        config = Configuration({})
        assert config.icons == {}

    def test_get_icon_existing(self):
        """Test get_icon returns icon for existing key."""
        config = Configuration({"icons": {"directory": "📁"}})
        assert config.get_icon("directory") == "📁"

    def test_get_icon_missing(self):
        """Test get_icon returns empty string for missing key."""
        config = Configuration({"icons": {}})
        assert config.get_icon("directory") == ""

    def test_colors_property(self):
        """Test colors property access."""
        colors = {"model": "blue", "cost": "red"}
        config = Configuration({"colors": colors})
        assert config.colors == colors

    def test_colors_default(self):
        """Test colors returns empty dict when missing."""
        config = Configuration({})
        assert config.colors == {}

    def test_get_color_existing(self):
        """Test get_color returns color for existing key."""
        config = Configuration({"colors": {"model": "blue"}})
        assert config.get_color("model") == "blue"

    def test_get_color_missing_uses_default(self):
        """Test get_color returns default for missing key."""
        config = Configuration({"colors": {}})
        assert config.get_color("model") == constants.COLOR_WHITE

    def test_get_color_custom_default(self):
        """Test get_color accepts custom default."""
        config = Configuration({"colors": {}})
        assert config.get_color("model", "cyan") == "cyan"

    def test_get_method(self):
        """Test get method with default value."""
        config = Configuration({"display_mode": "verbose"})
        assert config.get("display_mode") == "verbose"
        assert config.get("missing_key") is None
        assert config.get("missing_key", "default") == "default"

    def test_to_dict_method(self):
        """Test to_dict returns a copy of config."""
        original = {"display_mode": "verbose", "enable_colors": True}
        config = Configuration(original)
        result = config.to_dict()

        assert result == original
        # Verify it's a copy
        result["display_mode"] = "compact"
        assert config.display_mode == "verbose"

    def test_getitem_method(self):
        """Test __getitem__ for dictionary-style access."""
        config = Configuration({"display_mode": "verbose"})
        assert config["display_mode"] == "verbose"

    def test_getitem_missing_key(self):
        """Test __getitem__ raises KeyError for missing key."""
        config = Configuration({})
        with pytest.raises(KeyError):
            _ = config["missing_key"]

    def test_repr_method(self):
        """Test __repr__ for debugging."""
        config = Configuration({
            "display_mode": "verbose",
            "visible_fields": {"model": True, "version": False}
        })
        repr_str = repr(config)

        assert "Configuration" in repr_str
        assert "mode=verbose" in repr_str
        assert "fields=2" in repr_str
