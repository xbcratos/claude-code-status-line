# Changelog

All notable changes to the Claude Code Statusline Tool will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-04

### Added
- Initial release of Claude Code Statusline Tool
- Two display modes: compact and large
- Fine-grained field visibility control
- Custom color support with ANSI codes
- Custom icon configuration
- Interactive CLI configuration tool
- Automatic git branch detection
- Progress bar visualization for context usage
- NO_COLOR environment variable support
- Field reordering capability
- Persistent configuration storage
- Installation script with automatic setup
- Comprehensive documentation

### Features
- **Statusline Fields**:
  - Model ID display
  - Version information
  - Context window remaining percentage with progress bar
  - Total tokens with tokens per minute calculation
  - Current directory name
  - Git branch name
  - Total cost with cost per hour calculation
  - Session duration formatting
  - Lines changed count
  - Output style display

- **Customization Options**:
  - Toggle any field on/off
  - Reorder fields in any sequence
  - Customize icons for each field
  - Choose from 7 different colors per field
  - Adjust progress bar width (5-50 characters)
  - Toggle progress bars entirely
  - Switch between compact and large display modes
  - Enable/disable colors globally

- **Git Integration**:
  - Fast `.git/HEAD` file reading
  - Git command fallback for special cases
  - Git worktree support
  - Detached HEAD state detection (shows commit hash)
  - Graceful handling of non-git directories

- **Configuration Tool**:
  - Interactive menu system
  - Real-time preview with mock data
  - Save/discard changes
  - Reset to defaults option
  - No external dependencies (pure Python stdlib)

- **Color Support**:
  - Light/bright ANSI color variants for better visibility
  - Separate colors for progress bar filled/empty sections
  - Separator color customization
  - NO_COLOR standard compliance
  - Terminal compatibility detection

### Technical Details
- Python 3.6+ compatible
- Zero external dependencies
- Uses only Python standard library
- Cross-platform (macOS, Linux)
- Fast execution (< 100ms typical)
- JSON-based configuration
- Modular architecture

### Documentation
- Comprehensive README with installation and usage
- Quick start guide for new users
- Examples document with 8+ configuration scenarios
- Inline code documentation
- Installation script with helpful prompts
- Troubleshooting section

## [1.0.1] - 2026-02-04

### Fixed
- Changed statusLine configuration from `"type": "custom", "script"` to `"type": "command", "command"` to match Claude Code requirements
- Install script now automatically modifies existing `.claude/settings.json` instead of only creating new files
- Install script now properly creates default configuration using `config_manager.ensure_config_exists()`
- Updated all documentation (README.md, QUICKSTART.md) to reflect correct settings format

### Changed
- Default display mode is now "compact" (icons only) for better space efficiency
- Improved install script with better error handling and user feedback

## [1.0.2] - 2026-02-05

### Added
- **Comprehensive test suite** with 79+ unit tests covering all core functionality
- Type hints throughout the codebase for better IDE support and code clarity
- Input validation for configuration values (colors, progress bar width, field names, display modes)
- Better error logging with specific error messages instead of silent failures
- `IMPROVEMENTS.md` documenting all code quality improvements

### Fixed
- Removed duplicate `os` import in `statusline.py`
- Eliminated runtime environment variable modification (replaced with cleaner module-level override)
- Reduced git command timeout from 2s to 0.5s for faster statusline updates
- Fixed non-portable screen clearing in `configure.py` (now works on Windows and Unix)
- Fixed inconsistent color field naming for `lines_changed`
- Improved import order to follow PEP 8 conventions

### Changed
- **Major refactoring** of `display_formatter.py`:
  - Eliminated ~80% code duplication between `format_compact()` and `format_verbose()`
  - Introduced constants for line grouping (`LINE_IDENTITY`, `LINE_STATUS`, `LINE_METRICS`)
  - Created `FIELD_LINE_ASSIGNMENT` dictionary to replace magic numbers
  - Extracted common formatting logic into helper functions
  - Easier to maintain and extend
- Config validation now provides helpful warnings for invalid values
- Error messages are more descriptive and actionable

