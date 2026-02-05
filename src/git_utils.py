import os
import subprocess
from pathlib import Path
from typing import Optional, Tuple

import constants


def get_git_status(cwd: str) -> str:
    """
    Get git status indicators (dirty/clean, ahead/behind).

    Returns a formatted string with status indicators:
    - "✓" for clean
    - "★" for dirty (uncommitted changes)
    - "↑N" for N commits ahead
    - "↓N" for N commits behind

    Args:
        cwd: Current working directory path

    Returns:
        Status string (e.g., "★ ↑2", "✓", "★ ↓1 ↑3") or empty string
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

        # Check for uncommitted changes
        is_dirty = _is_git_dirty(cwd)
        if is_dirty is not None:
            indicators.append("★" if is_dirty else "✓")

        # Check for ahead/behind
        ahead, behind = _get_ahead_behind(cwd)
        if behind > 0:
            indicators.append(f"↓{behind}")
        if ahead > 0:
            indicators.append(f"↑{ahead}")

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
