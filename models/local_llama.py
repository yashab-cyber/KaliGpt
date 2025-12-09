#!/usr/bin/env python3
"""
Local LLaMA Model Interface (via Ollama)
"""

import requests
from typing import List, Dict, Optional
import json


class LocalLlamaModel:
    """Interface for local LLaMA models via Ollama"""
    
    def __init__(self, config: Dict):
        """
        Initialize Local LLaMA model
        
        Args:
            config: Configuration dict
        """
        self.config = config
        self.model = config.get('model', 'llama2')
        self.base_url = config.get('base_url', 'http://localhost:11434')
        self.temperature = config.get('temperature', 0.7)
        self.max_tokens = config.get('max_tokens', 2000)
        
        # Check if Ollama is running
        if not self._check_ollama():
            print("[Warning] Ollama not detected. Make sure it's running: ollama serve")
    
    def _check_ollama(self) -> bool:
        """Check if Ollama is running"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def generate(self, prompt: str, conversation_history: List[Dict] = None) -> str:
        """
        Generate response from LLaMA
        
        Args:
            prompt: User prompt
            conversation_history: Previous conversation
            
        Returns:
            Generated response
        """
        # Build full prompt with history
        full_prompt = ""
        
        if 'system_prompt' in self.config:
            full_prompt += f"System: {self.config['system_prompt']}\n\n"
        
        if conversation_history:
            for msg in conversation_history[-10:]:  # Last 10 messages
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
                
        except requests.exceptions.ConnectionError:
            return "Error: Cannot connect to Ollama. Make sure it's running (ollama serve)"
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def stream_generate(self, prompt: str, conversation_history: List[Dict] = None):
        """
        Stream response from LLaMA
        
        Args:
            prompt: User prompt
            conversation_history: Previous conversation
            
        Yields:
            Response chunks
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
                    "stream": True,
                    "options": {
                        "temperature": self.temperature,
                        "num_predict": self.max_tokens
                    }
                },
                stream=True,
                timeout=120
            )
            
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line)
                    if 'response' in chunk:
                        yield chunk['response']
                        
        except Exception as e:
            yield f"Error: {str(e)}"
    
    def list_models(self) -> List[str]:
        """List available Ollama models"""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                data = response.json()
                return [model['name'] for model in data.get('models', [])]
        except:
            pass
        return []
