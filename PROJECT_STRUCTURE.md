# Claude Code Statusline - Project Structure

## Directory Layout

```
claude-code-statusline/
├── src/                          # Source code directory
│   ├── statusline.py             # Main entry point (reads stdin, outputs formatted line)
│   ├── config_manager.py         # Configuration file management
│   ├── configure.py              # Interactive CLI for configuration
│   ├── display_formatter.py      # Format and render the statusline (uses Field classes)
│   ├── git_utils.py              # Git branch detection utilities
│   ├── colors.py                 # ANSI color codes and themes
│   ├── constants.py              # All constants, defaults, and validation rules (v1.0.3+)
│   ├── fields.py                 # Field class hierarchy (SimpleField, ProgressField, etc.) (v1.0.3+)
│   └── models.py                 # Data models (StatusLineData, Configuration) (v1.0.3+)
├── tests/                        # Test suite (90 tests: 79 unit + 11 integration)
│   ├── __init__.py               # Test package initializer
│   ├── test_colors.py            # Color module tests (10 tests)
│   ├── test_config_manager.py    # Config tests (13 tests)
│   ├── test_display_formatter.py # Formatter tests (21 tests)
│   ├── test_git_utils.py         # Git utility tests (10 tests)
│   ├── test_statusline.py        # Statusline tests (25 tests)
│   └── test_integration.py       # Integration tests (11 tests)
├── install.sh                    # Installation script
├── install_helper.py             # Installation helper (called by install.sh)
├── requirements-test.txt         # Test dependencies (pytest, pytest-cov)
├── pytest.ini                    # Pytest configuration
├── README.md                     # Main documentation
├── QUICKSTART.md                 # Quick start guide
├── EXTENDING.md                  # Developer guide for extending functionality (OOP architecture)
├── FIELD_ORDERING.md             # Guide to field ordering
├── OOP_REFACTORING.md            # OOP architecture documentation (v1.0.3+)
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
├── constants.py                  # Installed constants (v1.0.3+)
├── fields.py                     # Installed field classes (v1.0.3+)
├── models.py                     # Installed data models (v1.0.3+)
└── config.json                   # User configuration

Claude Code Settings:
~/.claude/settings.json           # Claude Code configuration
```

## Component Dependencies

