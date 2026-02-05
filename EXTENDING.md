# Extending the Statusline Tool (v1.1.0+)

This guide explains how to add new fields and features to the Claude Code Statusline Tool using the object-oriented architecture (v1.0.3+) and facade pattern (v1.1.0+).

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Adding a New Field](#adding-a-new-field)
- [Adding a New Field Type](#adding-a-new-field-type)
- [Adding Custom Calculations](#adding-custom-calculations)
- [Adding a Field from External Data Sources](#adding-a-field-from-external-data-sources)
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

## Adding a Field from External Data Sources

Sometimes you need to display information that doesn't come from Claude's JSON output. The **git branch field** is a perfect real-world example that extracts data from an external source (the filesystem/git).

### Example: Git Branch Field (Real Implementation)

This example shows the complete pattern for adding a field that:
- Extracts data from an external source (not Claude's JSON)
- Uses a helper utility module
- Handles errors gracefully when data isn't available
- Caches results efficiently

#### Step 1: Create a Helper Utility

**File:** `src/git_utils.py`

```python
import os
import subprocess
from pathlib import Path
from typing import Optional
import constants


def get_git_branch(cwd: str) -> str:
    """
    Get current git branch name.

    Uses fast file-based detection with command fallback.

    Args:
        cwd: Current working directory path

    Returns:
        Git branch name, short commit hash (detached HEAD), or empty string
    """
    try:
        # Method 1: Read .git/HEAD directly (faster than git command)
        git_dir = Path(cwd) / ".git"

        if git_dir.is_file():
            # Handle git worktrees - .git is a file pointing to actual git dir
            with open(git_dir, 'r') as f:
                git_dir_line = f.read().strip()
                if git_dir_line.startswith('gitdir: '):
                    git_dir = Path(git_dir_line[8:])

        if git_dir.is_dir():
            head_file = git_dir / "HEAD"
            if head_file.exists():
                with open(head_file, 'r') as f:
                    content = f.read().strip()
                    if content.startswith(constants.GIT_HEAD_REF_PREFIX):
                        # Extract branch name after 'ref: refs/heads/'
                        return content[len(constants.GIT_HEAD_REF_PREFIX):]
                    # Detached HEAD state - return short commit hash
                    return content[:constants.GIT_DETACHED_HEAD_HASH_LENGTH]
    except (IOError, OSError):
        # File read failed, try git command
        pass

    try:
        # Method 2: Fall back to git command
        result = subprocess.run(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=constants.GIT_COMMAND_TIMEOUT_SECONDS
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (subprocess.SubprocessError, FileNotFoundError):
        # Git not installed or not a git repo
        pass

    # Return empty string if not in a git repository
    return ""
```

**Key Design Points:**
1. **Fast primary method**: Direct file reading is faster than shell commands
2. **Fallback mechanism**: Git command handles edge cases
3. **Graceful failure**: Returns empty string instead of crashing
4. **Edge cases handled**: Worktrees, detached HEAD, missing git
5. **Timeout protection**: Prevents hanging on slow operations

#### Step 2: Add Constants

**File:** `src/constants/display.py`

```python
# Git Settings
GIT_COMMAND_TIMEOUT_SECONDS = 0.5
GIT_HEAD_REF_PREFIX = "ref: refs/heads/"
GIT_DETACHED_HEAD_HASH_LENGTH = 7
```

**File:** `src/constants/fields.py`

```python
FIELD_GIT_BRANCH = "git_branch"
FIELD_LABELS[FIELD_GIT_BRANCH] = "Git branch:"
FIELD_ICON_KEYS[FIELD_GIT_BRANCH] = "git_branch"
```

**File:** `src/constants/display.py`

```python
DEFAULT_ICONS["git_branch"] = "🌿"
```

#### Step 3: Extract Data in DataExtractor

**File:** `src/data_extractor.py`

```python
import os
from typing import Dict, Any
from git_utils import get_git_branch


class DataExtractor:
    def _extract_workspace(self, json_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract workspace information.

        Includes current directory (basename only) and git branch.

        Args:
            json_data: Raw JSON data

        Returns:
            Dictionary with 'current_dir' and optionally 'git_branch' keys
        """
        data = {}
        if "workspace" in json_data and "current_dir" in json_data["workspace"]:
            cwd = json_data["workspace"]["current_dir"]
            data["current_dir"] = os.path.basename(cwd) or cwd

            # Get git branch for the workspace
            git_branch = get_git_branch(cwd)
            if git_branch:
                data["git_branch"] = git_branch

        return data
```

**Key Design Points:**
1. **Conditional inclusion**: Only add git_branch to data if available
2. **Use existing data**: Leverage the `cwd` from Claude's JSON
3. **No exceptions**: Helper returns empty string on failure
4. **Optional field**: Missing git branch doesn't break the statusline

#### Step 4: Register as SimpleField

**File:** `src/fields.py`

```python
def create_field_registry() -> Dict[str, Field]:
    return {
        # ... other fields ...
        constants.FIELD_GIT_BRANCH: SimpleField(
            name=constants.FIELD_GIT_BRANCH,
            icon_key=constants.ICON_KEY_GIT_BRANCH,
            line=constants.LINE_IDENTITY,
            label=constants.FIELD_LABELS[constants.FIELD_GIT_BRANCH]
        ),
    }
```

Git branch doesn't need custom formatting, so `SimpleField` is perfect.

#### Step 5: Add to Configuration Defaults

**File:** `src/constants/config.py`

```python
DEFAULT_VISIBLE_FIELDS = {
    # ... other fields ...
    FIELD_GIT_BRANCH: True,
}

DEFAULT_FIELD_ORDER = [
    # ... other fields ...
    FIELD_GIT_BRANCH,
]
```

### Testing External Data Fields

**File:** `tests/test_git_utils.py`

```python
import pytest
import sys
from pathlib import Path
from unittest.mock import patch, mock_open

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from git_utils import get_git_branch


def test_get_branch_from_git_head_file(tmp_path):
    """Test reading branch from .git/HEAD file."""
    git_dir = tmp_path / ".git"
    git_dir.mkdir()
    head_file = git_dir / "HEAD"
    head_file.write_text("ref: refs/heads/main\n")

    result = get_git_branch(str(tmp_path))
    assert result == "main"


def test_detached_head_state(tmp_path):
    """Test detached HEAD returns short commit hash."""
    git_dir = tmp_path / ".git"
    git_dir.mkdir()
    head_file = git_dir / "HEAD"
    head_file.write_text("a1b2c3d4e5f6g7h8i9j0")

    result = get_git_branch(str(tmp_path))
    assert result == "a1b2c3d"  # First 7 characters


def test_no_git_repository(tmp_path):
    """Test non-git directory returns empty string."""
    result = get_git_branch(str(tmp_path))
    assert result == ""


def test_git_worktree(tmp_path):
    """Test git worktree support."""
    # Create fake worktree setup
    git_file = tmp_path / ".git"
    actual_git_dir = tmp_path / ".git_worktree"
    actual_git_dir.mkdir()

    git_file.write_text(f"gitdir: {actual_git_dir}\n")
    head_file = actual_git_dir / "HEAD"
    head_file.write_text("ref: refs/heads/feature\n")

    result = get_git_branch(str(tmp_path))
    assert result == "feature"
```

### Pattern Summary: External Data Sources

Use this pattern for any external data source:

1. **Create a utility module** (`src/your_utils.py`) with:
   - Clear function signature with type hints
   - Multiple extraction methods (fast + fallback)
   - Exception handling for all failure modes
   - Return empty/default value on failure
   - Timeout protection for slow operations

2. **Add necessary constants** for:
   - Timeouts and limits
   - Default values
   - Configuration keys

3. **Extract in DataExtractor**:
   - Call utility function with required parameters
   - Only add to data dict if value is available
   - Don't propagate exceptions

4. **Choose appropriate Field type**:
   - `SimpleField` for basic display
   - `MetricField` if you need units/rates
   - Custom Field if you need special formatting

5. **Test thoroughly**:
   - Mock external dependencies
   - Test all failure modes
   - Verify graceful degradation
   - Test edge cases (worktrees, permissions, missing tools)

### Other Use Cases for External Data

This pattern works for:
- **Docker container info**: `docker ps` to show container status
- **Kubernetes context**: `kubectl config current-context`
- **Python virtual env**: Check `VIRTUAL_ENV` or `.venv`
- **Node version**: Parse `.nvmrc` or `package.json`
- **AWS profile**: Read from `~/.aws/config`
- **System metrics**: CPU, memory, disk usage
- **Time tracking**: Toggl, Clockify API
- **Calendar events**: Next meeting from Google Calendar API

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
