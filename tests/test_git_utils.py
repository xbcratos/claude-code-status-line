"""Tests for git_utils module."""
import subprocess
import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch, mock_open

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from git_utils import get_git_branch, get_git_status, _is_git_dirty, _get_ahead_behind, get_pr_status


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


class TestIsGitDirty:
    """Tests for _is_git_dirty function."""

    def test_clean_repository(self, tmp_path):
        """Test returns False for clean repository."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = ""

        with patch('subprocess.run', return_value=mock_result):
            result = _is_git_dirty(str(tmp_path))
            assert result is False

    def test_dirty_repository_with_changes(self, tmp_path):
        """Test returns True when there are uncommitted changes."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = " M src/file.py\n"

        with patch('subprocess.run', return_value=mock_result):
            result = _is_git_dirty(str(tmp_path))
            assert result is True

    def test_dirty_repository_with_untracked_files(self, tmp_path):
        """Test returns True for untracked files."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "?? newfile.py\n"

        with patch('subprocess.run', return_value=mock_result):
            result = _is_git_dirty(str(tmp_path))
            assert result is True

    def test_git_command_failure(self, tmp_path):
        """Test returns None when git command fails."""
        mock_result = Mock()
        mock_result.returncode = 128

        with patch('subprocess.run', return_value=mock_result):
            result = _is_git_dirty(str(tmp_path))
            assert result is None

    def test_git_not_installed(self, tmp_path):
        """Test returns None when git is not installed."""
        with patch('subprocess.run', side_effect=FileNotFoundError):
            result = _is_git_dirty(str(tmp_path))
            assert result is None

    def test_subprocess_error(self, tmp_path):
        """Test returns None on subprocess error."""
        with patch('subprocess.run', side_effect=subprocess.SubprocessError):
            result = _is_git_dirty(str(tmp_path))
            assert result is None


class TestGetAheadBehind:
    """Tests for _get_ahead_behind function."""

    def test_up_to_date_with_remote(self, tmp_path):
        """Test returns (0, 0) when up-to-date with remote."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "0\t0\n"

        with patch('subprocess.run', return_value=mock_result):
            ahead, behind = _get_ahead_behind(str(tmp_path))
            assert ahead == 0
            assert behind == 0

    def test_ahead_of_remote(self, tmp_path):
        """Test returns correct count when ahead of remote."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "3\t0\n"

        with patch('subprocess.run', return_value=mock_result):
            ahead, behind = _get_ahead_behind(str(tmp_path))
            assert ahead == 3
            assert behind == 0

    def test_behind_remote(self, tmp_path):
        """Test returns correct count when behind remote."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "0\t5\n"

        with patch('subprocess.run', return_value=mock_result):
            ahead, behind = _get_ahead_behind(str(tmp_path))
            assert ahead == 0
            assert behind == 5

    def test_both_ahead_and_behind(self, tmp_path):
        """Test returns correct counts when both ahead and behind."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "2\t3\n"

        with patch('subprocess.run', return_value=mock_result):
            ahead, behind = _get_ahead_behind(str(tmp_path))
            assert ahead == 2
            assert behind == 3

    def test_no_upstream_branch(self, tmp_path):
        """Test returns (0, 0) when no upstream branch is configured."""
        mock_result = Mock()
        mock_result.returncode = 128
        mock_result.stdout = ""

        with patch('subprocess.run', return_value=mock_result):
            ahead, behind = _get_ahead_behind(str(tmp_path))
            assert ahead == 0
            assert behind == 0

    def test_git_command_failure(self, tmp_path):
        """Test returns (0, 0) on git command failure."""
        with patch('subprocess.run', side_effect=subprocess.SubprocessError):
            ahead, behind = _get_ahead_behind(str(tmp_path))
            assert ahead == 0
            assert behind == 0

    def test_invalid_output_format(self, tmp_path):
        """Test returns (0, 0) when output format is unexpected."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "invalid\n"

        with patch('subprocess.run', return_value=mock_result):
            ahead, behind = _get_ahead_behind(str(tmp_path))
            assert ahead == 0
            assert behind == 0

    def test_non_integer_values(self, tmp_path):
        """Test returns (0, 0) when output contains non-integer values."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "abc\tdef\n"

        with patch('subprocess.run', return_value=mock_result):
            ahead, behind = _get_ahead_behind(str(tmp_path))
            assert ahead == 0
            assert behind == 0


class TestGetGitStatus:
    """Tests for get_git_status function."""

    def test_clean_and_up_to_date(self, tmp_path):
        """Test shows checkmark for clean, up-to-date repository."""
        # Mock git rev-parse (check if in git repo)
        mock_rev_parse = Mock()
        mock_rev_parse.returncode = 0

        # Mock git status --porcelain (clean)
        mock_status = Mock()
        mock_status.returncode = 0
        mock_status.stdout = ""

        # Mock git rev-list (up-to-date)
        mock_rev_list = Mock()
        mock_rev_list.returncode = 0
        mock_rev_list.stdout = "0\t0\n"

        with patch('subprocess.run', side_effect=[mock_rev_parse, mock_status, mock_rev_list]):
            result = get_git_status(str(tmp_path))
            assert result == "✓"

    def test_dirty_repository(self, tmp_path):
        """Test shows star for dirty repository."""
        mock_rev_parse = Mock()
        mock_rev_parse.returncode = 0

        mock_status = Mock()
        mock_status.returncode = 0
        mock_status.stdout = " M file.py\n"

        mock_rev_list = Mock()
        mock_rev_list.returncode = 0
        mock_rev_list.stdout = "0\t0\n"

        with patch('subprocess.run', side_effect=[mock_rev_parse, mock_status, mock_rev_list]):
            result = get_git_status(str(tmp_path))
            assert result == "★"

    def test_ahead_of_remote(self, tmp_path):
        """Test shows ahead indicator."""
        mock_rev_parse = Mock()
        mock_rev_parse.returncode = 0

        mock_status = Mock()
        mock_status.returncode = 0
        mock_status.stdout = ""

        mock_rev_list = Mock()
        mock_rev_list.returncode = 0
        mock_rev_list.stdout = "2\t0\n"

        with patch('subprocess.run', side_effect=[mock_rev_parse, mock_status, mock_rev_list]):
            result = get_git_status(str(tmp_path))
            assert result == "✓ ↑2"

    def test_behind_remote(self, tmp_path):
        """Test shows behind indicator."""
        mock_rev_parse = Mock()
        mock_rev_parse.returncode = 0

        mock_status = Mock()
        mock_status.returncode = 0
        mock_status.stdout = ""

        mock_rev_list = Mock()
        mock_rev_list.returncode = 0
        mock_rev_list.stdout = "0\t3\n"

        with patch('subprocess.run', side_effect=[mock_rev_parse, mock_status, mock_rev_list]):
            result = get_git_status(str(tmp_path))
            assert result == "✓ ↓3"

    def test_dirty_ahead_and_behind(self, tmp_path):
        """Test shows all indicators when dirty, ahead, and behind."""
        mock_rev_parse = Mock()
        mock_rev_parse.returncode = 0

        mock_status = Mock()
        mock_status.returncode = 0
        mock_status.stdout = "?? newfile.py\n"

        mock_rev_list = Mock()
        mock_rev_list.returncode = 0
        mock_rev_list.stdout = "1\t2\n"

        with patch('subprocess.run', side_effect=[mock_rev_parse, mock_status, mock_rev_list]):
            result = get_git_status(str(tmp_path))
            assert result == "★ ↓2 ↑1"

    def test_not_in_git_repository(self, tmp_path):
        """Test returns empty string when not in git repository."""
        mock_result = Mock()
        mock_result.returncode = 128

        with patch('subprocess.run', return_value=mock_result):
            result = get_git_status(str(tmp_path))
            assert result == ""

    def test_git_command_error(self, tmp_path):
        """Test returns empty string on git command error."""
        with patch('subprocess.run', side_effect=subprocess.SubprocessError):
            result = get_git_status(str(tmp_path))
            assert result == ""

    def test_git_not_installed(self, tmp_path):
        """Test returns empty string when git is not installed."""
        with patch('subprocess.run', side_effect=FileNotFoundError):
            result = get_git_status(str(tmp_path))
            assert result == ""


class TestGetPRStatus:
    """Tests for get_pr_status function."""

    def test_approved_pr_shows_green(self, tmp_path):
        """Test shows green color for approved PR."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = '{"number": 123, "isDraft": false, "reviewDecision": "APPROVED", "statusCheckRollup": []}'

        with patch('subprocess.run', return_value=mock_result):
            result = get_pr_status(str(tmp_path))
            # Should contain PR#123 with green color code
            assert "PR#123" in result
            assert "\033[92m" in result  # Green color code

    def test_draft_pr_shows_yellow(self, tmp_path):
        """Test shows yellow color for draft PR."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = '{"number": 456, "isDraft": true, "reviewDecision": "", "statusCheckRollup": []}'

        with patch('subprocess.run', return_value=mock_result):
            result = get_pr_status(str(tmp_path))
            # Should contain PR#456 with yellow color code
            assert "PR#456" in result
            assert "\033[93m" in result  # Yellow color code

    def test_changes_requested_shows_red(self, tmp_path):
        """Test shows red color for PR with changes requested."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = '{"number": 789, "isDraft": false, "reviewDecision": "CHANGES_REQUESTED", "statusCheckRollup": []}'

        with patch('subprocess.run', return_value=mock_result):
            result = get_pr_status(str(tmp_path))
            # Should contain PR#789 with red color code
            assert "PR#789" in result
            assert "\033[91m" in result  # Red color code

    def test_failing_checks_show_red(self, tmp_path):
        """Test shows red color for PR with failing status checks."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = '{"number": 100, "isDraft": false, "reviewDecision": "", "statusCheckRollup": [{"status": "FAILURE"}]}'

        with patch('subprocess.run', return_value=mock_result):
            result = get_pr_status(str(tmp_path))
            # Should contain PR#100 with red color code
            assert "PR#100" in result
            assert "\033[91m" in result  # Red color code

    def test_pending_checks_show_yellow(self, tmp_path):
        """Test shows yellow color for PR with pending status checks."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = '{"number": 200, "isDraft": false, "reviewDecision": "", "statusCheckRollup": [{"status": "PENDING"}]}'

        with patch('subprocess.run', return_value=mock_result):
            result = get_pr_status(str(tmp_path))
            # Should contain PR#200 with yellow color code
            assert "PR#200" in result
            assert "\033[93m" in result  # Yellow color code

    def test_passing_checks_show_green(self, tmp_path):
        """Test shows green color for PR with passing status checks."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = '{"number": 300, "isDraft": false, "reviewDecision": "", "statusCheckRollup": [{"status": "SUCCESS"}]}'

        with patch('subprocess.run', return_value=mock_result):
            result = get_pr_status(str(tmp_path))
            # Should contain PR#300 with green color code
            assert "PR#300" in result
            assert "\033[92m" in result  # Green color code

    def test_no_pr_returns_empty_string(self, tmp_path):
        """Test returns empty string when no PR exists for branch."""
        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stdout = ""

        with patch('subprocess.run', return_value=mock_result):
            result = get_pr_status(str(tmp_path))
            assert result == ""

    def test_gh_not_installed_returns_empty_string(self, tmp_path):
        """Test returns empty string when gh CLI is not installed."""
        with patch('subprocess.run', side_effect=FileNotFoundError):
            result = get_pr_status(str(tmp_path))
            assert result == ""

    def test_gh_command_timeout(self, tmp_path):
        """Test handles gh command timeout gracefully."""
        with patch('subprocess.run', side_effect=subprocess.TimeoutExpired('gh', 0.5)):
            result = get_pr_status(str(tmp_path))
            assert result == ""

    def test_invalid_json_returns_empty_string(self, tmp_path):
        """Test returns empty string when gh returns invalid JSON."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "invalid json"

        with patch('subprocess.run', return_value=mock_result):
            result = get_pr_status(str(tmp_path))
            assert result == ""

    def test_missing_pr_number_returns_empty_string(self, tmp_path):
        """Test returns empty string when PR number is missing."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = '{"isDraft": false, "reviewDecision": ""}'

        with patch('subprocess.run', return_value=mock_result):
            result = get_pr_status(str(tmp_path))
            assert result == ""

    def test_subprocess_error_returns_empty_string(self, tmp_path):
        """Test returns empty string on subprocess error."""
        with patch('subprocess.run', side_effect=subprocess.SubprocessError):
            result = get_pr_status(str(tmp_path))
            assert result == ""

    def test_checks_with_conclusion_field(self, tmp_path):
        """Test handles status checks with 'conclusion' field instead of 'status'."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = '{"number": 400, "isDraft": false, "reviewDecision": "", "statusCheckRollup": [{"conclusion": "FAILURE"}]}'

        with patch('subprocess.run', return_value=mock_result):
            result = get_pr_status(str(tmp_path))
            # Should contain PR#400 with red color code
            assert "PR#400" in result
            assert "\033[91m" in result  # Red color code

    def test_error_status_shows_red(self, tmp_path):
        """Test shows red color for PR with ERROR status."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = '{"number": 500, "isDraft": false, "reviewDecision": "", "statusCheckRollup": [{"status": "ERROR"}]}'

        with patch('subprocess.run', return_value=mock_result):
            result = get_pr_status(str(tmp_path))
            assert "PR#500" in result
            assert "\033[91m" in result  # Red color code

    def test_cancelled_status_shows_red(self, tmp_path):
        """Test shows red color for PR with CANCELLED status."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = '{"number": 600, "isDraft": false, "reviewDecision": "", "statusCheckRollup": [{"status": "CANCELLED"}]}'

        with patch('subprocess.run', return_value=mock_result):
            result = get_pr_status(str(tmp_path))
            assert "PR#600" in result
            assert "\033[91m" in result  # Red color code

    def test_in_progress_status_shows_yellow(self, tmp_path):
        """Test shows yellow color for PR with IN_PROGRESS status."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = '{"number": 700, "isDraft": false, "reviewDecision": "", "statusCheckRollup": [{"status": "IN_PROGRESS"}]}'

        with patch('subprocess.run', return_value=mock_result):
            result = get_pr_status(str(tmp_path))
            assert "PR#700" in result
            assert "\033[93m" in result  # Yellow color code
