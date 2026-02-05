# Extending the Statusline Tool (v1.1.0+)

This guide explains how to add new fields and features to the Claude Code Statusline Tool using the object-oriented architecture (v1.0.3+) and facade pattern (v1.1.0+).

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Adding a New Field](#adding-a-new-field)
- [Adding a New Field Type](#adding-a-new-field-type)
- [Adding Custom Calculations](#adding-custom-calculations)
- [Modifying Defaults](#modifying-defaults)
- [Testing Your Changes](#testing-your-changes)

---

## Architecture Overview

The tool uses an object-oriented architecture with Facade pattern (v1.1.0+):

- **`src/statusline.py`** - StatusLine facade class that orchestrates all components
- **`src/config_manager.py`** - ConfigManager class for loading/saving configuration with caching
- **`src/data_extractor.py`** - DataExtractor class for extracting and transforming JSON data
- **`src/display_formatter.py`** - StatusLineFormatter class that uses Field classes to format output
- **`src/fields.py`** - Field class hierarchy (SimpleField, ProgressField, MetricField, DurationField)
- **`src/models.py`** - Data models (StatusLineData, Configuration)
- **`src/constants/`** - Organized package with focused modules:
  - `constants/fields.py` - Field names, labels, icons, line assignments
  - `constants/colors.py` - Color definitions and mappings
  - `constants/config.py` - Configuration keys and defaults
  - `constants/display.py` - Display modes, icons, time formatting

### Key Architectural Benefits (v1.1.0)

The v1.1.0 architecture provides several benefits for extensibility:

1. **Organized Constants**: Split into focused modules, making it easier to find and modify related constants
2. **DataExtractor Class**: Extraction logic organized into focused methods following Single Responsibility Principle
3. **ConfigManager with Caching**: Stateful configuration management reduces file I/O
4. **StatusLine Facade**: Simplified API for programmatic use without CLI dependencies
5. **Dependency Injection**: All classes accept optional dependencies for easier testing and customization

---

## Adding a New Field

### Step 1: Add Constants

**Files:** `src/constants/fields.py`, `src/constants/colors.py`, `src/constants/config.py`

Add your field name constant and update the relevant dictionaries in the appropriate constants modules:

```python
# In src/constants/fields.py:
# Field Names
FIELD_YOUR_FIELD = "your_field"

# Add to valid field names list
VALID_FIELD_NAMES: List[str] = [
    # ... existing fields ...
    FIELD_YOUR_FIELD,
]

# Add to line assignment (where should it appear?)
FIELD_LINE_ASSIGNMENT: Dict[str, int] = {
    # ... existing assignments ...
    FIELD_YOUR_FIELD: LINE_METRICS,  # or LINE_IDENTITY or LINE_STATUS
}

# Add label for verbose mode
FIELD_LABELS: Dict[str, str] = {
    # ... existing labels ...
    FIELD_YOUR_FIELD: "Your Field:",
}

# Add icon key mapping
FIELD_ICON_KEYS: Dict[str, str] = {
    # ... existing mappings ...
    FIELD_YOUR_FIELD: "your_field",
}

# In src/constants/colors.py:
# Add default color
DEFAULT_COLORS: Dict[str, str] = {
    # ... existing colors ...
    FIELD_YOUR_FIELD: COLOR_CYAN,
}

# In src/constants/config.py:
# Add to defaults
DEFAULT_VISIBLE_FIELDS: Dict[str, bool] = {
    # ... existing fields ...
    FIELD_YOUR_FIELD: True,  # or False if hidden by default
}

DEFAULT_FIELD_ORDER: List[str] = [
    # ... existing fields ...
    FIELD_YOUR_FIELD,  # Position determines default order
]

# In src/constants/display.py:
# Add default icon
DEFAULT_ICONS: Dict[str, str] = {
    # ... existing icons ...
    "your_field": "🆕",
}
```

### Step 2: Extract Data from JSON

**File:** `src/data_extractor.py`

Add extraction logic in the `DataExtractor` class. You can either:

**Option A: Add a new extraction method** (recommended for complex fields):

```python
class DataExtractor:
    def extract(self, json_data: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
        data = {}
        # ... existing extraction calls ...
        data.update(self._extract_your_field(json_data))
        return data

    def _extract_your_field(self, json_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract your custom field."""
        data = {}
        if "your_field_location" in json_data:
            # Extract and process the value
            raw_value = json_data["your_field_location"]["field_name"]

            # Optional: Transform the value
            processed_value = self._transform_value(raw_value)

            data["your_field"] = processed_value
        return data
```

**Option B: Add to an existing extraction method** (for simple fields):

```python
# In an appropriate existing method like _extract_cost() or _extract_context()
def _extract_workspace(self, json_data: Dict[str, Any]) -> Dict[str, Any]:
    data = {}
    # ... existing code ...

    # Add your new field extraction
    if "api" in json_data and "total_calls" in json_data["api"]:
        data["api_calls"] = json_data["api"]["total_calls"]

    return data
```

### Step 3: Create Field Instance

**File:** `src/fields.py`

Add your field to the registry in `create_field_registry()`:

```python
def create_field_registry() -> Dict[str, Field]:
    """Create a registry of all available fields."""
    return {
        # ... existing fields ...
        constants.FIELD_YOUR_FIELD: SimpleField(
            name=constants.FIELD_YOUR_FIELD,
            icon_key="your_field",
            line=constants.LINE_METRICS,
            label=constants.FIELD_LABELS[constants.FIELD_YOUR_FIELD]
        ),
    }
```

**That's it!** The display formatter will automatically handle your new field.

---

## Adding a New Field Type

If your field needs custom formatting logic, create a new Field subclass.

**File:** `src/fields.py`

### Example: Adding a Temperature Field with Unit Conversion

```python
class TemperatureField(Field):
    """
    A field that displays temperature with optional unit conversion.
    """

    def format_value(self, data: Dict[str, Any], config: Dict[str, Any]) -> str:
        """Format temperature value with unit."""
        temp_celsius = data.get(self.name)
        if temp_celsius is None:
            return ""

        # Check if user wants Fahrenheit
        use_fahrenheit = config.get("use_fahrenheit", False)

        if use_fahrenheit:
            temp_fahrenheit = (temp_celsius * 9/5) + 32
            return f"{temp_fahrenheit:.1f}°F"
        else:
            return f"{temp_celsius:.1f}°C"
```

### Register Your New Field Type

```python
def create_field_registry() -> Dict[str, Field]:
    return {
        # ... existing fields ...
        constants.FIELD_CPU_TEMP: TemperatureField(
            name=constants.FIELD_CPU_TEMP,
            icon_key="temperature",
            line=constants.LINE_METRICS,
            label="CPU Temp:"
        ),
    }
```

---

## Adding Custom Calculations

### Example: Adding Response Time Average

**File:** `src/data_extractor.py`

```python
class DataExtractor:
    def _extract_performance(self, json_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract performance metrics with calculations."""
        data = {}

        if "performance" in json_data:
            perf = json_data["performance"]

            # Calculate average response time
            if "total_response_time_ms" in perf and "total_requests" in perf:
                total_time = perf["total_response_time_ms"]
                total_requests = perf["total_requests"]
                if total_requests > 0:
                    data["avg_response_time"] = total_time / total_requests

        return data

    def extract(self, json_data: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
        data = {}
        # ... existing extraction calls ...
        data.update(self._extract_performance(json_data))
        return data
```

**File:** `src/fields.py`

```python
class ResponseTimeField(MetricField):
    """Display average response time."""

    def format_value(self, data: Dict[str, Any], config: Dict[str, Any]) -> str:
        avg_time = data.get(self.name)
        if avg_time is None:
            return ""

        # Format with appropriate unit
        if avg_time < 1000:
            return f"{avg_time:.0f}ms"
        else:
            return f"{avg_time/1000:.2f}s"
```

---

## Modifying Defaults

All defaults are organized in the `src/constants/` package. Edit the appropriate module:

### Change Default Colors

**File:** `src/constants/colors.py`

```python
DEFAULT_COLORS: Dict[str, str] = {
    constants.FIELD_COST: COLOR_YELLOW,  # Changed from RED
    # ... other colors ...
}
```

### Change Default Icons

**File:** `src/constants/display.py`

```python
DEFAULT_ICONS: Dict[str, str] = {
    "model": "🔮",  # Changed from 🤖
    # ... other icons ...
}
```

### Change Default Field Order

**File:** `src/constants/config.py`

```python
DEFAULT_FIELD_ORDER: List[str] = [
    FIELD_MODEL,  # Put model first
    FIELD_CURRENT_DIR,
    # ... rest of fields ...
]
```

### Change Progress Bar Defaults

**File:** `src/constants/config.py`

```python
DEFAULT_PROGRESS_BAR_WIDTH = 15  # Changed from 10
MIN_PROGRESS_BAR_WIDTH = 10      # Changed from 5
MAX_PROGRESS_BAR_WIDTH = 30      # Changed from 50
```

---

## Testing Your Changes

### Step 1: Write Unit Tests

**File:** `tests/test_your_field.py`

```python
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from fields import YourFieldClass
from config_manager import get_default_config

def test_your_field_formatting():
    """Test your field formats correctly."""
    field = YourFieldClass(
        name="your_field",
        icon_key="your_icon",
        line=1,
        label="Your Field:"
    )

    data = {"your_field": "test_value"}
    config = get_default_config()

    result = field.format(data, config, verbose=False)
    assert "test_value" in result
```

### Step 2: Test with Mock Data

```bash
echo '{
  "model": {"id": "claude-sonnet-4"},
  "version": "v1.0.0",
  "your_field_location": {
    "field_name": "your_value"
  }
}' | python3 src/statusline.py
```

### Step 3: Run Full Test Suite

```bash
python3 -m pytest tests/ -v
```

### Step 4: Test in Configure Tool

```bash
python3 src/configure.py
# Navigate to preview to see your field
```

---

## Advanced: Custom Field with Conditional Logic

```python
class AdaptiveField(Field):
    """
    A field that changes its display based on value.
    """

    def format_value(self, data: Dict[str, Any], config: Dict[str, Any]) -> str:
        value = data.get(self.name)
        if value is None:
            return ""

        # Different formatting based on value
        if value < 10:
            return f"Low: {value}"
        elif value < 100:
            return f"Medium: {value}"
        else:
            return f"High: {value}"

    def format_compact(self, data: Dict[str, Any], config: Dict[str, Any]) -> str:
        """Override to add warning icon for high values."""
        value = data.get(self.name)
        if value and value >= 100:
            # Add warning icon
            return "⚠️ " + super().format_compact(data, config)
        return super().format_compact(data, config)
```

---

## Best Practices

1. **Use constants**: Never hardcode field names, colors, or icons
2. **Type hints**: Add type hints to all new functions
3. **Documentation**: Document your field's purpose and format
4. **Test coverage**: Write tests for new fields
5. **Single Responsibility**: Each Field class should do one thing
6. **Reuse existing types**: Use SimpleField, MetricField, etc. when possible
7. **Follow naming conventions**: Use clear, descriptive names

---

## Example: Complete End-to-End Addition

Let's add a "memory_used" field showing memory usage:

### 1. Constants

**File:** `src/constants/fields.py`
```python
FIELD_MEMORY_USED = "memory_used"

VALID_FIELD_NAMES = [..., FIELD_MEMORY_USED]
FIELD_LINE_ASSIGNMENT = {..., FIELD_MEMORY_USED: LINE_METRICS}
FIELD_LABELS = {..., FIELD_MEMORY_USED: "Memory:"}
FIELD_ICON_KEYS = {..., FIELD_MEMORY_USED: "memory"}
```

**File:** `src/constants/colors.py`
```python
DEFAULT_COLORS = {..., FIELD_MEMORY_USED: COLOR_MAGENTA}
```

**File:** `src/constants/config.py`
```python
DEFAULT_VISIBLE_FIELDS = {..., FIELD_MEMORY_USED: False}
DEFAULT_FIELD_ORDER = [..., FIELD_MEMORY_USED]
```

**File:** `src/constants/display.py`
```python
DEFAULT_ICONS = {..., "memory": "💾"}
```

### 2. Extraction (`src/data_extractor.py`)

```python
class DataExtractor:
    def _extract_system_info(self, json_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract system information like memory usage."""
        data = {}
        if "system" in json_data and "memory_mb" in json_data["system"]:
            data["memory_used"] = json_data["system"]["memory_mb"]
        return data

    def extract(self, json_data: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
        data = {}
        # ... existing extraction calls ...
        data.update(self._extract_system_info(json_data))
        return data
```

### 3. Field Class (`src/fields.py`)

```python
class MemoryField(MetricField):
    """Display memory usage with unit."""

    def format_value(self, data: Dict[str, Any], config: Dict[str, Any]) -> str:
        memory_mb = data.get(self.name)
        if memory_mb is None:
            return ""

        if memory_mb < 1024:
            return f"{memory_mb}MB"
        else:
            memory_gb = memory_mb / 1024
            return f"{memory_gb:.2f}GB"

# In create_field_registry():
constants.FIELD_MEMORY_USED: MemoryField(
    name=constants.FIELD_MEMORY_USED,
    icon_key="memory",
    line=constants.LINE_METRICS,
    label=constants.FIELD_LABELS[constants.FIELD_MEMORY_USED]
),
```

**Done!** Your field is now fully integrated.

---

## Need Help?

- Check existing fields in `src/fields.py` for examples
- See `PROJECT_STRUCTURE.md` for comprehensive architecture documentation
- See `CODE_REVIEW.md` for detailed architectural evolution and improvements
- Review `tests/` for testing patterns
- Open an issue on GitHub for questions
