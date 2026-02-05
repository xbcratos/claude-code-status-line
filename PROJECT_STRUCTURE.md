# Claude Code Statusline - Project Structure

## Directory Layout

```
claude-code-statusline/
├── src/                          # Source code directory
│   ├── statusline.py             # Main entry point (reads stdin, outputs formatted line)
│   ├── config_manager.py         # Configuration file management
│   ├── configure.py              # Interactive CLI for configuration
│   ├── display_formatter.py      # Format and render the statusline
│   ├── git_utils.py              # Git branch detection utilities
│   └── colors.py                 # ANSI color codes and themes
├── tests/                        # Test suite (79+ unit tests)
│   ├── __init__.py               # Test package initializer
│   ├── test_colors.py            # Color module tests (10 tests)
│   ├── test_config_manager.py    # Config tests (13 tests)
│   ├── test_display_formatter.py # Formatter tests (21 tests)
│   ├── test_git_utils.py         # Git utility tests (10 tests)
│   └── test_statusline.py        # Statusline tests (25 tests)
├── install.sh                    # Installation script
├── requirements-test.txt         # Test dependencies (pytest, pytest-cov)
├── pytest.ini                    # Pytest configuration
├── README.md                     # Main documentation
├── QUICKSTART.md                 # Quick start guide
├── EXTENDING.md                  # Developer guide for extending functionality
├── FIELD_ORDERING.md             # Guide to field ordering
├── CHANGELOG.md                  # Version history
├── IMPROVEMENTS.md               # Code quality improvements log
├── LICENSE                       # MIT License
├── .gitignore                    # Git ignore rules
└── PROJECT_STRUCTURE.md          # This file

User Installation:
~/.claude-code-statusline/        # Installation directory
├── statusline.py                 # Installed main script
├── config_manager.py             # Installed config manager
├── configure.py                  # Installed config tool
├── display_formatter.py          # Installed formatter
├── git_utils.py                  # Installed git utils
├── colors.py                     # Installed color module
└── config.json                   # User configuration

Claude Code Settings:
~/.claude/settings.json           # Claude Code configuration
```

## Component Dependencies

```
statusline.py
├── config_manager.py
├── display_formatter.py
│   └── colors.py
└── git_utils.py

configure.py
├── config_manager.py
├── display_formatter.py
│   └── colors.py
└── colors.py
```

## Data Flow

```
Claude Code
    │
    ├─> Sends JSON via stdin
    │
    ▼
statusline.py
    │
    ├─> Reads config.json via config_manager.py
    ├─> Extracts data from JSON
    ├─> Gets git branch via git_utils.py
    ├─> Formats output via display_formatter.py
    │   └─> Applies colors via colors.py
    │
    └─> Outputs formatted statusline to stdout
    │
    ◀─┘
Claude Code displays statusline
```

## Module Descriptions

### statusline.py (Main Entry Point)
- Reads JSON from stdin
- Loads user configuration
- Extracts relevant fields
- Coordinates git detection
- Formats and outputs statusline

**Key Functions:**
- `main() -> None`: Entry point
- `extract_data(json_data: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]`: Parse Claude Code JSON

**Type Hints:** Full type annotations using Python 3.6+ typing module

### config_manager.py (Configuration Management)
- Manages configuration file I/O
- Provides defaults
- Validates configuration values
- Logs helpful error messages

**Key Functions:**
- `load_config() -> Dict[str, Any]`: Load user config
- `save_config(config: Dict[str, Any]) -> None`: Save config to file
- `get_default_config() -> Dict[str, Any]`: Return default configuration
- `ensure_config_exists() -> None`: Create config if missing
- `validate_config(config: Dict[str, Any]) -> Dict[str, Any]`: Validate and sanitize config

**Constants:**
- `VALID_COLORS`: List of valid color names
- `VALID_DISPLAY_MODES`: List of valid display modes
- `VALID_FIELD_NAMES`: List of valid field names
- `MIN_PROGRESS_BAR_WIDTH`, `MAX_PROGRESS_BAR_WIDTH`: Validation bounds

**Type Hints:** Full type annotations

### display_formatter.py (Output Formatting)
- Renders statusline in compact/verbose modes
- Formats progress bars
- Applies colors to fields
- Uses constants for line grouping (eliminates magic numbers)

**Constants:**
- `LINE_IDENTITY = 1`: Directory, branch, model, version, style
- `LINE_STATUS = 2`: Context, duration
- `LINE_METRICS = 3`: Cost, tokens, lines changed
- `FIELD_LINE_ASSIGNMENT`: Dictionary mapping fields to line numbers

