#!/usr/bin/env python3
"""
Nmap Output Parser
Parses Nmap scan results and extracts structured data
"""

import re
from typing import Dict, List, Optional
from xml.etree import ElementTree as ET


class NmapParser:
    """Parse Nmap scan output"""
    
    def __init__(self):
        self.port_pattern = re.compile(r'(\d+)/(\w+)\s+(\w+)\s+(\S+)(?:\s+(.+))?')
        self.host_pattern = re.compile(r'Nmap scan report for (.+)')
        self.os_pattern = re.compile(r'Running: (.+)')
        
    def parse(self, output: str) -> Dict:
        """
        Parse Nmap output
        
        Args:
            output: Raw Nmap output
            
        Returns:
            Structured dict with parsed data
        """
        result = {
            'tool': 'nmap',
            'targets': [],
            'open_ports': [],
            'filtered_ports': [],
            'closed_ports': [],
            'os_detection': [],
            'vulnerabilities': [],
            'summary': {}
        }
        
        lines = output.split('\n')
        current_host = None
        
        for line in lines:
            line = line.strip()
            
            # Parse host
            host_match = self.host_pattern.search(line)
            if host_match:
                current_host = host_match.group(1)
                if current_host not in result['targets']:
                    result['targets'].append(current_host)
                continue
            
            # Parse open ports
            port_match = self.port_pattern.search(line)
            if port_match and current_host:
                port = int(port_match.group(1))
                protocol = port_match.group(2)
                state = port_match.group(3)
                service = port_match.group(4)
                version = port_match.group(5) if port_match.group(5) else ''
                
                port_info = {
                    'host': current_host,
                    'port': port,
                    'protocol': protocol,
                    'state': state,
                    'service': service,
                    'version': version.strip()
                }
                
                if state.lower() == 'open':
                    result['open_ports'].append(port_info)
                elif state.lower() == 'filtered':
                    result['filtered_ports'].append(port_info)
                elif state.lower() == 'closed':
                    result['closed_ports'].append(port_info)
                
                # Check for known vulnerabilities
                vuln = self._check_vulnerability(port, service, version)
                if vuln:
                    result['vulnerabilities'].append(vuln)
            
            # Parse OS detection
            os_match = self.os_pattern.search(line)
            if os_match:
                result['os_detection'].append(os_match.group(1))
        
        # Generate summary
        result['summary'] = {
            'total_hosts': len(result['targets']),
            'open_ports_count': len(result['open_ports']),
            'filtered_ports_count': len(result['filtered_ports']),
            'vulnerabilities_found': len(result['vulnerabilities'])
        }
        
        return result
    
    def parse_xml(self, xml_file: str) -> Dict:
        """
        Parse Nmap XML output (more accurate)
        
        Args:
            xml_file: Path to Nmap XML file
            
        Returns:
            Structured dict with parsed data
        """
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            
            result = {
                'tool': 'nmap',
                'targets': [],
                'open_ports': [],
                'os_detection': [],
                'vulnerabilities': []
            }
            
            for host in root.findall('.//host'):
                # Get host address
                address = host.find('.//address[@addrtype="ipv4"]')
                if address is None:
                    address = host.find('.//address[@addrtype="ipv6"]')
                
                if address is not None:
                    host_addr = address.get('addr')
                    result['targets'].append(host_addr)
                    
                    # Get hostname if available
                    hostname_elem = host.find('.//hostname')
                    hostname = hostname_elem.get('name') if hostname_elem is not None else None
                    
                    # Parse ports
                    for port in host.findall('.//port'):
                        port_id = int(port.get('portid'))
                        protocol = port.get('protocol')
                        
                        state = port.find('state')
                        state_val = state.get('state') if state is not None else 'unknown'
                        
                        service = port.find('service')
                        service_name = service.get('name') if service is not None else 'unknown'
                        service_product = service.get('product') if service is not None else ''
                        service_version = service.get('version') if service is not None else ''
                        
                        port_info = {
                            'host': host_addr,
                            'hostname': hostname,
                            'port': port_id,
                            'protocol': protocol,
                            'state': state_val,
                            'service': service_name,
                            'product': service_product,
                            'version': service_version
                        }
                        
                        if state_val == 'open':
                            result['open_ports'].append(port_info)
                            
                            # Check vulnerabilities
                            vuln = self._check_vulnerability(port_id, service_name, service_version)
                            if vuln:
                                vuln['host'] = host_addr
                                result['vulnerabilities'].append(vuln)
                    
                    # Parse OS detection
                    os_matches = host.findall('.//osmatch')
                    for os_match in os_matches[:3]:  # Top 3 matches
                        os_name = os_match.get('name')
                        accuracy = os_match.get('accuracy')
                        result['os_detection'].append({
                            'name': os_name,
                            'accuracy': accuracy
                        })
            
            return result
            
        except Exception as e:
            return {
                'tool': 'nmap',
                'error': str(e),
                'targets': [],
                'open_ports': []
            }
    
    def _check_vulnerability(self, port: int, service: str, version: str) -> Optional[Dict]:
        """Check for known vulnerabilities"""
        
        vulnerabilities = {
            21: {
                'vsftpd 2.3.4': {
                    'name': 'vsftpd 2.3.4 Backdoor',
                    'severity': 'critical',
                    'cve': 'N/A',
                    'description': 'Backdoor command execution',
                    'exploit': 'exploit/unix/ftp/vsftpd_234_backdoor'
                }
            },
            22: {
                'OpenSSH 7.2': {
                    'name': 'OpenSSH Username Enumeration',
                    'severity': 'medium',
                    'cve': 'CVE-2016-6210',
                    'description': 'Username enumeration via timing attack',
                    'exploit': 'auxiliary/scanner/ssh/ssh_enumusers'
                }
            },
            445: {
                'Samba 3.0.20': {
                    'name': 'Samba Username Map Script',
                    'severity': 'critical',
                    'cve': 'CVE-2007-2447',
                    'description': 'Command execution vulnerability',
                    'exploit': 'exploit/multi/samba/usermap_script'
                }
            },
            3306: {
                'MySQL 5.0': {
                    'name': 'MySQL Authentication Bypass',
                    'severity': 'high',
                    'cve': 'CVE-2012-2122',
                    'description': 'Authentication bypass vulnerability',
                    'exploit': 'auxiliary/scanner/mysql/mysql_authbypass_hashdump'
                }
            }
        }
        
        if port in vulnerabilities:
            for vuln_version, vuln_info in vulnerabilities[port].items():
                if vuln_version.lower() in version.lower():
                    return {
                        'port': port,
                        'service': service,
                        'version': version,
                        **vuln_info
                    }
        
        return None
    
    def get_recommendations(self, parsed_data: Dict) -> List[str]:
        """
        Get recommended next steps based on parsed data
        
        Args:
            parsed_data: Parsed Nmap data
            
        Returns:
            List of recommended commands
        """
        recommendations = []
        
        for port_info in parsed_data.get('open_ports', []):
            port = port_info['port']
            host = port_info['host']
            service = port_info['service']
            
            if port in [80, 443, 8080, 8443]:
                protocol = 'https' if port in [443, 8443] else 'http'
                recommendations.append(f"nikto -h {protocol}://{host}:{port}")
                recommendations.append(f"gobuster dir -u {protocol}://{host}:{port} -w /usr/share/wordlists/dirb/common.txt")
            
            elif port in [139, 445]:
                recommendations.append(f"enum4linux -a {host}")
                recommendations.append(f"smbclient -L //{host} -N")
                recommendations.append(f"nmap --script smb-vuln* -p{port} {host}")
            
            elif port == 21:
                recommendations.append(f"ftp {host}")
                recommendations.append(f"nmap --script ftp-anon,ftp-vuln* -p21 {host}")
            
            elif port == 22:
                recommendations.append(f"ssh-audit {host}")
                recommendations.append(f"nmap --script ssh-auth-methods,ssh2-enum-algos -p22 {host}")
            
            elif port == 3306:
                recommendations.append(f"nmap --script mysql-* -p3306 {host}")
            
            elif port == 1433:
                recommendations.append(f"nmap --script ms-sql-* -p1433 {host}")
        
        return recommendations


if __name__ == "__main__":
    # Test parser
    test_output = """
Starting Nmap 7.80 ( https://nmap.org ) at 2024-01-01 12:00 UTC
Nmap scan report for 192.168.1.10
Host is up (0.0010s latency).

PORT    STATE SERVICE     VERSION
21/tcp  open  ftp         vsftpd 2.3.4
22/tcp  open  ssh         OpenSSH 7.2p2 Ubuntu 4ubuntu2.2
80/tcp  open  http        Apache httpd 2.4.18
445/tcp open  netbios-ssn Samba smbd 3.0.20

Nmap done: 1 IP address (1 host up) scanned in 5.23 seconds
"""
    
    parser = NmapParser()
    result = parser.parse(test_output)
    
    print("Parsed Data:")
    print(f"Targets: {result['targets']}")
    print(f"Open Ports: {len(result['open_ports'])}")
    print(f"Vulnerabilities: {len(result['vulnerabilities'])}")
    
    for vuln in result['vulnerabilities']:
        print(f"\n[!] {vuln['name']} - {vuln['severity']}")
        print(f"    Exploit: {vuln['exploit']}")
