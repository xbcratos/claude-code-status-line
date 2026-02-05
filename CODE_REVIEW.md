# Code Review: Version 1.0.3

Comprehensive code review identifying potential improvements for future versions.

## Executive Summary

**Overall Status:** ✅ Production-ready
- **Test Coverage:** 62% (90/90 tests passing)
- **Code Quality:** Good (SOLID principles applied, OOP architecture)
- **Technical Debt:** Low to Medium
- **Lines of Code:** 1,916 (well-structured)

---

## Priority 1: High Impact Improvements

### 1.1 Convert display_formatter.py to OOP Class

**Issue:** Module uses global variable for field registry
```python
# Current (module-level)
_field_registry: Dict[str, Field] = create_field_registry()

def get_field(field_name: str) -> Field:
    return _field_registry[field_name]
```

**Recommendation:** Create `StatusLineFormatter` class
```python
class StatusLineFormatter:
    """Formats statusline output using Field classes."""

    def __init__(self):
        self._field_registry = create_field_registry()

    def get_field(self, field_name: str) -> Field:
        return self._field_registry[field_name]

    def format(self, data: Dict[str, Any], config: Dict[str, Any],
               verbose: bool = False) -> str:
        # Current format_statusline logic
        pass
```

**Benefits:**
- Proper encapsulation
- Easier to test (can mock registry)
- Supports multiple formatter instances
- Aligns with OOP architecture

**Effort:** Medium (1-2 hours)
**Risk:** Low (well-tested code)

---

### 1.2 Convert config_manager.py to ConfigManager Class

**Issue:** Module-level functions make state management difficult
```python
# Current
def load_config() -> Dict[str, Any]: ...
def save_config(config: Dict[str, Any]) -> None: ...
```

**Recommendation:** Create `ConfigManager` class
```python
class ConfigManager:
    """Manages configuration loading, validation, and persistence."""

    def __init__(self, config_file: Path = CONFIG_FILE):
        self.config_file = config_file
        self._config: Optional[Dict[str, Any]] = None

    def load(self) -> Dict[str, Any]:
        if self._config is None:
            self._config = self._load_from_file()
        return self._config

    def save(self, config: Dict[str, Any]) -> None:
        self._validate(config)
        self._save_to_file(config)
        self._config = config

    def reload(self) -> Dict[str, Any]:
        self._config = None
        return self.load()
```

**Benefits:**
- Better state management (caching)
- Easier to test
- Support for multiple config files
- Clear ownership of config lifecycle

**Effort:** Medium (2-3 hours)
**Risk:** Medium (affects all imports)

---

### 1.3 Extract Data Extraction to Dedicated Class

**Issue:** `statusline.py::extract_data()` is 73 lines doing too much
```python
# Current: Single function with nested logic
def extract_data(json_data, config) -> Dict[str, Any]:
    # Model extraction (7 lines)
    # Context window extraction (15 lines)
    # Cost calculations (15 lines)
    # etc...
```

**Recommendation:** Create `DataExtractor` class with specialized methods
```python
class DataExtractor:
    """Extracts and transforms Claude Code JSON data."""

    def extract(self, json_data: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
        data = {}
        data.update(self._extract_model(json_data))
        data.update(self._extract_context(json_data))
        data.update(self._extract_workspace(json_data))
        data.update(self._extract_cost(json_data))
        data.update(self._extract_output_style(json_data))
        return data

    def _extract_model(self, json_data: Dict[str, Any]) -> Dict[str, Any]:
        # Model extraction logic
        pass

    def _extract_context(self, json_data: Dict[str, Any]) -> Dict[str, Any]:
        # Context window + tokens logic
        pass

    def _extract_cost(self, json_data: Dict[str, Any]) -> Dict[str, Any]:
        # Cost, duration, rates, lines_changed logic
        pass
```

**Benefits:**
- Single Responsibility Principle
- Easier to test each extraction method
- Easier to add new extractors
- Better code organization

