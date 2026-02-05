"""
Configuration management for the Claude Code Statusline Tool.

This module handles loading, saving, and validating user configuration.
Uses constants module for all default values and validation.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

import constants
from exceptions import ConfigurationError

# Configure logger
logger = logging.getLogger("claude_statusline.config")

# Default configuration paths
CONFIG_DIR = Path.home() / ".claude-code-statusline"
CONFIG_FILE = CONFIG_DIR / "config.json"


class ConfigManager:
    """
    Manages configuration loading, validation, and persistence.

    This class provides stateful configuration management with caching,
    validation, and support for multiple config files.

    Attributes:
        config_file: Path to the configuration file
        config_dir: Directory containing the configuration file
    """

    def __init__(self, config_file: Path = None):
        """
        Initialize the ConfigManager.

        Args:
            config_file: Path to configuration file (defaults to CONFIG_FILE if None)
        """
        # Check CONFIG_FILE at runtime to support testing with monkeypatch
        self.config_file = config_file if config_file is not None else CONFIG_FILE
        self.config_dir = self.config_file.parent
        self._config: Optional[Dict[str, Any]] = None

    @staticmethod
    def get_default_config() -> Dict[str, Any]:
        """
        Return default configuration using constants.

        Returns:
            Dictionary containing default configuration values
        """
        return {
            "display_mode": constants.DEFAULT_DISPLAY_MODE,
            "visible_fields": constants.DEFAULT_VISIBLE_FIELDS.copy(),
            "field_order": constants.DEFAULT_FIELD_ORDER.copy(),
            "icons": constants.DEFAULT_ICONS.copy(),
            "colors": constants.DEFAULT_COLORS.copy(),
            "show_progress_bars": constants.DEFAULT_SHOW_PROGRESS_BARS,
            "progress_bar_width": constants.DEFAULT_PROGRESS_BAR_WIDTH,
            "enable_colors": constants.DEFAULT_ENABLE_COLORS
        }

    def validate(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and sanitize configuration values.

        Args:
            config: Configuration dictionary to validate

        Returns:
            Validated configuration with invalid values replaced by defaults
        """
        default_config = self.get_default_config()
        warnings = []

        # Validate display_mode
        if config.get("display_mode") not in constants.VALID_DISPLAY_MODES:
            warnings.append(
                f"Invalid display_mode '{config.get('display_mode')}', "
                f"using default '{constants.DEFAULT_DISPLAY_MODE}'"
            )
            config["display_mode"] = default_config["display_mode"]

        # Validate progress_bar_width
        if "progress_bar_width" in config:
            width = config["progress_bar_width"]
            if not isinstance(width, int) or width < constants.MIN_PROGRESS_BAR_WIDTH or width > constants.MAX_PROGRESS_BAR_WIDTH:
                warnings.append(
                    f"Invalid progress_bar_width {width}, must be between "
                    f"{constants.MIN_PROGRESS_BAR_WIDTH} and {constants.MAX_PROGRESS_BAR_WIDTH}. "
                    f"Using default {default_config['progress_bar_width']}"
                )
                config["progress_bar_width"] = default_config["progress_bar_width"]

        # Validate colors
        if "colors" in config:
            for field, color in config["colors"].items():
                if color not in constants.VALID_COLORS:
                    warnings.append(f"Invalid color '{color}' for field '{field}', using default")
                    config["colors"][field] = default_config["colors"].get(field, constants.COLOR_WHITE)

        # Validate field_order
        if "field_order" in config:
            invalid_fields = [f for f in config["field_order"] if f not in constants.VALID_FIELD_NAMES]
            if invalid_fields:
                warnings.append(f"Invalid field names in field_order: {', '.join(invalid_fields)}")
                config["field_order"] = [f for f in config["field_order"] if f in constants.VALID_FIELD_NAMES]

            # Add any missing valid fields
            for field in constants.VALID_FIELD_NAMES:
                if field not in config["field_order"]:
                    config["field_order"].append(field)

        # Log warnings if any
        if warnings:
            logger.warning("Configuration validation warnings:")
            for warning in warnings:
                logger.warning(f"  - {warning}")

        return config

    def ensure_exists(self) -> None:
        """Create default config if missing."""
        self.config_dir.mkdir(parents=True, exist_ok=True)

        if not self.config_file.exists():
            self.save(self.get_default_config())

    def _load_from_file(self) -> Dict[str, Any]:
        """
        Load configuration from file.

        Returns:
            Configuration dictionary

        Note:
            Returns default config if file doesn't exist or is invalid.
        """
        self.ensure_exists()

        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)

            # Merge with defaults to handle missing keys
            default_config = self.get_default_config()
            for key, value in default_config.items():
                if key not in config:
                    config[key] = value
                elif isinstance(value, dict):
                    for subkey, subvalue in value.items():
                        if subkey not in config[key]:
                            config[key][subkey] = subvalue

            # Validate the loaded config
            config = self.validate(config)

            return config
        except json.JSONDecodeError as e:
            logger.warning(f"Config file contains invalid JSON: {e}")
            logger.warning("Using default configuration instead")
            return self.get_default_config()
        except IOError as e:
            logger.warning(f"Could not read config file: {e}")
            logger.warning("Using default configuration instead")
            return self.get_default_config()

    def load(self, force_reload: bool = False) -> Dict[str, Any]:
        """
        Load configuration with caching support.

        Args:
            force_reload: If True, ignore cache and reload from file

        Returns:
            Configuration dictionary
        """
        if force_reload or self._config is None:
            self._config = self._load_from_file()
        return self._config

    def save(self, config: Dict[str, Any]) -> None:
        """
        Save configuration to file.

        Args:
            config: Configuration dictionary to save
        """
        self.config_dir.mkdir(parents=True, exist_ok=True)

        # Validate before saving
        validated_config = self.validate(config.copy())

        with open(self.config_file, 'w') as f:
            json.dump(validated_config, f, indent=2)

        # Update cache
        self._config = validated_config

    def reload(self) -> Dict[str, Any]:
        """
        Force reload configuration from file.

        Returns:
            Reloaded configuration dictionary
        """
        return self.load(force_reload=True)


# ============================================================================
# Module-level convenience functions (backward compatibility)
# ============================================================================


def get_default_config() -> Dict[str, Any]:
    """
    Return default configuration using constants.

    Returns:
        Dictionary containing default configuration values
    """
    return ConfigManager.get_default_config()


def validate_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and sanitize configuration values.

    Args:
        config: Configuration dictionary to validate

    Returns:
        Validated configuration with invalid values replaced by defaults
    """
    # Create a temporary manager for validation (respects monkeypatched CONFIG_FILE)
    manager = ConfigManager(CONFIG_FILE)
    return manager.validate(config)


def ensure_config_exists() -> None:
    """Create default config if missing."""
    # Create a temporary manager (respects monkeypatched CONFIG_FILE)
    manager = ConfigManager(CONFIG_FILE)
    manager.ensure_exists()


def load_config() -> Dict[str, Any]:
    """
    Load config from ~/.claude-code-statusline/config.json.

    Returns:
        Configuration dictionary
    """
    # Create a temporary manager (respects monkeypatched CONFIG_FILE)
    manager = ConfigManager(CONFIG_FILE)
    return manager.load()


def save_config(config: Dict[str, Any]) -> None:
    """
    Save config to file.

    Args:
        config: Configuration dictionary to save
    """
    # Create a temporary manager (respects monkeypatched CONFIG_FILE)
    manager = ConfigManager(CONFIG_FILE)
    manager.save(config)
