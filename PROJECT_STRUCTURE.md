# Claude Code Statusline - Project Structure

## Directory Layout

```
claude-code-statusline/
├── src/                          # Source code directory
│   ├── statusline.py             # Main entry point with StatusLine facade class (v1.1.0+)
│   ├── config_manager.py         # ConfigManager class for stateful config management (v1.1.0+)
│   ├── data_extractor.py         # DataExtractor class for JSON data extraction (v1.1.0+)
│   ├── configure.py              # Interactive CLI for configuration
│   ├── display_formatter.py      # StatusLineFormatter class for rendering (v1.0.4+)
│   ├── git_utils.py              # Git branch detection utilities
│   ├── colors.py                 # ANSI color codes and themes
│   ├── constants/                # Organized constants modules (v1.1.0+)
│   │   ├── __init__.py           # Re-exports all constants for compatibility
│   │   ├── fields.py             # Field names, labels, icons, line assignments
│   │   ├── colors.py             # Color definitions and default mappings
│   │   ├── config.py             # Configuration keys and defaults
│   │   └── display.py            # Display modes, icons, time formatting, git settings
│   ├── fields.py                 # Field class hierarchy (SimpleField, ProgressField, etc.) (v1.0.3+)
│   ├── models.py                 # Data models (StatusLineData, Configuration) (v1.0.3+)
│   └── exceptions.py             # Custom exception hierarchy (v1.0.4+)
├── tests/                        # Test suite (232 tests, 75% coverage)
│   ├── __init__.py               # Test package initializer
│   ├── test_colors.py            # Color module tests (10 tests)
│   ├── test_config_manager.py    # ConfigManager tests (20 tests)
│   ├── test_display_formatter.py # Formatter tests (25 tests)
│   ├── test_exceptions.py        # Exception hierarchy tests (10 tests) (v1.0.4+)
│   ├── test_git_utils.py         # Git utility tests (10 tests)
│   ├── test_models.py            # Data model tests (54 tests) (v1.0.4+)
│   ├── test_statusline.py        # Statusline tests (21 tests)
│   └── test_integration.py       # Integration tests (11 tests)
├── install.sh                    # Installation script
├── install_helper.py             # Installation helper (called by install.sh)
├── requirements-test.txt         # Test dependencies (pytest, pytest-cov)
├── pytest.ini                    # Pytest configuration
├── README.md                     # Main documentation
├── QUICKSTART.md                 # Quick start guide
├── EXTENDING.md                  # Developer guide for extending functionality
├── FIELD_ORDERING.md             # Guide to field ordering
├── CODE_REVIEW.md                # Comprehensive code review and roadmap
├── CHANGELOG.md                  # Version history
├── LICENSE                       # MIT License
├── .gitignore                    # Git ignore rules
└── PROJECT_STRUCTURE.md          # This file

User Installation:
~/.claude-code-statusline/        # Installation directory
├── statusline.py                 # Installed main script
├── config_manager.py             # Installed ConfigManager
├── data_extractor.py             # Installed DataExtractor
├── configure.py                  # Installed config tool
├── display_formatter.py          # Installed StatusLineFormatter
├── git_utils.py                  # Installed git utils
├── colors.py                     # Installed color module
├── constants/                    # Installed constants package
│   ├── __init__.py
│   ├── fields.py
│   ├── colors.py
│   ├── config.py
│   └── display.py
├── fields.py                     # Installed field classes
├── models.py                     # Installed data models
├── exceptions.py                 # Installed exceptions
└── config.json                   # User configuration

Claude Code Settings:
~/.claude/settings.json           # Claude Code configuration
```

## Component Dependencies (v1.1.0 Architecture)

```
statusline.py
├── StatusLine (facade class)
│   ├── ConfigManager
│   │   └── constants/
│   ├── DataExtractor
│   │   ├── git_utils
│   │   │   └── constants/
│   │   └── constants/
│   └── StatusLineFormatter
│       ├── fields
│       │   ├── constants/
│       │   └── colors
│       ├── models
│       │   └── constants/
│       └── colors
├── exceptions
└── colors

configure.py
├── config_manager
│   └── constants/
├── display_formatter
│   ├── colors
│   ├── constants/
│   ├── fields
│   └── models
└── colors
```

