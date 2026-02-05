"""
Data extraction for the Claude Code Statusline Tool.

This module handles extracting and transforming Claude Code JSON data
into a structured format for display.
"""

import os
from datetime import datetime
from typing import Dict, Any

from git_utils import get_git_branch, get_git_status, get_pr_status
from system_utils import get_cpu_usage, get_memory_usage, get_battery_status
from python_utils import get_python_version, get_python_venv


class DataExtractor:
    """
    Extracts and transforms Claude Code JSON data.

    This class breaks down the complex extraction logic into specialized
    methods, each handling a specific aspect of the data extraction process.
    """

    def extract(self, json_data: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract all relevant fields from Claude Code JSON input.

        Args:
            json_data: Raw JSON data from Claude Code
            config: Configuration dictionary (unused currently, for future extensibility)

        Returns:
            Dictionary containing extracted and computed fields
        """
        data = {}
        data.update(self._extract_model(json_data))
        data.update(self._extract_version(json_data))
        data.update(self._extract_context(json_data))
        data.update(self._extract_workspace(json_data))
        # Pass accumulated data for cross-field calculations (e.g., tokens_per_minute)
        data.update(self._extract_cost(json_data, data))
        data.update(self._extract_output_style(json_data))
        # System and environment fields
        data.update(self._extract_system_info())
        data.update(self._extract_python_info())
        data.update(self._extract_datetime())
        return data

    def _extract_model(self, json_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract model information.

        Prefers model ID over display name for specificity.

        Args:
            json_data: Raw JSON data

        Returns:
            Dictionary with 'model' key if available
        """
        data = {}
        if "model" in json_data:
            if "id" in json_data["model"]:
                data["model"] = json_data["model"]["id"]
            elif "display_name" in json_data["model"]:
                # Fallback to display_name if id not available
                data["model"] = json_data["model"]["display_name"]
        return data

    def _extract_version(self, json_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract version information.

        Args:
            json_data: Raw JSON data

        Returns:
            Dictionary with 'version' key if available
        """
        data = {}
        if "version" in json_data:
            data["version"] = json_data["version"]
        return data

    def _extract_context(self, json_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract context window information.

        Includes context remaining percentage and total tokens
        (sum of input and output tokens).

        Args:
            json_data: Raw JSON data

        Returns:
            Dictionary with 'context_remaining' and 'tokens' keys if available
        """
        data = {}
        if "context_window" in json_data:
            cw = json_data["context_window"]

            # Context remaining percentage
            if "remaining_percentage" in cw:
                data["context_remaining"] = int(cw["remaining_percentage"])

            # Total tokens (input + output)
            total_tokens = 0
            if "total_input_tokens" in cw:
                total_tokens += cw["total_input_tokens"]
            if "total_output_tokens" in cw:
                total_tokens += cw["total_output_tokens"]

            if total_tokens > 0:
                data["tokens"] = total_tokens

        return data

    def _extract_workspace(self, json_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract workspace information.

        Includes current directory (basename only) and git branch with status.

        Args:
            json_data: Raw JSON data

        Returns:
            Dictionary with 'current_dir' and optionally 'git_branch' keys
        """
        data = {}
        if "workspace" in json_data and "current_dir" in json_data["workspace"]:
            cwd = json_data["workspace"]["current_dir"]
            data["current_dir"] = os.path.basename(cwd) or cwd

            # Get git branch for the workspace
            git_branch = get_git_branch(cwd)
            if git_branch:
                parts = [git_branch]

                # Add git status if available
                git_status = get_git_status(cwd)
                if git_status:
                    parts.append(git_status)

                # Add PR status if available
                pr_status = get_pr_status(cwd)
                if pr_status:
                    parts.append(pr_status)

                data["git_branch"] = " ".join(parts)

        return data

    def _extract_cost(self, json_data: Dict[str, Any], accumulated_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract cost and performance metrics.

        Includes:
        - Total cost in USD
        - Duration in milliseconds
        - Cost per hour (calculated)
        - Tokens per minute (calculated, uses tokens from accumulated_data)
        - Lines changed (added + removed)

        Args:
            json_data: Raw JSON data
            accumulated_data: Data extracted so far (used for cross-field calculations)

        Returns:
            Dictionary with cost-related fields if available
        """
        data = {}
        if "cost" in json_data:
            cost_data = json_data["cost"]

            # Total cost
            if "total_cost_usd" in cost_data:
                data["cost"] = cost_data["total_cost_usd"]

            # Duration and calculated rates
            if "total_duration_ms" in cost_data:
                duration_ms = cost_data["total_duration_ms"]
                data["duration"] = duration_ms

                # Calculate cost per hour
                if data.get("cost") and duration_ms > 0:
                    duration_hours = duration_ms / (1000 * 60 * 60)
                    data["cost_per_hour"] = data["cost"] / duration_hours if duration_hours > 0 else 0

                # Calculate tokens per minute
                # Use tokens from accumulated_data (extracted in _extract_context)
                if accumulated_data.get("tokens") and duration_ms > 0:
                    duration_minutes = duration_ms / (1000 * 60)
                    data["tokens_per_minute"] = int(accumulated_data["tokens"] / duration_minutes) if duration_minutes > 0 else 0

            # Lines changed (added + removed)
            lines_added = cost_data.get("total_lines_added", 0)
            lines_removed = cost_data.get("total_lines_removed", 0)
            if lines_added > 0 or lines_removed > 0:
                data["lines_changed"] = lines_added + lines_removed

        return data

    def _extract_output_style(self, json_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract output style information.

        Args:
            json_data: Raw JSON data

        Returns:
            Dictionary with 'output_style' key if available
        """
        data = {}
        if "output_style" in json_data and "name" in json_data["output_style"]:
            data["output_style"] = json_data["output_style"]["name"]
        return data

    def _extract_system_info(self) -> Dict[str, Any]:
        """
        Extract system monitoring information.

        Includes CPU usage, memory usage, and battery status.

        Returns:
            Dictionary with system info fields if available
        """
        data = {}

        cpu = get_cpu_usage()
        if cpu:
            data["cpu_usage"] = cpu

        memory = get_memory_usage()
        if memory:
            data["memory_usage"] = memory

        battery = get_battery_status()
        if battery:
            data["battery"] = battery

        return data

    def _extract_python_info(self) -> Dict[str, Any]:
        """
        Extract Python environment information.

        Includes Python version and virtual environment name.

        Returns:
            Dictionary with Python info fields if available
        """
        data = {}

        python_version = get_python_version()
        if python_version:
            data["python_version"] = python_version

        venv = get_python_venv()
        if venv:
            data["python_venv"] = venv

        return data

    def _extract_datetime(self) -> Dict[str, Any]:
        """
        Extract current date and time.

        Returns:
            Dictionary with 'datetime' key
        """
        data = {}
        now = datetime.now()
        # Format with seconds precision: YYYY-MM-DD HH:MM:SS
        data["datetime"] = now.strftime("%Y-%m-%d %H:%M:%S")
        return data


# ============================================================================
# Module-level convenience function (backward compatibility)
# ============================================================================

# Create default extractor instance
_default_extractor = DataExtractor()


def extract_data(json_data: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract relevant fields from Claude Code JSON input.

    This is a convenience function that uses a default DataExtractor instance
    for backward compatibility.

    Args:
        json_data: Raw JSON data from Claude Code
        config: Configuration dictionary

    Returns:
        Dictionary containing extracted and computed fields
    """
    return _default_extractor.extract(json_data, config)
