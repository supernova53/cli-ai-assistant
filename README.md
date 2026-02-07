# CLI AI Assistant

A natural language CLI assistant that translates plain English into shell commands for AWS, kubectl, Docker, Git, and more.

## Features

- 🗣️ **Natural Language to Commands**: Describe what you want in plain English
- 🔍 **Preview Before Execute**: See the command before running it
- 🛡️ **Safety First**: Dangerous commands require explicit confirmation
- 🎯 **Context-Aware**: Learns your environment (AWS profile, k8s context, etc.)
- 📚 **Multi-Tool Support**: AWS CLI, kubectl, Docker, Git, and general shell commands

## Installation

```bash
# Install with pip
pip install cli-ai-assistant

# Or install from source
git clone https://github.com/supernova53/cli-ai-assistant.git
cd cli-ai-assistant
pip install -e .
```

## Configuration

Set your API key (supports OpenAI and Anthropic):

```bash
# Using OpenAI
export OPENAI_API_KEY="your-key-here"

# Or using Anthropic
export ANTHROPIC_API_KEY="your-key-here"
```

Optionally create a `.env` file in your home directory or project root.

## Usage

```bash
# Basic usage
ai "list all s3 buckets"
ai "get pods in the production namespace"
ai "show running docker containers"
ai "check git status and show recent commits"

# Execute immediately (skip confirmation)
ai -y "list ec2 instances in us-east-1"

# Dry run (show command only)
ai --dry "delete all stopped containers"

# Specify provider
ai --provider anthropic "scale deployment nginx to 3 replicas"
```

## Examples

```bash
$ ai "find large files over 100MB in current directory"
Command: find . -type f -size +100M -exec ls -lh {} \;
Execute? [y/N]: y

$ ai "show me memory usage of top 5 processes"
Command: ps aux --sort=-%mem | head -6
Execute? [y/N]: y

$ ai "create a new git branch called feature/auth"
Command: git checkout -b feature/auth
Execute? [y/N]: y

$ ai "list all lambda functions in us-west-2"
Command: aws lambda list-functions --region us-west-2 --query 'Functions[].FunctionName' --output table
Execute? [y/N]: y
```

## Safety

The assistant will warn and require explicit confirmation for:
- Destructive operations (`rm -rf`, `DROP TABLE`, etc.)
- Privileged commands (`sudo`, etc.)
- Cloud resource deletion
- Force operations (`--force`, `-f` in dangerous contexts)

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black src/
ruff check src/ --fix
```

## License

MIT License - see [LICENSE](LICENSE) for details.