**Key Functions:**
- `format_compact(data: Dict[str, Any], config: Dict[str, Any]) -> str`: Generate compact output
- `format_verbose(data: Dict[str, Any], config: Dict[str, Any]) -> str`: Generate verbose output
- `format_progress_bar(percentage: int, width: int, config: Dict[str, Any]) -> str`: Create progress bar
- `format_field(field_name: str, value: str, config: Dict[str, Any]) -> str`: Format individual field
- `format_duration(duration_ms: int) -> str`: Convert duration to readable format
- `_format_output(data, config, verbose=False)`: Common formatting logic (eliminates duplication)
- `_get_formatted_field_value(...)`: Helper for field formatting

**Type Hints:** Full type annotations

**Architecture:** Refactored in v1.0.2 to eliminate ~80% code duplication

### git_utils.py (Git Integration)
- Detects git branch
- Handles worktrees
- Graceful fallback
- Fast file-based detection with command fallback

**Key Functions:**
- `get_git_branch(cwd: str) -> str`: Get current branch name

**Performance:**
- Primary method: Fast `.git/HEAD` file reading
- Fallback: Git command with 0.5s timeout (reduced from 2s in v1.0.2)

**Type Hints:** Full type annotations

### colors.py (Color Management)
- ANSI color code definitions
- Color application functions
- NO_COLOR support
- Module-level color override for config-based disabling

**Module Variables:**
- `COLORS: Dict[str, str]`: ANSI color code mapping
- `_color_override: Optional[bool]`: Module-level override set by statusline.py

**Key Functions:**
- `colorize(text: str, color_name: str) -> str`: Apply color to text
- `is_color_enabled() -> bool`: Check color support
- `reset() -> str`: Return reset code

**Type Hints:** Full type annotations

### configure.py (Interactive Configuration)
- Menu-driven configuration
- Field toggling
- Icon/color customization
- Preview functionality

**Key Functions:**
- `main()`: Entry point for config tool
- `show_menu(config)`: Display main menu
- `toggle_fields_menu(config)`: Toggle field visibility
- `customize_icons_menu(config)`: Customize icons
- `customize_colors_menu(config)`: Customize colors
- `reorder_fields_menu(config)`: Reorder fields
- `preview_statusline(config)`: Preview with mock data

## Installation Flow

```
./install.sh
    │
    ├─> Create ~/.claude-code-statusline/
    ├─> Copy src/* to installation directory
    ├─> Make scripts executable
    ├─> Create symlink (optional)
    ├─> Generate default config.json
    └─> Update ~/.claude/settings.json (if needed)
```

## Configuration Schema

```json
{
  "display_mode": "compact" | "large",
  "visible_fields": {
    "field_name": boolean,
    ...
  },
  "field_order": ["field1", "field2", ...],
  "icons": {
    "field_name": "emoji",
    ...
  },
  "colors": {
    "field_name": "color_name",
    ...
  },
  "show_progress_bars": boolean,
  "progress_bar_width": number (5-50),
  "enable_colors": boolean
}
```

## Testing Strategy

### Automated Unit Testing (v1.0.2+)
- **79+ comprehensive unit tests** covering all modules
- Test framework: pytest
- Coverage: 53% overall, 92%+ on core modules
- Run with: `python3 -m pytest tests/`

**Test Coverage:**
- `test_colors.py`: 10 tests, 100% coverage
- `test_git_utils.py`: 10 tests, 100% coverage
- `test_display_formatter.py`: 21 tests, 92% coverage
- `test_statusline.py`: 25 tests, 92% coverage
- `test_config_manager.py`: 13 tests, 74% coverage

### Manual Testing
- Tests compact/verbose modes
- Tests color support
- Tests git integration
- Tests edge cases

### Integration Testing
- Install via install.sh
- Configure with Claude Code
- Run actual sessions
- Verify output correctness

## Performance Characteristics

- **Startup Time**: < 100ms typical
- **Memory Usage**: < 10MB
- **Dependencies**: Python stdlib only
- **Git Detection**: Fast file read, command fallback

## Extension Points

Future enhancements can add:
1. New fields in `extract_data()`
2. New display modes in `display_formatter.py`
3. New configuration options in config schema
4. New detection utilities (language versions, etc.)

## Maintenance

- Keep documentation synchronized with code
- Test on multiple Python versions (3.6+)
- Verify terminal compatibility
- Update CHANGELOG.md for releases
