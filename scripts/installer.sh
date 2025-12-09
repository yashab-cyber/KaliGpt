#!/bin/bash
# KaliGPT Installer Script
# Installs KaliGPT and its dependencies on Kali Linux

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
echo -e "${CYAN}"
cat << "EOF"
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║   🔒 KaliGPT Installation Script                        ║
║   AI-Powered Penetration Testing Assistant              ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Check if running on Kali Linux
if [ ! -f /etc/os-release ]; then
    echo -e "${RED}Error: Cannot detect OS${NC}"
    exit 1
fi

source /etc/os-release
if [[ ! "$ID" == "kali" ]] && [[ ! "$ID_LIKE" =~ "debian" ]]; then
    echo -e "${YELLOW}Warning: This script is designed for Kali Linux${NC}"
    echo -e "${YELLOW}Detected OS: $ID${NC}"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check if running as root (needed for some installations)
if [ "$EUID" -eq 0 ]; then 
    echo -e "${YELLOW}Warning: Running as root. This is not recommended.${NC}"
    echo -e "${YELLOW}KaliGPT should be run as a regular user.${NC}"
    read -p "Continue? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Get installation directory
INSTALL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
echo -e "${BLUE}Installation directory: ${INSTALL_DIR}${NC}"
echo ""

# Ask user for preferred interface
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}  Select Your Preferred Interface:${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "  ${GREEN}1)${NC} Desktop GUI ${YELLOW}(Recommended)${NC}"
echo -e "     • Modern graphical interface"
echo -e "     • Multi-tab workspace"
echo -e "     • Visual payload generator"
echo -e "     • Desktop icon included"
echo ""
echo -e "  ${GREEN}2)${NC} Web GUI"
echo -e "     • Browser-based interface"
echo -e "     • Access from any device"
echo -e "     • Real-time updates"
echo ""
echo -e "  ${GREEN}3)${NC} CLI (Command Line)"
echo -e "     • Terminal-only interface"
echo -e "     • For automation scripts"
echo -e "     • Minimal resources"
echo ""
echo -e "  ${GREEN}4)${NC} Install All"
echo -e "     • Full installation"
echo -e "     • All interfaces available"
echo ""
read -p "Enter your choice [1-4] (default: 1): " INTERFACE_CHOICE
INTERFACE_CHOICE=${INTERFACE_CHOICE:-1}
echo ""

# Set default interface
case $INTERFACE_CHOICE in
    1)
        DEFAULT_INTERFACE="gui"
        INSTALL_GUI=true
        INSTALL_WEB=false
        INSTALL_CLI=true
        echo -e "${GREEN}✓ Desktop GUI selected (CLI included)${NC}"
        ;;
    2)
        DEFAULT_INTERFACE="web"
        INSTALL_GUI=false
        INSTALL_WEB=true
        INSTALL_CLI=true
        echo -e "${GREEN}✓ Web GUI selected (CLI included)${NC}"
        ;;
    3)
        DEFAULT_INTERFACE="cli"
        INSTALL_GUI=false
        INSTALL_WEB=false
        INSTALL_CLI=true
        echo -e "${GREEN}✓ CLI selected${NC}"
        ;;
    4)
        DEFAULT_INTERFACE="gui"
        INSTALL_GUI=true
        INSTALL_WEB=true
        INSTALL_CLI=true
        echo -e "${GREEN}✓ All interfaces will be installed${NC}"
        ;;
    *)
        echo -e "${YELLOW}Invalid choice, defaulting to Desktop GUI${NC}"
        DEFAULT_INTERFACE="gui"
        INSTALL_GUI=true
        INSTALL_WEB=false
        INSTALL_CLI=true
        ;;
esac
echo ""

# Update package list
echo -e "${GREEN}[1/7] Updating package list...${NC}"
sudo apt-get update -qq

# Install system dependencies
echo -e "${GREEN}[2/7] Installing system dependencies...${NC}"
SYSTEM_PACKAGES="python3 python3-pip python3-venv git curl wget"

# Add GUI dependencies if needed
if [ "$INSTALL_GUI" = true ]; then
    SYSTEM_PACKAGES="$SYSTEM_PACKAGES python3-tk"
fi

# Add pentesting tools
SYSTEM_PACKAGES="$SYSTEM_PACKAGES nmap nikto gobuster hydra sqlmap metasploit-framework"

sudo apt-get install -y $SYSTEM_PACKAGES > /dev/null 2>&1

