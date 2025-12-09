# Migration Guide: v1.0 → v1.1

This guide helps you upgrade from KaliGPT v1.0 to v1.1 with the latest AI models.

## ⚡ Quick Migration (5 minutes)

```bash
# 1. Update code
cd KaliGPT
git pull origin main

# 2. Update dependencies
pip3 install -r requirements.txt --upgrade

# 3. Verify setup
python3 scripts/verify_models.py

# 4. Done! Start using new models
kaligpt --model claude-sonnet-4.5
```

## 📋 What Changed

### ✅ Added (New Features)
- GPT-5.1 and GPT-5 support
- Gemini 3 Pro and Gemini 2.0 Pro support
- Claude Sonnet 4.5, Opus 4, and Sonnet 3.5 support
- Model verification script
- Comprehensive model documentation

### ✅ Updated (Improvements)
- Enhanced model selection
- Better error handling
- Updated default model to GPT-5.1
- Increased max_tokens to 4000 for new models

### ✅ No Breaking Changes
- All v1.0 functionality works exactly the same
- Existing configurations remain valid
- Old models (GPT-4, LLaMA, etc.) still supported

## 🔧 Detailed Migration Steps

### Step 1: Backup Your Configuration (Optional)

```bash
# Backup your custom settings
cp config/settings.json config/settings.json.backup
cp config/model_config.json config/model_config.json.backup
```

### Step 2: Update Repository

```bash
cd KaliGPT
git pull origin main
```

**What this does:**
- Downloads new model implementations
- Updates documentation
- Adds verification script
- Updates dependencies list

### Step 3: Install New Dependencies

```bash
pip3 install -r requirements.txt --upgrade
```

**New packages installed:**
- `google-generativeai>=0.3.0` - For Gemini models
- `anthropic>=0.25.0` - For Claude models

**Existing packages updated:**
- All packages upgraded to latest compatible versions

### Step 4: Configure API Keys

#### If Using OpenAI (GPT-5.1, GPT-5)
```bash
# Already set in v1.0? You're good!
export OPENAI_API_KEY=sk-your-existing-key

# Or add new key
export OPENAI_API_KEY=sk-new-key
```

#### If Using Google Gemini (New)
```bash
# Get key from: https://makersuite.google.com/app/apikey
export GOOGLE_API_KEY=your-google-api-key

# Make it permanent
echo 'export GOOGLE_API_KEY=your-key' >> ~/.bashrc
source ~/.bashrc
```

#### If Using Anthropic Claude (New)
```bash
# Get key from: https://console.anthropic.com/
export ANTHROPIC_API_KEY=sk-ant-your-key

# Make it permanent
echo 'export ANTHROPIC_API_KEY=your-key' >> ~/.bashrc
source ~/.bashrc
```

### Step 5: Verify Installation

```bash
python3 scripts/verify_models.py
```

**This checks:**
- ✓ Python dependencies installed
- ✓ API keys configured
- ✓ Local models available (Ollama)
- ✓ Model implementations working

**Expected output:**
```
✓ pexpect installed
✓ google-generativeai installed
✓ anthropic installed
✓ OPENAI_API_KEY set
✓ GOOGLE_API_KEY set
✓ ANTHROPIC_API_KEY set
✓ GPT models available
✓ Gemini models available
✓ Claude models available
```

### Step 6: Test New Models

```bash
# Test GPT-5.1
kaligpt --model gpt-5.1

# Test Gemini 3 Pro
kaligpt --model gemini-3

# Test Claude Sonnet 4.5
kaligpt --model claude-sonnet-4.5
```

## 🔄 Configuration Migration

### Your Old Config (v1.0)
```json
{
  "model_type": "gpt",
  "model": "gpt-4",
  "temperature": 0.7,
  "max_tokens": 2000
}
```

### Upgrade Options

#### Option 1: Use Latest Model
```json
{
  "model_type": "gpt",
  "model": "gpt-5.1",
  "temperature": 0.7,
  "max_tokens": 4000
}
```

#### Option 2: Use Gemini for Large Context
```json
{
  "model_type": "gemini",
  "model": "gemini-3-pro",
  "temperature": 0.7,
  "max_tokens": 4000
}
```

#### Option 3: Use Claude for Speed
```json
{
  "model_type": "claude",
  "model": "claude-sonnet-4.5",
  "temperature": 0.7,
  "max_tokens": 4000
}
```

#### Option 4: Keep Old Config (Still Works!)
```json
{
  "model_type": "gpt",
  "model": "gpt-4",
  "temperature": 0.7,
  "max_tokens": 2000
}
```

## 🎯 Choosing Your New Default Model

### Decision Matrix

| Your Priority | Recommended Model | Why |
|---------------|------------------|-----|
| **Best Quality** | GPT-5.1 | Most advanced reasoning |
| **Huge Context** | Gemini 3 Pro | 2M tokens, best value |
| **Speed** | Claude Sonnet 4.5 | Fastest responses |
| **Privacy** | LLaMA 3 (local) | No data leaves your machine |
| **Cost** | Gemini 3 Pro or LLaMA 3 | Best $/token or free |

