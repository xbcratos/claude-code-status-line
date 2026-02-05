#!/usr/bin/env python3
import sys
from pathlib import Path

# Add src directory to path for imports (must be before other local imports)
sys.path.insert(0, str(Path(__file__).parent))

from config_manager import load_config, save_config, get_default_config
from display_formatter import format_compact, format_verbose
import colors
import constants

# Require Python 3.6+
if sys.version_info < (3, 6):
    print("Error: Python 3.6 or higher is required", file=sys.stderr)
    print(f"Current version: {sys.version}", file=sys.stderr)
    sys.exit(1)

def clear_screen():
    """Clear the terminal screen in a portable way."""
    import os
    # Use os.system to clear screen portably
    os.system('cls' if os.name == 'nt' else 'clear')

def show_menu(config):
    """Display main configuration menu."""
    clear_screen()
    print("Claude Code Statusline Configuration")
    print("=" * 50)
    print()

    print(f"1. Display Mode")
    print(f"   Current: {config[constants.CONFIG_KEY_DISPLAY_MODE]}")
    print(f"   Options: [{constants.DISPLAY_MODE_COMPACT}, {constants.DISPLAY_MODE_VERBOSE}]")
    print()

    print("2. Toggle Visible Fields")
    visible = config[constants.CONFIG_KEY_VISIBLE_FIELDS]
    field_names = {
        constants.FIELD_MODEL: "Model Name",
        constants.FIELD_VERSION: "Version",
        constants.FIELD_CONTEXT_REMAINING: "Context Remaining",
        constants.FIELD_TOKENS: "Tokens",
        constants.FIELD_CURRENT_DIR: "Current Directory",
        constants.FIELD_GIT_BRANCH: "Git Branch",
        constants.FIELD_COST: "Cost",
        constants.FIELD_DURATION: "Duration",
        constants.FIELD_LINES_CHANGED: "Lines Changed",
        constants.FIELD_OUTPUT_STYLE: "Output Style"
    }
    for field, label in field_names.items():
        status = "✓" if visible.get(field, False) else "✗"
        print(f"   {status} {label}")
    print()

    print("3. Customize Icons")
    print("4. Customize Colors")
    print("5. Reorder Fields")
    print(f"6. Progress Bar Settings (Currently: {'On' if config[constants.CONFIG_KEY_SHOW_PROGRESS_BARS] else 'Off'}, Width: {config[constants.CONFIG_KEY_PROGRESS_BAR_WIDTH]})")
    print(f"7. Toggle Colors On/Off (Currently: {'On' if config[constants.CONFIG_KEY_ENABLE_COLORS] else 'Off'})")
    print("8. Reset to Defaults")
    print("9. Preview Statusline")
    print("10. Save and Exit")
    print()
    print("0. Exit without saving")
    print()

def toggle_fields_menu(config):
    """Menu for toggling visible fields."""
    clear_screen()
    print("Toggle Visible Fields")
    print("=" * 50)
    print()

    visible = config[constants.CONFIG_KEY_VISIBLE_FIELDS]
    field_names = {
        "1": (constants.FIELD_MODEL, "Model Name"),
        "2": (constants.FIELD_VERSION, "Version"),
        "3": (constants.FIELD_CONTEXT_REMAINING, "Context Remaining"),
        "4": (constants.FIELD_TOKENS, "Tokens"),
        "5": (constants.FIELD_CURRENT_DIR, "Current Directory"),
        "6": (constants.FIELD_GIT_BRANCH, "Git Branch"),
        "7": (constants.FIELD_COST, "Cost"),
        "8": (constants.FIELD_DURATION, "Duration"),
        "9": (constants.FIELD_LINES_CHANGED, "Lines Changed"),
        "10": (constants.FIELD_OUTPUT_STYLE, "Output Style")
    }

    for num, (field, label) in field_names.items():
        status = "✓" if visible.get(field, False) else "✗"
        print(f"{num}. {status} {label}")

    print()
    print("0. Back to main menu")
    print()

    choice = input("Toggle field (enter number): ").strip()

    if choice in field_names:
        field, _ = field_names[choice]
        visible[field] = not visible.get(field, False)
        return True

    return choice != "0"