```
statusline.py
├── config_manager.py
│   └── constants.py
├── display_formatter.py
│   ├── colors.py
│   ├── constants.py
│   ├── fields.py
│   │   ├── constants.py
│   │   └── colors.py
│   └── models.py
│       └── constants.py
└── git_utils.py
    └── constants.py

configure.py
├── config_manager.py
│   └── constants.py
├── display_formatter.py
│   ├── colors.py
│   ├── constants.py
│   ├── fields.py
│   └── models.py
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
    ├─> Reads config.json via config_manager.py (uses constants.py)
    ├─> Extracts data from JSON
    ├─> Gets git branch via git_utils.py (uses constants.py)
    ├─> Formats output via display_formatter.py
    │   ├─> Uses Field classes (fields.py) for formatting
    │   ├─> Uses constants.py for defaults and validation
    │   ├─> Uses models.py for typed data access
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
- Provides defaults from constants.py
- Validates configuration values using constants.py
- Logs helpful error messages

**Key Functions:**
- `load_config() -> Dict[str, Any]`: Load user config
- `save_config(config: Dict[str, Any]) -> None`: Save config to file
- `get_default_config() -> Dict[str, Any]`: Return default configuration using constants
- `ensure_config_exists() -> None`: Create config if missing
- `validate_config(config: Dict[str, Any]) -> Dict[str, Any]`: Validate using constants

**Type Hints:** Full type annotations

**Architecture (v1.0.3+):** Uses constants.py for all defaults and validation rules

### display_formatter.py (Output Formatting)
- Renders statusline in compact/verbose modes using Field classes
- Coordinates field formatting through Field class hierarchy
- Uses constants.py for line grouping and defaults
- Uses models.py for typed data access

**Key Functions:**
- `format_statusline(data, config, verbose=False) -> str`: Unified formatter using Field classes
- `format_compact(data: Dict[str, Any], config: Dict[str, Any]) -> str`: Generate compact output
- `format_verbose(data: Dict[str, Any], config: Dict[str, Any]) -> str`: Generate verbose output
- `get_field(field_name: str) -> Field`: Get field instance from registry
- Legacy functions for backward compatibility: `format_progress_bar`, `format_field`, `format_duration`

**Type Hints:** Full type annotations

**Architecture:**
- v1.0.2: Eliminated ~80% code duplication
- v1.0.3: OOP refactoring with Field classes - each field knows how to format itself

### git_utils.py (Git Integration)
- Detects git branch
- Handles worktrees
- Graceful fallback
- Fast file-based detection with command fallback
- Uses constants.py for configuration values

**Key Functions:**
- `get_git_branch(cwd: str) -> str`: Get current branch name

**Performance:**
- Primary method: Fast `.git/HEAD` file reading
- Fallback: Git command with 0.5s timeout (reduced from 2s in v1.0.2)

**Type Hints:** Full type annotations

**Architecture (v1.0.3+):** Uses constants.py for timeout values and git prefixes

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

### constants.py (Constants and Defaults) [v1.0.3+]
- Centralized constants, defaults, and validation rules
- Eliminates hardcoded values throughout codebase
- Single source of truth for all configuration

**Constants Defined:**
- Field name constants: `FIELD_MODEL`, `FIELD_VERSION`, `FIELD_COST`, etc.
- Display modes: `DISPLAY_MODE_COMPACT`, `DISPLAY_MODE_VERBOSE`
- Line assignments: `LINE_IDENTITY`, `LINE_STATUS`, `LINE_METRICS`
- Default colors: `DEFAULT_COLORS` dictionary
- Default icons: `DEFAULT_ICONS` dictionary
- Valid values: `VALID_COLORS`, `VALID_DISPLAY_MODES`, `VALID_FIELD_NAMES`
- Configuration defaults: `DEFAULT_VISIBLE_FIELDS`, `DEFAULT_FIELD_ORDER`
- Time conversion constants: `MILLISECONDS_PER_SECOND`, `SECONDS_PER_MINUTE`, etc.
- Git constants: `GIT_HEAD_REF_PREFIX`, `GIT_COMMAND_TIMEOUT_SECONDS`

**Type Hints:** Full type annotations

**Architecture:** Foundation of OOP refactoring - all modules import constants instead of using magic values

### fields.py (Field Class Hierarchy) [v1.0.3+]
- Object-oriented field formatting architecture
- Each field knows how to format itself
- Eliminates code duplication in display_formatter.py

**Field Classes:**
- `Field` (ABC): Base class with `format()`, `format_compact()`, `format_verbose()` methods
- `SimpleField`: Direct value display (model, version, directory, git_branch)
- `ProgressField`: Percentage with optional progress bar (context_remaining)
- `MetricField`: Metrics with optional rates (tokens with tpm, cost with $/h)
- `DurationField`: Time formatting from milliseconds (duration)

**Key Functions:**
- `create_field_registry() -> Dict[str, Field]`: Creates registry of all available fields

**Type Hints:** Full type annotations with ABC for base class

**Architecture:** Implements Strategy pattern - each field type encapsulates formatting logic

### models.py (Data Models) [v1.0.3+]
- Typed interfaces for data and configuration
- Provides property-based access with type safety
- Improves code readability and maintainability

**Classes:**
- `StatusLineData`: Typed wrapper for extracted data dictionary with properties for each field
- `Configuration`: Typed wrapper for configuration dictionary with helper methods

**Type Hints:** Full type annotations

**Architecture:** Provides type-safe access layer over raw dictionaries

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
    ├─> Generate default config.json (via install_helper.py)
    └─> Update ~/.claude/settings.json (via install_helper.py)
```

## Configuration Schema

```json
{
  "display_mode": "compact" | "verbose",
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

### Automated Testing (v1.0.2+)
- **90 comprehensive tests** (79 unit + 11 integration)
- Test framework: pytest
- Coverage: 53% overall, 92%+ on core modules
- Run with: `python3 -m pytest tests/`

**Test Coverage:**
- `test_colors.py`: 10 tests, 100% coverage
- `test_git_utils.py`: 10 tests, 100% coverage
- `test_display_formatter.py`: 21 tests, 92% coverage
- `test_statusline.py`: 25 tests, 92% coverage
- `test_config_manager.py`: 13 tests, 74% coverage
- `test_integration.py`: 11 integration tests (v1.0.3+)
  - Full statusline output verification with icons
  - End-to-end workflow testing
  - Installation helper testing
  - Visual output validation

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

The OOP architecture (v1.0.3+) makes extension easy:

1. **New fields**: Add constants, extract data in `statusline.py`, create Field instance in `fields.py` registry
2. **Custom field types**: Subclass `Field` in `fields.py` for custom formatting logic
3. **New configuration options**: Add defaults to `constants.py`, validation to `config_manager.py`
4. **New detection utilities**: Add to `git_utils.py` or create new utility modules

See `EXTENDING.md` for detailed step-by-step guides and examples.

## Maintenance

- Keep documentation synchronized with code
- Test on multiple Python versions (3.6+)
- Verify terminal compatibility
- Update CHANGELOG.md for releases
