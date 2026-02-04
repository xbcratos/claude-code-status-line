#!/bin/bash

set -e

echo "Installing Claude Code Statusline Tool..."
echo

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 6 ]); then
    echo "Error: Python 3.6 or higher is required"
    echo "Current version: Python $PYTHON_VERSION"
    exit 1
fi

echo "✓ Python $PYTHON_VERSION detected"
echo

# Define paths
INSTALL_DIR="$HOME/.claude-code-statusline"
SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/src"
CLAUDE_SETTINGS="$HOME/.claude/settings.json"

# Create installation directory
mkdir -p "$INSTALL_DIR"

# Copy source files
echo "Copying source files..."
cp -r "$SRC_DIR"/* "$INSTALL_DIR/"

# Make scripts executable
chmod +x "$INSTALL_DIR/statusline.py"
chmod +x "$INSTALL_DIR/configure.py"

# Create symlink for easy access to configure script
SYMLINK_DIR="/usr/local/bin"
if [ -w "$SYMLINK_DIR" ]; then
    ln -sf "$INSTALL_DIR/configure.py" "$SYMLINK_DIR/claude-statusline-config"
    echo "Created symlink: claude-statusline-config"
else
    echo "Note: Could not create symlink in $SYMLINK_DIR (requires sudo)"
    echo "You can manually create it with:"
    echo "  sudo ln -sf $INSTALL_DIR/configure.py $SYMLINK_DIR/claude-statusline-config"
fi

# Create default config
echo "Creating default configuration..."
python3 -c "
import sys
sys.path.insert(0, '$INSTALL_DIR')
from config_manager import ensure_config_exists
ensure_config_exists()
" 2>/dev/null || {
    echo "Warning: Could not create default config automatically"
    echo "It will be created on first run"
}

# Update Claude Code settings
echo
echo "Updating Claude Code settings..."

python3 << 'PYTHON_SCRIPT'
import json
import os
from pathlib import Path

settings_file = Path.home() / ".claude" / "settings.json"
settings_dir = settings_file.parent

# Create .claude directory if it doesn't exist
settings_dir.mkdir(parents=True, exist_ok=True)

# Load existing settings or create new ones
if settings_file.exists():
    try:
        with open(settings_file, 'r') as f:
            settings = json.load(f)
        print(f"✓ Loaded existing settings from {settings_file}")
    except json.JSONDecodeError:
        settings = {}
        print(f"Warning: Could not parse {settings_file}, creating new settings")
else:
    settings = {}
    print(f"✓ Creating new settings file at {settings_file}")

# Update statusLine configuration
settings["statusLine"] = {
    "type": "command",
    "command": "~/.claude-code-statusline/statusline.py"
}

# Save settings
with open(settings_file, 'w') as f:
    json.dump(settings, f, indent=2)

print(f"✓ Updated statusLine configuration in {settings_file}")
PYTHON_SCRIPT

if [ $? -eq 0 ]; then
    echo
    echo "Installation complete!"
    echo
    echo "Next steps:"
    echo "1. Run 'claude-statusline-config' to customize your statusline (or python3 $INSTALL_DIR/configure.py)"
    echo "2. Restart Claude Code to see your new statusline"
    echo
    echo "Installation directory: $INSTALL_DIR"
else
    echo
    echo "Error: Failed to update settings file"
    echo "Please manually add the following to $CLAUDE_SETTINGS:"
    echo
    cat << 'EOF'
{
  "statusLine": {
    "type": "command",
    "command": "~/.claude-code-statusline/statusline.py"
  }
}
EOF
    echo
fi
