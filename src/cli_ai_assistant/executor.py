"""Command execution utilities."""

import subprocess
import sys
from typing import Optional


def execute_command(command: str, timeout: Optional[int] = None) -> tuple[int, str, str]:
    """
    Execute a shell command and return the result.
    
    Returns:
        Tuple of (return_code, stdout, stderr)
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", f"Command timed out after {timeout} seconds"
    except Exception as e:
        return -1, "", str(e)


def stream_command(command: str) -> int:
    """
    Execute a command with streaming output to stdout/stderr.
    
    Returns:
        The command's return code
    """
    try:
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=sys.stdout,
            stderr=sys.stderr,
        )
        process.wait()
        return process.returncode
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return -1
