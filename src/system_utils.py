"""
System utilities for the Claude Code Statusline Tool.

Provides cross-platform system monitoring functions for CPU, memory,
and battery status. Uses only stdlib with graceful degradation.
"""

import os
import platform
import subprocess
from typing import Optional


def get_cpu_usage() -> str:
    """
    Get current CPU usage percentage.

    Returns:
        CPU usage string (e.g., "45%") or empty string if unavailable
    """
    system = platform.system()

    try:
        if system == "Linux":
            return _get_cpu_linux()
        elif system == "Darwin":  # macOS
            return _get_cpu_macos()
        elif system == "Windows":
            return _get_cpu_windows()
    except (OSError, subprocess.SubprocessError, ValueError):
        pass

    return ""


def get_memory_usage() -> str:
    """
    Get current memory usage.

    Returns:
        Memory usage string (e.g., "8.5GB" or "65%") or empty string if unavailable
    """
    system = platform.system()

    try:
        if system == "Linux":
            return _get_memory_linux()
        elif system == "Darwin":  # macOS
            return _get_memory_macos()
        elif system == "Windows":
            return _get_memory_windows()
    except (OSError, subprocess.SubprocessError, ValueError):
        pass

    return ""


def get_battery_status() -> str:
    """
    Get current battery status.

    Returns:
        Battery percentage string (e.g., "85%") or empty string if unavailable
    """
    system = platform.system()

    try:
        if system == "Linux":
            return _get_battery_linux()
        elif system == "Darwin":  # macOS
            return _get_battery_macos()
        elif system == "Windows":
            return _get_battery_windows()
    except (OSError, subprocess.SubprocessError, ValueError):
        pass

    return ""


# ============================================================================
# Linux Implementations
# ============================================================================

def _get_cpu_linux() -> str:
    """Get CPU usage on Linux by reading /proc/stat."""
    # Read CPU stats twice with a small interval
    stat1 = _read_proc_stat()
    if not stat1:
        return ""

    import time
    time.sleep(0.1)  # Small delay for measurement

    stat2 = _read_proc_stat()
    if not stat2:
        return ""

    # Calculate CPU usage from delta
    total_delta = stat2['total'] - stat1['total']
    idle_delta = stat2['idle'] - stat1['idle']

    if total_delta == 0:
        return ""

    usage = 100.0 * (1.0 - idle_delta / total_delta)
    return f"{usage:.0f}%"


def _read_proc_stat() -> Optional[dict]:
    """Read /proc/stat and return CPU time values."""
    try:
        with open('/proc/stat', 'r') as f:
            line = f.readline()
            if not line.startswith('cpu '):
                return None

            values = [int(x) for x in line.split()[1:]]
            # CPU times: user, nice, system, idle, iowait, irq, softirq, ...
            total = sum(values)
            idle = values[3] if len(values) > 3 else 0

            return {'total': total, 'idle': idle}
    except (IOError, ValueError, IndexError):
        return None


def _get_memory_linux() -> str:
    """Get memory usage on Linux by reading /proc/meminfo."""
    try:
        meminfo = {}
        with open('/proc/meminfo', 'r') as f:
            for line in f:
                parts = line.split()
                if len(parts) >= 2:
                    key = parts[0].rstrip(':')
                    value = int(parts[1])  # Value in KB
                    meminfo[key] = value

        mem_total = meminfo.get('MemTotal', 0)
        mem_available = meminfo.get('MemAvailable', 0)

        if mem_total == 0:
            return ""

        mem_used_kb = mem_total - mem_available
        mem_used_gb = mem_used_kb / (1024 * 1024)

        if mem_used_gb < 1:
            return f"{mem_used_kb / 1024:.0f}MB"
        else:
            return f"{mem_used_gb:.1f}GB"
    except (IOError, ValueError, KeyError):
        return ""


def _get_battery_linux() -> str:
    """Get battery status on Linux by reading /sys/class/power_supply/."""
    try:
        # Look for battery in common locations
        power_supply_dir = '/sys/class/power_supply'
        if not os.path.exists(power_supply_dir):
            return ""

        for entry in os.listdir(power_supply_dir):
            if entry.startswith('BAT'):
                battery_path = os.path.join(power_supply_dir, entry)
                capacity_file = os.path.join(battery_path, 'capacity')

                if os.path.exists(capacity_file):
                    with open(capacity_file, 'r') as f:
                        capacity = int(f.read().strip())
                        return f"{capacity}%"
    except (IOError, ValueError, OSError):
        pass

    return ""


# ============================================================================
# macOS Implementations
# ============================================================================

