#!/bin/bash

set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "Installing Claude Code Statusline Tool..."
echo

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 6 ]); then
    echo -e "${RED}Error: Python 3.6 or higher is required${NC}"
    echo -e "${RED}Current version: Python $PYTHON_VERSION${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python $PYTHON_VERSION detected${NC}"
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
    echo -e "${GREEN}Created symlink: claude-statusline-config${NC}"
else
    echo -e "${RED}Note: Could not create symlink in $SYMLINK_DIR (requires sudo)${NC}"
    echo "You can manually create it with:"
    echo "  sudo ln -sf $INSTALL_DIR/configure.py $SYMLINK_DIR/claude-statusline-config"
fi

# Create default config
echo "Creating default configuration..."
python3 "$(dirname "${BASH_SOURCE[0]}")/install_helper.py" create-config "$INSTALL_DIR"

# Update Claude Code settings
echo
echo "Updating Claude Code settings..."

python3 "$(dirname "${BASH_SOURCE[0]}")/install_helper.py" update-settings "$CLAUDE_SETTINGS"

if [ $? -eq 0 ]; then
    echo
    echo -e "${GREEN}✓ Installation complete!${NC}"
    echo
    echo "Next steps:"
    echo "1. Run 'claude-statusline-config' to customize your statusline (or python3 $INSTALL_DIR/configure.py)"
    echo "2. Restart Claude Code to see your new statusline"
    echo
    echo "Installation directory: $INSTALL_DIR"
else
    echo
    echo -e "${RED}Error: Failed to update settings file${NC}"
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
