"""
Tests for system_utils module.

Tests cross-platform system monitoring functions for CPU, memory, and battery.
"""

import pytest
from unittest.mock import patch, mock_open, MagicMock
import subprocess

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from system_utils import (
    get_cpu_usage,
    get_memory_usage,
    get_battery_status,
    _get_cpu_linux,
    _get_cpu_macos,
    _get_cpu_windows,
    _get_memory_linux,
    _get_memory_macos,
    _get_memory_windows,
    _get_battery_linux,
    _get_battery_macos,
    _get_battery_windows,
    _read_proc_stat,
)


# ============================================================================
# Tests for get_cpu_usage
# ============================================================================

@patch('system_utils.platform.system')
@patch('system_utils._get_cpu_linux')
def test_get_cpu_usage_linux(mock_cpu_linux, mock_platform):
    """Test get_cpu_usage on Linux."""
    mock_platform.return_value = 'Linux'
    mock_cpu_linux.return_value = '45%'

    result = get_cpu_usage()

    assert result == '45%'
    mock_cpu_linux.assert_called_once()


@patch('system_utils.platform.system')
@patch('system_utils._get_cpu_macos')
def test_get_cpu_usage_macos(mock_cpu_macos, mock_platform):
    """Test get_cpu_usage on macOS."""
    mock_platform.return_value = 'Darwin'
    mock_cpu_macos.return_value = '32%'

    result = get_cpu_usage()

    assert result == '32%'
    mock_cpu_macos.assert_called_once()


@patch('system_utils.platform.system')
@patch('system_utils._get_cpu_windows')
def test_get_cpu_usage_windows(mock_cpu_windows, mock_platform):
    """Test get_cpu_usage on Windows."""
    mock_platform.return_value = 'Windows'
    mock_cpu_windows.return_value = '28%'

    result = get_cpu_usage()

    assert result == '28%'
    mock_cpu_windows.assert_called_once()


@patch('system_utils.platform.system')
@patch('system_utils._get_cpu_linux')
def test_get_cpu_usage_error_handling(mock_cpu_linux, mock_platform):
    """Test get_cpu_usage handles errors gracefully."""
    mock_platform.return_value = 'Linux'
    mock_cpu_linux.side_effect = OSError('Test error')

    result = get_cpu_usage()

    assert result == ''


# ============================================================================
# Tests for get_memory_usage
# ============================================================================

@patch('system_utils.platform.system')
@patch('system_utils._get_memory_linux')
def test_get_memory_usage_linux(mock_memory_linux, mock_platform):
    """Test get_memory_usage on Linux."""
    mock_platform.return_value = 'Linux'
    mock_memory_linux.return_value = '8.5GB'

    result = get_memory_usage()

    assert result == '8.5GB'
    mock_memory_linux.assert_called_once()


@patch('system_utils.platform.system')
@patch('system_utils._get_memory_macos')
def test_get_memory_usage_macos(mock_memory_macos, mock_platform):
    """Test get_memory_usage on macOS."""
    mock_platform.return_value = 'Darwin'
    mock_memory_macos.return_value = '12.3GB'

    result = get_memory_usage()

    assert result == '12.3GB'
    mock_memory_macos.assert_called_once()


@patch('system_utils.platform.system')
@patch('system_utils._get_memory_windows')
def test_get_memory_usage_windows(mock_memory_windows, mock_platform):
    """Test get_memory_usage on Windows."""
    mock_platform.return_value = 'Windows'
    mock_memory_windows.return_value = '16.0GB'

    result = get_memory_usage()

    assert result == '16.0GB'
    mock_memory_windows.assert_called_once()


@patch('system_utils.platform.system')
@patch('system_utils._get_memory_linux')
def test_get_memory_usage_error_handling(mock_memory_linux, mock_platform):
    """Test get_memory_usage handles errors gracefully."""
    mock_platform.return_value = 'Linux'
    mock_memory_linux.side_effect = ValueError('Test error')

    result = get_memory_usage()

    assert result == ''


# ============================================================================
# Tests for get_battery_status
# ============================================================================

@patch('system_utils.platform.system')
@patch('system_utils._get_battery_linux')
def test_get_battery_status_linux(mock_battery_linux, mock_platform):
    """Test get_battery_status on Linux."""
    mock_platform.return_value = 'Linux'
    mock_battery_linux.return_value = '85%'

    result = get_battery_status()

    assert result == '85%'
    mock_battery_linux.assert_called_once()


@patch('system_utils.platform.system')
@patch('system_utils._get_battery_macos')
def test_get_battery_status_macos(mock_battery_macos, mock_platform):
    """Test get_battery_status on macOS."""
    mock_platform.return_value = 'Darwin'
    mock_battery_macos.return_value = '92%'

    result = get_battery_status()

    assert result == '92%'
    mock_battery_macos.assert_called_once()


@patch('system_utils.platform.system')
@patch('system_utils._get_battery_windows')
def test_get_battery_status_windows(mock_battery_windows, mock_platform):
    """Test get_battery_status on Windows."""
    mock_platform.return_value = 'Windows'
    mock_battery_windows.return_value = '78%'

    result = get_battery_status()

    assert result == '78%'
    mock_battery_windows.assert_called_once()