### Technical Improvements
- Added constants for validation: `VALID_COLORS`, `VALID_DISPLAY_MODES`, `VALID_FIELD_NAMES`
- Color override now uses module-level variable instead of environment modification
- Type hints added to all major functions using Python 3.6+ typing module
- Screen clearing now portable (supports both Windows and Unix systems)

### Testing
- Created `tests/` directory with comprehensive test coverage
- Added `requirements-test.txt` for test dependencies
- Added `pytest.ini` for test configuration
- All 79 tests passing with strong coverage metrics

## [1.0.3] - 2026-02-05

### Added
- **OOP Refactoring - Field Classes**: Introduced Field class hierarchy for better organization
  - Created base `Field` class with common formatting logic
  - Specialized subclasses: `SimpleField`, `ProgressBarField`, `MetricField`, `RateField`
  - Each field knows how to format itself (Strategy pattern)
  - Eliminated code duplication across formatting functions
- **Comprehensive Integration Tests**: 11 new integration tests covering end-to-end workflows
- Better code organization with clear separation of concerns

### Changed
- `display_formatter.py`: Refactored from procedural to OOP design
- Fields are now registered and formatted through a centralized registry
- Format functions simplified by delegating to Field classes

### Technical Improvements
- Applied Strategy and Factory patterns for field formatting
- Improved maintainability and extensibility
- Test coverage increased to 90 tests (62% coverage)

## [1.0.4] - 2026-02-05

### Added
- **StatusLineFormatter Class**: Converted module-level functions to proper OOP class
  - Encapsulated field registry as instance variable
  - Added methods: `get_field()`, `format()`, `format_compact()`, `format_verbose()`
  - Maintained backward compatibility with module-level convenience functions
- **Custom Exception Hierarchy**: Created specialized exceptions for better error handling
  - `StatusLineError`: Base exception for all statusline errors
  - `ConfigurationError`: Invalid configuration issues
  - `FieldNotFoundError`: Field not found in registry (stores field name)
  - `InvalidJSONError`: JSON parsing failures
  - `ValidationError`: Data validation failures
- **Logging Module**: Replaced print statements with proper logging
  - Configurable via `LOG_LEVEL` environment variable
  - Levels: DEBUG, INFO, WARNING (default), ERROR
  - Debug logging throughout workflow for troubleshooting
- **Test Coverage Improvements**: Increased from 90 to 154 tests (70% coverage)
  - Added 54 tests for StatusLineData and Configuration models
  - Added 7 validation tests for config_manager
  - Added 10 exception hierarchy tests
  - Coverage: 96.3% for testable code (excluding interactive CLI)

### Changed
- All error handling now uses custom exceptions
- Console output uses logging module (logs to stderr)
- config_manager warnings use logger instead of print

### Technical Improvements
- Better testability with OOP classes
- Proper error hierarchy for specific error handling
- Professional logging infrastructure

## [1.1.0] - 2026-02-05

### Added
- **ConfigManager Class**: Stateful configuration management
  - Caching support with `load(force_reload)` and `reload()` methods
  - Support for multiple config files via constructor parameter
  - Instance-based design for better testability
  - Maintained backward compatibility with module-level functions
- **DataExtractor Class**: Organized data extraction into focused methods
  - Extracted 73-line `extract_data()` function into specialized class
  - Methods: `_extract_model()`, `_extract_version()`, `_extract_context()`, `_extract_workspace()`, `_extract_cost()`, `_extract_output_style()`
  - Proper handling of cross-field dependencies (e.g., tokens_per_minute calculation)
  - Clean separation of concerns (Single Responsibility Principle)
- **StatusLine Facade Class**: Simplified API for statusline generation
  - Orchestrates ConfigManager, DataExtractor, and StatusLineFormatter
  - Provides clean `generate(json_input: str) -> str` API
  - Simplified `main()` from 50 lines to 15 lines
  - Easy to test without CLI dependencies
  - Better for programmatic use

