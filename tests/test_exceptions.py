"""
Tests for custom exceptions.
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from exceptions import (
    StatusLineError,
    ConfigurationError,
    FieldNotFoundError,
    InvalidJSONError,
    ValidationError
)
from display_formatter import StatusLineFormatter


class TestExceptionHierarchy:
    """Test exception inheritance and hierarchy."""

    def test_all_exceptions_inherit_from_statusline_error(self):
        """All custom exceptions should inherit from StatusLineError."""
        assert issubclass(ConfigurationError, StatusLineError)
        assert issubclass(FieldNotFoundError, StatusLineError)
        assert issubclass(InvalidJSONError, StatusLineError)
        assert issubclass(ValidationError, StatusLineError)

    def test_statusline_error_inherits_from_exception(self):
        """StatusLineError should inherit from Exception."""
        assert issubclass(StatusLineError, Exception)


class TestFieldNotFoundError:
    """Test FieldNotFoundError exception."""

    def test_field_not_found_error_stores_field_name(self):
        """FieldNotFoundError should store the field name."""
        error = FieldNotFoundError("missing_field")
        assert error.field_name == "missing_field"

    def test_field_not_found_error_message(self):
        """FieldNotFoundError should have informative message."""
        error = FieldNotFoundError("test_field")
        assert "test_field" in str(error)
        assert "not found" in str(error).lower()

    def test_formatter_raises_field_not_found_error(self):
        """StatusLineFormatter should raise FieldNotFoundError for invalid field."""
        formatter = StatusLineFormatter()
        with pytest.raises(FieldNotFoundError) as exc_info:
            formatter.get_field("nonexistent_field")

        assert exc_info.value.field_name == "nonexistent_field"


class TestConfigurationError:
    """Test ConfigurationError exception."""

    def test_configuration_error_can_be_raised(self):
        """ConfigurationError should be raisable with custom message."""
        with pytest.raises(ConfigurationError) as exc_info:
            raise ConfigurationError("Invalid config value")

        assert "Invalid config value" in str(exc_info.value)


class TestInvalidJSONError:
    """Test InvalidJSONError exception."""

    def test_invalid_json_error_can_be_raised(self):
        """InvalidJSONError should be raisable with custom message."""
        with pytest.raises(InvalidJSONError) as exc_info:
            raise InvalidJSONError("Malformed JSON")

        assert "Malformed JSON" in str(exc_info.value)


class TestValidationError:
    """Test ValidationError exception."""

    def test_validation_error_can_be_raised(self):
        """ValidationError should be raisable with custom message."""
        with pytest.raises(ValidationError) as exc_info:
            raise ValidationError("Invalid field value")

        assert "Invalid field value" in str(exc_info.value)


class TestExceptionCatching:
    """Test that exceptions can be caught properly."""

    def test_catch_specific_exception(self):
        """Specific exceptions should be catchable."""
        try:
            raise FieldNotFoundError("test")
        except FieldNotFoundError as e:
            assert e.field_name == "test"
        else:
            pytest.fail("Should have caught FieldNotFoundError")

    def test_catch_base_exception(self):
        """Base StatusLineError should catch all custom exceptions."""
        exceptions_to_test = [
            ConfigurationError("test"),
            FieldNotFoundError("test"),
            InvalidJSONError("test"),
            ValidationError("test")
        ]

        for exc in exceptions_to_test:
            try:
                raise exc
            except StatusLineError:
                pass  # Successfully caught
            else:
                pytest.fail(f"Should have caught {type(exc).__name__} as StatusLineError")
