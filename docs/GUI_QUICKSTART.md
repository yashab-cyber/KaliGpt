# KaliGPT GUI Quick Start Guide

Get up and running with KaliGPT's graphical interfaces in minutes!

## Prerequisites

```bash
# Ensure you have Python 3.10+
python3 --version

# Install KaliGPT
git clone https://github.com/yashab-cyber/KaliGpt.git
cd KaliGpt

# Install all dependencies
pip install -r requirements.txt
```

## Set Up API Keys

```bash
# For OpenAI models (GPT-5, GPT-5.1)
export OPENAI_API_KEY="your-api-key-here"

# For Google models (Gemini 3, Gemini 2)
export GOOGLE_API_KEY="your-api-key-here"

# For Anthropic models (Claude Sonnet 4.5, Opus 4)
export ANTHROPIC_API_KEY="your-api-key-here"
```

## Launch Options

### Option 1: Use Launch Script (Recommended)

```bash
./launch.sh
```

Select your preferred interface:
1. Desktop GUI
2. Web GUI
3. CLI

### Option 2: Direct Launch

**Desktop GUI:**
```bash
python3 ui/gui.py
```

**Web GUI:**
```bash
python3 ui/web_gui.py
# Open browser to http://localhost:5000
```

**CLI:**
```bash
python3 ui/cli.py
```

## First Steps

### Desktop GUI

1. **Connect to AI**
   - Select model from dropdown (e.g., "gpt-5.1")
   - Click "🔌 Connect to AI"
   - Wait for green status indicator

2. **Analyze Command Output**
   - Switch to "Terminal" tab
   - Paste command output (e.g., nmap results)
   - Click "🤖 Analyze with AI"
   - View recommendations

3. **Generate Payload**
   - Switch to "Payloads" tab
   - Select payload type (e.g., "sqli")
   - Choose template
   - Edit variables in JSON
   - Click "🚀 Generate Payload"

4. **Create Report**
   - Switch to "Report" tab
   - Select format (Markdown/HTML/JSON)
   - Click "🔄 Generate Preview"
   - Click "💾 Save Report"

### Web GUI

1. **Open Browser**
   - Navigate to http://localhost:5000
   - You'll see the KaliGPT dashboard

2. **Configure AI**
   - In left sidebar, select AI model
   - Click "🔌 Connect to AI"
   - Wait for status: "Connected"

3. **Run Analysis**
   - Click "Terminal" tab
   - Paste command output
   - Click "🤖 Analyze with AI"
   - Results appear in real-time

4. **Generate Payloads**
   - Click "Payloads" tab
   - Configure payload type and template
   - Or use AI-powered generation
   - Click "📋 Copy to Clipboard"

## Common Use Cases

### Case 1: Analyze Nmap Scan

```bash
# Run nmap scan
nmap -sV -sC 192.168.1.100 > scan.txt

# In GUI:
# 1. Paste scan.txt content
# 2. Click "Analyze with AI"
# 3. Get recommendations for next steps
```

### Case 2: Generate SQL Injection Payload

```bash
# In GUI Payloads tab:
# 1. Select "sqli" type
# 2. Choose "union_based_mysql"
# 3. Set variables:
{
  "TABLE": "users",
  "COLUMN": "password"
}
# 4. Generate and copy
```

### Case 3: Create Custom Payload with AI

```bash
# In GUI Payloads tab:
# 1. Use "AI-Powered Generation"
# 2. Enter target info:
{
  "target_type": "web_application",
  "technology": "PHP/MySQL",
  "vulnerability": "SQL Injection",
  "context": "Login form, WAF enabled",
  "objective": "Extract admin hash"
}
# 3. AI generates custom payload
```

### Case 4: Generate Pentest Report

```bash
# After completing analysis:
# 1. Go to "Report" tab
# 2. Enter target name
# 3. Select format (Markdown recommended)
# 4. Generate preview
# 5. Export to file
```

## Tips & Tricks

### Desktop GUI

- **Keyboard Shortcuts:**
  - `Ctrl+N` - New session
  - `Ctrl+S` - Save session
  - `Ctrl+Q` - Quit

- **Session Management:**
  - File → Save Session (keeps all history)
  - File → Load Session (restore previous work)

- **Quick Actions:**
  - Use sidebar buttons for fast access
  - Stats show session progress

### Web GUI

- **Multi-Device:**
  - Access from any browser on network
  - Use phone/tablet for monitoring

- **API Integration:**
  - Use REST endpoints in scripts
  - Automate with curl/Python

- **Real-time Updates:**
  - WebSocket keeps UI synced
  - No need to refresh page

## Troubleshooting

### "Failed to connect to AI"

```bash
# Check API key
echo $OPENAI_API_KEY

# Set if missing
export OPENAI_API_KEY="your-key"

# Verify in config
cat config/model_config.json
```

### "Module not found" errors

```bash
# Reinstall dependencies
pip install -r requirements.txt

# For GUI-specific issues
pip install pillow flask flask-socketio
```

### Desktop GUI won't start

```bash
# Check tkinter
python3 -c "import tkinter"

# Install if missing (Ubuntu/Debian)
sudo apt-get install python3-tk

# Install if missing (Kali Linux)
sudo apt install python3-tk
```

### Web GUI - Port already in use

```bash
# Use different port
python3 ui/web_gui.py --port 8080

# Or kill existing process
lsof -ti:5000 | xargs kill -9
```

### Logo not displaying

```bash
# Ensure logo exists
ls -la public/*.png

# Check file permissions
chmod 644 public/*.png
```

## Next Steps

- 📖 Read [UI README](ui/README.md) for advanced features
- 📚 Check [Payload Documentation](payloads/README.md)
- 🔧 Explore [Model Guide](docs/MODEL_GUIDE.md)
- 🎯 Try different AI models for best results

## Getting Help

- **Documentation:** https://github.com/yashab-cyber/KaliGpt/docs
- **Issues:** https://github.com/yashab-cyber/KaliGpt/issues
- **Examples:** Check `/examples` directory

## Security Reminder

⚠️ **Use Responsibly:**
- Only test authorized systems
- Keep API keys secure
- Don't commit sensitive data
- Follow ethical hacking guidelines

---

**Happy Hacking with KaliGPT! 🔒**
