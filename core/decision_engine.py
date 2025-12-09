#!/usr/bin/env python3
"""
KaliGPT Decision Engine
Makes intelligent decisions about next steps in penetration testing
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime
import re


class DecisionEngine:
    """
    Analyzes parsed tool output and makes tactical decisions
    """
    
    def __init__(self):
        self.decision_tree = self._build_decision_tree()
        self.priority_matrix = self._build_priority_matrix()
        
    def _build_decision_tree(self) -> Dict:
        """Build decision tree for common scenarios"""
        return {
            'open_port_detected': {
                21: ['ftp_anonymous_check', 'ftp_version_exploit'],
                22: ['ssh_enumeration', 'ssh_bruteforce'],
                23: ['telnet_enumeration'],
                25: ['smtp_enumeration', 'smtp_user_enum'],
                53: ['dns_enumeration', 'zone_transfer'],
                80: ['web_enumeration', 'nikto_scan', 'directory_bruteforce'],
                443: ['web_enumeration', 'ssl_scan', 'directory_bruteforce'],
                139: ['smb_enumeration', 'smb_vuln_scan'],
                445: ['smb_enumeration', 'eternal_blue_check', 'smb_bruteforce'],
                1433: ['mssql_enumeration'],
                3306: ['mysql_enumeration'],
                3389: ['rdp_enumeration', 'rdp_bruteforce'],
                5432: ['postgresql_enumeration'],
                8080: ['web_enumeration', 'tomcat_check'],
            },
            'service_detected': {
                'vsftpd_2.3.4': 'metasploit_vsftpd_backdoor',
                'ProFTPD': 'proftpd_exploits',
                'Apache': 'apache_version_check',
                'nginx': 'nginx_version_check',
                'OpenSSH': 'ssh_version_check',
                'Samba': 'samba_exploits',
                'Microsoft-IIS': 'iis_exploits',
                'MySQL': 'mysql_exploits',
                'PostgreSQL': 'postgresql_exploits',
            },
            'vulnerability_found': {
                'sql_injection': ['sqlmap_exploitation', 'manual_sqli'],
                'xss': ['xss_exploitation', 'session_hijacking'],
                'lfi': ['lfi_to_rce', 'log_poisoning'],
                'rfi': ['rfi_exploitation'],
                'command_injection': ['rce_exploitation'],
                'file_upload': ['upload_shell', 'bypass_filters'],
            }
        }
    
    def _build_priority_matrix(self) -> Dict:
        """Build priority matrix for findings"""
        return {
            'critical': {
                'score': 10,
                'examples': ['rce', 'authentication_bypass', 'sql_injection', 'privilege_escalation']
            },
            'high': {
                'score': 7,
                'examples': ['xss', 'lfi', 'directory_traversal', 'weak_credentials']
            },
            'medium': {
                'score': 5,
                'examples': ['information_disclosure', 'insecure_configuration']
            },
            'low': {
                'score': 3,
                'examples': ['version_disclosure', 'missing_headers']
            }
        }
    
    def analyze_and_decide(self, parsed_data: Dict, tool_type: str) -> Dict:
        """
        Analyze parsed data and make decision
        
        Args:
            parsed_data: Parsed output from tool parser
            tool_type: Type of tool (nmap, metasploit, etc.)
            
        Returns:
            Decision dict with recommendations
        """
        decisions = {
            'timestamp': datetime.now().isoformat(),
            'tool_type': tool_type,
            'findings': [],
            'recommendations': [],
            'priority_actions': [],
            'next_commands': []
        }
        
        # Route to appropriate analyzer
        if tool_type == 'nmap':
            decisions = self._analyze_nmap(parsed_data, decisions)
        elif tool_type == 'metasploit':
            decisions = self._analyze_metasploit(parsed_data, decisions)
        elif tool_type == 'sqlmap':
            decisions = self._analyze_sqlmap(parsed_data, decisions)
        elif tool_type == 'nikto':
            decisions = self._analyze_nikto(parsed_data, decisions)
        elif tool_type == 'gobuster':
            decisions = self._analyze_gobuster(parsed_data, decisions)
        elif tool_type == 'hydra':
            decisions = self._analyze_hydra(parsed_data, decisions)
        
        # Prioritize actions
        decisions = self._prioritize_actions(decisions)
        
        return decisions
    
    def _analyze_nmap(self, data: Dict, decisions: Dict) -> Dict:
        """Analyze nmap output"""
        # Check for open ports
        if 'open_ports' in data:
            for port_info in data['open_ports']:
                port = port_info.get('port')
                service = port_info.get('service', '')
                version = port_info.get('version', '')
                
                decisions['findings'].append({
                    'type': 'open_port',
                    'port': port,
                    'service': service,
                    'version': version
                })
                
                # Get recommendations for this port
                if port in self.decision_tree['open_port_detected']:
                    next_steps = self.decision_tree['open_port_detected'][port]
                    for step in next_steps:
                        decisions['recommendations'].append({
                            'action': step,
                            'port': port,
                            'reason': f'Port {port} ({service}) is open'
                        })
                
                # Check for vulnerable versions
                vuln_check = self._check_vulnerable_version(service, version)
                if vuln_check:
                    decisions['priority_actions'].append({
                        'type': 'vulnerability',
                        'severity': 'high',
                        'description': vuln_check['description'],
                        'exploit': vuln_check['exploit']
                    })
        
        # Generate next commands
        decisions['next_commands'] = self._generate_nmap_followup(data)
        
        return decisions
    
    def _analyze_metasploit(self, data: Dict, decisions: Dict) -> Dict:
        """Analyze metasploit output"""
        if data.get('exploit_success'):
            decisions['findings'].append({
                'type': 'successful_exploit',
                'module': data.get('module'),
                'target': data.get('target')
            })
            
            decisions['recommendations'].append({
                'action': 'post_exploitation',
                'reason': 'Exploit successful, proceed with post-exploitation'
            })
            
            decisions['next_commands'] = [
                'getuid',
                'sysinfo',
                'ps',
                'migrate -N explorer.exe',
                'hashdump'
            ]
        else:
            decisions['recommendations'].append({
                'action': 'try_alternative_exploit',
                'reason': 'Current exploit failed'
            })
        
        return decisions
    
    def _analyze_sqlmap(self, data: Dict, decisions: Dict) -> Dict:
        """Analyze sqlmap output"""
        if data.get('injection_found'):
            decisions['findings'].append({
                'type': 'sql_injection',
                'severity': 'critical',
                'parameter': data.get('parameter'),
                'technique': data.get('technique')
            })
            
            decisions['priority_actions'].append({
                'type': 'data_extraction',
                'severity': 'critical',
                'description': 'SQL injection confirmed - extract data',
                'commands': [
                    f"sqlmap -u {data.get('url')} --dbs",
                    f"sqlmap -u {data.get('url')} --tables",
                    f"sqlmap -u {data.get('url')} --dump"
                ]
            })
        
        if data.get('databases'):
            decisions['next_commands'] = [
                f"sqlmap -u {data.get('url')} -D {db} --tables" 
                for db in data.get('databases', [])[:3]
            ]
        
        return decisions
    
    def _analyze_nikto(self, data: Dict, decisions: Dict) -> Dict:
        """Analyze nikto output"""
        if 'vulnerabilities' in data:
            for vuln in data['vulnerabilities']:
                decisions['findings'].append({
                    'type': 'web_vulnerability',
                    'description': vuln.get('description'),
                    'severity': vuln.get('severity', 'medium')
                })
        
        decisions['recommendations'].append({
            'action': 'directory_enumeration',
            'reason': 'Web server identified, enumerate directories'
        })
        
        decisions['next_commands'] = [
            f"gobuster dir -u {data.get('url', 'http://target')} -w /usr/share/wordlists/dirb/common.txt",
            f"ffuf -u {data.get('url', 'http://target')}/FUZZ -w /usr/share/wordlists/dirb/common.txt"
        ]
        
        return decisions
    
    def _analyze_gobuster(self, data: Dict, decisions: Dict) -> Dict:
        """Analyze gobuster output"""
        interesting_paths = []
        
        if 'found_paths' in data:
            for path in data['found_paths']:
                status_code = path.get('status_code')
                url = path.get('url')
                
                # Identify interesting paths
                if '/admin' in url or '/login' in url or '/upload' in url:
                    interesting_paths.append(url)
                    decisions['findings'].append({
                        'type': 'interesting_directory',
                        'url': url,
                        'status_code': status_code
                    })
        
        if interesting_paths:
            decisions['recommendations'].append({
                'action': 'investigate_paths',
                'paths': interesting_paths,
                'reason': 'Found potentially interesting directories'
            })
        
        return decisions
    
    def _analyze_hydra(self, data: Dict, decisions: Dict) -> Dict:
        """Analyze hydra output"""
        if data.get('credentials_found'):
            for cred in data.get('credentials_found', []):
                decisions['findings'].append({
                    'type': 'valid_credentials',
                    'severity': 'high',
                    'username': cred.get('username'),
                    'password': cred.get('password'),
                    'service': data.get('service')
                })
                
                decisions['priority_actions'].append({
                    'type': 'access_service',
                    'severity': 'high',
                    'description': f"Use credentials to access {data.get('service')}",
                    'credentials': cred
                })
        
        return decisions
    
    def _check_vulnerable_version(self, service: str, version: str) -> Optional[Dict]:
        """Check if a service version is known to be vulnerable"""
        
        vulnerable_versions = {
            'vsftpd_2.3.4': {
                'description': 'vsftpd 2.3.4 backdoor vulnerability',
                'exploit': 'exploit/unix/ftp/vsftpd_234_backdoor'
            },
            'Apache_2.4.49': {
                'description': 'Apache 2.4.49 Path Traversal (CVE-2021-41773)',
                'exploit': 'exploit/multi/http/apache_normalize_path_rce'
            },
            'ProFTPD_1.3.5': {
                'description': 'ProFTPD 1.3.5 mod_copy RCE',
                'exploit': 'exploit/unix/ftp/proftpd_modcopy_exec'
            }
        }
        
        # Normalize the check
        check_key = f"{service}_{version}".replace(' ', '_')
        
        for vuln_key, vuln_info in vulnerable_versions.items():
            if vuln_key.lower() in check_key.lower():
                return vuln_info
        
        return None
    
    def _generate_nmap_followup(self, data: Dict) -> List[str]:
        """Generate follow-up commands after nmap scan"""
        commands = []
        target = data.get('target', 'TARGET')
        
        # If we found web ports, suggest web enumeration
        web_ports = [p['port'] for p in data.get('open_ports', []) 
                     if p['port'] in [80, 443, 8080, 8443]]
        
        for port in web_ports[:2]:  # Limit to first 2
            protocol = 'https' if port in [443, 8443] else 'http'
            commands.append(f"nikto -h {protocol}://{target}:{port}")
            commands.append(f"gobuster dir -u {protocol}://{target}:{port} -w /usr/share/wordlists/dirb/common.txt")
        
        # If SMB is open, suggest SMB enumeration
        smb_ports = [p['port'] for p in data.get('open_ports', []) 
                     if p['port'] in [139, 445]]
        
        if smb_ports:
            commands.append(f"enum4linux -a {target}")
            commands.append(f"smbclient -L //{target} -N")
        
        return commands
    
    def _prioritize_actions(self, decisions: Dict) -> Dict:
        """Prioritize actions by severity and impact"""
        
        # Sort priority actions by severity
        if 'priority_actions' in decisions:
            severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
            decisions['priority_actions'].sort(
                key=lambda x: severity_order.get(x.get('severity', 'low'), 4)
            )
        
        return decisions
    
    def suggest_next_phase(self, current_phase: str, findings: List[Dict]) -> Tuple[str, str]:
        """
        Suggest next penetration testing phase
        
        Args:
            current_phase: Current phase
            findings: Current findings
            
        Returns:
            Tuple of (next_phase, reason)
        """
        phase_progression = {
            'reconnaissance': ('enumeration', 'Basic recon complete, time to enumerate services'),
            'enumeration': ('exploitation', 'Services enumerated, ready to exploit vulnerabilities'),
            'exploitation': ('post-exploitation', 'Initial access gained, escalate privileges'),
            'post-exploitation': ('lateral-movement', 'System compromised, move laterally'),
            'lateral-movement': ('reporting', 'All targets compromised, document findings'),
        }
        
        # Check if we have findings that suggest moving to next phase
        has_open_ports = any(f.get('type') == 'open_port' for f in findings)
        has_vulnerabilities = any(f.get('type') in ['sql_injection', 'web_vulnerability'] for f in findings)
        has_access = any(f.get('type') in ['successful_exploit', 'valid_credentials'] for f in findings)
        
        if current_phase == 'reconnaissance' and has_open_ports:
            return phase_progression['reconnaissance']
        elif current_phase == 'enumeration' and has_vulnerabilities:
            return phase_progression['enumeration']
        elif current_phase == 'exploitation' and has_access:
            return phase_progression['exploitation']
        elif current_phase in phase_progression:
            return phase_progression[current_phase]
        
        return (current_phase, 'Continue current phase')
