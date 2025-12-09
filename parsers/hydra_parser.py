#!/usr/bin/env python3
"""
Hydra Output Parser
Parses Hydra password cracking output
"""

import re
from typing import Dict, List, Optional


class HydraParser:
    """Parse Hydra output"""
    
    def __init__(self):
        self.credential_pattern = re.compile(
            r'\[(\d+)\]\[(\w+)\]\s+host:\s*(\S+)\s+login:\s*(\S+)\s+password:\s*(.+)'
        )
        self.status_pattern = re.compile(r'\[STATUS\].*?(\d+\.\d+) tries/min')
        
    def parse(self, output: str, command: str = "") -> Dict:
        """
        Parse Hydra output
        
        Args:
            output: Raw Hydra output
            command: Original command
            
        Returns:
            Structured dict with parsed data
        """
        result = {
            'tool': 'hydra',
            'command': command,
            'service': self._extract_service(command),
            'target': self._extract_target(command),
            'credentials_found': [],
            'attempts': 0,
            'valid_count': 0,
            'status': 'running',
            'speed': 0.0,
            'started': False,
            'completed': False
        }
        
        lines = output.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Check for start
            if 'Starting' in line or 'starting' in line:
                result['started'] = True
            
            # Check for completion
            if line.startswith('[STATUS]') and 'attack finished' in line.lower():
                result['completed'] = True
                result['status'] = 'completed'
            
            # Parse found credentials
            cred_match = self.credential_pattern.search(line)
            if cred_match:
                port = cred_match.group(1)
                protocol = cred_match.group(2)
                host = cred_match.group(3)
                login = cred_match.group(4)
                password = cred_match.group(5)
                
                credential = {
                    'port': port,
                    'protocol': protocol,
                    'host': host,
                    'username': login,
                    'password': password
                }
                
                result['credentials_found'].append(credential)
                result['valid_count'] += 1
            
            # Alternative credential format
            elif '[VALID]' in line or 'valid' in line.lower():
                parts = line.split()
                if len(parts) >= 4:
                    # Try to extract username and password
                    for i, part in enumerate(parts):
                        if 'login:' in part.lower() and i + 1 < len(parts):
                            username = parts[i + 1]
                        elif 'password:' in part.lower() and i + 1 < len(parts):
                            password = ' '.join(parts[i + 1:])
                    
                    if 'username' in locals() and 'password' in locals():
                        result['credentials_found'].append({
                            'username': username,
                            'password': password,
                            'service': result['service']
                        })
            
            # Parse status and speed
            status_match = self.status_pattern.search(line)
            if status_match:
                result['speed'] = float(status_match.group(1))
            
            # Count attempts
            if 'attempt' in line.lower() or 'tried' in line.lower():
                # Try to extract number of attempts
                numbers = re.findall(r'\d+', line)
                if numbers:
                    result['attempts'] = max(result['attempts'], int(numbers[0]))
        
        # Determine final status
        if result['completed']:
            result['status'] = 'success' if result['valid_count'] > 0 else 'failed'
        
        return result
    
    def _extract_service(self, command: str) -> str:
        """Extract target service from command"""
        services = [
            'ftp', 'ssh', 'telnet', 'http', 'https', 'smb', 'smtp',
            'pop3', 'imap', 'rdp', 'mysql', 'postgres', 'vnc',
            'ldap', 'snmp', 'mssql', 'mongodb', 'redis'
        ]
        
        command_lower = command.lower()
        for service in services:
            if service in command_lower:
                return service
        
        return 'unknown'
    
    def _extract_target(self, command: str) -> Optional[str]:
        """Extract target IP/hostname from command"""
        # Look for IP address
        ip_pattern = re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b')
        match = ip_pattern.search(command)
        if match:
            return match.group(0)
        
        # Look for hostname after service name
        parts = command.split()
        for i, part in enumerate(parts):
            if part in ['ssh://', 'ftp://', 'http://', 'https://']:
                if i + 1 < len(parts):
                    return parts[i + 1]
        
        return None
    
    def get_recommendations(self, parsed_data: Dict) -> List[str]:
        """
        Get recommended next steps
        
        Args:
            parsed_data: Parsed Hydra data
            
        Returns:
            List of recommended commands
        """
        recommendations = []
        
        if parsed_data['credentials_found']:
            service = parsed_data['service']
            target = parsed_data['target'] or 'TARGET'
            
            for cred in parsed_data['credentials_found']:
                username = cred.get('username', '')
                password = cred.get('password', '')
                
                # Service-specific recommendations
                if service == 'ssh':
                    recommendations.append(f"ssh {username}@{target}")
                    recommendations.append(f"sshpass -p '{password}' ssh {username}@{target}")
                
                elif service == 'ftp':
                    recommendations.append(f"ftp {target}")
                    recommendations.append(f"# Use credentials: {username}/{password}")
                
                elif service in ['http', 'https']:
                    recommendations.append(f"curl -u {username}:{password} {service}://{target}")
                
                elif service == 'smb':
                    recommendations.append(f"smbclient -U {username}%{password} //{target}/share")
                    recommendations.append(f"crackmapexec smb {target} -u {username} -p '{password}'")
                
                elif service == 'rdp':
                    recommendations.append(f"xfreerdp /u:{username} /p:{password} /v:{target}")
                
                elif service == 'mysql':
                    recommendations.append(f"mysql -h {target} -u {username} -p'{password}'")
        
        else:
            # If no credentials found, suggest alternatives
            recommendations.extend([
                "Try different wordlists",
                "Use -e nsr flags for null/same/reverse password attempts",
                "Check for default credentials",
                "Consider using medusa or ncrack as alternatives"
            ])
        
        return recommendations
    
    def export_credentials(self, parsed_data: Dict, format: str = 'txt') -> str:
        """
        Export credentials in various formats
        
        Args:
            parsed_data: Parsed Hydra data
            format: Output format (txt, json, csv)
            
        Returns:
            Formatted credential string
        """
        credentials = parsed_data.get('credentials_found', [])
        
        if not credentials:
            return "No credentials found"
        
        if format == 'txt':
            lines = []
            for cred in credentials:
                username = cred.get('username', '')
                password = cred.get('password', '')
                service = cred.get('service', cred.get('protocol', ''))
                host = cred.get('host', parsed_data.get('target', ''))
                
                lines.append(f"{host}:{service} - {username}:{password}")
            
            return '\n'.join(lines)
        
        elif format == 'json':
            import json
            return json.dumps(credentials, indent=2)
        
        elif format == 'csv':
            lines = ['host,service,username,password']
            for cred in credentials:
                host = cred.get('host', parsed_data.get('target', ''))
                service = cred.get('service', cred.get('protocol', ''))
                username = cred.get('username', '')
                password = cred.get('password', '')
                
                lines.append(f"{host},{service},{username},{password}")
            
            return '\n'.join(lines)
        
        return "Unsupported format"


