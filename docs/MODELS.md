# KaliGPT Supported AI Models (December 2025)

## 🌟 Latest Cloud Models

### OpenAI GPT Models

| Model | ID | Context | Speed | Cost | Best For |
|-------|----|---------:|-------|------|----------|
| **GPT-5.1** | `gpt-5.1` | 128K | ⚡⚡⚡ | $$$$ | Most advanced reasoning |
| **GPT-5** | `gpt-5` | 128K | ⚡⚡⚡ | $$$ | Complex multi-step analysis |
| **GPT-4** | `gpt-4` | 128K | ⚡⚡ | $$$ | Reliable, proven |
| **GPT-3.5-turbo** | `gpt-3.5-turbo` | 16K | ⚡⚡⚡ | $ | Fast, economical |

**Setup:**
```bash
export OPENAI_API_KEY=sk-your-key-here
kaligpt --model gpt-5.1
```

### Google Gemini Models

| Model | ID | Context | Speed | Cost | Best For |
|-------|----|---------:|-------|------|----------|
| **Gemini 3 Pro** | `gemini-3-pro` | 2M | ⚡⚡⚡ | $$$ | Massive context, multimodal |
| **Gemini 2.0 Pro** | `gemini-2-pro` | 1M | ⚡⚡⚡ | $$ | Large context analysis |

**Setup:**
```bash
export GOOGLE_API_KEY=your-google-key-here
kaligpt --model gemini-3
```

### Anthropic Claude Models

| Model | ID | Context | Speed | Cost | Best For |
|-------|----|---------:|-------|------|----------|
| **Claude Sonnet 4.5** | `claude-sonnet-4.5` | 200K | ⚡⚡⚡⚡ | $$$ | Lightning-fast, precise |
| **Claude Opus 4** | `claude-opus-4` | 200K | ⚡⚡ | $$$$ | Most powerful |
| **Claude Sonnet 3.5** | `claude-sonnet-3.5` | 200K | ⚡⚡⚡ | $$ | Fast & intelligent |

**Setup:**
```bash
export ANTHROPIC_API_KEY=sk-ant-your-key-here
kaligpt --model claude-sonnet-4.5
```

## 🆓 Local Models (Free, Privacy-Focused)

### Meta LLaMA (via Ollama)

| Model | ID | Size | Speed | Best For |
|-------|----|---------:|-------|----------|
| **LLaMA 3** | `llama3` | 8B/70B | ⚡⚡ | Latest, most capable local |
| **LLaMA 2** | `llama2` | 7B/13B/70B | ⚡⚡ | Stable, well-tested |

**Setup:**
```bash
ollama pull llama3
kaligpt --model llama3
```

### Other Local Models

| Model | ID | Size | Speed | Best For |
|-------|----|---------:|-------|----------|
| **Mistral** | `mistral` | 7B | ⚡⚡⚡ | Fast local inference |
| **Qwen** | `qwen` | 7B/14B | ⚡⚡ | Multilingual support |

**Setup:**
```bash
ollama pull mistral
kaligpt --model mistral
```

## 📊 Complete Model Matrix

### Performance Comparison

| Model | Provider | Type | Context Tokens | Speed | Quality | Privacy | Cost/1M Tokens |
|-------|----------|------|---------------:|-------|---------|---------|----------------|
| GPT-5.1 | OpenAI | Cloud | 128,000 | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | ❌ | ~$60 |
| GPT-5 | OpenAI | Cloud | 128,000 | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | ❌ | ~$50 |
| Gemini 3 Pro | Google | Cloud | 2,000,000 | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | ❌ | ~$7 |
| Claude Sonnet 4.5 | Anthropic | Cloud | 200,000 | ⚡⚡⚡⚡ | ⭐⭐⭐⭐⭐ | ❌ | ~$15 |
| Claude Opus 4 | Anthropic | Cloud | 200,000 | ⚡⚡ | ⭐⭐⭐⭐⭐ | ❌ | ~$75 |
| LLaMA 3 | Meta | Local | 8,000 | ⚡⚡ | ⭐⭐⭐⭐ | ✅ | Free |
| Mistral | Mistral | Local | 8,000 | ⚡⚡⚡ | ⭐⭐⭐ | ✅ | Free |

### Use Case Recommendations

| Use Case | Primary Model | Backup Model | Reasoning |
|----------|---------------|--------------|-----------|
| **Initial Reconnaissance** | Gemini 3 Pro | LLaMA 3 | Massive context for large scan outputs |
| **Vulnerability Analysis** | Claude Sonnet 4.5 | GPT-5.1 | Fast, precise technical analysis |
| **Exploit Development** | GPT-5.1 | Claude Opus 4 | Advanced reasoning for complex chains |
| **Payload Generation** | Claude Sonnet 4.5 | Mistral | Fast generation, good at code |
| **Report Writing** | GPT-5 | Gemini 2 Pro | Excellent structured output |
| **Privacy-Critical** | LLaMA 3 | Mistral | All processing stays local |
| **Learning/Practice** | LLaMA 3 | LLaMA 2 | Free, unlimited usage |
| **Budget-Conscious** | Gemini 3 Pro | LLaMA 3 | Best value for cloud option |