**Effort:** Medium (2-3 hours)
**Risk:** Low (good test coverage)

---

### 1.4 Create StatusLine Facade Class

**Issue:** `statusline.py::main()` orchestrates too much
```python
# Current: main() does everything
def main():
    input_data = sys.stdin.read()
    json_data = json.loads(input_data)
    config = load_config()
    colors._color_override = ...  # Direct module manipulation
    data = extract_data(json_data, config)
    output = format_compact(data, config)
    print(output)
```

**Recommendation:** Create `StatusLine` facade class
```python
class StatusLine:
    """Facade for statusline generation workflow."""

    def __init__(self):
        self.config_manager = ConfigManager()
        self.data_extractor = DataExtractor()
        self.formatter = StatusLineFormatter()

    def generate(self, json_input: str) -> str:
        """Generate statusline from JSON input."""
        json_data = json.loads(json_input)
        config = self.config_manager.load()

        self._configure_colors(config)
        data = self.data_extractor.extract(json_data, config)

        return self.formatter.format(
            data,
            config,
            verbose=self._is_verbose(config)
        )

    def _configure_colors(self, config: Dict[str, Any]) -> None:
        # Color configuration logic
        pass

def main():
    """CLI entry point."""
    try:
        statusline = StatusLine()
        output = statusline.generate(sys.stdin.read())
        print(output)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
```

**Benefits:**
- Facade pattern simplifies usage
- Easy to test without CLI
- Clear separation of concerns
- Better for programmatic use

**Effort:** Medium (2-3 hours)
**Risk:** Low (facade wraps existing code)

---

## Priority 2: Medium Impact Improvements

### 2.1 Add Custom Exception Classes

**Issue:** Generic exceptions don't convey intent
```python
# Current
raise KeyError(f"Field {field_name} not found")
raise ValueError("Invalid configuration")
```

**Recommendation:** Create specific exceptions
```python
class StatusLineError(Exception):
    """Base exception for statusline errors."""
    pass

class ConfigurationError(StatusLineError):
    """Invalid configuration."""
    pass

class FieldNotFoundError(StatusLineError):
    """Field not found in registry."""
    def __init__(self, field_name: str):
        self.field_name = field_name
        super().__init__(f"Field '{field_name}' not found in registry")

class InvalidJSONError(StatusLineError):
    """Invalid JSON input."""
    pass
```

**Benefits:**
- Better error messages
- Easier to catch specific errors
- Better API for library usage

**Effort:** Low (1 hour)
**Risk:** Very Low

---

### 2.2 Improve Type Hints with TypedDict

**Issue:** Dictionaries lack type safety
```python
# Current
def format_statusline(data: Dict[str, Any], config: Dict[str, Any]) -> str:
    pass
```

**Recommendation:** Use TypedDict for known structures
```python
from typing import TypedDict, Optional

class ClaudeCodeInput(TypedDict, total=False):
    model: dict
    version: str
    context_window: dict
    workspace: dict
    cost: dict
    output_style: dict

class ExtractedData(TypedDict, total=False):
    model: str
    version: str
    current_dir: str
    git_branch: str
    context_remaining: int
    tokens: int
    cost: float
    duration: int
    # ...

def extract_data(json_data: ClaudeCodeInput, config: Dict[str, Any]) -> ExtractedData:
    pass
```

**Benefits:**
- IDE autocomplete
- Better type checking
- Self-documenting code
- Catch errors earlier

**Effort:** Medium (2-3 hours)
**Risk:** Low

---

### 2.3 Add Logging Module

**Issue:** Uses print to stderr, limited control
```python
# Current
print(f"Error: {e}", file=sys.stderr)
print(f"Warning: Invalid color '{color}'", file=sys.stderr)
```

**Recommendation:** Use logging module
```python
import logging

logger = logging.getLogger("claude_statusline")

# Usage
logger.error(f"Invalid JSON input: {e}")
logger.warning(f"Invalid color '{color}', using default")
logger.debug(f"Extracted data: {data}")
```