echo -e "${GREEN}✓ System dependencies installed${NC}"

# Install Python dependencies
echo -e "${GREEN}[3/7] Installing Python dependencies...${NC}"
pip3 install -q --upgrade pip

# Core dependencies
PYTHON_PACKAGES="pexpect rich requests openai google-generativeai anthropic weasyprint markdown"

# Add GUI dependencies
if [ "$INSTALL_GUI" = true ]; then
    PYTHON_PACKAGES="$PYTHON_PACKAGES pillow"
fi

# Add Web GUI dependencies
if [ "$INSTALL_WEB" = true ]; then
    PYTHON_PACKAGES="$PYTHON_PACKAGES flask flask-socketio python-socketio eventlet"
fi

pip3 install -q $PYTHON_PACKAGES

echo -e "${GREEN}✓ Python dependencies installed${NC}"

# Install Ollama (for local LLM)
echo -e "${GREEN}[4/7] Installing Ollama (local LLM runtime)...${NC}"
if ! command -v ollama &> /dev/null; then
    echo "Installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
    echo -e "${GREEN}✓ Ollama installed${NC}"
else
    echo -e "${YELLOW}Ollama already installed${NC}"
fi

# Pull default LLM model
echo -e "${GREEN}[5/7] Downloading default AI model (llama2)...${NC}"
echo "This may take a few minutes..."

# Start Ollama in background if not running
if ! pgrep -x "ollama" > /dev/null; then
    echo "Starting Ollama service..."
    ollama serve &> /dev/null &
    sleep 3
fi

# Pull llama2 model
if ! ollama list | grep -q "llama2"; then
    ollama pull llama2
    echo -e "${GREEN}✓ llama2 model downloaded${NC}"
else
    echo -e "${YELLOW}llama2 model already downloaded${NC}"
fi

# Create necessary directories
echo -e "${GREEN}[6/7] Setting up KaliGPT...${NC}"
cd "$INSTALL_DIR"
mkdir -p logs reports sessions

# Make scripts executable
chmod +x ui/cli.py
chmod +x launch.sh

# Create bin directory
BIN_DIR="$HOME/.local/bin"
mkdir -p "$BIN_DIR"

# Create wrapper scripts based on selected interface
if [ "$DEFAULT_INTERFACE" = "gui" ]; then
    cat > "$BIN_DIR/kaligpt" << EOL
#!/bin/bash
cd "$INSTALL_DIR" && python3 ui/gui.py "\$@"
EOL
elif [ "$DEFAULT_INTERFACE" = "web" ]; then
    cat > "$BIN_DIR/kaligpt" << EOL
#!/bin/bash
cd "$INSTALL_DIR" && python3 ui/web_gui.py "\$@"
EOL
else
    cat > "$BIN_DIR/kaligpt" << EOL
#!/bin/bash
cd "$INSTALL_DIR" && python3 ui/cli.py "\$@"
EOL
fi

chmod +x "$BIN_DIR/kaligpt"

# Create launcher script for all interfaces
cat > "$BIN_DIR/kaligpt-launcher" << EOL
#!/bin/bash
cd "$INSTALL_DIR" && ./launch.sh
EOL
chmod +x "$BIN_DIR/kaligpt-launcher"

echo -e "${GREEN}✓ KaliGPT configured${NC}"

# Create desktop integration
echo -e "${GREEN}[7/7] Creating desktop integration...${NC}"

# Create .desktop file
DESKTOP_FILE="$HOME/.local/share/applications/kaligpt.desktop"
mkdir -p "$HOME/.local/share/applications"

cat > "$DESKTOP_FILE" << EOL
[Desktop Entry]
Version=1.2.0
Type=Application
Name=KaliGPT
GenericName=AI-Powered Penetration Testing Assistant
Comment=AI-powered penetration testing with multiple interfaces
Exec=$BIN_DIR/kaligpt
Icon=$INSTALL_DIR/public/Untitled design.png
Terminal=false
Categories=Security;Network;
Keywords=pentest;hacking;security;ai;gpt;
StartupNotify=true
EOL

# Also create launcher version
LAUNCHER_DESKTOP_FILE="$HOME/.local/share/applications/kaligpt-launcher.desktop"
cat > "$LAUNCHER_DESKTOP_FILE" << EOL
[Desktop Entry]
Version=1.2.0
Type=Application
Name=KaliGPT Launcher
GenericName=KaliGPT Interface Selector
Comment=Choose KaliGPT interface (GUI/Web/CLI)
Exec=$BIN_DIR/kaligpt-launcher
Icon=$INSTALL_DIR/public/Untitled design.png
Terminal=true
Categories=Security;Network;
Keywords=pentest;hacking;security;ai;gpt;
StartupNotify=true
EOL

