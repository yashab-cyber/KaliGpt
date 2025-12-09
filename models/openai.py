#!/usr/bin/env python3
"""
OpenAI-Compatible API Model Interface
For services that use OpenAI's API format (e.g., Azure OpenAI, local LLM servers)
"""

import os
import requests
from typing import List, Dict, Optional


class OpenAICompatibleModel:
    """Interface for OpenAI-compatible APIs"""
    
    def __init__(self, config: Dict):
        """
        Initialize OpenAI-compatible model
        
        Args:
            config: Configuration dict
        """
        self.config = config
        self.api_key = config.get('api_key') or os.getenv('OPENAI_API_KEY')
        self.base_url = config.get('base_url', 'https://api.openai.com/v1')
        self.model = config.get('model', 'gpt-3.5-turbo')
        self.temperature = config.get('temperature', 0.7)
        self.max_tokens = config.get('max_tokens', 2000)
    
    def generate(self, prompt: str, conversation_history: List[Dict] = None) -> str:
        """
        Generate response
        
        Args:
            prompt: User prompt
            conversation_history: Previous conversation
            
        Returns:
            Generated response
        """
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
        
        headers = {
            "Content-Type": "application/json"
        }
        
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
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
                return f"Error: API returned status {response.status_code}: {response.text}"
                
        except Exception as e:
            return f"Error generating response: {str(e)}"