**Benefits:**
- Configurable log levels
- Can write to files
- Better for debugging
- Professional standard

**Effort:** Low (1-2 hours)
**Risk:** Very Low

---

### 2.4 Split Large Constants File

**Issue:** constants.py is 246 lines and growing
```
src/
├── constants/
│   ├── __init__.py          # Re-export all
│   ├── fields.py            # Field-related constants
│   ├── config.py            # Config-related constants
│   ├── colors.py            # Color constants
│   └── display.py           # Display constants
```

**Benefits:**
- Better organization
- Easier to navigate
- Logical grouping
- Easier to extend

**Effort:** Medium (2-3 hours)
**Risk:** Low (update imports)

---

### 2.5 Add Field Validation to Field Classes

**Issue:** No validation that data is appropriate for field type
```python
# Current: No validation
class MetricField(Field):
    def format_value(self, data, config):
        value = data.get(self.name)  # Could be anything
        return f"{value}"
```

**Recommendation:** Add validation methods
```python
class MetricField(Field):
    def validate(self, value: Any) -> bool:
        """Validate that value is numeric."""
        return isinstance(value, (int, float))

    def format_value(self, data, config):
        value = data.get(self.name)
        if value is not None and not self.validate(value):
            logger.warning(f"Invalid value for {self.name}: {value}")
            return ""
        # ... format logic
```

**Benefits:**
- Early error detection
- Better error messages
- Type safety at runtime
- Self-documenting expectations

**Effort:** Low (1-2 hours)
**Risk:** Low

---

## Priority 3: Code Quality Improvements

### 3.1 Reduce Complexity in extract_data()

**Current Cyclomatic Complexity:** ~15 (High)
**Target:** < 10 (Medium)

**Method:** Extract sub-functions (see 1.3 above)

---

### 3.2 Improve Test Coverage

**Current Coverage:** 62% overall
**Target:** 80%+

**Areas needing coverage:**
- `configure.py`: 0% (238 lines untested)
- `models.py`: 68% (30 lines untested)
- `config_manager.py`: 72% (19 lines untested)

**Recommendation:** Add tests for:
- `configure.py`: Mock user input, test menu flows
- `models.py`: Test all property methods
- `config_manager.py`: Test error paths

**Effort:** High (4-6 hours)
**Risk:** Very Low

---

### 3.3 Add Documentation Strings

**Issue:** Some methods lack docstrings
```python
# Missing docstrings in:
- Field.format_compact() - has docstring but minimal
- Field.format_verbose() - has docstring but minimal
- Some helper methods in fields.py
```

**Recommendation:** Add comprehensive docstrings with examples
```python
def format_compact(self, data: Dict[str, Any], config: Dict[str, Any]) -> str:
    """
    Format field in compact mode (icon + value).

    Args:
        data: Extracted data dictionary containing field values
        config: Configuration with icons, colors, and settings

    Returns:
        Formatted string like "📁 my-project" or empty string if no value

    Example:
        >>> field = SimpleField("current_dir", "directory", 1, "Directory:")
        >>> field.format_compact({"current_dir": "project"}, default_config)
        '📁 project'
    """
```

**Effort:** Low (1-2 hours)
**Risk:** Very Low

---

### 3.4 Add Performance Benchmarks

**Recommendation:** Add performance tests
```python
# tests/test_performance.py
def test_format_statusline_performance():
    """Statusline generation should complete in < 50ms."""
    import time

    config = get_default_config()
    data = generate_full_dataset()

    start = time.time()
    result = format_compact(data, config)
    elapsed = (time.time() - start) * 1000  # ms

    assert elapsed < 50, f"Formatting took {elapsed:.2f}ms (> 50ms)"
```

**Benefits:**
- Catch performance regressions
- Establish baselines
- Guide optimization efforts

**Effort:** Low (1 hour)
**Risk:** Very Low

