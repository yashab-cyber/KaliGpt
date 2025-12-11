# KaliGPT GUI Interfaces

**Created by Yashab Alam** | [Instagram](https://www.instagram.com/yashab.alam) | [LinkedIn](https://www.linkedin.com/in/yashab-alam) | [💎 Donate](../DONATE.md)

KaliGPT provides multiple graphical user interfaces for different use cases.

## 🖥️ Desktop GUI (Tkinter)

Modern desktop application with native look and feel.

### Features

- **Dark Theme**: Kali Linux-inspired color scheme
- **Multi-Tab Interface**: Terminal, Payloads, History, Reports
- **Real-time AI Analysis**: Instant feedback on command output
- **Payload Generator**: Visual template selection and generation
- **Session Management**: Save and load sessions
- **Report Generation**: Export in Markdown, HTML, or JSON

### Installation

```bash
# Install GUI dependencies
pip install pillow

# Or install all requirements
pip install -r requirements.txt
```

### Usage

```bash
# Launch desktop GUI
python3 ui/gui.py
```

### Interface Overview

#### Terminal Tab
- Paste command output for AI analysis
- Get real-time recommendations
- View analysis history

#### Payloads Tab
- Select payload type (SQLi, XSS, Shells, etc.)
- Choose from pre-built templates
- Customize with variables
- Generate AI-powered payloads based on target info

#### History Tab
- View all session activities
- Review past analyses
- Track progress

#### Report Tab
- Generate professional reports
- Choose format (Markdown, HTML, JSON)
- Export to file

### Screenshots

<div align="center">
  <img src="../public/Untitled design.png" alt="Desktop GUI" width="800"/>
</div>

---

## 🌐 Web GUI (Flask)

Browser-based interface accessible from anywhere on your network.

### Features

- **Responsive Design**: Works on desktop, tablet, and mobile
- **WebSocket Support**: Real-time updates without page refresh
- **RESTful API**: Integrate with other tools
- **Multi-user Ready**: Access from multiple devices
- **Session Persistence**: Save sessions to server
- **Modern UI**: Clean, intuitive interface

### Installation

```bash
# Install web GUI dependencies
pip install flask flask-socketio python-socketio eventlet

# Or install all requirements
pip install -r requirements.txt
```

### Usage

```bash
# Launch web GUI
python3 ui/web_gui.py

# Access at: http://localhost:5000
# Or from other devices: http://<your-ip>:5000
```

### Configuration

```bash
# Custom host and port
python3 ui/web_gui.py --host 0.0.0.0 --port 8080

# Debug mode
python3 ui/web_gui.py --debug
```

### API Endpoints

The web GUI exposes a RESTful API:

#### Connection
- `GET /api/models` - List available AI models
- `POST /api/connect` - Connect to AI engine
- `GET /api/status` - Get connection status

#### Analysis
- `POST /api/analyze` - Analyze command output

#### Payloads
- `GET /api/templates` - Get available templates
- `POST /api/payload/generate` - Generate payload from template
- `POST /api/payload/ai-generate` - Generate AI-powered payload

#### Reports
- `POST /api/report/preview` - Generate report preview

#### Session
- `POST /api/session/save` - Save current session
- `POST /api/session/load` - Load saved session
- `POST /api/session/clear` - Clear session

### WebSocket Events

- `connect` - Client connected
- `analyze_stream` - Stream analysis results
- `status` - Status updates
- `progress` - Progress notifications
- `analysis_result` - Analysis completed
- `error` - Error occurred

---

## 💻 CLI Interface

For terminal purists, KaliGPT also provides a full-featured CLI:

```bash
python3 ui/cli.py
```

See main [README.md](../README.md) for CLI usage instructions.

---

## Comparison

| Feature | Desktop GUI | Web GUI | CLI |
|---------|-------------|---------|-----|
| **Platform** | Desktop only | Any device with browser | Terminal |
| **Installation** | Pillow | Flask, Flask-SocketIO | None |
| **Real-time Updates** | ✅ | ✅ | ✅ |
| **Multi-device Access** | ❌ | ✅ | ❌ |
| **Offline Use** | ✅ | ✅ | ✅ |
| **Resource Usage** | Medium | Low | Very Low |
| **Best For** | Desktop users | Team collaboration | Automation |

---

## Keyboard Shortcuts

### Desktop GUI
- `Ctrl+N` - New session
- `Ctrl+S` - Save session
- `Ctrl+O` - Load session
- `Ctrl+Q` - Quit

### Web GUI
- Browser standard shortcuts apply
- `Ctrl+Enter` in text areas to submit

---

## Troubleshooting

### Desktop GUI

**Logo not showing:**
```bash
pip install --upgrade pillow
```

**Window too small:**
- Resize manually or edit `gui.py` line with `geometry()`

### Web GUI

**Port already in use:**
```bash
# Use different port
python3 ui/web_gui.py --port 8080
```

**Can't access from other devices:**
- Ensure host is set to `0.0.0.0`
- Check firewall settings
- Verify network connectivity

**WebSocket connection failed:**
```bash
# Reinstall dependencies
pip install --upgrade flask-socketio python-socketio eventlet
```

---

## Development

### Desktop GUI (Tkinter)

The desktop GUI is built with Python's built-in Tkinter library:

- `ui/gui.py` - Main application code
- Uses threading for non-blocking AI calls
- Queue-based communication between threads

### Web GUI (Flask)

The web GUI uses modern web technologies:

- `ui/web_gui.py` - Flask application server
- `ui/templates/index.html` - HTML template
- `ui/static/css/style.css` - Stylesheets
- `ui/static/js/app.js` - JavaScript logic
- WebSocket for real-time updates

### Contributing

To add features to the GUIs:

1. Fork the repository
2. Create feature branch
3. Add your feature to appropriate GUI
4. Test thoroughly
5. Submit pull request

---

## Security Notes

⚠️ **Important Security Considerations:**

1. **Web GUI Network Exposure**: 
   - By default, runs on localhost only
   - Only expose to trusted networks
   - Use HTTPS in production (reverse proxy)
   - Implement authentication for multi-user setups

2. **API Keys**:
   - Never hardcode API keys in GUI
   - Use environment variables
   - Don't commit keys to version control

3. **Session Files**:
   - May contain sensitive pentesting data
   - Store securely
   - Encrypt if needed

---

## Support

For issues, questions, or feature requests:
- GitHub Issues: https://github.com/yashab-cyber/KaliGpt/issues
- Documentation: https://github.com/yashab-cyber/KaliGpt/docs

---

## License

See main repository [LICENSE](../LICENSE) file for details.
