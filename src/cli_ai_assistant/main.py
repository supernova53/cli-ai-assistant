"""Main CLI entry point."""

import sys
import click
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

from .environment import detect_environment
from .executor import stream_command
from .prompts import is_dangerous_command
from .providers import get_provider


console = Console()


@click.command()
@click.argument("request", nargs=-1, required=True)
@click.option("-y", "--yes", is_flag=True, help="Execute without confirmation")
@click.option("--dry", is_flag=True, help="Show command only, don't execute")
@click.option("--provider", "-p", type=str, help="AI provider (openai, anthropic)")
@click.option("--copy", "-c", is_flag=True, help="Copy command to clipboard")
@click.version_option(package_name="cli-ai-assistant")
def cli(request: tuple[str, ...], yes: bool, dry: bool, provider: str, copy: bool):
    """
    Translate natural language into shell commands.
    
    Examples:
    
        ai list all s3 buckets
        
        ai "show running docker containers"
        
        ai -y get pods in production namespace
        
        ai --dry delete all stopped containers
    """
    request_str = " ".join(request)
    
    if not request_str.strip():
        console.print("[red]Error:[/red] Please provide a request")
        sys.exit(1)
    
    try:
        # Detect environment
        env = detect_environment()
        
        # Get AI provider
        ai_provider = get_provider(provider)
        
        # Generate command
        with console.status("[bold blue]Thinking..."):
            command = ai_provider.generate_command(request_str, env)
        
        # Clean up command (remove markdown code blocks if present)
        command = clean_command(command)
        
        # Display the command
        console.print()
        syntax = Syntax(command, "bash", theme="monokai", word_wrap=True)
        console.print(Panel(syntax, title="[bold green]Command", border_style="green"))
        
        # Check for dangerous commands
        is_dangerous = is_dangerous_command(command)
        if is_dangerous:
            console.print("[bold yellow]⚠️  Warning:[/bold yellow] This command may be destructive!")
        
        # Copy to clipboard if requested
        if copy:
            try:
                import subprocess
                subprocess.run(["pbcopy"], input=command.encode(), check=True)
                console.print("[dim]✓ Copied to clipboard[/dim]")
            except Exception:
                # Try xclip for Linux
                try:
                    subprocess.run(["xclip", "-selection", "clipboard"], input=command.encode(), check=True)
                    console.print("[dim]✓ Copied to clipboard[/dim]")
                except Exception:
                    console.print("[dim]Could not copy to clipboard[/dim]")
        
        # Dry run - just show the command
        if dry:
            sys.exit(0)
        
        # Execute or prompt
        if yes and not is_dangerous:
            console.print()
            return_code = stream_command(command)
            sys.exit(return_code)
        else:
            prompt = "[bold red]Execute? (dangerous)[/bold red]" if is_dangerous else "Execute?"
            console.print()
            if click.confirm(prompt, default=not is_dangerous):
                console.print()
                return_code = stream_command(command)
                sys.exit(return_code)
            else:
                console.print("[dim]Cancelled[/dim]")
                sys.exit(0)
                
    except ValueError as e:
        console.print(f"[red]Configuration Error:[/red] {e}")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


def clean_command(command: str) -> str:
    """Remove markdown formatting from command."""
    command = command.strip()
    
    # Remove markdown code blocks
    if command.startswith("```"):
        lines = command.split("\n")
        # Remove first line (```bash or ```)
        lines = lines[1:]
        # Remove last line if it's just ```
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        command = "\n".join(lines)
    
    # Remove inline code backticks
    if command.startswith("`") and command.endswith("`"):
        command = command[1:-1]
    
    return command.strip()


if __name__ == "__main__":
    cli()