def _get_cpu_macos() -> str:
    """Get CPU usage on macOS using top command."""
    try:
        result = subprocess.run(
            ['top', '-l', '1', '-n', '0'],
            capture_output=True,
            text=True,
            timeout=1.0
        )
        if result.returncode == 0:
            # Parse CPU line: "CPU usage: 12.34% user, 5.67% sys, 82.0% idle"
            for line in result.stdout.split('\n'):
                if 'CPU usage' in line:
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if part == 'idle' and i > 0:
                            idle_str = parts[i - 1].rstrip('%,')
                            idle = float(idle_str)
                            usage = 100.0 - idle
                            return f"{usage:.0f}%"
    except (subprocess.SubprocessError, ValueError, IndexError):
        pass

    return ""


def _get_memory_macos() -> str:
    """Get memory usage on macOS using vm_stat command."""
    try:
        result = subprocess.run(
            ['vm_stat'],
            capture_output=True,
            text=True,
            timeout=1.0
        )
        if result.returncode == 0:
            # Parse vm_stat output
            page_size = 4096  # Default page size on macOS
            mem_used_pages = 0

            for line in result.stdout.split('\n'):
                if 'page size' in line:
                    # Extract page size
                    parts = line.split()
                    if len(parts) >= 3:
                        page_size = int(parts[2])
                elif 'Pages active' in line or 'Pages wired' in line:
                    # Count active and wired pages as used
                    parts = line.split()
                    if len(parts) >= 2:
                        pages = int(parts[-1].rstrip('.'))
                        mem_used_pages += pages

            mem_used_bytes = mem_used_pages * page_size
            mem_used_gb = mem_used_bytes / (1024 ** 3)

            if mem_used_gb < 1:
                return f"{mem_used_bytes / (1024 ** 2):.0f}MB"
            else:
                return f"{mem_used_gb:.1f}GB"
    except (subprocess.SubprocessError, ValueError, IndexError):
        pass

    return ""


def _get_battery_macos() -> str:
    """Get battery status on macOS using pmset command."""
    try:
        result = subprocess.run(
            ['pmset', '-g', 'batt'],
            capture_output=True,
            text=True,
            timeout=1.0
        )
        if result.returncode == 0:
            # Parse output like: "Now drawing from 'Battery Power' -InternalBattery-0 (id=12345678) 85%; discharging; 3:45 remaining"
            for line in result.stdout.split('\n'):
                if 'InternalBattery' in line or '%' in line:
                    # Extract percentage
                    parts = line.split()
                    for part in parts:
                        if part.endswith('%;') or part.endswith('%'):
                            percentage = part.rstrip('%;')
                            return f"{percentage}%"
    except (subprocess.SubprocessError, ValueError):
        pass

    return ""


# ============================================================================
# Windows Implementations
# ============================================================================

def _get_cpu_windows() -> str:
    """Get CPU usage on Windows using wmic command."""
    try:
        result = subprocess.run(
            ['wmic', 'cpu', 'get', 'loadpercentage'],
            capture_output=True,
            text=True,
            timeout=2.0
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            if len(lines) >= 2:
                usage = int(lines[1].strip())
                return f"{usage}%"
    except (subprocess.SubprocessError, ValueError, FileNotFoundError):
        pass

    return ""


def _get_memory_windows() -> str:
    """Get memory usage on Windows using wmic command."""
    try:
        # Get total physical memory
        result_total = subprocess.run(
            ['wmic', 'ComputerSystem', 'get', 'TotalPhysicalMemory'],
            capture_output=True,
            text=True,
            timeout=2.0
        )
        # Get available memory
        result_free = subprocess.run(
            ['wmic', 'OS', 'get', 'FreePhysicalMemory'],
            capture_output=True,
            text=True,
            timeout=2.0
        )

        if result_total.returncode == 0 and result_free.returncode == 0:
            total_lines = result_total.stdout.strip().split('\n')
            free_lines = result_free.stdout.strip().split('\n')

            if len(total_lines) >= 2 and len(free_lines) >= 2:
                total_bytes = int(total_lines[1].strip())
                free_kb = int(free_lines[1].strip())
                free_bytes = free_kb * 1024

                used_bytes = total_bytes - free_bytes
                used_gb = used_bytes / (1024 ** 3)

                if used_gb < 1:
                    return f"{used_bytes / (1024 ** 2):.0f}MB"
                else:
                    return f"{used_gb:.1f}GB"
    except (subprocess.SubprocessError, ValueError, FileNotFoundError):
        pass

    return ""


def _get_battery_windows() -> str:
    """Get battery status on Windows using wmic command."""
    try:
        result = subprocess.run(
            ['wmic', 'path', 'win32_battery', 'get', 'estimatedchargeremaining'],
            capture_output=True,
            text=True,
            timeout=2.0
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            if len(lines) >= 2:
                percentage = int(lines[1].strip())
                return f"{percentage}%"
    except (subprocess.SubprocessError, ValueError, FileNotFoundError):
        pass

    return ""
