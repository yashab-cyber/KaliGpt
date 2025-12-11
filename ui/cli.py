#!/usr/bin/env python3
"""
KaliGPT CLI Interface
Main command-line interface for KaliGPT
"""

import sys
import os
import argparse
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import print as rprint
from rich.prompt import Prompt, Confirm
from rich.progress import Progress
from rich.markdown import Markdown

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.terminal_capture import SmartTerminal
from core.ai_engine import AIEngine, ContextManager
from core.decision_engine import DecisionEngine
from core.executor import InteractiveExecutor
from parsers import ParserManager
from payloads.generator import PayloadGenerator
from reporting.report_builder import ReportBuilder
from models.model_selector import ModelSelector

console = Console()


class KaliGPT:
    """
    Main KaliGPT application class
    """
    
    def __init__(self, model_type: str = "llama", auto_execute: bool = False):
        """
        Initialize KaliGPT
        
        Args:
            model_type: LLM model to use
            auto_execute: Auto-execute recommended commands
        """
        self.model_type = model_type
        self.auto_execute = auto_execute
        
        # Initialize components
        console.print("[bold cyan]Initializing KaliGPT...[/bold cyan]")
        
        try:
            self.ai_engine = AIEngine(model_type=model_type)
            self.decision_engine = DecisionEngine()
            self.context_manager = ContextManager()
            self.parser_manager = ParserManager()
            self.payload_generator = PayloadGenerator()
            self.executor = InteractiveExecutor(auto_execute=auto_execute, safe_mode=True)
            self.report_builder = ReportBuilder()
            
            console.print("[bold green]✓ Initialization complete![/bold green]\n")
        except Exception as e:
            console.print(f"[bold red]✗ Initialization failed: {e}[/bold red]")
            sys.exit(1)
    
    def show_banner(self):
        """Display KaliGPT banner"""
        banner = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   ██╗  ██╗ █████╗ ██╗     ██╗ ██████╗ ██████╗ ████████╗  ║