## Data Flow (v1.1.0)

```
Claude Code
    │
    ├─> Sends JSON via stdin
    │
    ▼
statusline.py::main()
    │
    ├─> Creates StatusLine facade
    │   │
    │   ├─> StatusLine.generate(json_input)
    │       │
    │       ├─> ConfigManager.load()
    │       │   └─> Validates using constants/
    │       │
    │       ├─> DataExtractor.extract()
    │       │   ├─> Extracts model, version, context, workspace
    │       │   ├─> Gets git branch via git_utils
    │       │   └─> Calculates rates and metrics
    │       │
    │       └─> StatusLineFormatter.format()
    │           ├─> Uses Field classes for formatting
    │           ├─> Uses models for typed data access
    │           ├─> Uses constants/ for defaults
    │           └─> Applies colors via colors module
    │
    └─> Outputs formatted statusline to stdout
    │
    ◀─┘
Claude Code displays statusline
```

## Module Descriptions

### statusline.py (Main Entry Point) [v1.1.0]
Main CLI entry point with StatusLine facade class for orchestration.

**Classes:**
- `StatusLine`: Facade that coordinates ConfigManager, DataExtractor, and StatusLineFormatter
  - `generate(json_input: str) -> str`: Main API for generating statusline

**Key Functions:**
- `main() -> None`: CLI entry point (simplified to 15 lines in v1.1.0)
- `_configure_logging() -> None`: Set up logging based on LOG_LEVEL env var

**Type Hints:** Full type annotations

**Architecture:**
- v1.0.0-1.0.3: Procedural with extract_data() function
- v1.1.0: Facade pattern - StatusLine class orchestrates all components

### config_manager.py (Configuration Management) [v1.1.0]
Stateful configuration management with caching and validation.

**Classes:**
- `ConfigManager`: Manages configuration loading, validation, and persistence
  - `__init__(config_file: Path = None)`: Initialize with optional custom config file
  - `load(force_reload: bool = False) -> Dict[str, Any]`: Load config with caching
  - `save(config: Dict[str, Any]) -> None`: Validate and save config
  - `reload() -> Dict[str, Any]`: Force reload from file
  - `validate(config: Dict[str, Any]) -> Dict[str, Any]`: Validate configuration
  - `ensure_exists() -> None`: Create default config if missing

**Module-level Functions (backward compatibility):**
- `load_config()`: Uses default ConfigManager instance
- `save_config(config)`: Uses default ConfigManager instance
- `get_default_config()`: Returns default configuration
- `validate_config(config)`: Validates configuration
- `ensure_config_exists()`: Creates default config

**Type Hints:** Full type annotations

**Architecture:**
- v1.0.0-1.0.3: Module-level functions only
- v1.1.0: ConfigManager class with caching and multi-file support

### data_extractor.py (Data Extraction) [v1.1.0]
Extracts and transforms Claude Code JSON data into structured format.

**Classes:**
- `DataExtractor`: Organized extraction with specialized methods
  - `extract(json_data, config) -> Dict[str, Any]`: Main extraction orchestrator
  - `_extract_model(json_data)`: Extract model information
  - `_extract_version(json_data)`: Extract version string
  - `_extract_context(json_data)`: Extract context window and tokens
  - `_extract_workspace(json_data)`: Extract directory and git branch
  - `_extract_cost(json_data, accumulated_data)`: Extract cost, duration, rates
  - `_extract_output_style(json_data)`: Extract output style

**Module-level Functions (backward compatibility):**
- `extract_data(json_data, config)`: Uses default DataExtractor instance

**Type Hints:** Full type annotations with Dict[str, Any]

**Architecture:**
- v1.0.0-1.0.3: 73-line extract_data() function in statusline.py
- v1.1.0: DataExtractor class with focused methods (Single Responsibility)

### display_formatter.py (Output Formatting) [v1.0.4]
Formats statusline using StatusLineFormatter class and Field hierarchy.

