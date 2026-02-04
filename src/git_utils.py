import os
import subprocess
from pathlib import Path

def get_git_branch(cwd):
    """Get current git branch name."""
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
                    if content.startswith('ref: refs/heads/'):
                        return content[16:]  # Extract branch name
                    # Detached HEAD state - return short commit hash
                    return content[:7]
    except (IOError, OSError):
        pass

    try:
        # Method 2: Fall back to git command
        result = subprocess.run(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=2
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (subprocess.SubprocessError, FileNotFoundError):
        pass

    return ""
