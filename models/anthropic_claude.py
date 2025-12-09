#!/usr/bin/env python3
"""
Anthropic Claude Model Interface
Supports Claude Sonnet 4.5, Claude Opus, and other Claude models
"""

import os
import json
from typing import List, Dict, Optional


class ClaudeModel:
    """Interface for Anthropic Claude models"""
    
    def __init__(self, config: Dict):
        """
        Initialize Claude model
        
        Args:
            config: Configuration dict
        """
        self.config = config
        self.api_key = config.get('api_key') or os.getenv('ANTHROPIC_API_KEY') or os.getenv('CLAUDE_API_KEY')
        self.model = config.get('model', 'claude-sonnet-4.5')
        self.temperature = config.get('temperature', 0.7)
        self.max_tokens = config.get('max_tokens', 2000)
        
        if not self.api_key:
            raise ValueError("Anthropic API key not found. Set ANTHROPIC_API_KEY or CLAUDE_API_KEY environment variable.")
        
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Anthropic client"""
        try:
            from anthropic import Anthropic
            self.client = Anthropic(api_key=self.api_key)
            
            # Map model names to official API names
            self.model_mapping = {
                'claude-sonnet-4.5': 'claude-sonnet-4.5-20250101',
                'claude-sonnet-3.5': 'claude-3-5-sonnet-20241022',
                'claude-opus-4': 'claude-opus-4-20250101',
                'claude-opus-3': 'claude-3-opus-20240229',
                'claude-haiku-3': 'claude-3-haiku-20240307',
                'sonnet-4.5': 'claude-sonnet-4.5-20250101',
                'sonnet-3.5': 'claude-3-5-sonnet-20241022',
                'opus-4': 'claude-opus-4-20250101',
                'opus-3': 'claude-3-opus-20240229'
            }
            
        except ImportError:
            raise ImportError("anthropic package not installed. Run: pip install anthropic")
    
    def _get_model_name(self) -> str:
        """Get the official API model name"""
        model_key = self.model.lower()
        return self.model_mapping.get(model_key, 'claude-sonnet-4.5-20250101')
    
    def generate(self, prompt: str, conversation_history: List[Dict] = None) -> str:
        """
        Generate response from Claude
        
        Args:
            prompt: User prompt
            conversation_history: Previous conversation
            
        Returns:
            Generated response
        """
        try:
            # Build messages list
            messages = []
            
            # Add conversation history
            if conversation_history:
                for msg in conversation_history[-10:]:  # Last 10 messages
                    if msg.get('role') in ['user', 'assistant']:
                        messages.append({
                            "role": msg['role'],
                            "content": msg['content']
                        })
            
            # Add current prompt
            messages.append({
                "role": "user",
                "content": prompt
            })
            
            # Get system prompt
            system_prompt = self.config.get('system_prompt', '')
            
            # Create message
            response = self.client.messages.create(
                model=self._get_model_name(),
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                system=system_prompt,
                messages=messages
            )
            
            return response.content[0].text
            
        except Exception as e:
            print(f"[Error] Claude generation failed: {e}")
            return f"Error generating response: {str(e)}"
    
    def generate_stream(self, prompt: str, conversation_history: List[Dict] = None):
        """
        Generate streaming response from Claude
        
        Args:
            prompt: User prompt
            conversation_history: Previous conversation
            
        Yields:
            Response chunks
        """
        try:
            # Build messages list
            messages = []
            
            if conversation_history:
                for msg in conversation_history[-10:]:
                    if msg.get('role') in ['user', 'assistant']:
                        messages.append({
                            "role": msg['role'],
                            "content": msg['content']
                        })
            
            messages.append({
                "role": "user",
                "content": prompt
            })
            
            system_prompt = self.config.get('system_prompt', '')
            
            # Stream response
            with self.client.messages.stream(
                model=self._get_model_name(),
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                system=system_prompt,
                messages=messages
            ) as stream:
                for text in stream.text_stream:
                    yield text
                    
        except Exception as e:
            yield f"Error generating response: {str(e)}"
