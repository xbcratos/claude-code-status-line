# Quick Start Guide

Get up and running with Claude Code Statusline in 5 minutes.

## Requirements

- **Python 3.6 or higher** - Check with: `python3 --version`
- macOS or Linux

## Installation

```bash
cd claude-code-status-line
./install.sh
```

## Configure Claude Code

If the installer didn't automatically update your settings, add this to `~/.claude/settings.json`:

```json
{
  "statusLine": {
    "type": "command",
    "command": "~/.claude-code-statusline/statusline.py"
  }
}
```

## Restart Claude Code

Restart Claude Code to see your new statusline.

## Customize (Optional)

Run the interactive configuration tool:

```bash
claude-statusline-config
```

Or:

```bash
python3 ~/.claude-code-statusline/configure.py
```

## What You'll See

By default, you'll see:

```
📁 my-project  🌿 main  🤖 Sonnet 4  📟 v1.0.85
🧠 Context Remaining: 95% [=========-]
💰 $2.48 ($12.40/h)  📊 15000 tok (1250 tpm)
```

## Quick Customization Tips

### Change Display Mode
In the config tool: Option 1 → Choose "verbose" for labeled fields

### Hide Fields You Don't Need
In the config tool: Option 2 → Toggle off unwanted fields

### Disable Colors
```bash
export NO_COLOR=1
```

Or in the config tool: Option 7

### Change Icons
In the config tool: Option 3 → Select field and enter new emoji

### Preview Changes
In the config tool: Option 9 → See your changes before saving

## Common Configurations

### Minimal
Show only model and context:
- Toggle Fields → Disable everything except model, version, context_remaining

### Developer Focus
Show directory, git branch, and code stats:
- Toggle Fields → Enable current_dir, git_branch, context_remaining, lines_changed

### Cost Tracker
Show usage and costs:
- Toggle Fields → Enable model, tokens, cost, duration

## Troubleshooting

### Statusline not showing?
1. Check settings.json has correct path
2. Verify script is executable: `chmod +x ~/.claude-code-statusline/statusline.py`
3. Test manually: `echo '{"model":{"display_name":"Test"}}' | python3 ~/.claude-code-statusline/statusline.py`

### No colors?
1. Check if NO_COLOR is set: `echo $NO_COLOR`
2. Verify terminal supports ANSI colors
3. Try toggling colors in config tool

### Git branch not showing?
1. Make sure you're in a git repository
2. Verify git is installed: `git --version`

## Next Steps

- Read [README.md](README.md) for full documentation
- Check [EXAMPLES.md](EXAMPLES.md) for configuration examples
- Customize your statusline with the config tool

## Support

Issues? Questions? Visit: https://github.com/anthropics/claude-code/issues