## 🎯 Selection Guide

### Choose GPT-5.1 if:
- You need the absolute best reasoning
- Working on complex, multi-step exploitation
- Budget is not a concern
- Need reliable, consistent outputs

### Choose Gemini 3 Pro if:
- Dealing with very large outputs (massive nmap scans)
- Need excellent value (low cost per token)
- Want multimodal capabilities (future features)
- Need huge context window

### Choose Claude Sonnet 4.5 if:
- Speed is critical
- Need precise technical responses
- Want fast iteration during pentesting
- Need excellent code generation

### Choose Claude Opus 4 if:
- Working on research-level problems
- Need absolute highest quality
- Complex reasoning is essential
- Cost is justified by importance

### Choose LLaMA 3 if:
- Privacy is paramount
- Working offline
- Need unlimited usage without costs
- Pentesting sensitive systems

## 🔄 Model Switching Strategies

### Strategy 1: Phase-Based
```bash
# Recon phase: Use Gemini 3 Pro (large context)
kaligpt --model gemini-3

# Switch to exploitation: Claude Sonnet 4.5 (fast)
KaliGPT> model claude-sonnet-4.5

# Complex exploitation: GPT-5.1 (best reasoning)
KaliGPT> model gpt-5.1

# Reporting: Back to Gemini 3 Pro (large context)
KaliGPT> model gemini-3
```

### Strategy 2: Privacy-First
```bash
# Start local
kaligpt --model llama3

# Only use cloud for complex problems
KaliGPT> model gpt-5.1  # temporarily

# Back to local
KaliGPT> model llama3
```

### Strategy 3: Cost-Optimized
```bash
# Most work on local
kaligpt --model llama3

# Critical analysis on budget cloud model
KaliGPT> model gemini-3

# Only most complex on premium
KaliGPT> model gpt-5.1  # when really needed
```

## 📝 Configuration Examples

### config/model_config.json Profiles

All models are pre-configured:

```json
{
  "gpt5.1": {...},      // Latest OpenAI
  "gpt5": {...},        // OpenAI GPT-5
  "gemini3": {...},     // Latest Google
  "gemini2": {...},     // Google Gemini 2
  "claude-sonnet-4.5": {...},  // Latest Anthropic
  "claude-opus-4": {...},      // Most powerful
  "claude-sonnet-3.5": {...},  // Fast Anthropic
  "llama3": {...},      // Latest local
  "llama2": {...},      // Stable local
  "mistral": {...},     // Fast local
  "qwen": {...}         // Multilingual local
}
```

## 🔑 API Key Management

### Environment Variables
```bash
# Add to ~/.bashrc or ~/.zshrc for persistence
export OPENAI_API_KEY=sk-proj-...
export GOOGLE_API_KEY=AIza...
export ANTHROPIC_API_KEY=sk-ant-...
```

### Verify Setup
```bash
# Test each model
kaligpt --test-model gpt-5.1
kaligpt --test-model gemini-3
kaligpt --test-model claude-sonnet-4.5
kaligpt --test-model llama3
```

## 💰 Cost Estimates

### Example Pentest (1 hour, 100K tokens)

| Model | Estimated Cost |
|-------|---------------:|
| GPT-5.1 | ~$6.00 |
| GPT-5 | ~$5.00 |
| Gemini 3 Pro | ~$0.70 |
| Claude Sonnet 4.5 | ~$1.50 |
| Claude Opus 4 | ~$7.50 |
| LLaMA 3 | $0.00 |

**Recommendation**: Use Gemini 3 Pro for best value, or LLaMA 3 for free.

## 🚀 Getting Started

1. **Install KaliGPT**
   ```bash
   ./scripts/installer.sh
   ```

2. **Choose your model** (see guide above)

3. **Set API key** (if using cloud model)
   ```bash
   export OPENAI_API_KEY=...
   # or
   export GOOGLE_API_KEY=...
   # or
   export ANTHROPIC_API_KEY=...
   ```

4. **Start pentesting**
   ```bash
   kaligpt --model claude-sonnet-4.5
   ```

## 📚 Additional Resources

- [Model Configuration Guide](MODEL_GUIDE.md) - Detailed setup instructions
- [Quick Start Guide](QUICKSTART.md) - Get started in 5 minutes
- [Main Documentation](../README.md) - Full KaliGPT documentation

---

**Last Updated**: December 9, 2025  
**KaliGPT Version**: 1.1.0

**All models listed are currently available and supported.**
