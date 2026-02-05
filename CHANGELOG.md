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
  - Model name display
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

## [Unreleased]

### Possible Future Enhancements
- Multiple configuration profiles
- Language/runtime version detection
- Custom field expressions/formulas
- Export/import configuration
- Shell completion for configure.py
- Powerline-style separators
- Theme presets
