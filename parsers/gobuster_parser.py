#!/usr/bin/env python3
"""
Gobuster Output Parser
Parses Gobuster directory/file enumeration output
"""

import re
from typing import Dict, List, Optional


class GobusterParser:
    """Parse Gobuster output"""
    
    def __init__(self):
        self.found_pattern = re.compile(r'(/\S+)\s+\(Status:\s*(\d+)\)\s*\[Size:\s*(\d+)\]')
        self.redirect_pattern = re.compile(r'\[--> (.+?)\]')
        
    def parse(self, output: str, command: str = "") -> Dict:
        """
        Parse Gobuster output
        
        Args:
            output: Raw Gobuster output
            command: Original command
            
        Returns:
            Structured dict with parsed data
        """
        result = {
            'tool': 'gobuster',
            'command': command,
            'mode': self._detect_mode(command),
            'target_url': self._extract_url(command),
            'found_paths': [],
            'interesting_paths': [],
            'status_codes': {},
            'total_found': 0
        }
        
        lines = output.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Parse found paths
            match = self.found_pattern.search(line)
            if match:
                path = match.group(1)
                status_code = int(match.group(2))
                size = int(match.group(3))
                
                # Check for redirect
                redirect = None
                redirect_match = self.redirect_pattern.search(line)
                if redirect_match:
                    redirect = redirect_match.group(1)
                
                path_info = {
                    'path': path,
                    'url': result['target_url'] + path if result['target_url'] else path,
                    'status_code': status_code,
                    'size': size,
                    'redirect': redirect
                }
                
                result['found_paths'].append(path_info)
                
                # Count status codes
                if status_code not in result['status_codes']:
                    result['status_codes'][status_code] = 0
                result['status_codes'][status_code] += 1
                
                # Identify interesting paths
                if self._is_interesting(path, status_code):
                    result['interesting_paths'].append(path_info)
        
        result['total_found'] = len(result['found_paths'])
        
        return result
    
    def _detect_mode(self, command: str) -> str:
        """Detect Gobuster mode from command"""
        if 'dir' in command:
            return 'directory'
        elif 'dns' in command:
            return 'dns'
        elif 'vhost' in command:
            return 'vhost'
        elif 's3' in command:
            return 's3'
        return 'unknown'
    
    def _extract_url(self, command: str) -> Optional[str]:
        """Extract target URL from command"""
        url_pattern = re.compile(r'-u\s+(https?://[^\s]+)')
        match = url_pattern.search(command)
        if match:
            url = match.group(1)
            # Remove trailing slash
            return url.rstrip('/')
        return None
    
    def _is_interesting(self, path: str, status_code: int) -> bool:
        """Determine if a path is interesting"""
        
        # Status codes that are interesting
        interesting_codes = [200, 201, 204, 301, 302, 307, 401, 403]
        
        if status_code not in interesting_codes:
            return False
        
        # Keywords that make paths interesting
        interesting_keywords = [
            'admin', 'login', 'dashboard', 'panel', 'upload', 'backup',
            'config', 'api', 'test', 'dev', 'staging', 'private',
            'secret', 'hidden', '.git', '.svn', '.env', 'phpinfo',
            'console', 'management', 'wp-admin', 'phpmyadmin',
            'database', 'db', 'sql', 'dumps', 'logs'
        ]
        
        path_lower = path.lower()
        return any(keyword in path_lower for keyword in interesting_keywords)
    
    def parse_dns_mode(self, output: str) -> List[str]:
        """
        Parse DNS/subdomain enumeration mode
        
        Args:
            output: Gobuster DNS mode output
            
        Returns:
            List of found subdomains
        """
        subdomains = []
        lines = output.split('\n')
        
        for line in lines:
            # Format: Found: subdomain.example.com
            if line.startswith('Found:'):
                subdomain = line.split('Found:')[1].strip()
                subdomains.append(subdomain)
        
        return subdomains
    
    def parse_vhost_mode(self, output: str) -> List[Dict]:
        """
        Parse virtual host enumeration mode
        
        Args:
            output: Gobuster vhost mode output
            
        Returns:
            List of found vhosts
        """
        vhosts = []
        lines = output.split('\n')
        
        for line in lines:
            if 'Found:' in line:
                # Extract vhost and status
                parts = line.split()
                if len(parts) >= 3:
                    vhost = parts[1]
                    status = parts[3] if len(parts) > 3 else 'unknown'
                    vhosts.append({
                        'vhost': vhost,
                        'status': status
                    })
        
        return vhosts
    
    def get_recommendations(self, parsed_data: Dict) -> List[str]:
        """
        Get recommended next steps
        
        Args:
            parsed_data: Parsed Gobuster data
            
        Returns:
            List of recommended commands
        """
        recommendations = []
        base_url = parsed_data.get('target_url', 'http://target')
        
        # Investigate interesting paths
        for path_info in parsed_data.get('interesting_paths', [])[:5]:
            path = path_info['path']
            status = path_info['status_code']
            
            if status == 401:
                recommendations.append(f"hydra -L users.txt -P passwords.txt {base_url}{path} http-get")
            elif status in [200, 201]:
                recommendations.append(f"curl -v {base_url}{path}")
                recommendations.append(f"nikto -h {base_url}{path}")
            elif '/upload' in path.lower():
                recommendations.append(f"Test file upload at {base_url}{path}")
            elif any(x in path.lower() for x in ['/api', '/rest']):
                recommendations.append(f"ffuf -u {base_url}{path}/FUZZ -w /usr/share/wordlists/api-endpoints.txt")
        
        # Deeper enumeration on found directories
        for path_info in [p for p in parsed_data.get('found_paths', []) if p['status_code'] in [200, 301, 302]][:3]:
            path = path_info['path']
            if path.endswith('/'):
                recommendations.append(f"gobuster dir -u {base_url}{path} -w /usr/share/wordlists/dirb/big.txt")
        
        # If we found admin/login pages
        admin_paths = [p for p in parsed_data.get('found_paths', []) 
                       if any(x in p['path'].lower() for x in ['admin', 'login'])]
        
        if admin_paths:
            recommendations.append(f"wpscan --url {base_url} --enumerate u,vp")
        
        return recommendations
    
    def categorize_findings(self, parsed_data: Dict) -> Dict[str, List]:
        """
        Categorize findings by type
        
        Args:
            parsed_data: Parsed Gobuster data
            
        Returns:
            Dict with categorized findings
        """
        categories = {
            'admin_panels': [],
            'api_endpoints': [],
            'backup_files': [],
            'config_files': [],
            'upload_points': [],
            'sensitive_info': [],
            'other': []
        }
        
        for path_info in parsed_data.get('found_paths', []):
            path = path_info['path'].lower()
            
            if any(x in path for x in ['admin', 'administrator', 'manage', 'panel']):
                categories['admin_panels'].append(path_info)
            elif any(x in path for x in ['api', 'rest', 'graphql', 'v1', 'v2']):
                categories['api_endpoints'].append(path_info)
            elif any(x in path for x in ['backup', '.bak', '.old', '.sql', '.zip', '.tar']):
                categories['backup_files'].append(path_info)
            elif any(x in path for x in ['config', '.env', 'settings', 'web.config']):
                categories['config_files'].append(path_info)
            elif 'upload' in path:
                categories['upload_points'].append(path_info)
            elif any(x in path for x in ['.git', '.svn', 'phpinfo', 'test', 'debug']):
                categories['sensitive_info'].append(path_info)
            else:
                categories['other'].append(path_info)
        
        return categories


