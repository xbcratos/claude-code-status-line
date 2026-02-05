"""Tests for git_utils module."""
import subprocess
import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch, mock_open

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from git_utils import get_git_branch


class TestGetGitBranch:
    """Tests for get_git_branch function."""

    def test_get_branch_from_git_head_file(self, tmp_path):
        """Test reading branch from .git/HEAD file."""
        git_dir = tmp_path / ".git"
        git_dir.mkdir()
        head_file = git_dir / "HEAD"
        head_file.write_text("ref: refs/heads/main\n")

        result = get_git_branch(str(tmp_path))
        assert result == "main"

    def test_get_branch_from_git_head_feature_branch(self, tmp_path):
        """Test reading feature branch from .git/HEAD."""
        git_dir = tmp_path / ".git"
        git_dir.mkdir()
        head_file = git_dir / "HEAD"
        head_file.write_text("ref: refs/heads/feature/awesome-feature\n")

        result = get_git_branch(str(tmp_path))
        assert result == "feature/awesome-feature"

    def test_detached_head_state(self, tmp_path):
        """Test handling detached HEAD (returns short commit hash)."""
        git_dir = tmp_path / ".git"
        git_dir.mkdir()
        head_file = git_dir / "HEAD"
        head_file.write_text("abc123def456789\n")

        result = get_git_branch(str(tmp_path))
        assert result == "abc123d"  # First 7 chars

    def test_git_worktree(self, tmp_path):
        """Test handling git worktrees where .git is a file."""
        git_file = tmp_path / ".git"
        actual_git_dir = tmp_path / "actual-git"
        actual_git_dir.mkdir()
        head_file = actual_git_dir / "HEAD"
        head_file.write_text("ref: refs/heads/worktree-branch\n")

        git_file.write_text(f"gitdir: {actual_git_dir}\n")

        result = get_git_branch(str(tmp_path))
        assert result == "worktree-branch"

    def test_no_git_repository(self, tmp_path):
        """Test returns empty string when not in a git repo."""
        result = get_git_branch(str(tmp_path))
        assert result == ""

    def test_fallback_to_git_command(self, tmp_path, monkeypatch):
        """Test falls back to git command when HEAD file doesn't exist."""
        # Create .git dir but no HEAD file
        git_dir = tmp_path / ".git"
        git_dir.mkdir()

        # Mock subprocess to return a branch name
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "command-branch\n"

        with patch('subprocess.run', return_value=mock_result) as mock_run:
            result = get_git_branch(str(tmp_path))
            assert result == "command-branch"
            mock_run.assert_called_once()

    def test_git_command_failure(self, tmp_path):
        """Test handles git command failure gracefully."""
        with patch('subprocess.run', side_effect=subprocess.SubprocessError):
            result = get_git_branch(str(tmp_path))
            assert result == ""

    def test_git_command_timeout(self, tmp_path):
        """Test handles git command timeout."""
        with patch('subprocess.run', side_effect=subprocess.TimeoutExpired('git', 2)):
            result = get_git_branch(str(tmp_path))
            assert result == ""

    def test_git_not_installed(self, tmp_path):
        """Test handles missing git binary."""
        with patch('subprocess.run', side_effect=FileNotFoundError):
            result = get_git_branch(str(tmp_path))
            assert result == ""

    def test_ioerror_reading_head_file(self, tmp_path):
        """Test handles IO errors when reading HEAD file."""
        git_dir = tmp_path / ".git"
        git_dir.mkdir()
        head_file = git_dir / "HEAD"
        head_file.write_text("ref: refs/heads/main\n")

        # Make file unreadable
        with patch('builtins.open', side_effect=IOError("Permission denied")):
            # Should fall back to git command
            with patch('subprocess.run') as mock_run:
                mock_run.return_value.returncode = 1
                result = get_git_branch(str(tmp_path))
                assert result == ""
