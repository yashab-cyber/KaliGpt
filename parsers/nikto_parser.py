#!/usr/bin/env python3
"""
Nikto Output Parser
Parses Nikto web vulnerability scanner output
"""

import re
from typing import Dict, List, Optional


class NiktoParser:
    """Parse Nikto scan output"""
    
    def __init__(self):
        self.vuln_pattern = re.compile(r'\+\s+(.+)')
        self.osvdb_pattern = re.compile(r'OSVDB-(\d+)')
        self.cve_pattern = re.compile(r'CVE-(\d{4}-\d+)')
        
    def parse(self, output: str, command: str = "") -> Dict:
        """
        Parse Nikto output
        
        Args:
            output: Raw Nikto output
            command: Original command
            
        Returns:
            Structured dict with parsed data
        """
        result = {
            'tool': 'nikto',
            'command': command,
            'target': '',
            'port': 80,
            'server': '',
            'vulnerabilities': [],
            'interesting_findings': [],
            'headers': {},
            'allowed_methods': [],
            'directories': [],
            'files': []
        }
        
        lines = output.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Extract target
            if line.startswith('+ Target IP:') or line.startswith('+ Target Host:'):
                result['target'] = line.split(':', 1)[1].strip()
            
            # Extract port
            if line.startswith('+ Target Port:'):
                try:
                    result['port'] = int(line.split(':', 1)[1].strip())
                except:
                    pass
            
            # Extract server
            if line.startswith('+ Server:'):
                result['server'] = line.split(':', 1)[1].strip()
            
            # Parse vulnerabilities and findings
            if line.startswith('+'):
                finding = self._parse_finding(line)
                if finding:
                    if finding['severity'] in ['high', 'critical']:
                        result['vulnerabilities'].append(finding)
                    else:
                        result['interesting_findings'].append(finding)
                    
                    # Categorize specific items
                    if 'directory' in finding['description'].lower():
                        result['directories'].append(finding['item'])
                    elif any(ext in finding['item'] for ext in ['.php', '.asp', '.jsp', '.cgi']):
                        result['files'].append(finding['item'])
            
            # Extract HTTP methods
            if 'Allowed HTTP Methods:' in line:
                methods = line.split(':', 1)[1].strip()
                result['allowed_methods'] = [m.strip() for m in methods.split(',')]
        
        return result
    
    def _parse_finding(self, line: str) -> Optional[Dict]:
        """Parse a single finding line"""
        if not line.startswith('+'):
            return None
        
        # Remove the leading '+'
        content = line[1:].strip()
        
        finding = {
            'description': content,
            'item': '',
            'severity': 'info',
            'osvdb': [],
            'cve': []
        }
        
        # Extract OSVDB references
        osvdb_matches = self.osvdb_pattern.findall(content)
        if osvdb_matches:
            finding['osvdb'] = osvdb_matches
        
        # Extract CVE references
        cve_matches = self.cve_pattern.findall(content)
        if cve_matches:
            finding['cve'] = [f"CVE-{cve}" for cve in cve_matches]
        
        # Determine severity based on keywords
        severity_keywords = {
            'critical': ['sql injection', 'command injection', 'remote code execution', 'rce'],
            'high': ['authentication bypass', 'directory traversal', 'file inclusion', 'arbitrary file'],
            'medium': ['xss', 'cross-site scripting', 'csrf', 'information disclosure'],
            'low': ['outdated', 'version disclosure', 'banner']
        }
        
        content_lower = content.lower()
        for severity, keywords in severity_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                finding['severity'] = severity
                break
        
        # Extract item/path if present
        if ':' in content:
            parts = content.split(':', 1)
            potential_item = parts[0].strip()
            if potential_item.startswith('/'):
                finding['item'] = potential_item
                finding['description'] = parts[1].strip()
        
        return finding
    
    def get_recommendations(self, parsed_data: Dict) -> List[str]:
        """
        Get recommended next steps
        
        Args:
            parsed_data: Parsed Nikto data
            
        Returns:
            List of recommended commands
        """
        recommendations = []
        target = parsed_data.get('target', 'target')
        port = parsed_data.get('port', 80)
        protocol = 'https' if port == 443 else 'http'
        url = f"{protocol}://{target}:{port}"
        
        # Directory enumeration
        recommendations.append(f"gobuster dir -u {url} -w /usr/share/wordlists/dirb/common.txt")
        recommendations.append(f"ffuf -u {url}/FUZZ -w /usr/share/wordlists/dirb/big.txt")
        
        # If interesting directories found
        for directory in parsed_data.get('directories', [])[:3]:
            recommendations.append(f"curl -v {url}{directory}")
        
        # Check for specific vulnerabilities
        for vuln in parsed_data.get('vulnerabilities', []):
            if 'admin' in vuln['description'].lower():
                recommendations.append(f"hydra -L users.txt -P passwords.txt {target} http-get /admin")
            elif 'sql' in vuln['description'].lower():
                recommendations.append(f"sqlmap -u {url} --batch --level 5")
        
        # If methods like PUT, DELETE are allowed
        dangerous_methods = ['PUT', 'DELETE', 'TRACE']
        if any(method in parsed_data.get('allowed_methods', []) for method in dangerous_methods):
            recommendations.append(f"curl -X PUT -d 'test' {url}/test.txt")
        
        return recommendations


if __name__ == "__main__":
    # Test parser
    test_output = """
- Nikto v2.1.6
---------------------------------------------------------------------------
+ Target IP:          192.168.1.100
+ Target Hostname:    example.com
+ Target Port:        80
+ Start Time:         2024-01-01 12:00:00
---------------------------------------------------------------------------
+ Server: Apache/2.4.18 (Ubuntu)
+ The anti-clickjacking X-Frame-Options header is not present.
+ The X-XSS-Protection header is not defined.
+ The X-Content-Type-Options header is not set.
+ No CGI Directories found (use '-C all' to force check all possible dirs)
+ Server may leak inodes via ETags, header found with file /, inode: 2c3, size: 5a3e
+ Allowed HTTP Methods: GET, HEAD, POST, OPTIONS, DELETE, PUT 
+ OSVDB-397: HTTP method ('Allow' Header): 'PUT' method could allow clients to save files on the web server.
+ OSVDB-5646: HTTP method ('Allow' Header): 'DELETE' may allow clients to remove files on the web server.
+ /admin/: This might be interesting...
+ /config.php: PHP Config file may contain database IDs and passwords.
+ /phpinfo.php: Output from the phpinfo() function was found.
+ OSVDB-3233: /phpinfo.php: PHP is installed, and a test script which runs phpinfo() was found.
+ /admin/index.php: Admin login page/section found.
"""
    
    parser = NiktoParser()
    result = parser.parse(test_output)
    
    print("Parsed Data:")
    print(f"Target: {result['target']}")
    print(f"Server: {result['server']}")
    print(f"Vulnerabilities: {len(result['vulnerabilities'])}")
    print(f"Interesting Findings: {len(result['interesting_findings'])}")
    print(f"Allowed Methods: {result['allowed_methods']}")
    
    print("\nHigh Priority Findings:")
    for vuln in result['vulnerabilities']:
        print(f"  [{vuln['severity'].upper()}] {vuln['description'][:80]}...")
