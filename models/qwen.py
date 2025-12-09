#!/usr/bin/env python3
"""
Qwen Model Interface
"""

import requests
from typing import List, Dict, Optional
import json


class QwenModel:
    """Interface for Qwen models (via Ollama)"""
    
    def __init__(self, config: Dict):
        """
        Initialize Qwen model
        
        Args:
            config: Configuration dict
        """
        self.config = config
        self.model = config.get('model', 'qwen')
        self.base_url = config.get('base_url', 'http://localhost:11434')
        self.temperature = config.get('temperature', 0.7)
        self.max_tokens = config.get('max_tokens', 2000)
    
    def generate(self, prompt: str, conversation_history: List[Dict] = None) -> str:
        """
        Generate response from Qwen
        
        Args:
            prompt: User prompt
            conversation_history: Previous conversation
            
        Returns:
            Generated response
        """
        full_prompt = ""
        
        if 'system_prompt' in self.config:
            full_prompt += f"System: {self.config['system_prompt']}\n\n"
        
        if conversation_history:
            for msg in conversation_history[-10:]:
                role = msg.get('role', 'user')
                content = msg.get('content', '')
                full_prompt += f"{role.capitalize()}: {content}\n\n"
        
        full_prompt += f"User: {prompt}\n\nAssistant:"
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": full_prompt,
                    "stream": False,
                    "options": {
                        "temperature": self.temperature,
                        "num_predict": self.max_tokens
                    }
                },
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '')
            else:
                return f"Error: Ollama returned status {response.status_code}"
                
        except Exception as e:
            return f"Error generating response: {str(e)}"
