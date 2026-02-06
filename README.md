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
- **System Monitoring** (v1.2.0+): Real-time CPU usage, memory usage, and battery level display
- **Python Environment Detection** (v1.2.0+): Display Python version and active virtual environment
- **Enhanced Git Status** (v1.2.0+): Shows clean/dirty state, commits ahead/behind remote, and PR status with color-coded indicators
- **Date/Time Display** (v1.2.0+): Current timestamp with seconds precision
- **Custom Colors**: Full ANSI color customization with light/bright variants for better visibility
- **Custom Icons**: Customize or remove icons for each field
- **Field Ordering**: Reorder fields in any sequence you prefer
- **Progress Bars**: Visual progress bars for context usage
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
📁 my-project  🌿 main ✓  🤖 claude-sonnet-4-5-20250929  📟 v1.0.85  🐍 3.11.5  🕐 2026-02-05 15:30:42
🧠 Context Remaining: 85% [========--]
📊 75000 tok (2500 tpm)  💰 $12.50 ($25.00/h)  💻 25%  🧮 8.5GB  🔋 85%
```

**Verbose Mode** - Labeled fields for clarity:
```
📁 Directory: my-project  🌿 Git branch: main ✓  🤖 Model: claude-sonnet-4-5-20250929  📟 Version: v1.0.85  🐍 Python: 3.11.5  🕐 Time: 2026-02-05 15:30:42
🧠 Context remaining: 85% [========--]  ⌛ Duration: 30m
📊 Tokens: 75000 tok (2500 tpm)  💰 Cost: $12.50 ($25.00/h)  💻 CPU: 25%  🧮 Memory: 8.5GB  🔋 Battery: 85%
```

### Available Fields

**Session Information:**
- **Model**: Claude model ID (e.g., "claude-sonnet-4-5-20250929")
- **Version**: Claude Code version
- **Context Remaining**: Percentage of context window remaining (with progress bar)
- **Tokens**: Total input + output tokens (with tokens per minute)
- **Current Directory**: Current working directory name
- **Git Branch**: Current git branch with color-coded status indicators:
  - ✓ clean (green), ★ dirty (yellow)
  - ↑N ahead (cyan), ↓N behind (purple)
  - PR status: approved/passing (green), draft/pending (yellow), failing/changes requested (red)
- **Cost**: Total cost in USD (with cost per hour)
- **Duration**: Session duration
- **Lines Changed**: Total lines added + removed
- **Output Style**: Output style name

**System Monitoring (v1.2.0+):**
- **CPU Usage**: Current CPU usage percentage
- **Memory Usage**: Current memory usage (GB or percentage)
- **Battery**: Battery level percentage (laptops only)

**Python Environment (v1.2.0+):**
- **Python Version**: Current Python interpreter version
- **Date/Time**: Current date and time with seconds precision

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
    "output_style": false,
    "cpu_usage": true,
    "memory_usage": true,
    "battery": true,
    "python_version": true,
    "datetime": true
  },
  "field_order": [
    "current_dir",
    "git_branch",
    "model",
    "version",
    "output_style",
    "python_version",
    "datetime",
    "context_remaining",
    "duration",
    "tokens",
    "cost",
    "lines_changed",
    "cpu_usage",
    "memory_usage",
    "battery"
  ],
  "icons": {
    "directory": "📁",
    "git_branch": "🌿",
    "model": "🤖",
    "version": "📟",
    "context": "🧠",
    "cost": "💰",
    "tokens": "📊",
    "duration": "⌛",
    "cpu": "💻",
    "memory": "🧮",
    "battery": "🔋",
    "python": "🐍",
    "datetime": "🕐"
  },
  "colors": {
    "directory": "cyan",
    "git_branch": "green",
    "model": "blue",
    "version": "magenta",
    "context": "yellow",
    "cost": "red",
    "tokens": "cyan",
    "cpu": "green",
    "memory": "cyan",
    "battery": "yellow",
    "python": "blue",
    "datetime": "white"
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

The project includes a comprehensive test suite with **216 tests** covering all core functionality.

**Run tests:**
```bash
# Install test dependencies
pip install -r requirements-test.txt

# Run all tests
python3 -m pytest tests/

# Run with coverage
python3 -m pytest tests/ --cov=src --cov-report=term-missing
```

**Test coverage (v1.2.6):**
- Overall: 75% coverage (1331 statements)
- colors.py: 100%
- git_utils.py: 100%
- exceptions.py: 100%
- models.py: 100%
- constants: 100%
- system_utils.py: 99%
- data_extractor.py: 98%
- display_formatter.py: 97%
- config_manager.py: 94%
- fields.py: 93%
- statusline.py: 90%
- python_utils.py: 71%
- configure.py: 0% (interactive CLI, not unit-tested)

Test breakdown: 232 tests (221 unit tests + 11 integration tests)

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

### PR status not showing
- Ensure GitHub CLI (gh) is installed: `gh --version`
- Authenticate with GitHub: `gh auth login`
- Ensure you're on a branch with an associated pull request
- PR status will appear as "PR#123" in green (approved/passing), yellow (draft/pending), or red (failing/changes requested)

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

<div align="center">

## 🌟 Show Your Support

Give a ⭐ if this project helped you!

[![GitHub stars](https://img.shields.io/github/stars/xbcratos/claude-code-status-line?style=social)](https://github.com/xbcratos/claude-code-status-line/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/xbcratos/claude-code-status-line?style=social)](https://github.com/xbcratos/claude-code-status-line/network/members)
[![GitHub watchers](https://img.shields.io/github/watchers/xbcratos/claude-code-status-line?style=social)](https://github.com/xbcratos/claude-code-status-line/watchers)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/xbcratos/claude-code-status-line/blob/main/LICENSE)
[![Python 3.6+](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/downloads/)

[![Issues](https://img.shields.io/github/issues/xbcratos/claude-code-status-line)](https://github.com/xbcratos/claude-code-status-line/issues)
[![Pull Requests](https://img.shields.io/github/issues-pr/xbcratos/claude-code-status-line)](https://github.com/xbcratos/claude-code-status-line/pulls)
[![Contributors](https://img.shields.io/github/contributors/xbcratos/claude-code-status-line)](https://github.com/xbcratos/claude-code-status-line/graphs/contributors)

### 💬 Connect

[Report Bug](https://github.com/xbcratos/claude-code-status-line/issues) · [Request Feature](https://github.com/xbcratos/claude-code-status-line/issues) · [Discussions](https://github.com/xbcratos/claude-code-status-line/discussions)

</div>