# Make desktop files executable
chmod +x "$DESKTOP_FILE"
chmod +x "$LAUNCHER_DESKTOP_FILE"

# Copy to Desktop if it exists
if [ -d "$HOME/Desktop" ]; then
    cp "$DESKTOP_FILE" "$HOME/Desktop/"
    chmod +x "$HOME/Desktop/kaligpt.desktop"
    
    # Try to trust the desktop file (for some desktop environments)
    if command -v gio &> /dev/null; then
        gio set "$HOME/Desktop/kaligpt.desktop" "metadata::trusted" true 2>/dev/null || true
    fi
    
    echo -e "${GREEN}✓ Desktop icon created${NC}"
fi

# Update desktop database
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database "$HOME/.local/share/applications" 2>/dev/null || true
fi

# Add to PATH if not already there
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo ""
    echo -e "${YELLOW}Add the following to your ~/.bashrc or ~/.zshrc:${NC}"
    echo -e "${YELLOW}export PATH=\"\$HOME/.local/bin:\$PATH\"${NC}"
fi

echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}   Installation Complete! 🎉${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${BLUE}🔒 KaliGPT v1.2.0 - AI-Powered Penetration Testing${NC}"
echo ""

# Show launch instructions based on installed interfaces
echo -e "${CYAN}━━━ Launch Methods ━━━${NC}"
echo ""

if [ "$INSTALL_GUI" = true ]; then
    echo -e "${GREEN}📱 Desktop GUI:${NC}"
    echo -e "  • Click the KaliGPT icon on your desktop"
    echo -e "  • Or find it in Applications → Security → KaliGPT"
    echo -e "  • Or run: ${YELLOW}kaligpt${NC}"
    echo ""
fi

if [ "$INSTALL_WEB" = true ]; then
    echo -e "${GREEN}🌐 Web GUI:${NC}"
    echo -e "  • Run: ${YELLOW}cd $INSTALL_DIR && python3 ui/web_gui.py${NC}"
    echo -e "  • Open browser to: ${YELLOW}http://localhost:5000${NC}"
    echo ""
fi

if [ "$INSTALL_CLI" = true ]; then
    echo -e "${GREEN}💻 Command Line:${NC}"
    echo -e "  • Run: ${YELLOW}cd $INSTALL_DIR && python3 ui/cli.py${NC}"
    echo ""
fi

echo -e "${GREEN}🚀 Quick Launcher (All Interfaces):${NC}"
echo -e "  • Run: ${YELLOW}kaligpt-launcher${NC}"
echo -e "  • Or: ${YELLOW}cd $INSTALL_DIR && ./launch.sh${NC}"
echo ""

echo -e "${CYAN}━━━ Configuration ━━━${NC}"
echo ""
echo -e "${GREEN}Set up your API keys (optional):${NC}"
echo ""
echo -e "  ${YELLOW}OpenAI (GPT-5.1, GPT-5, GPT-4):${NC}"
echo -e "    export OPENAI_API_KEY=your_api_key"
echo ""
echo -e "  ${YELLOW}Google Gemini (Gemini 3 Pro, Gemini 2.0 Pro):${NC}"
echo -e "    export GOOGLE_API_KEY=your_api_key"
echo ""
echo -e "  ${YELLOW}Anthropic Claude (Sonnet 4.5, Opus 4):${NC}"
echo -e "    export ANTHROPIC_API_KEY=your_api_key"
echo ""

echo -e "${GREEN}📚 Additional local models:${NC}"
echo -e "  ollama pull mistral"
echo -e "  ollama pull llama3"
echo -e "  ollama pull qwen"
echo ""

echo -e "${CYAN}━━━ Resources ━━━${NC}"
echo ""
echo -e "  📖 Documentation: ${YELLOW}$INSTALL_DIR/docs/${NC}"
echo -e "  🐛 Report Issues: ${YELLOW}https://github.com/yashab-cyber/KaliGpt/issues${NC}"
echo -e "  💡 Quick Start: ${YELLOW}$INSTALL_DIR/docs/GUI_QUICKSTART.md${NC}"
echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${GREEN}Happy Hacking! 🔒${NC}"
echo ""
