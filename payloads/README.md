# KaliGPT Payload System

## Overview

The KaliGPT payload system provides a comprehensive collection of penetration testing payloads with three powerful generation modes:

1. **Standard Generation** - Generate payloads programmatically
2. **Template-Based** - Use pre-built JSON templates with variable substitution
3. **AI-Powered** - Leverage AI to generate custom payloads based on target context

## Features

- 🎯 **Target-Aware Generation**: AI analyzes target information to create contextual payloads
- 📚 **Extensive Template Library**: Pre-built templates for common attack vectors
- 🔄 **Variable Substitution**: Customize payloads with dynamic variables
- 🤖 **AI Integration**: Generate sophisticated payloads using GPT-5, Gemini 3, or Claude
- 🛡️ **Multiple Categories**: Shells, web shells, exploits, privilege escalation, wordlists

## Quick Start

### Basic Usage

```python
from payloads.generator import PayloadGenerator

# Initialize generator
generator = PayloadGenerator()

# Generate from template
payload = generator.get_from_template('sqli', 'union_based_mysql', {
    'TABLE': 'users',
    'COLUMN': 'password'
})

# List available templates
templates = generator.list_templates()
```

### AI-Powered Generation

```python
from ai.engine import AIEngine
from payloads.generator import PayloadGenerator

# Initialize with AI engine
ai_engine = AIEngine(model='gpt-5.1')
generator = PayloadGenerator(ai_engine)

# Generate payload based on target info
target_info = {
    'target_type': 'web_application',
    'technology': 'PHP/MySQL',
    'vulnerability': 'SQL Injection',
    'context': 'Login form with username and password fields',
    'waf': 'ModSecurity'
}

payload = generator.generate_with_ai(target_info)
```

## Template Categories

### 1. Reverse Shells (`shells/`)

Pre-built reverse shell templates for various languages and scenarios.

**Available Templates:**
- Bash (TCP/UDP)
- Python (PTY/Windows)
- Netcat (Traditional/Mkfifo)
- PHP, Perl, Ruby
- PowerShell (TCP/Base64)
- Java, Socat, Golang, AWK, Lua

**Variables:**
- `{{ATTACKER_IP}}` - Your IP address
- `{{ATTACKER_PORT}}` - Listening port

**Example:**
```python
shell = generator.get_from_template('reverse_shells', 'bash_tcp', {
    'ATTACKER_IP': '10.10.14.5',
    'ATTACKER_PORT': '4444'
})
```

### 2. Web Shells (`webshells/`)

PHP web shell templates from simple to advanced.

**Available Templates:**
- Simple Shell
- Advanced Shell with File Browser
- Mini Shell
- C99-Style Shell
- WSO-Style Shell
- Upload Handler
- Eval Shell
- Reverse Shell
- Persistent Backdoor

**Variables:**
- `{{ATTACKER_IP}}` - Your IP address
- `{{ATTACKER_PORT}}` - Connection port
- `{{SECRET_KEY}}` - Authentication key

**Example:**
```python
webshell = generator.get_from_template('webshells', 'advanced_shell', {
    'SECRET_KEY': 'MySecretKey123'
})
```

### 3. Exploits (`exploits/`)

#### SQL Injection Payloads

**Categories:**
- Union-Based (MySQL, MSSQL, Oracle)
- Boolean-Based Blind
- Time-Based Blind (MySQL, PostgreSQL, MSSQL, Oracle)
- Error-Based
- Stacked Queries
- Authentication Bypass
- Out-of-Band
- Second Order
- WAF Bypass

**Variables:**
- `{{TABLE}}` - Target table name
- `{{COLUMN}}` - Target column name
- `{{CHAR}}` - Character position
- `{{POS}}` - String position
- `{{VALUE}}` - Test value
- `{{ATTACKER_DOMAIN}}` - Your domain for OOB

**Example:**
```python
sqli = generator.get_from_template('sqli', 'union_based_mysql', {
    'TABLE': 'users',
    'COLUMN': 'password'
})
```

#### XSS Payloads

**Categories:**
- Reflected XSS (HTML, JS, Attribute, URL contexts)
- Stored XSS
- DOM-Based XSS
- Filter Bypass Techniques
- Advanced Payloads (Cookie Stealer, Keylogger, Form Hijack, BeEF Hook)
- WAF Bypass (CloudFlare, Akamai, Generic)
- Polyglot Payloads

**Variables:**
- `{{ATTACKER_DOMAIN}}` - Your domain/IP
- `{{BEEF_SERVER}}` - BeEF server URL
- `{{PORT}}` - Server port

**Example:**
```python
xss = generator.get_from_template('xss', 'cookie_stealer', {
    'ATTACKER_DOMAIN': 'attacker.com'
})
```

### 4. Privilege Escalation (`privesc/`)

#### Linux Privilege Escalation

**Techniques:**
- SUID Binary Exploitation
- Linux Capabilities Abuse
- Sudo Misconfigurations
- Writable /etc/passwd
- Cron Job Exploitation
- PATH Hijacking
- NFS Root Squashing
- Docker Container Escape
- Kernel Exploits (DirtyCow, Dirty Pipe)

#### Windows Privilege Escalation

**Techniques:**
- Unquoted Service Paths
- AlwaysInstallElevated
- Token Impersonation
- Kernel Exploits (MS16-032, PrintNightmare)

**Variables:**
- `{{TARGET_IP}}` - Target machine IP
- `{{ATTACKER_IP}}` - Your IP address
- `{{PORT}}` - Connection port

