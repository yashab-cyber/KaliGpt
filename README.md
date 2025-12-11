<div align="center">
  <img src="public/Untitled design.png" alt="KaliGPT Logo" width="200"/>
  
  # 🔒 KaliGPT - AI-Powered Penetration Testing Assistant

  [![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![Kali Linux](https://img.shields.io/badge/Kali-Linux-557C94?logo=kalilinux)](https://www.kali.org/)
  [![GUI](https://img.shields.io/badge/GUI-Available-00d9ff.svg)](ui/)
  
  **Created by Yashab Alam**
  
  [![Instagram](https://img.shields.io/badge/Instagram-%23E4405F.svg?style=flat&logo=Instagram&logoColor=white)](https://www.instagram.com/yashab.alam)
  [![LinkedIn](https://img.shields.io/badge/LinkedIn-%230077B5.svg?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/yashab-alam)
  
  💎 [Support This Project - Donate](DONATE.md)
  
</div>

**KaliGPT** is a production-ready, AI-powered penetration testing assistant designed specifically for Kali Linux. It reads and understands terminal output in real-time, automatically recommends the next step in the pentesting process, generates custom payloads, and can execute commands with user approval.

**Available Interfaces:**
- 🖥️ **Desktop GUI** - Modern Tkinter-based interface
- 🌐 **Web GUI** - Flask-powered web interface
- 💻 **CLI** - Command-line interface for terminal users

## ✨ Features

### 🤖 AI-Powered Analysis
- **Real-time terminal output capture** using PTY/pexpect
- **Intelligent command analysis** with context awareness
- **Automatic next-step recommendations** following pentesting methodology
- **Multi-model LLM support** (GPT-4, LLaMA, Mistral, Qwen, local models)

### 🛠️ Tool Integration
Built-in parsers for popular pentesting tools:
- **Nmap** - Network scanning and service detection
- **Metasploit** - Exploitation framework integration
- **SQLmap** - SQL injection detection and exploitation
- **Nikto** - Web vulnerability scanning
- **Gobuster** - Directory/file enumeration
- **Hydra** - Password cracking
- And more...

### 💉 Payload Generation
Automatic generation of:
- SQL Injection payloads (Union, Boolean, Time-based, Error-based)
- XSS payloads (Reflected, Stored, DOM-based)
- LFI/RFI exploits
- Command injection payloads
- Reverse shells (Bash, Python, PHP, PowerShell, etc.)
- Web shells (PHP, ASP, JSP)
- Privilege escalation scripts

### 📊 Automated Reporting
Generate professional pentest reports in:
- **Markdown** - Easy to read and edit
- **HTML** - Styled, presentation-ready reports
- **JSON** - Machine-readable structured data
- **PDF** - (via HTML conversion)

### 🔄 Full Pentesting Workflow
Follows the complete methodology:
1. **Reconnaissance** - Initial information gathering
2. **Enumeration** - Service and vulnerability discovery
3. **Exploitation** - Gaining access
4. **Post-Exploitation** - Privilege escalation, lateral movement
5. **Reporting** - Automated documentation

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yashab-cyber/KaliGpt.git
cd KaliGpt

# Run the interactive installer (recommended)
chmod +x scripts/installer.sh
./scripts/installer.sh
```

**The installer will:**
- ✅ Ask you to choose your preferred interface (GUI/Web/CLI)
- ✅ Install all required dependencies
- ✅ Set up Ollama and download AI models
- ✅ Create a desktop icon and application menu entry
- ✅ Configure command-line shortcuts

**After installation:**
- 🖥️ **Desktop Icon**: Click the KaliGPT icon on your desktop or find it in Applications → Security
- 💻 **Command Line**: Run `kaligpt` from anywhere
- 🚀 **Launcher**: Run `kaligpt-launcher` to choose your interface

### Manual Installation

```bash
# Install dependencies
pip3 install -r requirements.txt

# For Desktop GUI
pip3 install pillow

# For Web GUI
pip3 install flask flask-socketio
```

### Uninstallation

```bash
# Run the uninstaller
./scripts/uninstall.sh
```

### Verify Installation

```bash
# Check model setup and dependencies
python3 scripts/verify_models.py

# This will show:
# - Installed dependencies
# - Configured API keys
# - Available local models
# - Ready-to-use AI models
```

### First Run

**Desktop GUI (Default):**
- Click the KaliGPT icon on your desktop
- Or run: `kaligpt`

**Web GUI:**
```bash
python3 ui/web_gui.py
# Open browser to http://localhost:5000
```

**Command Line:**
```bash
kaligpt
# Or directly: python3 ui/cli.py
```

## 🖥️ GUI Options

### Desktop GUI (Tkinter)

Modern desktop interface with full AI integration:

```bash
# Launch desktop GUI
python3 ui/gui.py
```

**Features:**
- 🎨 Kali Linux-inspired dark theme
- 🤖 Real-time AI analysis
- 💉 Interactive payload generator
- 📊 Visual session history
- 📝 Built-in report generation
- 🔄 Multi-tab interface

**Requirements:**
```bash
# Install GUI dependencies
pip install pillow  # For logo support
```

### Web GUI (Flask)

Browser-based interface accessible from anywhere:

```bash
# Launch web GUI
python3 ui/web_gui.py

# Access at: http://localhost:5000
```

**Features:**
- 🌐 Modern web interface
- 📱 Responsive design
- 🔌 WebSocket support for real-time updates
- 💻 Multi-device access
- 🎯 RESTful API
- 📊 Interactive dashboards

**Requirements:**
```bash
# Install web GUI dependencies
pip install flask flask-socketio
```

**Screenshots:**

<div align="center">
  <img src="public/Untitled design.png" alt="KaliGPT GUI" width="600"/>
</div>

## 📖 Usage

### Interactive Mode

```bash
# Launch interactive mode
kaligpt

# Set target
KaliGPT> target 192.168.1.100

# Run a command
KaliGPT> run nmap -sV 192.168.1.100

# AI will analyze the output and suggest next steps
# You can approve or reject recommendations

# Generate payloads
KaliGPT> payload sqli

# Get help
KaliGPT> help

# Generate report
KaliGPT> report
```

### Single Command Mode

```bash
# Execute a single command and analyze
kaligpt --command "nmap -sV 192.168.1.100"
```

### Model Selection

```bash
# Use GPT-5.1 (latest OpenAI model)
export OPENAI_API_KEY=your_key_here
kaligpt --model gpt-5.1

# Use GPT-5
kaligpt --model gpt-5

# Use Gemini 3 Pro (latest Google model)
export GOOGLE_API_KEY=your_key_here
kaligpt --model gemini-3

# Use Claude Sonnet 4.5 (latest Anthropic model)
export ANTHROPIC_API_KEY=your_key_here
kaligpt --model claude-sonnet-4.5

# Use Claude Opus 4 (most powerful)
kaligpt --model claude-opus-4

# Use local LLaMA (free, runs locally)
kaligpt --model llama

# List available models
kaligpt --list-models
```

## 🎯 Example Workflow

### Scenario: Web Application Pentesting

```bash
# 1. Set target
KaliGPT> target 192.168.1.100

# 2. Initial reconnaissance
KaliGPT> run nmap -sV -sC 192.168.1.100

# AI analyzes: Found web server on port 80
# AI recommends: Run Nikto scan

# 3. Web vulnerability scanning
KaliGPT> run nikto -h http://192.168.1.100

# AI analyzes: Found potential SQL injection
# AI recommends: Test with SQLmap

# 4. SQL injection testing
KaliGPT> run sqlmap -u "http://192.168.1.100/login.php?id=1" --dbs

# AI analyzes: SQL injection confirmed, databases found
# AI recommends: Dump database contents

# 5. Data extraction
KaliGPT> run sqlmap -u "http://192.168.1.100/login.php?id=1" -D webapp --dump

# 6. Generate report
KaliGPT> report
```

## 🏗️ Architecture

```
KaliGPT/
├── core/                    # Core functionality
│   ├── terminal_capture.py  # Real-time command capture
│   ├── ai_engine.py         # AI interaction engine
│   ├── decision_engine.py   # Tactical decision making
│   └── executor.py          # Safe command execution
│
├── parsers/                 # Tool output parsers
│   ├── nmap_parser.py
│   ├── msf_parser.py
│   ├── sqlmap_parser.py
│   ├── nikto_parser.py
│   ├── gobuster_parser.py
│   └── hydra_parser.py
│
├── payloads/               # Payload generation
│   ├── generator.py
│   └── templates/
│
├── models/                 # LLM integrations
│   ├── gpt.py
│   ├── local_llama.py
│   ├── mistral.py
│   ├── qwen.py
│   └── model_selector.py
│
├── reporting/              # Report generation
│   ├── report_builder.py
│   └── templates/
│
├── ui/                     # User interface
│   └── cli.py
│
├── config/                 # Configuration
│   ├── settings.json
│   └── model_config.json
│
└── scripts/                # Utility scripts
    └── installer.sh
```

## ⚙️ Configuration

### Model Configuration

Edit `config/model_config.json`:

```json
{
  "model_type": "llama",
  "model": "llama2",
  "temperature": 0.7,
  "max_tokens": 2000
}
```

### General Settings

Edit `config/settings.json`:

```json
{
  "general": {
    "auto_execute": false,
    "safe_mode": true
  },
  "ai": {
    "default_model": "llama",
    "temperature": 0.7
  }
}
```

## 🤖 Supported AI Models

### Cloud Models (Latest)
- **GPT-5.1** - OpenAI's latest flagship model (requires OpenAI API key)
- **GPT-5** - OpenAI's latest generation (requires OpenAI API key)
- **GPT-4** - Most capable GPT-4 model (requires OpenAI API key)
- **GPT-3.5-turbo** - Fast and cost-effective
- **Gemini 3 Pro** - Google's latest multimodal AI (requires Google API key)
- **Gemini 2.0 Pro** - Google's advanced model (requires Google API key)
- **Claude Sonnet 4.5** - Anthropic's latest flagship (requires Anthropic API key)
- **Claude Opus 4** - Anthropic's most powerful model (requires Anthropic API key)
- **Claude Sonnet 3.5** - Fast and intelligent (requires Anthropic API key)
- **Mistral** - Via Mistral AI API

### Local Models (Free, Privacy-Focused)
- **LLaMA 2** - Meta's open-source LLM (Recommended for local use)
- **LLaMA 3** - Latest version
- **Mistral** - Via Ollama
- **Qwen** - Alibaba's model

### Setting Up API Keys

```bash
# OpenAI (GPT-5.1, GPT-5, GPT-4, GPT-3.5)
export OPENAI_API_KEY=your_openai_key_here

# Google Gemini (Gemini 3 Pro, Gemini 2.0 Pro)
export GOOGLE_API_KEY=your_google_key_here

# Anthropic Claude (Sonnet 4.5, Opus 4, Sonnet 3.5)
export ANTHROPIC_API_KEY=your_anthropic_key_here

# Add to your shell profile for persistence
echo 'export OPENAI_API_KEY=your_key' >> ~/.bashrc
echo 'export GOOGLE_API_KEY=your_key' >> ~/.bashrc
echo 'export ANTHROPIC_API_KEY=your_key' >> ~/.bashrc
```

### Setting Up Local Models

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Download models
ollama pull llama2      # Recommended
ollama pull mistral     # Alternative
ollama pull llama3      # Latest

# Start Ollama
ollama serve
```

## 🔐 Security Considerations

### Safe Mode
KaliGPT runs in **safe mode** by default, blocking potentially dangerous commands:
- `rm -rf /`
- `dd if=/dev/zero`
- Fork bombs
- Filesystem formatting commands

### User Confirmation
All commands require user approval before execution (unless `--auto` flag is used).

### Logging
All commands and outputs are logged for audit purposes.

## 📝 Payload Generation Examples

### SQL Injection

```bash
KaliGPT> payload sqli
```

Generates:
- Union-based SQLi
- Boolean-based blind SQLi
- Time-based blind SQLi
- Error-based SQLi
- Authentication bypass payloads

### XSS

```bash
KaliGPT> payload xss
```

Generates:
- Reflected XSS
- Stored XSS
- DOM-based XSS
- Filter bypass techniques
- Cookie stealers
- Keyloggers

### Reverse Shells

```bash
KaliGPT> payload reverse_shell
```

Generates shells for:
- Bash
- Python
- PHP
- Netcat
- PowerShell
- Perl
- Ruby

## 📊 Report Generation

Generate comprehensive penetration testing reports:

```bash
# Markdown report
KaliGPT> report

# HTML report with styling
Select format: html

# All formats
Select format: all
```

Reports include:
- Executive Summary
- Target Information
- Findings Summary Table
- Detailed Vulnerability Descriptions
- Remediation Recommendations
- Commands Executed
- Discovered Services
- Technical Appendix

## 🧪 Testing

```bash
# Test parsers
python3 parsers/nmap_parser.py
python3 parsers/sqlmap_parser.py

# Test payload generator
python3 payloads/generator.py

# Test report builder
python3 reporting/report_builder.py
```

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Adding New Tool Parsers

1. Create `parsers/your_tool_parser.py`
2. Implement the `parse()` method
3. Add to `parsers/__init__.py`
4. Update documentation

### Adding New Payload Types

1. Add generator method to `payloads/generator.py`
2. Update payload templates if needed
3. Document the new payload type

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

**IMPORTANT:** KaliGPT is designed for **authorized penetration testing and educational purposes only**. 

- Only use on systems you have explicit permission to test
- Unauthorized access to computer systems is illegal
- The developers assume no liability for misuse
- Always follow responsible disclosure practices
- Comply with all applicable laws and regulations

## 🙏 Acknowledgments

- Built for the Kali Linux community
- Inspired by the need for AI-assisted pentesting
- Thanks to the open-source security community
- Powered by OpenAI, Meta (LLaMA), Mistral AI, and Ollama

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/yashab-cyber/KaliGpt/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yashab-cyber/KaliGpt/discussions)
- **Documentation:** [Wiki](https://github.com/yashab-cyber/KaliGpt/wiki)
- **Model Guide:** [AI Model Configuration Guide](docs/MODEL_GUIDE.md)

## 🗺️ Roadmap

- [ ] GUI/Web interface
- [ ] Plugin system for custom tools
- [ ] Team collaboration features
- [ ] Cloud workspace sync
- [ ] Advanced AI training on pentest data
- [ ] Integration with vulnerability databases (NVD, ExploitDB)
- [ ] Automated exploit chaining
- [ ] Video/screenshot capture
- [ ] Integration with bug bounty platforms

## 💎 Support This Project

KaliGPT is a free, open-source project that requires significant time and resources to develop and maintain. Your support helps us continue improving and adding new features!

### 🏆 Donation Tiers
- 🥉 **Bronze Tier**: $500 - $999
- 🥇 **Gold Tier**: $1,000 - $4,999
- 💎 **Diamond Tier**: $5,000+

Each tier comes with special recognition and benefits!

📧 **Contact for donations:** [yashabalam9@gmail.com](mailto:yashabalam9@gmail.com)

📖 **Learn more:** See [DONATE.md](DONATE.md) for complete details on donation tiers, benefits, and how to contribute.

### Other Ways to Help
⭐ Star this repository | 🐛 Report bugs | 💻 Contribute code | 📖 Improve docs | 🗣️ Spread the word

---

## 📈 Version History

### v1.1.0 (December 2025)
- ✨ Added GPT-5.1 and GPT-5 support
- ✨ Added Google Gemini 3 Pro and Gemini 2.0 Pro support
- ✨ Added Claude Sonnet 4.5, Opus 4, and Sonnet 3.5 support
- 📚 Added comprehensive Model Configuration Guide
- 🔧 Updated dependencies (google-generativeai, anthropic)
- 📝 Enhanced documentation with latest AI models

### v1.0.0 (2024)
- Initial release
- Core AI engine
- Tool parsers (Nmap, Metasploit, SQLmap, Nikto, Gobuster, Hydra)
- Payload generator
- Report builder
- Multi-model LLM support
- CLI interface

---

**Made with ❤️ for the pentesting community**

**Star ⭐ this repo if you find it useful!**