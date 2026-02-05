"""
Data models for the Claude Code Statusline Tool.

This module provides typed data structures for configuration and statusline data.
Uses regular classes with type hints for Python 3.6 compatibility.
"""

from typing import Dict, Any, List, Optional
import constants


class StatusLineData:
    """
    Represents the extracted data from Claude Code JSON input.

    This provides a typed interface for the data dictionary, making it
    easier to work with and understand what fields are available.
    """

    def __init__(self, data: Dict[str, Any]):
        """
        Initialize from a data dictionary.

        Args:
            data: Dictionary of extracted field values
        """
        self._data = data

    # ========================================================================
    # Core Fields
    # ========================================================================

    @property
    def model(self) -> Optional[str]:
        """Claude model ID."""
        return self._data.get(constants.FIELD_MODEL)

    @property
    def version(self) -> Optional[str]:
        """Claude Code version."""
        return self._data.get(constants.FIELD_VERSION)

    @property
    def context_remaining(self) -> Optional[int]:
        """Context window remaining percentage."""
        return self._data.get(constants.FIELD_CONTEXT_REMAINING)

    @property
    def tokens(self) -> Optional[int]:
        """Total tokens (input + output)."""
        return self._data.get(constants.FIELD_TOKENS)

    @property
    def current_dir(self) -> Optional[str]:
        """Current working directory name."""
        return self._data.get(constants.FIELD_CURRENT_DIR)

    @property
    def git_branch(self) -> Optional[str]:
        """Current git branch name."""
        return self._data.get(constants.FIELD_GIT_BRANCH)

    @property
    def cost(self) -> Optional[float]:
        """Total cost in USD."""
        return self._data.get(constants.FIELD_COST)

    @property
    def duration(self) -> Optional[int]:
        """Session duration in milliseconds."""
        return self._data.get(constants.FIELD_DURATION)

    @property
    def lines_changed(self) -> Optional[int]:
        """Total lines added + removed."""
        return self._data.get(constants.FIELD_LINES_CHANGED)

    @property
    def output_style(self) -> Optional[str]:
        """Output style name."""
        return self._data.get(constants.FIELD_OUTPUT_STYLE)

    # ========================================================================
    # Calculated Fields
    # ========================================================================

    @property
    def cost_per_hour(self) -> Optional[float]:
        """Calculated cost per hour."""
        return self._data.get(constants.FIELD_COST_PER_HOUR)

    @property
    def tokens_per_minute(self) -> Optional[int]:
        """Calculated tokens per minute."""
        return self._data.get(constants.FIELD_TOKENS_PER_MINUTE)

    # ========================================================================
    # Dictionary Interface
    # ========================================================================

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a value from the data dictionary.

        Args:
            key: Field name
            default: Default value if key not found

        Returns:
            Field value or default
        """
        return self._data.get(key, default)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary representation.

        Returns:
            Dictionary of all data fields
        """
        return self._data.copy()

    def __repr__(self) -> str:
        """String representation for debugging."""
        fields = []
        for key, value in self._data.items():
            if value is not None:
                fields.append(f"{key}={value!r}")
        return f"StatusLineData({', '.join(fields)})"


class Configuration:
    """
    Represents the user configuration for the statusline.

    This provides a typed interface for the configuration dictionary,
    making it easier to work with and validate.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize from a configuration dictionary.

        Args:
            config: Configuration dictionary
        """
        self._config = config

    # ========================================================================
    # Display Settings
    # ========================================================================

    @property
    def display_mode(self) -> str:
        """Display mode: 'compact' or 'verbose'."""
        return self._config.get(constants.CONFIG_KEY_DISPLAY_MODE, constants.DISPLAY_MODE_COMPACT)

    @property
    def is_verbose(self) -> bool:
        """Whether verbose mode is enabled."""
        return self.display_mode == constants.DISPLAY_MODE_VERBOSE

    @property
    def enable_colors(self) -> bool:
        """Whether colors are enabled."""
        return self._config.get(constants.CONFIG_KEY_ENABLE_COLORS, constants.DEFAULT_ENABLE_COLORS)

    @property
    def show_progress_bars(self) -> bool:
        """Whether progress bars are enabled."""
        return self._config.get(constants.CONFIG_KEY_SHOW_PROGRESS_BARS, constants.DEFAULT_SHOW_PROGRESS_BARS)

    @property
    def progress_bar_width(self) -> int:
        """Width of progress bars."""
        return self._config.get(constants.CONFIG_KEY_PROGRESS_BAR_WIDTH, constants.DEFAULT_PROGRESS_BAR_WIDTH)

    # ========================================================================
    # Field Configuration
    # ========================================================================

    @property
    def visible_fields(self) -> Dict[str, bool]:
        """Dictionary of field visibility settings."""
        return self._config.get(constants.CONFIG_KEY_VISIBLE_FIELDS, {})

    def is_field_visible(self, field_name: str) -> bool:
        """
        Check if a field is visible.

        Args:
            field_name: Name of the field

        Returns:
            True if field should be displayed
        """
        return self.visible_fields.get(field_name, False)

    @property
    def field_order(self) -> List[str]:
        """Ordered list of field names."""
        return self._config.get(constants.CONFIG_KEY_FIELD_ORDER, [])

    # ========================================================================
    # Icons and Colors
    # ========================================================================

    @property
    def icons(self) -> Dict[str, str]:
        """Dictionary of icon settings."""
        return self._config.get(constants.CONFIG_KEY_ICONS, {})

    def get_icon(self, key: str) -> str:
        """
        Get icon for a key.

        Args:
            key: Icon key

        Returns:
            Icon string or empty string
        """
        return self.icons.get(key, "")

    @property
    def colors(self) -> Dict[str, str]:
        """Dictionary of color settings."""
        return self._config.get(constants.CONFIG_KEY_COLORS, {})

    def get_color(self, key: str, default: str = constants.COLOR_WHITE) -> str:
        """
        Get color for a key.

        Args:
            key: Color key
            default: Default color if not found

        Returns:
            Color name
        """
        return self.colors.get(key, default)

    # ========================================================================
    # Dictionary Interface
    # ========================================================================

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a value from the config dictionary.

        Args:
            key: Config key
            default: Default value if key not found

        Returns:
            Config value or default
        """
        return self._config.get(key, default)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary representation.

        Returns:
            Dictionary of all config values
        """
        return self._config.copy()

    def __getitem__(self, key: str) -> Any:
        """
        Dictionary-style access to config values.

        Args:
            key: Config key

        Returns:
            Config value
        """
        return self._config[key]

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"Configuration(mode={self.display_mode}, fields={len(self.visible_fields)})"
