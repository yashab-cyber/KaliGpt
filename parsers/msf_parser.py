#!/usr/bin/env python3
"""
Metasploit Output Parser
Parses Metasploit console output and extracts structured data
"""

import re
from typing import Dict, List, Optional
from datetime import datetime


class MetasploitParser:
    """Parse Metasploit/msfconsole output"""
    
    def __init__(self):
        self.session_pattern = re.compile(r'Session (\d+) opened')
        self.exploit_success_pattern = re.compile(r'\[\*\]\s+Sending stage')
        self.exploit_fail_pattern = re.compile(r'\[-\]\s+Exploit failed')
        self.meterpreter_pattern = re.compile(r'meterpreter >')
        
    def parse(self, output: str, command: str = "") -> Dict:
        """
        Parse Metasploit output
        
        Args:
            output: Raw Metasploit output
            command: Original command executed
            
        Returns:
            Structured dict with parsed data
        """
        result = {
            'tool': 'metasploit',
            'command': command,
            'session_opened': False,
            'session_id': None,
            'exploit_success': False,
            'exploit_failed': False,
            'meterpreter_shell': False,
            'messages': [],
            'errors': [],
            'module': self._extract_module(command),
            'target': self._extract_target(output)
        }
        
        lines = output.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Check for session opened
            session_match = self.session_pattern.search(line)
            if session_match:
                result['session_opened'] = True
                result['session_id'] = int(session_match.group(1))
                result['exploit_success'] = True
                result['messages'].append(f"Session {session_match.group(1)} opened successfully")
            
            # Check for exploit success
            if self.exploit_success_pattern.search(line):
                result['exploit_success'] = True
                result['messages'].append("Exploit payload staged successfully")
            
            # Check for exploit failure
            if self.exploit_fail_pattern.search(line):
                result['exploit_failed'] = True
                result['errors'].append(line)
            
            # Check for meterpreter shell
            if self.meterpreter_pattern.search(line):
                result['meterpreter_shell'] = True
            
            # Capture important messages
            if line.startswith('[*]'):
                result['messages'].append(line)
            elif line.startswith('[+]'):
                result['messages'].append(line)
            elif line.startswith('[-]'):
                result['errors'].append(line)
            elif line.startswith('[!]'):
                result['errors'].append(line)
        
        # Determine overall status
        result['status'] = self._determine_status(result)
        
        return result
    
    def parse_module_info(self, output: str) -> Dict:
        """
        Parse module info output
        
        Args:
            output: Output from 'info' command
            
        Returns:
            Module information
        """
        info = {
            'name': '',
            'description': '',
            'authors': [],
            'references': [],
            'platform': '',
            'targets': [],
            'options': []
        }
        
        lines = output.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            
            if 'Name:' in line:
                info['name'] = line.split('Name:')[1].strip()
            elif 'Description:' in line:
                current_section = 'description'
                info['description'] = line.split('Description:')[1].strip()
            elif line.startswith('Author:') or line.startswith('Authors:'):
                current_section = 'authors'
            elif 'Platform:' in line:
                info['platform'] = line.split('Platform:')[1].strip()
            elif current_section == 'authors' and line:
                info['authors'].append(line)
        
        return info
    
    def parse_search_results(self, output: str) -> List[Dict]:
        """
        Parse module search results
        
        Args:
            output: Output from 'search' command
            
        Returns:
            List of modules
        """
        modules = []
        lines = output.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Skip headers and empty lines
            if not line or line.startswith('=') or line.startswith('Matching'):
                continue
            
            # Parse module line
            parts = line.split()
            if len(parts) >= 2 and ('exploit' in parts[0] or 'auxiliary' in parts[0]):
                modules.append({
                    'path': parts[0],
                    'disclosure_date': parts[1] if len(parts) > 1 else '',
                    'rank': parts[2] if len(parts) > 2 else '',
                    'name': ' '.join(parts[3:]) if len(parts) > 3 else ''
                })
        
        return modules
    
    def _extract_module(self, command: str) -> Optional[str]:
        """Extract module name from command"""
        patterns = [
            r'use\s+(exploit/[^\s]+)',
            r'use\s+(auxiliary/[^\s]+)',
            r'use\s+(payload/[^\s]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, command)
            if match:
                return match.group(1)
        
        return None
    
    def _extract_target(self, output: str) -> Optional[str]:
        """Extract target IP from output"""
        patterns = [
            r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d+)',
            r'RHOST\s*=>\s*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, output)
            if match:
                return match.group(1)
        
        return None
    
    def _determine_status(self, result: Dict) -> str:
        """Determine overall exploit status"""
        if result['exploit_failed']:
            return 'failed'
        elif result['session_opened']:
            return 'success_session'
        elif result['exploit_success']:
            return 'success'
        else:
            return 'unknown'
    
    def get_recommendations(self, parsed_data: Dict) -> List[str]:
        """
        Get recommended next steps
        
        Args:
            parsed_data: Parsed Metasploit data
            
        Returns:
            List of recommended commands
        """
        recommendations = []
        
        if parsed_data['exploit_success'] and parsed_data['session_opened']:
            # Post-exploitation recommendations
            recommendations.extend([
                "getuid",
                "sysinfo",
                "ps",
                "shell",
                "hashdump",
                "run post/multi/recon/local_exploit_suggester",
                "run post/windows/gather/enum_applications",
                "run post/windows/gather/credentials/credential_collector"
            ])
        
        elif parsed_data['exploit_failed']:
            # Try alternative exploits
            recommendations.extend([
                "search {target_service}",
                "show options",
                "set payload different_payload",
                "exploit -j"
            ])
        
        return recommendations
    
    def extract_credentials(self, output: str) -> List[Dict]:
        """
        Extract credentials from output (e.g., hashdump)
        
        Args:
            output: Command output
            
        Returns:
            List of credentials
        """
        credentials = []
        lines = output.split('\n')
        
        for line in lines:
            # NTLM hash format: username:rid:lm_hash:ntlm_hash:::
            if ':::' in line:
                parts = line.split(':')
                if len(parts) >= 4:
                    credentials.append({
                        'username': parts[0],
                        'rid': parts[1] if len(parts) > 1 else '',
                        'lm_hash': parts[2] if len(parts) > 2 else '',
                        'ntlm_hash': parts[3] if len(parts) > 3 else '',
                        'type': 'ntlm'
                    })
        
        return credentials
    
    def extract_system_info(self, output: str) -> Dict:
        """
        Extract system information from sysinfo output
        
        Args:
            output: sysinfo command output
            
        Returns:
            System information dict
        """
        info = {
            'computer': '',
            'os': '',
            'architecture': '',
            'domain': '',
            'logged_on_users': ''
        }
        
        patterns = {
            'computer': r'Computer\s*:\s*(.+)',
            'os': r'OS\s*:\s*(.+)',
            'architecture': r'Architecture\s*:\s*(.+)',
            'domain': r'Domain\s*:\s*(.+)',
            'logged_on_users': r'Logged On Users\s*:\s*(.+)'
        }
        
        for key, pattern in patterns.items():
            match = re.search(pattern, output, re.IGNORECASE)
            if match:
                info[key] = match.group(1).strip()
        
        return info


if __name__ == "__main__":
    # Test parser
    test_output = """
[*] Started reverse TCP handler on 192.168.1.5:4444 
[*] 192.168.1.10:445 - Connecting to target for exploitation.
[*] 192.168.1.10:445 - Connection established for exploitation.
[*] 192.168.1.10:445 - Target OS selected valid for OS indicated by SMB reply
[*] 192.168.1.10:445 - CORE raw buffer dump (42 bytes)
[*] 192.168.1.10:445 - Sending stage (175174 bytes) to 192.168.1.10
[*] Meterpreter session 1 opened (192.168.1.5:4444 -> 192.168.1.10:49158)

meterpreter >
"""
    
    parser = MetasploitParser()
    result = parser.parse(test_output)
    
    print("Parsed Data:")
    print(f"Exploit Success: {result['exploit_success']}")
    print(f"Session Opened: {result['session_opened']}")
    print(f"Session ID: {result['session_id']}")
    print(f"Status: {result['status']}")
    
    print("\nRecommendations:")
    for cmd in parser.get_recommendations(result):
        print(f"  - {cmd}")
