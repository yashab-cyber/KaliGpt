# Quick Start with Latest AI Models

This guide gets you started with KaliGPT using the latest AI models (December 2025).

## 🚀 Installation

```bash
git clone https://github.com/yashab-cyber/KaliGpt.git
cd KaliGpt
./scripts/installer.sh
```

## 🤖 Choose Your AI Model

### Option 1: Latest Cloud Models (Recommended)

#### GPT-5.1 (OpenAI - Most Advanced)
```bash
# Get API key from: https://platform.openai.com/api-keys
export OPENAI_API_KEY=sk-your-api-key-here
kaligpt --model gpt-5.1
```

#### Gemini 3 Pro (Google - Huge Context)
```bash
# Get API key from: https://makersuite.google.com/app/apikey
export GOOGLE_API_KEY=your-google-api-key-here
kaligpt --model gemini-3
```

#### Claude Sonnet 4.5 (Anthropic - Fast & Precise)
```bash
# Get API key from: https://console.anthropic.com/
export ANTHROPIC_API_KEY=sk-ant-your-api-key-here
kaligpt --model claude-sonnet-4.5
```

### Option 2: Local Models (Free, Private)

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Download LLaMA 3
ollama pull llama3

# Start KaliGPT
kaligpt --model llama3
```

## 📋 First Pentest

### Example: Web Application Testing

```bash
# 1. Start KaliGPT with your preferred model
kaligpt --model claude-sonnet-4.5

# 2. Set target
KaliGPT> target 192.168.1.100

# 3. Initial scan
KaliGPT> run nmap -sV -sC 192.168.1.100

# AI analyzes output and suggests next steps
# Example output:
# ✓ Found: Apache 2.4.52 on port 80
# ✓ Found: MySQL 8.0 on port 3306
# 
# 🎯 Next Step: Web vulnerability scan
# Recommended command: nikto -h http://192.168.1.100

# 4. Follow AI recommendations
KaliGPT> run nikto -h http://192.168.1.100

# 5. Generate payloads when needed
KaliGPT> payload sqli

# 6. Create report
KaliGPT> report
```

## 🎯 Model Selection Guide

### When to Use Each Model

| Scenario | Best Model | Why |
|----------|-----------|-----|
| Complex exploitation chains | GPT-5.1 | Advanced reasoning |
| Large scan outputs | Gemini 3 Pro | 2M token context |
| Fast pentests | Claude Sonnet 4.5 | Fastest response |
| Privacy-critical work | LLaMA 3 | Local processing |
| Learning/practice | LLaMA 3 | Free, unlimited |

## 💡 Pro Tips

1. **Start with reconnaissance on Gemini 3 Pro** - Its huge context window handles large nmap outputs perfectly

2. **Switch to Claude Sonnet 4.5 for exploitation** - Fast, precise technical recommendations

3. **Use GPT-5.1 for complex scenarios** - When you need the smartest reasoning

4. **Always use local models for sensitive data** - Privacy matters in pentesting

5. **Enable auto-execute for trusted environments**:
   ```bash
   kaligpt --model gpt-5.1 --auto
   ```

## 🔄 Switching Models

You can switch models during a session:

```bash
# Start with free local model for recon
kaligpt --model llama3

# Switch to cloud model for complex analysis
KaliGPT> model gpt-5.1

# Check available models
KaliGPT> models

# Switch back to local for privacy
KaliGPT> model llama3
```

## 📊 Command Reference

```bash
# Target management
target <IP/URL>          # Set target
target show              # Show current target
target clear             # Clear target

# Command execution
run <command>            # Execute command with AI analysis
payload <type>           # Generate payload (sqli, xss, shell, etc.)
status                   # Show session status
history                  # Show command history

# Reporting
report                   # Generate comprehensive report
report --format html     # Generate HTML report
report --format pdf      # Generate PDF report

# Model management
model <name>             # Switch AI model
models                   # List available models

# Help
help                     # Show all commands
help <command>           # Show command details
exit                     # Exit KaliGPT
```

## 🔐 Security Best Practices

1. **Only test authorized systems**
   ```bash
   # KaliGPT always asks for confirmation
   Execute command? (yes/no):
   ```

2. **Use safe mode** (enabled by default)
   ```bash
   # Blocks dangerous commands like rm -rf /
   kaligpt --safe
   ```

3. **Keep logs for audit trails**
   ```bash
   # Logs saved to ~/.kaligpt/logs/
   ls -la ~/.kaligpt/logs/
   ```

## 🆘 Troubleshooting

### Model Not Working?

```bash
# Check API key
echo $OPENAI_API_KEY
echo $GOOGLE_API_KEY
echo $ANTHROPIC_API_KEY

# Test connection
kaligpt --test-model gpt-5.1
kaligpt --test-model gemini-3
kaligpt --test-model claude-sonnet-4.5

# Check local model
ollama list
ollama run llama3 "test"
```

### Installation Issues?

```bash
# Reinstall dependencies
pip3 install -r requirements.txt --upgrade

# Check Python version (needs 3.10+)
python3 --version

# Check pentesting tools
which nmap sqlmap nikto gobuster hydra
```

## 🎓 Learning Path

### Beginner
1. Start with local LLaMA 3 (free)
2. Run basic nmap scans
3. Let AI guide you through methodology
4. Generate simple payloads

### Intermediate
1. Try Claude Sonnet 4.5 (fast cloud model)
2. Full web application testing
3. Exploit chains with AI guidance
4. Custom payload generation

### Advanced
1. Use GPT-5.1 for complex scenarios
2. Multi-stage penetration tests
3. Custom tool integration
4. Automated reporting workflows

## 📚 Next Steps

- Read the [Full Documentation](../README.md)
- Check [Model Configuration Guide](MODEL_GUIDE.md)
- Join the community discussions
- Star ⭐ the repository

---

**Ready to start?**

```bash
kaligpt --model claude-sonnet-4.5
```

Happy ethical hacking! 🔒
