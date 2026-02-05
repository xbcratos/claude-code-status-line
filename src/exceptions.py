"""
Custom exceptions for the Claude Code Statusline Tool.

Provides specific exception types for better error handling and debugging.
"""


class StatusLineError(Exception):
    """
    Base exception for all statusline-related errors.

    All custom exceptions in this module inherit from this base class,
    making it easy to catch any statusline-specific error.
    """
    pass


class ConfigurationError(StatusLineError):
    """
    Raised when configuration is invalid or cannot be loaded.

    Examples:
        - Invalid JSON in config file
        - Missing required configuration keys
        - Invalid configuration values
    """
    pass


class FieldNotFoundError(StatusLineError):
    """
    Raised when a requested field is not found in the field registry.

    Attributes:
        field_name: The name of the field that was not found
    """

    def __init__(self, field_name: str):
        """
        Initialize with field name.

        Args:
            field_name: Name of the missing field
        """
        self.field_name = field_name
        super().__init__(f"Field '{field_name}' not found in registry")


class InvalidJSONError(StatusLineError):
    """
    Raised when JSON input cannot be parsed.

    This typically occurs when stdin contains malformed JSON data.
    """
    pass


class ValidationError(StatusLineError):
    """
    Raised when data validation fails.

    Examples:
        - Field value has wrong type
        - Value out of expected range
        - Required field missing
    """
    pass