### Changed
- **Constants Module Organization**: Split 247-line `constants.py` into focused modules
  - `constants/fields.py` (93 lines): Field names, labels, icons, line assignments
  - `constants/colors.py` (66 lines): Color definitions and default mappings
  - `constants/config.py` (74 lines): Configuration keys and defaults
  - `constants/display.py` (95 lines): Display modes, icons, time formatting, git settings
  - `constants/__init__.py` (174 lines): Re-exports all for backward compatibility
  - Better organization, easier to navigate and extend
- ConfigManager default parameter now evaluated at runtime (fixes test monkeypatching)

### Technical Improvements
- Consistent OOP design across all major modules
- Facade pattern for simplified high-level API
- Better dependency injection support
- Cleaner, more maintainable codebase
- All 154 tests passing

### Removed
- TypedDict implementation (initially added then reverted)
  - Removed due to Python version compatibility complexity
  - Simple `Dict[str, Any]` type hints are sufficient and clearer

## [1.1.1] - 2026-02-05

### Fixed
- **Documentation Updates** (no code changes)
- Updated README.md with correct test count (154 tests, was 90)
- Updated README.md with current coverage percentages for v1.1.0
- Fixed QUICKSTART.md reference from non-existent EXAMPLES.md to EXTENDING.md
- Restored CODE_REVIEW.md (accidentally deleted in previous commit)
- Updated CODE_REVIEW.md to reflect v1.1.0 completion status:
  - Marked TypedDict as implemented then reverted
  - Corrected "Split constants" completion (v1.1.0, not v2.0.0)
  - Marked plugin system and config migration as not implemented
- Updated EXTENDING.md for v1.1.0 architecture:
  - Changed references from constants.py to constants/ package
  - Updated data extraction examples to use DataExtractor class
  - Added Key Architectural Benefits section

### Notes
- This is a documentation-only release with no code changes
- All 154 tests continue to pass
- Codebase functionality identical to v1.1.0

## [1.1.2] - 2026-02-05

### Changed
- **configure.py Refactoring**: Replaced all hardcoded strings with constants
  - Field names now use `FIELD_*` constants (e.g., `FIELD_MODEL`, `FIELD_VERSION`)
  - Icon keys now use `ICON_KEY_*` constants (e.g., `ICON_KEY_DIRECTORY`, `ICON_KEY_GIT_BRANCH`)
  - Display modes now use `DISPLAY_MODE_COMPACT` and `DISPLAY_MODE_VERBOSE`
  - Config keys now use `CONFIG_KEY_*` constants (e.g., `CONFIG_KEY_DISPLAY_MODE`, `CONFIG_KEY_VISIBLE_FIELDS`)
  - Color validation now uses `VALID_COLORS` constant list
  - Progress bar width limits now use `MIN_PROGRESS_BAR_WIDTH` and `MAX_PROGRESS_BAR_WIDTH`
  - Default values now use constants (e.g., `DEFAULT_ENABLE_COLORS`)

### Technical Improvements
- Improved maintainability by eliminating magic strings throughout configure.py
- Better consistency with the rest of the codebase
- Easier to refactor field names or config keys in the future (single source of truth)
- Reduced risk of typos in field/config key names

### Notes
- No functional changes, only code quality improvements
- All 154 tests continue to pass
- Configuration file format remains unchanged

## [1.2.0] - 2026-02-05

### Added
- **System Monitoring Fields**: Real-time system resource monitoring
  - `cpu_usage`: Current CPU usage percentage (cross-platform: Linux, macOS, Windows)
  - `memory_usage`: Memory usage display (shows used memory in GB or as percentage)
  - `battery`: Battery level percentage (laptops only, gracefully omitted on desktops)
  - All system fields use platform-specific APIs with graceful degradation
  - Zero external dependencies (uses only Python stdlib)

- **Python Environment Detection**:
  - `python_version`: Current Python version (e.g., "3.11.5")
  - Positioned on LINE_IDENTITY

- **Date and Time Display**:
  - `datetime`: Current date and time with seconds precision
  - Format: "YYYY-MM-DD HH:MM:SS"
  - Positioned on LINE_IDENTITY for quick reference