if __name__ == "__main__":
    # Test parser
    test_output = """
===============================================================
Gobuster v3.1.0
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.1.100
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/common.txt
[+] Status codes:            200,204,301,302,307,401,403
===============================================================
2024/01/01 12:00:00 Starting gobuster in directory enumeration mode
===============================================================
/.hta                 (Status: 403) [Size: 277]
/.htaccess            (Status: 403) [Size: 277]
/.htpasswd            (Status: 403) [Size: 277]
/admin                (Status: 301) [Size: 312] [--> http://192.168.1.100/admin/]
/backup               (Status: 200) [Size: 1234]
/config.php           (Status: 200) [Size: 567]
/images               (Status: 301) [Size: 313] [--> http://192.168.1.100/images/]
/index.php            (Status: 200) [Size: 4567]
/login                (Status: 200) [Size: 2345]
/uploads              (Status: 301) [Size: 314] [--> http://192.168.1.100/uploads/]
===============================================================
2024/01/01 12:05:00 Finished
===============================================================
"""
    
    parser = GobusterParser()
    result = parser.parse(test_output, "gobuster dir -u http://192.168.1.100 -w /usr/share/wordlists/dirb/common.txt")
    
    print("Parsed Data:")
    print(f"Total Found: {result['total_found']}")
    print(f"Interesting Paths: {len(result['interesting_paths'])}")
    
    print("\nInteresting Findings:")
    for path in result['interesting_paths']:
        print(f"  {path['status_code']} - {path['path']}")
    
    print("\nRecommendations:")
    for cmd in parser.get_recommendations(result)[:5]:
        print(f"  - {cmd}")
