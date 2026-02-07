"""Environment detection utilities."""

import os
import shutil
import subprocess
from dataclasses import dataclass


@dataclass
class Environment:
    """Runtime environment context."""
    os_type: str
    shell: str
    cwd: str
    aws_profile: str | None
    k8s_context: str | None
    available_tools: list[str]


def detect_environment() -> Environment:
    """Detect the current runtime environment."""
    import platform
    
    # OS detection
    os_type = platform.system().lower()
    if os_type == "darwin":
        os_type = "macos"
    
    # Shell detection
    shell = os.environ.get("SHELL", "/bin/bash")
    shell = os.path.basename(shell)
    
    # Current directory
    cwd = os.getcwd()
    
    # AWS profile
    aws_profile = os.environ.get("AWS_PROFILE") or os.environ.get("AWS_DEFAULT_PROFILE")
    
    # Kubernetes context
    k8s_context = None
    if shutil.which("kubectl"):
        try:
            result = subprocess.run(
                ["kubectl", "config", "current-context"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0:
                k8s_context = result.stdout.strip()
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
    
    # Available tools
    tools_to_check = ["aws", "kubectl", "docker", "git", "terraform", "helm", "gcloud", "az"]
    available_tools = [tool for tool in tools_to_check if shutil.which(tool)]
    
    return Environment(
        os_type=os_type,
        shell=shell,
        cwd=cwd,
        aws_profile=aws_profile,
        k8s_context=k8s_context,
        available_tools=available_tools,
    )