### Update Default in Config

Edit `config/model_config.json`:

```json
{
  "model_type": "claude",  // Changed from "llama"
  "model": "claude-sonnet-4.5",  // Changed from "llama2"
  "temperature": 0.7,
  "max_tokens": 4000  // Increased from 2000
}
```

## 📊 Before/After Comparison

### v1.0 Available Models
- GPT-4, GPT-3.5
- LLaMA 2, LLaMA 3
- Mistral
- Qwen

### v1.1 Available Models
- **GPT-5.1, GPT-5** ⭐ NEW
- GPT-4, GPT-3.5
- **Gemini 3 Pro, Gemini 2.0 Pro** ⭐ NEW
- **Claude Sonnet 4.5, Opus 4, Sonnet 3.5** ⭐ NEW
- LLaMA 2, LLaMA 3
- Mistral
- Qwen

## ⚠️ Common Issues

### Issue 1: Import Error for google.generativeai

**Error:**
```
ModuleNotFoundError: No module named 'google.generativeai'
```

**Solution:**
```bash
pip3 install google-generativeai>=0.3.0
```

### Issue 2: Import Error for anthropic

**Error:**
```
ModuleNotFoundError: No module named 'anthropic'
```

**Solution:**
```bash
pip3 install anthropic>=0.25.0
```

### Issue 3: API Key Not Found

**Error:**
```
ValueError: Google API key not found
```

**Solution:**
```bash
export GOOGLE_API_KEY=your-key-here
# Or for Claude:
export ANTHROPIC_API_KEY=your-key-here
```

### Issue 4: Old Model Still Default

**Symptom:** KaliGPT still using old model

**Solution:**
```bash
# Explicitly specify new model
kaligpt --model gpt-5.1

# Or update config/model_config.json
```

## 💡 Best Practices

### 1. Keep Old and New
```bash
# Use new models for complex tasks
kaligpt --model gpt-5.1

# Keep using local models for privacy
kaligpt --model llama3
```

### 2. Gradual Migration
```bash
# Week 1: Test new models
kaligpt --model claude-sonnet-4.5  # Just testing

# Week 2: Use for real work
# Update default in config

# Week 3: Full migration
# Set API keys in .bashrc
```

### 3. Cost Management
```bash
# Development: Use local models
kaligpt --model llama3

# Production: Use cloud models
kaligpt --model gemini-3  # Best value
```

## 🎓 Learning the New Models

### Try Each Model

```bash
# 1. Test GPT-5.1 (advanced reasoning)
kaligpt --model gpt-5.1
KaliGPT> target example.com
KaliGPT> run nmap -sV example.com

# 2. Test Gemini 3 Pro (huge context)
kaligpt --model gemini-3
KaliGPT> target example.com
KaliGPT> run nmap -p- -A example.com  # Large output

# 3. Test Claude Sonnet 4.5 (speed)
kaligpt --model claude-sonnet-4.5
KaliGPT> target example.com
KaliGPT> run nikto -h example.com
```

### Compare Results

Same task, different models:
```bash
# Task: Analyze nmap output
echo "Compare how each model analyzes the same scan"

kaligpt --model gpt-5.1 < scan_output.txt
kaligpt --model gemini-3 < scan_output.txt
kaligpt --model claude-sonnet-4.5 < scan_output.txt
```

## 📚 Additional Resources

- **Model Comparison**: [docs/MODELS.md](docs/MODELS.md)
- **Configuration Guide**: [docs/MODEL_GUIDE.md](docs/MODEL_GUIDE.md)
- **Quick Start**: [docs/QUICKSTART.md](docs/QUICKSTART.md)
- **Changelog**: [CHANGELOG.md](CHANGELOG.md)

## ✅ Migration Checklist

- [ ] Backup existing configuration
- [ ] Update repository (`git pull`)
- [ ] Install new dependencies (`pip3 install -r requirements.txt --upgrade`)
- [ ] Set up new API keys (if using cloud models)
- [ ] Run verification script (`python3 scripts/verify_models.py`)
- [ ] Test new models
- [ ] Update default model (optional)
- [ ] Update documentation for your team
- [ ] Celebrate! 🎉

## 🆘 Need Help?

- **Verification Failed?** Run `python3 scripts/verify_models.py` for diagnostics
- **API Issues?** Check [docs/MODEL_GUIDE.md](docs/MODEL_GUIDE.md)
- **General Questions?** See [README.md](README.md)
- **Bugs?** Open an issue on GitHub

---

**Migration Time**: ~5 minutes  
**Difficulty**: Easy  
**Breaking Changes**: None  
**Rollback**: Just use old model names

**Happy Migrating! 🚀**
