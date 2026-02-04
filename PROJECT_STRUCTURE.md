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
├── install.sh                    # Installation script
├── test_statusline.sh            # Test suite
├── README.md                     # Main documentation
├── QUICKSTART.md                 # Quick start guide
├── EXAMPLES.md                   # Configuration examples
├── CHANGELOG.md                  # Version history
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
- `main()`: Entry point
- `extract_data(json_data, config)`: Parse Claude Code JSON

### config_manager.py (Configuration Management)
- Manages configuration file I/O
- Provides defaults
- Validates configuration

**Key Functions:**
- `load_config()`: Load user config
- `save_config(config)`: Save config to file
- `get_default_config()`: Return default configuration
- `ensure_config_exists()`: Create config if missing

### display_formatter.py (Output Formatting)
- Renders statusline in compact/large modes
- Formats progress bars
- Applies colors to fields

**Key Functions:**
- `format_compact(data, config)`: Generate compact output
- `format_large(data, config)`: Generate large output
- `format_progress_bar(percentage, width, config)`: Create progress bar
- `format_field(field_name, value, config)`: Format individual field
- `format_duration(duration_ms)`: Convert duration to readable format

### git_utils.py (Git Integration)
- Detects git branch
- Handles worktrees
- Graceful fallback

**Key Functions:**
- `get_git_branch(cwd)`: Get current branch name

### colors.py (Color Management)
- ANSI color code definitions
- Color application functions
- NO_COLOR support

**Key Functions:**
- `colorize(text, color_name)`: Apply color to text
- `is_color_enabled()`: Check color support
- `reset()`: Return reset code

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

### Manual Testing
- Tests compact/large modes
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