**Classes:**
- `StatusLineFormatter`: Main formatter class
  - `__init__()`: Initialize with field registry
  - `get_field(field_name) -> Field`: Get field instance
  - `format(data, config, verbose=False) -> str`: Main formatting method
  - `format_compact(data, config) -> str`: Compact mode formatting
  - `format_verbose(data, config) -> str`: Verbose mode formatting

**Module-level Functions (backward compatibility):**
- `format_compact(data, config)`: Uses default formatter
- `format_verbose(data, config)`: Uses default formatter
- `format_statusline(data, config, verbose)`: Uses default formatter
- Legacy helpers: `format_progress_bar`, `format_field`, `format_duration`

**Type Hints:** Full type annotations

**Architecture:**
- v1.0.0-1.0.1: Procedural with duplication
- v1.0.2: Eliminated duplication, added line grouping
- v1.0.3: OOP refactoring with Field classes
- v1.0.4: StatusLineFormatter class with field registry

### git_utils.py (Git Integration)
Fast git branch detection with graceful fallback and GitHub PR status integration.

**Key Functions:**
- `get_git_branch(cwd: str) -> str`: Get current branch name
- `get_git_status(cwd: str) -> str`: Get git status indicators (clean/dirty, ahead/behind)
- `get_pr_status(cwd: str) -> str`: Get PR status with color-coded indicators (v1.2.3+)

**Performance:**
- Primary: Fast `.git/HEAD` file reading
- Fallback: Git command with 0.5s timeout
- PR status: GitHub CLI with 2.0s timeout for API calls

**Type Hints:** Full type annotations

**Uses:** constants/display.py for git settings

### colors.py (Color Management)
ANSI color codes and color application functions.

**Module Variables:**
- `COLORS: Dict[str, str]`: ANSI color code mapping
- `_color_override: Optional[bool]`: Module-level override

**Key Functions:**
- `colorize(text: str, color_name: str) -> str`: Apply color to text
- `is_color_enabled() -> bool`: Check color support (NO_COLOR aware)
- `reset() -> str`: Return ANSI reset code

**Type Hints:** Full type annotations

### constants/ (Constants Package) [v1.1.0]
Organized constants split into focused modules.

**Structure:**
- `constants/__init__.py`: Re-exports all for backward compatibility
- `constants/fields.py`: Field names, labels, icons, line assignments
- `constants/colors.py`: Color definitions and default mappings
- `constants/config.py`: Configuration keys and defaults
- `constants/display.py`: Display modes, icons, time formatting, git settings

**Benefits:**
- Better organization (247 lines → 4 focused modules)
- Logical grouping of related constants
- Easier to navigate and extend
- Full backward compatibility

**Architecture:**
- v1.0.0-1.0.2: Magic values scattered in code
- v1.0.3: Centralized constants.py (247 lines)
- v1.1.0: Organized into constants/ package with 4 modules

### fields.py (Field Class Hierarchy) [v1.0.3]
Object-oriented field formatting with Strategy pattern.

**Field Classes:**
- `Field` (ABC): Base class with abstract methods
- `SimpleField`: Direct value display (model, version, directory, git_branch)
- `ProgressField`: Percentage with optional progress bar (context_remaining)
- `MetricField`: Metrics with optional rates (tokens with tpm, cost with $/h)
- `DurationField`: Time formatting from milliseconds (duration)

**Key Functions:**
- `create_field_registry() -> Dict[str, Field]`: Creates field registry

**Type Hints:** Full type annotations with ABC

**Architecture:** Implements Strategy pattern for formatting logic

### models.py (Data Models) [v1.0.3]
Typed interfaces for data and configuration dictionaries.

**Classes:**
- `StatusLineData`: Typed wrapper for extracted data
  - Property methods for all fields
  - `get(key, default=None)`: Dictionary-style access
  - `to_dict()`: Convert to dictionary

- `Configuration`: Typed wrapper for configuration
  - Property methods with defaults
  - `is_field_visible(field)`: Check field visibility
  - `get_icon(key)`: Get icon with fallback
  - `get_color(key, default)`: Get color with fallback

**Type Hints:** Full type annotations

**Architecture:** Type-safe access layer over dictionaries

