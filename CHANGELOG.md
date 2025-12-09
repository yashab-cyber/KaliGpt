# Changelog

All notable changes to KaliGPT will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2025-12-09

### Added - Graphical User Interfaces
- **Desktop GUI** - Modern Tkinter-based desktop application
  - Kali Linux-inspired dark theme
  - Multi-tab interface (Terminal, Payloads, History, Reports)
  - Real-time AI analysis with threading
  - Visual payload generator
  - Session save/load functionality
  - Integrated report generation
  
- **Web GUI** - Flask-powered web interface
  - Responsive modern web design
  - WebSocket support for real-time updates
  - RESTful API endpoints
  - Multi-device access capability
  - Interactive dashboards
  - Browser-based accessibility

- **Launch Script** - `launch.sh` for easy interface selection
- **GUI Documentation** - `ui/README.md` with complete guides
- **Logo Integration** - KaliGPT logo in header and README

### Added - Enhanced Installation System
- **Interactive Installer** - User chooses preferred interface during installation
  - Desktop GUI (default, recommended)
  - Web GUI option
  - CLI option
  - Install All option
  
- **Desktop Integration**
  - Desktop icon created automatically
  - Application menu entry in Security category
  - Launcher app for interface selection
  - Proper .desktop file with icon
  - Trusted desktop shortcut on installation

- **Command-Line Shortcuts**
  - `kaligpt` - Launch default interface
  - `kaligpt-launcher` - Interactive interface selector
  - Automatic PATH configuration

- **Uninstaller Script** - `scripts/uninstall.sh`
  - Clean removal of desktop files
  - Optional removal of Python packages
  - Optional removal of Ollama
  - Preserves session files and reports

- **Installation Documentation** - `docs/INSTALLATION.md`
  - Complete installation guide
  - Troubleshooting section
  - Desktop integration details
  - Uninstallation guide

### Added - Payload Template System
- **Template Library** - Comprehensive JSON-based templates
  - `shells/` - 16 reverse shell types
  - `webshells/` - 9 PHP web shell variants
  - `exploits/` - SQL injection and XSS payloads
  - `privesc/` - Linux and Windows privilege escalation
  - `wordlists/` - 8 intelligent wordlist generators

- **AI-Powered Payload Generation** - Context-aware payload creation
- **Variable Substitution** - Dynamic payload customization
- **Payload Documentation** - `payloads/README.md` with examples

### Enhanced
- Updated `requirements.txt` with GUI dependencies
- Added Pillow for image support
- Added Flask, Flask-SocketIO for web interface
- Logo now displayed in README.md and GUIs
- Enhanced payload generator with template loading
- Installer now creates proper desktop integration
- Default interface is Desktop GUI for best user experience

### Changed
- Repository URLs updated throughout documentation
- README.md restructured with GUI sections and installation details
- Added visual screenshots section
- Installer now asks for interface preference
- Desktop icon created by default on GUI installation

## [1.1.0] - 2025-12-09

### Added - Latest AI Models
- **GPT-5.1 Support** - OpenAI's latest flagship model with enhanced reasoning
- **GPT-5 Support** - OpenAI's newest generation model
- **Google Gemini 3 Pro** - Latest multimodal AI with 2M token context
- **Google Gemini 2.0 Pro** - Advanced model with 1M token context
- **Claude Sonnet 4.5** - Anthropic's latest and fastest model
- **Claude Opus 4** - Anthropic's most powerful model
- **Claude Sonnet 3.5** - Fast and intelligent Claude variant

### Added - New Model Infrastructure
- `models/gemini.py` - Google Gemini model implementation
- `models/anthropic_claude.py` - Anthropic Claude model implementation
- Model streaming support for Gemini and Claude
- Automatic model name mapping for API compatibility
- Enhanced error handling for all new models

### Added - Documentation
- `docs/MODELS.md` - Comprehensive model comparison and selection guide
- `docs/MODEL_GUIDE.md` - Detailed configuration guide for all models
- `docs/QUICKSTART.md` - Quick start guide featuring latest models
- `scripts/verify_models.py` - Model verification and testing script

### Changed - Configuration
- Updated `config/model_config.json` with profiles for all new models
- Enhanced `models/model_selector.py` with new model mappings
- Updated `models/gpt.py` default to GPT-5.1
- Increased default max_tokens to 4000 for new models

### Changed - Dependencies
- Added `google-generativeai>=0.3.0` for Gemini support
- Added `anthropic>=0.25.0` for Claude support
- Updated `requirements.txt` with new dependencies
- Updated `scripts/installer.sh` to install new packages

### Changed - Documentation
- Updated README.md with latest model information
- Enhanced model selection examples
- Added API key setup instructions for Google and Anthropic
- Updated roadmap and version history

### Technical Details

#### Model Support Matrix

| Model Family | Models | Context | Status |
|--------------|--------|---------|--------|
| OpenAI GPT | GPT-5.1, GPT-5, GPT-4, GPT-3.5 | 128K | ✅ Full Support |
| Google Gemini | Gemini 3 Pro, Gemini 2.0 Pro | 2M/1M | ✅ Full Support |
| Anthropic Claude | Sonnet 4.5, Opus 4, Sonnet 3.5 | 200K | ✅ Full Support |
| Meta LLaMA | LLaMA 3, LLaMA 2 | 8K | ✅ Full Support |
| Mistral | Mistral 7B | 8K | ✅ Full Support |
| Qwen | Qwen 7B/14B | 8K | ✅ Full Support |

