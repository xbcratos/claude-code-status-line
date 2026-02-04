# Extending the Statusline Tool

This guide explains how to add new fields and features to the Claude Code Statusline Tool.

## Table of Contents

- [Adding a New Field](#adding-a-new-field)
- [Adding a New Display Mode](#adding-a-new-display-mode)
- [Adding Custom Calculations](#adding-custom-calculations)
- [Adding New Color Options](#adding-new-color-options)
- [Testing Your Changes](#testing-your-changes)

---

## Adding a New Field

Follow these steps to add a new field (e.g., "session_duration" or "api_calls").

### Step 1: Update Default Configuration

**File:** `src/config_manager.py`

Add your field to the default config in three places:

```python
def get_default_config():
    return {
        # ... existing config ...
        "visible_fields": {
            # ... existing fields ...
            "your_new_field": True,  # ← Add here
        },
        "field_order": [
            # ... existing fields ...
            "your_new_field",  # ← Add here (position determines default order)
        ],
        "icons": {
            # ... existing icons ...
            "your_new_field": "🆕",  # ← Add your icon here
        },
        "colors": {
            # ... existing colors ...
            "your_new_field": "cyan",  # ← Add your color here
        }
    }
```

### Step 2: Extract Data from JSON

**File:** `src/statusline.py`

Add extraction logic in the `extract_data()` function:

```python
def extract_data(json_data, config):
    """Extract relevant fields from Claude Code JSON input."""
    data = {}

    # ... existing extraction code ...

    # Add your new field extraction
    if "your_field_location" in json_data:
        # Extract and process the value
        raw_value = json_data["your_field_location"]["field_name"]

        # Optional: Transform the value (e.g., format, calculate)
        processed_value = transform_value(raw_value)

        data["your_new_field"] = processed_value

    return data
```

**Example: Adding API call count**

```python
# In extract_data() function:
if "api" in json_data and "total_calls" in json_data["api"]:
    data["api_calls"] = json_data["api"]["total_calls"]
```

### Step 3: Update Display Formatters

**File:** `src/display_formatter.py`

Add your field to both display modes:

```python
def format_compact(data, config):
    """Generate compact format statusline."""
    # ... existing code ...

    # Add your field to the appropriate line
    if visible.get("your_new_field") and data.get("your_new_field"):
        # Format the field value
        formatted = format_field("your_new_field", data["your_new_field"], config)
        line_parts.append(formatted)

    # ... rest of function ...
```

```python
def format_large(data, config):
    """Generate large format statusline."""
    # ... existing code ...

    # Add your field (same logic as compact)
    if visible.get("your_new_field") and data.get("your_new_field"):
        formatted = format_field("your_new_field", data["your_new_field"], config)
        line_parts.append(formatted)

    # ... rest of function ...
```

**Tip:** Decide which line your field belongs on based on its category:
- **Line 1**: Identity fields (directory, branch, model, version)
- **Line 2**: Status fields (context, duration, progress)
- **Line 3**: Metrics fields (cost, tokens, statistics)

### Step 4: Update Configuration Tool

**File:** `src/configure.py`

Add your field to the toggle menu:

```python
def toggle_fields_menu(config):
    """Menu for toggling visible fields."""
    # ... existing code ...

    field_names = {
        # ... existing fields ...
        "11": ("your_new_field", "Your New Field Label"),  # ← Add here
    }

    # ... rest of function ...
```

Add icon customization:

```python
def customize_icons_menu(config):
    """Menu for customizing icons."""
    # ... existing code ...

    icon_names = {
        # ... existing icons ...
        "10": ("your_new_field", "Your New Field"),  # ← Add here
    }

    # ... rest of function ...
```

Add color customization:

```python
def customize_colors_menu(config):
    """Menu for customizing colors."""
    # ... existing code ...

    color_fields = {
        # ... existing fields ...
        "13": ("your_new_field", "Your New Field"),  # ← Add here
    }

    # ... rest of function ...
```

### Step 5: Update Documentation

**Files:** `README.md`, `EXAMPLES.md`

Add your field to the list of available fields:

```markdown
### Available Fields

- **Your New Field**: Description of what it shows
- Model: Claude model name
- ... (existing fields)
```

### Step 6: Test Your Changes

Create a test JSON file:

```bash
cat > /tmp/test_new_field.json << 'EOF'
{
  "model": {"display_name": "Sonnet 4"},
  "your_field_location": {
    "field_name": "test_value"
  }
}
EOF

python3 src/statusline.py < /tmp/test_new_field.json
```

---

## Adding a New Display Mode

To add a display mode beyond "compact" and "large":

### Step 1: Add Format Function

**File:** `src/display_formatter.py`

```python
def format_your_mode(data, config):
    """Generate your custom format."""
    lines = []
    visible = config["visible_fields"]
    separator = colorize("  ", config["colors"].get("separator", "white"))

    # Build your custom layout
    # Example: single line with all fields
    all_parts = []

    for field in config["field_order"]:
        if visible.get(field) and data.get(field):
            formatted = format_field(field, data[field], config)
            all_parts.append(formatted)

    lines.append(separator.join(all_parts))
    return "\n".join(lines)
```

### Step 2: Update Main Script

**File:** `src/statusline.py`

```python
def main():
    # ... existing code ...

    display_mode = config.get("display_mode", "compact")

    if display_mode == "large":
        output = format_large(data, config)
    elif display_mode == "your_mode":  # ← Add here
        output = format_your_mode(data, config)
    else:
        output = format_compact(data, config)

    # ... rest of function ...
```

### Step 3: Update Configuration Menu

**File:** `src/configure.py`

```python
def display_mode_menu(config):
    """Menu for changing display mode."""
    # ... existing code ...

    print("1. Compact")
    print("2. Large")
    print("3. Your Mode")  # ← Add here

    # ... handle choice ...

    if choice == "3":
        config["display_mode"] = "your_mode"
```

---

## Adding Custom Calculations

To add derived/calculated fields:

### Example: Adding "tokens_remaining"

**File:** `src/statusline.py`

```python
def extract_data(json_data, config):
    # ... existing extraction ...

    # Calculate derived value
    if "context_window" in json_data:
        total = json_data["context_window"].get("total_tokens", 0)
        used_input = json_data["context_window"].get("total_input_tokens", 0)
        used_output = json_data["context_window"].get("total_output_tokens", 0)

        # Calculate remaining
        data["tokens_remaining"] = total - used_input - used_output

    return data
```

### Example: Adding "efficiency_score"

```python
# In extract_data():
if data.get("cost") and data.get("tokens"):
    # Calculate cost per 1K tokens
    data["efficiency_score"] = (data["cost"] / data["tokens"]) * 1000
```

---

## Adding New Color Options

To add additional colors beyond the 7 defaults:

### Step 1: Add Color Code

**File:** `src/colors.py`

```python
COLORS = {
    # ... existing colors ...
    "orange": "\033[38;5;208m",      # 256-color orange
    "purple": "\033[38;5;141m",      # 256-color purple
    "pink": "\033[38;5;213m",        # 256-color pink
}
```

### Step 2: Update Documentation

**File:** `src/configure.py`

```python
def customize_colors_menu(config):
    # ... existing code ...

    print()
    print("Available colors: cyan, green, blue, magenta, yellow, red, white, orange, purple, pink")
    print()

    # ... update valid_colors list ...
    valid_colors = ["cyan", "green", "blue", "magenta", "yellow", "red", "white",
                    "orange", "purple", "pink"]
```

---

## Complete Example: Adding "Files Modified" Field

Here's a complete walkthrough:

### 1. Update config_manager.py

```python
def get_default_config():
    return {
        "visible_fields": {
            # ... existing ...
            "files_modified": False,  # New field, disabled by default
        },
        "field_order": [
            # ... existing ...
            "lines_changed",
            "files_modified",  # Add after lines_changed
        ],
        "icons": {
            # ... existing ...
            "files_modified": "📝",
        },
        "colors": {
            # ... existing ...
            "files_modified": "cyan",
        }
    }
```

### 2. Update statusline.py

```python
def extract_data(json_data, config):
    # ... existing code ...

    # Files modified
    if "cost" in json_data:
        files_added = json_data["cost"].get("total_files_added", 0)
        files_modified = json_data["cost"].get("total_files_modified", 0)
        files_removed = json_data["cost"].get("total_files_removed", 0)

        total_files = files_added + files_modified + files_removed
        if total_files > 0:
            data["files_modified"] = f"{total_files} files"

    return data
```

### 3. Update display_formatter.py

```python
def format_compact(data, config):
    # ... in the cost_parts section (Line 3) ...

    if visible.get("files_modified") and data.get("files_modified"):
        files_parts.append(format_field("files_modified", data["files_modified"], config))
```

### 4. Update configure.py

```python
# In toggle_fields_menu:
field_names = {
    # ... existing ...
    "11": ("files_modified", "Files Modified"),
}

# In customize_icons_menu:
icon_names = {
    # ... existing ...
    "10": ("files_modified", "Files Modified"),
}

# In customize_colors_menu:
color_fields = {
    # ... existing ...
    "13": ("files_modified", "Files Modified"),
}
```

### 5. Test

```bash
echo '{"cost":{"total_files_added":3,"total_files_modified":5,"total_files_removed":1}}' | python3 src/statusline.py
```

Expected output:
```
📝 9 files
```

---

## Testing Your Changes

### Unit Testing

Create a test script:

```bash
cat > test_my_field.sh << 'EOF'
#!/bin/bash

echo "Testing new field..."

# Test 1: Field appears when data present
echo '{"your_field_location":{"field_name":"test"}}' | python3 src/statusline.py

# Test 2: Field absent when data missing
echo '{}' | python3 src/statusline.py

# Test 3: Field respects visibility toggle
# ... create config with field disabled ...

echo "Tests complete"
EOF
```

### Integration Testing

1. Install your modified version: `./install.sh`
2. Run Claude Code with the statusline
3. Verify field appears correctly
4. Test configuration tool: `claude-statusline-config`
5. Toggle your field on/off
6. Change icon and color
7. Verify persistence (restart and check)

---

## Best Practices

### 1. Graceful Degradation
Always check if data exists before using it:

```python
# Good
if "field" in json_data and json_data["field"]:
    data["my_field"] = json_data["field"]

# Bad
data["my_field"] = json_data["field"]  # Will crash if missing
```

### 2. Meaningful Defaults
Choose sensible defaults for new fields:
- Disabled by default for optional/niche features
- Enabled by default for widely useful features
- Appropriate icons that clearly represent the field
- Colors that match the field's semantic meaning

### 3. Documentation
Always update:
- README.md (available fields list)
- EXAMPLES.md (show your field in examples)
- CHANGELOG.md (document the addition)

### 4. Configuration Tool
Make fields accessible via the interactive CLI:
- Add to field toggle menu
- Add to icon customization
- Add to color customization
- Update field reordering if needed

---

## Common Extension Patterns

### Pattern 1: Simple Value Display
Just show a value from the JSON:

```python
if "simple_field" in json_data:
    data["simple_field"] = json_data["simple_field"]
```

### Pattern 2: Formatted Value
Transform before displaying:

```python
if "timestamp" in json_data:
    ts = json_data["timestamp"]
    data["formatted_time"] = datetime.fromtimestamp(ts).strftime("%H:%M")
```

### Pattern 3: Calculated Value
Derive from multiple sources:

```python
if "requests" in json_data and "errors" in json_data:
    total = json_data["requests"]
    errors = json_data["errors"]
    success_rate = ((total - errors) / total) * 100
    data["success_rate"] = f"{success_rate:.1f}%"
```

### Pattern 4: Conditional Display
Only show under certain conditions:

```python
if data.get("cost", 0) > 10:
    data["high_cost_warning"] = "⚠️  High cost"
```

---

## Troubleshooting

### Field Not Appearing

1. Check `visible_fields` - is it enabled?
2. Check data extraction - is `data["field"]` set?
3. Check display formatter - is field in the right line?
4. Check config order - is field in `field_order`?

### Configuration Not Saving

1. Check `config_manager.py` - is field in default config?
2. Verify JSON format - run through validator
3. Check file permissions on `~/.claude-code-statusline/config.json`

### Colors Not Working

1. Check `colors.py` - is color defined?
2. Verify color name spelling matches exactly
3. Test with `NO_COLOR=0` to ensure colors are enabled
4. Check terminal supports ANSI colors

---

## Questions?

For issues or questions:
- Check existing fields for patterns to follow
- Review the modular architecture in PROJECT_STRUCTURE.md
- Test incrementally - add one piece at a time
- Use the test suite as a reference

Happy extending! 🚀
