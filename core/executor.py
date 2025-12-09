#!/usr/bin/env python3
"""
KaliGPT Command Executor
Executes commands with user approval and safety checks
"""

import subprocess
import os
import sys
from typing import Optional, Dict, List
from datetime import datetime
import shlex


class CommandExecutor:
    """
    Safely executes commands with user approval
    """
    
    def __init__(self, auto_execute: bool = False, safe_mode: bool = True):
        """
        Initialize executor
        
        Args:
            auto_execute: If True, execute without asking (dangerous!)
            safe_mode: If True, block potentially dangerous commands
        """
        self.auto_execute = auto_execute
        self.safe_mode = safe_mode
        self.execution_log = []
        self.dangerous_commands = [
            'rm -rf /',
            'mkfs',
            'dd if=/dev/zero',
            ':(){:|:&};:',  # Fork bomb
            'chmod -R 777 /',
        ]
        
    def execute(self, command: str, explanation: str = "", timeout: int = 300) -> Dict:
        """
        Execute a command with safety checks
        
        Args:
            command: Command to execute
            explanation: Explanation of what the command does
            timeout: Maximum execution time in seconds
            
        Returns:
            Dict with execution results
        """
        # Safety check
        if self.safe_mode and self._is_dangerous(command):
            return {
                'success': False,
                'command': command,
                'error': 'Command blocked by safety filter',
                'output': '',
                'blocked': True
            }
        
        # Get user approval if not auto-executing
        if not self.auto_execute:
            if not self._get_user_approval(command, explanation):
                return {
                    'success': False,
                    'command': command,
                    'error': 'User declined execution',
                    'output': '',
                    'declined': True
                }
        
        # Execute the command
        result = self._run_command(command, timeout)
        
        # Log execution
        self._log_execution(command, result, explanation)
        
        return result
    
    def execute_chain(self, commands: List[Dict], stop_on_error: bool = True) -> List[Dict]:
        """
        Execute multiple commands in sequence
        
        Args:
            commands: List of dicts with 'command' and optional 'explanation'
            stop_on_error: Stop if a command fails
            
        Returns:
            List of execution results
        """
        results = []
        
        for cmd_info in commands:
            command = cmd_info.get('command', '')
            explanation = cmd_info.get('explanation', '')
            
            if not command:
                continue
            
            result = self.execute(command, explanation)
            results.append(result)
            
            if stop_on_error and not result.get('success', False):
                print(f"\n[!] Command failed, stopping chain execution")
                break
        
        return results
    
    def _is_dangerous(self, command: str) -> bool:
        """Check if command is potentially dangerous"""
        # Check against known dangerous commands
        for dangerous in self.dangerous_commands:
            if dangerous in command:
                return True
        
        # Check for other patterns
        dangerous_patterns = [
            'rm -rf /',
            'rm -rf /*',
            '> /dev/sda',
            'dd if=/dev/zero of=/dev/sda',
        ]
        
        for pattern in dangerous_patterns:
            if pattern in command:
                return True
        
        return False
    
    def _get_user_approval(self, command: str, explanation: str) -> bool:
        """Ask user for approval to execute command"""
        print("\n" + "="*70)
        print("[KaliGPT] Command Ready for Execution")
        print("="*70)
        
        if explanation:
            print(f"\n📋 Explanation: {explanation}")
        
        print(f"\n💻 Command: {command}")
        print("\n" + "="*70)
        
        while True:
            response = input("\nExecute this command? [y/n/e(dit)]: ").lower().strip()
            
            if response == 'y':
                return True
            elif response == 'n':
                return False
            elif response == 'e':
                edited = input(f"Enter modified command [{command}]: ").strip()
                if edited:
                    command = edited
                    print(f"\n✏️  Modified command: {command}")
                continue
            else:
                print("Invalid input. Please enter y, n, or e.")
    
    def _run_command(self, command: str, timeout: int) -> Dict:
        """Actually run the command"""
        start_time = datetime.now()
        
        try:
            # Use shell=True for complex commands with pipes, redirects, etc.
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            return {
                'success': result.returncode == 0,
                'command': command,
                'output': result.stdout,
                'error': result.stderr,
                'return_code': result.returncode,
                'duration': duration,
                'timestamp': start_time.isoformat()
            }
            
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'command': command,
                'output': '',
                'error': f'Command timed out after {timeout} seconds',
                'return_code': -1,
                'timeout': True,
                'timestamp': start_time.isoformat()
            }
        except Exception as e:
            return {
                'success': False,
                'command': command,
                'output': '',
                'error': str(e),
                'return_code': -1,
                'exception': True,
                'timestamp': start_time.isoformat()
            }
    
    def _log_execution(self, command: str, result: Dict, explanation: str):
        """Log command execution"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'command': command,
            'explanation': explanation,
            'success': result.get('success', False),
            'output_length': len(result.get('output', '')),
            'return_code': result.get('return_code', -1)
        }
        self.execution_log.append(log_entry)
    
    def get_execution_log(self) -> List[Dict]:
        """Get execution log"""
        return self.execution_log
    
    def save_execution_log(self, filepath: str):
        """Save execution log to file"""
        import json
        with open(filepath, 'w') as f:
            json.dump(self.execution_log, f, indent=2)
        print(f"[KaliGPT] Execution log saved to {filepath}")
    
    def enable_auto_execute(self, confirm: bool = False):
        """Enable auto-execution mode"""
        if confirm:
            self.auto_execute = True
            print("[!] WARNING: Auto-execution enabled. Commands will run without confirmation!")
        else:
            print("[!] Auto-execution requires confirmation. Pass confirm=True")
    
    def disable_auto_execute(self):
        """Disable auto-execution mode"""
        self.auto_execute = False
        print("[✓] Auto-execution disabled. User confirmation required.")
    
    def toggle_safe_mode(self):
        """Toggle safe mode"""
        self.safe_mode = not self.safe_mode
        status = "enabled" if self.safe_mode else "disabled"
        print(f"[✓] Safe mode {status}")


class InteractiveExecutor(CommandExecutor):
    """
    Enhanced executor with interactive features
    """
    
    def execute_with_preview(self, command: str, explanation: str = "") -> Dict:
        """
        Execute command with live preview of output
        """
        if not self._get_user_approval(command, explanation):
            return {
                'success': False,
                'command': command,
                'error': 'User declined execution',
                'declined': True
            }
        
        print(f"\n[▶] Executing: {command}")
        print("="*70 + "\n")
        
        try:
            # Stream output in real-time
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            
            output_lines = []
            error_lines = []
            
            # Read stdout
            for line in process.stdout:
                print(line, end='')
                output_lines.append(line)
            
            # Wait for completion
            process.wait()
            
            # Read stderr
            stderr_content = process.stderr.read()
            if stderr_content:
                print(f"\n[stderr]\n{stderr_content}", file=sys.stderr)
                error_lines.append(stderr_content)
            
            print("\n" + "="*70)
            
            result = {
                'success': process.returncode == 0,
                'command': command,
                'output': ''.join(output_lines),
                'error': ''.join(error_lines),
                'return_code': process.returncode,
                'timestamp': datetime.now().isoformat()
            }
            
            self._log_execution(command, result, explanation)
            return result
            
        except Exception as e:
            return {
                'success': False,
                'command': command,
                'output': '',
                'error': str(e),
                'exception': True
            }


if __name__ == "__main__":
    # Test executor
    executor = CommandExecutor(auto_execute=False, safe_mode=True)
    
    # Test with a safe command
    result = executor.execute("ls -la", "List files in current directory")
    
    if result['success']:
        print("\n[✓] Command executed successfully")
        print(f"Output length: {len(result['output'])} bytes")
    else:
        print(f"\n[✗] Command failed: {result.get('error', 'Unknown error')}")
