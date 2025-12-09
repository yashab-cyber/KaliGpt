#!/usr/bin/env python3
"""
Mistral Model Interface
"""

import os
import requests
from typing import List, Dict, Optional
import json


class MistralModel:
    """Interface for Mistral AI models"""
    
    def __init__(self, config: Dict):
        """
        Initialize Mistral model
        
        Args:
            config: Configuration dict
        """
        self.config = config
        self.api_key = config.get('api_key') or os.getenv('MISTRAL_API_KEY')
        self.model = config.get('model', 'mistral-medium')
        self.temperature = config.get('temperature', 0.7)
        self.max_tokens = config.get('max_tokens', 2000)
        self.base_url = config.get('base_url', 'https://api.mistral.ai/v1')
        
        # Can use via Ollama as well (local)
        self.use_ollama = config.get('use_ollama', False)
        
        if not self.use_ollama and not self.api_key:
            print("[Warning] Mistral API key not found. Will try to use local Ollama.")
            self.use_ollama = True
    
    def generate(self, prompt: str, conversation_history: List[Dict] = None) -> str:
        """
        Generate response from Mistral
        
        Args:
            prompt: User prompt
            conversation_history: Previous conversation
            
        Returns:
            Generated response
        """
        if self.use_ollama:
            return self._generate_ollama(prompt, conversation_history)
        else:
            return self._generate_api(prompt, conversation_history)
    
    def _generate_api(self, prompt: str, conversation_history: List[Dict] = None) -> str:
        """Generate using Mistral API"""
        messages = []
        
        if 'system_prompt' in self.config:
            messages.append({
                "role": "system",
                "content": self.config['system_prompt']
            })
        
        if conversation_history:
            messages.extend(conversation_history)
        
        messages.append({
            "role": "user",
            "content": prompt
        })
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": messages,
                    "temperature": self.temperature,
                    "max_tokens": self.max_tokens
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                return f"Error: API returned status {response.status_code}"
                
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def _generate_ollama(self, prompt: str, conversation_history: List[Dict] = None) -> str:
        """Generate using local Ollama"""
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
                "http://localhost:11434/api/generate",
                json={
                    "model": "mistral",
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
            return f"Error: {str(e)}"