- **Enhanced Git Status Integration**:
  - Git dirty/clean indicator: "✓" for clean, "★" for uncommitted changes
  - Ahead/behind tracking: "↑N" for commits ahead, "↓N" for commits behind
  - Combined with existing git_branch field (e.g., "main ★ ↑2")
  - Uses `git status --porcelain` and `git rev-list` commands
  - Graceful handling when no upstream branch is configured

- **New Utility Modules**:
  - `system_utils.py`: Cross-platform system monitoring functions
  - `python_utils.py`: Python environment detection utilities
  - Enhanced `git_utils.py` with status functions

### Changed
- **Field Positioning**: Reorganized LINE_IDENTITY (line 1) to include:
  - Current directory, git branch (with status), model, version, output style, python version, datetime
  - System monitoring fields (CPU, memory, battery) remain on LINE_METRICS (line 3)

- **Default Configuration**: All new fields enabled by default
  - Users can disable unwanted fields via configure.py or config.json
  - New fields automatically added to existing configurations on first run

- **Config Manager Enhancement**: Improved field merging logic
  - Now always adds missing valid fields to existing configurations
  - Ensures new fields appear in statusline even with older config files

### Fixed
- **Config Validation Bug**: Fixed issue where new fields weren't added to field_order unless config had invalid fields
  - Moved field addition logic outside conditional block
  - Ensures backward compatibility with existing configurations

### Testing
- **Comprehensive Test Coverage for Git Status**:
  - Added 22 new tests covering `_is_git_dirty()`, `_get_ahead_behind()`, and `get_git_status()`
  - Tests cover success cases, edge cases, and error handling
  - Mock-based testing for platform-independent validation
  - **git_utils.py coverage: 55% → 100%**
  - **Overall test coverage: 65% → 67%**
  - **Total tests: 154 → 176 tests**
  - All tests passing

### Technical Details
- Cross-platform system monitoring:
  - **Linux**: Reads `/proc/stat` for CPU, `/proc/meminfo` for memory
  - **macOS**: Uses `top` command for CPU, `vm_stat` for memory, `pmset` for battery
  - **Windows**: Uses `wmic` commands for system metrics
- Git status uses fast subprocess calls with 0.5s timeout
- All new functionality uses only Python standard library
- Maintains zero external dependencies

### Documentation
- Updated field constants in `constants/fields.py`
- Added field labels for verbose mode display
- Updated default field order and visibility settings
- Enhanced `EXTENDING.md` with external data sources example (git branch)

## [1.2.1] - 2026-02-05

### Fixed
- **Documentation**: Updated README.md example configuration to accurately reflect default settings
  - **Confirmed memory_usage is enabled by default** (was enabled in v1.2.0, documentation was outdated)
  - Added missing system monitoring fields to examples: `cpu_usage`, `memory_usage`, `battery`
  - Added missing Python environment field: `python_version`
  - Added missing `datetime` field
  - Fixed memory icon in examples (🧮 abacus instead of 🧠 brain)
  - Fixed CPU icon in examples (💻 computer instead of 🖥️ desktop)
  - Updated field order to match default configuration
  - Added missing icons and colors for new fields

### Testing
- **Added comprehensive test suite for system_utils.py**:
  - Created 40 new tests covering all system monitoring functions
  - Tests for Linux, macOS, and Windows implementations
  - Coverage for CPU, memory, and battery monitoring
  - Error handling and edge case validation
  - **system_utils.py coverage: 34% → 94%**
  - **Overall test coverage: 67% → 77%**
  - **Total tests: 176 → 216 tests**
  - All tests passing

### Notes
- This is a documentation and testing-only release with no functional changes
- **Memory usage display has been enabled by default since v1.2.0**
- All v1.2.0 features (system monitoring, Python environment, datetime) are enabled by default
- Users can disable any field via the configuration tool: `claude-statusline-config`

## [1.2.3] - 2026-02-05

### Added
- **Pull Request Status Display**: GitHub PR status now appears in git_branch field
  - Automatically detects PR for current branch using GitHub CLI (`gh`)
  - Color-coded status indicators:
    - **Green**: PR is approved or all checks passing
    - **Yellow**: PR is in draft state or checks pending
    - **Red**: PR has failing checks or changes requested
  - Shows as "PR#123" after git status indicators
  - Gracefully handles missing `gh` CLI or branches without PRs
  - Fast execution with 0.5s timeout
  - Zero impact if gh is not installed

