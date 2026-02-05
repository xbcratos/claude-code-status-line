# Claude Code Statusline Tool

A highly customizable statusline tool for Claude Code that provides fine-grained control over what information is displayed and how it's formatted.

## Requirements

- **Python 3.6 or higher** (uses f-strings and modern stdlib features)
- Git (optional, for branch detection)
- Unix-like system (macOS, Linux, or Windows with WSL)

**Note:** This tool has **zero runtime dependencies** - it uses only Python's standard library. Test dependencies (pytest, pytest-cov) are listed in `requirements-test.txt` for developers.

## Features

- **Two Display Modes**: Compact (icons only) and verbose (labeled) formats to suit your preferences
- **Fine-grained Control**: Show/hide individual fields like model, version, context, tokens, cost, git branch, and more
- **Custom Colors**: Full ANSI color customization with light/bright variants for better visibility
- **Custom Icons**: Customize or remove icons for each field
- **Field Ordering**: Reorder fields in any sequence you prefer
- **Progress Bars**: Visual progress bars for context usage
- **Git Integration**: Automatic git branch detection
- **Interactive Configuration**: Easy-to-use CLI for customizing all settings
- **Persistent Config**: Settings are saved and persist across sessions

## Installation

1. Clone or download this repository
2. Run the installation script:

```bash
cd claude-code-status-line
chmod +x install.sh
./install.sh
```

3. The installer will:
   - Copy files to `~/.claude-code-statusline/`
   - Create a default configuration
   - Make scripts executable
   - Create a symlink for easy configuration access
   - Update (or prompt you to update) your Claude Code settings

4. If the installer couldn't automatically update your settings, manually add this to `~/.claude/settings.json`:

```json
{
  "statusLine": {
    "type": "command",
    "command": "~/.claude-code-statusline/statusline.py"
  }
}
```

5. Restart Claude Code

## Configuration

### Interactive Configuration Tool

Run the configuration tool to customize your statusline:

```bash
claude-statusline-config
```

Or directly:

```bash
python3 ~/.claude-code-statusline/configure.py
```

The configuration tool provides:
- Toggle display mode (compact/verbose)
- Show/hide individual fields
- Customize icons
- Customize colors
- Reorder fields
- Configure progress bar settings
- Preview your changes
- Reset to defaults

### Display Modes

**Compact Mode** (default) - Icons and values only:
```
📁 my-project  🤖 claude-sonnet-4-5-20250929  📟 v1.0.85
🧠 Context Remaining: 85% [========--]
📊 75000 tok (2500 tpm)  💰 $12.50 ($25.00/h)
```

**Verbose Mode** - Labeled fields for clarity:
```
📁 Directory: my-project  🤖 Model: claude-sonnet-4-5-20250929  📟 Version: v1.0.85
🧠 Context remaining: 85% [========--]  ⌛ Duration: 30m
📊 Tokens: 75000 tok (2500 tpm)  💰 Cost: $12.50 ($25.00/h)
```

### Available Fields

- **Model**: Claude model ID (e.g., "claude-sonnet-4-5-20250929")
- **Version**: Claude Code version
- **Context Remaining**: Percentage of context window remaining (with progress bar)
- **Tokens**: Total input + output tokens (with tokens per minute)
- **Current Directory**: Current working directory name
- **Git Branch**: Current git branch
- **Cost**: Total cost in USD (with cost per hour)
- **Duration**: Session duration
- **Lines Changed**: Total lines added + removed
- **Output Style**: Output style name

### Color Customization

The tool uses ANSI color codes with light/bright variants for better terminal visibility:

Available colors:
- **Cyan** (light): Default for directory, tokens
- **Green** (light): Default for git branch, progress bar filled
- **Blue** (light): Default for model, output style
- **Magenta** (light): Default for version, duration
- **Yellow** (light): Default for context warnings
- **Red** (light): Default for cost
- **White** (bright): Default for separators, progress bar empty

Colors can be disabled:
- Via configuration tool: Option 7 (Toggle Colors On/Off)
- Via config file: Set `"enable_colors": false`
- Via environment variable: Set `NO_COLOR=1`

### Manual Configuration

Configuration is stored in `~/.claude-code-statusline/config.json`. You can edit it manually if preferred.

Example configuration:

```json
{
  "display_mode": "compact",
  "visible_fields": {
    "model": true,
    "version": true,
    "context_remaining": true,
    "tokens": true,
    "current_dir": true,
    "git_branch": true,
    "cost": true,
    "duration": false,
    "lines_changed": false,
    "output_style": false
  },
  "field_order": [
    "current_dir",
    "git_branch",
    "model",
    "version",
    "context_remaining",
    "tokens",
    "cost"
  ],
  "icons": {
    "directory": "📁",
    "git_branch": "🌿",
    "model": "🤖",
    "version": "📟",
    "context": "🧠",
    "cost": "💰",
    "tokens": "📊"
  },
  "colors": {
    "directory": "cyan",
    "git_branch": "green",
    "model": "blue",
    "version": "magenta",
    "context": "yellow",
    "cost": "red"
  },
  "show_progress_bars": true,
  "progress_bar_width": 10,
  "enable_colors": true
}
```

## Testing

### Manual Testing

Test the statusline with mock data:

```bash
echo '{"model":{"display_name":"Sonnet 4"},"version":"v1.0.85","context_window":{"remaining_percentage":95,"total_input_tokens":1000,"total_output_tokens":500},"workspace":{"current_dir":"'$(pwd)'"},"cost":{"total_cost_usd":2.48,"total_duration_ms":720000}}' | python3 ~/.claude-code-statusline/statusline.py
```

### Automated Testing

The project includes a comprehensive test suite with 90 tests (79 unit tests + 11 integration tests) covering all core functionality.

**Run tests:**
```bash
# Install test dependencies
pip install -r requirements-test.txt

# Run all tests
python3 -m pytest tests/

# Run with coverage
python3 -m pytest tests/ --cov=src --cov-report=term-missing
```

**Test coverage:**
- colors.py: 100%
- git_utils.py: 100%
- display_formatter.py: 92%
- statusline.py: 92%
- config_manager.py: 74%

## Troubleshooting

### Statusline not appearing
- Check that Claude Code settings.json has the correct path
- Verify statusline.py is executable: `chmod +x ~/.claude-code-statusline/statusline.py`
- Test the script manually with the command above

### Colors not showing
- Check if `NO_COLOR` environment variable is set: `echo $NO_COLOR`
- Verify `enable_colors` is true in `~/.claude-code-statusline/config.json`
- Try toggling colors in config tool: `claude-statusline-config` → Option 7
- Some terminals may not support ANSI colors

### Git branch not showing
- Ensure you're in a git repository
- Verify git is installed: `git --version`
- Check that the git repository is properly initialized

## Uninstallation

To remove the statusline tool:

```bash
rm -rf ~/.claude-code-statusline
rm -f /usr/local/bin/claude-statusline-config
```

Then remove the `statusLine` section from `~/.claude/settings.json` and restart Claude Code.

## License

MIT License - feel free to modify and distribute as needed.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.