---

### 3.5 Add Pre-commit Hooks

**Recommendation:** Add pre-commit configuration
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        language_version: python3

  - repo: https://github.com/PyCQA/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        args: [--max-line-length=120]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.3.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
```

**Benefits:**
- Consistent code style
- Catch errors before commit
- Automate quality checks

**Effort:** Low (1 hour)
**Risk:** Very Low

---

## Priority 4: Nice-to-Have Improvements

### 4.1 Add Caching to ConfigManager

**Recommendation:** Cache loaded config
```python
class ConfigManager:
    def __init__(self):
        self._cache: Optional[Dict[str, Any]] = None
        self._cache_time: Optional[float] = None

    def load(self, force_reload: bool = False) -> Dict[str, Any]:
        if force_reload or self._is_cache_stale():
            self._cache = self._load_from_file()
            self._cache_time = time.time()
        return self._cache
```

**Effort:** Low (1 hour)

---

### 4.2 Add Field Builder Pattern

**Recommendation:** Fluent API for creating fields
```python
field = FieldBuilder() \
    .name("custom_field") \
    .icon("🎯") \
    .color("cyan") \
    .line(LINE_METRICS) \
    .label("Custom:") \
    .build()
```

**Effort:** Medium (2 hours)

---

### 4.3 Add Plugin System for Custom Fields

**Recommendation:** Allow users to define custom fields
```python
# ~/.claude-code-statusline/plugins/my_field.py
from statusline.fields import Field

class MyCustomField(Field):
    def format_value(self, data, config):
        return "custom output"

# Automatically discovered and loaded
```

**Effort:** High (4-6 hours)

---

### 4.4 Add Configuration Migration System

**Recommendation:** Handle config schema changes
```python
class ConfigMigration:
    @staticmethod
    def migrate_v1_to_v2(old_config: dict) -> dict:
        """Migrate config from v1.0.2 to v1.0.3."""
        new_config = old_config.copy()
        # Handle schema changes
        return new_config
```

**Effort:** Medium (2-3 hours)

---

## Summary and Recommendations

### Immediate Actions (Next Version - 1.0.4)
1. ✅ Convert `display_formatter.py` to OOP class (Priority 1.1)
2. ✅ Add custom exception classes (Priority 2.1)
3. ✅ Add logging module (Priority 2.3)
4. ✅ Improve test coverage to 80%+ (Priority 3.2)

### Medium-term (Version 1.1.0)
1. ✅ Convert `config_manager.py` to class (Priority 1.2)
2. ✅ Extract data extraction to class (Priority 1.3)
3. ✅ Create StatusLine facade (Priority 1.4)
4. ✅ Add TypedDict for type safety (Priority 2.2)

### Long-term (Version 2.0.0)
1. ✅ Split constants into modules (Priority 2.4)
2. ✅ Add plugin system (Priority 4.3)
3. ✅ Add configuration migration (Priority 4.4)

### Estimated Total Effort
- Priority 1: 10-13 hours
- Priority 2: 9-12 hours
- Priority 3: 7-10 hours
- Priority 4: 9-13 hours

**Total:** 35-48 hours of development work

### Risk Assessment
- **Low Risk:** Priorities 2.1, 2.3, 3.1, 3.3, 3.4, 3.5, 4.1
- **Medium Risk:** Priorities 1.2, 2.2, 2.4, 4.2, 4.4
- **Higher Risk:** Priorities 1.1, 1.3, 1.4 (require careful refactoring)

---

## Conclusion

The codebase is in excellent shape for v1.0.3. The OOP refactoring provides a solid foundation for future improvements. The recommendations above focus on:

1. **Consistency**: Apply OOP principles throughout (not just fields)
2. **Testability**: Improve coverage and add performance tests
3. **Maintainability**: Better organization and documentation
4. **Extensibility**: Plugin system for custom fields

All improvements maintain backward compatibility and build upon the existing architecture.
