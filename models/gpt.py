#!/usr/bin/env python3
"""
OpenAI/GPT Model Interface
"""

import os
from typing import List, Dict, Optional


class GPTModel:
    """Interface for OpenAI GPT models"""
    
    def __init__(self, config: Dict):
        """
        Initialize GPT model
        
        Args:
            config: Configuration dict
        """
        self.config = config
        self.api_key = config.get('api_key') or os.getenv('OPENAI_API_KEY')
        self.model = config.get('model', 'gpt-5.1')
        self.temperature = config.get('temperature', 0.7)
        self.max_tokens = config.get('max_tokens', 4000)
        
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
        
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize OpenAI client"""
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key)
        except ImportError:
            raise ImportError("openai package not installed. Run: pip install openai")
    
    def generate(self, prompt: str, conversation_history: List[Dict] = None) -> str:
        """
        Generate response from GPT
        
        Args:
            prompt: User prompt
            conversation_history: Previous conversation
            
        Returns:
            Generated response
        """
        messages = []
        
        # Add system message
        if 'system_prompt' in self.config:
            messages.append({
                "role": "system",
                "content": self.config['system_prompt']
            })
        
        # Add conversation history
        if conversation_history:
            messages.extend(conversation_history)
        
        # Add current prompt
        messages.append({
            "role": "user",
            "content": prompt
        })
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def stream_generate(self, prompt: str, conversation_history: List[Dict] = None):
        """
        Stream response from GPT
        
        Args:
            prompt: User prompt
            conversation_history: Previous conversation
            
        Yields:
            Response chunks
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
        
        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            yield f"Error: {str(e)}"
