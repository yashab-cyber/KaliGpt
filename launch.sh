#!/bin/bash
# KaliGPT Launcher Script

# Colors
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Banner
echo -e "${CYAN}"
cat << "EOF"
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║   🔒 KaliGPT - AI-Powered Penetration Testing           ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Check if running in KaliGPT directory
if [ ! -f "kaligpt.py" ]; then
    echo -e "${RED}Error: Please run this script from the KaliGPT root directory${NC}"
    exit 1
fi

# Function to check dependencies
check_dependencies() {
    echo -e "${YELLOW}Checking dependencies...${NC}"
    
    if ! python3 -c "import tkinter" 2>/dev/null; then
        echo -e "${YELLOW}Warning: tkinter not found. Desktop GUI may not work.${NC}"
    fi
    
    if ! python3 -c "import flask" 2>/dev/null; then
        echo -e "${YELLOW}Warning: flask not found. Web GUI may not work.${NC}"
        echo -e "${YELLOW}Install with: pip install flask flask-socketio${NC}"
    fi
    
    echo -e "${GREEN}Dependency check complete${NC}"
    echo
}

# Menu
echo -e "${GREEN}Select interface:${NC}"
echo "1) Desktop GUI (Tkinter)"
echo "2) Web GUI (Flask)"
echo "3) CLI (Command Line)"
echo "4) Check Dependencies"
echo "5) Exit"
echo

read -p "Enter choice [1-5]: " choice

case $choice in
    1)
        echo -e "${CYAN}Launching Desktop GUI...${NC}"
        python3 ui/gui.py
        ;;
    2)
        echo -e "${CYAN}Launching Web GUI...${NC}"
        echo -e "${GREEN}Access at: http://localhost:5000${NC}"
        python3 ui/web_gui.py
        ;;
    3)
        echo -e "${CYAN}Launching CLI...${NC}"
        python3 ui/cli.py
        ;;
    4)
        check_dependencies
        ;;
    5)
        echo -e "${GREEN}Goodbye!${NC}"
        exit 0
        ;;
    *)
        echo -e "${RED}Invalid choice${NC}"
        exit 1
        ;;
esac
