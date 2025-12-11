# KaliGPT Installation Guide

**Created by Yashab Alam** | [Instagram](https://www.instagram.com/yashab.alam) | [LinkedIn](https://www.linkedin.com/in/yashab-alam) | [💎 Donate](../DONATE.md)

Complete installation guide for KaliGPT with desktop integration.

## Installation Methods

### Method 1: Interactive Installer (Recommended)

The interactive installer provides the easiest way to install KaliGPT with desktop integration.

```bash
# Clone repository
git clone https://github.com/yashab-cyber/KaliGpt.git
cd KaliGpt

# Run installer
chmod +x scripts/installer.sh
./scripts/installer.sh
```

### Installation Steps

The installer will guide you through:

```
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║   🔒 KaliGPT Installation Script                        ║
║   AI-Powered Penetration Testing Assistant              ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Select Your Preferred Interface:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  1) Desktop GUI (Recommended)
     • Modern graphical interface
     • Multi-tab workspace
     • Visual payload generator
     • Desktop icon included

  2) Web GUI
     • Browser-based interface
     • Access from any device
     • Real-time updates

  3) CLI (Command Line)
     • Terminal-only interface
     • For automation scripts
     • Minimal resources

  4) Install All
     • Full installation
     • All interfaces available

Enter your choice [1-4] (default: 1):
```

### What Gets Installed

#### For All Options:
- ✅ Python 3 and pip
- ✅ Core Python packages (pexpect, rich, requests)
- ✅ AI libraries (openai, google-generativeai, anthropic)
- ✅ Pentesting tools (nmap, nikto, gobuster, hydra, sqlmap)
- ✅ Ollama with llama2 model
- ✅ Command-line shortcuts

#### Additional for Desktop GUI:
- ✅ Python Tkinter (python3-tk)
- ✅ Pillow for image support
- ✅ Desktop icon on desktop
- ✅ Application menu entry in Security category
- ✅ Quick launcher

#### Additional for Web GUI:
- ✅ Flask web framework
- ✅ Flask-SocketIO for real-time updates
- ✅ Eventlet async server

## Desktop Integration

### Desktop Icon

After installation, you'll find:

**On Desktop:**
```
┌─────────────────┐
│                 │
│   [KaliGPT]     │
│     LOGO        │
│                 │
└─────────────────┘
KaliGPT
```

**In Application Menu:**
```
Applications → Security → KaliGPT
Applications → Security → KaliGPT Launcher
```

**Location of .desktop files:**
- `~/.local/share/applications/kaligpt.desktop` - Main application
- `~/.local/share/applications/kaligpt-launcher.desktop` - Interface selector
- `~/Desktop/kaligpt.desktop` - Desktop shortcut

### Desktop File Contents

The installer creates a proper `.desktop` file:

```ini
[Desktop Entry]
Version=1.2.0
Type=Application
Name=KaliGPT
GenericName=AI-Powered Penetration Testing Assistant
Comment=AI-powered penetration testing with multiple interfaces
Exec=/home/user/.local/bin/kaligpt
Icon=/path/to/KaliGpt/public/Untitled design.png
Terminal=false
Categories=Security;Network;
Keywords=pentest;hacking;security;ai;gpt;
StartupNotify=true
```

## Command-Line Shortcuts

The installer creates these commands:

### `kaligpt`
Launches your default interface (GUI/Web/CLI based on installation choice)

```bash
kaligpt
```

### `kaligpt-launcher`
Opens an interactive menu to choose interface

```bash
kaligpt-launcher
```

Output:
```
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║   🔒 KaliGPT - AI-Powered Penetration Testing           ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝

Select interface:
1) Desktop GUI (Tkinter)
2) Web GUI (Flask)
3) CLI (Command Line)
4) Check Dependencies
5) Exit

Enter choice [1-5]:
```

## Launch Methods Summary

| Method | Command | Interface | Notes |
|--------|---------|-----------|-------|
| Desktop Icon | Click icon | Default (usually GUI) | Easiest |
| App Menu | Applications → Security → KaliGPT | Default | Standard |
| Command | `kaligpt` | Default | Quick access |
| Launcher | `kaligpt-launcher` | Choose | Interactive |
| Direct GUI | `python3 ui/gui.py` | Desktop GUI | Manual |
| Direct Web | `python3 ui/web_gui.py` | Web GUI | Manual |
| Direct CLI | `python3 ui/cli.py` | CLI | Manual |
| Launch Script | `./launch.sh` | Choose | From repo |

## Post-Installation

### Set Up API Keys

```bash
# OpenAI (GPT-5.1, GPT-5, GPT-4)
export OPENAI_API_KEY="your-openai-key"

# Google Gemini (Gemini 3 Pro, Gemini 2.0 Pro)
export GOOGLE_API_KEY="your-google-key"

# Anthropic Claude (Sonnet 4.5, Opus 4)
export ANTHROPIC_API_KEY="your-anthropic-key"

# Add to ~/.bashrc to make permanent
echo 'export OPENAI_API_KEY="your-key"' >> ~/.bashrc
```

### Download Additional Models

```bash
# Mistral - Fast and efficient
ollama pull mistral

# LLaMA 3 - Latest Meta model
ollama pull llama3

# Qwen - Multilingual support
ollama pull qwen
```

### Verify Installation

```bash
# Run verification script
python3 scripts/verify_models.py
```

Expected output:
```
╔══════════════════════════════════════════════════════════╗
║   KaliGPT Model Verification                            ║
╚══════════════════════════════════════════════════════════╝

✓ Dependencies installed
✓ Ollama running
✓ Local models available: llama2
✓ API keys configured: OPENAI_API_KEY

Ready to use:
  • GPT-5.1 (OpenAI)
  • llama2 (Local)
```

## Troubleshooting

### Desktop Icon Not Showing

**Problem:** Icon doesn't appear on desktop

**Solution:**
```bash
# Refresh desktop database
update-desktop-database ~/.local/share/applications

# Mark as trusted (GNOME)
gio set ~/Desktop/kaligpt.desktop "metadata::trusted" true

# Make executable
chmod +x ~/Desktop/kaligpt.desktop
```

### Command Not Found: kaligpt

**Problem:** `kaligpt` command not found

**Solution:**
```bash
# Add to PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Verify
which kaligpt
```

### Desktop GUI Won't Start

**Problem:** GUI fails to launch

**Solution:**
```bash
# Install tkinter
sudo apt install python3-tk

# Install Pillow
pip3 install pillow

# Test directly
python3 ui/gui.py
```

### Web GUI Port Already in Use

**Problem:** Port 5000 already in use

**Solution:**
```bash
# Use different port
python3 ui/web_gui.py --port 8080

# Or kill existing process
lsof -ti:5000 | xargs kill -9
```

### Logo Not Displaying

**Problem:** Logo missing in GUI

**Solution:**
```bash
# Verify logo exists
ls -la public/*.png

# Install Pillow
pip3 install --upgrade pillow
```

## Uninstallation

### Using Uninstaller Script

```bash
# Run uninstaller
./scripts/uninstall.sh
```

The uninstaller will:
1. Remove desktop icons and menu entries
2. Remove command-line shortcuts
3. Ask about removing Python packages
4. Ask about removing Ollama and models
5. Preserve your session files and reports

### Manual Uninstallation

```bash
# Remove desktop files
rm ~/.local/share/applications/kaligpt*.desktop
rm ~/Desktop/kaligpt.desktop

# Remove commands
rm ~/.local/bin/kaligpt*

# Update desktop database
update-desktop-database ~/.local/share/applications

# Remove repository (optional)
rm -rf ~/KaliGpt
```

## Reinstallation

To reinstall after uninstalling:

```bash
# Navigate to KaliGPT directory
cd KaliGpt

# Run installer again
./scripts/installer.sh

# Your session files and reports will be preserved
```

## Advanced Installation

### Custom Installation Directory

```bash
# Clone to custom location
git clone https://github.com/yashab-cyber/KaliGpt.git /opt/kaligpt
cd /opt/kaligpt

# Run installer
./scripts/installer.sh
```

### Silent Installation

For automation:

```bash
# Auto-select GUI and skip prompts
echo "1" | ./scripts/installer.sh
```

### Development Installation

```bash
# Install in development mode
pip3 install -e .

# Run tests
python3 -m pytest tests/
```

## System Requirements

### Minimum:
- **OS:** Kali Linux / Debian-based Linux
- **Python:** 3.10+
- **RAM:** 2GB (4GB for local models)
- **Disk:** 5GB free space
- **Network:** Internet for API-based models

### Recommended:
- **OS:** Kali Linux latest
- **Python:** 3.11+
- **RAM:** 8GB
- **Disk:** 20GB free space
- **GPU:** Optional (for faster local models)

## Support

- **Installation Issues:** https://github.com/yashab-cyber/KaliGpt/issues
- **Documentation:** https://github.com/yashab-cyber/KaliGpt/docs
- **Quick Start:** docs/GUI_QUICKSTART.md

---

**Ready to install? Run `./scripts/installer.sh` now! 🔒**