### Testing
- **Added comprehensive test suite for PR status**:
  - Created 16 new tests covering `get_pr_status()` function
  - Tests for all PR states: approved, draft, changes requested, passing/failing/pending checks
  - Error handling for missing gh CLI, invalid JSON, timeouts
  - Coverage for both 'status' and 'conclusion' fields in statusCheckRollup
  - **Total tests: 216 → 232 tests**
  - All tests passing

### Technical Details
- Uses `gh pr view --json number,isDraft,reviewDecision,statusCheckRollup`
- JSON parsing with proper error handling
- Color codes applied using existing `colorize()` function
- Integrates seamlessly into existing git_branch field architecture
- Maintains zero external dependencies (gh CLI is optional)

### Documentation
- Updated README.md with PR status feature description
- Added troubleshooting section for PR status
- Updated feature list to highlight color-coded PR indicators

## [1.2.2] - 2026-02-05

### Fixed
- **Memory usage display**: Fixed macOS memory parsing bugs that caused memory field to not display
  - Fixed page size extraction from vm_stat output (was reading wrong array index)
  - Fixed wired pages detection (changed from "Pages wired" to "Pages wired down")
- **Configure tool**: Added missing system monitoring fields (cpu_usage, memory_usage, battery, python_version, datetime) to all configuration menus

### Changed
- **Memory format**: Memory usage now displays as percentage (e.g., "40%") instead of absolute values (e.g., "18.5GB") for consistency with CPU and battery displays
- **Configure tool refactoring**: Eliminated hardcoded field lists in configure.py by dynamically generating menus from existing constants (VALID_FIELD_NAMES, DEFAULT_ICONS, DEFAULT_COLORS)
  - Reduced maintenance overhead - new fields automatically appear in all menus
  - Single source of truth for field definitions
  - Added helper functions `_get_field_display_name()` and `_get_icon_display_name()`

### Technical Improvements
- Updated all platform-specific memory functions (_get_memory_linux, _get_memory_macos, _get_memory_windows) to calculate and return percentages
- Updated test suite to reflect percentage format for memory usage
- All 216 tests passing

## [1.2.4] - 2026-02-05

### Fixed
- **PR status display**: Fixed timeout issue preventing PR information from displaying
  - Increased gh command timeout from 0.5s to 2.0s to accommodate GitHub API calls
  - Added new `GH_COMMAND_TIMEOUT_SECONDS` constant for better configurability
  - PR status now reliably displays for branches with associated pull requests

### Changed
- **Install script**: Added colored output for better readability
  - Success messages now display in green
  - Error messages now display in red
  - Makes installation progress easier to follow

### Technical Improvements
- Separated git command timeout (0.5s for local operations) from gh command timeout (2.0s for API calls)
- All 232 tests passing

## [1.2.5] - 2026-02-06

### Changed
- **Configure Tool Improvements**:
  - Changed "Model Name" to "Model ID" in field display names for clarity
  - Grouped fields by line assignment in toggle fields menu:
    - Line 1 (Identity): Fields showing who you are and what you're working on
    - Line 2 (Status): Fields showing current session state
    - Line 3 (Metrics): Fields showing usage and system stats
  - Improved main menu to show field grouping by line
  - Added descriptive line headers to make field organization clearer

### Removed
- **python_venv field**: Removed virtual environment name field as it was redundant
  - python_version field already provides Python environment information
  - Reduces clutter in the status line for users not working in virtual environments
  - Removed from all code, tests, and documentation

### Documentation
- Updated CHANGELOG.md: Changed "Model name display" to "Model ID display" for consistency
- Updated test coverage documentation (v1.2.5): 75% coverage (1345 statements)

## [Unreleased]

### Possible Future Enhancements
- Multiple configuration profiles
- Custom field expressions/formulas
- Export/import configuration
- Shell completion for configure.py
- Powerline-style separators
- Theme presets