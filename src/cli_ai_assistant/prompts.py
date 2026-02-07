"""Command generation prompts and templates."""

SYSTEM_PROMPT = """You are a CLI command generator. Your job is to translate natural language requests into shell commands.

RULES:
1. Output ONLY the command - no explanations, no markdown, no code blocks
2. Use the most common/standard tool for the job
3. Prefer safe, non-destructive operations when possible
4. For cloud commands (AWS, GCP, Azure), use the standard CLI tools
5. For Kubernetes, use kubectl
6. For Docker, use docker or docker-compose as appropriate
7. For Git, use standard git commands
8. Include helpful flags like --output table, -o wide, --format when they improve readability

CONTEXT:
- Operating System: {os_type}
- Shell: {shell}
- Current Directory: {cwd}
- AWS Profile (if set): {aws_profile}
- Kubernetes Context (if set): {k8s_context}

USER REQUEST: {request}

OUTPUT: Just the command, nothing else."""


DANGEROUS_PATTERNS = [
    # Destructive file operations
    "rm -rf",
    "rm -r",
    "rmdir",
    "del /s",
    # Database operations
    "DROP TABLE",
    "DROP DATABASE",
    "DELETE FROM",
    "TRUNCATE",
    # Cloud destructive operations
    "aws .* delete",
    "aws .* terminate",
    "aws .* remove",
    "kubectl delete",
    "docker rm",
    "docker rmi",
    "docker system prune",
    "docker volume rm",
    # Force flags in dangerous contexts
    "--force",
    "-f ",  # with space to avoid false positives
    # Privilege escalation
    "sudo rm",
    "sudo dd",
    "chmod 777",
    "chown -R",
    # Git destructive
    "git reset --hard",
    "git push --force",
    "git clean -fd",
]


def is_dangerous_command(command: str) -> bool:
    """Check if a command matches known dangerous patterns."""
    import re
    command_lower = command.lower()
    
    for pattern in DANGEROUS_PATTERNS:
        if pattern.lower() in command_lower:
            return True
        # Check regex patterns
        try:
            if re.search(pattern, command, re.IGNORECASE):
                return True
        except re.error:
            pass
    
    return False
