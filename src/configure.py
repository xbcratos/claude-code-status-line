#!/usr/bin/env python3
import sys
from pathlib import Path

# Require Python 3.6+
if sys.version_info < (3, 6):
    print("Error: Python 3.6 or higher is required", file=sys.stderr)
    print(f"Current version: {sys.version}", file=sys.stderr)
    sys.exit(1)

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from config_manager import load_config, save_config, get_default_config
from display_formatter import format_compact, format_verbose
import colors

def clear_screen():
    """Clear the terminal screen."""
    print("\033[2J\033[H", end="")

def show_menu(config):
    """Display main configuration menu."""
    clear_screen()
    print("Claude Code Statusline Configuration")
    print("=" * 50)
    print()

    print(f"1. Display Mode")
    print(f"   Current: {config['display_mode']}")
    print(f"   Options: [compact, verbose]")
    print()

    print("2. Toggle Visible Fields")
    visible = config["visible_fields"]
    field_names = {
        "model": "Model Name",
        "version": "Version",
        "context_remaining": "Context Remaining",
        "tokens": "Tokens",
        "current_dir": "Current Directory",
        "git_branch": "Git Branch",
        "cost": "Cost",
        "duration": "Duration",
        "lines_changed": "Lines Changed",
        "output_style": "Output Style"
    }
    for field, label in field_names.items():
        status = "✓" if visible.get(field, False) else "✗"
        print(f"   {status} {label}")
    print()

    print("3. Customize Icons")
    print("4. Customize Colors")
    print("5. Reorder Fields")
    print(f"6. Progress Bar Settings (Currently: {'On' if config['show_progress_bars'] else 'Off'}, Width: {config['progress_bar_width']})")
    print(f"7. Toggle Colors On/Off (Currently: {'On' if config['enable_colors'] else 'Off'})")
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

    visible = config["visible_fields"]
    field_names = {
        "1": ("model", "Model Name"),
        "2": ("version", "Version"),
        "3": ("context_remaining", "Context Remaining"),
        "4": ("tokens", "Tokens"),
        "5": ("current_dir", "Current Directory"),
        "6": ("git_branch", "Git Branch"),
        "7": ("cost", "Cost"),
        "8": ("duration", "Duration"),
        "9": ("lines_changed", "Lines Changed"),
        "10": ("output_style", "Output Style")
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

    icons = config["icons"]
    icon_names = {
        "1": ("directory", "Directory"),
        "2": ("git_branch", "Git Branch"),
        "3": ("model", "Model"),
        "4": ("version", "Version"),
        "5": ("context", "Context"),
        "6": ("cost", "Cost"),
        "7": ("tokens", "Tokens"),
        "8": ("duration", "Duration"),
        "9": ("style", "Style")
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
        "1": ("directory", "Directory"),
        "2": ("git_branch", "Git Branch"),
        "3": ("model", "Model"),
        "4": ("version", "Version"),
        "5": ("context", "Context"),
        "6": ("cost", "Cost"),
        "7": ("tokens", "Tokens"),
        "8": ("duration", "Duration"),
        "9": ("style", "Style"),
        "10": ("progress_bar_filled", "Progress Bar (Filled)"),
        "11": ("progress_bar_empty", "Progress Bar (Empty)"),
        "12": ("separator", "Separator")
    }

    color_config = config["colors"]

    for num, (field, label) in color_fields.items():
        current = color_config.get(field, "white")
        print(f"{num}. {label}: {current}")

    print()
    print("Available colors: cyan, green, blue, magenta, yellow, red, white")
    print()
    print("0. Back to main menu")
    print()

    choice = input("Select field to change color (enter number): ").strip()

    if choice in color_fields:
        field, label = color_fields[choice]
        print(f"\nAvailable colors: cyan, green, blue, magenta, yellow, red, white")
        new_color = input(f"Enter new color for {label}: ").strip().lower()

        valid_colors = ["cyan", "green", "blue", "magenta", "yellow", "red", "white"]
        if new_color in valid_colors:
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
        "current_dir": "Current Directory",
        "git_branch": "Git Branch",
        "model": "Model",
        "version": "Version",
        "context_remaining": "Context Remaining",
        "tokens": "Tokens",
        "cost": "Cost",
        "duration": "Duration",
        "lines_changed": "Lines Changed",
        "output_style": "Output Style"
    }

    for i, field in enumerate(config["field_order"], 1):
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

                if 0 <= idx1 < len(config["field_order"]) and 0 <= idx2 < len(config["field_order"]):
                    config["field_order"][idx1], config["field_order"][idx2] = \
                        config["field_order"][idx2], config["field_order"][idx1]
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
    print(f"1. Toggle Progress Bars (Currently: {'On' if config['show_progress_bars'] else 'Off'})")
    print(f"2. Set Width (Currently: {config['progress_bar_width']})")
    print()
    print("0. Back to main menu")
    print()

    choice = input("Choice: ").strip()

    if choice == "1":
        config["show_progress_bars"] = not config["show_progress_bars"]
        return True
    elif choice == "2":
        try:
            width = int(input("Enter new width (5-50): ").strip())
            if 5 <= width <= 50:
                config["progress_bar_width"] = width
            else:
                print("Width must be between 5 and 50")
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
        "model": "claude-sonnet-4-5-20250929",
        "version": "v1.0.85",
        "context_remaining": 83,
        "tokens": 14638846,
        "current_dir": "claude-code-statusline",
        "git_branch": "main",
        "cost": 49.00,
        "cost_per_hour": 16.55,
        "tokens_per_minute": 279900,
        "duration": 11220000,
        "lines_changed": 450,
        "output_style": "default"
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
    print(f"Current: {config['display_mode']}")
    print()
    print("1. Compact - Icons and values only")
    print("2. Verbose - Labeled fields with descriptions")
    print()
    print("0. Back to main menu")
    print()

    choice = input("Choice: ").strip()

    if choice == "1":
        config["display_mode"] = "compact"
    elif choice == "2":
        config["display_mode"] = "verbose"

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
            config["enable_colors"] = not config.get("enable_colors", True)
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