║   ██║ ██╔╝██╔══██╗██║     ██║██╔════╝ ██╔══██╗╚══██╔══╝  ║
║   █████╔╝ ███████║██║     ██║██║  ███╗██████╔╝   ██║     ║
║   ██╔═██╗ ██╔══██║██║     ██║██║   ██║██╔═══╝    ██║     ║
║   ██║  ██╗██║  ██║███████╗██║╚██████╔╝██║        ██║     ║
║   ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝ ╚═════╝ ╚═╝        ╚═╝     ║
║                                                           ║
║        AI-Powered Penetration Testing Assistant          ║
║                   for Kali Linux                          ║
║                                                           ║
║              Created by Yashab Alam                       ║
║    Instagram: @yashab.alam | LinkedIn: yashab-alam       ║
║         💎 Support: yashabalam9@gmail.com                ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""
        console.print(f"[bold cyan]{banner}[/bold cyan]")
        console.print(f"[yellow]Model:[/yellow] {self.model_type}")
        console.print(f"[yellow]Mode:[/yellow] {'Auto-Execute' if self.auto_execute else 'Interactive'}\n")
    
    def interactive_mode(self):
        """Run in interactive mode"""
        self.show_banner()
        
        console.print("[bold green]Welcome to KaliGPT Interactive Mode![/bold green]")
        console.print("Type 'help' for commands, 'exit' to quit.\n")
        
        while True:
            try:
                user_input = Prompt.ask("[bold cyan]KaliGPT[/bold cyan]")
                
                if not user_input:
                    continue
                
                # Handle special commands
                if user_input.lower() in ['exit', 'quit', 'q']:
                    if Confirm.ask("Save session before exiting?"):
                        self.save_session()
                    console.print("[yellow]Goodbye![/yellow]")
                    break
                
                elif user_input.lower() == 'help':
                    self.show_help()
                
                elif user_input.lower() == 'status':
                    self.show_status()
                
                elif user_input.lower() == 'report':
                    self.generate_report()
                
                elif user_input.lower().startswith('target '):
                    target = user_input.split(' ', 1)[1]
                    self.set_target(target)
                
                elif user_input.lower().startswith('payload '):
                    payload_type = user_input.split(' ', 1)[1]
                    self.generate_payload(payload_type)
                
                elif user_input.lower().startswith('run '):
                    command = user_input.split(' ', 1)[1]
                    self.run_command(command)
                
                else:
                    # Treat as a question for AI
                    self.ask_ai(user_input)
            
            except KeyboardInterrupt:
                console.print("\n[yellow]Use 'exit' to quit[/yellow]")
                continue
            except EOFError:
                break
    
    def run_command(self, command: str):
        """Execute a command and analyze results"""
        console.print(f"\n[bold]Executing:[/bold] {command}\n")
        
        # Execute command
        result = self.executor.execute_with_preview(command, "User-requested command")
        
        if not result['success']:
            console.print(f"[red]Command failed: {result.get('error', 'Unknown error')}[/red]")
            return
        
        # Parse output
        parsed = self.parser_manager.parse(command, result['output'])
        
        # Get AI analysis
        tool_type = self.parser_manager.detect_tool(command)
        
        with console.status("[cyan]AI analyzing results...[/cyan]"):
            ai_analysis = self.ai_engine.analyze_output(
                command, 
                result['output'], 
                tool_type
            )
        
        # Get decision engine recommendations
        if tool_type:
            decisions = self.decision_engine.analyze_and_decide(parsed, tool_type)
            
            # Update context
            self._update_context_from_parsed(parsed)
        
        # Display AI analysis
        self._display_analysis(ai_analysis)
    
    def ask_ai(self, question: str):
        """Ask AI a question"""
        with console.status("[cyan]AI thinking...[/cyan]"):
            context = self.context_manager.get_context()
            
            prompt = f"""User question: {question}

Current context:
{context}

Provide a helpful answer focused on penetration testing."""
            
            response = self.ai_engine.model.generate(prompt, self.ai_engine.conversation_history)
        
        console.print("\n[bold cyan]AI Response:[/bold cyan]")
        console.print(Panel(Markdown(response), border_style="cyan"))
        console.print()
    
    def generate_payload(self, payload_type: str):
        """Generate a payload"""
        console.print(f"\n[bold]Generating {payload_type} payload...[/bold]\n")
        
        payloads = self.payload_generator.generate(payload_type)
        
        if isinstance(payloads, dict):
            table = Table(title=f"{payload_type.upper()} Payloads")
            table.add_column("Name", style="cyan")
            table.add_column("Payload", style="green")
            
            for name, payload in list(payloads.items())[:10]:
                table.add_row(name, payload[:80] + "..." if len(payload) > 80 else payload)
            
            console.print(table)
        else:
            console.print(Panel(payloads, title="Generated Payload", border_style="green"))
        
        console.print()
    
    def set_target(self, target: str):
        """Set target IP/hostname"""
        self.context_manager.update_target(target)
        console.print(f"[green]✓ Target set to: {target}[/green]\n")
    
    def show_status(self):
        """Show current status"""
        context = self.context_manager.get_context()
        
        console.print("\n[bold cyan]Current Status[/bold cyan]\n")
        
        # Target info
        target = context.get('target', {})
        console.print(f"[yellow]Target:[/yellow] {target.get('ip', 'Not set')}")
        console.print(f"[yellow]Phase:[/yellow] {context.get('phase', 'reconnaissance').title()}")
        
        # Statistics
        console.print(f"\n[yellow]Discovered Services:[/yellow] {len(context.get('services', []))}")
        console.print(f"[yellow]Vulnerabilities:[/yellow] {len(context.get('vulnerabilities', []))}")
        console.print(f"[yellow]Exploits Attempted:[/yellow] {len(context.get('exploits', []))}")
        
        console.print()
    
    def generate_report(self):
        """Generate penetration testing report"""
        console.print("\n[bold cyan]Generating Report...[/bold cyan]\n")
        
        format_choice = Prompt.ask(
            "Report format",
            choices=["markdown", "html", "json", "all"],
            default="markdown"
        )
        
        session_data = {
            "context": self.context_manager.get_context(),
            "commands": self.executor.get_execution_log(),
            "start_time": "Session start"  # Add proper timestamp tracking
        }
        
        if format_choice == "all":
            formats = ["markdown", "html", "json"]
        else:
            formats = [format_choice]
        
        for fmt in formats:
            with console.status(f"[cyan]Generating {fmt.upper()} report...[/cyan]"):
                report_path = self.report_builder.build_report(session_data, format=fmt)
            console.print(f"[green]✓ {fmt.upper()} report saved: {report_path}[/green]")
        
        console.print()
    
    def save_session(self):
        """Save current session"""
        timestamp = __import__('datetime').datetime.now().strftime("%Y%m%d_%H%M%S")
        session_file = f"session_{timestamp}.json"
        
        self.context_manager.save_context(session_file)
        console.print(f"[green]✓ Session saved: {session_file}[/green]")
    
    def show_help(self):
        """Show help information"""
        help_text = """
[bold cyan]KaliGPT Commands:[/bold cyan]

[yellow]General:[/yellow]
  help                 - Show this help message
  exit / quit          - Exit KaliGPT
  status               - Show current session status
  report               - Generate penetration testing report

[yellow]Targeting:[/yellow]
  target <IP>          - Set target IP/hostname

[yellow]Execution:[/yellow]
  run <command>        - Execute a command and analyze results

[yellow]Payloads:[/yellow]
  payload <type>       - Generate payload (sqli, xss, lfi, rce, etc.)

[yellow]AI Interaction:[/yellow]
  <question>           - Ask AI anything about pentesting

[bold]Examples:[/bold]
  target 192.168.1.100
  run nmap -sV 192.168.1.100
  payload sqli
  What is SQL injection?
"""
        console.print(Panel(help_text, title="Help", border_style="cyan"))
    
    def _display_analysis(self, analysis: dict):
        """Display AI analysis results"""
        console.print("\n[bold cyan]═══ AI Analysis ═══[/bold cyan]\n")
        
        if analysis.get('analysis'):
            console.print(f"[yellow]Analysis:[/yellow] {analysis['analysis']}")
        
        if analysis.get('recommendation'):
            console.print(f"\n[yellow]Recommendation:[/yellow] {analysis['recommendation']}")
        
        if analysis.get('command'):
            console.print(f"\n[yellow]Suggested Command:[/yellow]")
            console.print(Panel(analysis['command'], border_style="green"))
            
            if Confirm.ask("Execute this command?"):
                self.run_command(analysis['command'])
        
        if analysis.get('explanation'):
            console.print(f"\n[yellow]Explanation:[/yellow] {analysis['explanation']}")
        
        console.print()
    
    def _update_context_from_parsed(self, parsed: dict):
        """Update context from parsed data"""
        tool = parsed.get('tool')
        
        if tool == 'nmap':
            for port_info in parsed.get('open_ports', []):
                self.context_manager.add_service(
                    port_info['port'],
                    port_info['service'],
                    port_info.get('version')
                )
            
            for vuln in parsed.get('vulnerabilities', []):
                self.context_manager.add_vulnerability(vuln)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="KaliGPT - AI-Powered Penetration Testing Assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '-m', '--model',
        default='llama',
        choices=['gpt', 'llama', 'mistral', 'qwen'],
        help='LLM model to use (default: llama)'
    )
    
    parser.add_argument(
        '-a', '--auto',
        action='store_true',
        help='Auto-execute recommended commands (dangerous!)'
    )
    
    parser.add_argument(
        '-c', '--command',
        help='Execute a single command and exit'
    )
    
    parser.add_argument(
        '--list-models',
        action='store_true',
        help='List available models'
    )
    
    args = parser.parse_args()
    
    # List models
    if args.list_models:
        console.print("\n[bold cyan]Available Models:[/bold cyan]\n")
        models = ModelSelector.list_available_models()
        for model, desc in models.items():
            console.print(f"[yellow]{model:12}[/yellow] - {desc}")
        console.print()
        return
    
    # Initialize KaliGPT
    try:
        app = KaliGPT(model_type=args.model, auto_execute=args.auto)
    except Exception as e:
        console.print(f"[bold red]Failed to initialize KaliGPT: {e}[/bold red]")
        return 1
    
    # Single command mode
    if args.command:
        app.run_command(args.command)
        return 0
    
    # Interactive mode
    app.interactive_mode()
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
