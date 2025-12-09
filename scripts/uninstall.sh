#!/bin/bash
# KaliGPT Uninstaller Script

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}"
cat << "EOF"
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║   🔒 KaliGPT Uninstaller                                ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo -e "${YELLOW}This will remove KaliGPT from your system.${NC}"
echo -e "${YELLOW}Your session files and reports will be preserved.${NC}"
echo ""
read -p "Are you sure you want to uninstall? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${GREEN}Uninstallation cancelled.${NC}"
    exit 0
fi

echo ""
echo -e "${CYAN}Removing KaliGPT...${NC}"
echo ""

# Remove desktop files
echo -e "${GREEN}[1/4] Removing desktop integration...${NC}"

if [ -f "$HOME/.local/share/applications/kaligpt.desktop" ]; then
    rm "$HOME/.local/share/applications/kaligpt.desktop"
    echo -e "${GREEN}✓ Removed application menu entry${NC}"
fi

if [ -f "$HOME/.local/share/applications/kaligpt-launcher.desktop" ]; then
    rm "$HOME/.local/share/applications/kaligpt-launcher.desktop"
    echo -e "${GREEN}✓ Removed launcher menu entry${NC}"
fi

if [ -f "$HOME/Desktop/kaligpt.desktop" ]; then
    rm "$HOME/Desktop/kaligpt.desktop"
    echo -e "${GREEN}✓ Removed desktop icon${NC}"
fi

# Update desktop database
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database "$HOME/.local/share/applications" 2>/dev/null || true
fi

# Remove bin scripts
echo -e "${GREEN}[2/4] Removing command-line tools...${NC}"

if [ -f "$HOME/.local/bin/kaligpt" ]; then
    rm "$HOME/.local/bin/kaligpt"
    echo -e "${GREEN}✓ Removed kaligpt command${NC}"
fi

if [ -f "$HOME/.local/bin/kaligpt-launcher" ]; then
    rm "$HOME/.local/bin/kaligpt-launcher"
    echo -e "${GREEN}✓ Removed kaligpt-launcher command${NC}"
fi

# Ask about Python packages
echo -e "${GREEN}[3/4] Python packages...${NC}"
echo ""
echo -e "${YELLOW}Remove Python packages? (pillow, flask, etc.)${NC}"
read -p "This may affect other applications. Remove? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    pip3 uninstall -y pillow flask flask-socketio python-socketio eventlet 2>/dev/null || true
    echo -e "${GREEN}✓ Python packages removed${NC}"
else
    echo -e "${YELLOW}Python packages kept${NC}"
fi

# Ask about Ollama
echo -e "${GREEN}[4/4] Ollama...${NC}"
echo ""
echo -e "${YELLOW}Remove Ollama and AI models?${NC}"
echo -e "${YELLOW}This will delete all downloaded models (llama2, mistral, etc.)${NC}"
read -p "Remove Ollama? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if command -v ollama &> /dev/null; then
        # Stop Ollama service
        sudo systemctl stop ollama 2>/dev/null || true
        sudo systemctl disable ollama 2>/dev/null || true
        
        # Remove Ollama
        sudo rm -f /usr/local/bin/ollama
        sudo rm -rf /usr/share/ollama
        rm -rf ~/.ollama
        
        echo -e "${GREEN}✓ Ollama removed${NC}"
    else
        echo -e "${YELLOW}Ollama not installed${NC}"
    fi
else
    echo -e "${YELLOW}Ollama kept${NC}"
fi

echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}   Uninstallation Complete!${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${YELLOW}Note: The KaliGPT directory has not been removed.${NC}"
echo -e "${YELLOW}Your session files, reports, and logs are preserved.${NC}"
echo ""
echo -e "${CYAN}To completely remove KaliGPT:${NC}"
INSTALL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
echo -e "  ${RED}rm -rf $INSTALL_DIR${NC}"
echo ""
echo -e "${GREEN}To reinstall KaliGPT:${NC}"
echo -e "  Run the installer script again"
echo ""
