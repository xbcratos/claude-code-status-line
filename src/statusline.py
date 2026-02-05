#!/usr/bin/env python3
import sys
from pathlib import Path

# Add src directory to path for imports (must be before other local imports)
sys.path.insert(0, str(Path(__file__).parent))

import json
import logging
import os
from typing import Dict, Any
from config_manager import ConfigManager, load_config
from display_formatter import StatusLineFormatter, format_compact, format_verbose
from data_extractor import DataExtractor, extract_data
from exceptions import InvalidJSONError
import colors

# Configure logger
logger = logging.getLogger("claude_statusline")


def _configure_logging() -> None:
    """
    Configure logging based on environment variables.

    LOG_LEVEL environment variable can be set to control verbosity:
    - DEBUG: Detailed information for debugging
    - INFO: Confirmation that things are working
    - WARNING: Something unexpected happened (default)
    - ERROR: Serious problem

    Logs go to stderr to avoid interfering with stdout output.
    """
    log_level = os.environ.get("LOG_LEVEL", "WARNING").upper()
    logging.basicConfig(
        level=getattr(logging, log_level, logging.WARNING),
        format="%(levelname)s: %(message)s",
        stream=sys.stderr
    )

# Require Python 3.6+
if sys.version_info < (3, 6):
    print("Error: Python 3.6 or higher is required", file=sys.stderr)
    print(f"Current version: {sys.version}", file=sys.stderr)
    sys.exit(1)


class StatusLine:
    """
    Facade for statusline generation workflow.

    This class provides a clean, testable API for generating statusline output
    from Claude Code JSON data. It orchestrates the configuration, data extraction,
    and formatting processes.

    Attributes:
        config_manager: Manages configuration loading and validation
        data_extractor: Extracts data from Claude Code JSON
        formatter: Formats the extracted data for display
    """

    def __init__(self, config_manager: ConfigManager = None):
        """
        Initialize the StatusLine facade.

        Args:
            config_manager: Optional ConfigManager instance (uses default if None)
        """
        self.config_manager = config_manager or ConfigManager()
        self.data_extractor = DataExtractor()
        self.formatter = StatusLineFormatter()

    def generate(self, json_input: str) -> str:
        """
        Generate statusline from JSON input.

        This is the main entry point for programmatic use of the statusline generator.

        Args:
            json_input: JSON string from Claude Code

        Returns:
            Formatted statusline string

        Raises:
            InvalidJSONError: If JSON input cannot be parsed
            Exception: For other unexpected errors during generation
        """
        # Parse JSON
        logger.debug("Parsing JSON input")
        try:
            json_data = json.loads(json_input)
            logger.debug(f"Successfully parsed JSON with keys: {list(json_data.keys())}")
        except json.JSONDecodeError as e:
            raise InvalidJSONError(f"Failed to parse JSON input: {e}")

        # Load configuration
        logger.debug("Loading configuration")
        config = self.config_manager.load()

        # Configure colors based on config and environment
        self._configure_colors(config)

        # Extract data from JSON
        logger.debug("Extracting data from JSON")
        data = self.data_extractor.extract(json_data, config)
        logger.debug(f"Extracted fields: {list(data.keys())}")

        # Format output based on display mode
        display_mode = config.get("display_mode", "compact")
        logger.debug(f"Using display mode: {display_mode}")

        verbose = self._is_verbose(display_mode)
        output = self.formatter.format(data, config, verbose=verbose)

        logger.debug("Statusline generation complete")
        return output

    def _configure_colors(self, config: Dict[str, Any]) -> None:
        """
        Configure color output based on config and environment.

        Sets the colors module state to enable or disable colors.

        Args:
            config: Configuration dictionary
        """
        # Set color state in colors module based on config and environment
        # Note: We modify the module state rather than environment to avoid side effects
        if not config.get("enable_colors", True):
            logger.debug("Colors disabled by config")
            colors._color_override = False
        elif not colors.is_color_enabled():
            logger.debug("Colors disabled by NO_COLOR environment variable")
            colors._color_override = False
        else:
            colors._color_override = None

    def _is_verbose(self, display_mode: str) -> bool:
        """
        Determine if verbose mode should be used.

        Args:
            display_mode: Display mode from config

        Returns:
            True if verbose mode should be used, False otherwise
        """
        # Support both "large" and "verbose" for compatibility
        return display_mode in ["large", "verbose"]


def main() -> None:
    """Main entry point for statusline script."""
    # Configure logging first
    _configure_logging()

    try:
        # Read JSON from stdin
        logger.debug("Reading JSON from stdin")
        input_data = sys.stdin.read()

        # Create StatusLine facade and generate output
        statusline = StatusLine()
        output = statusline.generate(input_data)

        # Output to stdout
        print(output)

    except InvalidJSONError as e:
        logger.error(f"Invalid JSON: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
