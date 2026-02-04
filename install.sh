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

# Create default config if it doesn't exist
if [ ! -f "$INSTALL_DIR/config.json" ]; then
    echo "Creating default configuration..."
    python3 "$INSTALL_DIR/statusline.py" <<< '{}' > /dev/null 2>&1 || true
fi

# Update Claude Code settings
echo
echo "Updating Claude Code settings..."

if [ ! -f "$CLAUDE_SETTINGS" ]; then
    echo "Creating new settings file..."
    mkdir -p "$(dirname "$CLAUDE_SETTINGS")"
    cat > "$CLAUDE_SETTINGS" << 'EOF'
{
  "statusLine": {
    "type": "custom",
    "script": "~/.claude-code-statusline/statusline.py"
  }
}
EOF
else
    echo "Settings file exists. Please manually add the following to $CLAUDE_SETTINGS:"
    echo
    cat << 'EOF'
{
  "statusLine": {
    "type": "custom",
    "script": "~/.claude-code-statusline/statusline.py"
  }
}
EOF
    echo
fi

echo
echo "Installation complete!"
echo
echo "Next steps:"
echo "1. If you haven't already, add the statusLine configuration to $CLAUDE_SETTINGS"
echo "2. Run 'claude-statusline-config' to customize your statusline (or python3 $INSTALL_DIR/configure.py)"
echo "3. Restart Claude Code to see your new statusline"
echo
echo "Installation directory: $INSTALL_DIR"