if __name__ == "__main__":
    # Test parser
    test_output = """
Hydra v9.1 (c) 2020 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2024-01-01 12:00:00
[DATA] max 16 tasks per 1 server, overall 16 tasks, 14344399 login tries (l:1/p:14344399), ~896525 tries per task
[DATA] attacking ssh://192.168.1.100:22/
[STATUS] 178.00 tries/min, 178 tries in 00:01h, 14344221 to do in 1343:24h, 16 active
[22][ssh] host: 192.168.1.100   login: admin   password: password123
[STATUS] attack finished for 192.168.1.100 (valid pair found)
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2024-01-01 12:05:23
"""
    
    parser = HydraParser()
    result = parser.parse(test_output, "hydra -l admin -P passwords.txt ssh://192.168.1.100")
    
    print("Parsed Data:")
    print(f"Service: {result['service']}")
    print(f"Target: {result['target']}")
    print(f"Status: {result['status']}")
    print(f"Credentials Found: {result['valid_count']}")
    
    if result['credentials_found']:
        print("\nCredentials:")
        for cred in result['credentials_found']:
            print(f"  {cred['username']}:{cred['password']}")
    
    print("\nRecommendations:")
    for cmd in parser.get_recommendations(result)[:5]:
        print(f"  - {cmd}")
