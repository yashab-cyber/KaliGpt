#!/usr/bin/env python3
"""
KaliGPT Terminal Capture Module
Captures terminal output in real-time using pexpect
"""

import pexpect
import sys
import os
import re
from typing import Optional, Callable
from datetime import datetime


class TerminalCapture:
    """
    Captures terminal commands and output in real-time.
    Provides hooks for AI analysis.
    """
    
    def __init__(self, callback: Optional[Callable] = None):
        """
        Initialize terminal capture
        
        Args:
            callback: Function to call with captured output
        """
        self.callback = callback
        self.session_log = []
        self.current_command = None
        self.ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        
    def strip_ansi(self, text: str) -> str:
        """Remove ANSI escape codes from text"""
        return self.ansi_escape.sub('', text)
    
    def log_command(self, command: str, output: str):
        """Log command and output to session"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'command': command,
            'output': output,
            'output_clean': self.strip_ansi(output)
        }
        self.session_log.append(entry)
        
        # Trigger AI analysis callback
        if self.callback:
            self.callback(entry)
    
    def start_interactive_shell(self):
        """
        Start an interactive shell with real-time capture
        """
        shell = os.environ.get('SHELL', '/bin/bash')
        
        try:
            # Spawn shell process
            child = pexpect.spawn(shell, encoding='utf-8', echo=False)
            child.setwinsize(100, 200)
            
            print("[KaliGPT] Interactive shell started. Type 'exit' to quit.")
            print("[KaliGPT] All commands will be analyzed by AI.\n")
            
            while True:
                try:
                    # Send output to terminal
                    child.interact(
                        escape_character=None,
                        input_filter=self._input_filter,
                        output_filter=self._output_filter
                    )
                    break
                except Exception as e:
                    print(f"\n[KaliGPT Error] {e}")
                    break
                    
        except KeyboardInterrupt:
            print("\n[KaliGPT] Session terminated by user.")
        except Exception as e:
            print(f"[KaliGPT Error] {e}")
    
    def _input_filter(self, data):
        """Filter and capture user input"""
        # Store the command being typed
        if data and data.strip():
            self.current_command = data
        return data
    
    def _output_filter(self, data):
        """Filter and capture command output"""
        # This captures the output
        if self.current_command and data:
            self.log_command(self.current_command, data)
        return data
    
    def execute_command(self, command: str, timeout: int = 30) -> dict:
        """
        Execute a single command and capture output
        
        Args:
            command: Command to execute
            timeout: Maximum time to wait for command completion
            
        Returns:
            dict with command, output, exit_code
        """
        try:
            child = pexpect.spawn(
                '/bin/bash',
                ['-c', command],
                encoding='utf-8',
                timeout=timeout
            )
            
            output = child.read()
            child.expect(pexpect.EOF)
            exit_code = child.wait()
            
            result = {
                'command': command,
                'output': output,
                'output_clean': self.strip_ansi(output),
                'exit_code': exit_code,
                'timestamp': datetime.now().isoformat()
            }
            
            self.session_log.append(result)
            
            # Trigger AI analysis
            if self.callback:
                self.callback(result)
            
            return result
            
        except pexpect.TIMEOUT:
            return {
                'command': command,
                'output': 'Command timed out',
                'output_clean': 'Command timed out',
                'exit_code': -1,
                'error': 'timeout'
            }
        except Exception as e:
            return {
                'command': command,
                'output': str(e),
                'output_clean': str(e),
                'exit_code': -1,
                'error': str(e)
            }
    
    def get_session_log(self) -> list:
        """Return full session log"""
        return self.session_log
    
    def save_session(self, filepath: str):
        """Save session log to file"""
        import json
        with open(filepath, 'w') as f:
            json.dump(self.session_log, f, indent=2)
        print(f"[KaliGPT] Session saved to {filepath}")


class SmartTerminal(TerminalCapture):
    """
    Enhanced terminal with command detection and categorization
    """
    
    PENTEST_TOOLS = {
        'nmap': 'reconnaissance',
        'masscan': 'reconnaissance',
        'rustscan': 'reconnaissance',
        'metasploit': 'exploitation',
        'msfconsole': 'exploitation',
        'msfvenom': 'payload_generation',
        'sqlmap': 'exploitation',
        'nikto': 'web_scanning',
        'gobuster': 'enumeration',
        'dirb': 'enumeration',
        'dirbuster': 'enumeration',
        'ffuf': 'enumeration',
        'feroxbuster': 'enumeration',
        'hydra': 'password_attack',
        'john': 'password_cracking',
        'hashcat': 'password_cracking',
        'burpsuite': 'web_testing',
        'wpscan': 'cms_scanning',
        'enum4linux': 'enumeration',
        'smbclient': 'smb_enumeration',
        'crackmapexec': 'lateral_movement',
        'mimikatz': 'credential_dumping',
        'linpeas': 'privilege_escalation',
        'winpeas': 'privilege_escalation',
        'bloodhound': 'active_directory'
    }
    
    def detect_tool(self, command: str) -> Optional[str]:
        """Detect which pentesting tool is being used"""
        cmd_parts = command.lower().split()
        if not cmd_parts:
            return None
        
        tool_name = cmd_parts[0]
        
        # Check if it's a known tool
        for tool, category in self.PENTEST_TOOLS.items():
            if tool in tool_name:
                return tool
        
        return None
    
    def categorize_command(self, command: str) -> str:
        """Categorize the command type"""
        tool = self.detect_tool(command)
        if tool:
            return self.PENTEST_TOOLS.get(tool, 'unknown')
        return 'unknown'


if __name__ == "__main__":
    # Test terminal capture
    def test_callback(entry):
        print(f"\n[AI Analysis Triggered]")
        print(f"Command: {entry['command'][:50]}...")
        print(f"Output length: {len(entry['output_clean'])} chars\n")
    
    terminal = SmartTerminal(callback=test_callback)
    
    # Test single command execution
    result = terminal.execute_command("ls -la")
    print("Command executed:", result['command'])
    print("Exit code:", result['exit_code'])
