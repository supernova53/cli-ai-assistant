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


def get_provider(provider_name: Optional[str] = None) -> AIProvider:
    """Get an AI provider, auto-detecting based on available API keys."""
    if provider_name:
        if provider_name.lower() == "openai":
            return OpenAIProvider()
        elif provider_name.lower() in ("anthropic", "claude"):
            return AnthropicProvider()
        else:
            raise ValueError(f"Unknown provider: {provider_name}")
    
    # Auto-detect based on available API keys
    if os.environ.get("ANTHROPIC_API_KEY"):
        return AnthropicProvider()
    elif os.environ.get("OPENAI_API_KEY"):
        return OpenAIProvider()
    else:
        raise ValueError(
            "No API key found. Set either ANTHROPIC_API_KEY or OPENAI_API_KEY environment variable."
        )