### exceptions.py (Custom Exceptions) [v1.0.4]
Hierarchical exception classes for better error handling.

**Exception Classes:**
- `StatusLineError`: Base exception for all statusline errors
- `ConfigurationError`: Invalid configuration issues
- `FieldNotFoundError`: Field not found in registry (stores field_name)
- `InvalidJSONError`: JSON parsing failures
- `ValidationError`: Data validation failures

**Type Hints:** Full type annotations

**Benefits:** Specific error handling and better debugging

### configure.py (Interactive Configuration)
Menu-driven configuration tool with field grouping by line assignment.

**Key Functions:**
- `main()`: Entry point
- `show_menu(config)`: Display main menu with field grouping by line
- `toggle_fields_menu(config)`: Toggle field visibility (grouped by Line 1/2/3)
- `customize_icons_menu(config)`: Customize icons
- `customize_colors_menu(config)`: Customize colors
- `reorder_fields_menu(config)`: Reorder fields
- `preview_statusline(config)`: Preview with mock data
- `_get_field_display_name(field_name)`: Get user-friendly display names (e.g., "Model ID")

## Installation Flow

```
./install.sh
    │
    ├─> Create ~/.claude-code-statusline/
    ├─> Copy src/* to installation directory (including constants/ package)
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

### Automated Testing (v1.0.4)
- **154 comprehensive tests** (143 unit + 11 integration)
- Test framework: pytest with pytest-cov
- Coverage: 75% overall (1345 statements, configure.py excluded as interactive CLI)
- Run with: `python3 -m pytest tests/`

**Test Coverage by Module:**
- `test_colors.py`: 10 tests, 100% coverage
- `test_git_utils.py`: 19 tests, 100% coverage
- `test_exceptions.py`: 10 tests, 100% coverage
- `test_models.py`: 54 tests, 100% coverage
- `test_system_utils.py`: 54 tests, 99% coverage
- `test_display_formatter.py`: 25 tests, 97% coverage
- `test_config_manager.py`: 20 tests, 94% coverage
- `test_statusline.py`: 38 tests, 90% coverage
- `test_integration.py`: 2 integration tests
  - Full statusline output verification
  - End-to-end workflow testing
  - Installation helper testing

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
- **Dependencies**: Python stdlib only (zero runtime dependencies)
- **Git Detection**: Fast file read with command fallback

## Extension Points (v1.1.0)

The OOP architecture makes extension straightforward:

1. **New fields**:
   - Add field constants to `constants/fields.py`
   - Add extraction logic to `DataExtractor` class in `data_extractor.py`
   - Create Field instance in `fields.py` registry

2. **Custom field types**:
   - Subclass `Field` in `fields.py` with custom formatting logic

3. **New configuration options**:
   - Add defaults to appropriate `constants/` module
   - Add validation to `ConfigManager.validate()` method

4. **Programmatic use**:
   - Import and use `StatusLine` facade class directly
   - No need to invoke CLI or use stdin/stdout

5. **Custom configuration sources**:
   - Create ConfigManager with custom file path
   - Inject custom ConfigManager into StatusLine

See `EXTENDING.md` for detailed guides and examples.

## Architecture Evolution

### v1.0.0-1.0.2: Procedural
- Module-level functions
- Code duplication
- Magic values in code

### v1.0.3: OOP Refactoring
- Field class hierarchy
- Centralized constants.py
- Data model classes

### v1.0.4: Exception Handling & Testing
- Custom exception hierarchy
- StatusLineFormatter class
- Logging infrastructure
- 232 tests, 75% coverage

### v1.1.0: Facade Pattern
- ConfigManager class (stateful, with caching)
- DataExtractor class (organized extraction)
- StatusLine facade (clean API)
- Organized constants/ package
- Simplified main() (50 lines → 15 lines)

## Maintenance

- Keep documentation synchronized with code
- Test on Python 3.6, 3.7, 3.8+ versions
- Verify terminal compatibility (ANSI colors, NO_COLOR support)
- Update CHANGELOG.md for all releases
- Run full test suite before releases: `python3 -m pytest tests/ -v --cov=src`