**Example:**
```python
privesc = generator.get_from_template('privesc', 'linux_suid', {
    'ATTACKER_IP': '10.10.14.5',
    'PORT': '4444'
})
```

### 5. Wordlists (`wordlists/`)

Intelligent wordlist generators for password cracking and user enumeration.

**Generators:**
- **Common Passwords** - Base words with common patterns
- **Username Generator** - Create username variations
- **Company Passwords** - Company-based password patterns
- **Season/Date Passwords** - Seasonal and date-based passwords
- **Mutation Rules** - Character substitution patterns
- **Keyboard Walk** - Keyboard pattern passwords
- **Default Credentials** - Common default username:password pairs
- **Email Generator** - Email address variations for enumeration

**Variables:**
- `{{FIRSTNAME}}`, `{{LASTNAME}}` - User names
- `{{COMPANY}}` - Company name
- `{{YEAR}}` - Current year
- `{{DOMAIN}}` - Email domain
- `{{WORD}}` - Base word for mutations

**Example:**
```python
# Generate username wordlist
usernames = generator.get_from_template('wordlists', 'username_generator', {
    'FIRSTNAME': 'john',
    'LASTNAME': 'smith',
    'FIRST_INITIAL': 'j',
    'LAST_INITIAL': 's'
})

# Generate company passwords
passwords = generator.get_from_template('wordlists', 'company_passwords', {
    'COMPANY': 'AcmeCorp',
    'YEAR': '2025'
})
```

## AI-Powered Payload Generation

The AI engine can generate custom payloads based on detailed target information.

### Target Information Structure

```python
target_info = {
    'target_type': 'web_application',  # or 'network', 'api', 'mobile', etc.
    'technology': 'PHP/MySQL',          # Technology stack
    'vulnerability': 'SQL Injection',   # Vulnerability type
    'context': 'Login form...',         # Detailed context
    'waf': 'ModSecurity',               # WAF/security controls
    'constraints': 'No special chars',  # Any limitations
    'objective': 'Extract admin hash'   # What you want to achieve
}
```

### AI Generation Examples

#### SQL Injection with WAF Bypass

```python
target = {
    'target_type': 'web_application',
    'technology': 'PHP/MySQL',
    'vulnerability': 'SQL Injection',
    'context': 'Search parameter in GET request, single quotes filtered',
    'waf': 'ModSecurity with OWASP Core Rule Set',
    'objective': 'Extract database version and table names'
}

payload = generator.generate_with_ai(target)
```

#### Privilege Escalation

```python
target = {
    'target_type': 'linux_server',
    'technology': 'Ubuntu 20.04',
    'vulnerability': 'Writable /etc/passwd',
    'context': 'Low-privilege user with write access to /etc/passwd',
    'constraints': 'No sudo, no SUID binaries available',
    'objective': 'Gain root access'
}

exploit = generator.generate_with_ai(target)
```

#### Custom Web Shell

```python
target = {
    'target_type': 'web_application',
    'technology': 'PHP 7.4',
    'vulnerability': 'File upload',
    'context': 'Can upload PHP files, but common functions are disabled',
    'constraints': 'exec, system, passthru, shell_exec disabled',
    'objective': 'Remote code execution with obfuscation'
}

webshell = generator.generate_with_ai(target)
```

## Advanced Features

### Template Listing

```python
# List all template categories
categories = generator.list_templates()

# Output:
# {
#   'sqli': ['union_based_mysql', 'boolean_based', ...],
#   'xss': ['reflected_xss', 'stored_xss', ...],
#   'webshells': ['simple_shell', 'advanced_shell', ...],
#   'reverse_shells': ['bash_tcp', 'python_pty', ...],
#   'privesc': ['linux_suid', 'windows_unquoted', ...],
#   'wordlists': ['common_passwords', 'username_generator', ...]
# }
```

### Variable Substitution

All templates support dynamic variable substitution using the `{{VARIABLE}}` syntax.

```python
# Variables are automatically replaced
payload = generator.get_from_template('category', 'template_name', {
    'VARIABLE1': 'value1',
    'VARIABLE2': 'value2'
})
```

### Custom Template Creation

Create your own templates in JSON format:

```json
{
  "template_name": {
    "name": "Display Name",
    "description": "What this template does",
    "payload": "Your payload with {{VARIABLES}}",
    "variables": ["VAR1", "VAR2"],
    "notes": "Usage notes"
  }
}
```

## Best Practices

1. **Always use AI generation for complex scenarios** - The AI can adapt to specific target configurations
2. **Combine templates with AI** - Use templates as a starting point, then refine with AI
3. **Provide detailed target context** - More information = better payload generation
4. **Test in safe environments** - Always test payloads in authorized environments
5. **Keep templates updated** - Regularly update templates with new techniques

## Security & Legal Notice

⚠️ **WARNING**: These tools are for authorized penetration testing and security research only.

- Only use on systems you have explicit permission to test
- Unauthorized access to computer systems is illegal
- Always follow responsible disclosure practices
- Comply with all applicable laws and regulations

## Contributing

To add new templates:

1. Create JSON file in appropriate `templates/` subdirectory
2. Follow the existing template structure
3. Include clear descriptions and variable documentation
4. Test all payloads before submitting
5. Submit pull request to https://github.com/yashab-cyber/KaliGpt

## Support

For issues, questions, or feature requests:
- GitHub Issues: https://github.com/yashab-cyber/KaliGpt/issues
- Documentation: https://github.com/yashab-cyber/KaliGpt/docs

## License

See main repository LICENSE file for details.
