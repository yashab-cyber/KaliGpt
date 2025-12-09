#!/usr/bin/env python3
"""
Model Verification Script
Tests all AI model configurations and API connections
"""

import os
import sys
from typing import Dict, List, Tuple

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
except ImportError:
    print("Error: rich library not installed. Run: pip install rich")
    sys.exit(1)


console = Console()


def check_api_keys() -> Dict[str, bool]:
    """Check which API keys are configured"""
    keys = {
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
        'GOOGLE_API_KEY': os.getenv('GOOGLE_API_KEY'),
        'GEMINI_API_KEY': os.getenv('GEMINI_API_KEY'),
        'ANTHROPIC_API_KEY': os.getenv('ANTHROPIC_API_KEY'),
        'CLAUDE_API_KEY': os.getenv('CLAUDE_API_KEY'),
    }
    
    return {k: bool(v) for k, v in keys.items()}


def check_local_models() -> List[str]:
    """Check which local models are available via Ollama"""
    import subprocess
    
    try:
        result = subprocess.run(
            ['ollama', 'list'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            models = [line.split()[0] for line in lines if line.strip()]
            return models
        else:
            return []
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return []


def test_model_import(model_name: str) -> Tuple[bool, str]:
    """Test if a model can be imported"""
    try:
        if model_name == 'gpt':
            from models.gpt import GPTModel
            return True, "✓ GPT model available"
        elif model_name == 'gemini':
            from models.gemini import GeminiModel
            return True, "✓ Gemini model available"
        elif model_name == 'claude':
            from models.anthropic_claude import ClaudeModel
            return True, "✓ Claude model available"
        elif model_name == 'llama':
            from models.local_llama import LocalLlamaModel
            return True, "✓ LLaMA model available"
        elif model_name == 'mistral':
            from models.mistral import MistralModel
            return True, "✓ Mistral model available"
        elif model_name == 'qwen':
            from models.qwen import QwenModel
            return True, "✓ Qwen model available"
        else:
            return False, "Unknown model"
    except ImportError as e:
        return False, f"✗ Import failed: {str(e)}"


def check_dependencies() -> Dict[str, bool]:
    """Check if required dependencies are installed"""
    deps = {}
    
    # Core dependencies
    try:
        import pexpect
        deps['pexpect'] = True
    except ImportError:
        deps['pexpect'] = False
    
    try:
        import requests
        deps['requests'] = True
    except ImportError:
        deps['requests'] = False
    
    try:
        from rich import console
        deps['rich'] = True
    except ImportError:
        deps['rich'] = False
    
    # AI model dependencies
    try:
        import openai
        deps['openai'] = True
    except ImportError:
        deps['openai'] = False
    
    try:
        import google.generativeai
        deps['google-generativeai'] = True
    except ImportError:
        deps['google-generativeai'] = False
    
    try:
        import anthropic
        deps['anthropic'] = True
    except ImportError:
        deps['anthropic'] = False
    
    return deps


def main():
    """Run all verification checks"""
    
    console.print(Panel.fit(
        "[bold cyan]KaliGPT Model Verification[/bold cyan]\n"
        "Checking AI model configurations and dependencies",
        border_style="cyan"
    ))
    console.print()
    
    # Check dependencies
    console.print("[bold yellow]📦 Checking Dependencies...[/bold yellow]")
    deps = check_dependencies()
    
    dep_table = Table(show_header=True, header_style="bold magenta")
    dep_table.add_column("Package", style="cyan")
    dep_table.add_column("Status", justify="center")
    
    for dep, installed in deps.items():
        status = "[green]✓ Installed[/green]" if installed else "[red]✗ Missing[/red]"
        dep_table.add_row(dep, status)
    
    console.print(dep_table)
    console.print()
    
    # Check API keys
    console.print("[bold yellow]🔑 Checking API Keys...[/bold yellow]")
    api_keys = check_api_keys()
    
    key_table = Table(show_header=True, header_style="bold magenta")
    key_table.add_column("API Key", style="cyan")
    key_table.add_column("Status", justify="center")
    key_table.add_column("Enables", style="dim")
    
    key_mapping = {
        'OPENAI_API_KEY': 'GPT-5.1, GPT-5, GPT-4, GPT-3.5',
        'GOOGLE_API_KEY': 'Gemini 3 Pro, Gemini 2.0 Pro',
        'GEMINI_API_KEY': 'Gemini models (alternative)',
        'ANTHROPIC_API_KEY': 'Claude Sonnet 4.5, Opus 4, Sonnet 3.5',
        'CLAUDE_API_KEY': 'Claude models (alternative)',
    }
    
    for key, configured in api_keys.items():
        status = "[green]✓ Set[/green]" if configured else "[dim]○ Not set[/dim]"
        enables = key_mapping.get(key, "")
        key_table.add_row(key, status, enables)
    
    console.print(key_table)
    console.print()
    
    # Check local models
    console.print("[bold yellow]🖥️  Checking Local Models (Ollama)...[/bold yellow]")
    local_models = check_local_models()
    
    if local_models:
        console.print(f"[green]✓ Ollama installed with {len(local_models)} model(s):[/green]")
        for model in local_models:
            console.print(f"  • {model}")
    else:
        console.print("[yellow]⚠ Ollama not installed or no models downloaded[/yellow]")
        console.print("[dim]Install: curl -fsSL https://ollama.com/install.sh | sh[/dim]")
    console.print()
    
    # Check model imports
    console.print("[bold yellow]🤖 Checking Model Implementations...[/bold yellow]")
    model_table = Table(show_header=True, header_style="bold magenta")
    model_table.add_column("Model Type", style="cyan")
    model_table.add_column("Status", justify="center")
    model_table.add_column("Models", style="dim")
    
    models_to_check = [
        ('gpt', 'GPT-5.1, GPT-5, GPT-4, GPT-3.5'),
        ('gemini', 'Gemini 3 Pro, Gemini 2.0 Pro'),
        ('claude', 'Claude Sonnet 4.5, Opus 4, Sonnet 3.5'),
        ('llama', 'LLaMA 2, LLaMA 3'),
        ('mistral', 'Mistral 7B'),
        ('qwen', 'Qwen 7B, 14B'),
    ]
    
    for model_type, model_list in models_to_check:
        success, message = test_model_import(model_type)
        status = "[green]✓ Available[/green]" if success else "[red]✗ Error[/red]"
        model_table.add_row(model_type.upper(), status, model_list)
    
    console.print(model_table)
    console.print()
    
    # Recommendations
    console.print("[bold yellow]💡 Recommendations:[/bold yellow]")
    
    recommendations = []
    
    if not any([api_keys['OPENAI_API_KEY'], api_keys['GOOGLE_API_KEY'], 
                api_keys['ANTHROPIC_API_KEY']]):
        recommendations.append(
            "[yellow]No cloud API keys configured. Using local models only.[/yellow]\n"
            "  To enable cloud models, set one of: OPENAI_API_KEY, GOOGLE_API_KEY, ANTHROPIC_API_KEY"
        )
    
    if not local_models:
        recommendations.append(
            "[yellow]No local models installed. Install Ollama for privacy-focused usage:[/yellow]\n"
            "  curl -fsSL https://ollama.com/install.sh | sh\n"
            "  ollama pull llama3"
        )
    
    if not deps.get('google-generativeai'):
        recommendations.append(
            "[yellow]Google Generative AI library not installed:[/yellow]\n"
            "  pip install google-generativeai"
        )
    
    if not deps.get('anthropic'):
        recommendations.append(
            "[yellow]Anthropic library not installed:[/yellow]\n"
            "  pip install anthropic"
        )
    
    if recommendations:
        for rec in recommendations:
            console.print(f"  • {rec}")
    else:
        console.print("  [green]✓ All recommended configurations are set![/green]")
    
    console.print()
    
    # Summary
    cloud_available = any([api_keys['OPENAI_API_KEY'], api_keys['GOOGLE_API_KEY'], 
                          api_keys['ANTHROPIC_API_KEY']])
    local_available = bool(local_models)
    
    if cloud_available and local_available:
        status_msg = "[bold green]🎉 Perfect! You can use both cloud and local models.[/bold green]"
    elif cloud_available:
        status_msg = "[bold blue]☁️  Cloud models available. Consider installing local models for privacy.[/bold blue]"
    elif local_available:
        status_msg = "[bold blue]🖥️  Local models available. Consider cloud models for advanced features.[/bold blue]"
    else:
        status_msg = "[bold yellow]⚠️  No models configured. Set up API keys or install Ollama.[/bold yellow]"
    
    console.print(Panel(status_msg, border_style="cyan"))
    console.print()
    
    # Available models summary
    console.print("[bold cyan]Available Models:[/bold cyan]")
    available = []
    
    if api_keys['OPENAI_API_KEY']:
        available.append("  • [green]GPT-5.1, GPT-5, GPT-4[/green] (OpenAI)")
    if api_keys['GOOGLE_API_KEY'] or api_keys['GEMINI_API_KEY']:
        available.append("  • [green]Gemini 3 Pro, Gemini 2.0 Pro[/green] (Google)")
    if api_keys['ANTHROPIC_API_KEY'] or api_keys['CLAUDE_API_KEY']:
        available.append("  • [green]Claude Sonnet 4.5, Opus 4, Sonnet 3.5[/green] (Anthropic)")
    if local_models:
        available.append(f"  • [green]{', '.join(local_models)}[/green] (Local/Ollama)")
    
    if available:
        for model in available:
            console.print(model)
    else:
        console.print("  [dim]No models currently available[/dim]")
    
    console.print()
    console.print("[dim]For more information, see: docs/MODELS.md[/dim]")


if __name__ == '__main__':
    main()
