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

## [Unreleased]

### Possible Future Enhancements
- Multiple configuration profiles
- Language/runtime version detection
- Custom field expressions/formulas
- Export/import configuration
- Shell completion for configure.py
- Powerline-style separators
- Theme presets