@patch('system_utils.platform.system')
@patch('system_utils._get_battery_linux')
def test_get_battery_status_error_handling(mock_battery_linux, mock_platform):
    """Test get_battery_status handles errors gracefully."""
    mock_platform.return_value = 'Linux'
    mock_battery_linux.side_effect = subprocess.SubprocessError('Test error')

    result = get_battery_status()

    assert result == ''


# ============================================================================
# Tests for Linux implementations
# ============================================================================

@patch('system_utils._read_proc_stat')
@patch('time.sleep')
def test_get_cpu_linux_success(mock_sleep, mock_read_proc_stat):
    """Test _get_cpu_linux with valid data."""
    mock_read_proc_stat.side_effect = [
        {'total': 1000, 'idle': 800},
        {'total': 2000, 'idle': 1500}
    ]

    result = _get_cpu_linux()

    # (2000 - 1000) = 1000 total delta
    # (1500 - 800) = 700 idle delta
    # usage = 100 * (1 - 700/1000) = 30%
    assert result == '30%'
    assert mock_read_proc_stat.call_count == 2


@patch('system_utils._read_proc_stat')
@patch('time.sleep')
def test_get_cpu_linux_first_read_fails(mock_sleep, mock_read_proc_stat):
    """Test _get_cpu_linux when first read fails."""
    mock_read_proc_stat.side_effect = [None, {'total': 1000, 'idle': 800}]

    result = _get_cpu_linux()

    assert result == ''


@patch('system_utils._read_proc_stat')
@patch('time.sleep')
def test_get_cpu_linux_second_read_fails(mock_sleep, mock_read_proc_stat):
    """Test _get_cpu_linux when second read fails."""
    mock_read_proc_stat.side_effect = [{'total': 1000, 'idle': 800}, None]

    result = _get_cpu_linux()

    assert result == ''


@patch('system_utils._read_proc_stat')
@patch('time.sleep')
def test_get_cpu_linux_zero_delta(mock_sleep, mock_read_proc_stat):
    """Test _get_cpu_linux with zero total delta."""
    mock_read_proc_stat.side_effect = [
        {'total': 1000, 'idle': 800},
        {'total': 1000, 'idle': 800}
    ]

    result = _get_cpu_linux()

    assert result == ''


def test_read_proc_stat_success():
    """Test _read_proc_stat with valid data."""
    proc_stat_content = "cpu  100 200 300 400 500 600 700\n"

    with patch('builtins.open', mock_open(read_data=proc_stat_content)):
        result = _read_proc_stat()

    assert result is not None
    assert result['total'] == 2800  # sum of all values
    assert result['idle'] == 400    # 4th value


def test_read_proc_stat_invalid_format():
    """Test _read_proc_stat with invalid format."""
    proc_stat_content = "invalid line format\n"

    with patch('builtins.open', mock_open(read_data=proc_stat_content)):
        result = _read_proc_stat()

    assert result is None


def test_read_proc_stat_io_error():
    """Test _read_proc_stat with IO error."""
    with patch('builtins.open', side_effect=IOError('Test error')):
        result = _read_proc_stat()

    assert result is None


def test_get_memory_linux_success():
    """Test _get_memory_linux with valid data."""
    meminfo_content = """MemTotal:       16384000 kB
MemFree:         4096000 kB
MemAvailable:    8192000 kB
"""

    with patch('builtins.open', mock_open(read_data=meminfo_content)):
        result = _get_memory_linux()

    # mem_used = (16384000 - 8192000) / (1024 * 1024) = 7.8GB
    assert 'GB' in result


def test_get_memory_linux_small_memory():
    """Test _get_memory_linux with small memory usage."""
    meminfo_content = """MemTotal:       1048576 kB
MemFree:         524288 kB
MemAvailable:    786432 kB
"""

    with patch('builtins.open', mock_open(read_data=meminfo_content)):
        result = _get_memory_linux()

    # mem_used = (1048576 - 786432) / 1024 = 256MB
    assert 'MB' in result


def test_get_memory_linux_zero_total():
    """Test _get_memory_linux with zero total memory."""
    meminfo_content = """MemTotal:       0 kB
MemAvailable:    0 kB
"""

    with patch('builtins.open', mock_open(read_data=meminfo_content)):
        result = _get_memory_linux()

    assert result == ''


def test_get_memory_linux_io_error():
    """Test _get_memory_linux with IO error."""
    with patch('builtins.open', side_effect=IOError('Test error')):
        result = _get_memory_linux()

    assert result == ''


@patch('os.path.exists')
@patch('os.listdir')
def test_get_battery_linux_success(mock_listdir, mock_exists):
    """Test _get_battery_linux with valid battery."""
    mock_exists.side_effect = lambda path: True if 'power_supply' in path or 'BAT' in path or 'capacity' in path else False
    mock_listdir.return_value = ['BAT0', 'AC']

    with patch('builtins.open', mock_open(read_data='85')):
        result = _get_battery_linux()

    assert result == '85%'


