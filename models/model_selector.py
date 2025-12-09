#!/usr/bin/env python3
"""
Model Selector
Manages different LLM models and selects the appropriate one
"""

from typing import Dict, Optional
from .gpt import GPTModel
from .local_llama import LocalLlamaModel
from .mistral import MistralModel
from .qwen import QwenModel
from .openai import OpenAICompatibleModel
from .gemini import GeminiModel
from .anthropic_claude import ClaudeModel


class ModelSelector:
    """
    Selects and initializes the appropriate model based on configuration
    """
    
    MODEL_CLASSES = {
        'gpt': GPTModel,
        'gpt-4': GPTModel,
        'gpt-5': GPTModel,
        'gpt-5.1': GPTModel,
        'gpt-3.5': GPTModel,
        'llama': LocalLlamaModel,
        'llama2': LocalLlamaModel,
        'llama3': LocalLlamaModel,
        'mistral': MistralModel,
        'qwen': QwenModel,
        'gemini': GeminiModel,
        'gemini-2': GeminiModel,
        'gemini-3': GeminiModel,
        'claude': ClaudeModel,
        'sonnet': ClaudeModel,
        'opus': ClaudeModel,
        'openai': OpenAICompatibleModel,
        'custom': OpenAICompatibleModel
    }
    
    def __init__(self, config: Dict):
        """
        Initialize model selector
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
    
    def get_model(self, model_type: str):
        """
        Get and initialize a model
        
        Args:
            model_type: Type of model to use
            
        Returns:
            Initialized model instance
        """
        model_type = model_type.lower()
        
        # Find the appropriate model class
        model_class = None
        for key, cls in self.MODEL_CLASSES.items():
            if key in model_type:
                model_class = cls
                break
        
        if not model_class:
            # Default to local LLaMA via Ollama
            print(f"[Warning] Unknown model type '{model_type}', defaulting to local LLaMA")
            model_class = LocalLlamaModel
        
        try:
            return model_class(self.config)
        except Exception as e:
            print(f"[Error] Failed to initialize {model_type}: {e}")
            print("[Info] Falling back to local LLaMA via Ollama")
            return LocalLlamaModel(self.config)
    
    @staticmethod
    def list_available_models() -> Dict[str, str]:
        """
        List all available model types
        
        Returns:
            Dict mapping model types to descriptions
        """
        return {
            'gpt-5.1': 'OpenAI GPT-5.1 (latest, requires API key)',
            'gpt-5': 'OpenAI GPT-5 (requires API key)',
            'gpt': 'OpenAI GPT-4/GPT-3.5 (requires API key)',
            'gemini-3': 'Google Gemini 3 Pro (requires API key)',
            'gemini-2': 'Google Gemini 2.0 Pro (requires API key)',
            'claude-sonnet-4.5': 'Claude Sonnet 4.5 (latest, requires API key)',
            'claude-opus-4': 'Claude Opus 4 (requires API key)',
            'claude-sonnet-3.5': 'Claude Sonnet 3.5 (requires API key)',
            'llama': 'Local LLaMA via Ollama (free, runs locally)',
            'llama2': 'LLaMA 2 via Ollama (free, runs locally)',
            'llama3': 'LLaMA 3 via Ollama (free, runs locally)',
            'mistral': 'Mistral AI (API or local via Ollama)',
            'qwen': 'Qwen models via Ollama (free, runs locally)',
            'openai': 'OpenAI-compatible API (custom endpoints)',
        }
    
    @staticmethod
    def get_recommended_config(model_type: str) -> Dict:
        """
        Get recommended configuration for a model type
        
        Args:
            model_type: Type of model
            
        Returns:
            Recommended configuration dict
        """
        configs = {
            'gpt': {
                'model_type': 'gpt',
                'model': 'gpt-4',
                'temperature': 0.7,
                'max_tokens': 2000
            },
            'llama': {
                'model_type': 'llama',
                'model': 'llama2',
                'base_url': 'http://localhost:11434',
                'temperature': 0.7,
                'max_tokens': 2000
            },
            'mistral': {
                'model_type': 'mistral',
                'model': 'mistral',
                'use_ollama': True,
                'temperature': 0.7,
                'max_tokens': 2000
            },
            'qwen': {
                'model_type': 'qwen',
                'model': 'qwen',
                'base_url': 'http://localhost:11434',
                'temperature': 0.7,
                'max_tokens': 2000
            }
        }
        
        return configs.get(model_type, configs['llama'])


class FallbackModel:
    """
    Fallback model that provides basic responses when no LLM is available
    """
    
    def __init__(self, config: Dict):
        self.config = config
        print("[Warning] Using fallback model - no LLM backend available")
    
    def generate(self, prompt: str, conversation_history=None) -> str:
        """Generate a basic fallback response"""
        return """I'm running in fallback mode without an LLM backend.
        
To use KaliGPT's AI features, please:
1. Set up OpenAI API key: export OPENAI_API_KEY=your_key
2. Or install Ollama: curl -fsSL https://ollama.com/install.sh | sh
3. Then run: ollama pull llama2

For now, I can still parse tool output and provide basic recommendations."""


__all__ = [
    'ModelSelector',
    'GPTModel',
    'LocalLlamaModel',
    'MistralModel',
    'QwenModel',
    'OpenAICompatibleModel',
    'FallbackModel'
]
