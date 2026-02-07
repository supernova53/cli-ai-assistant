"""Tests for CLI AI Assistant."""

import pytest
from cli_ai_assistant.prompts import is_dangerous_command
from cli_ai_assistant.environment import detect_environment
from cli_ai_assistant.main import clean_command


class TestDangerousCommands:
    """Tests for dangerous command detection."""
    
    def test_rm_rf_is_dangerous(self):
        assert is_dangerous_command("rm -rf /tmp/test")
    
    def test_kubectl_delete_is_dangerous(self):
        assert is_dangerous_command("kubectl delete pod nginx")
    
    def test_docker_rm_is_dangerous(self):
        assert is_dangerous_command("docker rm -f container123")
    
    def test_git_force_push_is_dangerous(self):
        assert is_dangerous_command("git push --force origin main")
    
    def test_drop_table_is_dangerous(self):
        assert is_dangerous_command("psql -c 'DROP TABLE users'")
    
    def test_ls_is_not_dangerous(self):
        assert not is_dangerous_command("ls -la")
    
    def test_kubectl_get_is_not_dangerous(self):
        assert not is_dangerous_command("kubectl get pods")
    
    def test_docker_ps_is_not_dangerous(self):
        assert not is_dangerous_command("docker ps")
    
    def test_aws_list_is_not_dangerous(self):
        assert not is_dangerous_command("aws s3 ls")


class TestEnvironment:
    """Tests for environment detection."""
    
    def test_environment_detection(self):
        env = detect_environment()
        assert env.os_type in ("linux", "macos", "windows")
        assert env.shell is not None
        assert env.cwd is not None


class TestCleanCommand:
    """Tests for command cleaning."""
    
    def test_clean_markdown_code_block(self):
        command = "```bash\nls -la\n```"
        assert clean_command(command) == "ls -la"
    
    def test_clean_inline_backticks(self):
        command = "`ls -la`"
        assert clean_command(command) == "ls -la"
    
    def test_clean_plain_command(self):
        command = "ls -la"
        assert clean_command(command) == "ls -la"
    
    def test_clean_multiline_code_block(self):
        command = "```bash\naws s3 ls\naws s3 cp file.txt s3://bucket/\n```"
        expected = "aws s3 ls\naws s3 cp file.txt s3://bucket/"
        assert clean_command(command) == expected
