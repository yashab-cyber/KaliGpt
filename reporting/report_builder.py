#!/usr/bin/env python3
"""
KaliGPT Report Builder
Generates penetration testing reports in various formats
"""

import os
import json
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path

# Optional dependencies (installed separately)
# - weasyprint: for HTML to PDF conversion
# - pdfkit: alternative PDF generation (requires wkhtmltopdf)


class ReportBuilder:
    """
    Build comprehensive penetration testing reports
    """
    
    def __init__(self, output_dir: str = "reports"):
        """
        Initialize report builder
        
        Args:
            output_dir: Directory to save reports
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.template_dir = Path("reporting/templates")
        
    def build_report(self, session_data: Dict, format: str = 'markdown') -> str:
        """
        Build a report from session data
        
        Args:
            session_data: Session data including findings, commands, etc.
            format: Output format (markdown, html, pdf, json)
            
        Returns:
            Path to generated report
        """
        if format == 'markdown':
            return self._build_markdown(session_data)
        elif format == 'html':
            return self._build_html(session_data)
        elif format == 'pdf':
            return self._build_pdf(session_data)
        elif format == 'json':
            return self._build_json(session_data)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def _build_markdown(self, session_data: Dict) -> str:
        """Build Markdown report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.output_dir / f"pentest_report_{timestamp}.md"
        
        with open(filename, 'w') as f:
            # Header
            f.write("# Penetration Testing Report\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**Prepared by:** KaliGPT\n\n")
            f.write("---\n\n")
            
            # Executive Summary
            f.write("## Executive Summary\n\n")
            f.write(self._generate_executive_summary(session_data))
            f.write("\n\n")
            
            # Target Information
            f.write("## Target Information\n\n")
            target_info = session_data.get('context', {}).get('target', {})
            f.write(f"- **Target IP:** {target_info.get('ip', 'N/A')}\n")
            f.write(f"- **Hostname:** {target_info.get('hostname', 'N/A')}\n")
            f.write(f"- **Scan Date:** {session_data.get('start_time', 'N/A')}\n\n")
            
            # Findings Summary
            f.write("## Findings Summary\n\n")
            vulnerabilities = session_data.get('context', {}).get('vulnerabilities', [])
            f.write(self._generate_findings_table(vulnerabilities))
            f.write("\n\n")
            
            # Detailed Findings
            f.write("## Detailed Findings\n\n")
            for i, vuln in enumerate(vulnerabilities, 1):
                f.write(f"### {i}. {vuln.get('name', 'Unknown Vulnerability')}\n\n")
                f.write(f"**Severity:** {vuln.get('severity', 'Unknown').upper()}\n\n")
                f.write(f"**Description:**\n{vuln.get('description', 'No description available')}\n\n")
                
                if 'cve' in vuln:
                    f.write(f"**CVE:** {vuln['cve']}\n\n")
                
                if 'exploit' in vuln:
                    f.write(f"**Exploit Module:** `{vuln['exploit']}`\n\n")
                
                f.write(f"**Remediation:**\n{self._generate_remediation(vuln)}\n\n")
                f.write("---\n\n")
            
            # Services Discovered
            f.write("## Discovered Services\n\n")
            services = session_data.get('context', {}).get('services', [])
            if services:
                f.write("| Port | Protocol | Service | Version |\n")
                f.write("|------|----------|---------|----------|\n")
                for svc in services:
                    f.write(f"| {svc.get('port', 'N/A')} | ")
                    f.write(f"{svc.get('protocol', 'tcp')} | ")
                    f.write(f"{svc.get('service', 'unknown')} | ")
                    f.write(f"{svc.get('version', 'N/A')} |\n")
                f.write("\n\n")
            
            # Commands Executed
            f.write("## Commands Executed\n\n")
            commands = session_data.get('commands', [])
            if commands:
                f.write("```bash\n")
                for cmd in commands[-20:]:  # Last 20 commands
                    f.write(f"{cmd.get('command', '')}\n")
                f.write("```\n\n")
            
            # Recommendations
            f.write("## Recommendations\n\n")
            f.write(self._generate_recommendations(session_data))
            f.write("\n\n")
            
            # Appendix
            f.write("## Appendix\n\n")
            f.write("### Tools Used\n\n")
            tools = set()
            for cmd in commands:
                tool = cmd.get('command', '').split()[0] if cmd.get('command') else ''
                if tool:
                    tools.add(tool)
            
            for tool in sorted(tools):
                f.write(f"- {tool}\n")
            
        return str(filename)
    
    def _build_html(self, session_data: Dict) -> str:
        """Build HTML report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.output_dir / f"pentest_report_{timestamp}.html"
        
        vulnerabilities = session_data.get('context', {}).get('vulnerabilities', [])
        services = session_data.get('context', {}).get('services', [])
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Penetration Testing Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f4f4f4;
        }}
        .container {{
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 8px;
        }}
        .severity-critical {{
            background: #e74c3c;
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            font-weight: bold;
        }}
        .severity-high {{
            background: #e67e22;
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            font-weight: bold;
        }}
        .severity-medium {{
            background: #f39c12;
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            font-weight: bold;
        }}
        .severity-low {{
            background: #3498db;
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            font-weight: bold;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #34495e;
            color: white;
        }}
        tr:hover {{
            background-color: #f5f5f5;
        }}
        .vulnerability {{
            background: #fff;
            border-left: 4px solid #3498db;
            padding: 15px;
            margin: 15px 0;
            border-radius: 4px;
        }}
        .code {{
            background: #2c3e50;
            color: #ecf0f1;
            padding: 15px;
            border-radius: 4px;
            overflow-x: auto;
        }}
        .meta {{
            color: #7f8c8d;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔒 Penetration Testing Report</h1>
        
        <div class="meta">
            <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p><strong>Prepared by:</strong> KaliGPT</p>
        </div>
        
        <h2>Executive Summary</h2>
        <p>{self._generate_executive_summary(session_data)}</p>
        
        <h2>Findings Summary</h2>
        {self._generate_findings_html_table(vulnerabilities)}
        
        <h2>Detailed Findings</h2>
"""
        
        for i, vuln in enumerate(vulnerabilities, 1):
            severity = vuln.get('severity', 'low')
            html += f"""
        <div class="vulnerability">
            <h3>{i}. {vuln.get('name', 'Unknown Vulnerability')}</h3>
            <p><span class="severity-{severity}">{severity.upper()}</span></p>
            <p><strong>Description:</strong> {vuln.get('description', 'No description')}</p>
            <p><strong>Remediation:</strong> {self._generate_remediation(vuln)}</p>
        </div>
"""
        
        html += """
        <h2>Discovered Services</h2>
        <table>
            <tr>
                <th>Port</th>
                <th>Protocol</th>
                <th>Service</th>
                <th>Version</th>
            </tr>
"""
        
        for svc in services:
            html += f"""
            <tr>
                <td>{svc.get('port', 'N/A')}</td>
                <td>{svc.get('protocol', 'tcp')}</td>
                <td>{svc.get('service', 'unknown')}</td>
                <td>{svc.get('version', 'N/A')}</td>
            </tr>
"""
        
        html += """
        </table>
        
        <h2>Recommendations</h2>
        """ + self._generate_recommendations(session_data) + """
        
    </div>
</body>
</html>
"""
        
        with open(filename, 'w') as f:
            f.write(html)
        
        return str(filename)
    
    def _build_pdf(self, session_data: Dict) -> str:
        """Build PDF report (converts from HTML)"""
        # First generate HTML
        html_file = self._build_html(session_data)
        
        # Try to convert to PDF using various methods
        pdf_file = html_file.replace('.html', '.pdf')
        
        try:
            # Try weasyprint first
            import weasyprint
            weasyprint.HTML(filename=html_file).write_pdf(pdf_file)
            return pdf_file
        except ImportError:
            pass
        
        try:
            # Try pdfkit (requires wkhtmltopdf)
            try:
                import pdfkit
            except ImportError:
                # pdfkit not installed, skip this method
                raise ImportError("pdfkit not available")
            pdfkit.from_file(html_file, pdf_file)
            return pdf_file
        except:
            pass
        
        # If PDF generation fails, return HTML
        print("[Warning] PDF generation failed. Install weasyprint or pdfkit.")
        print(f"[Info] HTML report available at: {html_file}")
        return html_file
    
    def _build_json(self, session_data: Dict) -> str:
        """Build JSON report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.output_dir / f"pentest_report_{timestamp}.json"
        
        report = {
            "metadata": {
                "generated": datetime.now().isoformat(),
                "tool": "KaliGPT",
                "format_version": "1.0"
            },
            "target": session_data.get('context', {}).get('target', {}),
            "vulnerabilities": session_data.get('context', {}).get('vulnerabilities', []),
            "services": session_data.get('context', {}).get('services', []),
            "exploits": session_data.get('context', {}).get('exploits', []),
            "commands": session_data.get('commands', []),
            "summary": {
                "total_vulnerabilities": len(session_data.get('context', {}).get('vulnerabilities', [])),
                "critical": len([v for v in session_data.get('context', {}).get('vulnerabilities', []) if v.get('severity') == 'critical']),
                "high": len([v for v in session_data.get('context', {}).get('vulnerabilities', []) if v.get('severity') == 'high']),
                "medium": len([v for v in session_data.get('context', {}).get('vulnerabilities', []) if v.get('severity') == 'medium']),
                "low": len([v for v in session_data.get('context', {}).get('vulnerabilities', []) if v.get('severity') == 'low'])
            }
        }
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        return str(filename)
    
    def _generate_executive_summary(self, session_data: Dict) -> str:
        """Generate executive summary"""
        vulns = session_data.get('context', {}).get('vulnerabilities', [])
        
        critical = len([v for v in vulns if v.get('severity') == 'critical'])
        high = len([v for v in vulns if v.get('severity') == 'high'])
        medium = len([v for v in vulns if v.get('severity') == 'medium'])
        low = len([v for v in vulns if v.get('severity') == 'low'])
        
        summary = f"""This penetration test was conducted using KaliGPT, an AI-powered penetration testing assistant. 