def customize_icons_menu(config):
    """Menu for customizing icons."""
    clear_screen()
    print("Customize Icons")
    print("=" * 50)
    print()

    icons = config[constants.CONFIG_KEY_ICONS]
    icon_names = {
        "1": (constants.ICON_KEY_DIRECTORY, "Directory"),
        "2": (constants.ICON_KEY_GIT_BRANCH, "Git Branch"),
        "3": (constants.ICON_KEY_MODEL, "Model"),
        "4": (constants.ICON_KEY_VERSION, "Version"),
        "5": (constants.ICON_KEY_CONTEXT, "Context"),
        "6": (constants.ICON_KEY_COST, "Cost"),
        "7": (constants.ICON_KEY_TOKENS, "Tokens"),
        "8": (constants.ICON_KEY_DURATION, "Duration"),
        "9": (constants.ICON_KEY_STYLE, "Style")
    }

    for num, (field, label) in icon_names.items():
        current = icons.get(field, "")
        print(f"{num}. {label}: {current}")

    print()
    print("0. Back to main menu")
    print()

    choice = input("Select field to change icon (enter number): ").strip()

    if choice in icon_names:
        field, label = icon_names[choice]
        new_icon = input(f"Enter new icon for {label} (or press Enter to remove): ").strip()
        icons[field] = new_icon
        return True

    return choice != "0"

def customize_colors_menu(config):
    """Menu for customizing colors."""
    clear_screen()
    print("Customize Colors")
    print("=" * 50)
    print()

    color_fields = {
        "1": (constants.ICON_KEY_DIRECTORY, "Directory"),
        "2": (constants.ICON_KEY_GIT_BRANCH, "Git Branch"),
        "3": (constants.ICON_KEY_MODEL, "Model"),
        "4": (constants.ICON_KEY_VERSION, "Version"),
        "5": (constants.ICON_KEY_CONTEXT, "Context"),
        "6": (constants.ICON_KEY_COST, "Cost"),
        "7": (constants.ICON_KEY_TOKENS, "Tokens"),
        "8": (constants.ICON_KEY_DURATION, "Duration"),
        "9": (constants.ICON_KEY_STYLE, "Style"),
        "10": ("progress_bar_filled", "Progress Bar (Filled)"),
        "11": ("progress_bar_empty", "Progress Bar (Empty)"),
        "12": ("separator", "Separator")
    }

    color_config = config[constants.CONFIG_KEY_COLORS]

    for num, (field, label) in color_fields.items():
        current = color_config.get(field, constants.COLOR_WHITE)
        print(f"{num}. {label}: {current}")

    print()
    colors_list = ", ".join(constants.VALID_COLORS)
    print(f"Available colors: {colors_list}")
    print()
    print("0. Back to main menu")
    print()

    choice = input("Select field to change color (enter number): ").strip()

    if choice in color_fields:
        field, label = color_fields[choice]
        print(f"\nAvailable colors: {colors_list}")
        new_color = input(f"Enter new color for {label}: ").strip().lower()

        if new_color in constants.VALID_COLORS:
            color_config[field] = new_color
        else:
            print(f"Invalid color. Keeping current color: {color_config[field]}")
            input("Press Enter to continue...")
        return True

    return choice != "0"

def reorder_fields_menu(config):
    """Menu for reordering fields."""
    clear_screen()
    print("Reorder Fields")
    print("=" * 50)
    print()
    print("Current order:")

    field_names = {
        constants.FIELD_CURRENT_DIR: "Current Directory",
        constants.FIELD_GIT_BRANCH: "Git Branch",
        constants.FIELD_MODEL: "Model",
        constants.FIELD_VERSION: "Version",
        constants.FIELD_CONTEXT_REMAINING: "Context Remaining",
        constants.FIELD_TOKENS: "Tokens",
        constants.FIELD_COST: "Cost",
        constants.FIELD_DURATION: "Duration",
        constants.FIELD_LINES_CHANGED: "Lines Changed",
        constants.FIELD_OUTPUT_STYLE: "Output Style"
    }

    for i, field in enumerate(config[constants.CONFIG_KEY_FIELD_ORDER], 1):
        label = field_names.get(field, field)
        print(f"{i}. {label}")

    print()
    print("Enter two numbers to swap their positions (e.g., '1 3')")
    print("Or press Enter to go back")
    print()

    choice = input("Swap: ").strip()

    if choice:
        try:
            parts = choice.split()
            if len(parts) == 2:
                idx1 = int(parts[0]) - 1
                idx2 = int(parts[1]) - 1

                field_order = config[constants.CONFIG_KEY_FIELD_ORDER]
                if 0 <= idx1 < len(field_order) and 0 <= idx2 < len(field_order):
                    field_order[idx1], field_order[idx2] = \
                        field_order[idx2], field_order[idx1]
                else:
                    print("Invalid positions")
                    input("Press Enter to continue...")
        except ValueError:
            print("Invalid input")
            input("Press Enter to continue...")
        return True

    return False

