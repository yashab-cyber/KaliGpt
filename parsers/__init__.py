#!/usr/bin/env python3
"""
Parser Manager
Central manager for all tool parsers
"""

from typing import Dict, Optional, Type
from .nmap_parser import NmapParser
from .msf_parser import MetasploitParser
from .sqlmap_parser import SQLmapParser
from .nikto_parser import NiktoParser
from .gobuster_parser import GobusterParser
from .hydra_parser import HydraParser


class ParserManager:
    """
    Manages all tool parsers and routes output to appropriate parser
    """
    
    def __init__(self):
        self.parsers = {
            'nmap': NmapParser(),
            'metasploit': MetasploitParser(),
            'msfconsole': MetasploitParser(),
            'sqlmap': SQLmapParser(),
            'nikto': NiktoParser(),
            'gobuster': GobusterParser(),
            'hydra': HydraParser(),
            'dirb': GobusterParser(),  # Similar enough
            'dirbuster': GobusterParser(),
            'ffuf': GobusterParser(),
        }
    
    def detect_tool(self, command: str) -> Optional[str]:
        """
        Detect which tool was used based on command
        
        Args:
            command: The command string
            
        Returns:
            Tool name or None
        """
        command_lower = command.lower().strip()
        
        # Get the first word (usually the tool name)
        first_word = command_lower.split()[0] if command_lower else ''
        
        # Direct matches
        for tool_name in self.parsers.keys():
            if first_word == tool_name or first_word.endswith(tool_name):
                return tool_name
        
        # Special cases
        if 'msfconsole' in command_lower or 'metasploit' in command_lower:
            return 'metasploit'
        
        return None
    
    def parse(self, command: str, output: str) -> Dict:
        """
        Parse command output using appropriate parser
        
        Args:
            command: The command that was executed
            output: The output from the command
            
        Returns:
            Parsed data dictionary
        """
        tool = self.detect_tool(command)
        
        if tool and tool in self.parsers:
            parser = self.parsers[tool]
            return parser.parse(output, command)
        
        # Return generic structure if no parser found
        return {
            'tool': 'unknown',
            'command': command,
            'output': output,
            'parsed': False
        }
    
    def get_parser(self, tool_name: str):
        """
        Get a specific parser
        
        Args:
            tool_name: Name of the tool
            
        Returns:
            Parser instance or None
        """
        return self.parsers.get(tool_name.lower())
    
    def get_recommendations(self, parsed_data: Dict) -> list:
        """
        Get recommendations based on parsed data
        
        Args:
            parsed_data: Parsed data from a tool
            
        Returns:
            List of recommended next steps
        """
        tool = parsed_data.get('tool', 'unknown')
        
        if tool in self.parsers:
            parser = self.parsers[tool]
            if hasattr(parser, 'get_recommendations'):
                return parser.get_recommendations(parsed_data)
        
        return []


__all__ = [
    'ParserManager',
    'NmapParser',
    'MetasploitParser',
    'SQLmapParser',
    'NiktoParser',
    'GobusterParser',
    'HydraParser'
]
