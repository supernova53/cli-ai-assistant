"""AI providers for command generation."""

import os
from abc import ABC, abstractmethod
from typing import Optional

from .environment import Environment
from .prompts import SYSTEM_PROMPT


class AIProvider(ABC):
    """Base class for AI providers."""
    
    @abstractmethod
    def generate_command(self, request: str, env: Environment) -> str:
        """Generate a shell command from natural language."""
        pass


class OpenAIProvider(AIProvider):
    """OpenAI provider using GPT models."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
        self.model = model
    
    def generate_command(self, request: str, env: Environment) -> str:
        """Generate command using OpenAI."""
        from openai import OpenAI
        
        client = OpenAI(api_key=self.api_key)
        
        prompt = SYSTEM_PROMPT.format(
            os_type=env.os_type,
            shell=env.shell,
            cwd=env.cwd,
            aws_profile=env.aws_profile or "not set",
            k8s_context=env.k8s_context or "not set",
            request=request,
        )
        
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.1,
        )
        
        return response.choices[0].message.content.strip()


class AnthropicProvider(AIProvider):
    """Anthropic provider using Claude models."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-5-sonnet-20241022"):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("Anthropic API key not found. Set ANTHROPIC_API_KEY environment variable.")
        self.model = model
    
    def generate_command(self, request: str, env: Environment) -> str:
        """Generate command using Anthropic."""
        import anthropic
        
        client = anthropic.Anthropic(api_key=self.api_key)
        
        prompt = SYSTEM_PROMPT.format(
            os_type=env.os_type,
            shell=env.shell,
            cwd=env.cwd,
            aws_profile=env.aws_profile or "not set",
            k8s_context=env.k8s_context or "not set",
            request=request,
        )
        
        response = client.messages.create(
            model=self.model,
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}],
        )
        
        return response.content[0].text.strip()


class MinimaxProvider(AIProvider):
    """Minimax provider using OpenAI-compatible API."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "MiniMax-M2.1"):
        self.api_key = api_key or os.environ.get("MINIMAX_API_KEY")
        if not self.api_key:
            raise ValueError("Minimax API key not found. Set MINIMAX_API_KEY environment variable.")
        self.model = model
        self.base_url = "https://api.minimax.io/v1"
    
    def generate_command(self, request: str, env: Environment) -> str:
        """Generate command using Minimax."""
        from openai import OpenAI
        
        client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        
        prompt = SYSTEM_PROMPT.format(
            os_type=env.os_type,
            shell=env.shell,
            cwd=env.cwd,
            aws_profile=env.aws_profile or "not set",
            k8s_context=env.k8s_context or "not set",
            request=request,
        )
        
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.1,
        )
        
        return response.choices[0].message.content.strip()


class QwenProvider(AIProvider):
    """Qwen provider using OpenAI-compatible API."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "qwen-coder-plus"):
        self.api_key = api_key or os.environ.get("QWEN_API_KEY")
        if not self.api_key:
            raise ValueError("Qwen API key not found. Set QWEN_API_KEY environment variable.")
        self.model = model
        self.base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    
    def generate_command(self, request: str, env: Environment) -> str:
        """Generate command using Qwen."""
        from openai import OpenAI
        
        client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        
        prompt = SYSTEM_PROMPT.format(
            os_type=env.os_type,
            shell=env.shell,
            cwd=env.cwd,
            aws_profile=env.aws_profile or "not set",
            k8s_context=env.k8s_context or "not set",
            request=request,
        )
        
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.1,
        )
        
        return response.choices[0].message.content.strip()


class AmpCodeProvider(AIProvider):
    """AmpCode local provider using OpenAI-compatible API."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-2.5-flash"):
        self.api_key = api_key or os.environ.get("AMPCODE_API_KEY", "your-api-key-1")
        self.model = model
        self.base_url = os.environ.get("AMPCODE_BASE_URL", "http://127.0.0.1:8317/v1")
    
    def generate_command(self, request: str, env: Environment) -> str:
        """Generate command using AmpCode."""
        from openai import OpenAI
        
        client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        
        prompt = SYSTEM_PROMPT.format(
            os_type=env.os_type,
            shell=env.shell,
            cwd=env.cwd,
            aws_profile=env.aws_profile or "not set",
            k8s_context=env.k8s_context or "not set",
            request=request,
        )
        
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.1,
        )
        
        return response.choices[0].message.content.strip()


def get_provider(provider_name: Optional[str] = None) -> AIProvider:
    """Get an AI provider, auto-detecting based on available API keys."""
    if provider_name:
        provider_lower = provider_name.lower()
        if provider_lower == "openai":
            return OpenAIProvider()
        elif provider_lower in ("anthropic", "claude"):
            return AnthropicProvider()
        elif provider_lower == "minimax":
            return MinimaxProvider()
        elif provider_lower == "qwen":
            return QwenProvider()
        elif provider_lower == "ampcode":
            return AmpCodeProvider()
        else:
            raise ValueError(f"Unknown provider: {provider_name}")
    
    # Auto-detect based on available API keys or local services
    # Try AmpCode first (local, fast, free)
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex(('127.0.0.1', 8317))
        sock.close()
        if result == 0:
            return AmpCodeProvider()
    except Exception:
        pass
    
    if os.environ.get("ANTHROPIC_API_KEY"):
        return AnthropicProvider()
    elif os.environ.get("OPENAI_API_KEY"):
        return OpenAIProvider()
    elif os.environ.get("MINIMAX_API_KEY"):
        return MinimaxProvider()
    elif os.environ.get("QWEN_API_KEY"):
        return QwenProvider()
    else:
        raise ValueError(
            "No API key found. Set ANTHROPIC_API_KEY, OPENAI_API_KEY, MINIMAX_API_KEY, or QWEN_API_KEY."
        )
