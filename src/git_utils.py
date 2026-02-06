import os
import subprocess
import json
from pathlib import Path
from typing import Optional, Tuple

import constants
from colors import colorize


def get_git_status(cwd: str) -> str:
    """
    Get git status indicators (dirty/clean, ahead/behind) with colors.

    Returns a formatted string with colored status indicators:
    - "✓" for clean (green)
    - "★" for dirty (yellow)
    - "↑N" for N commits ahead (cyan)
    - "↓N" for N commits behind (purple/magenta)

    Args:
        cwd: Current working directory path

    Returns:
        Status string with colored indicators (e.g., "★ ↑2", "✓", "★ ↓1 ↑3") or empty string
    """
    try:
        # Check if we're in a git repository
        result = subprocess.run(
            ['git', 'rev-parse', '--git-dir'],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=constants.GIT_COMMAND_TIMEOUT_SECONDS
        )
        if result.returncode != 0:
            return ""

        indicators = []

        # Check for uncommitted changes (green for clean, yellow for dirty)
        is_dirty = _is_git_dirty(cwd)
        if is_dirty is not None:
            if is_dirty:
                indicators.append(colorize("★", constants.COLOR_YELLOW))
            else:
                indicators.append(colorize("✓", constants.COLOR_GREEN))

        # Check for ahead/behind
        ahead, behind = _get_ahead_behind(cwd)
        if behind > 0:
            # Purple/magenta for behind
            indicators.append(colorize(f"↓{behind}", constants.COLOR_MAGENTA))
        if ahead > 0:
            # Cyan for ahead
            indicators.append(colorize(f"↑{ahead}", constants.COLOR_CYAN))

        return " ".join(indicators) if indicators else ""

    except (subprocess.SubprocessError, FileNotFoundError):
        return ""


def _is_git_dirty(cwd: str) -> Optional[bool]:
    """
    Check if git working directory has uncommitted changes.

    Args:
        cwd: Current working directory path

    Returns:
        True if dirty, False if clean, None if error
    """
    try:
        result = subprocess.run(
            ['git', 'status', '--porcelain'],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=constants.GIT_COMMAND_TIMEOUT_SECONDS
        )
        if result.returncode == 0:
            # If output is non-empty, there are changes
            return bool(result.stdout.strip())
    except (subprocess.SubprocessError, FileNotFoundError):
        pass

    return None


def _get_ahead_behind(cwd: str) -> Tuple[int, int]:
    """
    Get number of commits ahead and behind remote.

    Args:
        cwd: Current working directory path

    Returns:
        Tuple of (ahead_count, behind_count)
    """
    try:
        result = subprocess.run(
            ['git', 'rev-list', '--left-right', '--count', 'HEAD...@{upstream}'],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=constants.GIT_COMMAND_TIMEOUT_SECONDS
        )
        if result.returncode == 0:
            # Output format: "ahead\tbehind"
            parts = result.stdout.strip().split()
            if len(parts) == 2:
                ahead = int(parts[0])
                behind = int(parts[1])
                return (ahead, behind)
    except (subprocess.SubprocessError, FileNotFoundError, ValueError):
        pass

    return (0, 0)


def get_git_branch(cwd: str) -> str:
    """
    Get current git branch name.

    Uses fast file-based detection with command fallback.

    Args:
        cwd: Current working directory path

    Returns:
        Git branch name, short commit hash (detached HEAD), or empty string
    """
    try:
        # Method 1: Read .git/HEAD directly (faster)
        git_dir = Path(cwd) / ".git"

        if git_dir.is_file():
            # Handle git worktrees - .git is a file pointing to actual git dir
            with open(git_dir, 'r') as f:
                git_dir_line = f.read().strip()
                if git_dir_line.startswith('gitdir: '):
                    git_dir = Path(git_dir_line[8:])

        if git_dir.is_dir():
            head_file = git_dir / "HEAD"
            if head_file.exists():
                with open(head_file, 'r') as f:
                    content = f.read().strip()
                    if content.startswith(constants.GIT_HEAD_REF_PREFIX):
                        # Extract branch name after 'ref: refs/heads/'
                        return content[len(constants.GIT_HEAD_REF_PREFIX):]
                    # Detached HEAD state - return short commit hash
                    return content[:constants.GIT_DETACHED_HEAD_HASH_LENGTH]
    except (IOError, OSError):
        pass

    try:
        # Method 2: Fall back to git command
        result = subprocess.run(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=constants.GIT_COMMAND_TIMEOUT_SECONDS
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (subprocess.SubprocessError, FileNotFoundError):
        pass

    return ""


def get_pr_status(cwd: str) -> str:
    """
    Get PR status for the current branch using GitHub CLI.

    Returns a colored PR status string:
    - Green: PR is approved or all checks pass
    - Yellow: PR is in draft state
    - Red: PR has failing checks or changes requested

    Args:
        cwd: Current working directory path

    Returns:
        Colored PR status string (e.g., "PR#123") or empty string
    """
    try:
        # Check if gh CLI is available and we're in a GitHub repo
        # Use longer timeout for gh command since it makes API calls
        result = subprocess.run(
            ['gh', 'pr', 'view', '--json', 'number,isDraft,reviewDecision,statusCheckRollup'],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=constants.GH_COMMAND_TIMEOUT_SECONDS
        )

        if result.returncode != 0:
            # No PR for this branch or gh not available
            return ""

        pr_data = json.loads(result.stdout)
        pr_number = pr_data.get('number')
        if not pr_number:
            return ""

        # Determine color based on PR state
        is_draft = pr_data.get('isDraft', False)
        review_decision = pr_data.get('reviewDecision', '')
        status_checks = pr_data.get('statusCheckRollup', [])

        # Determine overall status
        color = 'green'  # Default to green (optimistic)

        if is_draft:
            color = 'yellow'
        elif review_decision == 'CHANGES_REQUESTED':
            color = 'red'
        elif status_checks:
            # Check if any status checks failed
            for check in status_checks:
                status = check.get('status') or check.get('conclusion')
                if status in ['FAILURE', 'ERROR', 'CANCELLED', 'TIMED_OUT']:
                    color = 'red'
                    break
                elif status in ['PENDING', 'IN_PROGRESS']:
                    color = 'yellow'
                    break

        pr_text = f"PR#{pr_number}"
        return colorize(pr_text, color)

    except (subprocess.SubprocessError, FileNotFoundError, json.JSONDecodeError, ValueError):
        # gh not installed, timeout, or invalid JSON
        return ""