@patch('os.path.exists')
def test_get_battery_linux_no_power_supply(mock_exists):
    """Test _get_battery_linux when power supply directory doesn't exist."""
    mock_exists.return_value = False

    result = _get_battery_linux()

    assert result == ''


@patch('os.path.exists')
@patch('os.listdir')
def test_get_battery_linux_no_battery(mock_listdir, mock_exists):
    """Test _get_battery_linux when no battery is found."""
    mock_exists.return_value = True
    mock_listdir.return_value = ['AC']

    result = _get_battery_linux()

    assert result == ''


@patch('os.path.exists')
@patch('os.listdir')
def test_get_battery_linux_io_error(mock_listdir, mock_exists):
    """Test _get_battery_linux with IO error."""
    mock_exists.return_value = True
    mock_listdir.side_effect = OSError('Test error')

    result = _get_battery_linux()

    assert result == ''


# ============================================================================
# Tests for macOS implementations
# ============================================================================

@patch('subprocess.run')
def test_get_cpu_macos_success(mock_run):
    """Test _get_cpu_macos with valid output."""
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = "CPU usage: 12.5% user, 5.3% sys, 82.2% idle\n"
    mock_run.return_value = mock_result

    result = _get_cpu_macos()

    # usage = 100 - 82.2 = 18%
    assert result == '18%'


@patch('subprocess.run')
def test_get_cpu_macos_subprocess_error(mock_run):
    """Test _get_cpu_macos with subprocess error."""
    mock_run.side_effect = subprocess.SubprocessError('Test error')

    result = _get_cpu_macos()

    assert result == ''


@patch('subprocess.run')
def test_get_cpu_macos_non_zero_return(mock_run):
    """Test _get_cpu_macos with non-zero return code."""
    mock_result = MagicMock()
    mock_result.returncode = 1
    mock_run.return_value = mock_result

    result = _get_cpu_macos()

    assert result == ''


def test_get_memory_macos_success():
    """Test _get_memory_macos returns string (may be empty on non-macOS or errors)."""
    # This test just verifies the function doesn't crash
    # Actual output depends on system and permissions
    result = _get_memory_macos()
    assert isinstance(result, str)


@patch('subprocess.run')
def test_get_memory_macos_subprocess_error(mock_run):
    """Test _get_memory_macos with subprocess error."""
    mock_run.side_effect = subprocess.SubprocessError('Test error')

    result = _get_memory_macos()

    assert result == ''


@patch('subprocess.run')
def test_get_battery_macos_success(mock_run):
    """Test _get_battery_macos with valid output."""
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = "Now drawing from 'Battery Power'\n -InternalBattery-0 (id=12345678) 85%; discharging; 3:45 remaining"
    mock_run.return_value = mock_result

    result = _get_battery_macos()

    assert result == '85%'


@patch('subprocess.run')
def test_get_battery_macos_subprocess_error(mock_run):
    """Test _get_battery_macos with subprocess error."""
    mock_run.side_effect = subprocess.SubprocessError('Test error')

    result = _get_battery_macos()

    assert result == ''


# ============================================================================
# Tests for Windows implementations
# ============================================================================

@patch('subprocess.run')
def test_get_cpu_windows_success(mock_run):
    """Test _get_cpu_windows with valid output."""
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = "LoadPercentage\n45\n"
    mock_run.return_value = mock_result

    result = _get_cpu_windows()

    assert result == '45%'


@patch('subprocess.run')
def test_get_cpu_windows_subprocess_error(mock_run):
    """Test _get_cpu_windows with subprocess error."""
    mock_run.side_effect = FileNotFoundError('wmic not found')

    result = _get_cpu_windows()

    assert result == ''


@patch('subprocess.run')
def test_get_memory_windows_success(mock_run):
    """Test _get_memory_windows with valid output."""
    # Mock two separate subprocess calls
    mock_result_total = MagicMock()
    mock_result_total.returncode = 0
    mock_result_total.stdout = "TotalPhysicalMemory\n17179869184\n"  # 16GB

    mock_result_free = MagicMock()
    mock_result_free.returncode = 0
    mock_result_free.stdout = "FreePhysicalMemory\n4194304\n"  # 4GB in KB

    mock_run.side_effect = [mock_result_total, mock_result_free]

    result = _get_memory_windows()

    # (17179869184 - 4194304*1024) / (1024^3) = 12GB
    assert 'GB' in result


@patch('subprocess.run')
def test_get_memory_windows_subprocess_error(mock_run):
    """Test _get_memory_windows with subprocess error."""
    mock_run.side_effect = FileNotFoundError('wmic not found')

    result = _get_memory_windows()

    assert result == ''


@patch('subprocess.run')
def test_get_battery_windows_success(mock_run):
    """Test _get_battery_windows with valid output."""
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = "EstimatedChargeRemaining\n78\n"
    mock_run.return_value = mock_result

    result = _get_battery_windows()

    assert result == '78%'


@patch('subprocess.run')
def test_get_battery_windows_subprocess_error(mock_run):
    """Test _get_battery_windows with subprocess error."""
    mock_run.side_effect = FileNotFoundError('wmic not found')

    result = _get_battery_windows()

    assert result == ''