The assessment identified **{len(vulns)} total vulnerabilities** across the target system(s).

**Severity Breakdown:**
- Critical: {critical}
- High: {high}
- Medium: {medium}
- Low: {low}

"""
        
        if critical > 0:
            summary += "⚠️ **CRITICAL**: Immediate action required. Critical vulnerabilities pose severe risk to the organization.\n\n"
        elif high > 0:
            summary += "⚠️ **HIGH PRIORITY**: High-severity vulnerabilities require prompt remediation.\n\n"
        else:
            summary += "✓ No critical or high-severity vulnerabilities were identified during this assessment.\n\n"
        
        return summary
    
    def _generate_findings_table(self, vulnerabilities: List[Dict]) -> str:
        """Generate findings summary table (Markdown)"""
        if not vulnerabilities:
            return "No vulnerabilities found.\n"
        
        table = "| # | Vulnerability | Severity | Port/Service |\n"
        table += "|---|---------------|----------|-------------|\n"
        
        for i, vuln in enumerate(vulnerabilities, 1):
            name = vuln.get('name', 'Unknown')[:50]
            severity = vuln.get('severity', 'unknown').upper()
            port = vuln.get('port', 'N/A')
            service = vuln.get('service', 'N/A')
            
            table += f"| {i} | {name} | {severity} | {port}/{service} |\n"
        
        return table
    
    def _generate_findings_html_table(self, vulnerabilities: List[Dict]) -> str:
        """Generate findings summary table (HTML)"""
        if not vulnerabilities:
            return "<p>No vulnerabilities found.</p>"
        
        html = "<table><tr><th>#</th><th>Vulnerability</th><th>Severity</th><th>Port/Service</th></tr>"
        
        for i, vuln in enumerate(vulnerabilities, 1):
            name = vuln.get('name', 'Unknown')
            severity = vuln.get('severity', 'unknown')
            port = vuln.get('port', 'N/A')
            service = vuln.get('service', 'N/A')
            
            html += f"""<tr>
                <td>{i}</td>
                <td>{name}</td>
                <td><span class="severity-{severity}">{severity.upper()}</span></td>
                <td>{port}/{service}</td>
            </tr>"""
        
        html += "</table>"
        return html
    
    def _generate_remediation(self, vuln: Dict) -> str:
        """Generate remediation advice"""
        name = vuln.get('name', '').lower()
        
        remediations = {
            'sql injection': 'Use parameterized queries and input validation. Implement ORM frameworks. Apply principle of least privilege to database accounts.',
            'xss': 'Implement output encoding. Use Content Security Policy (CSP). Sanitize user input.',
            'weak credentials': 'Enforce strong password policy. Implement multi-factor authentication. Disable default accounts.',
            'outdated': 'Update to the latest stable version. Apply security patches. Monitor vendor security advisories.',
            'directory traversal': 'Implement input validation. Use whitelist of allowed files. Apply proper access controls.',
            'command injection': 'Avoid system calls with user input. Use parameterized APIs. Implement strict input validation.'
        }
        
        for key, remediation in remediations.items():
            if key in name:
                return remediation
        
        return 'Apply security patches. Follow vendor security guidelines. Implement defense-in-depth strategies.'
    
    def _generate_recommendations(self, session_data: Dict) -> str:
        """Generate general recommendations"""
        recommendations = """