#### API Compatibility

- OpenAI API: Compatible with GPT-5.1, GPT-5, GPT-4, GPT-3.5-turbo
- Google AI Studio: Compatible with Gemini 3 Pro, Gemini 2.0 Pro
- Anthropic API: Compatible with Claude Sonnet 4.5, Opus 4, Sonnet 3.5
- Ollama: Compatible with LLaMA, Mistral, Qwen

#### Environment Variables

New environment variable support:
- `OPENAI_API_KEY` - For GPT models
- `GOOGLE_API_KEY` / `GEMINI_API_KEY` - For Gemini models
- `ANTHROPIC_API_KEY` / `CLAUDE_API_KEY` - For Claude models

## [1.0.0] - 2024-12-01

### Added - Initial Release

#### Core Features
- **AI-Powered Analysis Engine** - Real-time terminal output understanding
- **Smart Terminal Capture** - PTY/pexpect-based command monitoring
- **Decision Engine** - Tactical pentesting recommendations
- **Command Executor** - Safe command execution with user approval

#### Tool Parsers
- **Nmap Parser** - Network scanning and service detection
- **Metasploit Parser** - Exploitation framework integration
- **SQLmap Parser** - SQL injection detection and exploitation
- **Nikto Parser** - Web vulnerability scanning
- **Gobuster Parser** - Directory/file enumeration
- **Hydra Parser** - Password cracking results

#### Payload Generation
- SQL Injection (Union, Boolean, Time-based, Error-based)
- XSS (Reflected, Stored, DOM-based)
- LFI/RFI exploits
- Command injection payloads
- Reverse shells (Bash, Python, PHP, PowerShell, Netcat, Perl, Ruby)
- Web shells (PHP, ASP, JSP)
- Privilege escalation scripts
- SSTI, XXE, CSRF payloads

#### AI Models (v1.0)
- OpenAI GPT-4
- OpenAI GPT-3.5-turbo
- LLaMA 2 (local via Ollama)
- LLaMA 3 (local via Ollama)
- Mistral (API and local)
- Qwen (local via Ollama)

#### Reporting
- Markdown report generation
- HTML report with CSS styling
- JSON structured export
- PDF generation (via HTML conversion)
- Executive summaries
- Severity-based findings categorization

#### User Interface
- Rich CLI with color support
- Interactive command mode
- Single command mode
- Progress indicators
- Formatted tables and panels
- Command history
- Help system

#### Configuration
- JSON-based configuration
- Model profiles
- Safety settings
- Workflow customization
- Tool configurations

#### Installation & Setup
- Automated installer script
- Dependency management
- PATH integration
- Ollama integration
- Model download automation

#### Documentation
- Comprehensive README
- Installation guide
- Usage examples
- Architecture documentation
- Contributing guidelines
- MIT License with security disclaimer

### Infrastructure

#### Project Structure
```
KaliGPT/
├── core/           # Core functionality
├── parsers/        # Tool output parsers
├── payloads/       # Payload generation
├── models/         # LLM integrations
├── reporting/      # Report generation
├── ui/             # User interface
├── config/         # Configuration files
├── scripts/        # Utility scripts
├── docs/           # Documentation
└── tests/          # Test suite
```

#### Dependencies
- Python 3.10+
- pexpect>=4.8.0
- requests>=2.31.0
- rich>=13.0.0
- openai>=1.0.0
- markdown>=3.5.0
- weasyprint>=60.0

#### Security Features
- Safe mode (blocks dangerous commands)
- User confirmation for all commands
- Command logging and audit trails
- Session management
- Privacy-focused local model option

---

## Version Numbering

KaliGPT follows [Semantic Versioning](https://semver.org/):

- **MAJOR** version: Incompatible API changes
- **MINOR** version: New functionality (backwards compatible)
- **PATCH** version: Bug fixes (backwards compatible)

## Release Types

- **Stable**: Production-ready releases (e.g., 1.0.0, 1.1.0)
- **Beta**: Feature-complete pre-releases (e.g., 1.1.0-beta.1)
- **Alpha**: Early testing releases (e.g., 1.1.0-alpha.1)

## Upgrade Guide

### From 1.0.0 to 1.1.0

1. **Update KaliGPT**
   ```bash
   git pull origin main
   ```

2. **Install new dependencies**
   ```bash
   pip3 install -r requirements.txt --upgrade
   ```

3. **Set up new API keys (optional)**
   ```bash
   export GOOGLE_API_KEY=your_key
   export ANTHROPIC_API_KEY=your_key
   ```

4. **Verify installation**
   ```bash
   python3 scripts/verify_models.py
   ```

5. **Start using new models**
   ```bash
   kaligpt --model gemini-3
   kaligpt --model claude-sonnet-4.5
   kaligpt --model gpt-5.1
   ```

### Breaking Changes

None in v1.1.0 - fully backwards compatible with v1.0.0

### Deprecation Notices

None in this release

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Reporting bugs
- Suggesting enhancements
- Submitting pull requests
- Development workflow

## Support

- **Issues**: [GitHub Issues](https://github.com/yashab-cyber/KaliGpt/issues)
- **Security**: See [SECURITY.md](SECURITY.md) for reporting vulnerabilities

---

**Legend:**
- ✅ Completed
- 🚧 In Progress
- 📋 Planned
- ❌ Deprecated