def progress_bar_settings_menu(config):
    """Menu for progress bar settings."""
    clear_screen()
    print("Progress Bar Settings")
    print("=" * 50)
    print()
    print(f"1. Toggle Progress Bars (Currently: {'On' if config[constants.CONFIG_KEY_SHOW_PROGRESS_BARS] else 'Off'})")
    print(f"2. Set Width (Currently: {config[constants.CONFIG_KEY_PROGRESS_BAR_WIDTH]})")
    print()
    print("0. Back to main menu")
    print()

    choice = input("Choice: ").strip()

    if choice == "1":
        config[constants.CONFIG_KEY_SHOW_PROGRESS_BARS] = not config[constants.CONFIG_KEY_SHOW_PROGRESS_BARS]
        return True
    elif choice == "2":
        try:
            width = int(input(f"Enter new width ({constants.MIN_PROGRESS_BAR_WIDTH}-{constants.MAX_PROGRESS_BAR_WIDTH}): ").strip())
            if constants.MIN_PROGRESS_BAR_WIDTH <= width <= constants.MAX_PROGRESS_BAR_WIDTH:
                config[constants.CONFIG_KEY_PROGRESS_BAR_WIDTH] = width
            else:
                print(f"Width must be between {constants.MIN_PROGRESS_BAR_WIDTH} and {constants.MAX_PROGRESS_BAR_WIDTH}")
                input("Press Enter to continue...")
        except ValueError:
            print("Invalid input")
            input("Press Enter to continue...")
        return True

    return choice != "0"

def preview_statusline(config):
    """Preview the statusline with mock data."""
    clear_screen()
    print("Statusline Preview")
    print("=" * 50)
    print()

    # Mock data
    mock_data = {
        constants.FIELD_MODEL: "claude-sonnet-4-5-20250929",
        constants.FIELD_VERSION: "v1.0.85",
        constants.FIELD_CONTEXT_REMAINING: 83,
        constants.FIELD_TOKENS: 14638846,
        constants.FIELD_CURRENT_DIR: "claude-code-statusline",
        constants.FIELD_GIT_BRANCH: "main",
        constants.FIELD_COST: 49.00,
        constants.FIELD_COST_PER_HOUR: 16.55,
        constants.FIELD_TOKENS_PER_MINUTE: 279900,
        constants.FIELD_DURATION: 11220000,
        constants.FIELD_LINES_CHANGED: 450,
        constants.FIELD_OUTPUT_STYLE: "default"
    }

    print("Compact Mode:")
    print("-" * 50)
    print(format_compact(mock_data, config))
    print()

    print("\nVerbose Mode:")
    print("-" * 50)
    print(format_verbose(mock_data, config))
    print()

    input("\nPress Enter to continue...")

def display_mode_menu(config):
    """Menu for changing display mode."""
    clear_screen()
    print("Display Mode")
    print("=" * 50)
    print()
    print(f"Current: {config[constants.CONFIG_KEY_DISPLAY_MODE]}")
    print()
    print(f"1. {constants.DISPLAY_MODE_COMPACT.capitalize()} - Icons and values only")
    print(f"2. {constants.DISPLAY_MODE_VERBOSE.capitalize()} - Labeled fields with descriptions")
    print()
    print("0. Back to main menu")
    print()

    choice = input("Choice: ").strip()

    if choice == "1":
        config[constants.CONFIG_KEY_DISPLAY_MODE] = constants.DISPLAY_MODE_COMPACT
    elif choice == "2":
        config[constants.CONFIG_KEY_DISPLAY_MODE] = constants.DISPLAY_MODE_VERBOSE

    return choice in ["1", "2"]

def main():
    """Main entry point for configure script."""
    config = load_config()

    while True:
        show_menu(config)
        choice = input("Choice: ").strip()

        if choice == "1":
            display_mode_menu(config)
        elif choice == "2":
            while toggle_fields_menu(config):
                pass
        elif choice == "3":
            while customize_icons_menu(config):
                pass
        elif choice == "4":
            while customize_colors_menu(config):
                pass
        elif choice == "5":
            while reorder_fields_menu(config):
                pass
        elif choice == "6":
            while progress_bar_settings_menu(config):
                pass
        elif choice == "7":
            config[constants.CONFIG_KEY_ENABLE_COLORS] = not config.get(constants.CONFIG_KEY_ENABLE_COLORS, constants.DEFAULT_ENABLE_COLORS)
        elif choice == "8":
            confirm = input("Reset to defaults? (y/n): ").strip().lower()
            if confirm == "y":
                config = get_default_config()
                print("Configuration reset to defaults")
                input("Press Enter to continue...")
        elif choice == "9":
            preview_statusline(config)
        elif choice == "10":
            save_config(config)
            print("\nConfiguration saved!")
            break
        elif choice == "0":
            print("\nExiting without saving")
            break
        else:
            print("\nInvalid choice")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()