### Immediate Actions
1. Address all critical and high-severity vulnerabilities immediately
2. Implement security patches and updates
3. Review and strengthen authentication mechanisms
4. Conduct security awareness training for staff

### Short-term Recommendations
1. Implement regular vulnerability scanning
2. Establish patch management processes
3. Deploy intrusion detection/prevention systems
4. Implement logging and monitoring

### Long-term Strategic Recommendations
1. Develop comprehensive security policies
2. Implement security development lifecycle (SDL)
3. Regular penetration testing and security audits
4. Build security incident response capabilities
"""
        return recommendations


if __name__ == "__main__":
    # Test report builder
    test_data = {
        "start_time": "2024-01-01 12:00:00",
        "context": {
            "target": {
                "ip": "192.168.1.100",
                "hostname": "target.local"
            },
            "vulnerabilities": [
                {
                    "name": "SQL Injection in login form",
                    "severity": "critical",
                    "port": 80,
                    "service": "http",
                    "description": "Authentication bypass via SQL injection",
                    "cve": "CVE-2024-1234"
                },
                {
                    "name": "Weak SSH credentials",
                    "severity": "high",
                    "port": 22,
                    "service": "ssh",
                    "description": "Default credentials detected"
                }
            ],
            "services": [
                {"port": 22, "protocol": "tcp", "service": "ssh", "version": "OpenSSH 7.2"},
                {"port": 80, "protocol": "tcp", "service": "http", "version": "Apache 2.4.18"}
            ]
        },
        "commands": [
            {"command": "nmap -sV 192.168.1.100"},
            {"command": "nikto -h http://192.168.1.100"}
        ]
    }
    
    builder = ReportBuilder()
    
    print("Generating Markdown report...")
    md_report = builder.build_report(test_data, format='markdown')
    print(f"Markdown report: {md_report}")
    
    print("\nGenerating HTML report...")
    html_report = builder.build_report(test_data, format='html')
    print(f"HTML report: {html_report}")
