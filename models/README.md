# KaliGPT Models

This directory contains interfaces for various LLM models that can power KaliGPT.

## Supported Models

### Cloud-Based Models
- **GPT-4/GPT-3.5** (`gpt.py`) - OpenAI's models (requires API key)
- **Mistral** (`mistral.py`) - Mistral AI models (API or local)

### Local Models (Free)
- **LLaMA** (`local_llama.py`) - Meta's LLaMA models via Ollama
- **Qwen** (`qwen.py`) - Alibaba's Qwen models via Ollama

## Setup Instructions

### Using OpenAI GPT
```bash
export OPENAI_API_KEY=your_api_key_here
```

### Using Local Models (Recommended for Pentesting)
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull a model
ollama pull llama2
ollama pull mistral
ollama pull qwen

# Start Ollama server
ollama serve
```

## Configuration

Edit `config/model_config.json`:
```json
{
  "model_type": "llama",
  "model": "llama2",
  "temperature": 0.7,
  "max_tokens": 2000
}
```

## Model Selection

The `model_selector.py` automatically chooses the appropriate model interface based on your configuration.
