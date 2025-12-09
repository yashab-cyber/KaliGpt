# AI Model Configuration Guide

This guide provides detailed information about configuring and using different AI models with KaliGPT.

## 🚀 Latest Models (December 2025)

### OpenAI Models

#### GPT-5.1 (Latest Flagship)
- **Model ID**: `gpt-5.1`
- **Best For**: Most advanced reasoning, complex pentesting scenarios
- **Context**: 128K tokens
- **Setup**:
  ```bash
  export OPENAI_API_KEY=sk-your-api-key
  kaligpt --model gpt-5.1
  ```

#### GPT-5
- **Model ID**: `gpt-5`
- **Best For**: Advanced analysis, multi-step pentesting
- **Context**: 128K tokens
- **Setup**:
  ```bash
  export OPENAI_API_KEY=sk-your-api-key
  kaligpt --model gpt-5
  ```

#### GPT-4
- **Model ID**: `gpt-4`
- **Best For**: Reliable, proven performance
- **Context**: 128K tokens
- **Setup**:
  ```bash
  export OPENAI_API_KEY=sk-your-api-key
  kaligpt --model gpt-4
  ```

### Google Gemini Models

#### Gemini 3 Pro (Latest)
- **Model ID**: `gemini-3-pro`
- **Best For**: Multimodal analysis, latest capabilities
- **Context**: 2M tokens
- **Setup**:
  ```bash
  export GOOGLE_API_KEY=your-google-api-key
  kaligpt --model gemini-3
  ```

#### Gemini 2.0 Pro
- **Model ID**: `gemini-2-pro`
- **Best For**: Advanced reasoning, large context
- **Context**: 1M tokens
- **Setup**:
  ```bash
  export GOOGLE_API_KEY=your-google-api-key
  kaligpt --model gemini-2
  ```

### Anthropic Claude Models

#### Claude Sonnet 4.5 (Latest Flagship)
- **Model ID**: `claude-sonnet-4.5`
- **Best For**: Complex reasoning, precise technical analysis
- **Context**: 200K tokens
- **Setup**:
  ```bash
  export ANTHROPIC_API_KEY=sk-ant-your-api-key
  kaligpt --model claude-sonnet-4.5
  ```

#### Claude Opus 4
- **Model ID**: `claude-opus-4`
- **Best For**: Most powerful, research-level tasks
- **Context**: 200K tokens
- **Setup**:
  ```bash
  export ANTHROPIC_API_KEY=sk-ant-your-api-key
  kaligpt --model claude-opus-4
  ```

#### Claude Sonnet 3.5
- **Model ID**: `claude-sonnet-3.5`
- **Best For**: Fast, intelligent responses
- **Context**: 200K tokens
- **Setup**:
  ```bash
  export ANTHROPIC_API_KEY=sk-ant-your-api-key
  kaligpt --model claude-sonnet-3.5
  ```

## 🆓 Local Models (Free, Privacy-Focused)

### LLaMA Models (via Ollama)

#### LLaMA 3
- **Model ID**: `llama3`
- **Best For**: Local inference, privacy
- **Setup**:
  ```bash
  ollama pull llama3
  kaligpt --model llama3
  ```

#### LLaMA 2
- **Model ID**: `llama2`
- **Best For**: Stable, well-tested
- **Setup**:
  ```bash
  ollama pull llama2
  kaligpt --model llama2
  ```

### Other Local Models

#### Mistral
- **Model ID**: `mistral`
- **Setup**:
  ```bash
  ollama pull mistral
  kaligpt --model mistral
  ```

#### Qwen
- **Model ID**: `qwen`
- **Setup**:
  ```bash
  ollama pull qwen
  kaligpt --model qwen
  ```

## 📊 Model Comparison

| Model | Provider | Type | Context | Speed | Cost | Best For |
|-------|----------|------|---------|-------|------|----------|
| GPT-5.1 | OpenAI | Cloud | 128K | Fast | $$$ | Advanced reasoning |
| GPT-5 | OpenAI | Cloud | 128K | Fast | $$$ | Complex analysis |
| Gemini 3 Pro | Google | Cloud | 2M | Fast | $$ | Large context |
| Claude Sonnet 4.5 | Anthropic | Cloud | 200K | Very Fast | $$$ | Technical precision |
| Claude Opus 4 | Anthropic | Cloud | 200K | Medium | $$$$ | Research tasks |
| LLaMA 3 | Meta | Local | 8K | Medium | Free | Privacy, offline |
| Mistral | Mistral | Local | 8K | Fast | Free | Local inference |

## 🔧 Configuration Examples

### Multi-Model Setup
Configure different models for different tasks:

```json
{
  "reconnaissance": "gemini-3-pro",
  "exploitation": "claude-sonnet-4.5",
  "reporting": "gpt-5.1",
  "local_fallback": "llama3"
}
```

### Performance Tuning

#### For Speed
```json
{
  "model": "claude-sonnet-4.5",
  "temperature": 0.5,
  "max_tokens": 1000
}
```

#### For Accuracy
```json
{
  "model": "gpt-5.1",
  "temperature": 0.3,
  "max_tokens": 4000
}
```

#### For Creativity (Payload Generation)
```json
{
  "model": "gemini-3-pro",
  "temperature": 0.9,
  "max_tokens": 2000
}
```

## 🔑 Getting API Keys

### OpenAI
1. Visit https://platform.openai.com/api-keys
2. Create new API key
3. Export: `export OPENAI_API_KEY=sk-...`

### Google Gemini
1. Visit https://makersuite.google.com/app/apikey
2. Create API key
3. Export: `export GOOGLE_API_KEY=...`

### Anthropic Claude
1. Visit https://console.anthropic.com/
2. Create API key
3. Export: `export ANTHROPIC_API_KEY=sk-ant-...`

## 💡 Tips

1. **Use latest models for complex scenarios**: GPT-5.1, Gemini 3 Pro, Claude Sonnet 4.5
2. **Use local models for privacy**: LLaMA 3, Mistral
3. **Gemini 3 Pro for large context**: 2M token context is excellent for comprehensive reports
4. **Claude Sonnet 4.5 for speed**: Fastest response times with excellent quality
5. **GPT-5.1 for reasoning**: Best for multi-step exploitation chains

## 🔄 Switching Models Mid-Session

```bash
# Start with local model
kaligpt --model llama3

# Switch to cloud model for complex task
KaliGPT> model gpt-5.1

# Switch to Gemini for large context
KaliGPT> model gemini-3

# Back to local for privacy
KaliGPT> model llama3
```

## 📈 Cost Optimization

- **Development/Testing**: Use local models (free)
- **Quick scans**: Claude Sonnet 4.5 (fast, affordable)
- **Complex exploitation**: GPT-5.1 (worth the cost)
- **Large reports**: Gemini 3 Pro (huge context, good value)

## 🛡️ Privacy Considerations

**Cloud Models** (OpenAI, Google, Anthropic):
- Data sent to external servers
- Subject to provider's privacy policy
- Best for non-sensitive work

**Local Models** (LLaMA, Mistral):
- All processing on your machine
- No data leaves your system
- Best for sensitive pentests

---

**Updated**: December 2025
**KaliGPT Version**: 1.0.0
